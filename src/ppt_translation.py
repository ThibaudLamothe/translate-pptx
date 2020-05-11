# Python pip libraries
from logzero import logger
from pptx import Presentation

# Available in the repo
from deepL_selenium import seleniumDeepL
import ppt_interaction as ppt
from ppt_interaction import TextModification as tm


if __name__ == "__main__":

    # PATH for execution
    file_name = 'test'
    file_source = '../ppts/{}.pptx'.format(file_name)
    file_dest = file_source.replace('.pptx', '_translated.pptx')
    translation_path = '../translations/translations_bd_small.json'
    translation_path = None


    # # DEFINING PATH
    # file_source = '../ppts/medium.pptx'
    # file_dest =  '../ppts/medium_translated.pptx'
    # translation_path = '../translations/translations_medium.json'


    # Get information from PowerPoint
    ppt.browse_file(file_source, text_modif=tm.STORE_TEXT)
    
    # Create translation object
    deepL = seleniumDeepL(driver_path='../chromedriver', loglevel='info')

    # (Load,) Run (& Store) Translations
    deepL.run_translation(corpus=ppt.CORPUS, time_to_translate=60, destination_language='en',
                          load_and_store_at=translation_path, quit_web=False, raise_error=True)

    # Close connection
    deepL.close_driver()

    # Set the translated corpus (dictionnary)
    ppt.TRANSLATION =  deepL.get_translated_corpus()

    # Make Power Point Translation
    ppt.browse_file(file_source, file_dest, text_modif=tm.TRANSLATE, open_file=True)
