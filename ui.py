import streamlit as st
from app import summarize_website
from dotenv import load_dotenv

# Load environment variables (API keys)
load_dotenv()

st.set_page_config(
    page_title="Web Reader Summarizer",
    page_icon="📖",
    layout="centered"
)

st.title("📖 Web Reader Summarizer")
st.markdown("Enter a website URL below to get a structured summary using Gemini AI.")

# Input fields
url_input = st.text_input("Website URL", placeholder="https://example.com")

with st.expander("Advanced Settings"):
    model_input = st.selectbox(
        "Model", 
        ["gemini-3.5-flash-lite", "gemini-3.5-flash", "gemini-3.1-pro-preview"],
        index=0
    )

if st.button("Generate Summary", type="primary"):
    if not url_input:
        st.error("Please enter a URL first.")
    else:
        with st.spinner("Fetching and summarizing content... this might take a few seconds."):
            try:
                summary = summarize_website(url=url_input, model_name=model_input)
                st.success("Summary Generated!")
                
                st.markdown("### Summary")
                st.info(summary)
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
