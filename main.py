import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv("./api.env")
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

def main():
    print("Hello from crosswords!")


if __name__ == "__main__":
    main()
