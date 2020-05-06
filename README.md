# How to translate ppt files ?

 `python-pptx` and `selenium`

## 1. PPT Extraction

- Checking we have all information with UPPER or EMPTY presentations
- Texts in shapes
- Texts in Tables
- Texts in other elements

## 2. Traduction with DeepL using Selenium
- Construction of the defaultSelenium class
- Construction of the DeepL class

<center><img src="https://github.com/ThibaudLamothe/translate-pptx/blob/master/fig/translation_example.png?raw=true" alt="drawing" width="500" /></center>

self.available_languages = ['fr', 'en', 'de', 'es', 'pt', 'it', 'nl', 'pl', 'ru', 'ja', 'zh']

## 3. PPT Insertion
- Replacing text without modifying its look


# Resources
https://python-pptx.readthedocs.io/en/latest/
https://github.com/scanny/python-pptx/issues/285
https://stackoverflow.com/questions/1977362/how-to-create-module-wide-variables-in-python
https://www.selenium.dev/documentation/fr/
https://selenium-python.readthedocs.io/

Chromedriver : http://chromedriver.storage.googleapis.com/index.html
CSS Selectors : https://saucelabs.com/resources/articles/selenium-tips-css-selectors
