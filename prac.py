from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
import re

app = FastAPI()

class QueryRequest(BaseModel):
    query: str
    assets: List[str] = []

@app.post("/v1/answer")
async def solve(data: QueryRequest):
    text = data.query.lower()
    
    # Simple, bulletproof math extractor
    numbers = [float(n) for n in re.findall(r'-?\d+(?:\.\d+)?', text)]

    if len(numbers) >= 2:
        ans = sum(numbers)
        if ans.is_integer():
            ans = int(ans)
        return {"output": f"The sum is {ans}."}
    
    return {"output": "I am alive and running on Render!"}
