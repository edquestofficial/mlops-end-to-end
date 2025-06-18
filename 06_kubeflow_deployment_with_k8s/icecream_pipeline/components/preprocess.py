import pandas as pd

def preprocess(output_csv_path: str):

    df = pd.read_csv("data/ice_cream.csv")  # Bundled inside image or mounted
    df.to_csv(output_csv_path, index=False)
    print(f"Preprocessed data saved to: {output_csv_path}")
