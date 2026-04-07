# AI Workflow Automation Demo

A Streamlit web app that demonstrates an AI workflow: URL → scrape → summarize → PDF report.

## Features

- **URL Input**: Enter any web page URL
- **Content Scraping**: Extracts main text content using BeautifulSoup
- **AI Summarization**: Uses OpenRouter LLM to generate concise summaries
- **PDF Report**: Generates a formatted PDF with original content and summary
- **Clean UI**: Simple, responsive Streamlit interface

## Quick Start

### 1. Clone and Setup

```bash
cd ai-demo
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configure API Key

Copy `.env.example` to `.env` and add your OpenRouter API key:

```bash
cp .env.example .env
# Edit .env and set OPENROUTER_API_KEY=your_key_here
```

Get an API key from [OpenRouter](https://openrouter.ai/).

### 3. Run the App

```bash
streamlit run app.py
```

Open your browser to `http://localhost:8501`.

## Production Deployment

### Using Streamlit Cloud

1. Push this repo to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Deploy from your repo
4. Add `OPENROUTER_API_KEY` in Secrets settings

### Using Docker

```bash
docker build -t ai-demo .
docker run -p 8501:8501 -e OPENROUTER_API_KEY=your_key ai-demo
```

## Architecture

- **app.py**: Main Streamlit UI and workflow orchestration
- **src/scraper.py**: Web content extraction with requests+BeautifulSoup
- **src/summarizer.py**: OpenRouter LLM integration for summarization
- **src/pdf_generator.py**: ReportLab-based PDF generation

## Configuration

- `OPENROUTER_API_KEY`: Required for LLM access
- `OPENROUTER_MODEL`: Model to use (default: `anthropic/claude-3-haiku`)
- `MAX_CONTENT_LENGTH`: Maximum characters to scrape (default: 10000)

## Dependencies

- streamlit
- requests
- beautifulsoup4
- reportlab
- python-dotenv
- openai (for OpenRouter compatibility)

## License

MIT
