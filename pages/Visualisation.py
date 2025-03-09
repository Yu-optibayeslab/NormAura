import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
from dataprocessors import Visualiser

def app():
    st.title("NormAura: Data visualising page.")

    st.sidebar.markdown("---")  # Shortcut for <hr> in Markdown 
    st.sidebar.header("Visualisation Options")

    # Initialize Visualiser instance
    visualiser = Visualiser()

    # Dropdown to select dataset
    dataset_options = ["Preprocessed Data", "Normalised Data", "Reduced Data"]
    selected_dataset = st.sidebar.selectbox("Select Dataset", dataset_options)

    # Display appropriate plot based on selected dataset and plot type
    if selected_dataset == "Preprocessed Data" or selected_dataset == "Normalised Data" :
        # Retrieve data from session state
        if selected_dataset == "Preprocessed Data":
            data = st.session_state.get("preprocessed_data", None)
        else:
            data = st.session_state.get("normalised_data", None)
        if data is None:
            st.warning("No processed data found. Please process data on the main page first.")
            st.stop()
        # Allow user to choose a plot type
        plot_options = [
            "---Select a plot ---",
            "Scatterplot Matrix",
            "Parallel Coordinates Plot",
            "RadViz plot",
            "Heatmap (Correlation Matrix)"
            ]
        selected_plot = st.sidebar.selectbox("Select a plot", plot_options)
        if selected_plot == "Scatterplot Matrix":
            st.subheader("Scatterplot Matrix")
            hue = st.sidebar.selectbox(
                                        "hue (feature name for coloring):",
                                        options=data.columns,  # All columns are available for selection
                                        key = "selectbox_hue"
                                        )
            st.write(f"hue = {hue}!\n")
            fig = visualiser.scatterplot_matrix(data, hue=hue)
            st.pyplot(fig)

        elif selected_plot == "Parallel Coordinates Plot":
            st.subheader("Parallel Coordinates Plot")
            class_column = st.sidebar.selectbox(
                                                "class_column:",
                                                options=data.columns,  # All columns are available for selection
                                                key = "selectbox_class_column1"
                                                )
            fig = visualiser.parallel_coordinates_plot(data, class_column=class_column)
            st.pyplot(fig)

        elif selected_plot == "RadViz plot":
            st.subheader("RadViz plot")
            class_column = st.sidebar.selectbox(
                                                "class_column:",
                                                options=data.columns,  # All columns are available for selection
                                                key = "selectbox_class_column1"
                                                )
            fig = visualiser.radviz(data, class_column=class_column)
            st.pyplot(fig)

        elif selected_plot == "Heatmap (Correlation Matrix)":
            st.subheader("Heatmap (Correlation Matrix)")
            fig = visualiser.heatmap(data.corr())
            st.pyplot(fig)

        else:
            st.warning("Please select a type of plot to present.")
    elif selected_dataset == "Reduced Data":
        reduced_data = st.session_state.get("reduced_data", None)
        data = st.session_state.get("preprocessed_data", None)
        if reduced_data is None:
            st.warning("No processed data found. Please process data on the main page first.")
            st.stop()
        # Allow user to choose a plot type
        plot_options = [
            "---Select a plot ---",
            "2D Scatter Plot (Reduced Data)",
            "3D Scatter Plot (Reduced Data)",
            ]
        selected_plot = st.sidebar.selectbox("Select a plot", plot_options)
        if reduced_data is not None:
            if selected_plot == "3D Scatter Plot (Reduced Data)":
                st.subheader("3D Scatter Plot of Reduced Data")
                x = st.sidebar.selectbox(
                                    "x-axis:",
                                    options=reduced_data.columns,  # All columns are available for selection
                                    key = "selectbox_PC1"
                                )

                y = st.sidebar.selectbox(
                                    "y-axis:",
                                    options=reduced_data.columns,  # All columns are available for selection
                                    key = "selectbox_PC2"
                                )

                z = st.sidebar.selectbox(
                                    "z-axis:",
                                    options=reduced_data.columns,  # All columns are available for selection
                                    key = "selectbox_z"
                                )
                fig = visualiser.scatter_3d(reduced_data, x=x, y=y, z=z, hue=z)
                #st.pyplot(fig)
                st.plotly_chart(fig, use_container_width=True)
            elif selected_plot == "2D Scatter Plot (Reduced Data)":
                st.subheader("2D Scatter Plot of Reduced Data")
                x = st.sidebar.selectbox(
                                    "x-axis:",
                                    options=reduced_data.columns,  # All columns are available for selection
                                    key = "selectbox_PC1"
                                )

                y = st.sidebar.selectbox(
                                    "y-axis:",
                                    options=reduced_data.columns,  # All columns are available for selection
                                    key = "selectbox_PC2"
                                )

                z = st.sidebar.selectbox(
                                    "Output:",
                                    options=reduced_data.columns,  # All columns are available for selection
                                    key = "selectbox_z"
                                )
                fig = visualiser.scatter_2d(reduced_data, x=x, y=y, z=z, s=20)
                st.pyplot(fig)

        else:
            st.info("Reduced data is not available. Please perform dimensionality reduction on the main page.")


    # Self defined code for visulisation
    st.sidebar.markdown("---")  # Shortcut for <hr> in Markdown 
    # Sidebar checkbox to enable/disable code editing
    enable_editing = st.sidebar.checkbox("Enable User Defined Code")
    # Default code (can be predefined or loaded from a file)
    default_code = """
# Please enter your own visualisation code here.
# The following is the example code:
df = st.session_state.get("preprocessed_data", None)

# List of columns to plot
columns_to_plot = df.columns  # Use all columns in the DataFrame

# Determine the number of rows and columns for the subplot grid
num_plots = len(columns_to_plot)
num_cols = 3  # Number of columns in the subplot grid
num_rows = (num_plots + num_cols - 1) // num_cols  # Calculate the number of rows needed

# Create a figure with subplots
fig, axes = plt.subplots(num_rows, num_cols, figsize=(12, 6 * num_rows))
axes = axes.flatten()  # Flatten the axes array for easy iteration

# Loop through the columns and create subplots
for i, column in enumerate(columns_to_plot):
    ax = axes[i]
    sns.violinplot(y=df[column], ax=ax)  # Use a violin plot for each column
    ax.set_title(f'Violin Plot of {column}')
    ax.set_ylabel(column)  # Add the column name as the y-axis label

# Hide any unused subplots
for j in range(i + 1, num_rows * num_cols):
    axes[j].axis('off')

# Adjust layout to prevent overlap
plt.tight_layout()

# Display the figure in Streamlit by hitting the 'Generate Plot' button.
"""

    # Display the code editor if editing is enabled
    if enable_editing:
        st.warning(" #### Please enter your own code for data visualisation below. ####")
        st.warning(" Current version support four libraries:\n 1. streamlit as st;\n 2. matplotlib.pyplot as plt; \
                    \n 3. seaborn as sns;\n 4. plotly.express as px.\n")
        st.warning("The \'raw_data\', \'preprocessed_data\', \'normalised_data\', and demensionally \'reduced_data\' are stored in: st.session_state\n \
                    you can retrieve them simply using \n\n \
                    data = st.session_state.get(\"raw_data\", None)")
        user_code = st.text_area("Edit your Python code here:", value=default_code, height=300)
        # Button to execute the code
        if st.button("Generate Plot", key="generate_plot"):
            try:
                # Define a safe execution environment
                allowed_globals = {
                    "plt": plt,
                    "sns": sns,
                    "px": px,
                    "st": st
                }
                allowed_locals = {}

                # Execute the user's code in a restricted environment
                exec(user_code, allowed_globals, allowed_locals)

                # Display the plot if it was created
                if plt.gcf().get_axes():
                    st.pyplot(plt.gcf())
                else:
                    st.warning("No plot was generated. Did you use plt, sns, or px?")
            except Exception as e:
                st.error(f"An error occurred: {e}")
            finally:
                # Clear the plot to avoid overlapping with future plots
                plt.clf()