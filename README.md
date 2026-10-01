# Web Reader Extension Backend

This project serves as the core backend for a web reader browser extension. It extracts content from any given website URL and leverages LangChain alongside Google's Gemini models to generate a structured, highly readable summary. 

The application is built to be modular and provides three distinct interfaces: a Command Line Interface (CLI), an interactive Web UI, and a RESTful API.

## Features

*   **Intelligent Summarization:** Uses Gemini (default: gemini-3.5-flash-lite) to generate structured summaries consisting of high-level overviews, key takeaways, and conclusions.
*   **Multi-Interface Support:**
    *   **CLI:** For rapid testing and terminal-based workflows.
    *   **REST API:** A FastAPI backend designed to receive requests directly from a browser extension.
    *   **Web UI:** A Streamlit interface for manual input and visual testing.
*   **Anti-Scraping Bypass:** Injects standard browser User-Agent headers to prevent basic blocks from target websites.
*   **Robust Error Handling:** Validates URLs and safely catches scraping or LLM generation failures.

## Tools and Technologies

*   **Python:** Core programming language.
*   **LangChain:** Framework for orchestrating the document loading and LLM prompt chaining.
*   **Google Generative AI (Gemini):** The Large Language Model used for summarization.
*   **FastAPI & Uvicorn:** Used to build and serve the API endpoints for the browser extension.
*   **Streamlit:** Used to build the rapid prototyping Web UI.
*   **BeautifulSoup4:** Underlying parser used by LangChain to extract readable text from raw HTML.

## Setup and Installation

1.  **Navigate to the project directory:**
    ```bash
    cd rag_based/Doc_Loader/Web_Reader
    ```

2.  **Install dependencies:**
    It is recommended to use a virtual environment. Install the required Python packages:
    ```bash
    pip install -r requirements.txt
    ```

3.  **Configure Environment Variables:**
    Create a `.env` file in the root of the `Web_Reader` directory and add your Google API Key:
    ```env
    GOOGLE_API_KEY="your_api_key_here"
    ```

## Usage

### 1. Using the Command Line Interface (CLI)
Run the core application directly from your terminal. This is useful for debugging and quick tests.
```bash
python app.py "https://en.wikipedia.org/wiki/LangChain"
```
You can also specify a different model using the `--model` argument:
```bash
python app.py "https://example.com" --model "gemini-3.5-flash"
```

### 2. Using the API (For Browser Extensions)
Start the FastAPI server. This is the mode you will use when connecting your frontend Chrome/Edge extension.
```bash
python api.py
```
*   The server runs by default on `http://localhost:8000`.
*   Interactive API Documentation is available at `http://localhost:8000/docs`.
*   **Endpoint:** `POST /summarize`
    *   Payload: `{"url": "https://example.com"}`
    *   Response: `{"url": "https://example.com", "summary": "..."}`

### 3. Using the Web UI
Start the Streamlit application for a visual interface.
```bash
streamlit run ui.py
```
This will automatically open a browser tab where you can paste URLs and read the generated summaries.

## Architecture Notes

*   **app.py:** Contains the core scraping and summarization logic (`summarize_website`), along with the CLI argument parsing.
*   **api.py:** Imports the core logic from `app.py` and wraps it in a FastAPI POST route.
*   **ui.py:** Imports the core logic from `app.py` and wraps it in a Streamlit interface. 
