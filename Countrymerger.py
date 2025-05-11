import streamlit as st
import pandas as pd
from io import BytesIO

st.title("📁 Excel File Merger")
st.write("Upload multiple Excel files to merge them into a single file.")

uploaded_files = st.file_uploader("Upload Excel files", type=["xlsx", "xls"], accept_multiple_files=True)

merge_type = st.radio("Merge Type", ["Merge by Rows (Vertical)", "Merge by Columns (Horizontal)"])

if uploaded_files:
    dataframes = []
    for file in uploaded_files:
        try:
            df = pd.read_excel(file)
            dataframes.append(df)
        except Exception as e:
            st.error(f"Error reading {file.name}: {e}")

    if dataframes:
        if merge_type == "Merge by Rows (Vertical)":
            merged_df = pd.concat(dataframes, ignore_index=True)
        else:
            merged_df = pd.concat(dataframes, axis=1)

        st.success("Files merged successfully!")
        st.write("Preview of Merged Data:")
        st.dataframe(merged_df.head())

        # Convert to Excel
        def to_excel(df):
            output = BytesIO()
            with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                df.to_excel(writer, index=False, sheet_name='MergedData')
            output.seek(0)
            return output

        excel_data = to_excel(merged_df)

        st.download_button(
            label="📥 Download Merged Excel File",
            data=excel_data,
            file_name="merged_excel_file.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    else:
        st.warning("No valid Excel files uploaded.")
