import streamlit as st
import gen_certs

uploaded_file = st.file_uploader(
    label="Выберите файл для отправки", 
    type=["xlsx"]
)

if uploaded_file is not None:
    gen_certs.excel_to_pdfs(uploaded_file, "certs")
    with open("certs.zip", "rb") as file:
        st.download_button(
            label="Скачать архив",
            data=file,
            file_name="certs.zip",
            mime="application/zip"
        )