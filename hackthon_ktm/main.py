import torch
from transformers import GPT2LMHeadModel, GPT2Tokenizer
from history import load_dataset, get_unique_next_words_from_dataset

# Load the model and tokenizer
model = GPT2LMHeadModel.from_pretrained("gpt2")
tokenizer = GPT2Tokenizer.from_pretrained("gpt2")


dataset_name = "dataset.txt"
dataset = load_dataset(dataset_name)


refresh = False
refresh_value = 0



input_text = "i feel"
history_next_text = get_unique_next_words_from_dataset(input_text, dataset)
print(f"Unique next words for '{input_text}':", history_next_text)


# Move the model to CPU (this is the default, but we can be explicit)
model = model.to("cpu")


input_text = ""

# Tokenize input (no need to move to device since it's CPU by default)
inputs = tokenizer("i want, after this sentence give noun", return_tensors="pt").to("cpu")

# Forward pass through the model to get logits
with torch.no_grad():
    outputs = model(**inputs, return_dict=True)
    logits = outputs.logits

# Get the logits for the last token (the token corresponding to the last input)
last_token_logits = logits[:, -1, :]

# Apply softmax to get probabilities
probabilities = torch.softmax(last_token_logits, dim=-1)

# Get the top 100 most probable next tokens 
top_100_probs, top_100_indices = torch.topk(probabilities, 50)

# Decode the top 100 tokens and their probabilities
top_100_tokens = [tokenizer.decode([idx]) for idx in top_100_indices[0]]



words =[]
removable_words  = [' (', ' a', "'s", ' "',' -', ' as', " '"]

for i in top_100_tokens:
    if len(i) != 1 and i not in removable_words:
        words.append(i)
        
start = 0
end = 8
predicted_words = history_next_text + words
print(predicted_words)
display_words = predicted_words[start: end]
if refresh and (end+8)< len(predicted_words):
    
    display_words = predicted_words[start+8*refresh_value: end+8*refresh_value]
    
print("predicted_words",predicted_words)
print("display_words", display_words)
