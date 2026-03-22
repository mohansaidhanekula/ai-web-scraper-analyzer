# AI Web Scraper & Analyzer
# Scrapes websites using BeautifulSoup and analyzes content with LLMs

import requests
from bs4 import BeautifulSoup
import openai
import json
from urllib.parse import urlparse
from datetime import datetime

openai.api_key = "YOUR_OPENAI_API_KEY"

# ============================================================
# 1. WEB SCRAPER
# ============================================================
def scrape_website(url: str) -> dict:
    """Scrape text content from a webpage."""
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        # Remove scripts and style tags
        for tag in soup(["script", "style", "nav", "footer", "header"]):
            tag.decompose()

        # Extract key elements
        title = soup.title.string.strip() if soup.title else "No title"
        headings = [h.get_text(strip=True) for h in soup.find_all(['h1', 'h2', 'h3'])[:10]]
        paragraphs = [p.get_text(strip=True) for p in soup.find_all('p') if len(p.get_text(strip=True)) > 50][:20]
        links = [a.get('href') for a in soup.find_all('a', href=True) if a.get('href').startswith('http')][:20]

        text_content = ' '.join(paragraphs)[:3000]  # Limit for API

        return {
            "url": url,
            "title": title,
            "domain": urlparse(url).netloc,
            "headings": headings,
            "text_content": text_content,
            "links": links,
            "word_count": len(text_content.split()),
            "scraped_at": datetime.now().isoformat()
        }
    except Exception as e:
        return {"error": str(e), "url": url}


# ============================================================
# 2. AI CONTENT ANALYZER
# ============================================================
def analyze_content(scraped_data: dict, analysis_type: str = "summary") -> str:
    """Analyze scraped web content using LLM."""
    content = f"""
    URL: {scraped_data.get('url', 'N/A')}
    Title: {scraped_data.get('title', 'N/A')}
    Headings: {', '.join(scraped_data.get('headings', [])[:5])}
    Content: {scraped_data.get('text_content', '')[:2000]}
    """

    prompts = {
        "summary": "Summarize this webpage content in 3-5 key bullet points.",
        "sentiment": "Analyze the sentiment and tone of this webpage content.",
        "keywords": "Extract the top 10 keywords and topics from this content.",
        "competitor": "Identify strengths, weaknesses, and unique value propositions from this content."
    }

    prompt = prompts.get(analysis_type, prompts["summary"])

    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a web intelligence analyst."},
            {"role": "user", "content": f"{prompt}\n\n{content}"}
        ]
    )
    return response.choices[0].message.content


# ============================================================
# DEMO OUTPUT (Simulated scraping results)
# ============================================================
if __name__ == "__main__":
    print("AI WEB SCRAPER & ANALYZER")
    print("=" * 60)
    print(f"Run Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

    # Simulated scraped data for demo
    DEMO_SCRAPED = [
        {
            "url": "https://openai.com",
            "title": "OpenAI",
            "domain": "openai.com",
            "headings": ["ChatGPT", "GPT-4o", "DALL-E 3", "API", "Safety"],
            "word_count": 1240,
            "text_content": "OpenAI is an AI research company. ChatGPT is their flagship product...",
            "analysis": {
                "summary": [
                    "OpenAI develops advanced AI systems including GPT-4, DALL-E, and Whisper",
                    "Their main product ChatGPT has 100M+ users worldwide",
                    "Focus on AI safety and responsible deployment",
                    "Offers API access for developers to build AI-powered applications",
                    "Committed to AGI development for humanity's benefit"
                ],
                "keywords": ["ChatGPT", "GPT-4", "AI Safety", "API", "Language Models", "DALL-E", "Multimodal AI", "Generative AI", "Machine Learning", "OpenAI"],
                "sentiment": "Positive and authoritative tone. Technical content with emphasis on safety and responsibility."
            }
        },
        {
            "url": "https://github.com/trending",
            "title": "Trending repositories on GitHub today",
            "domain": "github.com",
            "headings": ["Trending", "Today", "This week"],
            "word_count": 890,
            "text_content": "Trending repositories from various programming languages...",
            "analysis": {
                "summary": [
                    "GitHub trending shows most popular open-source projects",
                    "AI/ML repositories dominate the trending list in 2026",
                    "Python remains the most common language in trending repos",
                    "Many automation and LLM-related projects gaining traction"
                ],
                "keywords": ["Python", "Machine Learning", "LLM", "Open Source", "API", "React", "TypeScript", "Automation", "AI Agents", "RAG"],
                "sentiment": "Neutral and informational. Developer-focused content."
            }
        }
    ]

    for item in DEMO_SCRAPED:
        print(f"{'='*60}")
        print(f"URL     : {item['url']}")
        print(f"Title   : {item['title']}")
        print(f"Domain  : {item['domain']}")
        print(f"Words   : {item['word_count']}")
        print(f"Headings: {', '.join(item['headings'][:4])}")
        print(f"\n[AI SUMMARY]")
        for bullet in item['analysis']['summary']:
            print(f"  • {bullet}")
        print(f"\n[TOP KEYWORDS]")
        print(f"  {', '.join(item['analysis']['keywords'][:8])}")
        print(f"\n[SENTIMENT]")
        print(f"  {item['analysis']['sentiment']}")
        print()

    print(f"{'='*60}")
    print(f"SCRAPING STATS")
    print(f"  Pages scraped    : {len(DEMO_SCRAPED)}")
    print(f"  Total words      : {sum(d['word_count'] for d in DEMO_SCRAPED)}")
    print(f"  Analysis types   : Summary, Keywords, Sentiment")
    print(f"{'='*60}")
