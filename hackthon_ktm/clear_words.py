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
 'would', 'may', 'do', 'does', 'will', 'shall', 'did', 'have', 'has', 
 'had', 'am', 'were', 'was', 'should', 'might', 'must', 'please', 'you', 
 'he', 'she', 'they', 'it', 'this', 'that', 'these', 'those', 'let', 
 'we', 'my', 'your', 'his', 'her', 'their', 'our', 'the', 
 'there', 'come', 'go', 'bring', 'take', 'give', 'help', 'want', 
 'need', 'eat', 'drink', 'sleep', 'play', 'run', 'walk', 'talk', 'call', 
 'find', 'make', 'see', 'get', 'know']


def generate_predicted_words(input_text):
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
    removable_words = [' (', ' a', "'s", ' "', ' -', ' as', " '", "the", " the", "an", " an", "<|endoftext|>, "]

    for token in top_50_tokens:
        if len(token) != 1 and token not in removable_words:
            words.append(token)

    return history_next_text + words

# @app.route('/api/display_words', methods=['GET'])
# def get_display_words():
#     count = int(request.args.get('count', 0))
#     start_index = 9 * count
#     end_index = start_index + 9

#     if start_index >= len(predicted_words):  # Reset if out of bounds
#         count = 0
#         start_index = 0
#         end_index = 9

#     display_words = default_predicted_words[start_index:end_index]
    
        
#     sending = []
    
#     for i in display_words:
#         new_dict = {"words": i.lower(), "url": f"require('../assets/images/{i}.png')"}
#         sending.append(new_dict)
        
    
#     return jsonify({
#         'display_words': display_words[start_index:end_index],  # Return only the first 9 predicted words
#         'sending': sending  # Return the sending list
#     })

@app.route('/api/sending_words', methods=['GET'])
def get_sending_words():
    count = int(request.args.get('count', 0))
    start_index = 9 * count
    end_index = start_index + 9

    if start_index >= len(predicted_words):  # Reset if out of bounds
        count = 0
        start_index = 0
        end_index = 9

    display_words = default_predicted_words[start_index:end_index]
    # Create the sending list from default_predicted_words
    sending = []
    
    for word in display_words:
        new_dict = {"words": word, "url": f"require('../assets/images/{word}.png')"}
        sending.append(new_dict)
        
    return jsonify(sending)



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





        # # Update append_list with the new input text
        # append_list.append(input_text)
        
        # # Combine existing words in append_list
        # combined_input = ' '.join(append_list)
        
        # # Generate predicted words based on the combined input
        # predicted_words = generate_predicted_words(combined_input)
        
        # sending = []
        
        # for i in predicted_words:
        #     new_dict = {"words": i.lower(), "url": f"require('../assets/images/{i}.png')"}
        #     sending.append(new_dict)

        # print("This is sending", sending)
        
        # # Limit the number of predicted words to 9
        # return jsonify({
        #     'predicted_words': predicted_words[:9],  # Return only the first 9 predicted words
        #     'sending': sending  # Return the sending list
        # })