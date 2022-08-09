from dis import Bytecode
from ensurepip import version
from re import I
from solcx import compile_standard, install_solc
import json
from web3 import Web3
import web3
import os
from dotenv import load_dotenv

load_dotenv()

with open("./simpleStorage.sol", "r") as file:
    simple_storage_file = file.read()

# Compile our solidity
install_solc("0.6.0")

compiled_sol = compile_standard(
    {
        "language": "Solidity",
        "sources": {"SimpleStorage.sol": {"content": simple_storage_file}},
        "settings": {
            "outputSelection": {
                "*": {"*": ["abi", "metadata", "evm.bytecode", "evm.sourceMap"]}
            }
        },
    },
    solc_version="0.6.0",
)
with open("compiled_code.json", "w") as file:
    json.dump(compiled_sol, file)

# get bytcode
bytecode = compiled_sol["contracts"]["SimpleStorage.sol"]["simpleStorage"]["evm"][
    "bytecode"
]["object"]

# get ABI
abi = compiled_sol["contracts"]["SimpleStorage.sol"]["simpleStorage"]["abi"]

# to connect to rinkeby
w3 = Web3(
    Web3.HTTPProvider("https://rinkeby.infura.io/v3/e09afcd318364ad8a5c4378246357963")
)
chain_id = 4
my_address = "0xC5531e74FD909f2bAe8d7a6c93E09ff57971Bd4C"
# private_key = "0x824a7190ce4775cccf8fbd7404c735a469a01b2f40712effedd7e39a8d110889"
private_key = os.getenv("PRIVATE_KEY")

# create the conctrat in python
SimpleStorage = w3.eth.contract(abi=abi, bytecode=bytecode)

# get the latesteste transation
nonce = w3.eth.getTransactionCount(my_address)

# 1. build transaction
# 2. Sign a transaction
# 3. Send a transaction
transaction = SimpleStorage.constructor().buildTransaction(
    {
        "chainId": chain_id,
        "gasPrice": w3.eth.gas_price,
        "from": my_address,
        "nonce": nonce,
    }
)
# 2.
signed_txn = w3.eth.account.sign_transaction(transaction, private_key=private_key)
# 3.Send this signed transation
print("Deploying contract...")
tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

print("Deployed!")

# working with the contract, you always need
# Contract Address AND
# Contract ABI

simple_storage = w3.eth.contract(address=tx_receipt.contractAddress, abi=abi)
# Há 2 formas de interagir com a bockchain
# Call -> simulate making the call and getting a return value (nunca vai fazer um state change apenas ve)
# Transact -> actualy make a state change (pode fazer um state change)

# Valor incial do favoriteNumber
print(simple_storage.functions.retrive().call())
# 1.
store_transaction = simple_storage.functions.store(15).buildTransaction(
    {
        "chainId": chain_id,
        "gasPrice": w3.eth.gas_price,
        "from": my_address,
        "nonce": nonce + 1,
    }
)
# 2.
signed_store_tx = w3.eth.account.sign_transaction(
    store_transaction, private_key=private_key
)
# 3.
print("Updating contract...")
send_store_tx = w3.eth.send_raw_transaction(signed_store_tx.rawTransaction)
tx_receipt = w3.eth.wait_for_transaction_receipt(send_store_tx)

print(simple_storage.functions.retrive().call())
print("Contract Updated!")
