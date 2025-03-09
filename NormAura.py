import streamlit as st
import importlib
import os

def main():
    st.markdown(
        """
        <style>
        [data-testid="stSidebarNav"] {
            display: none;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # Custom Sidebar Title
    st.sidebar.title("NormAura")

    # Mapping from display names to module names
    pages = {
        "-- Select an Action --": "Welcome",
        "Raw Date Loader": "DataLoader",
        "Preprocessor": "Dataprocessor",
        "Transformer": "DataTransformer",
        "Visualisations": "Visualisation",
    }
    
    # Use a dropdown (selectbox) for navigation
    st.sidebar.subheader("Main Manue")
    selected_page = st.sidebar.selectbox("Actions:", list(pages.keys()))

    # Check if a valid page has been selected
    if selected_page == "-- Select an Action --":
        #module_name = pages[selected_page]
        #page_module = importlib.import_module(f"pages.{module_name}")
        #page_module.app()
        st.sidebar.info("Please select a action from the dropdown.")
    else:
        #st.sidebar.write(f"**Current Page:** {selected_page}")
        module_name = pages[selected_page]
        page_module = importlib.import_module(f"pages.{module_name}")
        page_module.app()

    # Markdown at the bottom of the page
    st.markdown(
        "---\n"  # Adds a horizontal line for separation
        "**NormAura** is a free, powerful tool for data processing and visualisation, developed by **OptiBayesLab**. "
        "Explore more AI tools created by us at [https://optibayeslab.com/products](https://optibayeslab.com/products).\n\n"
        "We value your feedback! If you have any comments, suggestions, or questions, please email us at **contact_us@optibayeslab.com**."
    )
            
if __name__ == "__main__":
    main()
