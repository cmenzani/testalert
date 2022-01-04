# import requests



# params = {}

# params = {
#     'asset_contract_address': '0x495f947276749ce646f68ac8c248420045cb7b5e',
#     'collection_slug': 'thenftmag',
#     'account_address': '0xC4d646d92E180d7f385c6e35c2aE7749d6CcE9Dd',
#     'only_opensea': 'false',
#     'offset': '0',
#     'limit': '20'
# }

# headers = {
#     "Accept": "application/json",
#     "X-API-KEY": "54f28eb29db648719c2eaaabccc414fc"
# }


# response = requests.get('https://api.opensea.io/api/v1/events', params=params, headers=headers)
# # # =====================================================================

# print(f"status code: {response.status_code}")
# print(f"raise_for_status: { response.raise_for_status()}")

# print(f"response.text: {response.text}")


# =============================================================================================================
# =============================================================================================================
#   A   S   S   E   T   S     B Y   ETHERSCAN.IO         R   O   U   T   I   N   E
# =============================================================================================================
# =============================================================================================================

# import requests
# import json

# address = '0xC4d646d92E180d7f385c6e35c2aE7749d6CcE9Dd'
# api_key = 'NVWRUTS4NUD7PCFPU5TFNMU8RGP249D9FP'
# url =   "https://api.etherscan.io/api?module=account&action=tokennfttx&address=" + address +\
#         "&page=1&offset=100&startblock=0&endblock=99999999&sort=asc&apikey=" + api_key 

# r = requests.get(url)

# print(r.content)
# response_json = r.json()
# a = json.dumps(response_json, indent=3)
# print(a)

# opensea_file = open("etherscan_NFT.json", "w")

# opensea_file.write(str(a))

# opensea_file.close()

# ===================================================================

import requests
import json 
 
# url =   "https://api.etherscan.io/api?module=account&action=tokennfttx&address=" + address +\
#         "&page=1&offset=1000&startblock=0&endblock=99999999&sort=asc&apikey=" + api_key

# params = {
#     'clooection': address,
#     'order_by': 'pk',
#     'order_direction': 'desc',
#     'offset': 0,
#     'limit': 50
# }

    # r = requests.get('https://api.opensea.io/api/v1/collection', params=params)

# da dove ho preso spunto per risolvere il problema del recupero del floor price
# # view-source:https://www.floorchecker.com/
#
#   'https://api.opensea.io/api/v1/collection/'+obj.slug+'/stats'

#    https://api.opensea.io/api/v1/collections?offset=0&limit=300&asset_owner='+wallet

slug = 'queenskings'
url = 'https://api.opensea.io/api/v1/collection/'+  slug +'/stats'

r = requests.get(url)

response_json = r.json()


fp = response_json['stats']['floor_price']
print(f"collection {slug} - floor_price {fp}")



 