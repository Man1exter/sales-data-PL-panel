# Sales Data Analysis and Visualization

This repository contains a set of Python scripts for analyzing and visualizing sales data in Poland from 2020 onwards. The project uses various libraries such as `pandas`, `matplotlib`, `seaborn`, `streamlit`, and `plotly` to process and visualize the data.

## Repository Structure

### Files and Directories

- **.vscode/settings.json**: Contains VS Code settings, including custom dictionary words for spell checking.
- **Excel-Python/przykladowe_dane_produkcja.xlsx**: An Excel file with sample production data.
- **Excel-Python/wizualizacja_kosztow.py**: A script for visualizing production costs using data from the Excel file.
- **main.py**: The main script for the Streamlit application that provides an analytical dashboard for sales data.
- **pre-demo.py**: A pre-demo version of the main script with additional functionalities for displaying aggregated sales statistics.

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/your-username/sales-data-analysis.git
    cd sales-data-analysis
    ```

2. Install the required Python packages:
    ```sh
    pip install -r requirements.txt
    ```

## Usage

### Running the Streamlit Application

To run the main Streamlit application, use the following command:
```sh
streamlit run main.py
```
Scripts Overview
main.py
This script defines a Streamlit application that provides an analytical dashboard for sales data. It includes functionalities for:

Fetching data from the Main Statistical Office (GUS) and company systems.
Processing and merging the data.
Visualizing sales dynamics, channel shares, and sales by category.
Filtering data based on user inputs.
pre-demo.py
This script is a pre-demo version of the main Streamlit application. It includes additional functionalities for displaying aggregated sales statistics over a selected period.

wizualizacja_kosztow.py
This script loads production cost data from an Excel file and visualizes it using matplotlib and seaborn. It includes:

Bar plots for labor and packaging costs.
Line plots for cumulative labor costs.
Pie charts for the share of costs by department and packaging type.
Analysis of packaging costs per unit.

License
This project is licensed under the MIT License. See the LICENSE file for details.

Acknowledgements
pandas
matplotlib
seaborn
streamlit
plotly
Contact
For any questions or suggestions, please contact