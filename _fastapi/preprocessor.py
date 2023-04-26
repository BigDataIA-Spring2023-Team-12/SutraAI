import spacy
nlp = spacy.load("en_core_web_sm")


def preprocess_and_chunk(text: str) -> list:
    """
    This function performs preprocessing on input text, including sentence splitting,
    stop word removal, and lemmatization.

    Args:
    - text (str): a string of text to be preprocessed

    Returns:
    - chunks (List[str]): a list of preprocessed sentence chunks, where each chunk
      is a string containing one or more sentences
    """
    chunks = []

    # Process the text using spaCy
    doc = nlp(text)

    # Iterate over the sentences in the doc
    for sent in doc.sents:
        # Lemmatize the tokens in the sentence, remove stop words and non-alphabetic tokens
        tokens = [token.lemma_.lower() for token in sent if not token.is_stop and token.is_alpha]

        # Join the tokens into a string
        sentence = " ".join(tokens)

        # Append the sentence to the list of chunks
        if sentence:
            chunks.append(sentence)

    return chunks

