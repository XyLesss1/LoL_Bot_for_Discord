import json

with open('champion.json') as champs_data:
    champs = json.load(champs_data)

def find_champ(id):
    for key in champs['data']:
        if champs['data'][key]['key'] == str(id):
            return key

# def find_picture(id):


