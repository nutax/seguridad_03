import hashlib
import json
import time
from web3 import Web3

#llenar lo que falta con los datos de tu cuenta
ganache_url = 'https://sepolia.infura.io/v3/1ece952fe1284236a950b41fa084af6c'
account_from = "0x6757d4702bcD391e959C0dc296ea640A58A76340"
account_to = "0xa7F3c68f32B2f5E6C1B11c26258Ff015631b2Cd1"
private_key = "9a17700131b96ecd1f57e8448747abb6bb5fff80db55a34fc1d4554c9093ce34"
w3 = Web3(Web3.HTTPProvider(ganache_url))
blockchain = []
VALUE = 0.01
GAS = 21000
GAS_PRICE = 5

def create_transaction(nonce, to, value, gas, gasPrice, pk):
    tx = {
        'nonce': nonce,
        'to': to,
        'value': w3.to_wei(value, 'ether'),
        'gas': gas,
        'gasPrice': w3.to_wei(gasPrice, 'gwei')
    }
    #firmar la transaccion
    signed_tx = w3.eth.account.sign_transaction(tx, pk)
    return signed_tx

def send_eth_transaction():
    res = w3.is_connected()
    if (res):
        #usar la cantidad de transacciones como nonce
        nonce = w3.eth.get_transaction_count(account_from)
        #fijar los valores del value, gas y el gasPrice. Hint: usa la funcion w3.eth.fee_history para determinar un valor que vaya a ser aceptado por la red
        #CUIDADO con mandar transacciones con valores de gas y gasPrice muy bajos, ya que pueden ser rechazadas por la red
        #prueba enviando un value pequeños, como unos cuantos wei
        signed_tx = create_transaction(nonce, account_to, VALUE, GAS, GAS_PRICE, private_key)
        tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
        return w3.eth.get_transaction(tx_hash) 
    else:
        return None

# Converts hash to a number and checks if it is prime
def simplePow(blockHash):
    blockHash = int(blockHash, 16)
    return isPrime(blockHash)

# Checks if a number is prime fast
def isPrime(n):
    if (n == 2 or n == 3):
        return True
    if (n % 2 == 0 or n < 2):
        return False
    for i in range(3, int(n**0.5) + 1, 2):
        if (n % i == 0):
            return False
    return True


# Checks if a number is even
def isEven(n):
    return n % 2 == 0

# Calculates a valid block hash and updates block if necessary
# Returns the block with a valid hash
def generateHash(block):
    blockString = json.dumps(block, sort_keys=True).encode()
    curr_hash = hashlib.sha256(blockString).hexdigest()
    return curr_hash

# Creates a new block
# Block structure is as follows:
# {
#     'index': current_index,
#     'timestamp': current_timestamp,
#     'data': {
#         'to': to_address,
#         'from': from_address,
#         'amount': amount
#      },
#     'prevHash': previous_block_hash,
#     'hash': block_hash,
#     'ctr': pow_counter
# }
# Returns the new block
def createBlock(prevBlock, timestamp, toAccount, fromAccount, amount):
    index = prevBlock['index'] + 1
    data = {
        'to': toAccount,
        'from': fromAccount,
        'amount': amount
    }
    block = {
            'index': index,
            'timestamp': timestamp,
            'data': data,
            'prevHash': prevBlock['hash'],
            'hash': '',
            'ctr': 0
        }
    ctr = 0
    while True:
        block['ctr'] = ctr
        curr_hash = generateHash(block)
        if (simplePow(curr_hash)):
            block['hash'] = curr_hash
            break
        ctr += 1
    return block

# Creates and stores the genesis block
# Genesis block index is 0. It has no previous block, so the all previous fields are empty strings or -1 values
# The genesis black has a timestamp of 0, an amount of 0, and no to or from addresses
def createGenesisBlock():
    genesisBlock =  createBlock({
        'index': -1,
    }, 0, '', '', 0)
    return genesisBlock

# Checks if a block is valid
# A block is valid if:
#   - The index is the previous index + 1
#   - The previous hash is the same as the previous block's hash
#   - The hash is the same as the calculated hash
#   - The hash meets the PoW check
def isValidBlock(newBlock, prevBlock):
    # q: what would be the code to check if the block is valid
    # hint: use the functions isEven and simplePow
    if (newBlock['index'] != prevBlock['index'] + 1 or newBlock['prevHash'] != prevBlock['hash']):
        return False
    
    curr_hash = generateHash(newBlock)
    if (newBlock['hash'] != curr_hash or not simplePow(curr_hash)):
        return False

    return True

# Adds a new block to the blockchain
# A block is added if it is valid
def addBlock(newBlock):
    # q: what would be the code to add a block to the blockchain
    # hint: use the function isValidBlock
    if (isValidBlock(newBlock, blockchain[-1])):
        blockchain.append(newBlock)
        return True
    return False
