import os
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from tqdm import tqdm

RAW_DATA_PATH = "../data/raw"
METADATA_PATH = os.path.join(RAW_DATA_PATH, "metadata.xlsx")
OUTPUT_PATH = "../data/processed/timeseries_dataset.csv"
WINDOW_SIZE = 30
STRIDE = 10

def load_metadata():
    df = pd.read_excel(METADATA_PATH)
    df.columns = [col.strip() for col in df.columns]
    df.rename(columns={"TAG (SUBPASTA)": "TAG"}, inplace=True)
    return df.set_index(["TAG", "Locais de emissão"]).to_dict(orient="index")

def create_windows(data, label, window_size=30, stride=10):
    for i in range(0, len(data) - window_size + 1, stride):
        window = data[i:i+window_size]
        if window.shape[0] == window_size:
            yield window.flatten(), label

def build_dataset_timeseries():
    metadata = load_metadata()
    all_emission_points = ["E1", "E2", "E3"]
    total_tags = sum(len(os.listdir(os.path.join(RAW_DATA_PATH, classe))) for classe in all_emission_points)

    header_written = False
    with tqdm(total=total_tags, desc="Building Time Series Dataset") as pbar:
        for classe in all_emission_points:
            class_path = os.path.join(RAW_DATA_PATH, classe)
            if not os.path.isdir(class_path):
                continue
            for tag in os.listdir(class_path):
                tag_path = os.path.join(class_path, tag)
                csv_path = os.path.join(tag_path, "particle_devc.csv")

                if not os.path.isfile(csv_path):
                    pbar.update(1)
                    continue

                key = (tag, classe)
                if key not in metadata:
                    pbar.update(1)
                    continue

                try:
                    df = pd.read_csv(csv_path, skiprows=1)
                    df.columns = df.columns.str.strip()

                    if 'mass' in df.columns:
                        df = df.drop(columns=['mass'])

                    sensor_cols = [col for col in df.columns if col != 'Time']
                    scaler = StandardScaler()
                    df[sensor_cols] = scaler.fit_transform(df[sensor_cols])
                    data = df[sensor_cols].values

                    rows = []
                    for x_flat, label in create_windows(data, classe, window_size=WINDOW_SIZE, stride=STRIDE):
                        rows.append(np.append(x_flat, label))

                    if rows:
                        df_batch = pd.DataFrame(rows)
                        df_batch.columns = [f"f{i}" for i in range(df_batch.shape[1] - 1)] + ["classe"]
                        os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
                        df_batch.to_csv(OUTPUT_PATH, mode='a', header=not header_written, index=False)
                        header_written = True

                except Exception as e:
                    print(f"Erro ao processar {csv_path}: {e}")

                pbar.update(1)

    print(f"✅ Time series dataset saved incrementally to: {OUTPUT_PATH}")

if __name__ == "__main__":
    build_dataset_timeseries()