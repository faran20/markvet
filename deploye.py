from web3 import HTTPProvider, Web3, WebsocketProvider
from ethereum import utils as u

ADDRESS = '0x07F3fB05d8b7aF49450ee675A26A01592F922734' # ropsten based contract

AUTHORITY = {
    'address': '0x8F5498bAEC61169FDd532073693BB4F789727514', # ropsten based account
    'key': u.normalize_key(b'Private_Key')
}

ABI = '''Contract_ABI'''

# HTTPProvider
w3 = Web3(HTTPProvider('https://ropsten.infura.io/v3/Account_Private_Key'))

# WebsocketProvider
#w3 = Web3(WebsocketProvider('wss://ropsten.infura.io/ws'))

root_chain_instance = w3.eth.contract(abi=ABI, address=ADDRESS)

# Here sending arguments create problem. Should I encode these ?

txn = root_chain_instance.functions.\
depositKyberTokens(Web3.toChecksumAddress("0xeF06F410C26a0fF87b3a43927459Cce99268a2eF"), int(2), Web3.toChecksumAddress("0x30051b94273ad0F87fE53Ae9Ef27e16774Bf8cbA")).\
buildTransaction({'from': AUTHORITY['address'],
                  'gas': Web3.toHex(7000000),
                  'chainID': 3,
                  'nonce': Web3.toHex(w3.eth.getTransactionCount(AUTHORITY['address'])),
                  'gasPrice': Web3.toHex(9000000000)})


raw_tx = {'nonce': txn['nonce'],
      'gas': txn['gas'],
      'chainID': 3,
      'gasPrice': txn['gasPrice'],
      'to': ADDRESS,
      'data': txn['data'], # ***** PROBLEM HERE ******
      'from': txn['from']}


signed_txn = w3.eth.account.signTransaction(dict(raw_tx), AUTHORITY['key'])
w3.eth.sendRawTransaction(signed_txn['rawTransaction'])
print(Web3.toHex(Web3.sha3(signed_txn['rawTransaction'])))
