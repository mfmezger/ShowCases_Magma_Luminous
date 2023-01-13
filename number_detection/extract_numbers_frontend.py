import streamlit as st
import json
from dotenv import dotenv_values
from aleph_alpha_client import AlephAlphaModel
from aleph_alpha_client import Document, ImagePrompt, QaRequest
from typing import List
from aleph_alpha_client import Prompt, SemanticEmbeddingRequest, SemanticRepresentation, SummarizationRequest, EvaluationRequest, Document, ImagePrompt, QaRequest, Prompt, SemanticEmbeddingRequest, SemanticRepresentation, SummarizationRequest, EvaluationRequest
from PIL import Image
import pandas as pd


def extract_numbers(file_path) -> list:

    config = dotenv_values(".env")
    model = AlephAlphaModel.from_model_name(model_name="luminous-extended", token=config["AA_TOKEN"])
    img = ImagePrompt.from_file(file_path)
    prompt = [img]
    document = Document.from_prompt(prompt)
    # request = QaRequest(query=request.question, documents=[document])
    request = QaRequest(query="Q: What is the number near the line? A: ", documents=[document])
    result = model.qa(request)
    return result



def start():

    config = dotenv_values(".env")
    model = AlephAlphaModel.from_model_name(model_name="luminous-extended", token=config["AA_TOKEN"])

    # load image with pillow
    image = Image.open("1.png")

    # the split is from left top to right then bottom.
    # split the image in 4 parts
    width, height = image.size
    left = 0
    top = 0
    right = width / 2
    bottom = height / 2
    image1 = image.crop((left, top, right, bottom))

    left = width / 2
    top = 0
    right = width
    bottom = height / 2
    image2 = image.crop((left-20, top, right, bottom))

    left = 0
    top = height / 2
    right = width / 2
    bottom = height
    image3 = image.crop((left, top, right, bottom))

    left = width / 2
    top = height / 2
    right = width
    bottom = height
    image4 = image.crop((left, top, right, bottom))

    # save every image in the splitted_image folder
    image1.save("splitted_image/1.png")
    image2.save("splitted_image/2.png")
    image3.save("splitted_image/3.png")
    image4.save("splitted_image/4.png")

    # extract numbers from each part
    result1 = extract_numbers("splitted_image/1.png")
    result2 = extract_numbers("splitted_image/2.png")
    result3 = extract_numbers("splitted_image/3.png")
    result4 = extract_numbers("splitted_image/4.png")

    print("1: ", result1)
    print("2: ", result2)
    print("3: ", result3)
    print("4: ", result4)

    # save it to json
    with open('result.json', 'w') as fp:
        json.dump(result1, fp)
        json.dump(result2, fp)
        json.dump(result3, fp)
        json.dump(result4, fp)
    
        # display image
    st.image("1.png", caption="Uploaded Image.", use_column_width=True)

    # convert results with scores in a dataframe
    df = pd.DataFrame({"Links Oben": [result1.answers[0].answer, result1.answers[0].score], "Rechts Oben": [result2.answers[0].answer, result2.answers[0].score], "Links Unten": [result3.answers[0].answer, result3.answers[0].score], "Rechts Unten": [result4.answers[0].answer, result4.answers[0].score], })
    df.index = ["Number", "Score"]

    if result1.answers[0].score < 0.3:
        df["Links Oben"] = " "
    if result2.answers[0].score < 0.3:
        df["Rechts Oben"] = " "
    if result3.answers[0].score < 0.3:
        df["Links Unten"] = " "
    if result4.answers[0].score < 0.3:
        df["Rechts Unten"] = " "
        
    st.table(df)

    # bilder aufklappbar.
    with st.expander("See explanation"):
        col1, col2 = st.columns(2)
        col1.image("splitted_image/1.png", caption=f"{result1.answers[0].answer} Score: {result1.answers[0].score}", use_column_width=True)
        # show the result
        col2.image("splitted_image/2.png", caption=f"{result2.answers[0].answer} Score:{result2.answers[0].score}", use_column_width=True)
        # show the result

        col3, col4 = st.columns(2)
        col3.image("splitted_image/3.png", caption=f"{result3.answers[0].answer} Score: {result3.answers[0].score}", use_column_width=True)
        # show the result

        col4.image("splitted_image/4.png", caption=f"{result4.answers[0].answer} Score:{result4.answers[0].score}", use_column_width=True)
        # show the result



st.set_page_config(
    page_title="Number Extractor",
    page_icon=":rocket:",
)

st.title("Number Extractor")


uploaded_file = st.file_uploader("Choose a file")
if uploaded_file is not None:
    # store file to disk
    with open("1.png", "wb") as f:
        f.write(uploaded_file.getbuffer())

    start()






