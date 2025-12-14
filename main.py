# Entry point
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from scraper.twitter_scraper import TwitterScraper
from processing.cleaner import clean_text
from processing.deduplicator import hash_tweet
from storage.parquet_writer import write_parquet
from analysis.vectorizer import vectorize
from analysis.signal_generator import generate_signal

import os
from datetime import datetime
import time


def main():
    print("Starting Twitter scraper...")

    # ✅ Chrome options (attach to logged-in profile)
    options = Options()
    options.add_argument("--start-maximized")

    options.add_argument(
        r"--user-data-dir=C:\Users\amitj\AppData\Local\Google\Chrome\User Data"
    )
    options.add_argument("--profile-directory=Profile 2")

    # ❌ remove detach (can cause issues)
    # options.add_experimental_option("detach", True)

    # ✅ Use webdriver-manager (VERY IMPORTANT)
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    time.sleep(5)

    scraper = TwitterScraper(driver)
    scraper.scrape()

    print(f"Collected {len(scraper.tweets)} raw tweets")

    # Cleaning + Deduplication
    seen = set()
    processed = []

    for tweet in scraper.tweets:
        cleaned = clean_text(tweet["content"])
        h = hash_tweet(cleaned)

        if h not in seen:
            seen.add(h)
            processed.append({
                "content": cleaned,
                "timestamp": tweet["timestamp"]
            })

    print(f"After deduplication: {len(processed)} tweets")

    # Save to Parquet
    os.makedirs("data/processed", exist_ok=True)
    file_path = f"data/processed/tweets_{datetime.now().date()}.parquet"
    write_parquet(processed, file_path)

    print(f"Saved Parquet file: {file_path}")

    # 🛡️ Prevent vectorizer crash
    if not processed:
        print("No tweets collected. Exiting safely.")
        driver.quit()
        return

    # Analysis
    texts = [t["content"] for t in processed]
    vectors = vectorize(texts)
    signal, confidence = generate_signal(vectors)

    print("Signal generated")
    print(f"Confidence Interval: ±{confidence}")

    driver.quit()


if __name__ == "__main__":
    main()
