from brownie import accounts, Staking1

def deploy_staking():
    account = accounts[0]
    staking1 = Staking1.deploy({"from": account})

def main():
    deploy_staking()