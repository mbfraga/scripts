#!/bin/env python3

import mbrofi

# user variables

# application variables
bindings = ["alt+o"]
bindings += ["alt+p"]

# launcher variables
msg = "Help text. " + bindings[0] + " does something, " +  \
        bindings[1]  + " does something else."
prompt = "template:"
answer=""
sel=""
filt=""
index=0

# run correct launcher with prompt and help message
launcher_args = {}
launcher_args['prompt'] = prompt
launcher_args['mesg'] = msg
launcher_args['filter'] = filt
launcher_args['bindings'] = bindings
launcher_args['index'] = index


def list_entries():
    """Get list of entries to be displayed via rofi."""
    return(['a', 'b', 'bb', 'c'])


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
            # This is the case where enter is pressed
            print("Main function of the script.")
            break
        elif (exit == 1):
            # This is the case where rofi is escaped (should exit)
            break
        elif (exit == 10):
            # What to do if first bindings is pressed
            # remove if nothing should be done
            print(bindings[0] + " was pressed!")
        elif (exit == 11):
            # What to do if second binding is pressed
            print(bindings[1] + " was pressed!")
        else:
            break


if __name__ == '__main__':
    main(launcher_args)
