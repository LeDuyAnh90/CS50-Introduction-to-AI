import nltk
import sys
import os
import math

FILE_MATCHES = 1
SENTENCE_MATCHES = 1


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python questions.py corpus")

    # Calculate IDF values across files
    files = load_files(sys.argv[1])
    file_words = {
        filename: tokenize(files[filename])
        for filename in files
    }
    file_idfs = compute_idfs(file_words)

    # Prompt user for query
    query = set(tokenize(input("Query: ")))

    # Determine top file matches according to TF-IDF
    filenames = top_files(query, file_words, file_idfs, n=FILE_MATCHES)

    # Extract sentences from top files
    sentences = dict()
    for filename in filenames:
        for passage in files[filename].split("\n"):
            for sentence in nltk.sent_tokenize(passage):
                tokens = tokenize(sentence)
                if tokens:
                    sentences[sentence] = tokens

    # Compute IDF values across sentences
    idfs = compute_idfs(sentences)

    # Determine top sentence matches
    matches = top_sentences(query, sentences, idfs, n=SENTENCE_MATCHES)
    for match in matches:
        print(match)


def load_files(directory):
    """
    Given a directory name, return a dictionary mapping the filename of each
    `.txt` file inside that directory to the file's contents as a string.
    """
    results = dict()

    for filename in os.listdir(directory):
        if not filename.endswith(".txt"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            results[filename] = contents
    return results


def tokenize(document):
    """
    Given a document (represented as a string), return a list of all of the
    words in that document, in order.

    Process document by coverting all words to lowercase, and removing any
    punctuation or English stopwords.
    """
    result = []
    document = document.lower()
    tokenizer = nltk.tokenize.RegexpTokenizer('\w+')
    tokenized = tokenizer.tokenize(document)
    for word in tokenized:
        if word not in nltk.corpus.stopwords.words("english"):
            result.append(word)
    result.sort()
    return result


def compute_idfs(documents):
    """
    Given a dictionary of `documents` that maps names of documents to a list
    of words, return a dictionary that maps words to their IDF values.

    Any word that appears in at least one of the documents should be in the
    resulting dictionary.
    """
    doc_count = len(documents)
    all_words = set()
    result = dict()
    for words in documents.values():
        for word in words:
            all_words.add(word)
    for word1 in all_words:
        appear = 0
        for word2 in documents.values():
            if word1 in word2:
                appear += 1
        result[word1] = math.log(doc_count/appear)
    return result
    # raise NotImplementedError


def top_files(query, files, idfs, n):
    """
    Given a `query` (a set of words), `files` (a dictionary mapping names of
    files to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the filenames of the the `n` top
    files that match the query, ranked according to tf-idf.
    """
    file_scores = {filename:0 for filename in files}    
    for filename in files:
        for word in query:
            if word in files[filename]:
                tf = files[filename].count(word)
                tf_idf = tf * idfs[word]
                file_scores[filename] += tf_idf
    sorted_files = sorted([filename for filename in files], key = lambda x : file_scores[x], reverse=True)
    return sorted_files[:n]

def top_sentences(query, sentences, idfs, n):
    """
    Given a `query` (a set of words), `sentences` (a dictionary mapping
    sentences to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the `n` top sentences that match
    the query, ranked according to idf. If there are ties, preference should
    be given to sentences that have a higher query term density.
    """
    sentence_score = {sentence:{'length':len(sentences[sentence]),'idf':0,'word_in_query':0} for sentence in sentences}
    for sentence in sentences:
        for word in query:
            if word in sentences[sentence]:
                idf = idfs[word]
                sentence_score[sentence]['idf'] += idf
                sentence_score[sentence]['word_in_query'] += 1
    sorted_sentence = sorted([sentence for sentence in sentences],key= lambda x: (sentence_score[x]['idf'], sentence_score[x]['word_in_query']/ sentence_score[x]['length']), reverse=True)
    return sorted_sentence[:n]
    # raise NotImplementedError


if __name__ == "__main__":
    main()
