from collections import Counter

# Load dataset and strip sentences
file_path = 'dataset.txt'

def sentences_name(file_path):
    with open(file_path, 'r') as file:
        sentences = file.readlines()
    return [sentence.strip() for sentence in sentences]

# Count the frequency of each sentence
def get_most_repeated_sentences(sentences):
    sentence_counts = Counter(sentences)  # Use Counter to count frequencies
    # Sort sentences by their frequency in descending order
    most_repeated = sentence_counts.most_common()
    return most_repeated

# Save most repeated sentences to a .txt file
def save_most_repeated_sentences(most_repeated, output_file):
    with open(output_file, 'w') as file:
        for sentence, count in most_repeated:
            file.write(f"{sentence}: {count}\n")  # Write both sentence and count

# Load and display most repeated sentences
sentences = sentences_name(file_path)
most_repeated_sentences = get_most_repeated_sentences(sentences)

# Save to output file
output_file_path = 'most_repeated_sentences.txt'
save_most_repeated_sentences(most_repeated_sentences, output_file_path)  # Pass the entire list

# Optional: Print the top 5 most repeated sentences
print(most_repeated_sentences[:5])
