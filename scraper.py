import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

# Read the CSV file containing Medium article URLs
data = pd.read_csv('url_technology.csv')
data.columns = ['urls']
# Lists to store extracted data
titles = []
subtitles = []
articles = []
authors = []
author_urls = []
claps = []
reading_times = []
image_sources = []
scraped_urls = []
# Scrape articles from the list
for i in range(600):  # Changed range(1) to range(len(data)) to loop through all URLs
    # for i in range(500):
    try:
        url_to_scrap = data.iloc[i]['urls']
        response = requests.get(url_to_scrap, timeout=10)
        response.raise_for_status()  # Raise error for bad responses (4xx, 5xx)

        soup = BeautifulSoup(response.text, "html.parser")

        # Extract title
        title_tag = soup.find("h1", {"data-testid": "storyTitle"})  # Updated title selector
        title = title_tag.text.strip() if title_tag else "N/A"

        # Extract subtitles
        subtitle_texts = []
        subtitle_tags = soup.find_all(["h1", "h2", "h3", "h4"],
                                      class_=lambda x: x != "pw-post-title")  #Exclude title and find h2,h3,h4
        for tag in subtitle_tags:
            subtitle_texts.append(tag.text.strip())
        subtitle = "\n".join(subtitle_texts) if subtitle_texts else "N/A"

        # Extract article text
        article_tags = soup.find_all("p", class_="pw-post-body-paragraph")
        article_text_list = [tag.text.strip() for tag in article_tags]
        article_text = "\n".join(article_text_list) if article_text_list else "N/A"

        # Extract author details
        author_tag = soup.find("a", {"data-testid": "authorName"})
        author = author_tag.text.strip() if author_tag else "N/A"
        author_url = "https://medium.com" + author_tag['href'] if author_tag else "N/A"

        # Extract claps
        claps_tag = soup.find("div", {"class": "pw-multi-vote-count"})
        claps_count = claps_tag.find("button").text.strip() if claps_tag and claps_tag.find(
            "button") else "0"  # Default to 0 if not found

        # Extract reading time
        reading_time_tag = soup.find("span", {"data-testid": "storyReadTime"})
        reading_time = reading_time_tag.text.strip() if reading_time_tag else "N/A"

        # Extract image sources with role="presentation"
        for figure in soup.find_all("figure", class_="paragraph-image"):
            # Find <img> inside <picture>
            img_tag = figure.find("img", role="presentation")
            if img_tag and img_tag.get("src"):
                img_src_list.append(img_tag["src"])

            # Find <source> inside <picture> (for higher-resolution images)
            source_tag = figure.find("source")
            if source_tag and source_tag.get("srcset"):
                # Extract the last (highest resolution) URL from srcset
                img_src_list.append(source_tag["srcset"].split(",")[-1].split()[0])

        # Remove duplicates and join into a single string
        img_src_list = list(set(img_src_list))  # Remove duplicates
        img_src = "\n".join(img_src_list) if img_src_list else "N/A"


        # Store scraped data
        titles.append(title)
        subtitles.append(subtitle)
        articles.append(article_text)
        authors.append(author)
        author_urls.append(author_url)
        claps.append(claps_count)
        reading_times.append(reading_time)
        image_sources.append(img_src)
        scraped_urls.append(url_to_scrap)

        print(
            f"✅ Scraped {i + 1}/{len(data)}: {title} - Claps: {claps_count}, Image: {img_src[:50]}..., Subtitle: {subtitle[:50]}...")  # Added print for debugging

        # Pause to avoid getting blocked
        time.sleep(2)  # Adjust if needed

    except Exception as e:
        print(f"❌ Error scraping {url_to_scrap}: {e}")
        titles.append("N/A")
        subtitles.append("N/A")
        articles.append("N/A")
        authors.append("N/A")
        author_urls.append("N/A")
        claps.append("N/A")
        reading_times.append("N/A")
        image_sources.append("N/A")
        scraped_urls.append(url_to_scrap)
# Create a DataFrame and save it to CSV
df = pd.DataFrame({
    "URL": scraped_urls,
    "Title": titles,
    "Subtitle": subtitles,
    "Article": articles,
    "Author": authors,
    "Author URL": author_urls,
    "Claps": claps,
    "Reading Time": reading_times,
    "Image Source": image_sources
})

df.to_csv("medium_articles.csv", index=False)
print("✅ Scraping completed! Data saved to 'medium_articles.csv'.")