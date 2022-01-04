# in Terminal digitare

# per attivare l'ambiente virtuale:
#    su Windows:
#    .\venvmonitornft\Scripts\activate
#    .\casa-venv\Scripts\activate
#


from requests.models import Response
# import streamlit as st
import numpy as np
import pandas as pd
import json
from web3 import Web3
import requests
from datetime import datetime


# st.header(f"OpenSea NFTAlert.tools")



w3 = Web3(Web3.HTTPProvider('https://mainnet.infura.io/v3/e26aa26baa40400480ec0b2350086a85'))

# st.write(f"Ethereum blockchain connection is {w3.isConnected()}")
 


address = '0xC4d646d92E180d7f385c6e35c2aE7749d6CcE9Dd'
api_key = 'NVWRUTS4NUD7PCFPU5TFNMU8RGP249D9FP'
# url =   "https://api.etherscan.io/api?module=account&action=tokennfttx&address=" + address +\
#         "&page=1&offset=100&startblock=0&endblock=99999999&sort=asc&apikey=" + api_key 


# MEMO: se le transazioni nel mio account dovessero superare le 200 devo adeguare il parametro "offset"
#       o comunque capire come gestirlo al meglio
url = "https://api.etherscan.io/api?module=account&action=txlist&address=" + address +\
      "&page=1&offset=200&startblock=0&endblock=99999999&sort=asc&apikey=" + api_key 
   

r = requests.get(url)

response_json = r.json()
a = json.dumps(response_json, indent=3)



opensea_file = open("etherscan_ALL_TRX.json", "w")
opensea_file.write(str(a))
opensea_file.close()

tot_sell = 0
tot_eth_sell = 0 
tot_buy = 0   
tot_eth_buy = 0 

with open('etherscan_ALL_TRX.json') as access_json:
    read_content = json.load(access_json)


count_trx = 0

event_list = []
for assets in read_content['result']:

#    token_name = assets['tokenName']
    count_trx  += 1 

    try:
        date_str = datetime.fromtimestamp(int(assets['timeStamp'])).strftime('%d/%m/%y')
        date_time = datetime.strptime(date_str, '%d/%m/%y')
        date = datetime.date(date_time)
    except TypeError:
        date = 'nd'


    try:

        trx = w3.eth.get_transaction( assets['hash'] )
        trx_json = Web3.toJSON(trx)
        trx_json_dict = json.loads(trx_json)
        
        #if assets['hash'] == '0x09ed7b7fabaf97fa50d1a42171eef4bfa12e869c79218804fe5a7161d99c34fa':
        if assets['hash'] == '0xde17dc1166cfd03b6adc85664eadb2de7c555c7c57927b6c01875c5ef5b58b48':
            
            print(trx_json_dict)

            # # INIZIO
            # # codice preso da questo post https://medium.com/coinmonks/discovering-the-secrets-of-an-ethereum-transaction-64febb00935c
            # # TOPIC: come decodificare i dati di INPUT di una transazione:

            # # Get ABI for smart contract NOTE: Use "to" address as smart contract 'interacted with'
            # abi_endpoint = f"https://api.etherscan.io/api?module=contract&action=getabi&address={trx['to']}&apikey={api_key }"
            # abi = json.loads(requests.get(abi_endpoint).text)

            # # Create Web3 contract object
            # contract = w3.eth.contract(address=trx["to"], abi=abi["result"])

            # # Decode input data using Contract object's decode_function_input() method
            # func_obj, func_params = contract.decode_function_input(trx["input"])

            # print(f"func_obj {type(func_obj)}")
            # print(func_obj)

            # print(f"func_params {type(func_params)}")
            # print(func_params)

            # # FINE


            # INIZIO
            # codice preso da questo post https://medium.com/coinmonks/unlocking-the-secrets-of-an-ethereum-transaction-3a33991f696c
            # TOPIC: come decodificare EVENT LOGS di una transazione:

            # Get transaction receipt
            receipt = w3.eth.get_transaction_receipt(assets['hash'])

            # Isolate log to decode
            YOUR_LOG_INDEX = 0
            log = receipt["logs"][YOUR_LOG_INDEX]
            # Get smart contract address where log was initiated
            smart_contract = log["address"]

            print(f"smart_contract: {smart_contract}")

            # Get ABI of contract
            abi_endpoint = f"https://api.etherscan.io/api?module=contract&action=getabi&address={smart_contract}&apikey={api_key}"
            abi = json.loads(requests.get(abi_endpoint).text)

            print(f"abi: {abi}")

            # Create Web3 contract object
            contract = w3.eth.contract(address=trx["to"], abi=abi["result"])

            print(f"contract: {contract}")

            # Get event signature of log (first item in topics array)
            receipt_event_signature_hex = w3.toHex(log["topics"][0])

            print(f"receipt_event_signature_hex: {receipt_event_signature_hex}")

            # Find ABI events
            abi_events = [abi for abi in contract.abi if abi["type"] == "event"]

            print(f"abi_events: {abi_events}")

            # Determine which event in ABI matches the transaction log you are decoding
            for event in abi_events:
                # Get event signature components
                name = event["name"]

                print(f"name: {name}")

                inputs = [param["type"] for param in event["inputs"]]
                inputs = ",".join(inputs)
                # Hash event signature
                event_signature_text = f"{name}({inputs})"
                event_signature_hex = w3.toHex(w3.keccak(text=event_signature_text))
                # Find match between log's event signature and ABI's event signature
                if event_signature_hex == receipt_event_signature_hex:
                    # Decode matching log
                    decoded_logs = contract.events[event["name"]]().processReceipt(receipt)
                    print(f"decoded_logs: {decoded_logs}")

            # FINE
            print('==================================================================')

        gas_price = Web3.fromWei(int(trx_json_dict['gasPrice']), 'ether')
        gas_used = trx_json_dict['gas']
        trx_fee = str(round(gas_price * gas_used, 4))
    except TypeError:
        trx_fee = 'nd'
        

    try:
        bid_amount = Web3.fromWei(int(trx_json_dict['value']), 'ether')
    except TypeError:
        total_sale_price = 0
        bid_amount = 0
    
    low_address = address.lower()
    low_from = assets['from'].lower()
    if  low_address == low_from:
        sell_price = float(bid_amount)
        buy_cost = 0
        sell_buy = 'Sell'
        tot_sell += 1  
        tot_eth_sell += sell_price
    else:
        buy_cost = float(bid_amount)
        sell_price = 0
        sell_buy = 'Buy'
        tot_buy += 1  
        tot_eth_buy += buy_cost     


print(f"Total Items in JSON file {count_trx} ")