"""Merkle tree implementation for the blockchain."""
from .serialization import hash_transaction, hash_merkle_node, NULL_HASH


def build_node_hashes(transactions):
    """Build a list of hashes for the given transactions."""
    return [hash_transaction(tx) for tx in transactions]


def build_merkle_node(left_hash, right_hash):
    """Build a Merkle node by hashing the concatenation of two child hashes."""
    return hash_merkle_node(left_hash, right_hash)


def build_merkle_tree(transactions):
    """Build a Merkle tree from a list of transactions and return the root hash."""
    if not transactions:
        return None

    # Build the initial list of hashes for the transactions
    current_level_hashes = build_node_hashes(transactions)

    # Continue building the tree until we reach the root
    while len(current_level_hashes) > 1:
        next_level_hashes = []
        for i in range(0, len(current_level_hashes), 2):
            left_hash = current_level_hashes[i]
            right_hash = current_level_hashes[i + 1] if i + 1 < len(current_level_hashes) else NULL_HASH
            parent_hash = build_merkle_node(left_hash, right_hash)
            next_level_hashes.append(parent_hash)
        current_level_hashes = next_level_hashes

    # The last remaining hash is the Merkle root
    return current_level_hashes[0]
