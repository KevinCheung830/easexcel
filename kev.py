import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Set the title of the app
st.title("Kev's easexcel v1")

# File uploader for Table 1
st.subheader("Upload First CSV File")
uploaded_file1 = st.file_uploader("Upload the first CSV file", type=["csv"], key="file1")

# File uploader for Table 2 (for cross-checking)
st.subheader("Upload Second CSV File (For Validation)")
uploaded_file2 = st.file_uploader("Upload the second CSV file", type=["csv"], key="file2")

if uploaded_file1 is not None and uploaded_file2 is not None:
    # Read the CSV files
    df1 = pd.read_csv(uploaded_file1)
    df2 = pd.read_csv(uploaded_file2)

    # Display editable dataframes
    st.write("### Edit Table 1:")
    edited_df1 = st.data_editor(df1, num_rows="dynamic")  # Editable table 1

    st.write("### Edit Table 2 (For Validation):")
    edited_df2 = st.data_editor(df2, num_rows="dynamic")  # Editable table 2

    # Perform validation
    st.write("### Validation Results:")
    
    # Ensuring both tables have the same columns before validation
    if list(edited_df1.columns) == list(edited_df2.columns):
        validation_result = edited_df1.compare(edited_df2)

        if validation_result.empty:
            st.success("✅ Both tables match perfectly!")
        else:
            st.warning("⚠️ Discrepancies found between the two tables:")
            st.dataframe(validation_result)
    else:
        st.error("❌ The column names in both tables do not match. Please check your files.")

    # Select columns for visualization from Table 1
    numeric_columns = edited_df1.select_dtypes(["number"]).columns.tolist()
    if numeric_columns:
        x_axis = st.selectbox("Select X-axis", numeric_columns, key="x_axis")
        y_axis = st.selectbox("Select Y-axis", numeric_columns, key="y_axis")

        # Plot the updated data
        fig, ax = plt.subplots()
        ax.plot(edited_df1[x_axis], edited_df1[y_axis], marker='o', linestyle='-')
        ax.set_xlabel(x_axis)
        ax.set_ylabel(y_axis)
        ax.set_title(f"{y_axis} vs {x_axis}")

        # Display the plot
        st.pyplot(fig)
    else:
        st.warning("No numeric columns found for visualization in Table 1.")
else:
    st.write("Please upload both CSV files to proceed.")
