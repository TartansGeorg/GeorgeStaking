// SPDX-License-Identifier: MIT

pragma solidity ^0.8.0;

//import "@openzeppelin/contracts/token/ERC20/ERC20.sol";
import "OpenZeppelin/openzeppelin-contracts@4.6.0/contracts/token/ERC20/ERC20.sol";

contract GeorgeCoin is ERC20("GeorgeCoin", "GEC"){

    constructor () {
        _mint(msg.sender, 1000000000000000000000000);
    }
}