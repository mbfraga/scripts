#!/bin/env python3

import mbrofi

# user variables

# application variables

# launcher variables
msg = "Search on youtube."
prompt = "youtube:"
answer=""
sel=""
filt=""
index=0
bindings=[]

# run correct launcher with prompt and help message
launcher_args = {}
launcher_args['prompt'] = prompt
launcher_args['mesg'] = msg
launcher_args['filter'] = filt
launcher_args['bindings'] = bindings
launcher_args['index'] = index


def list_entries():
    """Return entries to be displayed in rofi."""
    return([''])


def youtube(query):
    """Generate youtube search url from query"""
    query.replace(" ", "+")
    url = "https://www.youtube.com/results?search_query=" + query.strip()
    print("Opening url in browser: " + query)
    mbrofi.xdg_open(url)


def main_rofi_function(launcher_args):
    """Call main rofi function and return the selection, filter, selection
    index, and exit code. Don't return any of these in case of rofi being 
    escaped.
    """
    answer, exit = mbrofi.rofi(list_entries(), launcher_args)
    if exit == 1:
        return(False, False, False, 1)
    index, filt, sel = answer.strip().split(';')
    return(index, filt, sel, exit)


def main(launcher_args):
    """Main function."""
    while True:
        index, filt, sel, exit = main_rofi_function(launcher_args)
        launcher_args['filter'] = filt
        launcher_args['index'] = index
        if (exit == 0):
            # this is the case where enter is pressed
            youtube(filt)
            break
        elif (exit == 1):
            # this is the case where rofi is escaped (should exit)
            break
        else:
            break


if __name__ == "__main__":
    main(launcher_args)
