from run_translation import translate_sentence


def translate_corpus(corpus):

    # Defining a joiner to separate the sentences
    joiner = '\n____\n'

    # Create a single "extended" string to load DeepL once
    full_text = corpus.join(joiner)

    # Running the translation process
    translated_text = translate_sentence(full_text)

    # Splitting the translation to get the list of sentences
    corpus_translated = translated_text.split(joiner)
    
    return corpus_translated

  
if __name__ == "__main__":


    # Sentences input
    sentence1 = 'I want to translate a first sentence without any link to the second one.'
    sentence2 = 'The starlings ate all the cherries in one afternoon, there won\'t be any more for us.''

    # Creation of the corpus as a list of strings
    corpus  = [sentence1, sentence2] 

    # Translating the full corpus
    corpus_translated = translate_corpus(corpus)

    # Checking that we have the  correct number of sentences after translation and split
    assert len(corpus)==len(corpus_translated)
    print("Translation of the corpus completed.")