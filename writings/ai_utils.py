import os
import google.generativeai as genai
from django.conf import settings

def generate_summary(text):
    """
    Sends text to Gemini and returns a summary in Nepali.
    """
    api_key = os.getenv("GEMINI_API_KEY")
    
    if not api_key:
        print("Warning: GEMINI_API_KEY not found.")
        return None

    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-2.5-flash')

        # Prompt engineering is key here
        prompt = f"""
        Please summarize the following Nepali literary text into a short, concise summary (max 3-4 sentences). 
        The summary must be in the Nepali language.
        
        Text:
        {text}
        """

        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"Error generating summary: {e}")
        return None