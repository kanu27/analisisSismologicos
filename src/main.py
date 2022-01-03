import pandas as pd
import numpy as np
import matplotlib


def getData():
    df = pd.read_csv(
        'src/data/sismosMundiales.csv',
        sep=","
        )
    df = df.fillna(0)
    dfCovid = pd.DataFrame(data=df)
    return dfCovid




if __name__ == "__main__":
    getData()



