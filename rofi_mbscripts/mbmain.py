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
        tempfiles = filerepo.filenames()
        files = []
        for f in tempfiles:
            if '.py' in f:
                files.append(f.split('.')[0])

        INDEX, FILTER, SEL, EXIT = main_function(files)
        if (EXIT == 0):
            # This is the case where enter is pressed
            print("Main function of the script.")
            mbrofi.run_mbscript(os.path.join(scripts_path, SEL + ".py"))
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
            print("Enabling " + sys.argv[2] + ".py ...")
            if '.py' not in sys.argv[2]:
                scriptname = sys.argv[2] + '.py'
            else:
                scriptname = sys.argv[2]
            enable_script(scriptname)
        elif sys.argv[1] == 'disable':
            if len(sys.argv) != 3:
                print("Invalid number of arguments. 'disable <scriptname>'")
                sys.exit(1)
            print("Disabling " + sys.argv[2] + ".py ...")
            if '.py' not in sys.argv[2]:
                scriptname = sys.argv[2] + '.py'
            else:
                scriptname = sys.argv[2]
            disable_script(scriptname)
        else:
            print("Invalid argument. Choose between enable/disable")
            sys.exit(1)
