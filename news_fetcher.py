import feedparser
import logging

# A list of RSS feeds to check for news.
# You can add or remove URLs here.
NEWS_FEEDS = [
    "https://habr.com/ru/rss/best/daily/?fl=ru",
    "http://feeds.feedburner.com/TechCrunch/",
    "https://www.theverge.com/rss/index.xml"
]

logger = logging.getLogger(__name__)

def fetch_news(limit_per_feed: int = 2) -> str:
    """
    Fetches news from a list of RSS feeds and formats it into a single string.
    
    Args:
        limit_per_feed: The maximum number of news items to take from each feed.
    
    Returns:
        A formatted string containing the news context for the prompt.
    """
    logger.info(f"Fetching news from {len(NEWS_FEEDS)} RSS feeds...")
    all_news = []
    
    for feed_url in NEWS_FEEDS:
        try:
            feed = feedparser.parse(feed_url)
            # Take the top N entries from the current feed
            entries = feed.entries[:limit_per_feed]
            for entry in entries:
                all_news.append(f"Новость: {entry.title}\nСсылка: {entry.link}")
            logger.info(f"Successfully fetched {len(entries)} items from {feed_url}")
        except Exception as e:
            logger.error(f"Failed to fetch or parse feed {feed_url}: {e}")
            
    if not all_news:
        logger.warning("No news items were fetched. Returning an empty string.")
        return "Новостей для анализа не найдено."

    # Join all news items into a single string for the context
    return "\n\n".join(all_news)