# per capire e testare le potenzialità della libreria => streamlit

# in Terminal digitare

# per attivare l'ambiente virtuale:
#    su Windows:
#    .\venvmonitornft\Scripts\activate
#    .\casa-venv\Scripts\activate
#
#
# poi digitare
#   streamlit run nft.py

# per commentare un BLOCCO DI CODICE

# seleziona il blocco di codice e usa Ctrl+k, Ctrl+c
#  Ctrl+k, Ctrl+u per scommentare.
# ========================================================================================




from requests.models import Response
import streamlit as st
import numpy as np
import pandas as pd
import json
from web3 import Web3
import requests
from datetime import datetime


st.header(f"OpenSea NFTAlert.tools")



w3 = Web3(Web3.HTTPProvider('https://mainnet.infura.io/v3/e26aa26baa40400480ec0b2350086a85'))

st.write(f"Ethereum blockchain connection is {w3.isConnected()}")
 



# =============================================================================================================
# =============================================================================================================
#   ETHERSCAN NFT              R   O   U   T   I   N   E
# =============================================================================================================
# =============================================================================================================

#   
# BEGIN => DEF MEDIA CONTENT CODE 
#
#   CODICE FUNZIONANTE
#   Non attiva per le motivazioni descritte più avanti nel codice che richiama questa def
#   

# def render_asset(asset):
#     print(f"asset['image_url'] {asset['image_url']}")
#     if asset['image_url'].endswith('mp4') or asset['image_url'].endswith('mov'):
#         media_content = st.video(asset['image_url'])
#     elif asset['image_url'].endswith('svg'):
#         svg = requests.get(asset['image_url']).content.decode()
#         media_content = st.image(svg)
#     elif asset['image_url']:
#         media_content = st.image(asset['image_url'])

#   
# END => DEF MEDIA CONTENT CODE 
#


# address = '0xC4d646d92E180d7f385c6e35c2aE7749d6CcE9Dd'
# api_key = 'NVWRUTS4NUD7PCFPU5TFNMU8RGP249D9FP'
# url =   "https://api.etherscan.io/api?module=account&action=tokennfttx&address=" + address +\
#         "&page=1&offset=100&startblock=0&endblock=99999999&sort=asc&apikey=" + api_key 

# r = requests.get(url)

# response_json = r.json()
# a = json.dumps(response_json, indent=3)

# opensea_file = open("etherscan_NFT.json", "w")
# opensea_file.write(str(a))
# opensea_file.close()

tot_sell = 0
tot_eth_sell = 0 
tot_buy = 0   
tot_eth_buy = 0 


# ==========================================================
# # fetch assets in collection 50 at a time
#
offset = 0

data = {'assets': []}
address = '0xC4d646d92E180d7f385c6e35c2aE7749d6CcE9Dd'

# fetch assets in collection 50 at a time
while True:
    params = {
        'owner': address,
        'order_by': 'pk',
        'order_direction': 'desc',
        'offset': offset,
        'limit': 50
    }
 
    r = requests.get('https://api.opensea.io/api/v1/assets', params=params)
       
    response_json = r.json()

    print(params)
    data['assets'].extend(response_json['assets'])

    if len(response_json['assets']) < 50:
        break
    
    offset += 50

a = json.dumps(response_json, indent=3)
print(a)

opensea_file = open("opensea_file.json", "w")

opensea_file.write(str(a))

opensea_file.close()


# ==========================================================




with open('opensea_file.json') as access_json:
    read_content = json.load(access_json)

event_list = []
for assets in read_content['assets']:

   
    # token_name = assets['tokenName']
    collection = assets['collection'] ['slug']
    token_name = assets['name']

    # try:
    #     date_str = datetime.fromtimestamp(int(assets['timeStamp'])).strftime('%d/%m/%y')
    #     date_time = datetime.strptime(date_str, '%d/%m/%y')
    #     date = datetime.date(date_time)
    # except TypeError:
    #     date = 'nd'

    try:
        name_collection = assets['asset_contract'] ['name'] 
    except TypeError:
        name_collection = 'nd'

    try:
        date = assets['last_sale'] ['event_timestamp'] 
    except TypeError:
        date = 'nd'

    
    try:
        #trx = w3.eth.get_transaction( assets['hash'] )
         
        trx = w3.eth.get_transaction(assets['last_sale'] ['transaction'] ['transaction_hash'])
        trx_json = Web3.toJSON(trx)
        trx_json_dict = json.loads(trx_json)
        print(f"trx_json_dict {trx_json_dict}")

        gas_price = Web3.fromWei(int(trx_json_dict['gasPrice']), 'ether')
        gas_used = trx_json_dict['gas']
        trx_fee = str(round(gas_price * gas_used, 4))
    except TypeError:
        trx_fee = 'nd'
        trx_json = Web3.toJSON(trx)
        trx_json_dict = json.loads(trx_json)


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
#    low_from = assets['from'].lower()
    low_from = trx_json_dict['from'].lower()
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


# ===============================================================

    print(f"NFT {token_name}")
    print(f"Collection {name_collection}")
    print(f"Date {date}")
    print(f"Sell/Buy {sell_buy}")
    print(f"Sell Price {sell_price}")
    print(f"Buy Cost {buy_cost}")
    print(f"Txn Fee {trx_fee}")
    print(f"Transaction Hash {assets['last_sale'] ['transaction'] ['transaction_hash']}")
    event_list.append([token_name, name_collection, date,  sell_buy, sell_price , buy_cost, trx_fee, assets['last_sale'] ['transaction'] ['transaction_hash'] ])
 

df = pd.DataFrame(event_list, columns=['NFT', 'Collection', 'Date', 'Sell/Buy', 'Sell Price', 'Buy Cost', 'Txn Fee', 'Transaction Hash'])
st.write(df)


st.sidebar.write("Total Sell: " + str(tot_sell) + "       " + "ETH " + str(tot_eth_sell)  )
st.sidebar.write("Total Buy : " + str(tot_buy) + "     " + "ETH " + str(tot_eth_buy))



# # =============================================================================================================
# # =============================================================================================================
# #   A   S   S   E   T   S              R   O   U   T   I   N   E
# # =============================================================================================================
# # =============================================================================================================

# #==========================

# with open('opensea_file.json') as access_json:
#     read_content = json.load(access_json)


# event_list = []
# for assets in read_content['assets']:
#     #print(assets['asset_contract'] ['name'])

#     collection = assets['collection'] ['slug']
#     token_name = assets['name']
    

#     try:
#         buy_date = assets['last_sale'] ['event_timestamp'] 
#     except TypeError:
#         buy_date = 'nd'


#     # try:
#     #     total_sale_price = assets['last_sale'] ['total_price'] 
#     #     bid_amount = Web3.fromWei(int(total_sale_price), 'ether')
#     # except TypeError:
#     #     total_sale_price = 0
#     #     bid_amount = 0
#     #   
#     # legge una intera transazione
#     #
#     try:
#         trx = w3.eth.get_transaction(assets )
#         trx_json = Web3.toJSON(trx)
#         trx_json_dict = json.loads(trx_json)

#         gas_price = Web3.fromWei(int(trx_json_dict['gasPrice']), 'ether')
#         gas_used = trx_json_dict['gas']
#         trx_fee = str(round(gas_price * gas_used, 4))
#     except TypeError:
#         trx_fee = 'nd'
        

#     try:
#         bid_amount = Web3.fromWei(int(trx_json_dict['value']), 'ether')
#     except TypeError:
#         total_sale_price = 0
#         bid_amount = 0

         
#     event_list.append([token_name, collection, buy_date,  float(bid_amount), trx_fee])
 

# df = pd.DataFrame(event_list, columns=['NFT', 'Collection', 'Buy Date', 'buy_cost', 'Txn Fee'])
# st.write(df)




# =============================================================================================================
# =============================================================================================================
#   E   V   E   N   T   S               R   O   U   T   I   N   E
# =============================================================================================================
# =============================================================================================================




# #==========================

# with open('opensea_file_events.json') as access_json:
#     read_content = json.load(access_json)


# event_list = []
# for events in read_content['asset_events']:


#     # collection = assets['collection'] ['slug']
#     # token_name = assets['name']
    
#     id = events['asset'] ['id']
#     token_id = events['asset'] ['token_id']
#     token_name = events['asset'] ['name']



#     # try:
#     #     buy_date = assets['last_sale'] ['event_timestamp'] 
#     # except TypeError:
#     #     buy_date = 'nd'


#     # # try:
#     # #     total_sale_price = assets['last_sale'] ['total_price'] 
#     # #     bid_amount = Web3.fromWei(int(total_sale_price), 'ether')
#     # # except TypeError:
#     # #     total_sale_price = 0
#     # #     bid_amount = 0
#     # #   
#     # # legge una intera transazione
#     # #
#     # try:
#     #     trx = w3.eth.get_transaction(assets['last_sale'] ['transaction'] ['transaction_hash'])
#     #     trx_json = Web3.toJSON(trx)
#     #     trx_json_dict = json.loads(trx_json)

#     #     gas_price = Web3.fromWei(int(trx_json_dict['gasPrice']), 'ether')
#     #     gas_used = trx_json_dict['gas']
#     #     trx_fee = str(round(gas_price * gas_used, 4))
#     # except TypeError:
#     #     trx_fee = 'nd'
        

#     # try:
#     #     bid_amount = Web3.fromWei(int(trx_json_dict['value']), 'ether')
#     # except TypeError:
#     #     total_sale_price = 0
#     #     bid_amount = 0


      
    
# #     event_list.append([token_name, collection, buy_date,  float(bid_amount), trx_fee])
 
#     event_list.append([id, token_id, token_name])
# # df = pd.DataFrame(event_list, columns=['NFT', 'Collection', 'Buy Date', 'buy_cost', 'Txn Fee'])
# #st.write(df)


# df_events = pd.DataFrame(event_list, columns=['id', 'token id', 'NFT'])
# st.write(df_events)

# ===================================================================
# codice salvato per copiarne pezzi 

    # event_list = []
    # for event in events['asset_events']:
    #     if event_type == 'offer_entered':
    #         if event['bid_amount']:
    #             bid_amount = Web3.fromWei(int(event['bid_amount']), 'ether')
    #         if event['from_account']['user']:
    #             bidder = event['from_account']['user']['username']
    #         else:
    #             bidder = event['from_account']['address']

    #         event_list.append([event['created_date'], bidder, float(bid_amount), event['asset']['collection']['name'], event['asset']['token_id']])

# === =============================================
 
