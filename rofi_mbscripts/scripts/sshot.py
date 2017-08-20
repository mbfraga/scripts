#!/bin/env python3

import os
import sys
from subprocess import Popen, PIPE
from datetime import datetime, date, time

import mbrofi

# user variables
upload=False

# application variables
delay = "0"
bindings = ["alt+d"]
bindings += ["alt+u"]
bindings += ["alt+i"]

# launcher variables
msg = "Enter to take screenshot, " + \
        bindings[0] + " to add delay, " +  \
        bindings[1]  + " to toggle upload, " + \
        bindings[2]  + " for interactive."

prompt = "sshot"
answer=""
sel=""
filt=""
index=0

# run correct launcher with prompt and help message
launcher_args = {}
if upload:
    launcher_args['prompt'] = prompt + "(upload):"
else:
    launcher_args['prompt'] = prompt + "(noupload):"
launcher_args['mesg'] = msg
launcher_args['filter'] = filt
launcher_args['bindings'] = bindings
launcher_args['index'] = index


def list_entries(delay="0"):
    """Get list of entries to be displayed via rofi."""
    proce = Popen(['sshot', 'list'], stdout=PIPE)
    answer = proce.stdout.read().decode('utf-8')
    exit_code = proce.wait()
    tmp_answer=answer.strip().split('\n')
    entries=[]
    for ans in tmp_answer:
        if (int(delay) > 0):
            newans = "-d " + str(delay) + " " + ans.strip()
        else:
            newans = ans.strip()
        entries.append(newans)

    if exit_code == 0:
        return(entries)
    else:
        return([])


def sshot(opts=[], upload=False):
    """Call sshot and upload screenshot. Returns the image name.
    
    Keyword arguments:
    opts -- options to send to sshot (default [])
    upload -- boolean to decide whether to upload screenshot or not.
              (default False)
    """
    my_env = os.environ.copy()
    date=datetime.now()
    imgname = "sshot-" + date.strftime('%Y-%m-%d_%H:%M:%S') + ".png"
    command = []
    if upload:
        my_env['SSHOT_UPLOAD'] = 'true'
    else:
        my_env['SSHOT_UPLOAD'] = 'false'
    my_env['IMGNAME'] = imgname

    command = ['sshot']
    command.extend(opts)
    proc = Popen(command, stdin=PIPE, stdout=PIPE, env=my_env)
    exit_code = proc.wait()
    if exit_code == 0:
        return(imgname)
    else:
        return(False)


def add_delay(delay_binding):
    """Show rofi menu to set a delay, and return the result as a string."""
    local_launcher_args = {}
    local_launcher_args['mesg'] = "Choose delay, or write custom one."
    local_launcher_args['mesg'] += " Press " + delay_binding + " to go back."
    local_launcher_args['prompt'] = "sshot (add delay):"
    local_launcher_args['format'] = "s"
    local_launcher_args['bindings'] = [delay_binding]
    delay, exit = mbrofi.rofi(["5","4","3","2","1","0"], local_launcher_args)
    if exit == 1:
        print("sshot.py delay menu was escaped, and right now" \
              + " this is set to abort the top script. This is expected " \
              + "behavior. Use '" + delay_binding + "' to go back to the" \
              + " main menu.")
        sys.exit(0)
    elif exit == 0:
        delay = delay.strip()
        try:
            d = int(delay)
            return(delay.strip())
        except ValueError:
            return(None)
    else:
        return(None)


def main_rofi_function(launcher_args, delay):
    """Call main rofi function and return the selection, filter, selection
    index, and exit code. Don't return any of these in case of rofi being 
    escaped.
    """
    answer, exit = mbrofi.rofi(list_entries(delay=delay), launcher_args)
    if exit == 1:
        return(False, False, False, 1)
    index, filt, sel = answer.strip().split(';')
    return(index, filt, sel, exit)


def main(launcher_args, upload, delay):
    """Main function."""
    while True:
        if upload:
            launcher_args['prompt'] = prompt + "(upload):"
        else:
            launcher_args['prompt'] = prompt + "(noupload):"
        index, filt, sel, exit = main_rofi_function(launcher_args, delay)
        launcher_args['filter'] = filt
        launcher_args['index'] = index
        if (exit == 0):
            sshot(opts=sel.split(" "), upload=upload)
            break
        elif (exit == 1):
            break
        elif (exit == 10):
            tmp_delay = add_delay(launcher_args['bindings'][0])
            if tmp_delay is not None:
                delay = tmp_delay
        elif (exit == 11):
            upload = (not upload)
        elif (exit == 12):
            print("Interactive Mode")
            imgname = sshot(opts=sel.split(" "), upload=upload)
            if imgname:
                mbrofi.run_mbscript('screenshots.py', [imgname])
            break
        else:
            break

if __name__ == '__main__':
    main(launcher_args, upload, delay)
