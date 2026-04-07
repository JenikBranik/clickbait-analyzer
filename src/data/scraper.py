import feedparser
import pandas as pd
import os
import time

rss_sources = {
    "CT24": {
        "label": 0,
        "urls": ["https://ct24.ceskatelevize.cz/rss/hlavni-zpravy"]
    },
    "iROZHLAS": {
        "label": 0,
        "urls": ["https://www.irozhlas.cz/rss/irozhlas"]
    },
    "Novinky": {
        "label": 0,
        "urls": ["https://www.novinky.cz/rss"]
    },
    "SeznamZpravy": {
        "label": 0,
        "urls": ["https://www.seznamzpravy.cz/rss"]
    },
    "Blesk": {
        "label": 1,
        "urls": ["https://www.blesk.cz/rss", "https://www.blesk.cz/rss/celebrity"]
    },
    "eXtra": {
        "label": 1,
        "urls": ["https://www.extra.cz/rss"]
    },
    "Super": {
        "label": 1,
        "urls": ["https://www.super.cz/rss"]
    }
}

output_file = "dataset.csv"
scraped_data = []


def fetch_headlines():
    for outlet_name, outlet_data in rss_sources.items():
        primary_label = outlet_data["label"]
        feed_urls = outlet_data["urls"]
        
        for url in feed_urls:
            try:
                feed = feedparser.parse(url)
                for entry in feed.entries:
                    title = entry.title.strip()
                    
                    scraped_data.append({
                        "Headline": title,
                        "Outlet": outlet_name,
                        "Is_Clickbait": primary_label
                    })
            except Exception as e:
                print(f" -> Error parsing {url}: {e}")
            
            time.sleep(1)

fetch_headlines()

new_df = pd.DataFrame(scraped_data)

if os.path.exists(output_file):
    existing_df = pd.read_csv(output_file)
    combined_df = pd.concat([existing_df, new_df], ignore_index=True)
else:
    combined_df = new_df

initial_count = len(combined_df)
combined_df.drop_duplicates(subset=['Headline'], inplace=True)
final_count = len(combined_df)


combined_df.to_csv(output_file, index=False, encoding='utf-8-sig')
