import google.generativeai as genai
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

# 1. Initialize the AI (Get a free key from Google AI Studio)
genai.configure(api_key="YOUR_GEMINI_API_KEY_HERE")
model = genai.GenerativeModel('gemini-1.5-flash') # Flash is perfect for low latency

app = FastAPI()

class QueryRequest(BaseModel):
    query: str
    assets: List[str] = []

@app.post("/v1/answer")
async def solve(data: QueryRequest):
    print(f"--- EVALUATOR SENT: {data.query} ---")
    
    # 2. Strict Prompt Engineering
    # We force the LLM to format math exactly how the evaluator wants it,
    # but give it the freedom to answer any other random text question.
    system_prompt = (
        "You are an automated API responding to test cases. "
        "Rule 1: If the user asks a simple addition math question like 'What is 10 + 15?', "
        "you MUST reply exactly in this format: 'The sum is [X].' (include the period). "
        "Rule 2: For any other question, answer concisely in one sentence."
    )
    
    # 3. Generate the answer
    try:
        response = model.generate_content(f"{system_prompt}\nQuery: {data.query}")
        final_answer = response.text.strip()
    except Exception as e:
        final_answer = "I encountered an error processing the query."
        print(f"Error: {e}")

    print(f"--- AI REPLIED: {final_answer} ---")
    
    return {"output": final_answer}