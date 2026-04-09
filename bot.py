import os
import requests
from google import genai
from google.genai import types

# API Key setup
api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

def generate_content():
    try:
        # 1. Gemini se Image Prompt aur Quote lena
        # Hum ek hi call mein dono mangwa lenge time bachane ke liye
        combined_query = "Generate a detailed 1-sentence English prompt for an AI to create a cinematic 9:16 portrait of Lord Krishna. Also, provide a deep 10-word Hindi quote about life."
        response = client.models.generate_content(model="gemini-2.0-flash", contents=combined_query)
        
        full_text = response.text
        # Simple split logic (prompt English mein hoga, quote Hindi mein)
        image_prompt = full_text.split('.')[0].strip() 
        quote = full_text.split('.')[-1].strip()

        print(f"Prompt: {image_prompt}")
        print(f"Quote: {quote}")

        # 2. IMAGE GENERATION (Priority Logic)
        image_saved = False

        # PRIORITY 1: Gemini (Imagen)
        try:
            print("Trying Priority 1: Gemini Imagen...")
            # Note: Gemini Imagen 3 use karne ke liye model name 'imagen-3' hota hai
            img_response = client.models.generate_images(
                model='imagen-3',
                prompt=image_prompt,
                config=types.GenerateImagesConfig(
                    number_of_images=1,
                    aspect_ratio="9:16"
                )
            )
            # Agar image mil gayi toh save karo
            if img_response.generated_images:
                img_response.generated_images[0].image.save("krishna_image.jpg")
                print("Success: Image generated via Gemini!")
                image_saved = True
        except Exception as e:
            print(f"Gemini Image failed or not available: {e}")

        # PRIORITY 2: Pollinations (Fallback)
        if not image_saved:
            print("Switching to Priority 2: Pollinations.ai...")
            image_url = f"https://pollinations.ai/p/{image_prompt.replace(' ', '%20')}?width=720&height=1280&model=flux"
            img_data = requests.get(image_url).content
            with open('krishna_image.jpg', 'wb') as handler:
                handler.write(img_data)
            print("Success: Image generated via Pollinations!")

        # 3. Save Quote for next step
        with open('quote.txt', 'w', encoding='utf-8') as f:
            f.write(quote)

    except Exception as e:
        print(f"Main Error: {e}")

if __name__ == "__main__":
    generate_content()
