import pandas as pd
import numpy as np
from sklearn.impute import KNNImputer

def load_and_clean_data(path: str) -> pd.DataFrame:
    # Load data from CSV file using semicolon as separator
    df = pd.read_csv(path, sep=";")

    # Replace spaces in column names with underscores for consistency
    df.columns = [col.replace(" ", "_") for col in df.columns]

    # Define numeric columns to be cleaned and converted
    num_attrs = ["Val_1", "Val_2", "Val_3", "Val_A", "Val_B", "Val_C", "Val_X", "Val_Y", "Val_Z"]

    # Convert values from string to numeric, replacing comma with dot (European decimal format)
    for attr in num_attrs:
        df[attr] = pd.to_numeric(df[attr].astype(str).str.replace(",", "."), errors="coerce")

    # Use KNN imputer to fill missing values based on nearest neighbors
    imputer = KNNImputer(n_neighbors=7)
    df[num_attrs] = imputer.fit_transform(df[num_attrs])

    return df

def apply_modifications(df: pd.DataFrame, config: dict) -> pd.DataFrame:
    # Create a copy to avoid modifying the original dataframe
    new_df = df.copy()

    # Set a fixed random seed for reproducibility
    np.random.seed(1234)

    # === Value modifications ===

    for attr, settings in config["modifications"]["value_modifications"].items():
        # Calculate how many rows to modify
        n = int(len(new_df) * settings["percent_to_modify"])
        rows = np.random.choice(new_df.index, n, replace=False)

        # Apply the increase or decrease operation
        if settings["operation"] == "increase_percent":
            new_df.loc[rows, attr] *= (1 + settings["value"])
        else:
            new_df.loc[rows, attr] *= (1 - settings["value"])

    # === Missing value modifications ===
    
    # Randomly choose rows and set some columns to NaN
    nan_rows = np.random.choice(new_df.index, config["modifications"]["missing_value_changes"]["num_to_nan"], replace=False)
    for row in nan_rows:
        cols = np.random.choice(new_df.columns, size=np.random.randint(1, 4), replace=False)
        new_df.loc[row, cols] = np.nan

    # Fill in random values into some previously missing cells
    nan_to_num_rows = np.random.choice(new_df.index, config["modifications"]["missing_value_changes"]["nan_to_num"], replace=False)
    for row in nan_to_num_rows:
        for col in new_df.columns:
            if pd.isna(new_df.at[row, col]):
                new_df.at[row, col] = np.random.random()

    # === Sample modifications ===

    # Remove a specified number of rows
    remove_n = config["modifications"]["sample_changes"]["remove"]
    add_n = config["modifications"]["sample_changes"]["add"]
    rows_to_remove = np.random.choice(new_df.index, remove_n, replace=False)
    new_df = new_df.drop(rows_to_remove)

    # Add new synthetic rows with random values
    new_rows = pd.DataFrame(np.random.random(size=(add_n, new_df.shape[1])), columns=new_df.columns)
    new_df = pd.concat([new_df, new_rows], ignore_index=True)

    return new_df
