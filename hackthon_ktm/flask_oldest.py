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

default_predicted_words = ['i', 'what', 'hello', 'where', 'who', 'how', 'can', 'is', 'are', 'could', 
 'would', 'may', 'can', 'please', 'will', 'shall', 'did', 'have', 'has', 
 'had', 'am', 'were', 'was', 'should', 'might', 'must', 'please', 'you', 
 'he', 'she', 'they', 'it', 'this', 'that', 'these', 'those', 'let', 
 'we', 'my', 'your', 'his', 'her', 'their', 'our', 'the', 
 'there', 'come', 'go', 'bring', 'take', 'give', 'help', 'want', 
 'need', 'eat', 'drink', 'sleep', 'play', 'run', 'walk', 'talk', 'call', 
 'find', 'make', 'see', 'get', 'know']

def generate_predicted_words(input_text,index =0):
    # Load the dataset
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
    removable_words = [' (', ' a', "'s", ' "', ' -', ' as', " '", "the", " the", "an", " an", "<|endoftext|>", 'â€™d','â€™m', 'â€™ll','tâ€™s' ,]

    for token in top_50_tokens:
        if len(token) != 1 and token not in removable_words:
            words.append(token.strip().lower())

    return history_next_text + words

@app.route('/api/display_words', methods=['GET'])
def get_display_words():
    count = int(request.args.get('count', 0))
    start_index = 9 * count
    end_index = start_index + 9

    if start_index >= len(predicted_words):  # Reset if out of bounds
        count = 0
        start_index = 0
        end_index = 9

    display_words = default_predicted_words[start_index:end_index]
    return jsonify(display_words)


# @app.route('/api/scenerio', methods=['POST'])
# # @app.route('/api/select_location', methods=['GET'])
# def scenerio():
#     # Get the query parameter from the URL, e.g., /api/select_location?place=home
#     place = request.args.get('place')
#     if place == "home":
    


    # display_words = default_predicted_words[start_index:end_index]
    # return jsonify(display_words)


@app.route('/api/huu', methods=['GET'])
def fetch_most_repeated_sentences():  # Ensure the function name is unique
    try:
        with open('most_repeated_sentences.txt', 'r') as file:
            # Read the first 5 lines
            lines = []
            for _ in range(5):
                text = file.readline().strip().split(":")[0]
                print(text)
                lines.append(text)
                
            # lines = [file.readline().strip().split(':')[0] for _ in range(5)]
        
        return jsonify(lines), 200  # Return the lines as JSON with a 200 OK status
    except FileNotFoundError:
        return jsonify({"error": "File not found."}), 404  # Handle file not found error
    except Exception as e:
        return jsonify({"error": str(e)}), 500  # Handle other potential errors



@app.route('/api/guu', methods=['POST'])
def predict_words():
    global predicted_words, append_list

    try:
        data = request.get_json()
        print("Received data:", data)

        if not isinstance(data, dict):
            return jsonify({'error': 'Invalid JSON format'}), 400
        
        input_text = data.get('item', '').strip()  # Ensure we are checking the stripped input

        # Handle case when input_text is "1"
        if input_text == "1":
            print("Resetting append_list")
            append_list = []  # Reset the append list
            return jsonify(default_predicted_words[:9])  # Return the default words

        if not input_text:
            return jsonify({'error': 'No input text provided'}), 400

        append_list.append(input_text)
        print("Current append list:", append_list)
        combined_input = ' '.join(append_list)
        print("Combined input for prediction:", combined_input)
        predicted_words = generate_predicted_words(combined_input)
        print("Predicted words:", predicted_words)

        return jsonify(predicted_words[:9])

    except Exception as e:
        print(f"An error occurred: {str(e)}")  # Log the error message
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='192.168.1.66', port=5000, debug=True)