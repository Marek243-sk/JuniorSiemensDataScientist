import pandas as pd

def compare_values(gt_df, mod_df, global_threshold, thresholds):
    results = []

    # Iterate through all columns in the ground truth dataframe
    for column in gt_df.columns:
        if column in mod_df.columns:
            # Compare each row for the given column
            for idx in gt_df.index:
                orig = gt_df.at[idx, column]
                mod = mod_df.at[idx, column]

                # Ensure both values are numbers and not NaN
                if pd.notna(orig) and pd.notna(mod) and isinstance(orig, (int, float)) and isinstance(mod, (int, float)):
                    # Use column-specific threshold or fall back to global threshold
                    thresh = thresholds.get(column, global_threshold)

                    # Calculate relative difference and check against threshold
                    if orig != 0:
                        diff = abs(orig - mod) / abs(orig)
                        if diff > thresh:
                            results.append({
                                "index": idx,
                                "column": column,
                                "original_value": orig,
                                "modified_value": mod,
                                "difference_percentage": diff
                            })

    return results

def compare_statistics(gt_df, mod_df, attributes, global_threshold, thresholds):
    # List of statistics to compare
    stats = ["Mean", "Std", "Variance", "Max", "Min", "Median", "5th Percentile", "95th Percentile"]
    diffs = []

    # Iterate through each attribute and each statistic
    for attr in attributes:
        for stat in stats:
            # Calculate the statistic for both original and modified data
            gt_val = calculate_stat(gt_df[attr], stat)
            mod_val = calculate_stat(mod_df[attr], stat)

            # Check for valid numbers and calculate relative difference
            if pd.notna(gt_val) and pd.notna(mod_val) and gt_val != 0:
                diff = abs(gt_val - mod_val) / abs(gt_val)
                threshold = thresholds.get(stat, global_threshold)

                # Only record if the difference exceeds the threshold
                if diff > threshold:
                    diffs.append({
                        "attribute": attr,
                        "statistic": stat,
                        "gt_value": gt_val,
                        "modified_val": mod_val,
                        "percent_difference": diff,
                        "threshold": threshold
                    })

    return diffs

def calculate_stat(series, stat):
    # Calculate specific statistic from pandas Series
    if stat == "Mean": return series.mean()
    if stat == "Std": return series.std()
    if stat == "Variance": return series.var()
    if stat == "Max": return series.max()
    if stat == "Min": return series.min()
    if stat == "Median": return series.median()
    if stat == "5th Percentile": return series.quantile(0.05)
    if stat == "95th Percentile": return series.quantile(0.95)
