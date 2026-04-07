"""
LLM summarization using OpenRouter API.
"""

import os
from openai import OpenAI
from typing import Optional
from dotenv import load_dotenv

load_dotenv()


def summarize_content(content: str, model: Optional[str] = None) -> str:
    """
    Summarize content using OpenRouter LLM.

    Args:
        content: The text content to summarize
        model: OpenRouter model ID (default: anthropic/claude-3-haiku)

    Returns:
        Summarized text

    Raises:
        ValueError: If API key is missing or API call fails
    """
    api_key = os.getenv('OPENROUTER_API_KEY')
    if not api_key:
        raise ValueError("OPENROUTER_API_KEY not set. Please configure your .env file.")

    if model is None:
        model = os.getenv('OPENROUTER_MODEL', 'anthropic/claude-3-haiku')

    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
    )

    # Trim content if too long for context (Claude has ~200k context but keep reasonable)
    max_input = 15000
    if len(content) > max_input:
        content = content[:max_input] + "... [content truncated for summarization]"

    prompt = f"""Please provide a concise but comprehensive summary of the following web content.

The summary should:
- Be 2-3 paragraphs maximum
- Highlight key points and main ideas
- Maintain the original tone and intent
- Be suitable for inclusion in a formal report

Content to summarize:

{content}

Summary:"""

    try:
        completion = client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.3,
            max_tokens=1000,
        )
        return completion.choices[0].message.content.strip()
    except Exception as e:
        raise ValueError(f"OpenRouter API error: {e}")
