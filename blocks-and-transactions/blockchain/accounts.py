"""Helpers for managing accounts in the blockchain."""

ZERO_ADDRESS = "0x" + "0" * 40 


def calculate_balances(blockchain):
    """Calculate the balances of all accounts based on the blockchain."""
    balances = {}
    for block in blockchain:
        block_fees = 0
        for transaction in block['transactions']:
            sender = transaction['sender']
            receiver = transaction['receiver']
            amount = transaction['amount']
            fee = transaction['transaction_fee']

            # Genesis transactions create funds from the zero address
            if sender != ZERO_ADDRESS:
                balances[sender] = balances.get(sender, 0) - amount - fee

            balances[receiver] = balances.get(receiver, 0) + amount
            block_fees += fee

        # Transaction fees go to the miner of this block
        if block_fees:
            miner = block['header']['miner']
            balances[miner] = balances.get(miner, 0) + block_fees

    return balances