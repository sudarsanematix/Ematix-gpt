import os
import io
from dotenv import load_dotenv
from huggingface_hub import InferenceClient

load_dotenv()

# The API key was previously loaded as HF_API_KEY in the .env file.
hf_key = os.getenv("HF_API_KEY")
if not hf_key:
    hf_key = os.getenv("HF_TOKEN") # Fallback to HF_TOKEN if the user used that

client = InferenceClient(
    provider="auto",
    api_key=hf_key,
)

def query_image(prompt: str) -> bytes:
    # output is a PIL.Image object
    image = client.text_to_image(
        prompt,
        model="Artples/LAI-ImageGeneration-vSDXL-1",
    )
    
    # Convert PIL Image to bytes
    img_byte_arr = io.BytesIO()
    image.save(img_byte_arr, format='JPEG')
    return img_byte_arr.getvalue()
