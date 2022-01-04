#######################################
# NFT ONLY 721 -  
#            
#######################################


# 
# in Terminal digitare

# per attivare l'ambiente virtuale:
#    su Windows:
#    .\venvmonitornft\Scripts\activate
#    .\casa-venv\Scripts\activate
#
#
# poi digitare
#   streamlit run nft-only-721.py

# per commentare un BLOCCO DI CODICE

# seleziona il blocco di codice e usa Ctrl+k, Ctrl+c
#  Ctrl+k, Ctrl+u per scommentare.
# ========================================================================================
#   001 - RISOLTO 
#   Problema:
#   Utilizzando le API Etherscan che leggono la situazione attuale, quando un NFT è 
#   stato venduto si perde la transazione di acquisto
#   
#   Soluzione:
#   le Etherscan API recuperano ,in genere, sia la trx di buy che di sell,
#   escluso che per il case #004 
#
# 
#   ---------------------------------------------------------------------------------------
#   002 - RISOLTO
#   Problema:
#   Quando si acquistano multipli NFT. come succede in fase di minting e come è successo per 
#   i 4 Queens+Kings degli Hackatao dal JSON risultante dalla lettura con Etherscan API ci sono
#   correttamente 4 righe, ma tutte riportano il costo complessivo dell'operazione sia di acquisto
#   che di fees.
# 
#   Soluzione:
#   inserita routine che attribuisce il buy_cost e le fee complessive ad una sola delle transazioni
#   
#   
# #   ---------------------------------------------------------------------------------------#  
#
#   003 - 
#   Problema:
#   Pare, ma non sono sicuro, che per gli NFT non acquistati su OpenSea 
#   esempio: 
#   262801  KnownOriginDigitalAsset : ho la data di acquisto ma non il costo
#   130913  Sandbox's LANDs         : ho Buy Date ma non Buy Price, ma non ho la Sell Date ma ho il Sell Cost
# 
#   Soluzione:
#   da trovare
#   
# #   ---------------------------------------------------------------------------------------#  
#
#   004 -
#   Problema:
#   A differenza del case 001, in questo caso:
#   5427    0bits   OK Buy Date e Buy Price, ma non ho la Sell Date ma ho il Sell Cost
# 
#   Soluzione:
#   da trovare
#   #  
    
# ========================================================================================

#
#   005 -
#   Problema:
#   I token 0xHunter sono stati mintati con una unica trx esattamente come i Queens+Kings (case #002)
#   ma a differenza di quel caso dove nella trx è presente il valore complessivo, in questo caso
#   il Value è 0.
#   Quindi al momento per gli 0xHunter mi ritrovo con un buy_cost = 0 
#   5427    0bits   OK Buy Date e Buy Price, ma non ho la Sell Date ma ho il Sell Cost
# 
#   Soluzione:
#   da trovare
#   #  
    
# ========================================================================================

from types import NoneType
from requests.models import Response
import streamlit as st
import numpy as np
import pandas as pd
import json
from web3 import Web3
import requests
from datetime import datetime

 
f = open("nft.json", "w")

st.header(f"OpenSea NFTAlert.tools")



w3 = Web3(Web3.HTTPProvider('https://mainnet.infura.io/v3/e26aa26baa40400480ec0b2350086a85'))

st.write(f"Ethereum blockchain connection is {w3.isConnected()}")


# Recupero del Floor Price di uno specifico progetto/collezione
def floor_price(slug):

    url = 'https://api.opensea.io/api/v1/collection/'+  slug +'/stats'

    r = requests.get(url)

    response_json = r.json()

    fp = response_json['stats']['floor_price']
   # print(f"collection {slug} - floor_price {fp}")
    return(fp) 


# Calcolo della variazione percentuale fra il Buy Price e l'attuale Floor Price
# COME CALCOLARE LA PERCENTUALE TRA DUE NUMERI  
# Se ancora non ti è chiaro il procedimento, ecco un esempio pratico che ti aiuterà 
# a capire come calcolare la variazione percentuale. 
# Il nostro valore iniziale Xi è uguale a 10 euro, mentre il valore finale Xf equivale a 15 euro. 
# Sostituendo i due valori a Xi e Xf nella nostra formula, avremo che:
# {[(15 - 10)/ 10] x 100 }% = {[ 5/10] x 100} %= 50%

def var_perc(buy_price, floor_price):
    #calcolo vp = variazione percentualr
    vp = ((floor_price - buy_price)/ buy_price) * 100 
    if len(str(vp)) > 5:
            l1 = str(vp)[0:4]
            vpperc = str(l1) + ' %'
    else:
        vpperc = str(vp) + ' %'
    return(vpperc)


# Claudio HOT wallet
address = '0xC4d646d92E180d7f385c6e35c2aE7749d6CcE9Dd'

# Paolo
# address = '0xBCb127e3E3977a152a5873Ea707BeFF0aE88E66B'

# Andrea Biancolli Vault
#address = '0xb6c5af8e01c993f2897f7698d777b5c34c29e5ef'

# Andrea Biancolli HOT wallet
# address = '0xbe2da1bff5351c794400d55546550e85d9bbf344'


api_key = 'NVWRUTS4NUD7PCFPU5TFNMU8RGP249D9FP'
url =   "https://api.etherscan.io/api?module=account&action=tokennfttx&address=" + address +\
        "&page=1&offset=1000&startblock=0&endblock=99999999&sort=asc&apikey=" + api_key

r = requests.get(url)

response_json = r.json()
a = json.dumps(response_json, indent=3)

opensea_file = open("etherscan_NFT.json", "w")
opensea_file.write(str(a))
opensea_file.close()

tot_sell = 0
tot_eth_sell = 0
tot_buy = 0
tot_eth_buy = 0


now = datetime.now()
dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
 

with open('etherscan_NFT.json') as access_json:
    read_content = json.load(access_json)



event_list = []

nft_list = {}
nft_list['erc721'] = []

 

first_time = True


for assets in read_content['result']:

    isUpdate = False

    #
    #  cerco lo "slug" di questa collezione
    #
    try:

        url = 'https://api.opensea.io/api/v1/asset/'+ assets['contractAddress'] + '/' + assets['tokenID'] +'/'
        
        r = requests.get(url)
        response_json = r.json()

        slug = response_json['collection'] ['slug']
        #print(slug)
    except TypeError:
        slug = ''

    #
    #  recupero "floor price" di questa collezione
    #
    try:
        fp = floor_price(slug)
    except TypeError:
        floor_price = 0

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

        gas_price = Web3.fromWei(int(trx_json_dict['gasPrice']), 'ether')
        gas_used = trx_json_dict['gas']
        trx_fee = str(round(gas_price * gas_used, 4))
    except TypeError:
        trx_fee = ''


    try:
        bid_amount = Web3.fromWei(int(trx_json_dict['value']), 'ether')
    except TypeError:
        total_sale_price = 0
        bid_amount  = 0

    low_address = address.lower()
    low_from = assets['from'].lower()
    if  low_address == low_from:
        sell_price  = float(bid_amount)
        date_sell = date
        date_buy = ''
        buy_cost = 0
        tot_sell += 1
        tot_eth_sell += sell_price
    else:
        buy_cost = float(bid_amount)
        sell_price = 0
        date_buy = date
        date_sell = ''
        tot_buy += 1


    if first_time:
        first_time = False
       
        nft_list['erc721'].append({
                'token_ID':  assets['tokenID'],
                'token_name': assets['tokenName'],
                'date_buy':  date_buy,
                'buy_cost': buy_cost,
                'date_sell':  date_sell,
                'sell_price': sell_price,
                'trx_fee': trx_fee,
                'floor_price': fp,
                'hash': assets['hash']
        })
        tot_eth_buy += buy_cost
    else:
        # cerca se esiste stesso token_ID
        for nft in nft_list['erc721']:

            if  (assets['tokenID'] == nft['token_ID'] and assets['tokenName'] == nft['token_name']):
               
                # aggiornare sell_price
                nft['sell_price'] = sell_price
                nft['date_sell'] = date_sell
                isUpdate = True
            elif (assets['hash'] == nft['hash']):
                nft['buy_cost'] = 0
                nft['trx_fee'] = 'mint'
                

        if not isUpdate:
             
            nft_list['erc721'].append({
            'token_ID':  assets['tokenID'],
            'token_name': assets['tokenName'],
            'date_buy':  date_buy,
            'buy_cost': buy_cost,
            'date_sell':  date_sell,
            'sell_price': sell_price,
            'trx_fee': trx_fee,
            'floor_price': fp,
            'hash': assets['hash']
            })
            tot_eth_buy += nft['buy_cost']


nft_json = json.dumps(nft_list, indent=4, default=str)
f.write(nft_json)
f.close()

with open('nft.json') as access_json:
    nft_json = json.load(access_json)

    
#################################################
# Routine di "pulizia" prima di visualizzare
#################################################

# se il token ID è troppo lungo si visualizzano solo i primi e gli ultimi 4 caratteri
for n in nft_json['erc721']:
    s = n['token_ID']
    if len(n['token_ID']) > 15:
        l1 = s[0:4]
        l2 = s[-4:]
        s = l1 + "..." + l2

    if n['buy_cost'] > 0:
        vp = var_perc(n['buy_cost'], n['floor_price'])
    else:
        vp = ''

    event_list.append([s, n['token_name'],  n['date_buy'] , n['buy_cost'], n['date_sell'],  n['sell_price'] ,n['floor_price'], vp,  n['trx_fee']  ])



df = pd.DataFrame(event_list, columns=['TokenID', 'NFT', 'Buy Date',  'Buy Cost', 'Sell Date' , 'Sell Price', 'Floor Price' ,' Var. %', 'Txn Fee'])
st.write(df)


# st.sidebar.write("Total Sell: " + str(tot_sell) + "       " + "ETH " + str(tot_eth_sell)  )
st.sidebar.write("Total Sell: " + str(tot_sell)  )
st.sidebar.write("ETH " + str(tot_eth_sell))
st.sidebar.write("")
st.sidebar.write("Total Buy : " + str(tot_buy) )
st.sidebar.write("ETH " + str(tot_eth_buy))
st.sidebar.write("")
st.sidebar.write("Time Floor Price : " + dt_string )




