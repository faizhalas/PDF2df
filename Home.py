import streamlit as st
import pdfplumber
import pandas as pd
import streamlit.components.v1 as components

st.set_page_config(
     page_title="PDFs to dataframe",
     page_icon="https://github.com/faizhalas/Search4All/blob/main/images/logo.png?raw=true",
     layout="wide"
)

def clear_data():
     st.cache_data.clear()

@st.cache_data(experimental_allow_widgets=True)
def convert(uploaded_files):
    data = []
    for file in uploaded_files:
        with pdfplumber.open(file) as pdf:
            text = ""
            for page in pdf.pages:
                text += page.extract_text()
        data.append({"File Name": file.name, "Text": text})
    df = pd.DataFrame(data).replace(r'\n',' ', regex=True)
    return df

@st.cache_data()
def remove_before(df):
    if rmv:
         df['Text'] = df['Text'].str.split(rmv).str[-1].str.strip()
    return df


@st.cache_data()
def split(extracted_data):
    pattern = '|'.join(word_list)
    split_df = df['Text'].str.split(pattern, expand=True)
    result_df = pd.concat([df, split_df], axis=1)
    new_columns = ['File Name', 'Text', 'intro'] + word_list
    result_df.columns = new_columns
    return result_df    


st.title("PDF to Text Converter")
st.header("Upload PDF Files")

uploaded_files = st.file_uploader("Choose files", type=['pdf'], accept_multiple_files=True)

rmv = st.text_input("Remove certain text before 'your text'.")

text_search = st.text_input("Split your PDFs into parts. Separate words (cAsE sEnSiTiVe) by semicolons (;)")
word_list = [keyword.strip() for keyword in text_search.split(";")]

if st.button("Convert", on_click=clear_data):
    try:
         df = convert(uploaded_files)
         rdf = remove_before(df)
         result_df = split(rdf)
    except ValueError:
            st.error('Error: Please double-check the words that are used as splitter.')
            sys.exit(1)
         
    if not result_df.empty:
        st.subheader("Extracted Text")
        st.dataframe(result_df)
