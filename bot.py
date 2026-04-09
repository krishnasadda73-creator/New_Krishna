import os
import requests
import time
import urllib.parse
import random
from PIL import Image, ImageDraw
import subprocess

def generate_content():
    try:
        # 1. Assets Generation
        print("Step 1: Generating Text...")
        system_prompt = "Write a 1-sentence prompt for Lord Krishna image and a 10-word Hindi quote. Separate with |"
        text_url = f"https://text.pollinations.ai/{urllib.parse.quote(system_prompt)}"
        full_text = requests.get(text_url).text
        
        image_prompt = full_text.split('|')[0].strip() if "|" in full_text else "Lord Krishna divine portrait cinematic"
        quote = full_text.split('|')[1].strip() if "|" in full_text else "Jai Shree Krishna"
        print(f"Quote: {quote}")

        # 2. Robust Image Download
        print("Step 2: Downloading Image (Waiting for AI)...")
        encoded_prompt = urllib.parse.quote(image_prompt)
        # Seed badalne se fresh image milti hai
        img_url = f"https://pollinations.ai/p/{encoded_prompt}?width=1080&height=1920&model=flux&seed={random.randint(1, 99999)}"
        
        max_retries = 5
        image_downloaded = False
        
        for i in range(max_retries):
            print(f"Attempt {i+1} to download image...")
            response = requests.get(img_url)
            
            # Check if file is valid (at least 20KB)
            if response.status_code == 200 and len(response.content) > 20000:
                with open('raw_image.jpg', 'wb') as f:
                    f.write(response.content)
                print(f"Image saved! Size: {len(response.content)} bytes")
                image_downloaded = True
                break
            else:
                print("Image not ready yet, waiting 10 seconds...")
                time.sleep(10) # 10 second ka gap
        
        if not image_downloaded:
            print("Pollinations is slow. Using a stable fallback image...")
            fallback_url = "https://pollinations.ai/p/lord%20krishna%20divine%20cinematic?width=1080&height=1920&seed=123"
            with open('raw_image.jpg', 'wb') as f:
                f.write(requests.get(fallback_url).content)

        # 3. Drawing Text (Pillow)
        print("Step 3: Processing Image...")
        img = Image.open("raw_image.jpg").convert("RGB")
        draw = ImageDraw.Draw(img)
        w, h = img.size
        # Bottom transparent overlay
        overlay = Image.new('RGBA', img.size, (0,0,0,0))
        d = ImageDraw.Draw(overlay)
        d.rectangle([0, h-450, w, h-50], fill=(0, 0, 0, 160))
        img = Image.alpha_composite(img.convert('RGBA'), overlay).convert('RGB')
        
        draw = ImageDraw.Draw(img)
        draw.text((w/2, h-250), quote, fill="white", anchor="mm")
        img.save("processed_image.jpg")

        # 4. BGM Selection
        bgm_folder = "BGM"
        selected_bgm = ""
        if os.path.exists(bgm_folder):
            files = [f for f in os.listdir(bgm_folder) if f.endswith('.mp3')]
            if files:
                selected_bgm = os.path.join(bgm_folder, random.choice(files))
                print(f"BGM selected: {selected_bgm}")

        # 5. FFmpeg
        print("Step 5: Final Rendering...")
        if selected_bgm:
            cmd = f'ffmpeg -loop 1 -i processed_image.jpg -i "{selected_bgm}" -c:v libx264 -t 10 -pix_fmt yuv420p -vf "scale=1080:1920" -c:a aac -shortest -y final_reel.mp4'
        else:
            cmd = f'ffmpeg -loop 1 -i processed_image.jpg -c:v libx264 -t 10 -pix_fmt yuv420p -vf "scale=1080:1920" -y final_reel.mp4'
        
        subprocess.run(cmd, shell=True, check=True)
        print("MISSION ACCOMPLISHED: final_reel.mp4 created!")

    except Exception as e:
        print(f"Final Attempt Failed: {e}")
        # Build empty files to prevent git error
        open('final_reel.mp4', 'a').close()

if __name__ == "__main__":
    generate_content()
