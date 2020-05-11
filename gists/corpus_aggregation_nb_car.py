def prepare_batch_corpus(corpus, max_caracter=5000):

    # Size information
    nb_sentence = len(corpus)

    # Batch information (reset these values after each batch finalization)
    batch = []
    batch_length = 0

    # All batches are stored in that list, which will bbe the output of the function
    batch_corpus = []
    
    # Going throug each sentence of the initial corpus to create the batches
    for idx, sentence in enumerate(corpus):
        
        # Are we dealing with the last sentence ?
        last_sentence = idx + 1 == nb_sentence

        # Checking the batch size before adding a new sentence in it
        hypothetical_length = batch_length + len(sentence)
        if hypothetical_length < max_caracter:
            batch.append(sentence)
            batch_length += len(sentence) + len(joiner)
            
            # If sentence can be added to the corpus wa add it and don't save the corpus yet
            # Except if this is the last sentence
            if not last_sentence:
                continue
        
        # Finalizing batch beforee storing
        joined_batch = joiner.join(batch)
    
        # Save batch in the corpus
        batch_corpus.append(joined_batch)
        
        # Reseting batch parameters
        batch = []
        batch_length = 0
                    
    return batch_corpus