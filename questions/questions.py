import nltk
import sys
import os
import string
from math import log

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
    files = {}
    for file in os.listdir(directory):
        with open(os.path.join(directory, file)) as f:
            files[file] = f.read()

    return files


def tokenize(document):
    """
    Given a document (represented as a string), return a list of all of the
    words in that document, in order.

    Process document by coverting all words to lowercase, and removing any
    punctuation or English stopwords.
    """
    # Tokenize words
    words = nltk.word_tokenize(document)

    # Get lower case words
    words = [word.lower() for word in words]

    # Filter punctuation
    words = [word for word in words
             if word not in list(string.punctuation)]

    # Filter stopwords
    words = [word for word in words
             if word not in nltk.corpus.stopwords.words("english")]

    return words


def compute_idfs(documents):
    """
    Given a dictionary of `documents` that maps names of documents to a list
    of words, return a dictionary that maps words to their IDF values.

    Any word that appears in at least one of the documents should be in the
    resulting dictionary.
    """
    words_idfs = {}
    num_of_docs = len(documents)

    for doc in documents:
        # Create a second dict without current doc
        other_documents = documents.copy()
        del other_documents[doc]

        for word in documents[doc]:
            if word not in words_idfs:
                num_docs_has_word = 1
                for other_doc in other_documents:
                    if word in other_documents[other_doc]:
                        num_docs_has_word += 1
                words_idfs[word] = log(num_of_docs/num_docs_has_word)

    return words_idfs


def top_files(query, files, idfs, n):
    """
    Given a `query` (a set of words), `files` (a dictionary mapping names of
    files to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the filenames of the the `n` top
    files that match the query, ranked according to tf-idf.
    """
    tf_idfs = dict.fromkeys(files.keys(), 0)
    # Calculate tf for each word of the query in each document
    for word in query:
        for doc in files:
            if word in files[doc]:
                # Sum tf_idf of current word
                tf_idfs[doc] += files[doc].count(word)*idfs[word]

    # Rank pages by their tf_idf
    ranking = []
    while len(ranking) < n:
        current_tf_idfs = {"doc": "",
                           "tf_idf": 0}
        for doc in tf_idfs:
            if tf_idfs[doc] > current_tf_idfs["tf_idf"]:
                current_tf_idfs = {"doc": doc,
                                   "tf_idf": tf_idfs[doc]}

        ranking.append(current_tf_idfs["doc"])

    return ranking


def top_sentences(query, sentences, idfs, n):
    """
    Given a `query` (a set of words), `sentences` (a dictionary mapping
    sentences to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the `n` top sentences that match
    the query, ranked according to idf. If there are ties, preference should
    be given to sentences that have a higher query term density.
    """
    sentences_idfs = list([0]*len(sentences))
    term_density = list([0]*len(sentences))
    # Calculate tf for each word of the query in each document
    for word in query:
        for i, sentence in enumerate(sentences):
            if word in sentences[sentence]:
                # Sum tf_idf of current word
                sentences_idfs[i] += idfs[word]
                term_density[i] += 1

    for i, sentence in enumerate(sentences):
        term_density[i] = term_density[i]/len(sentences[sentence])

    # Rank pages by their idf and term_density
    ranking = []
    while len(ranking) < n:
        current_idfs = {"sentence": "",
                        "idf": 0,
                        "term_density": 0}
        for i, sentence in enumerate(sentences):
            if sentences_idfs[i] > current_idfs["idf"]:
                current_idfs = {"sentence": sentence,
                                "idf": sentences_idfs[i],
                                "term_density": term_density[i]}

            elif (sentences_idfs[i] == current_idfs["idf"] and
                  term_density[i] > current_idfs["term_density"]):
                current_idfs = {"sentence": sentence,
                                "idf": sentences_idfs[i],
                                "term_density": term_density[i]}
        ranking.append(current_idfs["sentence"])

    return ranking


if __name__ == "__main__":
    main()
