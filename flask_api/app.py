import pandas as pd
from flask import Flask, request, jsonify, render_template
import os
from flask_cors import CORS
import urllib.parse

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Add custom filters to Jinja2
@app.template_filter('urlencode')
def urlencode_filter(s):
    if isinstance(s, str):
        s = s.encode('utf-8')
    return urllib.parse.quote_plus(s)

# Cache the dataframe in memory
article_data = None

# Load CSV data into memory
def load_data():
    global article_data
    
    # If data is already loaded, return it
    if article_data is not None:
        return article_data
        
    # Assuming the CSV file is named 'medium_articles.csv' and placed in the same directory
    csv_path = os.path.join(os.path.dirname(__file__), 'medium_articles.csv')
    
    try:
        # Read the CSV file
        article_data = pd.read_csv(csv_path)
        return article_data
    except Exception as e:
        print(f"Error loading CSV: {e}")
        return pd.DataFrame()

# Route for frontend homepage
@app.route('/', methods=['GET'])
def homepage():
    return render_template('index.html')

# Route for article details page
@app.route('/article/<int:article_id>', methods=['GET'])
def article_page(article_id):
    df = load_data()
    
    if df.empty or article_id < 0 or article_id >= len(df):
        return render_template('error.html', message="Article not found"), 404
    
    article = df.iloc[article_id].to_dict()
    return render_template('article.html', article=article)

# API health check
@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({
        "status": "success",
        "message": "Medium Articles Search API is running"
    })

# Search endpoint
@app.route('/api/search', methods=['GET'])
def search():
    # Get the keyword parameter from request
    keyword = request.args.get('keyword', '')
    search_field = request.args.get('field', 'title')  # Default search field is title
    limit = request.args.get('limit', 10, type=int)
    offset = request.args.get('offset', 0, type=int)
    
    if not keyword:
        return jsonify({
            "status": "error",
            "message": "No search keyword provided"
        }), 400
    
    # Load data
    df = load_data()
    
    if df.empty:
        return jsonify({
            "status": "error",
            "message": "Failed to load article data"
        }), 500
    
    # Validate search field
    valid_fields = df.columns.tolist()
    if search_field not in valid_fields:
        return jsonify({
            "status": "error",
            "message": f"Invalid search field. Valid fields are: {', '.join(valid_fields)}"
        }), 400
    
    # Search for keyword in specified column (case insensitive)
    try:
        results = df[df[search_field].str.contains(keyword, case=False, na=False)]
        # Get the indices of matching articles
        matching_indices = results.index.tolist()
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Search error: {str(e)}"
        }), 500
    
    # Get total results before pagination
    total_results = len(results)
    
    # Apply pagination
    paginated_results = results.iloc[offset:offset+limit]
    paginated_indices = matching_indices[offset:offset+limit]
    
    # Convert results to list of dictionaries
    articles = paginated_results.to_dict(orient='records')
    
    # Add the original indices to each article
    for i, article in enumerate(articles):
        article['original_index'] = paginated_indices[i]
    
    # If this is an AJAX request, return JSON
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return jsonify({
            "status": "success",
            "count": len(articles),
            "total": total_results,
            "offset": offset,
            "limit": limit,
            "results": articles
        })
    
    # Otherwise, render the search results template
    return render_template('search_results.html', 
                          keyword=keyword,
                          field=search_field,
                          articles=articles,
                          total=total_results,
                          offset=offset,
                          limit=limit,
                          page=(offset // limit) + 1,
                          total_pages=(total_results + limit - 1) // limit)

# Get all available fields endpoint
@app.route('/api/fields', methods=['GET'])
def get_fields():
    df = load_data()
    
    if df.empty:
        return jsonify({
            "status": "error",
            "message": "Failed to load article data"
        }), 500
    
    return jsonify({
        "status": "success",
        "fields": df.columns.tolist()
    })

# Get article by ID (using index as ID)
@app.route('/api/article/<int:article_id>', methods=['GET'])
def get_article(article_id):
    df = load_data()
    
    if df.empty:
        return jsonify({
            "status": "error",
            "message": "Failed to load article data"
        }), 500
    
    if article_id < 0 or article_id >= len(df):
        return jsonify({
            "status": "error",
            "message": "Article ID out of range"
        }), 404
    
    article = df.iloc[article_id].to_dict()
    
    return jsonify({
        "status": "success",
        "article": article
    })

if __name__ == '__main__':
    # Load data at startup
    data = load_data()
    if data.empty:
        print("Warning: Failed to load CSV data")
    else:
        print(f"Loaded {len(data)} articles from CSV")
    
    # Run the app
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)), debug=True)