from flask import Flask, jsonify, request
from flask_cors import CORS
import torch
from transformers import GPT2LMHeadModel, GPT2Tokenizer
from history import load_dataset, get_unique_next_words_from_dataset

app = Flask(__name__)
CORS(app)

# Load the model and tokenizer once when the app starts
model = GPT2LMHeadModel.from_pretrained("gpt2").to("cuda" if torch.cuda.is_available() else "cpu")
tokenizer = GPT2Tokenizer.from_pretrained("gpt2")

# Global variables
predicted_words = []
append_list = []

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
    # Load the dataset
    dataset_name = ['C:\Users\bhand\OneDrive\Desktop\hackthon_ktm\scenerio\home_scenerio.txt', 'C:\Users\bhand\OneDrive\Desktop\hackthon_ktm\scenerio\school_school.txt', "dataset.txt"]
    dataset_name = "dataset.txt"
    dataset = load_dataset(dataset_name)

    history_next_text = get_unique_next_words_from_dataset(input_text, dataset)

    # Tokenize input
    inputs = tokenizer(input_text, return_tensors="pt").to(model.device)

    # Forward pass through the model
    with torch.no_grad():
        outputs = model(**inputs, return_dict=True)
        logits = outputs.logits

    # Get the logits for the last token
    last_token_logits = logits[:, -1, :]
    probabilities = torch.softmax(last_token_logits, dim=-1)

    # Get the top 50 most probable next tokens
    top_50_probs, top_50_indices = torch.topk(probabilities, 50)
    top_50_tokens = [tokenizer.decode([idx], clean_up_tokenization_spaces=False) for idx in top_50_indices[0]]

    words = []
    removable_words = [' (', ' a', "'s", ' "', ' -', ' as', " '", "the", " the", "an", " an", "<|endoftext|>, "]

    for token in top_50_tokens:
        if len(token) != 1 and token not in removable_words:
            words.append(token)

    return history_next_text + words

@app.route('/api/display_words', methods=['GET'])
def get_display_words():
    count = int(request.args.get('count', 0))
    label = "home"
    if label == "home":
        index = 0
    start_index = 9 * count
    end_index = start_index + 9

    if start_index >= len(predicted_words):  # Reset if out of bounds
        count = 0
        start_index = 0
        end_index = 9

    display_words = default_predicted_words[start_index:end_index]
    return jsonify(display_words)

@app.route('/api/guu', methods=['POST'])
def predict_words():
    global predicted_words, append_list

    try: 
        data = request.get_json()

        if not isinstance(data, dict):
            return jsonify({'error': 'Invalid JSON format'}), 400
        
        flag = data.get('flag', 0) 
        print("This is ", flag)
        if flag == 1:
            print("Empty")
            append_list = []
        
        input_text = data.get('item', '')
        if not input_text:
            return jsonify({'error': 'No input text provided'}), 400

        append_list.append(input_text)
        combined_input = ' '.join(append_list)
        
        predicted_words = generate_predicted_words(combined_input)

        return jsonify(predicted_words[:9])

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
