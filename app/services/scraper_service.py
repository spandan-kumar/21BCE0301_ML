import pytest
from app.services.scraper_service import ScraperService

@pytest.mark.asyncio
async def test_scrape_article():
    url = "https://example.com"
    result = await ScraperService.scrape_article(url)
    assert result is not None
    assert "title" in result
    assert "content" in result
    assert "url" in result
    assert result["url"] == url

@pytest.mark.asyncio
async def test_scrape_article_invalid_url():
    url = "https://invalidurl.com"
    result = await ScraperService.scrape_article(url)
    assert result is None

def test_clean_text():
    text = "  This   is  a   test  "
    cleaned = ScraperService.clean_text(text)
    assert cleaned == "This is a test"

def test_is_allowed_by_robots():
    allowed_url = "https://example.com"
    disallowed_url = "https://example.com/private"
    assert ScraperService.is_allowed_by_robots(allowed_url) == True
    assert ScraperService.is_allowed_by_robots(disallowed_url) == False