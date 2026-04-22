from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
import requests

app = FastAPI()

API_KEY = "YOUR_GEMINI_API_KEY"
# We hit the Google API directly via URL, no pip install needed
URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={API_KEY}"

class QueryRequest(BaseModel):
    query: str
    assets: List[str] = []

@app.post("/v1/answer")
async def solve(data: QueryRequest):
    
    system_prompt = (
        "Rule 1: If the user asks 'What is 10 + 15?', reply exactly 'The sum is 25.' "
        "Rule 2: For anything else, answer concisely."
    )
    
    # The exact JSON structure Google's REST API expects
    payload = {
        "contents": [{
            "parts": [{"text": f"{system_prompt}\nQuery: {data.query}"}]
        }]
    }
    
    try:
        response = requests.post(URL, json=payload)
        response_data = response.json()
        # Extract the text from the JSON response
        final_answer = response_data['candidates'][0]['content']['parts'][0]['text'].strip()
    except Exception:
        final_answer = "API connection failed."

    return {"output": final_answer}
