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


print(preprocess_and_chunk("Gates was born and raised in Seattle. In 1975, he and Allen founded Microsoft in Albuquerque, New Mexico. It became the world's largest personal computer software company.[5][a] Gates led the company as chairman and CEO until stepping down as CEO in January 2000, succeeded by Steve Ballmer, but he remained chairman of the board of directors and became chief software architect.[8] During the late 1990s, he was criticized for his business tactics, which have been considered anti-competitive. This opinion has been upheld by numerous court rulings.[9] In June 2008, Gates transitioned to a part-time role at Microsoft and full-time work at the Bill & Melinda Gates Foundation, the private charitable foundation he and his then-wife Melinda established in 2000.[10] He stepped down as chairman of the board of Microsoft in February 2014 and assumed a new post as technology adviser to support the newly appointed CEO Satya Nadella.[11] In March 2020, Gates left his board positions at Microsoft and Berkshire Hathaway to focus on his philanthropic efforts on climate change, global health and development, and education.[12]"))
