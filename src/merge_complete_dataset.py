import os
import pandas as pd
from tqdm import tqdm

# Define the root path of the raw data
base_data_path = "../data/raw"
metadata_path = os.path.join(base_data_path, "metadata.xlsx")

# Load metadata from the Excel file
metadata_df = pd.read_excel(metadata_path, sheet_name='Planilha1')

# Rename columns for easier access
metadata_df.columns = ['Subfolder', 'Emission_Point', 'Wind_Direction', 'Wind_Speed', 'Emission_Interval', 'Height']

# Initialize list to collect each DataFrame
all_dataframes = []

# Use tqdm to show progress
for _, row in tqdm(metadata_df.iterrows(), total=len(metadata_df), desc="Merging data"):
    emission_point = row['Emission_Point']
    subfolder = row['Subfolder']
    folder_path = os.path.join(base_data_path, emission_point, subfolder)
    data_file_path = os.path.join(folder_path, "particle_devc.csv")

    if os.path.exists(data_file_path):
        try:
            df = pd.read_csv(data_file_path)

            # Adiciona metadados
            df["Emission_Point"] = emission_point
            df["Subfolder"] = subfolder
            df["Wind_Direction"] = row["Wind_Direction"]
            df["Wind_Speed"] = row["Wind_Speed"]
            df["Emission_Interval"] = row["Emission_Interval"]
            df["Height"] = row["Height"]

            all_dataframes.append(df)

        except Exception as e:
            print(f"Error reading {data_file_path}: {e}")
    else:
        print(f"File not found: {data_file_path}")

# Combinação final
if all_dataframes:
    complete_df = pd.concat(all_dataframes, ignore_index=True)

    # Ajusta o cabeçalho correto
    new_header = complete_df.iloc[0]
    complete_df = complete_df[1:]
    complete_df.columns = list(new_header)[:-6] + [
        "Emission_Point", "Subfolder", "Wind_Direction", "Wind_Speed", "Emission_Interval", "Height"
    ]

    # 🧠 Conversão de colunas numéricas
    for col in complete_df.columns:
        if col not in ["Emission_Point", "Subfolder"]:  # evita converter colunas categóricas
            complete_df[col] = pd.to_numeric(complete_df[col], errors='coerce')

    # 🔍 Checa se ainda restam colunas não numéricas
    non_numeric_cols = complete_df.select_dtypes(include='object').columns.tolist()
    if non_numeric_cols:
        print(f"⚠️ Atenção: as seguintes colunas permanecem com tipo 'object': {non_numeric_cols}")

    # Cria pasta de saída
    output_path = "../data/processed"
    os.makedirs(output_path, exist_ok=True)

    # Salva o dataset final
    complete_df.to_csv(os.path.join(output_path, "complete_dataset.csv"), index=False)
    print("✅ Dataset salvo com sucesso em '../data/processed/complete_dataset.csv'")
else:
    print("⚠️ Nenhum dado foi encontrado. Verifique os caminhos e o arquivo metadata.")
