"""Explore the content and structure of mempool.json."""

from pathlib import Path

from .storage import load_json_file


def inspect_mempool(mempool):
    # Number of transactions in the mempool
    num_transactions = len(mempool)
    print(f"\nNumber of transactions in the mempool: {num_transactions}")

    # Properties of any transaction
    if num_transactions > 0:
        first_transaction = mempool[0]
        print(f"\nProperties of the first transaction:")
        for key in first_transaction.keys():
            print(f"  {key}")


def transactions_after_timestamp(mempool, timestamp):
    # Filter transactions after a specific timestamp
    filtered_transactions = [tx for tx in mempool if tx['lock_time'] <= timestamp]

    print(f"\nNumber of transactions with lock time before or equal to timestamp {timestamp}: {len(filtered_transactions)}")

    # print(f"\nTransactions after timestamp {timestamp}:")
    # for tx in filtered_transactions:
    #     print(f"  Transaction ID: {tx['signature']}, Timestamp: {tx['lock_time']}")


def main():
    project_root = Path(__file__).resolve().parent.parent
    mempool_file_path = project_root / 'mempool.json'
    print("Loading mempool from mempool.json...")
    mempool = load_json_file(mempool_file_path)

    print("Mempool loaded successfully.")

    # Inspect the mempool
    inspect_mempool(mempool)

    timestamp = 1697413810
    transactions_after_timestamp(mempool, timestamp) 

if __name__ == "__main__":
    main()
