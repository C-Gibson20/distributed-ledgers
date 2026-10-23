# Principle of Distributed Ledgers, Tutorial 2

The goal of this tutorial is to implement an ERC-20 token and an ERC-721 token that can be bought using the ERC-20 token.

Please refer to the full tutorial for more details.

## Status

| Section | Status |
|---|---|
| 1. ERC-20 token | Implemented, 10/10 tests passing |
| 2. Deployment | Deployed and verified on OP Mainnet |
| 3. ERC-721 token | Implemented, 12/12 tests passing |
| 4. Bonus (ERC-165, operators, `safeTransferFrom`) | Implemented, 9/9 tests passing |

Run the tests with:

```
forge test
```

## Deployment (OP Mainnet)

The ERC-20 contract is deployed and its source is verified on Optimistic Etherscan.

Deployed from an encrypted Foundry keystore (`cast wallet import <ACCOUNT_NAME> --interactive`) rather than passing the private key on the command line:

```
forge create \
  --account <ACCOUNT_NAME> \
  --rpc-url <RPC_URL> \
  --chain optimism \
  --broadcast \
  --verify \
  --etherscan-api-key <ETHERSCAN_API_KEY> \
  src/ERC20.sol:ERC20 \
  --constructor-args "<TOKEN_NAME>" "<TOKEN_SYMBOL>"
```
