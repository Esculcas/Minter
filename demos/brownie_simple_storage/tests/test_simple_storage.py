from lib2to3.pgen2.literals import simple_escapes
from brownie import accounts, SimpleStorage


def test_deploy():
    # para fazer testes é preciso fazer 3 coisas_: arrange; act ; assert
    # arrange
    account = accounts[0]
    # act
    simple_storage = SimpleStorage.deploy({"from": account})
    starting_value = simple_storage.retrive()
    expected = 0
    # assert
    assert starting_value == expected


def test_updating_deploy():
    # Arrange
    account = accounts[0]
    simple_storage = SimpleStorage.deploy({"from": account})
    # Act
    expected = 15
    simple_storage.store(expected, {"from": account})
    # Assert
    assert expected == simple_storage.retrive()
