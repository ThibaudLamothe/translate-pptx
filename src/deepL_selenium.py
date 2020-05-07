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
    """ Using Selenium to translate corpus of texts through https://www.deepl.com/fr/translator
    """

    def __init__(self, destination_language='en', **kwargs):
        """ In addition de seleniumDefault object, we can select the translation language when creating a seleniumDeepL.
        PARAMETERS:
            - driver_path          : str - path to the selenium driver (mandatory)
            - loglevel             : str - [debug/info/warning/error] (default is error). Adapt the level of information displayed in terminal.
            - destination_language : str - [fr/en/de/es/pt/it/nl/pl/ru/ja/zh] (default is 'en' for english).
        """

        super(seleniumDeepL, self).__init__(**kwargs)
        
        self.sleep(2, 'Opening DeepL app.')

        self.translations = {}
        self.display_sleep_time = True
        
        self.default_url='https://www.deepl.com/<lang>/translator'
        self.destination_language = destination_language

        self.set_url()
        self.load_url()

        self.available_languages = ['fr', 'en', 'de', 'es', 'pt', 'it', 'nl', 'pl', 'ru', 'ja', 'zh']


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
        self.paste_clipboard(input_area)
     
  
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
        PARAMETER:
            - file_path : str  - source path of the translation json.
        NB : if file does not exist, continue wihtout data.
        NB : append translations. Possibility to load multiple files.
        """

        # Checking translation existence
        if not os.path.exists(file_path):
            logger.error('Specified path does not exist. Traduction not loaded.')
            logger.error('{}'.format(file_path))
            return

        # If exists loading it
        with open(file_path) as jfile:
            existing_translations = json.load(jfile)
        
        # And storring in translated corpus
        for original, translation in existing_translations.items():
            self.translations[original]=translation


    def prepare_batch_corpus(self, corpus, joiner, max_caracter=4900):
        """ Given a corpus of sentences, aggregate them by batch in order to make less request on DeepL website.
        PARAMETERS:
            - corpus : list of str - 
            - joiner : str - 
            - max_caracter : int - 

        OUTPUT : list of dict - batches of sentences with batch descriptions (text as str/ size as int/ joiner as str / original_batch as list of str)
        """
        
        # Size information
        nb_sentence = len(corpus)
        nb_iteration = int(nb_sentence/batch_value)

        # Batch information (reset these values after each batch finalization)
        batch = []
        batch_corpus = []
        batch_length = 0
                
        # Flag used in case of a last sentence which is already translated
        erase_last_sentence = False

        # Going throug each sentence of the initial corpus to create the batches
        for idx, sentence in enumerate(corpus):
            last_sentence = idx + 1 == nb_sentence

            # Check sentence size
            if len(sentence)> max_caracter:
                logger.error('SENTENCE IS TOO LONG. Can not go through translation process. Use shorter text.')
                logger.error('Max authorized size is {}'.format(max_caracter))
                logger.error(sentence)
                # TODO : split too big sentences on '\n', translate separated parts and reconciliate them.
                raise

            # Don't add to batch if sentence already traducted
            if sentence in self.translations.keys():
                self.print_translation(sentence, self.translations[sentence])
                if not last_sentence: continue
                erase_last_sentence = True

            # Don't add to batch if sentence already in batch
            if sentence in batch:
                if not last_sentence: continue
                erase_last_sentence = True

            # Checking the batch size before adding a new sentence in it
            hypothetical_length = batch_length + len(sentence)
            if hypothetical_length < max_caracter:
                if not erase_last_sentence:
                    batch.append(sentence)
                    batch_length += len(sentence) + len(joiner)
                if not last_sentence: continue
            
            # Finalizing batch beforee storing
            joined_batch = joiner.join(batch)
            joined_batch_size = len(joined_batch)
            logger.info("Batch has size : {}".format(joined_batch_size))
            assert joined_batch_size < max_caracter, "Batch size size is too long for DeepL : {}".format(max_caracter)

            # Do not add an empty batch
            if joined_batch_size == 0:
                continue

            # Save batch in the corpus
            batch_corpus.append({
                'text':joined_batch,
                'size':len(batch),
                'joiner':joiner,
                'original_batch':batch
            })
            
            batch = []
            batch_length = 0
                       
        return batch_corpus


    def translation_process(self, corpus_batch, time_to_translate, time_batch_rest):
        """ The magic operates in here. Add sentences from a corpus batch to the translation corpus of the object.

        PARAMETERS
            - corpus_batch : list of dict :
            - time_to_translate : int
            - time_batch_rest : int
        """

        logger.warning('************************ START TRANSLATION PROCESS ************************')
        nb_batch = len(corpus_batch)
        for idx_batch, batch in enumerate(corpus_batch):

            logger.warning('({}/{}) - nb translation iteration.'.format(idx_batch, nb_batch - 1)) 

            self.add_source_text(batch['text'])
            self.sleep(sleep=time_to_translate, message='Waiting for translation')
        
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
        self, corpus='Hello, World!', destination_language='en', joiner='\n____\n', quit_web=True, 
        time_to_translate=10, time_batch_rest=2, raise_error=False,
        load_at=None, store_at=None ,load_and_store_at=None):
        """ THE FUNCTION. This is the one which is called by final user and sets (almost) all the other things.
        
        PARAMETERS:
            - corpus : 
            - destination_language :
            - joiner : 
            - quit_web :
            - time_to_translate :
            - time_batch_rest : time to wait at the end of an iteration before starting a new one.
            - load_at:
            - store_at : 
            - load_and_store_at : 

        NO OUTPUT. Results are stored in self.translations, accessible through self.get_translated_corpus()
        """

        # Check corpus format
        if type(corpus)==str:
            corpus = [corpus]

        # Eventually load translation
        if load_and_store_at:
            load_at, store_at = load_and_store_at, load_and_store_at
        if load_at:
            self.load_translations(file_path=load_at)
        
        # Prepare batched corpus
        corpus_batch = self.prepare_batch_corpus(corpus, joiner)
        logger.warn('Initial corpus is composed of {} sentences'.format(len(corpus)))
        logger.warn('Formated corpus is composed of {} batches'.format(len(corpus_batch)))
        
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
        try:
            self.translation_process(corpus_batch, time_to_translate, time_batch_rest)
        
        # Dealing with error if one occurring during translation process
        except:
            store_at = 'translation_error.json' if store_at is None else store_at.replace('.json', '_error.json')
            self.close_driver()
            self.print_translation_error(store_at)        
            if raise_error:
                self.save_translations(file_path=store_at)
                raise

        # Eventually store translation
        if store_at:
            self.save_translations(file_path=store_at)
        
        # Close the driver session if necessary
        if quit_web:
            self.close_driver()


    def get_translated_corpus(self):
        """ Returns the dictionnary of alreday traducted sentences
        
        OUTPUT:
            - {'sentence1':'trraduction_1', 'sentence_2':'traducation_2", ...}
        """

        return self.translations


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


    def print_translation_error(self, store_error_at, nb_car=100):
        """ Display message when error on translation.
            Inform user on the storage of already translated data.
        PARAMETERS:
            - store_error_at : str - sentence in the corpus.
            - nb_car         : int - define message size

        NO OUTPUT. Only printing.
        """

        logger.error('')
        logger.error('/!\\' * int(nb_car/3))
        logger.error('')
        logger.error('!' * nb_car)
        logger.error('!' * nb_car)
        logger.error('!!!!!!{}TRANSLATION ERROR'.format(' '*35))
        logger.error('!' * nb_car)
        logger.error('!!!!! > Translations temporary stored at :')
        logger.error('*' * nb_car)
        special_str = '*' * (int((nb_car - len(store_error_at)) / 2) - 2)
        logger.error('{}  {}  {}'.format(special_str, store_error_at, special_str))
        logger.error('*' * nb_car)
        logger.error('!!!!!! > You can input this file through "load_at" parameter for your next translation.')
        logger.error('!!!!!! > To solve the problem, you should try raise the time for translations.')
        logger.error('!' * nb_car)
        logger.error('!' * nb_car)
        logger.error('')
        logger.error('/!\\' * int(nb_car/3))
        logger.error('')
        


if __name__ == "__main__":
    
    # Defining a French example
    corpus_fr = [
        "Bonjour j'aimerais traduire tous ces documents",
        "Mais je ne suis pas sur d'avoir un niveau d'anglais suffisant",
        "Et surtout ! Je suis Data Scientistt, pas traducteur."
        ]

    # Defining an English example
    corpus_en = [
        "Hi, I'd like to translate all these documents",
        "But I'm not sure I have a sufficient level of English",
        "And above all! I am Data Scientist, not a translator."
        ]

    # Running en example
    translation_path = None  # '../translations/example.json'
    deepL = seleniumDeepL(driver_path='../chromedriver', loglevel='debug')
    deepL.run_translation(corpus=corpus_fr, quit_web=False, destination_language='en', load_and_store_at=translation_path, time_to_translate=1)
    deepL.close_driver()
    