# Making necessary imports
import clipboard
from selenium.webdriver.common.keys import Keys

# Identifying the text area in the html structure
input_css = 'div.lmt__inner_textarea_container textarea'

# Connecting to it with our driver
input_area = driver.find_element_by_css_selector(input_css)

# Set the sentence into the clipboard
clipboard.copy(sentence)

# Making sure that there is no previous text
input_area.clear()

# Pasting the copied sentence into the input_area
input_area.send_keys(Keys.SHIFT, Keys.INSERT)
