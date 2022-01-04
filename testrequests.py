# ====================================================================================
# ESEMPIO 1 
#
# import requests

# url = "https://api.opensea.io/api/v1/events?only_opensea=false&offset=0&limit=20"

# headers = {"Accept": "application/json"}

# response = requests.request("GET", url, headers=headers)

# print(response.text)

#   =====================================================================================================


# ====================================================================================
# ESEMPIO 2  
# CODICE FUNZIONANTE (OTTIMO e FONDAMENTALE PER GLI ESERCIZI)
# estrae tutti gli asset collegati con uno specifico wallet address e li scrive in un file: opensea_file.json
# 
# # estrae tutti gli events collegati con uno specifico wallet address e li scrive in un file: opensea_fileevents.json#



#
# ASSETS.JSON 
#


import requests, json

offset = 0

data = {'assets': []}

# fetch assets in collection 50 at a time
while True:
    params = {
        'owner': '0xC4d646d92E180d7f385c6e35c2aE7749d6CcE9Dd',
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

# /////////////////////////////////////////////////////////////
# EVENTS.JSON 
# /////////////////////////////////////////////////////////////

# import requests, json

# offset = 0

# data = {'asset_events': []}

# # fetch assets in collection 50 at a time
# while True:
#     params = {
#         'account_address': '0xC4d646d92E180d7f385c6e35c2aE7749d6CcE9Dd',
#         'only_opensea': 'false',
#         'offset': offset,
#         'limit': 50
#     }
 
     
#     headers = {
#         "Accept": "application/json",
#         "X-API-KEY": "54f28eb29db648719c2eaaabccc414fc"
#     }


#     r = requests.get('https://api.opensea.io/api/v1/events', params=params, headers=headers)
    
#     print(f"offset: {offset}")
#     print(f"status code: {r.status_code}")
#     print(f"raise_for_status: { r.raise_for_status()}")
#     print(f"response.text: {r.text}")



#     response_json = r.json()

#     print(params)
#     data['asset_events'].extend(response_json['asset_events'])

#     print(len(response_json['asset_events']))
#     if len(response_json['asset_events']) < 50:
#         break
    
#     offset += 50

# a = json.dumps(response_json, indent=3)
# #print(a)

# opensea_file = open("opensea_file_events.json", "w")

# opensea_file.write(str(a))

# opensea_file.close()



# ====================================================================================
# ESEMPIO 3
#
#   CODICE FUNZIONANTE
#   diversamente dall'esempio precedente (ESEMPIO 2) questo codiceestrae solo il numero di asset definiti nel parametro asset
#   quindi da 0 ad un massimo di 50
#
# url = "https://api.opensea.io/api/v1/assets?owner=0xC4d646d92E180d7f385c6e35c2aE7749d6CcE9Dd&order_direction=desc&offset=0&limit=20"

# headers = {"X-API-KEY": "54f28eb29db648719c2eaaabccc414fc"}

# response = requests.request("GET", url, headers=headers)

# # print(response.text)
# data = requests.get(url).json()

# # a = print(json.dumps(data, indent=3))
# a = json.dumps(data, indent=3)


# print(a)

# opensea_file = open("opensea_file.json", "w")

# opensea_file.write(str(a))

# opensea_file.close()

#   =====================================================================================================


#   =====================================================================================================
# ESEMPIO 4
#
# CODICE FUNZIONANTE
#  preso da https://docs.opensea.io/reference/retrieving-asset-events
# 
# recupera gli eventi per :
#       asset_contract_address (smart contract del progetto)
#       coollection_slug
#       token id
#       account_address
#       event_type
# #


#import requests

# url = "https://api.opensea.io/api/v1/events?asset_contract_address=0x24998f0A028d197413EF57C7810f7a5EF8B9FA55&collection_slug=pandaparadise&token_id=4377&account_address=0xC4d646d92E180d7f385c6e35c2aE7749d6CcE9Dd&event_type=successful&only_opensea=false&offset=0&limit=20"

# headers = {
#     "Accept": "application/json",
#     "X-API-KEY": "54f28eb29db648719c2eaaabccc414fc "
# }

# response = requests.request("GET", url, headers=headers)

# print(response.text)

#   =====================================================================================================

# ====================================================================================
# ESEMPIO 5  
# CODICE FUNZIONANTE  
#  e: opensea_file.json
# #

# import   json
# from types import NoneType
# from requests import NullHandler
# from web3 import Web3

# # def render_asset(asset):
# #     #print(f"asset['name']{asset['name']}")
     
# #     if asset['name'] is not None:
# #         print(asset['name'])
# #     else:
# #         print(f"{asset['collection']['name']} #{asset['token_id']}")

# #     # if asset['description'] is not None:
# #     #     print(asset['description'])
# #     # else:
# #     #     print(asset['collection']['description'])

# #     if asset['asset_contract'] is not None:
# #         print(asset['asset_contract'] )
# #     else:
# #         print("pippo")



# with open('opensea_file.json') as access_json:
#     read_content = json.load(access_json)

# for assets in read_content['assets']:
#     print(assets['asset_contract'] ['name'])

#     try:
#         total_sale_price = assets['last_sale'] ['total_price'] 
#     except TypeError:
#         total_sale_price = 0
    
#     bid_amount = Web3.fromWei(int(total_sale_price), 'ether')
#     print(f"ETH {bid_amount}")

