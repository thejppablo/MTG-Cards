from pathlib import Path

MTG_CARDS_FOLDER = Path(__file__).parent.joinpath("./Cards")
MTG_CARDS_RESULT_FOLDER = MTG_CARDS_FOLDER.joinpath("Result")
MTG_CARDS_COMPARE_FOLDER = MTG_CARDS_FOLDER.joinpath("Cards_to_compare")


FILE_OWNED_CARDS = "MTG_CARDS_FOR_COMMANDER_SPELLBOOK.txt"
FILE_TO_COMPARE = "Cards_Pato.txt"

def main():
    
    card_owned_hashmap = dict()
    cards_not_owned = set()
    for row in open(MTG_CARDS_RESULT_FOLDER.joinpath(FILE_OWNED_CARDS), "r").readlines():
        card_owned_hashmap[row.split(" ", 1)[-1].replace("\n", "")] = row.split(" ", 1)[0].replace("\n", "")
    for row in open(MTG_CARDS_COMPARE_FOLDER.joinpath(FILE_TO_COMPARE), "r").readlines():
        cards_not_owned.add(row.split(" ", 1)[-1].replace("\n", ""))
    for card in set(card_owned_hashmap.keys()).intersection(cards_not_owned):
        print(f"{card_owned_hashmap[card]} {card}")

if __name__ == '__main__':
    main()