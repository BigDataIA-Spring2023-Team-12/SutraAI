import spacy

# Load the spaCy model
nlp = spacy.load('en_core_web_sm')


def preprocess_and_chunk(text):
    """
    This function takes a string as input, performs NLP preprocessing using spaCy,
    removes stop words, lemmatizes the text, and chunks it into meaningful phrases
    using Named Entity Recognition (NER), dependency parsing, and noun chunking.

    Parameters:
    text (str): Input text to preprocess and chunk.

    Returns:
    chunks (list): List of chunks generated from the input text.
    """
    # Perform NLP preprocessing
    doc = nlp(text)

    # Remove stop words, punctuation marks, and lemmatize the text
    tokens = [token.lemma_.lower() for token in doc if not token.is_stop and not token.is_punct]

    # Chunk the text into meaningful phrases using NER, dependency parsing, and noun chunking
    chunks = []
    for chunk in doc.noun_chunks:
        chunks.append(chunk.text)
    for token in doc:
        if token.ent_type_ and token.ent_iob == 3:
            chunks.append(token.text)
        elif token.dep_ in ('ROOT', 'conj', 'appos'):
            chunks.append(token.text)

    return chunks
