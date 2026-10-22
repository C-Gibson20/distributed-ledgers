// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.17;

import "./interfaces/IERC20.sol";
import "./interfaces/IERC721.sol";
import "./interfaces/IERC721TokenReceiver.sol";
import "./libraries/StringUtils.sol";

contract ERC721 is IERC721Metadata {
    string private _name_;
    string private _symbol_;
    string private _baseUri;
    IERC20 immutable private _paymentToken;
    uint256 private _tokenPrice;
    uint256 private _nextTokenId = 1;
    mapping(uint256 => address) private _owners;
    mapping(address => uint256) private _balances;
    mapping(uint256 => address) private _tokenApprovals;
    mapping(address => mapping(address => bool)) private _operatorApprovals;

    constructor(
        string memory name_,
        string memory symbol_,
        string memory baseUri,
        IERC20 paymentToken,
        uint256 initialTokenPrice
    ) {
        _name_ = name_;
        _symbol_ = symbol_;
        _baseUri = baseUri;
        _paymentToken = paymentToken;
        _tokenPrice = initialTokenPrice;
    }

    function mint(address to) external {
        // Mint a new token and assign it to a user
        uint256 tokenId = _nextTokenId++;
        _owners[tokenId] = to;
        _balances[to]++;
        _paymentToken.transferFrom(msg.sender, address(0), _tokenPrice);
        _tokenPrice = (_tokenPrice * 11) / 10; 
        emit Transfer(address(0), to, tokenId);
    }

    function balanceOf(address _owner) external view returns (uint256) {
        // Retrieve the number of tokens that a user owns
        return _balances[_owner];
    }

    function ownerOf(uint256 _tokenId) external view returns (address) {
        // Retrieve the owner of a given token
        return _owners[_tokenId];
    }

    function transferFrom(
        address _from,
        address _to,
        uint256 _tokenId
    ) external {
        // Transfer a token to another address external wrapper
        _transfer(_from, _to, _tokenId);
    }

    function _transfer(address from, address to, uint256 tokenId) internal {
        // Transfer a token to another address internal function
        if (_owners[tokenId] != from) {
            revert("transfer from incorrect owner");
        }
        if (msg.sender != from && msg.sender != _tokenApprovals[tokenId] && !_operatorApprovals[from][msg.sender]) {
            revert("caller is not owner nor approved");
        }
        _owners[tokenId] = to;
        _balances[from]--;
        _balances[to]++;
        _tokenApprovals[tokenId] = address(0);
        emit Transfer(from, to, tokenId);

    }

    function approve(address _approved, uint256 _tokenId) external {
        // Approve another user to transfer a given token 
        // on the user's behalf
        address owner = _owners[_tokenId];
        if (msg.sender != owner && !_operatorApprovals[owner][msg.sender]) {
            revert("not authorized");
        }
        _tokenApprovals[_tokenId] = _approved;
        emit Approval(owner, _approved, _tokenId);
    }

    function getApproved(uint256 _tokenId) external view returns (address) {
        // Retrieve the user approved to transfer a given token
        return _tokenApprovals[_tokenId];
    }

    function name() external view returns (string memory _name) {
        // The name of the token
        return _name_;
    }

    function symbol() external view returns (string memory _symbol) {
        // The symbol of the token
        return _symbol_;
    }

    function tokenURI(uint256 _tokenId) external view returns (string memory) {
        // The URI of the given token
        return string.concat(_baseUri, StringUtils.toString(_tokenId));
    }

    // Bonus functions

    function supportsInterface(bytes4 interfaceID)
        external
        pure
        returns (bool)
    {
        // Retrieve whether the contract implements a given interface
        return interfaceID == type(IERC721).interfaceId;
    }

    function safeTransferFrom(
        address _from,
        address _to,
        uint256 _tokenId,
        bytes memory data
    ) external {
        // Transfer a token to another address, 
        // and call the onERC721Received function on the recipient if it is a contract
        // external wrapper
        _safeTransfer(_from, _to, _tokenId, data);
    }

    function safeTransferFrom(
        address _from,
        address _to,
        uint256 _tokenId
    ) external {
        // Transfer a token to another address, 
        // and call the onERC721Received function on the recipient if it is a contract
        // external wrapper
        _safeTransfer(_from, _to, _tokenId, "");
    }

    function _safeTransfer(
        address from,
        address to,
        uint256 tokenId,
        bytes memory data
    ) internal {
        // Transfer a token to another address, 
        // and call the onERC721Received function on the recipient if it is a contract
        // internal function
        _transfer(from, to, tokenId);
        if (to.code.length > 0) {
            bytes4 retval = IERC721TokenReceiver(to).onERC721Received(msg.sender, from, tokenId, data);
            if (retval != IERC721TokenReceiver.onERC721Received.selector) {
                revert("magic value not returned");
            }
        }
    }

    function setApprovalForAll(address _operator, bool _approved) external {
        // Approve another user to manage all tokens owned by the user
        _operatorApprovals[msg.sender][_operator] = _approved;
        emit ApprovalForAll(msg.sender, _operator, _approved);
    }

    function isApprovedForAll(address _owner, address _operator)
        external
        view
        returns (bool)
    {
        // Retrieve whether a user is approved to manage all tokens 
        // managed by another user
        return _operatorApprovals[_owner][_operator];
    }
}
