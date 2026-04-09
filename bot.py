import os
from google import genai
from google.genai import types

# API Key setup
api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

def generate_content():
    try:
        # 1. Prompt & Quote Generation
        print("Step 1: Asking Gemini for a Divine Prompt...")
        prompt_request = client.models.generate_content(
            model="gemini-2.0-flash", 
            contents="Write a highly detailed 1-sentence prompt for Imagen 3 to create a 9:16 cinematic portrait of Lord Krishna. Also, give a 10-word Hindi quote."
        )
        
        full_text = prompt_request.text
        lines = full_text.strip().split('\n')
        image_prompt = lines[0].strip()
        quote = " ".join(lines[1:]).strip() if len(lines) > 1 else "Jai Shree Krishna"
        
        print(f"Prompt: {image_prompt}")

        # 2. Asli Image Generation (Gemini Imagen 3)
        print("Step 2: Generating Image via Gemini Imagen 3...")
        
        # 'imagen-3' is the official model for image generation
        response = client.models.generate_images(
            model='imagen-3',
            prompt=image_prompt,
            config=types.GenerateImagesConfig(
                number_of_images=1,
                aspect_ratio="9:16",
                output_mime_type="image/jpeg"
            )
        )

        if response.generated_images:
            # Image ko save karna
            with open("krishna_image.jpg", "wb") as f:
                f.write(response.generated_images[0].image.get_bytes())
            print(f"SUCCESS: Gemini generated a {len(response.generated_images[0].image.get_bytes())} bytes image.")
        else:
            print("FAILED: Gemini returned no image.")
            exit(1)

        # 3. Save Quote
        with open('quote.txt', 'w', encoding='utf-8') as f:
            f.write(quote)

    except Exception as e:
        print(f"CRITICAL ERROR: {e}")
        # Agar yahan error aaya, toh iska matlab hai Gemini API key 
        # mein Imagen 3 enabled nahi hai ya quota issue hai.
        exit(1)

if __name__ == "__main__":
    generate_content()
