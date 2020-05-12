# For each paragraph of each text_frame    
for text_frame in  all_presentation_text_frames:
    for paragraph in text_frame.paragraphs:

        # We get the translated text
        old_text = text_frame.paragraphs[idx].text
        new_text = corpus_translated[old_text]

        # And inspect the runs (for font analysis)
        if len(paragraph.runs)>0:
            
            # If there is a run : we replace text without changing the font
            p = paragraph._p 
            for idx, run in enumerate(paragraph.runs):
                if idx == 0:
                    continue
                p.remove(run._r)
            paragraph.runs[0].text = new_text
        
        # If no runs, we can modify the text directly
        else:
            text_frame.paragraphs[idx].text = new_text