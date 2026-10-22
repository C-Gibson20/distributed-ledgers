// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.17;

import "./interfaces/IERC20.sol";

contract ERC20 is IERC20Metadata {
    address immutable public minter;
    string private _name;
    string private _symbol;
    uint256 private _totalSupply;
    mapping(address => uint256) private _balances;
    mapping(address => mapping(address => uint256)) private _allowances;
    
    constructor (string memory name_, string memory symbol_) {
        minter = msg.sender;
        _name = name_;
        _symbol = symbol_; 
    }

    function name() external view returns (string memory) {
        // The name of the token
        return _name;
    }

    function symbol() external view returns (string memory) {
        // The symbol of the token
        return _symbol;
    }

    function decimals() external pure returns (uint8) {
        // The number of decimals by which the amounts are scaled
        return 18;
    }

    function totalSupply() external view returns (uint256) {
        // Retrieve the total number of tokens in existence
        return _totalSupply;
    }

    function balanceOf(address account) external view returns (uint256) {
        // Retrieve the balance of a user
        return _balances[account];
    }

    function transfer(address to, uint256 amount) external returns (bool) {
        // Transfer tokens to another user
        if (_balances[msg.sender] < amount) {
            revert("insufficient balance");
        }
        _balances[msg.sender] -= amount;
        _balances[to] += amount;
        emit Transfer(msg.sender, to, amount);
        return true;
    }

    function allowance(address owner, address spender)
        external
        view
        returns (uint256)
    {
        // Retrieve the number of tokens that a user is allowed to 
        // transfer on another's behalf
        return _allowances[owner][spender];
    }

    function approve(address spender, uint256 amount) external returns (bool) {
        // Approve another user to transfer tokens on the user's behalf
        _allowances[msg.sender][spender] = amount;
        emit Approval(msg.sender, spender, amount);
        return true;
    }

    function transferFrom(
        address from,
        address to,
        uint256 amount
    ) external returns (bool) {
        //  Transfer tokens on another user's behalf
        if (_allowances[from][msg.sender] < amount) {
            revert("insufficient allowance");
        }
        if (_balances[from] < amount) {
            revert("insufficient balance");
        }
        _balances[from] -= amount;
        _balances[to] += amount;
        _allowances[from][msg.sender] -= amount;
        emit Transfer(from, to, amount);
        return true;
    }

    function mint(address to, uint256 amount) external {
        // Mint new tokens and assign them to a user
        if (msg.sender != minter) {
            revert("only minter can mint");
        }
        _totalSupply += amount;
        _balances[to] += amount;
        emit Transfer(address(0), to, amount);
    }
}
