import os
import logging
from datetime import datetime, date
import urllib.request
import urllib.parse
import json
import xml.etree.ElementTree as ET
from typing import List, Dict, Any, Optional
from bs4 import BeautifulSoup

from sqlalchemy.orm import Session
from app.models.article import Article
from app.models.topic import Topic
from app.models.tag import Tag

logger = logging.getLogger(__name__)


def fetch_raw(url: str, headers: Optional[Dict[str, str]] = None) -> Optional[str]:
    try:
        default_headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
        }
        if headers:
            default_headers.update(headers)
        req = urllib.request.Request(url, headers=default_headers)
        with urllib.request.urlopen(req, timeout=10) as resp:
            if resp.status == 200:
                return resp.read().decode("utf-8", errors="ignore")
    except Exception as exc:
        logger.warning(f"Failed to fetch raw data from {url}: {exc}")
    return None


def fetch_json(url: str, headers: Optional[Dict[str, str]] = None) -> Optional[Dict[str, Any]]:
    raw = fetch_raw(url, headers=headers)
    if raw:
        try:
            return json.loads(raw)
        except Exception:
            pass
    return None


class LiveNewsService:

    def fetch_google_news_rss(self, query: str, max_results: int = 10) -> List[Dict[str, Any]]:
        articles = []
        try:
            encoded_query = urllib.parse.quote(query)
            url = f"https://news.google.com/rss/search?q={encoded_query}&hl=en-US&gl=US&ceid=US:en"
            xml_data = fetch_raw(url)
            if not xml_data:
                return []

            root = ET.fromstring(xml_data)
            items = root.findall(".//item")
            for item in items[:max_results]:
                title_elem = item.find("title")
                link_elem = item.find("link")
                pub_elem = item.find("pubDate")
                desc_elem = item.find("description")

                title = title_elem.text if title_elem is not None else "Breaking Event"
                source_url = link_elem.text if link_elem is not None else ""

                pub_date_str = str(date.today())
                if pub_elem is not None and pub_elem.text:
                    try:
                        # RFC 822 date parsing e.g. "Thu, 03 Sep 2026 18:00:00 GMT"
                        dt = datetime.strptime(pub_elem.text[:25].strip(), "%a, %d %b %Y %H:%M:%S")
                        pub_date_str = dt.strftime("%Y-%m-%d")
                    except Exception:
                        pass

                summary = ""
                if desc_elem is not None and desc_elem.text:
                    soup = BeautifulSoup(desc_elem.text, "html.parser")
                    summary = soup.get_text().strip()

                articles.append({
                    "title": title,
                    "summary": summary or title,
                    "content": f"[Google News] {title}\nFull reporting at: {source_url}",
                    "event_date": pub_date_str,
                    "source_url": source_url,
                    "source_name": "Google News"
                })
        except Exception as exc:
            logger.warning(f"Google News RSS fetch failed: {exc}")
        return articles

    def fetch_duckduckgo_web(self, query: str, max_results: int = 8) -> List[Dict[str, Any]]:
        articles = []
        try:
            encoded_query = urllib.parse.quote(query)
            url = f"https://html.duckduckgo.com/html/?q={encoded_query}"
            html_data = fetch_raw(url)
            if not html_data:
                return []

            soup = BeautifulSoup(html_data, "html.parser")
            results = soup.find_all("div", class_="result")
            for res in results[:max_results]:
                title_a = res.find("a", class_="result__title")
                snippet_a = res.find("a", class_="result__snippet")
                url_a = res.find("a", class_="result__url")

                if not title_a:
                    continue

                title = title_a.get_text().strip()
                snippet = snippet_a.get_text().strip() if snippet_a else title
                source_url = url_a.get("href", "").strip() if url_a else ""
                if source_url.startswith("//"):
                    source_url = "https:" + source_url

                articles.append({
                    "title": title,
                    "summary": snippet,
                    "content": f"[Web Scraping] {title}\nSummary: {snippet}\nURL: {source_url}",
                    "event_date": str(date.today()),
                    "source_url": source_url,
                    "source_name": "Web Scraping"
                })
        except Exception as exc:
            logger.warning(f"DuckDuckGo web scraper failed: {exc}")
        return articles

    def fetch_arxiv(self, query: str, max_results: int = 5) -> List[Dict[str, Any]]:
        articles = []
        try:
            encoded_query = urllib.parse.quote(query)
            url = f"http://export.arxiv.org/api/query?search_query=all:{encoded_query}&max_results={max_results}"
            xml_data = fetch_raw(url)
            if not xml_data:
                return []

            root = ET.fromstring(xml_data)
            # Namespace mapping for ArXiv Atom feed
            ns = {"atom": "http://www.w3.org/2005/Atom"}
            entries = root.findall("atom:entry", ns)
            for entry in entries:
                title_elem = entry.find("atom:title", ns)
                summary_elem = entry.find("atom:summary", ns)
                published_elem = entry.find("atom:published", ns)
                id_elem = entry.find("atom:id", ns)

                title = title_elem.text.replace("\n", " ").strip() if title_elem is not None else "ArXiv Paper"
                summary = summary_elem.text.replace("\n", " ").strip() if summary_elem is not None else title
                source_url = id_elem.text.strip() if id_elem is not None else ""

                pub_date = str(date.today())
                if published_elem is not None and published_elem.text:
                    pub_date = published_elem.text[:10]

                articles.append({
                    "title": f"[ArXiv] {title}",
                    "summary": summary[:400] + "...",
                    "content": f"Research Paper: {title}\nAbstract: {summary}\nPaper Link: {source_url}",
                    "event_date": pub_date,
                    "source_url": source_url,
                    "source_name": "ArXiv Research"
                })
        except Exception as exc:
            logger.warning(f"ArXiv fetch failed: {exc}")
        return articles

    def fetch_hackernews(self, query: str, max_results: int = 8) -> List[Dict[str, Any]]:
        articles = []
        encoded_query = urllib.parse.quote(query)
        url = f"https://hn.algolia.com/api/v1/search?query={encoded_query}&tags=story&hitsPerPage={max_results}"
        data = fetch_json(url)
        if data and "hits" in data:
            for item in data.get("hits", []):
                created_at = item.get("created_at", "")[:10] or str(date.today())
                title = item.get("title") or item.get("story_title") or "Tech News"
                source_url = item.get("url") or f"https://news.ycombinator.com/item?id={item.get('objectID')}"
                points = item.get("points", 0)
                articles.append({
                    "title": title,
                    "summary": f"Discussion item with {points} points on Hacker News.",
                    "content": f"Community tech news: '{title}'. Direct link: {source_url}",
                    "event_date": created_at,
                    "source_url": source_url,
                    "source_name": "HackerNews"
                })
        return articles

    def fetch_wikipedia(self, query: str, max_results: int = 5) -> List[Dict[str, Any]]:
        articles = []
        encoded_query = urllib.parse.quote(query)
        url = f"https://en.wikipedia.org/w/api.php?action=query&list=search&srsearch={encoded_query}&format=json&utf8=1"
        data = fetch_json(url)
        if data and "query" in data and "search" in data["query"]:
            for item in data["query"]["search"]:
                title = item.get("title")
                snippet = BeautifulSoup(item.get("snippet", ""), "html.parser").get_text().strip()
                page_id = item.get("pageid")
                source_url = f"https://en.wikipedia.org/?curid={page_id}" if page_id else "https://wikipedia.org"
                articles.append({
                    "title": title,
                    "summary": snippet,
                    "content": f"[Wikipedia Milestone] {title}: {snippet}",
                    "event_date": str(date.today()),
                    "source_url": source_url,
                    "source_name": "Wikipedia"
                })
        return articles

    def fetch_articles_for_query(self, query: str, max_results: int = 15) -> List[Dict[str, Any]]:
        news_api_key = os.getenv("NEWS_API_KEY")
        gnews_api_key = os.getenv("GNEWS_API_KEY")
        all_articles = []

        # 1. Google News RSS (Fast, multi-source, real-time dates)
        gnews_rss = self.fetch_google_news_rss(query, max_results=max_results)
        all_articles.extend(gnews_rss)

        # 2. DuckDuckGo Web Scraper (Coverage for new model releases / unindexed news)
        if len(all_articles) < max_results:
            ddg = self.fetch_duckduckgo_web(query, max_results=5)
            all_articles.extend(ddg)

        # 3. HackerNews Algolia
        if len(all_articles) < max_results:
            hn = self.fetch_hackernews(query, max_results=5)
            all_articles.extend(hn)

        # 4. ArXiv Papers
        if len(all_articles) < max_results:
            arxiv = self.fetch_arxiv(query, max_results=3)
            all_articles.extend(arxiv)

        # 5. Wikipedia Historical Events
        if len(all_articles) < max_results:
            wiki = self.fetch_wikipedia(query, max_results=3)
            all_articles.extend(wiki)

        # 6. Optional NewsAPI / GNews if keys are set
        if news_api_key:
            encoded_query = urllib.parse.quote(query)
            url = f"https://newsapi.org/v2/everything?q={encoded_query}&sortBy=publishedAt&pageSize=5&apiKey={news_api_key}"
            data = fetch_json(url)
            if data and data.get("status") == "ok":
                for item in data.get("articles", []):
                    pub_date = item.get("publishedAt", "")[:10] or str(date.today())
                    all_articles.append({
                        "title": item.get("title") or "Live News",
                        "summary": item.get("description") or "",
                        "content": item.get("content") or item.get("description") or "",
                        "event_date": pub_date,
                        "source_url": item.get("url") or "",
                        "source_name": "NewsAPI"
                    })

        return all_articles[:max_results]

    def sync_live_articles(
        self,
        db: Session,
        topic_id: int,
        query: Optional[str] = None,
        max_results: int = 12
    ) -> List[Article]:
        topic = db.query(Topic).filter(Topic.id == topic_id).first()
        if not topic:
            return []

        search_query = query or topic.name
        raw_articles = self.fetch_articles_for_query(search_query, max_results=max_results)

        synced_articles = []
        all_tags = db.query(Tag).all()

        realtime_tag = db.query(Tag).filter(Tag.name.ilike("RealTime")).first()
        if not realtime_tag:
            realtime_tag = Tag(name="RealTime")
            db.add(realtime_tag)
            db.commit()
            db.refresh(realtime_tag)

        for item in raw_articles:
            title = item["title"].strip()
            source_url = item["source_url"].strip()

            if not title:
                continue

            # Deduplication
            existing = (
                db.query(Article)
                .filter(
                    (Article.title == title) |
                    (Article.source_url == source_url if source_url else False)
                )
                .first()
            )
            if existing:
                continue

            try:
                event_date = datetime.strptime(item["event_date"], "%Y-%m-%d").date()
            except Exception:
                event_date = date.today()

            # Match tags
            matched_tags = [realtime_tag]
            for t in all_tags:
                if t.name.lower() in title.lower() or t.name.lower() in item["summary"].lower():
                    if t.id != realtime_tag.id and t not in matched_tags:
                        matched_tags.append(t)

            new_article = Article(
                title=title,
                summary=item["summary"][:500] if item["summary"] else title,
                content=item["content"],
                event_date=event_date,
                source_url=source_url,
                topic_id=topic_id,
                tags=matched_tags
            )

            db.add(new_article)
            synced_articles.append(new_article)

        db.commit()
        for art in synced_articles:
            db.refresh(art)

        return synced_articles


live_news_service = LiveNewsService()
