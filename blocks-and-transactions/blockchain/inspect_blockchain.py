"""Explore the content and structure of blockchain.json."""

from pathlib import Path

from .storage import load_json_file


def inspect_blockchain(blockchain):
    # Number of blocks in the blockchain
    num_blocks = len(blockchain)
    print(f"\nNumber of blocks in the blockchain: {num_blocks}")

    # Properties of any block
    if num_blocks > 0:
        first_block = blockchain[0]
        print(f"\nProperties of the first block:")
        for key in first_block.keys():
            print(f"  {key}")

    # Properties of transactions in any block
    if num_blocks > 0 and 'transactions' in first_block:
        transactions = first_block['transactions']
        if len(transactions) > 0:
            first_transaction = transactions[0]
            print(f"\nProperties of the first transaction in the first block:")
            for key in first_transaction.keys():
                print(f"  {key}")


def inspect_last_block_header(blockchain):
    # Inspect the header of the last block in the blockchain
    if len(blockchain) > 0:
        last_block_header = blockchain[-1]['header']
        print(f"\nHeader of the last block:")
        for key, value in last_block_header.items():
            print(f"  {key}: {value}")


def main():
    project_root = Path(__file__).resolve().parent.parent
    blockchain_file_path = project_root / 'blockchain.json'
    print("Loading blockchain from blockchain.json...")
    blockchain = load_json_file(blockchain_file_path)

    print("Blockchain loaded successfully.")

    # Inspect the blockchain
    inspect_blockchain(blockchain)
    inspect_last_block_header(blockchain)


if __name__ == "__main__":
    main()
