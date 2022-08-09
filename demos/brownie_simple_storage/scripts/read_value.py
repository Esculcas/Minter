from brownie import SimpleStorage, accounts, config


def read_contract():
    simple_storage = SimpleStorage[-1]
    # o -1 significa que vai sempre buscar o contrato mais recente
    print(simple_storage.retrive())


def main():
    read_contract()
