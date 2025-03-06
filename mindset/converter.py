import streamlit as st
import pandas as pd
from io import BytesIO

st.set_page_config(page_title="Data Sweeper", layout='wide')

# Custom CSS for the app:
st.markdown(
"""
<style>
.stApp{
    background-color: #f0f0f5;
    color: black;
    align-items: center;
    justify-content: center;
}
</style>
""",
unsafe_allow_html=True
)



# title and description
st.title("📀 Data Sweeper and File Converter By Tooba Saleem")
st.markdown("This is a simple web app that allows you to upload a dataset and perform some basic data cleaning operations on it.The app will display the first 5 rows of the dataset and allow you to download the cleaned dataset.")

# upload the dataset:
uploaded_files = st.file_uploader("Upload your file (accepts CSV or Excel):", type=["csv", "xlsx"],accept_multiple_files= True)

if uploaded_files:
    for file in uploaded_files:
        ext = file.name.split(".")[-1]
        df = pd.read_csv(file) if ext =="csv" else pd.read_excel(file)

        #file details
        
        st.subheader(f"{file.name} -Preview the head of the Dataframe 🔍")
        st.dataframe(df.head())

        # Data cleaning options
        st.subheader("🆑 Data Cleaning")
        if st.checkbox(f"Clean data for {file.name}"):
            col1, col2 = st.columns(2)
            with col1:
                if st.checkbox(f"Remove duplicates from: {file.name}"):
                    df.drop_duplicates(inplace=True)
                    st.success("✅ Removed duplicates!")
            with col2:
                if st.checkbox(f"Fill missing values from: {file.name}"):
                    numeric_cols = df.select_dtypes(include=['number']).columns
                    df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
                    st.success("❓ Filled missing values!")

                
               # Column selection for display:
        st.subheader("🔍 Select the columns to Keep")
        columns = st.multiselect("Select the columns to keep", df.columns, default=df.columns)
        df = df[columns]

                # Data visualization
        st.subheader("📊 Data Visualization")
        if st.checkbox(f"Show Visualization for: {file.name}"):
            st.bar_chart(df.select_dtypes(include ='number').iloc[:,:2])

                # Conversion options
        st.subheader("🔄 Conversion Options")
        conversion_type = st.radio(f"Convert the file: {file.name} to", ["CSV", "Excel"], key=file.name)
        if st.button(f"Convert"):
            buffer = BytesIO()
            if conversion_type == "CSV":
                       df.to_csv(buffer, index=False)
                       file_name = file.name.replace(ext, ".csv")
                       mime_type = "text/csv"
            elif conversion_type == "Excel":
                     df.to_excel(buffer, index=False)
                     file_name = file.name.replace(ext, ".xlsx")
                     mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            buffer.seek(0)

            st.download_button(
                label=f"Download",
                data=buffer,
                file_name=file_name,
                mime=mime_type
            )
st.success("🎉 All operations completed successfully!")
            


