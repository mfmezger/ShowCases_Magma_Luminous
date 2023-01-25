import streamlit as st
from transformers import pipeline
from uuid import uuid4

st.set_page_config(
    page_title="Hello",
    page_icon="👋",
)

st.write("# Welcome to Adesso Showcases")


nlp = pipeline(
    "document-question-answering",
    model="impira/layoutlm-document-qa",
)


def show_image(id):
    # display image
    st.image(f"{id}.png", caption="Uploaded Image.", use_column_width=True)
    # give the user the ability to turn the image with buttons right or left


def start(id, question, nlp):

    result = nlp(
        f"{id}.png",
        question=question,
    )
    st.write(result[0]["answer"])


uploaded_file = st.file_uploader("Choose a file")
if uploaded_file is not None:
    # generate random uuid
    id = uuid4()

    # store file to disk
    with open(f"{id}.png", "wb") as f:
        f.write(uploaded_file.getbuffer())
    show_image(id)
    st.write("Whats your Question?")
    question = st.text_input("Question")
    if st.button("Start"):
        start(id, question, nlp)
