import glob
import random

from contender_and_headtohead import *

# wtf happened here?
import cv2.cv2 as cv2





DIRECTORY_OF_CONTENDERS = "cuter_pokemon"


def generate_list_of_image_paths():
    contender_directory = os.path.join(os.getcwd(), DIRECTORY_OF_CONTENDERS)
    images = os.path.join(contender_directory, "*.png")

    pokemon_files = []

    for file in glob.glob(images):
        pokemon_files.append(file)

    return pokemon_files


def two_random_candidates(candidates):
    left = random.randrange(0, len(candidates))

    right = left
    while right == left:
        right = random.randrange(0, len(candidates))

    return candidates[left], candidates[right]


def generate_name_and_rank_from_image_path(path):
    base_path = os.path.basename(path)
    rank = base_path[:4]
    pokemon_name = base_path[4:].split(".")[0]
    # print(f"{pokemon_name} with rank {rank}")
    return pokemon_name, int(rank)


def update_dict_of_contenders(contenders, contender_to_add):
    # dictionary of Pokemon objects
    try:
        contenders[contender_to_add.name]
    except KeyError:
        contenders[contender_to_add.name] = contender_to_add

    return contenders


def single_head_to_head():
    # randomly pull out a pairing
    all_candidates = generate_list_of_image_paths()
    left_pathway, right_pathway = two_random_candidates(all_candidates)


    contenders = {}

    left_name, left_rank = generate_name_and_rank_from_image_path(left_pathway)
    left_pokemon = Pokemon(left_name, left_rank, left_pathway)
    contenders = update_dict_of_contenders(contenders, left_pokemon)

    right_name, right_rank = generate_name_and_rank_from_image_path(right_pathway)

    right_pokemon = Pokemon(right_name, right_rank, right_pathway)
    contenders = update_dict_of_contenders(contenders, right_pokemon)

    show_both_pokemon(left_pokemon, right_pokemon, contenders)



def show_both_pokemon(left_pokemon: Pokemon, right_pokemon: Pokemon, contenders):
    competition = HeadToHead((contenders[left_pokemon.name], contenders[right_pokemon.name]))

    left_image = left_pokemon.load_image_from_file()
    right_image = right_pokemon.load_image_from_file()

    scale = 2
    width = left_image.shape[1] * 2
    height = left_image.shape[0] * 2
    dim = (width, height)
    left_image = cv2.resize(left_image, dim)
    right_image = cv2.resize(right_image, dim)

    both_images = cv2.hconcat([left_image, right_image])
    cv2.imshow("both images", both_images)
    key_pressed = cv2.waitKey()

    competition_is_active = True
    while competition_is_active:
        # "a" was pressed.
        if key_pressed == 97:
            competition.declare_an_outcome_and_append_actual_scores("left")
            competition_is_active = False
            break
        # "b" was pressed
        if key_pressed == 100:
            competition.declare_an_outcome_and_append_actual_scores("right")
            competition_is_active = False
            break
        if key_pressed == 120 or key_pressed == -1:
            raise ValueError("Exited on purpose")

        # try again cuz bad key
        print(f"wrong key, you pressed {key_pressed}")
        key_pressed = cv2.waitKey()

    cv2.destroyAllWindows()
    competition.adjust_ranks_for_contenders()
    left_pokemon.rename_file()
    right_pokemon.rename_file()





if __name__ == "__main__":

    pokemon_counted = 0
    while True:
        single_head_to_head()
        pokemon_counted += 1
        print(f"You have compared {pokemon_counted} pokemon.")
