import os
import zipfile
from kaggle.api.kaggle_api_extended import KaggleApi

def download_and_extract_kaggle_dataset(dataset, output_folder, extracted_file):
    # Check if the dataset is already downloaded and extracted
    if os.path.exists(extracted_file):
        print(f"Dataset already exists at: {extracted_file}")
        return

    # Authenticate with Kaggle
    api = KaggleApi()
    api.authenticate()

    # Create output directory if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)

    # Download dataset
    print(f"Downloading dataset: {dataset}")
    api.dataset_download_files(dataset, path=output_folder, unzip=False)

    # Extract dataset
    zip_file = os.path.join(output_folder, f"{dataset.split('/')[-1]}.zip")
    print(f"Extracting {zip_file}")
    with zipfile.ZipFile(zip_file, 'r') as zip_ref:
        zip_ref.extractall(output_folder)
    os.remove(zip_file)  # Clean up zip file after extraction

    print(f"Dataset extracted to {output_folder}")

if __name__ == "__main__":
    dataset_id = "kazanova/sentiment140"
    output_folder = "./datasetFolder"
    extracted_file = os.path.join(output_folder, "training.1600000.processed.noemoticon.csv")  # Replace with the actual extracted file name
    download_and_extract_kaggle_dataset(dataset_id, output_folder, extracted_file)
