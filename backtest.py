import pandas as pd
import math

csv_files = ""
chunk_size = 100000

range = input("Entrez un range en pourcentage : ")
duree = input("Sur combien de temps faire le backtest :")


# Always having the good decimals for post calcul
def decimals(chunk):
    if chunk["decimals1"] > chunk["decimals0"]:
        return chunk["decimals1"] - chunk["decimals0"]
    else:
        return chunk["decimals0"] - chunk["decimals1"]


def liquidity(chunk):

    # put price in dollar
    price = (1.0001 ** chunk["tick"]) / (10 ** decimals(chunk))

    # define range
    low_range = price * (1 - range / 200)
    high_range = price * (1 + range / 200)

    # range tick
    bottom_tick = round(
        math.floor(10 ** decimals(chunk) / low_range) / math.floor(1.0001)
    )
    top_tick = round(
        math.floor(10 ** decimals(chunk) / high_range) / math.floor(1.0001)
    )

    # sa sb sp
    sa = math.sqrt(1.0001**top_tick)
    sb = math.sqrt(1.0001**bottom_tick)
    sp = (1.0001 ** chunk["tick"]) ** 0.5

    # Amount of token0
    amount0 = chunk["liquidity"] * (sb - sp) / (sb * sp) / chunk["decimals0"]
    amount1 = chunk["liquidity"] * (sp - sa) / chunk["decimals1)"]

    # Total liquidity for that range
    total_liquidity = amount0 + (amount1 * price)

    return total_liquidity


def fee(chunk):

    # Calcul les frais sur l'UT pour 1$
    fee = chunk["volume"] / liquidity(chunk) * chunk["fee"]

    return fee

results = []

for i, chunk in enumerate(pd.read_csv(csv_file, chunksize=chunk_size)):
    print(f"Processing chunk {i + 1}")
    processed_chunk = fee(chunk)
    results.append(processed_chunk)

rendement = sum(results)
