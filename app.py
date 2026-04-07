"""
AI Workflow Automation Demo - Streamlit App

URL → Scrape → Summarize → PDF Report
"""

import streamlit as st
import os
import tempfile
from datetime import datetime

from src.scraper import scrape_url
from src.summarizer import summarize_content
from src.pdf_generator import generate_pdf_report

# Page configuration
st.set_page_config(
    page_title="AI Workflow Automation Demo",
    page_icon="🤖",
    layout="centered"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 1rem;
    }
    .subheader {
        font-size: 1.2rem;
        color: #666;
        text-align: center;
        margin-bottom: 2rem;
    }
    .stProgress > div > div > div > div {
        background-color: #1f77b4;
    }
</style>
""", unsafe_allow_html=True)

# Title
st.markdown('<h1 class="main-header">🤖 AI Workflow Automation</h1>', unsafe_allow_html=True)
st.markdown('<p class="subheader">Enter a URL to scrape, summarize, and generate a PDF report</p>', unsafe_allow_html=True)

# Sidebar for configuration
with st.sidebar:
    st.header("⚙️ Configuration")

    # Check for API key
    api_key = os.getenv('OPENROUTER_API_KEY')
    if api_key:
        st.success("✅ API Key configured")
    else:
        st.error("❌ OPENROUTER_API_KEY not set")
        st.info("Set it in `.env` or enter below")

        api_key_input = st.text_input("OpenRouter API Key", type="password")
        if api_key_input:
            os.environ['OPENROUTER_API_KEY'] = api_key_input
            st.success("✅ API Key set for this session")

    st.divider()

    model = st.selectbox(
        "LLM Model",
        [
            "anthropic/claude-3-haiku",
            "anthropic/claude-3-sonnet",
            "openai/gpt-4o-mini",
            "openai/gpt-4o",
            "meta-llama/llama-3.1-8b-instruct",
        ],
        index=0
    )
    os.environ['OPENROUTER_MODEL'] = model

    max_length = st.slider(
        "Max Content Length",
        min_value=1000,
        max_value=50000,
        value=10000,
        step=1000,
        help="Maximum characters to scrape from the URL"
    )

    st.divider()
    st.markdown("---")
    st.caption("Powered by Streamlit + OpenRouter")

# Main form
with st.form("workflow_form"):
    url = st.text_input(
        "🌐 URL to Process",
        placeholder="https://example.com/article",
        help="Enter the full URL including https://"
    )

    submitted = st.form_submit_button("🚀 Start Workflow", use_container_width=True)

if submitted:
    if not url:
        st.error("Please enter a URL")
    else:
        # Validate URL format
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url

        # Workflow steps with progress
        st.markdown("---")
        st.subheader("🔄 Workflow Progress")

        # Step 1: Scrape
        with st.status("📥 Step 1: Scraping content...", expanded=True) as status:
            try:
                st.write(f"Fetching: {url}")
                content = scrape_url(url, max_length=max_length)
                st.write(f"✅ Extracted {len(content):,} characters")
                st.session_state['content'] = content
                status.update(label="✅ Scraping complete!", state="complete")
            except Exception as e:
                st.error(f"❌ Scraping failed: {str(e)}")
                status.update(label="❌ Scraping failed", state="error")
                st.stop()

        # Step 2: Summarize
        with st.status("🤖 Step 2: Summarizing with AI...", expanded=True) as status:
            try:
                st.write(f"Using model: {os.getenv('OPENROUTER_MODEL', 'default')}")
                summary = summarize_content(st.session_state['content'])
                st.write("✅ Summary generated")
                st.session_state['summary'] = summary
                status.update(label="✅ Summarization complete!", state="complete")
            except ValueError as e:
                if "API key" in str(e):
                    st.error("❌ OpenRouter API key missing. Set it in the sidebar or .env file.")
                else:
                    st.error(f"❌ Summarization failed: {str(e)}")
                status.update(label="❌ Summarization failed", state="error")
                st.stop()
            except Exception as e:
                st.error(f"❌ LLM API error: {str(e)}")
                status.update(label="❌ Summarization failed", state="error")
                st.stop()

        # Step 3: Generate PDF
        with st.status("📄 Step 3: Generating PDF report...", expanded=True) as status:
            try:
                # Create temp file for PDF
                with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp:
                    pdf_path = tmp.name

                generate_pdf_report(url, st.session_state['content'], summary, pdf_path)
                st.write(f"✅ PDF created: {os.path.basename(pdf_path)}")
                st.session_state['pdf_path'] = pdf_path
                status.update(label="✅ PDF generation complete!", state="complete")
            except Exception as e:
                st.error(f"❌ PDF generation failed: {str(e)}")
                status.update(label="❌ PDF generation failed", state="error")
                st.stop()

        st.success("🎉 Workflow completed successfully!")

        # Display results
        st.markdown("---")
        col1, col2 = st.columns(2)

        with col1:
            st.download_button(
                label="📥 Download PDF Report",
                data=open(pdf_path, 'rb').read(),
                file_name=f"ai_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
                mime="application/pdf",
                use_container_width=True
            )

        with col2:
            if st.button("🔄 Start Over", use_container_width=True):
                st.rerun()

        # Show summary preview
        with st.expander("📋 View Summary", expanded=False):
            st.write(summary)

        # Show content preview
        with st.expander("📄 View Full Content", expanded=False):
            st.text_area("Extracted Content", content, height=300)

# Footer
st.markdown("---")
st.caption("AI Workflow Automation Demo | Built with Streamlit, OpenRouter, and ReportLab")
