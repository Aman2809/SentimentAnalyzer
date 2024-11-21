## How to Set Up the Dataset
1. Make sure you have Python installed on your system.
2. Install the Kaggle Python package into your .ipnyb file:
   ```bash
   !pip install kaggle
   ```
3. Set up your Kaggle API key:
   - Download `kaggle.json` from [Kaggle](https://www.kaggle.com/account).
   - Place it in the directory `~/.kaggle/` (Linux/Mac) or `%USERPROFILE%\.kaggle\` (Windows).

4. Run the dataset download script:
   ```bash
   python download_dataset.py
   ```
5. The dataset will be downloaded and extracted into the `datasetFolder/` directory.

Now you can run the project as usual.
