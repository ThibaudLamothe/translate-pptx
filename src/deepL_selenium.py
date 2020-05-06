from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import logzero
import logging
import os
import json
from logzero import logger
import clipboard
from selenium.webdriver.common.action_chains import ActionChains
from default_selenium import seleniumDefault

    
class seleniumDeepL(seleniumDefault):
    def __init__(self, destination_language='en', **kwargs):
        super(seleniumDeepL, self).__init__(**kwargs)
        self.sleep(2, 'Opening DeepL app.')

        self.traductions = {}
        self.display_sleep_time = True
        
        self.default_url='https://www.deepl.com/<lang>/translator'
        self.destination_language = destination_language

        self.set_url()
        self.load_url()

    def set_url(self):
        self.url = self.default_url.replace('<lang>', self.destination_language)


    def add_source_text(self, sentence):
        clipboard.copy(sentence)
        input_css = 'div.lmt__inner_textarea_container textarea'
        input_area = self.driver.find_element_by_css_selector(input_css)
        
        input_area.clear() # self.sleep(1)
        input_area.send_keys(Keys.SHIFT, Keys.INSERT)
     
    def wait_for_traduction(self, time=3):
        self.sleep(time, 'Waiting for translation')


    def get_translation_button(self):
        button_css = ' div.lmt__target_toolbar__copy button' 
        button = self.driver.find_element_by_css_selector(button_css)
        # attribute "_dl-attr should be onClick: $0.doCopy"
        return button

    def get_traduction(self, sleep_before_click_to_clipboard=2):
        button = self.get_translation_button()
        self.scroll_to_element(button, sleep_before_click_to_clipboard)
        button = self.get_translation_button()
        button.click()
        self.sleep(1)
        content = clipboard.paste()
        return content

    def print_traduction(self, origin, traduction, nb_car=75):
        logger.debug('='*nb_car)
        logger.debug('Original text : {}'.format(origin))
        logger.debug('---  '*int(nb_car/5))
        logger.debug('Translation   : {}'.format(traduction))
        logger.debug('='*nb_car)

    def save_traductions(self, file_path):
        with open(file_path, 'w') as jfile:
            json.dump(self.traductions, jfile, indent=4, separators=(',', ': '), sort_keys=True)

    def load_traductions(self, file_path):
        with open(file_path) as jfile:
            existing_translations = json.load(jfile)
        for original, translation in existing_translations.items():
            self.traductions[original]=translation



    def run_traduction(self, corpus='Hello, World!', quit_web=True, time=10, batch_value=10, destination_language='en', buffer_time_rest=5):

        if destination_language!=self.destination_language:
            self.destination_language = destination_language
            self.set_url()
            self.load_url()


        logger.warning('************************ START TRANSLATION PROCESS ************************')
        if type(corpus)==str:
            corpus = [corpus]

        batch_iteration = 0
        buffer = []
        joiner = '\n____\n'
        nb_sentence = len(corpus)
        nb_iteration = int(len(corpus)/batch_value)
        iteration_count = 0
        for idx, sentence in enumerate(corpus):
            last_sentence = idx + 1 == nb_sentence
            

            if sentence in self.traductions.keys():
                logger.debug('!!! Sentence already traducted.')
                self.print_traduction(sentence, self.traductions[sentence])
                if not last_sentence: continue
            
            if sentence in buffer:
                if not last_sentence: continue

            
            if last_sentence and buffer==[]:
                logger.error('No new data to be translated.')
                continue


            buffer.append(sentence)
            if (batch_iteration < batch_value) and (idx + 1 < nb_sentence):
                batch_iteration += 1
                if not last_sentence: continue

            iteration_count +=1
            logger.warn('({}/{}) - nb translation iteration.'.format(iteration_count, nb_iteration)) 
            joined = joiner.join(buffer)
            

            self.add_source_text(joined)
            self.wait_for_traduction(time)

            full_traduction = self.get_traduction(sleep_before_click_to_clipboard=3)
            separate = full_traduction.split(joiner)
        
            assertion_message = 'The number of sentences in the traduction does not match the original number of sentences'
            assert len(separate)==len(buffer), assertion_message
            # Solution could be : 1) Use another joiner 2) not to use batches

            for idx_trad, sentence in enumerate(buffer):
                traduction = separate[idx_trad]
                self.traductions[sentence] = traduction
                self.print_traduction(sentence, traduction)

            batch_iteration=0
            buffer = []
            self.sleep(buffer_time_rest, 'Repos après traduction.')
         
        logger.warning('************************* END TRANSLATION PROCESS *************************')
        if quit_web:
            self.close_driver()
        
        


# from deepL_selenium import seleniumDeepL ; deepL = seleniumDeepL(driver_path='../chromedriver') ; deepL.run_traduction()

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
    deepL.load_traductions('traductions.json')
    deepL.run_traduction(corpus=corpus_fr, quit_web=False, destination_language='en')
    deepL.close_driver()
    deepL.save_traductions('traductions.json')

    # print(deepL.traductions)
