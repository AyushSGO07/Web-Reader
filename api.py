from fastapi import FastAPI, HTTPException, Body
from pydantic import BaseModel, HttpUrl
from dotenv import load_dotenv
import uvicorn

# Import the summarize function from our core app
from app import summarize_website

# Load environment variables (API keys, etc.)
load_dotenv()

app = FastAPI(
    title="Web Reader Extension API",
    description="API backend for summarizing website content",
    version="1.0.0"
)

class SummarizeRequest(BaseModel):
    url: HttpUrl
    model: str = "gemini-3.5-flash-lite"

class SummarizeResponse(BaseModel):
    url: str
    summary: str

@app.get("/")
def read_root():
    return {"status": "active", "message": "Welcome to the Web Reader API"}

@app.post("/summarize", response_model=SummarizeResponse)
async def api_summarize_website(request: SummarizeRequest = Body(...)):
    """
    Takes a URL and returns a structured summary using Google Generative AI.
    """
    try:
        # Convert HttpUrl to string for our function
        url_str = str(request.url)
        summary = summarize_website(url=url_str, model_name=request.model)
        return SummarizeResponse(url=url_str, summary=summary)
    
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        # For other exceptions like LangChain/Gemini API errors or scraping failures
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")

if __name__ == "__main__":
    # Run the API locally on port 8000
    uvicorn.run("api:app", host="0.0.0.0", port=8000, reload=True)
