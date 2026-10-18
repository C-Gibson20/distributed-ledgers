"""Serialization functions for the blockchain."""
import hashlib

NULL_HASH = "0x" + "0" * 64  # Represents a null hash for empty nodes in the Merkle tree


def strip_prefix(hex_string):
    """Strip the '0x' prefix from a hexadecimal string."""
    return hex_string[2:] if hex_string.startswith("0x") else hex_string


def hash_without_prefix(data):
    """Hash arbitrary data using SHA-256."""
    return hashlib.sha256(data.encode()).hexdigest()


def hash_with_prefix(data):
    """Hash data with a 0x prefix using SHA-256."""
    return "0x" + hash_without_prefix(data)


def serialize_transaction(transaction):
    """Serialize a transaction into a comma separated string."""
    # Sort keys alphabetically and join values with commas
    return ','.join(str(transaction[key]) for key in sorted(transaction.keys()))


def hash_transaction(transaction):
    """Hash a transaction using SHA-256."""
    return hash_with_prefix(serialize_transaction(transaction))


def hash_merkle_node(left_hash, right_hash):
    """Hash a Merkle node by concatenating two child hashes and hashing the result."""
    # Sort lexicographically to ensure consistent ordering
    if left_hash > right_hash:
        left_hash, right_hash = right_hash, left_hash

    combined = left_hash + right_hash
    return hash_with_prefix(combined)


def serialize_block_header(block_header):
    """Serialize a block header into a comma separated string."""
    # Sort keys alphabetically and join values with commas
    return ','.join(str(block_header[key]) for key in sorted(block_header.keys()) if key != 'hash')  # Exclude the hash field from serialization


def hash_block_header(block_header):
    """Hash a block header using SHA-256."""
    return hash_with_prefix(serialize_block_header(block_header))
