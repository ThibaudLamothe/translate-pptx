# Getting button location on  the html tree
button_css = ' div.lmt__target_toolbar__copy button' 

# Getting the button object
button = driver.find_element_by_css_selector(button_css)

# Extracting its position
y = button.location['y']

# Positionning the button into the screen
driver.execute_script("window.scrollTo(0, {})".format(y - 150))

# Getting the button object
# (again - its position has been actualized and we need to get the new positions for the click)
button = driver.find_element_by_css_selector(button_css)

# Making the click => translation is now in our clipboard
button.click()