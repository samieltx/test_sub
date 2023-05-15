import pandas as pd
from tienda_amiga.cfg import DATA_DIR

def transform():
    # TODO: Apply transformations
    df = pd.read_csv(DATA_DIR / "data.csv")
    df.to_csv(DATA_DIR / "data_transformed.csv", index=False)
