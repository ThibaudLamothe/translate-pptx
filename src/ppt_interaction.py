import glob
from logzero import logger
from pptx import Presentation

import sys
config = sys.modules[__name__]
config.CORPUS = ['__CORPUS__']
config.DEEPL = None

def read_ppt_file(file_path):
    corpus = []
    prs = Presentation(file_path)
    for slide in prs.slides:
        for shape in slide.shapes:
            if hasattr(shape, "text"):
                print(shape.text)
                corpus.append(shape.text)
    return corpus


def read_folder_files(folder_path= '../ppts/'):
    request = folder_path + '*.pptx'
    for eachfile in glob.glob(request):
    
        print(eachfile)
        print("----------------------")
        read_ppt_file(eachfile)


def make_text_modif(text):
    if config.CORPUS:
        config.CORPUS.append(text)
    else:
        text = config.DEEPL.traductions[text]

    # Delete
    # text = ''
    
    # ToUpper
    # text = text.upper() 
    
    # Store
    # CORPUS.append(text)
    
    # Display
    # print(text)

    # Translate
    # text = deepL.traductions[text]

    return text


def replace_paragraph_text_retaining_initial_formatting(paragraph, new_text):
    p = paragraph._p  # the lxml element containing the `<a:p>` paragraph element
    # remove all but the first run
    for idx, run in enumerate(paragraph.runs):
        if idx == 0:
            continue
        p.remove(run._r)
    paragraph.runs[0].text = new_text


def translate_table(shape):
    logger.warning('TABLE')
    table = shape.table
    nb_rows = len(table.rows)
    nb_col = len(table.columns)
    for col in range(nb_col):
        for row in range(nb_rows):
            old_text = table.cell(row, col).text
            new_text = make_text_modif(old_text)
            table.cell(row, col).text = new_text
    return shape


def translate_text_shape(shape):
    text_frame = shape.text_frame
    for idx in range(len(text_frame.paragraphs)):
        is_font=False
        old_text = text_frame.paragraphs[idx].text
        new_text = make_text_modif(old_text)
        
        para = text_frame.paragraphs[idx]
        if len(para.runs)>0:
            replace_paragraph_text_retaining_initial_formatting(para, new_text)
        else:
            text_frame.paragraphs[idx].text = new_text

    return shape


def translate_shape(shape):
    
    # Basic text
    if shape.has_text_frame:
        shape = translate_text_shape(shape)

    # Table
    elif shape.has_table:
        shape = translate_table(shape)

    # Group
    elif shape.shape_type==6:
        logger.warning('GROUPED')
        shape = translate_slide(shape)
    return shape


def translate_slide(slide):
    for shape in slide.shapes:
        shape = translate_shape(shape)
    return slide

    
def translate_file(input_file, output_file=None): 
    """"search and replace text in PowerPoint while preserving formatting"""
    c = 0
    
    prs = Presentation(input_file)
    for slide in prs.slides:  
        logger.info('> NEW Slide : {}'.format(c + 1))
        slide = translate_slide(slide)
        c+= 1
    if output_file:
        prs.save(output_file)
