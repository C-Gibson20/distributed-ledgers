"""Block implementation for the blockchain."""
from .merkle import build_merkle_tree
from .transactions import get_eligible_transactions


def create_block_header(height, previous_block_header_hash, timestamp, transactions_merkle_root, miner, nonce, difficulty, transactions_count):
    """Create a block header with the given parameters."""
    return {
        "height": height,
        "previous_block_header_hash": previous_block_header_hash,
        "timestamp": timestamp,
        "transactions_merkle_root": transactions_merkle_root,
        "miner": miner,
        "nonce": nonce,
        "difficulty": difficulty,
        "transactions_count": transactions_count
    }


def create_block_transactions(mempool, timestamp):
    """Create a list of transactions for the block based on the mempool and timestamp."""
    return get_eligible_transactions(mempool, timestamp)


def create_block(height, previous_block_header_hash, timestamp, miner, nonce, difficulty, transactions):
    """Create a block from its header data and an already selected transaction list."""
    transactions_merkle_root = build_merkle_tree(transactions)
    transactions_count = len(transactions)

    block_header = create_block_header(height, previous_block_header_hash, timestamp, transactions_merkle_root, miner, nonce, difficulty, transactions_count)

    return {
        "header": block_header,
        "transactions": transactions
    }