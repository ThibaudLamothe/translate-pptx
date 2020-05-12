# parameters
input_file = 'original.pptx'
output_file = 'translated.pptx'

# Opening presentation
prs = Presentation(input_file)

# List of all texts [text1, text2, ....]
corpus = extract_text_frames_from(prs)

# Dictionnary : {text1:translation1, text2:translation2, ...}
corpus_translated = get_translation(corpus)

# Replacing all values
for text_frame in  all_presentation_text_frames:
     for paragraph in text_frame.paragraphs:
            old_text = paragraph.text
            new_text = corpus_translated[old_text]
            paragraph.text = new_text

# Saving results
prs.save(output_file)
