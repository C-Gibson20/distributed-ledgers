"""Merkle-tree proof implementation for the blockchain."""

import argparse
from pathlib import Path

from .merkle import build_merkle_node
from .serialization import hash_transaction, NULL_HASH
from .storage import load_json_file


def generate_merkle_proof(transactions, target_index):
    """Generate a Merkle proof for the transaction at the given index."""
    if target_index < 0 or target_index >= len(transactions):
        raise ValueError("Target index is out of bounds.")

    # Build the initial list of hashes for the transactions
    current_level_hashes = [hash_transaction(tx) for tx in transactions]
    proof = []

    # Continue building the tree until we reach the root
    while len(current_level_hashes) > 1:
        sibling_index = (
            target_index - 1 if target_index % 2 else target_index + 1
        )
        if sibling_index < len(current_level_hashes):
            proof.append(current_level_hashes[sibling_index])
        else:
            proof.append(NULL_HASH)

        next_level_hashes = []
        for i in range(0, len(current_level_hashes), 2):
            left_hash = current_level_hashes[i]
            right_hash = current_level_hashes[i + 1] if i + 1 < len(current_level_hashes) else NULL_HASH
            parent_hash = build_merkle_node(left_hash, right_hash)
            next_level_hashes.append(parent_hash)

        current_level_hashes = next_level_hashes
        target_index //= 2

    return proof 


def verify_merkle_proof(transaction, proof, merkle_root):
    """Verify a Merkle proof for a given transaction and Merkle root."""
    current_hash = hash_transaction(transaction)

    for sibling_hash in proof:
        current_hash = build_merkle_node(current_hash, sibling_hash)
        
    return current_hash == merkle_root


def generate_and_verify_block_proof(blockchain_file_path, transaction_index, block_index=-1):
    """Generate and verify an inclusion proof for a transaction in a block."""
    blockchain = load_json_file(blockchain_file_path)

    if not blockchain:
        raise ValueError("The blockchain is empty.")

    if not -len(blockchain) <= block_index < len(blockchain):
        raise IndexError("Block index is out of range.")

    block = blockchain[block_index]
    transactions = block['transactions']
    if not transactions:
        raise ValueError("The selected block has no transactions to prove.")

    if not 0 <= transaction_index < len(transactions):
        raise IndexError("Transaction index is out of range.")

    transaction = transactions[transaction_index]
    proof = generate_merkle_proof(transactions, transaction_index)
    merkle_root = block['header']['transactions_merkle_root']
    is_valid = verify_merkle_proof(transaction, proof, merkle_root)
    return transaction, proof, is_valid


def main(argv=None):
    """Parse command-line options and verify a transaction inclusion proof."""
    project_root = Path(__file__).resolve().parent.parent
    parser = argparse.ArgumentParser(description="Generate and verify a Merkle inclusion proof.")
    parser.add_argument(
        "--blockchain",
        type=Path,
        default=project_root / 'blockchain_updated.json',
    )
    parser.add_argument("--block-index", type=int, default=-1, help="Block index (default: last block)")
    parser.add_argument("--transaction-index", required=True, type=int)
    args = parser.parse_args(argv)

    transaction, proof, is_valid = generate_and_verify_block_proof(
        args.blockchain,
        args.transaction_index,
        args.block_index,
    )

    print(f"Transaction: {transaction}")
    print(f"Transaction index: {args.transaction_index}")
    print(f"Merkle proof: {proof}")
    print(f"Proof valid: {is_valid}")


if __name__ == "__main__":
    main()

    
