import pandas as pd
from pathlib import Path
from requests import get
from multiprocessing import Pool, cpu_count
from time import sleep
from tqdm import tqdm
from threading import Lock

request_lock = Lock()

MTG_CARDS_FOLDER = Path(__file__).parent.joinpath("./Cards")
MTG_CARDS_RESULT_FOLDER = Path(__file__).parent.joinpath("./Cards").joinpath("Result")

def get_info(args):
    cn, exp = args
    with request_lock:
        result = get(f"https://api.scryfall.com/cards/{exp}/{cn}")
        sleep(0.05)
        if result.status_code == 429:
            print("TOO MANY REQUESTS")
            exit()
        if result.status_code != 200:
            return ("ERROR", "ERROR", "ERROR")
    return (cn, exp, result.json())


def get_json_info(
    json_info: dict,
    info: str
):

    try:
        return str(json_info.get(info)).replace("\n", "").split("//")[0]
    except Exception:
        return "ERROR"

def main():
    file = MTG_CARDS_FOLDER.joinpath("./MTG_CARDS.csv")

    df = pd.read_csv(file)
    df["exp"] = df["exp"].str.strip()
    df = df.groupby(by=["cn", "exp"])["qt_cards"].sum().reset_index().sort_values(by=["qt_cards", "cn", "exp"], ascending=False).reset_index(drop=True)

    p = Pool(cpu_count())
    r = list(
        tqdm(
            p.imap(get_info, [*df[["cn", "exp"]].itertuples(index=False, name=None)]),
            desc="MTG Cards",
            total=df.shape[0],
        )
    )

    info_df = pd.DataFrame(r, columns=["cn", "exp", "info"])
    df = df.merge(info_df, how="left", on=["cn", "exp"])
    infos_to_get = [
        "name",
        "mana_cost",
        "cmc",
        "type_line",
        "oracle_text",
        "power",
        "toughness",
        "colors",
        "color_identity",
        "keywords",
        "legalities",
    ]

    for info in infos_to_get:
        df[info] = df["info"].apply(lambda json_info: get_json_info(json_info, info=info))

    df.drop(columns=["info"], inplace=True)
    df.to_csv(
        MTG_CARDS_RESULT_FOLDER.joinpath("./MTG_CARDS_RESULT.tsv"), sep="\t", index=False
    )

    with open(MTG_CARDS_RESULT_FOLDER.joinpath("./MTG_CARDS_FOR_COMMANDER_SPELLBOOK.txt"), mode="w",encoding="utf-8") as commander_spellbook:
        for data in df[["qt_cards", "name"]].itertuples(index=False, name=None):
            commander_spellbook.write(f"{data[0]}x {data[1]}\n")


if __name__ == "__main__":
    main()
