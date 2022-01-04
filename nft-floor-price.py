# =======================================================================0
# è il sito da dove ho preso spunto per risolvere il problema del recupero del floor price
# view-source:https://www.floorchecker.com/
#
#   'https://api.opensea.io/api/v1/collection/'+obj.slug+'/stats'
#    https://api.opensea.io/api/v1/collections?offset=0&limit=300&asset_owner='+wallet

import requests
import json 
 
slug = 'queenskings'
url = 'https://api.opensea.io/api/v1/collection/'+  slug +'/stats'

r = requests.get(url)

response_json = r.json()


fp = response_json['stats']['floor_price']
print(f"collection {slug} - floor_price {fp}")