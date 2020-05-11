prs = Presentation(input_file)
for slide_number, slide in enumerate(prs.slides):  
    logger.info('NEW Slide : {}'.format(slide_number + 1))  