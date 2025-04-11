import pandas as pd
from pathlib import Path
import json
from preprocessing import load_and_clean_data, apply_modifications
from comparison import compare_values, compare_statistics
from reporting import generate_statistics_report

def main():
    # Get the base project directory (up one level from the script's location)
    base_path = Path(__file__).resolve().parent.parent

    # Load configuration file
    config_path = base_path / "Config" / "config.json"
    with open(config_path) as file:
        config = json.load(file)

    # Load the original dataset
    gt_path = base_path / config["data"]["gt_path"]
    df = load_and_clean_data(gt_path)

    # Apply modifications to the dataset based on config
    modified_df = apply_modifications(df.copy(), config)

    # Save the modified dataset
    modified_path = base_path / config["data"]["modified_data_path"]
    modified_df.to_csv(modified_path, index=False)

    # Compare original and modified datasets for value differences
    value_diff = compare_values(df, modified_df,
                                config["comparison"]["global_threshold"],
                                config["comparison"]["per_measurement_thresholds"])

    # Ensure the output directory exists and save value comparison
    (base_path / "Template" / "comparison.csv").parent.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(value_diff).to_csv(base_path / "Template" / "comparison.csv", index=False)

    # Identify numerical columns for statistical comparison
    numerical_attributes = df.select_dtypes(include=["float64", "int64"]).columns.tolist()

    # Compare statistics between the original and modified datasets
    stat_diff = compare_statistics(df, modified_df,
                                   numerical_attributes,
                                   config["statistics_comparison"]["global_threshold"],
                                   config["statistics_comparison"]["per_statistic_thresholds"])

    # Generate an HTML report based on the statistical differences
    html = generate_statistics_report(stat_diff)
    with open(base_path / "Template/comparison.html", "w", encoding="utf-8") as f:
        f.write(html)

    print("DONE! Report and comparison saved.")

if __name__ == "__main__":
    main()
