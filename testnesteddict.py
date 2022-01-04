import json

#with open('source-data.json') as access_json:
with open('opensea_file_lite.json') as access_json:
    read_content = json.load(access_json)


# print(read_content['assets'])
# print(type(read_content))

for assets in read_content['assets']:
    print(assets['asset_contract'] ['name'])
    print(assets['last_sale'] ['total_price'])
print('ZERO  ======================================================================')
##question_access = read_content['assets']
# #question_access = read_content['results']
# print(question_access)
# print(type(question_access))

# # print(question_access)

# for question_data in question_access:
#     print(question_data)

# print(type(question_data))
# print('UNO ======================================================================')
# replies_access = question_data['asset_contract']
# #replies_access = question_data['traits']
# #replies_access = question_data['replies']

# print(replies_access)

# print(type(replies_access))

# print('DUE ======================================================================')

# for replies_data in replies_access:
#     print(replies_data)
#     print(type(replies_data))

# print('TRE ======================================================================')
# # user_name = replies_data['user']['display_name']
# #user_name = replies_data['traits']['trait_count']

# # print(user_name)