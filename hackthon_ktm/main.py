from flask import Flask, jsonify, request
import requests
import redis
import json
from flask_cors import CORS
import torch
from transformers import GPT2LMHeadModel, GPT2Tokenizer
from dotenv import load_dotenv
import os
from typing import List, Dict, Optional, Union
import logging
from hackthon_ktm.most_repeted_sentences import get_most_repeated_sentences, save_most_repeated_sentences


# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
CORS(app)


# Constants
DEFAULT_PREDICTED_WORDS = [
    'i', 'what', 'hello', 'where', 'who', 'how', 'can', 'is', 'are', 'could',
    'would', 'may', 'can', 'please', 'will', 'shall', 'did', 'have', 'has',
    'had', 'am', 'were', 'was', 'should', 'might', 'must', 'please', 'you',
    'he', 'she', 'they', 'it', 'this', 'that', 'these', 'those', 'let',
    'we', 'my', 'your', 'his', 'her', 'their', 'our', 'the',
    'there', 'come', 'go', 'bring', 'take', 'give', 'help', 'want',
    'need', 'eat', 'drink', 'sleep', 'play', 'run', 'walk', 'talk', 'call',
    'find', 'make', 'see', 'get', 'know'
]

# Environment variable validation
REQUIRED_ENV_VARS = ['API_KEY', 'REDIS_PASSWORD']
for var in REQUIRED_ENV_VARS:
    if not os.getenv(var):
        raise EnvironmentError(f"Missing required environment variable: {var}")

# Pixabay API configuration
PIXABAY_BASE_URL = "https://pixabay.com/api/"
PIXABAY_API_KEY = os.getenv("API_KEY")

# Redis configuration
try:
    redis_client = redis.Redis(
        host='redis-18594.c301.ap-south-1-1.ec2.redns.redis-cloud.com',
        port=18594,
        decode_responses=True,
        username="default",
        password=os.getenv("REDIS_PASSWORD")
    )
    redis_client.ping()  # Test connection
    logger.info("Redis connection established successfully")
except redis.ConnectionError as e:
    logger.error(f"Failed to connect to Redis: {e}")
    raise

# Initialize ML model
device = "cuda" if torch.cuda.is_available() else "cpu"
try:
    model = GPT2LMHeadModel.from_pretrained("gpt2").to(device)
    tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
    logger.info(f"Model loaded successfully on {device}")
except Exception as e:
    logger.error(f"Failed to load model: {e}")
    raise

# Global variables
global_count = 0
append_list = []

def generate_predicted_words(input_text: str) -> List[str]:
    """Generate predicted words using the GPT-2 model."""
    try:
        # Tokenize input
        inputs = tokenizer(input_text, return_tensors="pt").to(device)

        # Generate predictions
        with torch.no_grad():
            outputs = model(**inputs, return_dict=True)
            logits = outputs.logits

        # Process predictions
        last_token_logits = logits[:, -1, :]
        probabilities = torch.softmax(last_token_logits, dim=-1)
        top_50_probs, top_50_indices = torch.topk(probabilities, 50)
        top_50_tokens = [tokenizer.decode([idx], clean_up_tokenization_spaces=False) 
                        for idx in top_50_indices[0]]

        # Filter predictions
        removable_words = [' (', ' a', "'s", ' "', ' -', ' as', " '", "the", " the", 
                         "an", " an", "<|endoftext|>", 'â€™d', 'â€™m', 'â€™ll', 'tâ€™s']
        
        words = [token.strip().lower() for token in top_50_tokens 
                if len(token) > 1 and token not in removable_words]

        return words

    except Exception as e:
        logger.error(f"Error generating predictions: {e}")
        return []

def fetch_images_from_pixabay(query: str) -> Dict:
    """Fetch images from Pixabay API."""
    try:
        response = requests.get(
            PIXABAY_BASE_URL,
            params={
                "key": PIXABAY_API_KEY,
                "q": query,
                "image_type": "all",
                "per_page": "3"
            },
            timeout=5
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"Pixabay API error: {e}")
        return {"error": "Failed to fetch data from Pixabay"}

@app.route('/api/images', methods=['GET'])
def get_images():
    """Handle image retrieval requests."""
    query = request.args.get('query')
    correspond_id = request.args.get('id')

    if not query:
        return jsonify({"error": "Query parameter is required"}), 400

    try:
        # Check Redis cache
        cached_images = redis_client.get('image_cache')
        if cached_images:
            cached_data = json.loads(cached_images)
            for image in cached_data['hits']:
                if image.get('query_id') == correspond_id:
                    return jsonify(image['previewURL'])

        # Fetch from Pixabay if not in cache
        data = fetch_images_from_pixabay(query)
        if "error" in data:
            return jsonify(data), 500

        # Update cache
        for image in data['hits']:
            image['query_id'] = correspond_id

        if cached_images:
            cached_data = json.loads(cached_images)
            data['hits'] = cached_data['hits'] + data['hits']
            data['total'] = cached_data['total'] + data['total']

        redis_client.setex('image_cache', 86400, json.dumps(data))
        return jsonify(data['hits'][-1]['previewURL'])

    except Exception as e:
        logger.error(f"Error in get_images: {e}")
        return jsonify({"error": "Internal server error"}), 500



'''
GET is used in the case like this:
- It does not alter any server-side data or state, Hence GET
- Fetching Data/ Reading Data
- When user wants to see the data/ scrolls thorough the words

GET/api/display_words?count=1
- shows 
- No data sent to server
- Requesting to view data

Response:
[
    "word9", 'word10', 'word11', 'word12', 'word13', 'word14', 'word15', 'word16', 'word17'
]

'''


@app.route('/api/display_words', methods=['GET'])
def get_display_words():
    """Handle word display requests."""
    try:
        count = int(request.args.get('count', global_count))
        start_index = 9 * count
        end_index = start_index + 9

        if start_index >= len(DEFAULT_PREDICTED_WORDS):
            count = 0
            start_index = 0
            end_index = 9

        return jsonify(DEFAULT_PREDICTED_WORDS[start_index:end_index])

    except ValueError as e:
        return jsonify({"error": "Invalid count parameter"}), 400
    except Exception as e:
        logger.error(f"Error in get_display_words: {e}")
        return jsonify({"error": "Internal server error"}), 500

@app.route('/api/most_repeated_sentence', methods=['GET'])
def fetch_most_repeated_sentences():
    '''
    Most_repeated_sentences.txt
    Hello world: 3
    Python is cool: 2
    Programming is fun: 1
    Testing code: 1
    Flask API: 1
    

    API response:
    [
        "Hello world",
        "Python is cool",
        "Programming is fun",
        "Testing code",
        "Flask API"
    ]
    
    '''

    try:
        with open('hackthon_ktm\most_repeated_sentences.txt', 'r') as file:
            lines = [line.strip().split(':')[0] for line in file.readlines()[:5]]
        return jsonify(lines), 200
    except FileNotFoundError:
        return jsonify({"error": "File not found"}), 404
    except Exception as e:
        logger.error(f"Error in fetch_most_repeated_sentences: {e}")
        return jsonify({"error": "Internal server error"}), 500

    
'''
POST is used in the case like this: 
- Sending Data
- When user types a word
1) Post/api/guu
Body: {
    "item": "Hello"
}

Response:
[
   "predicted1", "predicted2", "predicted3", "predicted4", "predicted5", "predicted6", "predicted7", "predicted8", "predicted9"
]

'''



@app.route('/api/guu', methods=['POST'])
def predict_words():
    """Handle word prediction requests."""
    global append_list, global_count

    try:
        data = request.get_json()
        if not isinstance(data, dict):
            return jsonify({"error": "Invalid JSON format"}), 400

        input_text = data.get('item', '').strip()
        if not input_text:
            return jsonify({"error": "No input text provided"}), 400

        # Handle reset request
        if input_text == "1":
        
            with open('dataset.txt', 'a') as file:
                file.write(' '.join(append_list) + '\n')
            
            append_list = []
            global_count = 0
            
            repeated_sentences = get_most_repeated_sentences('hackthon_ktm/dataset.txt')
            save_most_repeated_sentences(repeated_sentences, 'most_repeated_sentences.txt')
            
            return jsonify(DEFAULT_PREDICTED_WORDS[:9])

        # Generate predictions
        append_list.append(input_text)
        combined_input = ' '.join(append_list)
        predicted_words = generate_predicted_words(combined_input)
        
        return jsonify(predicted_words[:9])

    except Exception as e:
        logger.error(f"Error in predict_words: {e}")
        return jsonify({"error": "Internal server error"}), 500
    
    

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
    
    
    
    