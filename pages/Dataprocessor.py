import streamlit as st
import pandas as pd
import numpy as np
# Import your custom classes (adjust paths as needed)
from dataprocessors import DataCleaner, MissingDataHandler, DimensionalityReducer
import os
import json

def app():
    # Retrieve raw data from session state
    data = st.session_state.get("raw_data", None)
    preprocessed_data = data.copy()
    
    # Initialize processing classes
    cleaner = DataCleaner()
    missing_handler = MissingDataHandler()
    reducer = DimensionalityReducer()

    st.title("NormAura: Data processing page.")
    
    st.write("## Processing Steps ##")
    num_rows_all_nan = data.isna().any(axis=1).sum() # Check the number of rows with nan values
    if num_rows_all_nan:
        st.error(f"### Missing data found. \nNumber of rows contains nan: {num_rows_all_nan}.\n \
                Please handle the missing data using a function in the sidebar ###")# Display the number of rows with nan values

    num_duplicated_rows = data.duplicated(keep=False).sum() #Check the number of duplicated rows in a pandas DataFrame
    if num_duplicated_rows:
        st.warning(f"### Duplicated rows (including all occurrences): {num_duplicated_rows}.\n \
                Please remove the duplicates using the function in the sidebar ###")

    # Data Cleansing Options
    st.sidebar.markdown("---")  # Shortcut for <hr> in Markdown
    if st.sidebar.button("Remove duplicates", key="unique_key_2"):
        preprocessed_data = cleaner.remove_duplicates(preprocessed_data)
        st.success(f"Duplicates are removed!\n")
    st.sidebar.markdown("---")  # Shortcut for <hr> in Markdown
    st.sidebar.subheader("Data Cleansing")
    outlier_method = st.sidebar.selectbox("Outlier Method", options=["iqr", "zscore"])
    if st.sidebar.button("Remove Outliers", key="unique_key_1"):
        # Perform outlier removal action here
        preprocessed_data = cleaner.remove_outliers(preprocessed_data, method=outlier_method)
        st.success(f"Outliers are removed using method: **{outlier_method}**")

    st.sidebar.markdown("---")  # Shortcut for <hr> in Markdown  
    # Missing Data Handling Options
    st.sidebar.subheader("Missing Data Handling")
    imputation_method = st.sidebar.selectbox("Imputation Method", options=["remove nan", "mean", "median", "simple", "knn", "mice"])
    
    if st.sidebar.button("Handle missing Data", key="unique_key_3"):
        st.write("### Missing Data Handling")
        if imputation_method == "mean":
            preprocessed_data = missing_handler.mean_imputation(preprocessed_data)
        elif imputation_method == "median":
            preprocessed_data = missing_handler.median_imputation(preprocessed_data)
        elif imputation_method == "most_frequent":
            preprocessed_data = missing_handler.mode_imputation(preprocessed_data)
        elif imputation_method == "knn": 
            preprocessed_data = missing_handler.knn_imputation(preprocessed_data)
        elif imputation_method == "mice": 
            preprocessed_data = missing_handler.mice_imputation(preprocessed_data)
        else:
            # The last is reserved for Removing rows with any NaN values
            preprocessed_data == preprocessed_data.dropna()
            
        st.success(f"Missing Data are filled using method: **{imputation_method}**")

    st.sidebar.markdown("---")  # Shortcut for <hr> in Markdown    
    # Save the processed data in session state
    st.session_state["preprocessed_data"] = preprocessed_data

    st.write("Processed data is now available for visualizations on the **Visualizations** page.")

    # --- Save Processed Data ---
    st.sidebar.subheader("~~~~~~ Save Processed Data ~~~~~~")
    save_format = st.sidebar.selectbox("Select file format", options=["CSV", "JSON"])

    output_dir = st.session_state["outputs_directory"]
    if st.sidebar.button("Save Data", key="unique_key_5"):
        #os.makedirs(output_dir, exist_ok=True)
        if save_format == "CSV":
            csv_data = preprocessed_data.to_csv(index=False)
            filename = os.path.join(output_dir, "preprocessed_data.csv")
            st.sidebar.write(f"saving {filename}")
            preprocessed_data.to_csv(filename, index=False)
        else:
            json_data = preprocessed_data.to_json(orient="records")
            filename = os.path.join(output_dir, "preprocessed_data.json")
            st.sidebar.write(f"saving {filename}")
            with open(filename, "w") as f:
                json.dump(json_data, f, indent=4)
