import streamlit as st
import pandas as pd
import numpy as np
# Import your custom classes (adjust paths as needed)
from dataprocessors import DataNormaliser, DimensionalityReducer
import os
import json

def app():
    # Retrieve raw data from session state
    processed_data = st.session_state.get("preprocessed_data", None)
    
    # Initialize processing classes
    transformer = DataNormaliser()
    #inverse_transform_data = DataNormaliser.inverse_transform()
    reducer = DimensionalityReducer()

    st.title("NormAura: Data transforming page.")
    st.write("## Processing Steps ##")
    
    # Data Normalisation Options
    st.sidebar.markdown("---")  # Shortcut for <hr> in Markdown   
    #st.sidebar.subheader("Data normalisation")
    data_normalisation = st.sidebar.checkbox("Data normalisation")
    if data_normalisation:
        st.sidebar.info("Please select the normalisation approaches in the main window!")

        # Get the list of columns
        columns = processed_data.columns.tolist()

        # Option to apply the same normalisation method to all columns
        st.subheader("Global normalisation")
        global_method = st.selectbox(
                "Select a normalisation method to apply to ALL columns",
                options=["none", "minmax", "standard", "robust", "l2", "log", "power"],
                key="global_method",
            )

        # Let the user select normalisation methods for each column (if global method is "none")
        normalisation_methods = {}
        if global_method == "none":
            st.subheader("Column-wise normalisation")
            for column in columns:
                method = st.selectbox(
                        f"Select normalisation method for column '{column}'",
                        options=["none", "minmax", "standard", "robust", "l2", "log", "power"],
                        key=column,
                    )
                if method != "none":
                    normalisation_methods[column] = method
        else:
            # Apply the global method to all columns
            for column in columns:
                normalisation_methods[column] = global_method

        st.write(f"normalisation_methods:\n{normalisation_methods}")

        # normalise the data if methods are selected
        if normalisation_methods:
            if st.button("normalise Data", key="normaliser"):
                normalised_data, scalers = transformer.normalise_data(processed_data, normalisation_methods)
                st.session_state["normalised_data"] = normalised_data
                st.session_state["scalers"] = scalers
                st.subheader("Normalised Data")
                st.write(normalised_data)
                st.subheader("Normalisation approaches")
                st.write(scalers)

        # --- Save Normalised Data ---
        output_dir = st.session_state["outputs_directory"]
        st.sidebar.subheader("~~ Save Normalised Data ~~")
        save_format = st.sidebar.selectbox("Select file format", options=["CSV", "JSON"])
        if st.sidebar.button("Save Normalised Data", key="save_normalised_data"):
            if "normalised_data" in st.session_state and "scalers" in st.session_state:
                normalised_data = st.session_state["normalised_data"]
                scalers = st.session_state["scalers"]
                if save_format == "CSV":
                    # Save normalised data
                    file_name = os.path.join(output_dir, "normalised_data.csv")
                    st.sidebar.write(f"saving {file_name}")
                    normalised_data.to_csv(file_name, index=False)
                    # Save scalers as JSON
                    scalers_filename = os.path.join(output_dir, "normalisation_methods.json")
                    st.sidebar.write(f"saving {scalers_filename}")
                    with open(scalers_filename, "w") as f:
                            json.dump({k: {"method": normalisation_methods[k]} for k in normalisation_methods}, f)
                else:
                    # Save normalised data and scalers together in a single JSON file
                    combined_data = {
                        "normalised_data": normalised_data.to_dict(orient="records"),
                        "scalers": {k: {"method": normalisation_methods[k]} for k in normalisation_methods}
                        }
                    jsonname = os.path.join(output_dir, "normalised_data_and_methods.json")
                    st.sidebar.write(f"saving {jsonname}")
                    with open(jsonname, "w") as f:
                        json.dump(combined_data, f, indent=4)
            else:
                st.warning("No normalised data found. Please normalise the data first.")
    
    # Dimensionality Reduction Options
    st.sidebar.markdown("---")  # Shortcut for <hr> in Markdown   
    st.sidebar.subheader("Dimensionality Reduction")
    #perform_reduction = st.sidebar.checkbox("Perform Dimensionality Reduction", value=True)
    data_to_be_reduced = st.sidebar.selectbox("Which data to be reduced", \
                                                options=["--- select an data type ---", "raw_data", "preprocessed_data", "normalised_data"])
    if data_to_be_reduced:
        if data_to_be_reduced == "preprocessed_data":
            data = st.session_state.get("preprocessed_data", None)
        elif data_to_be_reduced =="normalised_data":
            data = st.session_state.get("normalised_data", None)
        else:
            data = st.session_state.get("raw_data", None)


        reduction_method = st.sidebar.selectbox("Reduction Method", options=["--- select an approach ---", "pca", "tsne"])
        if reduction_method == "pca":
            columns_to_drop = st.sidebar.multiselect(
                            "Select features to be excluded in the PCA analysis:",
                            options=data.columns,  # All columns are available for selection
                            default=None  # No columns selected by default
                        )
            features = data.drop(columns=columns_to_drop)
            n_components = st.sidebar.text_input("Number of Components", value="2")  # Default value is 2
            n_components = int(n_components)
            if st.sidebar.button("Reducing Dimensionality", key="Reducing_Dimensionality"):
                reduced = reducer.pca(features, n_components=n_components)
                reduced_df = pd.DataFrame(reduced, columns=[f"PC{i+1}" for i in range(n_components)])
                reduced_df[columns_to_drop] = data[columns_to_drop].values
                st.write("Reduced Data:")
                st.write(reduced_df)
                # Save reduced data in session state so it can be used in the visualizations page
                st.session_state["reduced_data"] = reduced_df

        elif reduction_method == "tsne":
            columns_to_drop = st.sidebar.multiselect(
                            "Selected variables to be excluded in the TSNE analysis:",
                            options=data.columns,  # All columns are available for selection
                            default=None  # No columns selected by default
                        )
            features = data.drop(columns=columns_to_drop)
            n_components = st.sidebar.text_input("Number of Components", value="2")  # Default value is 2
            n_components = int(n_components)
            perplexity = st.sidebar.text_input("Perplexity", value="30")  # Default value is 2
            perplexity = int(perplexity)
            n_iter = st.sidebar.text_input("Number of iterations (n_iter)", value="1000")  # Default value is 1000
            n_iter = int(n_iter)
        
            if st.sidebar.button("Reducing Dimensionality", key="Reducing_Dimensionality"):
                random_state = 42
                reduced = reducer.tsne(features, n_components=n_components, perplexity=perplexity, random_state=random_state)
                reduced_df = pd.DataFrame(reduced, columns=[f"PC{i+1}" for i in range(n_components)])
                reduced_df[columns_to_drop] = data[columns_to_drop].values
                st.write("Reduced Data:")
                st.write(reduced_df)
                # Save reduced data in session state so it can be used in the visualizations page
                st.session_state["reduced_data"] = reduced_df

        else:
            if st.sidebar.button("Reducing Dimensionality", key="Reducing_Dimensionality"):
                st.sidebar.error("No method selected! Please select a dimensionality reducing approach from the droplist!!!")