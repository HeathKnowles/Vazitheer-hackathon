import os
from dotenv import load_dotenv
import google.generativeai as genai
import requests
import streamlit as st

# Load environment variables from .env file
load_dotenv()

# Configure Gemini API
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 40,
  "max_output_tokens": 8192,
  "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
  model_name="gemini-1.5-flash",
  generation_config=generation_config,
)

chat_session = model.start_chat(
  history=[]
)

def get_country_from_ip():
    response = requests.get("https://ipinfo.io/json")
    location_data = response.json()
    return location_data.get("country", "IN")  

def get_state_from_ip():
    response = requests.get("https://ipinfo.io/json")
    location_data = response.json()
    return location_data.get("region", "Unknown")  

def get_local_language_from_state(state_code):
    prompt = f"What is the primary language spoken in the state of {state_code} in India?"
    response = chat_session.send_message(prompt)
    language = response.text.strip()
    if "is" in language:
        language = language.split("is")[-1].strip()
    return language

def get_gemini_response_in_local_language(query, local_language):
    prompt = f"Please respond in {local_language} to the following query: {query}"
    response = chat_session.send_message(prompt)
    return response.text.strip()

def main():
    country_code = get_country_from_ip()
    state_code = get_state_from_ip()

    local_language = get_local_language_from_state(state_code)

    st.write(f"Detected Country: {country_code}")
    st.write(f"Detected State: {state_code}")
    st.write(f"Detected Local Language: {local_language}")

    user_query = st.text_input("Enter your query about road safety:")

    if user_query:
        gemini_response = get_gemini_response_in_local_language(user_query, local_language)
        st.write(f"Gemini's response in {local_language}: {gemini_response}")

if __name__ == "__main__":
    main()
