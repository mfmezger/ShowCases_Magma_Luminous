import json
from dotenv import dotenv_values
from aleph_alpha_client import AlephAlphaModel
from aleph_alpha_client import Document, ImagePrompt, QaRequest
from typing import List
from aleph_alpha_client import Prompt, SemanticEmbeddingRequest, SemanticRepresentation, SummarizationRequest, EvaluationRequest, Document, ImagePrompt, QaRequest, Prompt, SemanticEmbeddingRequest, SemanticRepresentation, SummarizationRequest, EvaluationRequest


from PIL import Image

def extract_numbers(file_path) -> list:
    img = ImagePrompt.from_file(file_path)
    prompt = [img]
    document = Document.from_prompt(prompt)
    # request = QaRequest(query=request.question, documents=[document])
    request = QaRequest(query="Q: What is the number near the line? A: ", documents=[document])
    result = model.qa(request)
    return result


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

# print the result with the number of the part
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