# in Terminal digitare

# per attivare l'ambiente virtuale:
#    su Windows:
#    .\venvmonitornft\Scripts\activate
#    .\casa-venv\Scripts\activate
#

# per capire e testare le potenzialità della libreria => web3
from web3 import Web3
import json
from hexbytes import HexBytes






# connessione a nodo INFURA <<< FUNZIONA >>>
#w3 = Web3(Web3.HTTPProvider('https://mainnet.infura.io/v3/e26aa26baa40400480ec0b2350086a85'))


# connessione a nodo ERIGON di VIVIDO <<< FUNZIONA >>>
w3 = Web3(Web3.HTTPProvider('http://83.149.167.172:8545'))
print(f"Ethereum blockchain connection is {w3.isConnected()}")

# ========================================================================
# # utility: checksum di un indirizzo  ethereum 
# print(w3.toChecksumAddress('0x495f947276749ce646f68ac8c248420045cb7b5e'))


# ========================================================================
# legge una intera transazione
 
# trx = w3.eth.get_transaction('0xc1082ae65c6c9f538e0e6ee0ac08365859d6bba05a3278046f28f39a2cf662ff')
# trx_json = Web3.toJSON(trx)
# trx_json_dict = json.loads(trx_json)

# gas_price = Web3.fromWei(int(trx_json_dict['gasPrice']), 'ether')
# gas_used = trx_json_dict['gas']
 
# transaction_cost = str(round(gas_price * gas_used, 4))
# print(transaction_cost)



# scritto il file transaction,json per leggerlo meglio
#
# a = json.dumps(trx_json_dict, indent=3)
# print(a)

# opensea_file = open("transaction.json", "w")

# opensea_file.write(str(a))

# opensea_file.close()



# ========================================================================')
# legge il contenuto di uno specifico blocco 
#print( w3.eth.get_block(13568745))


# ========================================================================')
# legge il balance di un wallet 
# b = w3.eth.get_balance('0xC4d646d92E180d7f385c6e35c2aE7749d6CcE9Dd')
# balance = Web3.fromWei(int(b), 'ether')
# print(balance)


# ========================================================================
# test Filter 
# tratto da https://web3py.readthedocs.io/en/stable/filters.html

# AL MOMENTO NON FUNZIONA

# from web3.auto import w3

# event_filter = w3.eth.filter({"address": "0x495f947276749Ce646f68AC8c248420045cb7b5e"})

# print(f"event_filter {event_filter}")

# ========================================================================
# Returns the list of known accounts. 
#print(w3.eth.accounts)