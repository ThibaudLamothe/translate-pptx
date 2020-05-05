from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import logzero
import logging
from logzero import logger
import clipboard

from default_selenium import seleniumDefault

    
class seleniumDeepL(seleniumDefault):
    def __init__(self, **kwargs):
        super(seleniumDeepL, self).__init__(**kwargs)
        self.url='https://www.deepl.com/translator'
        self.display_sleep_time = True
        self.set_loglevel('debug')
        self.traductions = {}

        self.sleep(2, 'Opening DeepL webpage')
        self.load_url()

    def add_source_text(self, sentence):
        input_css = 'div.lmt__inner_textarea_container textarea'
        input_area = self.driver.find_element_by_css_selector(input_css)
        input_area.clear()
        input_area.send_keys(sentence)

    def wait_for_traduction(self, time=3):
        self.sleep(time, 'Waiting for translation')

    def get_traduction(self):
        button_css = ' div.lmt__target_toolbar__copy button' 
        button = self.driver.find_element_by_css_selector(button_css)
        button.click()
        content = clipboard.paste()
        return content

    def print_traduction(self, origin, traduction, nb_car=75):
        logger.debug('='*nb_car)
        logger.debug('Original text : {}'.format(origin))
        logger.debug('---  '*int(nb_car/5))
        logger.debug('Translation   : {}'.format(traduction))
        logger.debug('='*nb_car)


    def run_traduction(self, corpus='Hello, World!', quit_web=True):

        logger.warning('************************ START TRANSLATION PROCESS ************************')
        if type(corpus)==str:
            corpus = [corpus]

        
        for sentence in corpus:
            if sentence in self.traductions.keys():
                logger.info('!!! Sentence already traducted.')
                self.print_traduction(sentence, self.traductions[sentence])
                continue
            self.add_source_text(sentence)
            self.wait_for_traduction()
            traduction = self.get_traduction()
            self.traductions[sentence] = traduction
            self.print_traduction(sentence, traduction)
         
        logger.warning('************************* END TRANSLATION PROCESS *************************')
        if quit_web:
            self.close_driver()
        
        


# from deepL_selenium import seleniumDeepL ; deepL = seleniumDeepL(driver_path='../chromedriver') ; deepL.run_traduction()

if __name__ == "__main__":
    
    corpus = [
        "Bonjour j'aimerais traduire tout ces documents",
        "Mais je ne suis pas sur d'avoir un niveau d'anglais suffisant",
        "Et surtout ! Je suis Data Scientistt, pas traducteur."
        ]

    deepL = seleniumDeepL(driver_path='../chromedriver')
    deepL.run_traduction(corpus=corpus, quit_web=False)
    deepL.close_driver()
