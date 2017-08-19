#!/bin/env python3

import mbrofi

# user variables

# application variables
bindings = ["alt+o"]
bindings += ["alt+p"]

# launcher variables
MSG = "Help text. " + bindings[0] + " does something, " +  \
        bindings[1]  + " does something else."
PROMPT = "template:"
ANSWER=""
SEL=""
FILTER=""
INDEX=0
BINDINGS=bindings

# run correct launcher with prompt and help message
launcher_args = {}
launcher_args['prompt'] = PROMPT
launcher_args['mesg'] = MSG
launcher_args['filter'] = FILTER
launcher_args['bindings'] = BINDINGS
launcher_args['index'] = INDEX


# function that creates a list for the launcher
def list_entries():
    return(['a', 'b', 'bb', 'c'])

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
        print("Main function of the script.")
        break
    elif (EXIT == 1):
        # This is the case where rofi is escaped (should EXIT)
        break
    elif (EXIT == 10):
        # What to do if first bindings is pressed
        # remove if nothing should be done
        print(bindings[0] + " was pressed!")
    elif (EXIT == 11):
        # What to do if second binding is pressed
        print(bindings[1] + " was pressed!")
    else:
        break
