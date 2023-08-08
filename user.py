import requests
import os
import json
import xmltodict
from PIL import Image

class User:
    def __init__(self, nickname):
        self.vanityurl = nickname

        id_response = requests.get(f"https://steamcommunity.com/id/{nickname}?xml=1")
        data = xmltodict.parse(id_response.text)['profile']

        self.steam_id = data['steamID64']
        self.steam_name = data['steamID']

        avatar_response = requests.get(data['avatarFull'])
        with open("media/user_avatar.jpg", "wb") as f:
            f.write(avatar_response.content)

        print("Scraping inventory for: " + self.steam_name)
        
        self.inventory = Inventory(self.steam_id)

class Inventory:
    def __init__(self, steam_id):
        self.items = []
        
        response = requests.get(f"https://steamcommunity.com/inventory/{steam_id}/730/2?l=english&count=200")
        data = json.loads(response.text)

        try:
         for item in data['descriptions']:
          #  if item['classid'] != data['descriptions']['classid']:
            #    print("No se ha encontrado descripcion para asset: " + item['classid'])
              #  pass
            item_id = item['classid']

            new_item = Item(item_id, item['market_hash_name'], f'media/weapon_skins/{item_id}.png')

            if not os.path.exists('media/weapon_skins/{item_id}.png'):
                skin_response = requests.get("https://community.akamai.steamstatic.com/economy/image/" + item['icon_url'])

                with open(f"media/weapon_skins/{item_id}.jpg", "wb") as f:
                    f.write(skin_response.content)

                im = Image.open(f"media/weapon_skins/{item_id}.jpg")
                im = im.resize((150,113))
                im.save(f"media/weapon_skins/{item_id}.png")
                os.remove(f"media/weapon_skins/{item_id}.jpg")

            self.items.append(new_item)
        except TypeError as e:
            print("Cooldown active...")


class Item:
    def __init__(self, item_id, name, image):
        self.item_id = item_id
        self.name = name
        self.image = image

        price_response = requests.get(f"http://csgobackpack.net/api/GetItemPrice/?currency=USD&id={self.name}")
        data = json.loads(price_response.text)

        if data['success'] != True:
            print("No price found for: " + self.name)
            self.price = 'Not Availiable'
            return

        self.price = data['average_price']

  #      self.price = data['average_price']

