"""Demonstrate wallet payments and static-analysis improvements."""

import hashlib
import hmac
import os
import secrets
import tempfile
from datetime import datetime

GATEWAY_SECRET = os.environ.get("GATEWAY_SECRET")
WALLET_PIN = os.environ.get("WALLET_PIN")
PIN_SALT = secrets.token_bytes(16)
wallet = {"balance": 0.0, "daily_limit": 1000}
transactions = []


def hash_pin(pin):
    """Derive a PIN hash with PBKDF2 and a process-local random salt."""
    return hashlib.pbkdf2_hmac(
        "sha256", pin.encode(), PIN_SALT, 600_000
    ).hex()


def add_money(amount, source="UPI", log=None):
    """Credit a positive amount and optionally append it to a caller log."""
    if amount <= 0:
        return False
    wallet["balance"] += amount
    transactions.append({"type": "credit", "amount": amount, "party": source,
                         "time": datetime.now().isoformat()})
    if log is not None:
        log.append(amount)
    return True


def set_daily_limit(new_limit):
    """Set the positive payment limit used by this wallet demo."""
    if new_limit <= 0:
        raise ValueError("Daily limit must be positive")
    wallet["daily_limit"] = new_limit


def pay_merchant(merchant, amount, pin):
    """Authorize a positive payment within the balance and payment limit."""
    if WALLET_PIN is None or not hmac.compare_digest(
        hash_pin(pin), hash_pin(WALLET_PIN)
    ):
        print("Wrong PIN for payment to", merchant)
        return False
    if (amount <= 0 or amount > wallet["balance"]
            or amount > wallet["daily_limit"]):
        print("Payment to", merchant, "declined")
        return False
    wallet["balance"] -= amount
    transactions.append({"type": "debit", "amount": amount, "party": merchant,
                         "time": datetime.now().isoformat()})
    return True


def mini_statement(count=3):
    """Print the most recent transactions for a positive count."""
    if count <= 0:
        return
    for entry in transactions[-count:]:
        print(entry["type"], entry["amount"], entry["party"])


def cashback_for(amount):
    """Return the uniform two-percent cashback amount."""
    return round(amount * 0.02, 2)


def check_gateway(secret):
    """Compare a gateway key against the configured secret."""
    return GATEWAY_SECRET is not None and hmac.compare_digest(
        secret, GATEWAY_SECRET
    )


def receipt_path():
    """Create a receipt file securely; the caller must delete it."""
    # Helper kept for the lab: not called by the demo
    with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as receipt:
        return receipt.name


def main():
    """Run the wallet demonstration with credentials from the environment."""
    if not WALLET_PIN or not GATEWAY_SECRET:
        raise ValueError("Set WALLET_PIN and GATEWAY_SECRET before running")
    otp = secrets.randbelow(900000) + 100000
    print("OTP sent:", otp)
    add_money(2000)
    add_money(500, "Card")
    add_money(-10)
    set_daily_limit(1500)
    pay_merchant("Coffee Corner", 180, WALLET_PIN)
    pay_merchant("Book Store", 5000, WALLET_PIN)
    pay_merchant("Grocery Mart", 350, WALLET_PIN + "x")
    pay_merchant("Pharmacy", 420, WALLET_PIN)
    mini_statement()
    print("Cashback on 420:", cashback_for(420))
    print("Gateway check:", check_gateway("wrong")) # should be False
    print("Final balance: Rs.", wallet["balance"])
    credit_amounts=[t["amount"] for t in transactions if t["type"] == "credit"]
    print("Total credited:",sum(credit_amounts))
if __name__ == "__main__":
    main()
