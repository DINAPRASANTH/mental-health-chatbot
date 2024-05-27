# image-gen.py

import os
import io
import sys
import warnings
from PIL import Image
from stability_sdk import client
import stability_sdk.interfaces.gooseai.generation.generation_pb2 as generation

def generate_image(favorite_pet, favorite_color, favorite_season, gender, age_group):
    # Our Host URL should not be prepended with "https" nor should it have a trailing slash.
    os.environ['STABILITY_HOST'] = 'grpc.stability.ai:443'

    # Paste your API Key below.
    os.environ['STABILITY_KEY'] = 'sk-nl2ZBlPTRFlHzO94CcAUm360xHmipwy8mrWr1GLAc5xoUhWA'

    # Set up our connection to the API.
    stability_api = client.StabilityInference(
        key=os.environ['STABILITY_KEY'],
        verbose=True,
        engine="stable-diffusion-xl-1024-v1-0"
    )

    # Set up our initial generation parameters.
    prompt = f"A {age_group} {gender} in a {favorite_color} outfit, playing with a {favorite_pet} during a beautiful {favorite_season} day"
    answers = stability_api.generate(
        prompt=prompt,
        seed=4253978046,
        steps=50,
        cfg_scale=8.0,
        width=1380,
        height=620,
        samples=1,
        sampler=generation.SAMPLER_K_DPMPP_2M
    )

    # Set up warning to print to console if the adult content classifier is tripped.
    for resp in answers:
        for artifact in resp.artifacts:
            if artifact.finish_reason == generation.FILTER:
                warnings.warn(
                    "Your request activated the API's safety filters and could not be processed."
                    "Please modify the prompt and try again.")
            if artifact.type == generation.ARTIFACT_IMAGE:
                img = Image.open(io.BytesIO(artifact.binary))
                file_path = os.path.join("static", "bg-gen", "generated_image.png")
                img.save(file_path)  # Save the generated image
                return file_path  # Return the path of the generated image

if __name__ == "__main__":
    # Accept user inputs from command-line arguments
    if len(sys.argv) != 5:
        print("Usage: python image-gen.py <favorite_pet> <favorite_color> <favorite_season> <gender> <age_group>")
        sys.exit(1)

    favorite_pet = sys.argv[1]
    favorite_color = sys.argv[2]
    favorite_season = sys.argv[3]
    gender = sys.argv[4]
    age_group = sys.argv[5]

    # Generate the image using user inputs
    generate_image(favorite_pet, favorite_color, favorite_season, gender, age_group)
