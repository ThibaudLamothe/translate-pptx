# Python pip libraries
from pptx import Presentation

# Available in the repo
from deepL_selenium import seleniumDeepL
import ppt_interaction as ppt
from ppt_interaction import TextModification as tm


# DEFINING PATHs
file_source = '../ppts/medium.pptx'
file_dest =  '../ppts/medium_translated.pptx'
translation_path = '../translations/translations_medium.json'


# Get information from PowerPoint and store them in the Global list : ppt.CORPUS
ppt.browse_file(file_source, text_modif=tm.STORE_TEXT)

# Create translation object
deepL = seleniumDeepL(driver_path='../chromedriver', loglevel='info')

# (Load,) Run (& Store) Translations
deepL.run_translation(corpus=ppt.CORPUS, time_to_translate=20, destination_language='en',
                      load_and_store_at=translation_path, quit_web=False, raise_error=True)

# Close connection
deepL.close_driver()

# Set the translated corpus (dictionnary)
ppt.TRANSLATION =  deepL.get_translated_corpus()

# Make Power Point Translation
ppt.browse_file(file_source, file_dest, text_modif=tm.TRANSLATE, open_file=False)
 