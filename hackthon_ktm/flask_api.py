from flask import Flask, jsonify, request
from flask_cors import CORS
import torch
from transformers import GPT2LMHeadModel, GPT2Tokenizer
from history import load_dataset, get_unique_next_words_from_dataset

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Global variable to store the predicted words
predicted_words = []

# Predefined words for empty input
default_predicted_words = [
    "I", "What", "Hello", "Where", "Who", "How", "Can", "Is", "Are", "Could",
    "Would", "May", "Do", "Does", "Will", "Shall", "Did", "Have", "Has",
    "Had", "Am", "Were", "Was", "Should", "Might", "Must", "Please", "You",
    "He", "She", "They", "It", "This", "That", "These", "Those", "Let",
    "We", "My", "Your", "His", "Her", "Their", "Our", "The",
    "There", "Come", "Go", "Bring", "Take", "Give", "Help", "Want",
    "Need", "Eat", "Drink", "Sleep", "Play", "Run", "Walk", "Talk", "Call",
    "Find", "Make", "See", "Get", "Know"
]

def generate_predicted_words(input_text):
    global predicted_words
    print("THis is input text", input_text)
    
    # If the input is empty or just spaces, return the predefined list
    if not input_text.strip():
        predicted_words = default_predicted_words
        return
    print("This is awsome")
    # Load the model and tokenizer
    model = GPT2LMHeadModel.from_pretrained("gpt2")
    tokenizer = GPT2Tokenizer.from_pretrained("gpt2")

    # Load the dataset
    dataset_name = "dataset.txt"
    dataset = load_dataset(dataset_name)

    history_next_text = get_unique_next_words_from_dataset(input_text, dataset)

    # Tokenize input
    inputs = tokenizer(input_text, return_tensors="pt").to("cpu")

    # Forward pass through the model
    with torch.no_grad():
        outputs = model(**inputs, return_dict=True)
        logits = outputs.logits

    # Get the logits for the last token
    last_token_logits = logits[:, -1, :]
    probabilities = torch.softmax(last_token_logits, dim=-1)

    # Get the top 50 most probable next tokens
    top_50_probs, top_50_indices = torch.topk(probabilities, 50)
    top_50_tokens = [tokenizer.decode([idx]) for idx in top_50_indices[0]]

    words = []
    removable_words = [' (', ' a', "'s", ' "',' -', ' as', " '"]

    for i in top_50_tokens:
        if len(i) != 1 and i not in removable_words:
            words.append(i)

    # Combine words and history
    predicted_words = history_next_text + words  # Store the words globally


@app.route('/api/display_words', methods=['GET'])
def get_display_words():
    print("hehe")
    count = int(request.args.get('count', 0))  # Get the count from query parameters
    input_text = request.args.get('input', '').strip()  # Get input text from query parameters, default to empty

    if not predicted_words:  # Generate the list only once if it's not generated yet
        generate_predicted_words(input_text)

    # Serve the slice of predicted words based on the count
    start_index = 8 * count
    end_index = start_index + 8

    if start_index >= len(predicted_words):  # Reset if out of bounds
        count = 0
        start_index = 0
        end_index = 8

    display_words = predicted_words[start_index:end_index]

    return jsonify(display_words)



if __name__ == '__main__':
    app.run(debug=True)
