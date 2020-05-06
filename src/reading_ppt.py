
import glob
from logzero import logger
from pptx import Presentation

from deepL_selenium import seleniumDeepL
import ppt_interaction as ppt


if __name__ == "__main__":

    file_name = 'test'
    file_source = '../ppts/{}.pptx'.format(file_name)
    file_dest = file_source.replace('.pptx', '_translated.pptx')
    
    

    if False:
        # Display file content
        corpus = ppt.read_ppt_file(file_source)
        
    if False:
        ppt.CORPUS = ['__CORPUS__']
        translate_file(file_source, file_dest)
        print(file_dest, 'translated.')
        print(ppt.CORPUS)


    if True:
        ppt.CORPUS = ['__CORPUS__']
        ppt.translate_file(file_source)
        
        ppt.DEEPL = seleniumDeepL(driver_path='../chromedriver', loglevel='info')
        # ppt.DEEPL.load_traductions('traductions_tailnet.json')
        try:
            ppt.DEEPL.run_traduction(corpus=ppt.CORPUS, quit_web=False, time=12, batch_value=50, destination_language='de')
            ppt.DEEPL.close_driver()
            ppt.DEEPL.save_traductions('traductions_tailnet_de.json')
        except:
            ppt.DEEPL.close_driver()
            ppt.DEEPL.save_traductions('traductions_tailnet_de.json')
            raise


        # print(DEEPL.traductions)

        ppt.CORPUS = None
        ppt.translate_file(file_source, file_dest)
        print(file_dest, 'translated.')




