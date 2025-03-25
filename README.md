# Medium Articles Scraper

A web scraper and API for Medium articles that extracts key information from technology-related articles.

## Features

- Scrapes Medium articles based on topic/tag
- Extracts title, author, publication date, read time, and other metadata
- Provides a Flask API to access the data
- Deployable to Vercel

## Setup

1. Clone the repository
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Run the scraper:
   ```
   python scraper.py
   ```
4. Start the API server:
   ```
   python flask_api/app.py
   ```

## API Endpoints

- `/api/articles` - Get all articles
- `/api/articles/<id>` - Get a specific article by ID

## Technologies Used

- Python
- Flask
- BeautifulSoup
- Pandas
- Vercel for deployment 