import openai
from utils import config

def translate_text(text, source_lang="en-US", target_lang="es-ES"):
    try:
        openai.api_key = config.OPENAI_API_KEY
        messages = [
            {"role": "system", "content": "You are a helpful translator specializing in medical texts."},
            {"role": "user", "content": f"Translate the following medical text from {source_lang} to {target_lang}: {text}"}
        ]
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
            temperature=0.3,
            max_tokens=1000
        )
        translation = response["choices"][0]["message"]["content"].strip()
        return translation
    except Exception as e:
        raise RuntimeError(f"Translation failed: {e}")
