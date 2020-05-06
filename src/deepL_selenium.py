# Classical Python lib
import os
import json
import clipboard

# Web collection lib
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from default_selenium import seleniumDefault # project local

# Log lib
import logging
import logzero
from logzero import logger

    
class seleniumDeepL(seleniumDefault):
    """ This class
    """

    def __init__(self, destination_language='en', **kwargs):
        """
        """
        super(seleniumDeepL, self).__init__(**kwargs)
        self.sleep(2, 'Opening DeepL app.')

        self.translations = {}
        self.display_sleep_time = True
        
        self.default_url='https://www.deepl.com/<lang>/translator'
        self.destination_language = destination_language

        self.set_url()
        self.load_url()

        self.languages = ['fr', 'en', 'de', 'es', 'pt', 'it', 'nl', 'pl', 'ru', 'ja', 'zh']

    def set_url(self):
        """ Transforms the self.default_url into self.url depending on selected self.destination_language
            NB : The self.url is the one sent to the selenium driver.
        """
        self.url = self.default_url.replace('<lang>', self.destination_language)


    def add_source_text(self, sentence):
        """Place the text to be traducted into the textbox on www.deepl.com
        PARAMETER:
            - sentence : str - text to be translated
        """
        clipboard.copy(sentence)
        input_css = 'div.lmt__inner_textarea_container textarea'
        input_area = self.driver.find_element_by_css_selector(input_css)
        
        input_area.clear() # self.sleep(1)
        input_area.send_keys(Keys.SHIFT, Keys.INSERT)
     
  
    def get_translation_copy_button(self):
        """When text is translated, we get it back by clicking on the "Copy to clipboard" button.
           This function gets that button.
        """
        button_css = ' div.lmt__target_toolbar__copy button' 
        button = self.driver.find_element_by_css_selector(button_css)
        # attribute "_dl-attr should be onClick: $0.doCopy"
        return button


    def get_translation(self, sleep_before_click_to_clipboard=2):
        """ Click on the get to clipboard button of deepL and then return the results.
            As page might be long depending on text size, we scroll to the button so that we can click on it. 
        """
        button = self.get_translation_copy_button()
        self.scroll_to_element(button, sleep_before_click_to_clipboard)
        button = self.get_translation_copy_button()
        button.click() # self.sleep(1)
        content = clipboard.paste()
        return content


    def save_translations(self, file_path):
        """ Store the translations effectuated so far as a json file.
        PARAMETERS:
            - file_path : str - destination path for the translation json.
        """
        with open(file_path, 'w') as jfile:
            json.dump(self.translations, jfile, indent=4, separators=(',', ': '), sort_keys=True)


    def load_translations(self, file_path):
        """ Loads pre-existing translations not to do them multiple times.
        PARAMETERS:
            - file_path : str  - source path of the translation json.
        NB : if file does not exist, continue wihtout data.
        NB : append translations. Possibility to load multiple files.
        """
        # Checking translation existence
        if not os.path.exists(file_path):
            logger.error('Specified path does not exist. Traduction not loaded.')
            logger.error('> {}'.format(file_path))
            return

        logger.debug('ici')

        # If exists loading it
        with open(file_path) as jfile:
            existing_translations = json.load(jfile)
        
        # And storring in translated corpus
        for original, translation in existing_translations.items():
            self.translations[original]=translation


    def prepare_batch_corpus(self, corpus, batch_value, joiner):
        """ Given a corpus of sentences, aggregate them by batch in order to make less request on DeepL website.
        """
        
        batch = []
        batch_corpus = []
        batch_iteration = 0
        
        nb_sentence = len(corpus)
        nb_iteration = int(nb_sentence/batch_value)
    
        for idx, sentence in enumerate(corpus):
            last_sentence = idx + 1 == nb_sentence
            
            # Don't add to batch if sentence already traducted
            if sentence in self.translations.keys():
                logger.debug('!!! Sentence already traducted.')
                self.print_translation(sentence, self.translations[sentence])
                # if not last_sentence: continue
                continue


            # Don't add to batch if sentence already in batch
            if sentence in batch:
                # if not last_sentence: continue
                continue


            batch.append(sentence)

            # If batch is full, batch is added
            if (batch_iteration < batch_value) and not last_sentence: #(idx + 1 < nb_sentence):
                batch_iteration += 1
                # if not last_sentence: continue
                continue


            batch_corpus.append({
                'text':joiner.join(batch),
                'size':len(batch),
                'joiner':joiner,
                'original_batch':batch
            })
            
            batch = []
            batch_iteration=0
            
        return batch_corpus


    def translation_process(self, corpus_batch, time_between_translation_iteration, time_batch_rest):
        """ The magic operates in here. Add sentences from a corpus batch to the translation corpus of the object.

        """
        logger.warning('************************ START TRANSLATION PROCESS ************************')
        nb_batch = len(corpus_batch)
        for idx_batch, batch in enumerate(corpus_batch):

            logger.warn('({}/{}) - nb translation iteration.'.format(idx_batch, nb_batch - 1)) 

            self.add_source_text(batch['text'])
            self.sleep(sleep=time_between_translation_iteration, message='Waiting for translation')
        
            full_translation = self.get_translation(sleep_before_click_to_clipboard=3)
            separate = full_translation.split(batch['joiner'])
        
            assertion_message = 'The number of sentences in the translation does not match the original number of sentences'
            assert len(separate)==batch['size'], assertion_message
            # Solution could be : 1) Use another joiner 2) not to use batches

            for idx_trad, sentence in enumerate(batch['original_batch']):
                translation = separate[idx_trad]
                self.translations[sentence] = translation
                self.print_translation(sentence, translation)

           
            self.sleep(time_batch_rest, 'Rest post translation.')
         
        logger.warning('************************* END TRANSLATION PROCESS *************************')



    def run_translation(
        self, corpus='Hello, World!', destination_language='en', joiner='\n____\n', quit_web=True, batch_value=10,
        time_between_translation_iteration=10, time_batch_rest=5,
        load_at=None, store_at=None ,load_and_store_at=None):

        # Check corpus format
        if type(corpus)==str:
            corpus = [corpus]

        # Eventually load translation
        if load_and_store_at:
            load_at, store_at = load_and_store_at, load_and_store_at
        if load_at:
            self.load_translations(file_path=load_at)
        
        # Prepare batched corpus
        corpus_batch = self.prepare_batch_corpus(corpus, batch_value, joiner)
        
        # Check data to translate
        if len(corpus_batch)==0:
            self.add_source_text('No data to translate. Closing window.')
            self.sleep(1, 'No data to translate.')
            return
            
        # Check destination language
        if destination_language!=self.destination_language:
            self.destination_language = destination_language
            self.set_url()
            self.load_url()

        # MAKE TRANSLATION ON DEEPL WITH CORPUS BATCHED
        self.translation_process(corpus_batch, time_between_translation_iteration, time_batch_rest)

        # Eventually load translation
        if store_at:
            self.save_translations(file_path=store_at)
        
        # Close the driver session if necessary
        if quit_web:
            self.close_driver()



    def print_translation(self, origin, translation, nb_car=75):
        """ Display a traducted sentence from the orginial dataset.
        PARAMETERS:
            - origin     : str - sentence in the corpus.
            - translation : str - sentence traducted by deepL. 

        NO OUTPUT. Only printing.
        """
        logger.debug('='*nb_car)
        logger.debug('Original text : {}'.format(origin))
        logger.debug('---  '*int(nb_car/5))
        logger.debug('Translation   : {}'.format(translation))
        logger.debug('='*nb_car)


    def get_translated_corpus(self):
        return self.translations
        


        


# from deepL_selenium import seleniumDeepL ; deepL = seleniumDeepL(driver_path='../chromedriver') ; deepL.run_translation()

if __name__ == "__main__":
    
    corpus_fr = [
        "Bonjour j'aimerais traduire tous ces documents",
        "Mais je ne suis pas sur d'avoir un niveau d'anglais suffisant",
        "Et surtout ! Je suis Data Scientistt, pas traducteur."
        ]

    corpus_en = [
        "Hi, I'd like to translate all these documents",
        "But I'm not sure I have a sufficient level of English",
        " And above all! I am Data Scientist, not a translator."
        ]


    deepL = seleniumDeepL(driver_path='../chromedriver', loglevel='debug')
    deepL.run_translation(corpus=corpus_fr, quit_web=False, destination_language='en', load_and_store_at='../translations/example.json')
    deepL.close_driver()
    