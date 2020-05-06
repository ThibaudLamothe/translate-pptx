
import glob
from logzero import logger
from pptx import Presentation

from deepL_selenium import seleniumDeepL
import ppt_interaction as ppt
from ppt_interaction import TextModification as tm


if __name__ == "__main__":

    file_name = 'test'
    file_source = '../ppts/{}.pptx'.format(file_name)
    file_dest = file_source.replace('.pptx', '_translated.pptx')
    translation_path = '../translations/translations_tailnet_chinese.json'
    
    
    # Get information from PowerPoint
    ppt.browse_file(file_source, text_modif=tm.STORE_TEXT)
    
    # Create translation object
    deepL = seleniumDeepL(driver_path='../chromedriver', loglevel='debug')
    
    # (Load,) Run (& Store) Translations
    try:
        deepL.run_translation(corpus=ppt.CORPUS, batch_value=50, destination_language='zh', load_and_store_at=translation_path, time_between_translation_iteration=12, quit_web=False,)
    except:
        deepL.close_driver()
        deepL.save_translations(translation_path.replace('.json', '_error.json'))
        raise
    
    # Close connection
    deepL.close_driver()

    # Set the translated corpus (dictionnary)
    cont = deepL.get_translated_corpus()
    ppt.TRANSLATION = cont

    # Make Power Point Translation
    ppt.browse_file(file_source, file_dest, text_modif=tm.TRANSLATE, open_file=True)




