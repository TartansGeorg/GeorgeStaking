// SPDX-License-Identifier: GPL-3.0

pragma solidity >=0.7.0 <0.9.0;

//import "@openzeppelin/contracts/token/ERC20/ERC20.sol";
import "OpenZeppelin/openzeppelin-contracts@4.6.0/contracts/token/ERC20/ERC20.sol";

/**
 * @title Staking1
 * @dev Stake and earn rewrads
 */
contract Staking1 is ERC20("GeorgeCoin", "GEC"){
    mapping (address => uint256) public balances;
    mapping (address => uint256) private stakeTime;
    address public manager;

    constructor() {
        manager = msg.sender;
        _mint(address(this), 1000000000000000000000000);
    }

    function stake() public payable {
        balances[msg.sender] += msg.value;
        stakeTime[msg.sender] = block.number;
    }

    function unstake(uint amount) public {
        require (amount <= balances[msg.sender], 'Cannot withdraw more than you staked');
        balances[msg.sender] -= amount;
        stakeTime[msg.sender] = 0;
        payable(msg.sender).transfer(amount);
    }

    function seeReward() public view returns (uint256) {
        if (stakeTime[msg.sender] > 0) {
            return (block.number - stakeTime[msg.sender]) * balances[msg.sender] / 1000;
        }
        return 0;
    }

    function claimReward() public {
        require(stakeTime[msg.sender] > 0, "You have nothing staked");
        require(block.number >= stakeTime[msg.sender] + 10, "Rewards can only be claimed after 10 blocks");
        uint256 reward = (block.number - stakeTime[msg.sender]) * balances[msg.sender] / 1000;
        require(balanceOf(address(this)) > reward, "All rewards have been paid already.");
        stakeTime[msg.sender] = block.number;
        _transfer(address(this), msg.sender, reward);
    }

    function georgeCoinBalance() public view returns (uint256) {
        return balanceOf(msg.sender);
    }
}