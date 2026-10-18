"""Helpers for loading and saving the chain, and producing a mined block."""

import argparse
from pathlib import Path

from .accounts import calculate_balances
from .blocks import create_block, create_block_transactions
from .mining import mine_block
from .storage import load_json_file, save_json_file


def difficulty_for_height(height):
    """Return the scheduled difficulty: +1 every 50 blocks, capped at 6."""
    return min(height // 50 + 1, 6)


def produce_block(blockchain, mempool, miner):
    """Produce a block using the next scheduled timestamp and difficulty."""
    if not blockchain:
        raise ValueError("Cannot produce a block without an existing chain.")
    if not isinstance(miner, str) or not miner.startswith('0x') or len(miner) != 42:
        raise ValueError("Miner must be a 0x-prefixed 20-byte address.")
    try:
        int(miner[2:], 16)
    except ValueError as exc:
        raise ValueError("Miner must be a 0x-prefixed 20-byte address.") from exc

    previous_header = blockchain[-1]['header']
    previous_block_header_hash = previous_header['hash']
    height = previous_header['height'] + 1
    timestamp = previous_header['timestamp'] + 10
    difficulty = difficulty_for_height(height)

    # Create the list of transactions for the new block
    transactions = create_block_transactions(mempool, timestamp)

    # Create the block with the header and transactions
    block = create_block(height, previous_block_header_hash, timestamp, miner, 0, difficulty, transactions)

    # Mine the block to find a valid nonce and hash
    mine_block(block['header'], difficulty)

    return block


def update_blockchain(blockchain, new_block, output_file_path):
    """Update the blockchain with a new block and save it to a file."""
    blockchain.append(new_block)
    save_json_file(blockchain, output_file_path)


def produce_and_save_block(
    blockchain_file_path,
    mempool_file_path,
    output_file_path,
    miner,
):
    """Load the inputs, produce a block, append it, and save the updated chain."""
    blockchain = load_json_file(blockchain_file_path)
    mempool = load_json_file(mempool_file_path)

    new_block = produce_block(blockchain, mempool, miner)
    update_blockchain(blockchain, new_block, output_file_path)
    new_balances = calculate_balances(blockchain)  # Update balances after adding the new block

    return new_block, new_balances


def main(argv=None):
    """Parse command-line options and produce/save one block."""
    project_root = Path(__file__).resolve().parent.parent
    parser = argparse.ArgumentParser(description="Produce and save a mined block.")
    parser.add_argument("--blockchain", type=Path, default=project_root / 'blockchain.json')
    parser.add_argument("--mempool", type=Path, default=project_root / 'mempool.json')
    parser.add_argument("--output", type=Path, default=project_root / 'blockchain_updated.json')
    parser.add_argument("--miner", required=True, help="Miner's 0x-prefixed address")
    args = parser.parse_args(argv)

    new_block, new_balances = produce_and_save_block(
        args.blockchain,
        args.mempool,
        args.output,
        args.miner,
    )
    print(f"Saved block {new_block['header']['height']} to {args.output}")
    print(f"Block hash: {new_block['header']['hash']}")
    print(f"Updated balances:\n    Number of accounts: {len(new_balances)}\n    Miner's new balance: {new_balances.get(args.miner, 0)}")

if __name__ == "__main__":
    main()
