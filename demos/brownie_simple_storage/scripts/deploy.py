from ast import Store
from brownie import accounts, config, SimpleStorage, network


def deploy_simple_storage():
    account = get_account()
    simple_storage = SimpleStorage.deploy({"from": account})
    # simple_storage.wait(1)
    # print(account)
    # account = accounts.add(config["wallets"]["from_key"])
    # print(account)
    stored_value = simple_storage.retrive()
    print(stored_value)
    add_value = simple_storage.store(1, {"from": account})
    add_value.wait(1)
    update_tras = simple_storage.retrive()
    print(update_tras)


def get_account():
    if network.show_active() == "development":
        return accounts[0]
    else:
        return accounts.add(config["wallets"]["from_key"])


def main():
    deploy_simple_storage()
