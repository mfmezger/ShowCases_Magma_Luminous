import streamlit as st
from dotenv import dotenv_values
from aleph_alpha_client import AlephAlphaModel
from aleph_alpha_client import (
    ImagePrompt,
    CompletionRequest,
    Prompt,
)  # QaRequest,Document
from uuid import uuid4
from PIL import Image


def extract_numbers(file_path):

    config = dotenv_values(".env")
    model = AlephAlphaModel.from_model_name(model_name="luminous-base", token=config["AA_TOKEN"])
    img = ImagePrompt.from_file(file_path)
    # prompt = [img]
    # document = Document.from_prompt(prompt)
    prompt = Prompt(
        [
            ImagePrompt.from_file(file_path),
            "Q: What does the handwriting say?",
        ]
    )
    # request = QaRequest(query=request.question, documents=[document])
    request = CompletionRequest(prompt=prompt)
    result = model.complete(request)
    result_answer = result[1][0].completion
    # wenn nicht empty
    # if not result_answer == "":
    print("Text wird übersetzt")
    prompt_translation = Prompt(
        f"""Frage: Kannst du den Text auf Deutsch Übersetzen?
                                    Text: {result_answer}
                                    Antwort:  """
    )
    request = CompletionRequest(prompt=prompt)
    result = model.complete(request)
    result_answer = result[1][0].completion
    # request = QaRequest(query="Du bis eine KI die Text aus Bildern liest. Was steht in dem Bild bitte auf deutsch antworten. Antwort:", documents=[document])
    try:
        # result_answer = result[1][0].answer

        print(result_answer)
        # score_answer = result[1][0].score
        # return result_answer, score_answer
        return result_answer  # , score_answer
    except Exception as e:
        print(e)
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

    # resize the image to 300x300
    image = image.resize((300, 300))
    image.save(f"{id}.png")

    # generate prediction for hole image
    result_answer = extract_numbers(f"{id}.png")

    st.text(f"Text im Bild: {result_answer}")


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
