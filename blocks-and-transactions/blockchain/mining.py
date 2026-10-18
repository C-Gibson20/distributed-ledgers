"""Mining functions for the blockchain."""
from .serialization import strip_prefix, hash_block_header


def mine_block(block_header, difficulty):
    """Simulate the mining process by finding a nonce that satisfies the difficulty requirement."""
    from .serialization import hash_block_header

    nonce = 0
    while True:
        # Update the block header with the current nonce
        block_header['nonce'] = nonce
        # Hash the block header
        block_hash = hash_block_header(block_header)
        block_hash_no_prefix = strip_prefix(block_hash)  # Remove the '0x' prefix for comparison
        # Check if the hash meets the difficulty requirement (e.g., starts with a certain number of zeros)
        if block_hash_no_prefix.startswith('0' * difficulty):
            block_header['hash'] = block_hash  # Store the valid hash in the block header
            return nonce, block_hash
        nonce += 1