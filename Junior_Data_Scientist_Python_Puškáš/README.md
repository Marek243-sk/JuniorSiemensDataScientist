# Dataset Comparison and Statistical Report  

## Overview  

This project compares two datasets — a Ground Truth dataset and a Modified dataset — and identifies differences based on configurable thresholds. It evaluates:  

- Differences in measurement values  
- Changes in missing values  
- Added or removed samples  
- Differences in statistical metrics  

The output is a well-structured HTML report highlighting these differences in a color-coded format.  

---

## Features  

- Comparison of numerical values with hierarchical threshold logic  
- Per-measurement and global threshold support  
- Statistical comparison of:  
  - Mean  
  - Standard Deviation  
  - Variance  
  - Min & Max  
  - Median  
  - 5th & 95th Percentiles  
- Color-coded HTML report generation  
- Missing value simulation and imputation using KNN  
- All parameters are configurable via a single JSON config file  

---

## Folder Structure

Siemens_Puškáš/  
```  Config/  
        config.json
    DATA/  
        Data.csv  
        Modified_data.csv  
    Solution_python/  
        comparison.py  
        main.py  
        preprocessing.py  
        reporting.py  
    Template/  
        comparison.csv  
        comparison.html  
    requirements.txt  
    README.md   

---

## The config.json file includes all parameters needed for the script:  

- Data paths (original and modified dataset)  
- Global and per-measurement thresholds  
- Thresholds for individual statistics  
- Modifications to simulate changes:  
    - Value changes  
    - Missing value handling  
    - Sample removal and addition  

## Output
- comparison.csv: CSV file showing individual value changes that exceed thresholds  
- comparison.html: report that visualizes statistical differences
