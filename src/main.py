# main.py
from tokenizer import Tokenizer
from parser import TRECParser
from indexer import Indexer
import os

def main():
    tokenizer = Tokenizer(r'C:\Users\src\Downloads\ir_project\stopwords.txt')
    parser = TRECParser()
    indexer = Indexer()

    data_dir = r'C:\Users\src\Downloads\ir_project\data'  # Directory containing TREC data files

    for filename in os.listdir(data_dir):
        filepath = os.path.join(data_dir, filename)
        if os.path.isfile(filepath):
            documents = parser.parse_documents(filepath)
            for doc in documents:
                docno = doc['docno']
                content = doc['content']
                tokenizer.add_to_file_dictionary(docno)
                doc_id = tokenizer.file_dictionary[docno]
                tokens = tokenizer.tokenize(content)
                tokenizer.add_to_word_dictionary(tokens)
                token_ids = [tokenizer.word_dictionary[token] for token in tokens]
                indexer.add_to_forward_index(doc_id, token_ids)
    
    # Build inverted index
    indexer.build_inverted_index()

    # Output parser_output.txt
    with open(r'C:\Users\src\Downloads\ir_project\output\parser_output.txt', 'w') as f:
        # Word Dictionary
        f.write("Word Dictionary:\n")
        for word, word_id in sorted(tokenizer.word_dictionary.items(), key=lambda x: x[1]):
            f.write(f"{word:<20}{word_id}\n")

        # File Dictionary
        f.write("\nFile Dictionary:\n")
        for docno, doc_id in sorted(tokenizer.file_dictionary.items(), key=lambda x: x[1]):
            f.write(f"{docno:<20}{doc_id}\n")

    # Save forward index
    with open(r'C:\Users\src\Downloads\ir_project\output\forward_index.txt', 'w') as f:
        for doc_id, tokens in indexer.forward_index.items():
            token_str = '; '.join([f"{token_id}: {freq}" for token_id, freq in tokens.items()])
            f.write(f"{doc_id}: {token_str}\n")

    # Save inverted index
    with open(r'C:\Users\src\Downloads\ir_project\output\inverted_index.txt', 'w') as f:
        for token_id, docs in indexer.inverted_index.items():
            doc_str = '; '.join([f"{doc_id}: {freq}" for doc_id, freq in docs.items()])
            f.write(f"{token_id}: {doc_str}\n")

if __name__ == '__main__':
    main()
