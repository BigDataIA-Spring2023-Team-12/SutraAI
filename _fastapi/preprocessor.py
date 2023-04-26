import spacy


def preprocess_and_chunk(text, chunk_size=100):
    # load spaCy model
    nlp = spacy.load("en_core_web_sm")

    # remove stopwords and lemmatize words
    doc = nlp(text)
    filtered_text = [token.lemma_.lower() for token in doc if not token.is_stop and token.is_alpha]

    # split into larger chunks
    chunks = []
    current_chunk = ""
    current_chunk_size = 0
    for sentence in doc.sents:
        sentence_text = sentence.text.strip()
        sentence_length = len(sentence_text.split())

        # if adding the sentence would exceed the chunk size, start a new chunk
        if current_chunk_size + sentence_length > chunk_size:
            chunks.append(current_chunk.strip())
            current_chunk = sentence_text
            current_chunk_size = sentence_length
        else:
            current_chunk += " " + sentence_text
            current_chunk_size += sentence_length

    # add the final chunk
    if current_chunk:
        chunks.append(current_chunk.strip())

    # split each chunk on periods and commas and normalize the chunks
    normalized_chunks = []
    for chunk in chunks:
        subchunks = [subchunk.strip() for subchunk in chunk.split(".") if subchunk.strip()]
        for i, subchunk in enumerate(subchunks):
            subchunks[i] = [subsubchunk.strip() for subsubchunk in subchunk.split(",") if subsubchunk.strip()]
        normalized_chunks += [subchunk for subchunks in subchunks for subchunk in subchunks]

    return normalized_chunks
