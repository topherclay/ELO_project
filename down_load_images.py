import requests
import re
import os







with open("pokemon_image_links.txt") as file:
    pokemon_and_links = file.readlines()

for pairing in pokemon_and_links:
    # format is "'Charmander' #start#https://img.pokemondb.net/sprites/bank/normal/charmander.png#end#"

    name = re.search("'(.*)'", pairing).group(1)


    link = re.search("#start#(.*)#end#", pairing).group(1)
    print(link)

    image = requests.get(link)

    with open(f"pokemon/0000{name}", mode="wb") as file:
        file.write(image.content)



for pairing in pokemon_and_links:
    name = re.search("'(.*)'", pairing).group(1)

    os.rename(f"pokemon/0000{name}", f"pokemon/0000{name}.png")

