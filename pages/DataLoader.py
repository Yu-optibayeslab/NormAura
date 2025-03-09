import streamlit as st
import pandas as pd
import numpy as np
import os

def load_csv_data(file_path):
    try:
        data = pd.read_csv(file_path)
        return data
    except Exception as e:
        st.error(f"Error loading CSV file: {e}")
        return None

def app():
    st.title("NormAura: Data loading page.")
    # Initialize session state for working_directory
    if "working_directory" not in st.session_state:
        st.session_state["working_directory"] = []

    DEFUALT_WORKING_DIRECTORY = os.getcwd()
    # Working Directory input
    working_directory = st.text_input("Enter Your Working Directory:", value = "", key="working_directory_input")
    st.write(f"Current Directory is: {DEFUALT_WORKING_DIRECTORY}")
    
    # Store the working directory in session state
    if working_directory:
        st.session_state["working_directory"] = working_directory
        os.makedirs(working_directory, exist_ok=True)
        st.success(f"Working Directory Set: {working_directory}")
            # Display the working directory
        if "working_directory" in st.session_state:
            st.write(f"Current Working Directory: {st.session_state['working_directory']}")
            inputs_dir = os.path.join(working_directory, "inputs")
            outputs_dir = os.path.join(working_directory, "outputs")
            st.session_state["inputs_directory"] = inputs_dir
            st.session_state["outputs_directory"] = outputs_dir
            st.success(f"Please move all raw .csv data files to: {inputs_dir}! .")
            st.warning(f"The files downloaded in the actions will be savd as the default download directoy of your webbrowser. \
                        Please move them to {outputs_dir} as they may needed in further actions! ")
            os.makedirs(inputs_dir, exist_ok=True)
            os.makedirs(outputs_dir, exist_ok=True)
            inputs_directory = st.session_state["inputs_directory"]

            # Process CSVs in the directory
            if inputs_directory and os.path.isdir(inputs_directory):
                csv_files = [f for f in os.listdir(inputs_directory) if f.endswith(".csv")]
                ##############################
                # Sidebar for chunk settings #
                ##############################
                if csv_files:
                    # Dropdown to select a document
                    selected_csv = st.sidebar.selectbox(
                        "Select a csv file",
                        options=csv_files,
                        index=None  # No document is selected by default
                    )
                    # Clear session state if a new CSV file is selected
                    if "selected_csv" in st.session_state and st.session_state.selected_csv != selected_csv:
                        st.session_state.selected_csv = ""  # Reset only the selected_csv key
                    st.session_state.selected_csv = selected_csv  # Update the selected CSV in session state
        
                    if st.session_state.selected_csv:
                        file_path = os.path.join(inputs_directory, selected_csv)
                        # Data Loading
                        if st.sidebar.button("Load CSV Data", key="unique_key_0"):
                            data = load_csv_data(file_path)
                            if data is not None:
                                st.session_state["raw_data"] = data
                                st.success(f"CSV data loaded from: {file_path}!")
                                st.session_state["preprocessed_data"] = data
                                st.dataframe(st.session_state["raw_data"])  # Display the loaded data
                                # Identify columns that have any NaN values
                                nan_columns = data.columns[data.isna().any()].tolist()
                                if nan_columns:
                                    st.write("Columns with NaN values:", nan_columns)# Display the list of columns with NaN values
                            else:
                                st.error("Failed to load data.")
                    if "raw_data" not in st.session_state:
                        st.warning("Please load the CSV data from the sidebar.")
                        return
                else:
                    st.sidebar.error(f"No .csv files found!!! \n ### Please move your .csv files to the {inputs_dir} ###")
    else:
        st.warning("Please enter the directory!")
