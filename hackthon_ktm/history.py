import re

# Load dataset from a text file
def load_dataset(file_path):
    with open(file_path, 'r') as file:
        sentences = file.readlines()
    return [sentence.strip() for sentence in sentences]

# Function to get unique next words
def get_unique_next_words_from_dataset(input_phrase, dataset):
    next_words = set()  # Use a set to store unique words

    # Process each sentence in the dataset
    for sentence in dataset:
        # Check if the sentence starts with the input phrase
        if sentence.lower().startswith(input_phrase.lower()):
            # Remove the input phrase from the sentence
            remaining_text = sentence[len(input_phrase):].strip()

            # Extract the first word after the input phrase
            if remaining_text:
                next_word = remaining_text.split()[0]  # Get the first word
                next_words.add(next_word)  # Add to the set for uniqueness

    return list(next_words)  # Convert set back to list for output
