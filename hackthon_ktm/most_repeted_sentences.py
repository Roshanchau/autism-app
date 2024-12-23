from collections import Counter

# Load dataset and strip sentences
# file_path = 'dataset.txt'

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
    with open(output_file, 'a') as file:
        for sentence, count in most_repeated:
            file.write(f"{sentence}: {count}\n")  # Write both sentence and count