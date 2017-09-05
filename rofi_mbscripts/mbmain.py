#!/bin/env python3

import os
import sys


mbmain_path = os.path.dirname(os.path.realpath(sys.argv[0]))
scripts_path = os.path.join(mbmain_path, "scripts")
enabled_path = os.path.join(mbmain_path, "enabled")
sys.path.append(scripts_path)
import mbrofi


MSG = ""
PROMPT = "mbscripts:"
ANSWER=""
SEL=""
FILTER=""
INDEX=0
BINDINGS=[]

launcher_args = {}
launcher_args['prompt'] = PROMPT
launcher_args['mesg'] = MSG
launcher_args['filter'] = FILTER
launcher_args['bindings'] = BINDINGS
launcher_args['index'] = INDEX

def enable_script(scriptname):
    if (scriptname == "mbrofi.py"):
        print("mbrofi.py is not meant to be an mbscript, " +
              "it is a helper script.")
        sys.exit(1)
    spath = os.path.join(scripts_path, scriptname)
    epath = os.path.join(enabled_path, scriptname)
    if not os.path.isfile(spath):
        print("Script '" + scriptname + "' does not exist in " + scripts_path)
        sys.exit(1)

    if os.path.isfile(epath):
        print("Script '" + scriptname + "' already enabled.")
    else:
        os.symlink(spath, epath)


def disable_script(scriptname):
    pass


def main_function(mlist=[]):
    ANSWER, EXIT = mbrofi.rofi(mlist, launcher_args)
    if EXIT == 1:
        return(False, False, False, 1)
    INDEX, FILTER, SEL = ANSWER.strip().split(';')
    return(INDEX, FILTER, SEL, EXIT)

if __name__ == "__main__":
    if len(sys.argv) == 1:
        filerepo = mbrofi.FileRepo(enabled_path)
        filerepo.scan_files()
        files = filerepo.filenames()
        displaynames = []
        for f in files:
            if '.' in f:
                displaynames.append(f.split('.')[0])
            else:
                displaynames.append(f)
        INDEX, FILTER, SEL, EXIT = main_function(displaynames)
        if (EXIT == 0):
            # This is the case where enter is pressed
            print("Main function of the script.")
            mbrofi.run_mbscript(os.path.join(enabled_path, files[int(INDEX)]))
        elif (EXIT == 1):
            # This is the case where rofi is escaped (should EXIT)
            sys.exit(0)
        else:
            sys.exit(0)
    else:
        if sys.argv[1] == 'enable':
            if len(sys.argv) != 3:
                print("Invalid number of arguments. 'enable <scriptname>'")
                sys.exit(1)
            print("Enabling " + sys.argv[2] + " ...")
            scriptname = sys.argv[2]
            enable_script(scriptname)
        elif sys.argv[1] == 'disable':
            if len(sys.argv) != 3:
                print("Invalid number of arguments. 'disable <scriptname>'")
                sys.exit(1)
            print("Disabling " + sys.argv[2] + "...")
            scriptname = sys.argv[2]
            disable_script(scriptname)
        else:
            print("Invalid argument. Choose between enable/disable")
            sys.exit(1)
