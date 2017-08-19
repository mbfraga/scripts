#!/bin/env python3
import mbrofi

# user variables

# application variables

# launcher variables
MSG = "Search on google."
PROMPT = "google:"
ANSWER=""
SEL=""
FILTER=""
INDEX=0
BINDINGS=[]

# run correct launcher with prompt and help message
launcher_args = {}
launcher_args['prompt'] = PROMPT
launcher_args['mesg'] = MSG
launcher_args['filter'] = FILTER
launcher_args['bindings'] = BINDINGS
launcher_args['index'] = INDEX


# function that creates a list for the launcher
def list_entries():
    return([''])


def google(query):
    query.replace(" ", "%20")
    url = "https://www.google.com/search?q=" + query.strip()
    print("Opening url in browser: " + query)
    mbrofi.xdg_open(url)


# main function that calls rofi with the settings and entries
def main_function():
    ANSWER, EXIT = mbrofi.rofi(list_entries(), launcher_args)
    if EXIT == 1:
        return(False, False, False, 1)
    INDEX, FILTER, SEL = ANSWER.strip().split(';')
    return(INDEX, FILTER, SEL, EXIT)

while True:
    INDEX, FILTER, SEL, EXIT = main_function()
    launcher_args['filter'] = FILTER
    launcher_args['index'] = INDEX
    if (EXIT == 0):
        # This is the case where enter is pressed
        google(FILTER)
        break
    elif (EXIT == 1):
        # This is the case where rofi is escaped (should EXIT)
        break
    else:
        break
