import bs4
import requests
import re



def get_web_content():
    page = requests.get(url="https://pokemondb.net/pokedex/national")
    return page.content


def get_name_and_url(_html):
    _html = str(_html)

    name = re.search('alt="(.*) sprite', _html)
    name = name.group(1)

    url = re.search('src="(.*)"', _html)
    url = url.group(1)
    return name, url



if __name__ == "__main__":
    content = get_web_content()

    soup = bs4.BeautifulSoup(content, "html.parser")
    gen_i_div = soup.find(class_="infocard-list infocard-list-pkmn-lg")
    links = gen_i_div.findAll(class_="img-fixed img-sprite")

    # links are in format of:
    # <span class="img-fixed img-sprite" data-alt="Bulbasaur sprite"
    # data-src="https://img.pokemondb.net/sprites/bank/normal/bulbasaur.png">
    # </span>

    pairings = []
    for link in links:
        name, url = get_name_and_url(link)
        pairings.append((name, url))


    with open("pokemon_image_links.txt", mode="a") as file:
        for item in pairings:

            entry = f"'{item[0]}' #start#{item[1]}#end#\n"
            try:
                entry = entry.encode(encoding="ascii")
                entry = entry.decode()
            except UnicodeEncodeError:
                print(entry)
            else:
                file.write(entry)

