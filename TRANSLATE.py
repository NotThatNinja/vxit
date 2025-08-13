import shutil
import os
from google import genai
import time

# TO_TRANSLATE = [
#     "index.astro",
#     "about.astro",
#     "contact.astro",
#     "legal.astro",
#     "privacy-policy.astro",
#     "services\\website-development.astro",
#     "services\\ai-integration.astro",
#     "services\\ecommerce-solutions.astro",
#     "services\\maintenance.astro",
#     "services\\seo-optimization.astro"
# ]

TO_TRANSLATE = [
    "contact.astro",
]

BASE = "src\\pages"

# LANGUAGES = ["it", "es", "fr", "de", "et"]
LANGUAGES = ["it", "es", "fr", "de", "et"]

def translate(content, language, client):
    content = content.split("<style>", 1)

    # Translate content
    translation = llm_translate(content[0], language, client)

    # Remove markdown syntax
    if translation.startswith("```"):
        lines = translation.split("\n")
        lines[0] = '---'
        translation = "\n".join(lines)
        translation = translation.replace("```", "")

    if len(content) > 1:
        translation += "<style>" + "\n".join(content[1:])

    return translation

def llm_translate(content, language, client):
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=f"Translate the following text from English to the language associated with this language code: {language}. Keep all html, css, js, json etc. syntax intact, ONLY TRANSLATE TEXT CONTENT.\n\n{content}"
    )
    return response.text

def main():
    rpm = 0
    request_start_time = time.time()
    client = genai.Client()

    for language in LANGUAGES:
        print(f"--- Starting translation to {language.upper()} ---")
        time.sleep(1)

        # Create base dir
        print("> Creating base directories")
        lang_dir = os.path.join(BASE, language)
        services_dir = os.path.join(lang_dir, "services")
        os.makedirs(services_dir, exist_ok=True)

        print(f"> Starting translation. Files to translate: {len(TO_TRANSLATE)}")
        time.sleep(1)
        for i, file in enumerate(TO_TRANSLATE):
            # Reset RPM if more than 60 seconds have passed
            if time.time() - request_start_time >= 60:
                request_start_time = time.time()
                rpm = 0

            # Check if RPM has exceeded 10
            rpm += 1
            if rpm > 10:
                time_to_sleep = 70 - (time.time() - request_start_time)
                print(f"> Rate limit exceeded ({rpm} requests in the last minute). Waiting {time_to_sleep} seconds")
                if time_to_sleep < 0:
                    time_to_sleep = 0
                time.sleep(time_to_sleep)
                rpm = 0

            # Start translating
            print(f"> Translating file {i + 1} of {len(TO_TRANSLATE)}: {file}")

            src_file = os.path.join(BASE, "en", file)
            dst_file = os.path.join(lang_dir, file)
            
            print(f"> Reading {src_file}")
            content = []
            with open(src_file, "r", encoding="utf-8") as f:
                content = f.read()
            
            print("> Translating...")
            translation = translate(content, language, client)

            print(f"> Writing translation to {dst_file}")
            with open(dst_file, "w", encoding="utf-8") as f:
                f.write(translation)

            print(f"> Finished translating file {i + 1} of {len(TO_TRANSLATE)}: {file}")
            print()
        
        print(f"--- Finished translation to {language.upper()} ---")
        print()
        time.sleep(3)

if __name__ == "__main__":
    main()
