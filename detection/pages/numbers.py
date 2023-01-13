import streamlit as st
import json
from dotenv import dotenv_values
from aleph_alpha_client import AlephAlphaModel
from aleph_alpha_client import Document, ImagePrompt, QaRequest
from PIL import Image
import pandas as pd
from uuid import uuid4


def extract_numbers(file_path) -> list:

    config = dotenv_values(".env")
    model = AlephAlphaModel.from_model_name(model_name="luminous-extended", token=config["AA_TOKEN"])
    img = ImagePrompt.from_file(file_path)
    prompt = [img]
    document = Document.from_prompt(prompt)
    # request = QaRequest(query=request.question, documents=[document])
    request = QaRequest(query="Q: What is the number near the line? A: ", documents=[document])
    result = model.qa(request)
    try:
        result_answer = result[1][0].answer
        score_answer = result[1][0].score

        return result_answer, score_answer
    except Exception as e:
        return "No numbers found", 0


def start(id):

    config = dotenv_values(".env")
    model = AlephAlphaModel.from_model_name(model_name="luminous-extended", token=config["AA_TOKEN"])

    # load image with pillow
    image = Image.open(f"{id}.png")

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
    image2 = image.crop((left - 20, top, right, bottom))

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

    # save every image in the detection/splitted_image folder
    image1.save(f"detection/splitted_image/{id}_1.png")
    image2.save(f"detection/splitted_image/{id}_2.png")
    image3.save(f"detection/splitted_image/{id}_3.png")
    image4.save(f"detection/splitted_image/{id}_4.png")

    # extract numbers from each part
    result1_answer, result1_score = extract_numbers(f"detection/splitted_image/{id}_1.png")
    result2_answer, result2_score = extract_numbers(f"detection/splitted_image/{id}_2.png")
    result3_answer, result3_score = extract_numbers(f"detection/splitted_image/{id}_3.png")
    result4_answer, result4_score = extract_numbers(f"detection/splitted_image/{id}_4.png")

    print("1: ", result1_answer)
    print("2: ", result2_answer)
    print("3: ", result3_answer)
    print("4: ", result4_answer)

    # save it to json
    with open("result.json", "w") as fp:
        json.dump(result1_answer, fp)
        json.dump(result2_answer, fp)
        json.dump(result3_answer, fp)
        json.dump(result4_answer, fp)

        # display image
    st.image(f"{id}.png", caption="Uploaded Image.", use_column_width=True)

    # convert results with scores in a dataframe
    df = pd.DataFrame(
        {
            "Links Oben": [result1_answer, result1_score],
            "Rechts Oben": [result2_answer, result2_score],
            "Links Unten": [result3_answer, result3_score],
            "Rechts Unten": [result4_answer, result4_score],
        }
    )
    df.index = ["Number", "Score"]

    if result1_score < 0.3:
        df["Links Oben"] = " "
    if result2_score < 0.3:
        df["Rechts Oben"] = " "
    if result3_score < 0.3:
        df["Links Unten"] = " "
    if result4_score < 0.3:
        df["Rechts Unten"] = " "

    st.table(df)

    # bilder aufklappbar.
    with st.expander("See explanation"):
        col1, col2 = st.columns(2)
        col1.image(f"detection/splitted_image/{id}_1.png", caption=f"{result1.answers[0].answer} Score: {result1.answers[0].score}", use_column_width=True)
        # show the result
        col2.image(f"detection/splitted_image/{id}_2.png", caption=f"{result2.answers[0].answer} Score:{result2.answers[0].score}", use_column_width=True)
        # show the result

        col3, col4 = st.columns(2)
        col3.image(f"detection/splitted_image/{id}_3.png", caption=f"{result3.answers[0].answer} Score: {result3.answers[0].score}", use_column_width=True)
        # show the result

        col4.image(f"detection/splitted_image/{id}_4.png", caption=f"{result4.answers[0].answer} Score:{result4.answers[0].score}", use_column_width=True)
        # show the result


st.set_page_config(
    page_title="Number Extractor",
    page_icon=":rocket:",
)

st.title("Number Extractor")

# Sidebar
st.sidebar.title("Adesso Data & Analytics")
# Sidebar display logo
st.sidebar.text("CC AI & Data Science")
st.sidebar.image("detection/ressources/white.png", use_column_width=True)


uploaded_file = st.file_uploader("Choose a file")
if uploaded_file is not None:
    # generate random uuid
    id = uuid4()

    # store file to disk
    with open(f"{id}.png", "wb") as f:
        f.write(uploaded_file.getbuffer())

    start(id)
