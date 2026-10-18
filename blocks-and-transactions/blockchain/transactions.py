"""Transaction-related functions for the blockchain."""
import argparse
import hashlib
from pathlib import Path

from ecdsa import SigningKey, VerifyingKey, util

from .serialization import serialize_transaction
from .storage import load_json_file, save_json_file


def _is_address(value):
    """Return whether value is a 20-byte hexadecimal address."""
    if not value.startswith("0x") or len(value) != 42:
        return False
    try:
        int(value[2:], 16)
    except ValueError:
        return False
    return True


def verify_transaction_signature(transaction):
    """Return whether a transaction's signature matches its sender and contents."""
    try:
        public_key_hex, signature_hex = transaction["signature"].split(",")
        public_key_der = bytes.fromhex(public_key_hex.removeprefix("0x"))
        signature_der = bytes.fromhex(signature_hex.removeprefix("0x"))

        # The signature covers the transaction fields except the signature itself.
        unsigned_transaction = {
            key: value
            for key, value in transaction.items()
            if key != "signature"
        }
        serialized = serialize_transaction(unsigned_transaction)
        transaction_hash = hashlib.sha256(serialized.encode()).digest()

        # Verify the signature using the public key.
        public_key = VerifyingKey.from_der(public_key_der)
        public_key.verify_digest(
            signature_der,
            transaction_hash,
            sigdecode=util.sigdecode_der,
        )

        # Confirm that the public key belongs to the claimed sender address.
        derived_sender = "0x" + hashlib.sha256(public_key_der).digest()[-20:].hex()
        return derived_sender.lower() == transaction["sender"].lower()
    except Exception:
        return False


def create_signed_transaction(sender, receiver, amount, transaction_fee, lock_time, private_key_der):
    """Build and sign a transaction."""
    transaction = {
        "amount": amount,
        "lock_time": lock_time,
        "receiver": receiver,
        "sender": sender,
        "transaction_fee": transaction_fee,
    }

    serialized = serialize_transaction(transaction)
    transaction_digest = hashlib.sha256(serialized.encode()).digest()

    # Sign the transaction with the private key.
    signing_key = SigningKey.from_der(private_key_der)
    public_key_der = signing_key.get_verifying_key().to_der()

    derived_sender = "0x" + hashlib.sha256(public_key_der).digest()[-20:].hex()
    if derived_sender.lower() != sender.lower():
        raise ValueError("The private key does not match the sender address.")

    signature_der = signing_key.sign_digest(
        transaction_digest,
        sigencode=util.sigencode_der,
    )
    transaction["signature"] = (
        f"0x{public_key_der.hex()},0x{signature_der.hex()}"
    )
    return transaction


def get_eligible_transactions(mempool, timestamp):
    """Get transactions from the mempool that are eligible for inclusion in a block based on the timestamp."""
    eligible_transactions = [tx for tx in mempool if tx['lock_time'] <= timestamp]
    valid_transactions = [
        tx for tx in eligible_transactions
        if verify_transaction_signature(tx)
    ]
    sorted_top_100_transactions = sorted(
        valid_transactions,
        key=lambda tx: tx['transaction_fee'],
        reverse=True,
    )[:100]
    return sorted_top_100_transactions


def main(argv=None):
    """Create a signed transaction and save it in an updated mempool file."""
    project_root = Path(__file__).resolve().parent.parent
    parser = argparse.ArgumentParser(description="Create and add a signed transaction to a mempool.")
    parser.add_argument("--sender", required=True, help="Sender address from keys.json")
    parser.add_argument("--receiver", required=True, help="Transaction receiver address")
    parser.add_argument("--amount", required=True, type=int, help="Amount to transfer")
    parser.add_argument("--fee", required=True, type=int, help="Transaction fee")
    parser.add_argument("--lock-time", required=True, type=int, help="Earliest block timestamp for inclusion")
    parser.add_argument("--keys", type=Path, default=project_root / "keys.json")
    parser.add_argument("--mempool", type=Path, default=project_root / "mempool.json")
    parser.add_argument("--output", type=Path, default=project_root / "mempool_updated.json")
    args = parser.parse_args(argv)

    if not _is_address(args.sender):
        parser.error("--sender must be a 0x-prefixed 20-byte hexadecimal address")
    if not _is_address(args.receiver):
        parser.error("--receiver must be a 0x-prefixed 20-byte hexadecimal address")
    if args.amount <= 0:
        parser.error("--amount must be greater than zero")
    if args.fee < 0:
        parser.error("--fee cannot be negative")
    if args.lock_time < 0:
        parser.error("--lock-time cannot be negative")

    keys = load_json_file(args.keys)
    private_key_hex = next(
        (key for address, key in keys.items() if address.lower() == args.sender.lower()),
        None,
    )
    if private_key_hex is None:
        parser.error("No private key was found for the sender address in the keys file")

    try:
        private_key_der = bytes.fromhex(private_key_hex.removeprefix("0x"))
    except ValueError:
        parser.error("The sender's private key is not valid hexadecimal data")

    transaction = create_signed_transaction(
        args.sender,
        args.receiver,
        args.amount,
        args.fee,
        args.lock_time,
        private_key_der,
    )

    mempool = load_json_file(args.mempool)
    mempool.append(transaction)
    save_json_file(mempool, args.output)

    print(f"Signed transaction created for {args.sender}.")
    print(f"Updated mempool saved to {args.output} ({len(mempool)} transactions).")


if __name__ == "__main__":
    main()
