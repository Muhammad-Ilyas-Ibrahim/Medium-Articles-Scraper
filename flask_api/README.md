# Medium Articles Search API

A Flask API that makes a CSV file containing scraped Medium articles searchable by keyword.

## API Endpoints

### 1. Health Check
- **URL**: `/`
- **Method**: `GET`
- **Description**: Check if the API is running
- **Example**: `GET /`

### 2. Search Articles
- **URL**: `/api/search`
- **Method**: `GET`
- **Parameters**:
  - `keyword` (required): Search term to find in articles
  - `field` (optional): Field to search in (default: 'title')
  - `limit` (optional): Number of results to return (default: 10)
  - `offset` (optional): Results offset for pagination (default: 0)
- **Example**: `GET /api/search?keyword=javascript&field=title&limit=5&offset=0`

### 3. Get Fields
- **URL**: `/api/fields`
- **Method**: `GET`
- **Description**: Get all available fields in the dataset
- **Example**: `GET /api/fields`

### 4. Get Article by ID
- **URL**: `/api/article/<id>`
- **Method**: `GET`
- **Description**: Get a specific article by its ID (index in the dataset)
- **Example**: `GET /api/article/5`

## Deployment Instructions

### Local Development
1. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

2. Run the application:
   ```
   python app.py
   ```

3. Access the API at `http://localhost:5000`

### Deployment to Heroku (Free Tier)

1. Create a Heroku account at [heroku.com](https://www.heroku.com/)

2. Install the Heroku CLI: [Instructions](https://devcenter.heroku.com/articles/heroku-cli)

3. Login to Heroku:
   ```
   heroku login
   ```

4. Create a new Heroku app:
   ```
   heroku create your-app-name
   ```

5. Initialize git (if not already done):
   ```
   git init
   git add .
   git commit -m "Initial commit"
   ```

6. Deploy to Heroku:
   ```
   git push heroku main
   ```

7. Open your app:
   ```
   heroku open
   ```

### Deployment to PythonAnywhere (Free Tier)

1. Create an account at [pythonanywhere.com](https://www.pythonanywhere.com/)

2. Upload your files to PythonAnywhere via the Files tab

3. Create a new web app from the Web tab:
   - Select "Flask" as the framework
   - Set the Python version to 3.9 or higher
   - Set the path to your Flask app: `/home/yourusername/mysite/app.py`

4. Install required packages:
   - Open a Bash console
   - Create a virtual environment:
     ```
     mkvirtualenv --python=/usr/bin/python3.9 myenv
     ```
   - Install packages:
     ```
     pip install -r requirements.txt
     ```

5. Configure the WSGI file to point to your Flask app

6. Reload the web app to apply changes

## Data Structure

The API expects a CSV file named `medium_articles.csv` with the following columns:
- url
- title
- subtitle
- content
- author
- author_url
- claps
- reading_time
- image_source