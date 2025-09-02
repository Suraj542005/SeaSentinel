import httpx    # Load image from the Web pages
import base64
import google.generativeai as genai
from dotenv import dotenv_values    # Import dotenv to manage environment variables.


# Load environment variables from the .env file
env_vars = dotenv_values(".env")
Key = env_vars.get("key")     # Retrieve the Gemini-2.5-pro API Key.
genai.configure(api_key=Key)


# model = genai.GenerativeModel(model_name="gemini-2.5-pro")
model = genai.GenerativeModel(model_name="gemini-2.5-flash")
# image_path = "https://i.pinimg.com/736x/bd/11/47/bd1147dca8fa712cf5512e325a1a2924.jpg"
# image_path = "https://i.pinimg.com/736x/e5/50/23/e55023a05a5bbcc876b4d5e9868c132a.jpg"
# image_path = "https://qph.cf2.quoracdn.net/main-qimg-561466c0109226359788066c6f4bfe78"
image_path = "https://www.bodhisurfyoga.com/wp-content/uploads/2021/05/beach-break-wave.jpg"
# image_path = "https://thumbnails.production.thenounproject.com/Sl_QLnHZfHFZ_4y0DaXapGUYfVc=/fit-in/1000x1000/photos.production.thenounproject.com/photos/ocean_waves_crashing_on_shore_during_sunset-scopio-07306d0c-ae6a-404a-ad70-d3a7ba113b55.JPG"
# image_path = "https://i.pinimg.com/736x/ea/1e/a0/ea1ea0a487e73c865bec436c9f255b04.jpg"
# image_path = "page_1.pdf"
image = httpx.get(image_path)

prompt = """
System Instruction:
You are an AI agent specialized in analyzing and classifying ocean hazard images. You must carefully examine the image provided and return structured information about the hazard.

Task:
When an image is given, classify and provide the following details:

Disaster Name → (e.g., Tsunami, Cyclone, Oil Spill, Flood, Coral Bleaching, Red Tide, etc.)

Disaster Type → (Natural / Human-Induced / Climate-Related)

Risk / Intensity Level → (No Risk / Low / Moderate / High / Critical)

Short Summary → (2–3 sentences explaining what the image represents, potential impact, and risks involved).

Output Format (JSON-like):

{
  "disaster_name": "Tsunami",
  "disaster_type": "Natural",
  "risk_intensity": "Critical",
  "summary": "The image depicts a massive tsunami wave approaching the shore, posing severe risks to coastal populations, infrastructure, and ecosystems."
}
"""

# prompt = "Extract the question form this"
# prompt = "Caption this image."
# prompt = "Extract the text from this image."
# prompt = "Can you solve the question"
response = model.generate_content([{'mime_type': 'image/jpeg', 'data': base64.b64encode(image.content).decode('utf-8')}, prompt])
# response = model.generate_content([{'mime_type': 'image/jpeg', 'data': base64.b64encode(image_path).decode('utf-8')}, prompt])


print(response.text)
