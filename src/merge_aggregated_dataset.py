import os
import pandas as pd
from tqdm import tqdm

# File paths
METADATA_PATH = "../data/raw/metadata.xlsx"
BASE_DATA_PATH = "../data/raw"
AGG_OUTPUT_PATH = "../data/processed/aggregated_dataset.csv"

def load_metadata():
    """
    Loads the metadata Excel file and creates a dictionary of metadata indexed by (TAG, Locais de emissão).
    Handles duplicate rows by keeping the first occurrence and warning the user.

    Returns:
        dict: Metadata dictionary indexed by (TAG, Locais de emissão).
    """
    df = pd.read_excel(METADATA_PATH)
    df.columns = [col.strip() for col in df.columns]
    df.rename(columns={"TAG (SUBPASTA)": "TAG"}, inplace=True)

    # Check for duplicates in TAG + Local combination
    duplicate_mask = df.duplicated(subset=["TAG", "Locais de emissão"], keep=False)
    if duplicate_mask.any():
        print("⚠️ Warning: Duplicate (TAG, Locais de emissão) combinations found:")
        print(df[duplicate_mask])
        df = df.drop_duplicates(subset=["TAG", "Locais de emissão"], keep='first')

    return df.set_index(["TAG", "Locais de emissão"]).to_dict(orient="index")


def extract_aggregated_features(devc_path):
    """
    Extracts statistical features from particle_devc.csv by summarizing
    sensor values over time. Calculates mean, std, max, min for each sensor.

    Args:
        devc_path (str): Path to particle_devc.csv

    Returns:
        pd.Series: A row of aggregated statistics as a flat feature vector.
    """
    df = pd.read_csv(devc_path, skiprows=1)
    df.columns = df.iloc[0]  # Reset headers using second row
    df = df[1:]  # Drop header row
    df = df.apply(pd.to_numeric, errors='coerce')  # Convert all values to numeric

    # Drop Time column if it exists
    df = df.drop(columns=["Time"], errors="ignore")

    # Aggregate statistics per sensor (mean, std, max, min)
    stats = df.agg(['mean', 'std', 'max', 'min']).transpose()
    stats.columns = [f"{col}_{stat}" for stat in stats.columns for col in [stats.index.name]]
    stats = stats.reset_index(drop=True).iloc[0]
    return stats

def build_dataset_agregado():
    """
    Builds an aggregated dataset where each row corresponds to one simulation (subfolder),
    containing statistical summaries of sensor readings plus configuration metadata and labels.

    Output:
        CSV file saved at AGG_OUTPUT_PATH
    """
    metadata_dict = load_metadata()
    data_rows = []

    all_emission_points = ["E1", "E2", "E3"]
    total = sum(len(os.listdir(os.path.join(BASE_DATA_PATH, ep))) for ep in all_emission_points if os.path.isdir(os.path.join(BASE_DATA_PATH, ep)))

    with tqdm(total=total, desc="Building Aggregated Dataset") as pbar:
        for emission_point in all_emission_points:
            point_path = os.path.join(BASE_DATA_PATH, emission_point)
            if not os.path.isdir(point_path):
                continue

            for tag in os.listdir(point_path):
                tag_path = os.path.join(point_path, tag)
                devc_path = os.path.join(tag_path, "particle_devc.csv")

                if not os.path.isfile(devc_path):
                    pbar.update(1)
                    continue

                key = (tag, emission_point)
                if key not in metadata_dict:
                    print(f"Metadata not found for: {key}")
                    pbar.update(1)
                    continue

                try:
                    sensor_stats = extract_aggregated_features(devc_path)
                    meta = metadata_dict[key]

                    row = sensor_stats.to_dict()
                    row.update(meta)
                    row["classe"] = emission_point
                    row["tag"] = tag

                    data_rows.append(row)
                except Exception as e:
                    print(f"Error processing {devc_path}: {e}")

                pbar.update(1)

    df_final = pd.DataFrame(data_rows)
    os.makedirs(os.path.dirname(AGG_OUTPUT_PATH), exist_ok=True)
    df_final.to_csv(AGG_OUTPUT_PATH, index=False)
    print(f"Aggregated dataset saved to: {AGG_OUTPUT_PATH}")

# Optional: call directly for testing
if __name__ == "__main__":
    build_dataset_agregado()
