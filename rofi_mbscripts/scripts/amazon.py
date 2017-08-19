#!/bin/env python3

import mbrofi

# user variables

# application variables

# launcher variables
MSG = "Search on amazon."
PROMPT = "amazon:"
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


def amazon(query):
    query.replace(" ", "+")
    url="https://www.amazon.com/s?url=search-alias%3Daps&field-keywords=" \
            + query
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
        amazon(FILTER)
        break
    elif (EXIT == 1):
        # This is the case where rofi is escaped (should EXIT)
        break
    else:
        break
