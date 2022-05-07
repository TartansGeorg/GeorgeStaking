from brownie import accounts, Staking1, exceptions
import brownie
import pytest

def test_staking_withdraw():
    account1 = accounts[0]
    staking1 = Staking1.deploy({"from": account1})

    amount = 1000000000000000000

    tx = staking1.stake({"from": account1, "amount": amount})
    tx.wait(1)
    assert staking1.balances(account1) == amount

    tx2 = staking1.unstake(amount, {"from": account1})
    assert staking1.balances(account1) == 0


def test_withdraw_too_much():
    account1 = accounts[0]
    staking1 = Staking1.deploy({"from": account1})

    amount = 1000000000000000000

    tx = staking1.stake({"from": account1, "amount": amount})
    tx.wait(1)

    with pytest.raises(exceptions.VirtualMachineError):
        staking1.unstake(amount + 10000000, {"from": account1})


def test_see_reward():
    account1 = accounts[0]
    staking1 = Staking1.deploy({"from": account1})

    amount = 1000000000000000000

    tx = staking1.stake({"from": account1, "amount": amount, "required_confs": 1})

    # Send two transactions to increase block count by two
    staking1.stake({"from": accounts[1], "amount": amount, "required_confs": 1})
    staking1.stake({"from": accounts[1], "amount": amount, "required_confs": 1})

    reward = staking1.seeReward({"from": account1})

    assert reward == amount * 2 / 1000


def test_claim_reward_transfer():
    account1 = accounts[0]
    staking1 = Staking1.deploy({"from": account1})

    amount = 1000000000000000000

    tx = staking1.stake({"from": account1, "amount": amount, "required_confs": 1})

    # Send nine transactions to increase block count by nine
    staking1.stake({"from": accounts[1], "amount": amount, "required_confs": 1})
    staking1.stake({"from": accounts[1], "amount": amount, "required_confs": 1})
    staking1.stake({"from": accounts[2], "amount": amount, "required_confs": 1})
    staking1.stake({"from": accounts[2], "amount": amount, "required_confs": 1})
    staking1.stake({"from": accounts[3], "amount": amount, "required_confs": 1})
    staking1.stake({"from": accounts[3], "amount": amount, "required_confs": 1})
    staking1.stake({"from": accounts[4], "amount": amount, "required_confs": 1})
    staking1.stake({"from": accounts[4], "amount": amount, "required_confs": 1})
    staking1.stake({"from": accounts[5], "amount": amount, "required_confs": 1})

    tx2 = staking1.claimReward({"from": account1})
    georgeCoins = staking1.georgeCoinBalance({"from": account1})

    assert georgeCoins == amount * 10 / 1000

    # Send nine transactions to increase block count by nine
    staking1.stake({"from": accounts[1], "amount": amount, "required_confs": 1})
    staking1.stake({"from": accounts[1], "amount": amount, "required_confs": 1})
    staking1.stake({"from": accounts[2], "amount": amount, "required_confs": 1})
    staking1.stake({"from": accounts[2], "amount": amount, "required_confs": 1})
    staking1.stake({"from": accounts[3], "amount": amount, "required_confs": 1})
    staking1.stake({"from": accounts[3], "amount": amount, "required_confs": 1})
    staking1.stake({"from": accounts[4], "amount": amount, "required_confs": 1})
    staking1.stake({"from": accounts[4], "amount": amount, "required_confs": 1})
    staking1.stake({"from": accounts[5], "amount": amount, "required_confs": 1})

    tx3 = staking1.claimReward({"from": account1})
    georgeCoins = staking1.georgeCoinBalance({"from": account1})

    assert georgeCoins == amount * 20 / 1000

    staking1.transfer(accounts[2], amount * 2 / 1000, {"from": account1})
    assert staking1.georgeCoinBalance({"from": accounts[2]}) == amount * 2 / 1000


def test_malicious_transfer():
    account1 = accounts[0]
    staking1 = Staking1.deploy({"from": account1})

    with brownie.reverts():
        tx = staking1.transfer(accounts[1], 1000000000000000000, {"from": account1})