# How to translate ppt files ?

[Read my Medium article to discover how the library was built !](https://medium.com/@thibaud.lamothe2/using-selenium-and-deepl-to-automate-the-translation-of-power-point-files-3c01f81f113)

### Purpose

Free online translators of PowerPoint files have 2 main issues : 
- The translation API's are often neither robust to short half-sentences (very common in PowerPoints) not to long text traductions
- The structure of PowerPoint presentations are very complex (lots of unordered shapes) and after modification, nice presentation often get shapes misplaced  

This project aims to solve the problem and to automate the process of translating *.pptx files with the same nice-reendering as the original, with well-traducted sentences/expressions. 

### This repo contains materials to :
- Translate texts using [Selenium](https://selenium-python.readthedocs.io/) on [deepL](https://www.deepl.com/en/translator) translation website.
- Extract and modify PowerPoint texts from different objects with the powerful [python-pptx](https://python-pptx.readthedocs.io/en/latest/) library 


### 4 Scripts are available in `src` folder :
- [default_selenium.py](src/default_selenium.py) : `defaultSelenium` class contains the bases to connect to Selenium API and launch a website
- [deepL_selenium.py](src/deepL_selenium.py) :  `seleniumDeepL` inheritates from the previous one and contains all the interaction specifically needed to the deepL context 
- [ppt_interaction.py](src/ppt_interaction.py) : contains functions to inspect a presentations : from presentation, to slides, to shapes, to their `text_frame` properties.  
- [ppt_translation.py](src/ppt_translation.py) : uses both functions from ppt_interaction.py and `seleniumDeepL` to accomplish the final task : translating files.


# Running the translator

The translation object uses a `corpus` concept. Text must be given as a list of strings (each string equals to a sentence, max number of caracters in a single sentence is 4900 due to deepL's webpage limits). A translation example is provided.

There are 5 steps to run the translation on a corpus.

1. Clone the repo
> `git clone https://github.com/ThibaudLamothe/translate-pptx.git`


2. Download the selenium [chromedriver](http://chromedriver.storage.googleapis.com/index.html) at the project's root. By the way, Google Chrome needs to be installed.

3. Go to src folder
> `cd src/`


4. Install necessary libraries
> `pip install -r requirements.txt`

5. Run the deepL_selenium.py file
> `python deepL_selenium` 

The output is the following one :

<center><img src="https://github.com/ThibaudLamothe/translate-pptx/blob/master/fig/translation_example.png?raw=true" alt="drawing" width="500" /></center>


# Translator's features

Initiating the translator launchs the selenium driver and needs a driver to run correctly. This one has to be specified with the `driver_path` argument. The loglevel might also be indicated (error/warning/information/debug) depending on the level of information to track. See the previous picture.

 `deepL = seleniumDeepL(driver_path='../chromedriver', loglevel='debug')`

When running that command an empty internet pages open. We can now start the translation process.

## Functions available

The `seleniumDeepL` contains multiple methods, but only 4 are useful for the translation process. The other ones are only part of the processing.


__deepL.run_translation(__ _see next part for parameters_ __)__

This is the main function. It takes the corpus, transforms to better suit the deepL's website, make the traduction and store the results into a dictionnary.

__deepL.get_translated_corpus()__

It returns the dictionnary of the traducted sentences. Keys are the orginals sentences or group of words, values correspond to their translations.


__deepL.save_translations(json_path _as str_)__

It is possible to store the translated as a json file, using that function. It only needs one argument : the path to the json file as a string.

__deepL.load_translations(json_path _as str_)__

During the translation process, a sentence which has already been translated is not translated a second time. It is possible to reload translations from a previous run with that functions. It takes the path to a json file as a string.


## Running the translation

So far we've seen the 4 useful functions of `seleniumDeepL`. The `deepL.run_translation()` is the most important one. Wee'll see now how to correctly use and parameter it.

- __corpus__ (_as str or list, default_ : 'Hello, World!')

The corpus is the text to be translated. Can be a `string` or a `list` of strings. And as translating one sentence does not necessarly need automation, the list option is more interesting.

- __destination_language__ (_as str, default_ : `'en'`)


self.available_languages = ['fr', 'en', 'de', 'es', 'pt', 'it', 'nl', 'pl', 'ru', 'ja', 'zh']


- __joiner__ (_as str, default_ : `'\n____\n'`)


- __quit_web__ (_as boolean, default_ : True)

- __time_to_translate__ (_as integer, default_ : 10)

- __time_batch_rest__ (_as integer, default_ : 2)

- __raise_error__ (_as boolean, default_ : False)

- __load_at__ (_as string default_ : `None`)

- __store_at__ (_as string default_ : `None`)

- __load_and_store_at__ (_as string default_ : `None`)



# PPT Insertion
- Replacing text without modifying its look


# Good to know
_NB : the project was developped on MacOS and selenium used with Google Chrome_ 

# Resources


- [Changing the text but keeping the Font in python-pptx](https://github.com/scanny/python-pptx/issues/285)
- [Module-wide variables in Python (1/2)](how-to-create-module-wide-variables-in-python)
- [Module-wide variables in Python (2/2)](https://stackoverflow.com/questions/1977362/)
- [Selenium French Documentation](https://www.selenium.dev/documentation/fr/) 
- [Chromedriver](http://chromedriver.storage.googleapis.com/index.html)
- [CSS Selectors](https://saucelabs.com/resources/articles/selenium-tips-css-selectors) (recommended into the Selenium documentation)


# TODO
- Deal with bigger texts. Idea. Separate long sentences on \n's. Reconciliate them after translation. Do it at the reception and delivey of the corpus, so that no modification are done in the batch_corpus creation ?
