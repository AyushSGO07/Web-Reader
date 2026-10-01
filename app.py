import argparse
import logging
import sys
import os
from urllib.parse import urlparse

from dotenv import load_dotenv

# Set USER_AGENT to prevent LangChain warnings
os.environ["USER_AGENT"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.document_loaders import WebBaseLoader
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def is_valid_url(url: str) -> bool:
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False

def summarize_website(url: str, model_name: str = "gemini-3.5-flash-lite") -> str:
    """
    Fetches the content of a website and generates a structured summary.
    """
    if not is_valid_url(url):
        raise ValueError(f"Invalid URL provided: {url}")

    logger.info(f"Loading content from: {url}")
    
    # Custom headers to avoid basic scraper blocking by some websites
    header_template = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    
    try:
        loader = WebBaseLoader(url, header_template=header_template)
        docs = loader.load()
    except Exception as e:
        logger.error(f"Failed to load website content: {e}")
        raise

    if not docs or not docs[0].page_content.strip():
        raise ValueError("No content extracted from the website.")

    logger.info(f"Successfully loaded {len(docs[0].page_content)} characters. Generating summary...")

    # A more robust and structured prompt
    prompt = PromptTemplate(
        template=(
            "You are an expert summarizer. Please read the following website content "
            "and provide a comprehensive, well-structured summary.\n\n"
            "Include:\n"
            "- A high-level overview (1-2 sentences)\n"
            "- Key takeaways or main points (bullet points)\n"
            "- A brief conclusion or final thought\n\n"
            "Website Content:\n{document}\n\n"
            "Summary:"
        ),
        input_variables=["document"]
    )

    try:
        # Temperature is set to 0.3 for more focused and deterministic summaries
        model = ChatGoogleGenerativeAI(model=model_name, temperature=0.3)
        parser = StrOutputParser()
        chain = prompt | model | parser
        
        result = chain.invoke({"document": docs[0].page_content})
        logger.info("Summary generated successfully.")
        return result
    except Exception as e:
        logger.error(f"Failed to generate summary: {e}")
        raise

def main():
    load_dotenv()
    
    parser = argparse.ArgumentParser(description="Web Reader Extension: Summarize website content.")
    parser.add_argument("url", type=str, help="The URL of the website to summarize")
    parser.add_argument("--model", type=str, default="gemini-3.5-flash-lite", help="The Gemini model to use")
    
    args = parser.parse_args()
    
    try:
        summary = summarize_website(args.url, args.model)
        print("\n" + "="*60)
        print(f"SUMMARY FOR: {args.url}")
        print("="*60 + "\n")
        print(summary)
        print("\n" + "="*60)
    except Exception as e:
        logger.error(f"Execution failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()