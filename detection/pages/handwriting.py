import streamlit as st
import json
from dotenv import dotenv_values
from aleph_alpha_client import AlephAlphaModel
from aleph_alpha_client import Document, ImagePrompt, QaRequest
from PIL import Image
import pandas as pd
from uuid import uuid4


def extract_numbers(file_path):

    config = dotenv_values(".env")
    model = AlephAlphaModel.from_model_name(model_name="luminous-extended", token=config["AA_TOKEN"])
    img = ImagePrompt.from_file(file_path)
    prompt = [img]
    document = Document.from_prompt(prompt)
    # request = QaRequest(query=request.question, documents=[document])
    request = QaRequest(query="Q: What is the text? A: ", documents=[document])
    result = model.qa(request)
    try:
        result_answer = result[1][0].answer
        score_answer = result[1][0].score

        return result_answer, score_answer
    except Exception as e:
        return "Text not found", 0


def show_image(id):
    # display image
    st.image(f"{id}.png", caption="Uploaded Image.", use_column_width=True)
    # give the user the ability to turn the image with buttons right or left

    # save the image


def start(id):

    config = dotenv_values(".env")
    # load image with pillow
    image = Image.open(f"{id}.png")

    # split the image vertically in 4 parts
    width, height = image.size
    left = 0
    top = 0
    right = width
    bottom = height / 4
    image1 = image.crop((left, top, right, bottom))

    left = 0
    top = height / 4
    right = width
    bottom = height / 2
    image2 = image.crop((left, top, right, bottom))

    left = 0
    top = height / 2
    right = width
    bottom = height / 4 * 3
    image3 = image.crop((left, top, right, bottom))

    left = 0
    top = height / 4 * 3
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

    # generate prediction for hole image
    result_answer, score_answer = extract_numbers(f"{id}.png")

    st.text(f"Ganzes Bild: {result_answer}")

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

    df = pd.DataFrame(
        {
            "1. Slice": [result1_answer, result1_score],
            "2. Slice": [result2_answer, result2_score],
            "3. Slice": [result3_answer, result3_score],
            "4. Slice": [result4_answer, result4_score],
        }
    )
    df.index = ["Text", "Score"]

    if result1_score < 0.3:
        df["1. Slice"] = " "
    if result2_score < 0.3:
        df["2. Slice"] = " "
    if result3_score < 0.3:
        df["3. Slice"] = " "
    if result4_score < 0.3:
        df["4. Slice"] = " "

    st.table(df)

    # bilder aufklappbar.
    with st.expander("See explanation"):
        col1, col2 = st.columns(2)
        col1.image(f"detection/splitted_image/{id}_1.png", caption=f"{result1_answer} Score: {result1_score}", use_column_width=True)
        # show the result
        col2.image(f"detection/splitted_image/{id}_2.png", caption=f"{result2_answer} Score:{result2_score}", use_column_width=True)
        # show the result

        col3, col4 = st.columns(2)
        col3.image(f"detection/splitted_image/{id}_3.png", caption=f"{result3_answer} Score: {result3_score}", use_column_width=True)
        # show the result

        col4.image(f"detection/splitted_image/{id}_4.png", caption=f"{result4_answer} Score:{result4_score}", use_column_width=True)
        # show the result


st.set_page_config(
    page_title="Handwriting Detector",
    page_icon=":rocket:",
)

st.title("Handwriting Detector")

# Sidebar
st.sidebar.title("Adesso Data & Analytics")
# Sidebar display logo
st.sidebar.text("CC AI & Data Science")
st.sidebar.image("detection/ressources/white.png", use_column_width=True)

st.markdown(
    """Hi, Willkommen bei unserer Handwriting Detection Demo! Um die Demo auszuprobieren bitte ein Bild hochkant von einer Handschrift hochladen.
Wenn die Ausrichtung stimmt auf Start drücken. Dann wird das Bild prozessiert, das Bild wird dabei einmal als Ganzes erkannt und dann noch einmal in 4 Bereiche zerlegt.
Das Ergebnis wird dann angezeigt, einmal für das gesamte Bild und einmal für die vier Zerlegten Bilder. Wenn man auf Show Explanations drückt, werden die vier zerlegten
Bereiche angezeigt.
"""
)

uploaded_file = st.file_uploader("Choose a file")
if uploaded_file is not None:
    # generate random uuid
    id = uuid4()

    # store file to disk
    with open(f"{id}.png", "wb") as f:
        f.write(uploaded_file.getbuffer())
    show_image(id)
    if st.button("Start"):
        start(id)
