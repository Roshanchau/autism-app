import torch
from transformers import GPT2LMHeadModel, GPT2Tokenizer

# Load the model and tokenizer
model = GPT2LMHeadModel.from_pretrained("gpt2")
tokenizer = GPT2Tokenizer.from_pretrained("gpt2")

# Move the model to CPU
model = model.to("cpu")

# Load dataset from a text file


def load_dataset(file_path):
    with open(file_path, 'r') as file:
        sentences = file.readlines()
    return [sentence.strip() for sentence in sentences]

# print("dataset", load_da)


# Specify the path to your dataset
dataset_file = 'dataset.txt'  # Update this to your file's location
dataset = load_dataset(dataset_file)

print(dataset)


# def predict_next_words(input_word):
#     # Check if the input word is in the dataset
#     possible_sentences = [sentence for sentence in dataset if sentence.lower(
#     ).startswith(input_word.lower())]

#     # If there are possible sentences, return them
#     if possible_sentences:
#         return possible_sentences

#     # If not, use the model to predict next words
#     inputs = tokenizer(input_word, return_tensors="pt").to("cpu")
#     with torch.no_grad():
#         outputs = model(**inputs, return_dict=True)
#         logits = outputs.logits

#     last_token_logits = logits[:, -1, :]
#     probabilities = torch.softmax(last_token_logits, dim=-1)
#     top_100_probs, top_100_indices = torch.topk(probabilities, 50)

#     # Decode the top 100 tokens
#     top_100_tokens = [tokenizer.decode([idx]) for idx in top_100_indices[0]]

#     # Filter out unwanted tokens
#     removable_words = ['(', 'a', "'s", '"', '-', 'as', "'"]
#     predicted_words = [token for token in top_100_tokens if len(
#         token) > 1 and token not in removable_words]

#     return predicted_words


# # Example usage
# input_word = "I want"
# predictions = predict_next_words(input_word)
# print(f"Possible next words for '{input_word}':", predictions)
