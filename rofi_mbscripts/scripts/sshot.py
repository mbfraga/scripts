#!/bin/env python3

import mbrofi
from datetime import datetime, date, time
from subprocess import Popen, PIPE
import os

# user variables
upload=False

# application variables
bindings = ["alt+d"]
bindings += ["alt+u"]
bindings += ["alt+i"]
delay = "0"

# launcher variables
MSG = "Enter to take screenshot, " + \
        bindings[0] + " to add delay, " +  \
        bindings[1]  + " to toggle upload, " + \
        bindings[2]  + " for interactive."

PROMPT = "sshot"
ANSWER=""
SEL=""
FILTER=""
INDEX=0
BINDINGS=bindings

# run correct launcher with prompt and help message
launcher_args = {}
if upload:
    launcher_args['prompt'] = PROMPT + "(upload):"
else:
    launcher_args['prompt'] = PROMPT + "(noupload):"
launcher_args['mesg'] = MSG
launcher_args['filter'] = FILTER
launcher_args['bindings'] = BINDINGS
launcher_args['index'] = INDEX


# function that creates a list for the launcher
def list_entries(delay="0"):
    proce = Popen(['sshot', 'list'], stdout=PIPE)
    answer = proce.stdout.read().decode('utf-8')
    exit_code = proce.wait()
    TMP_ANSWER=answer.strip().split('\n')
    ANSWER=[]
    for ans in TMP_ANSWER:
        if (int(delay) > 0):
            newans = "-d " + str(delay) + " " + ans.strip()
        else:
            newans = ans.strip()
        ANSWER.append(newans)

    if exit_code == 0:
        return(ANSWER)
    else:
        return([])


def sshot(opts=[], upload=False):
    my_env = os.environ.copy()
    date=datetime.now()
    imgname = "sshot-" + date.strftime('%Y-%m-%d_%H:%M:%S') + ".png"
    command = []
    if upload:
        my_env['SSHOT_UPLOAD'] = 'true'
    else:
        my_env['SSHOT_UPLOAD'] = 'false'
    my_env['IMGNAME'] = imgname

    #command = 'sshot '
    #for opt in opts:
        #command += opt + " "
    command = ['sshot']
    command.extend(opts)
    proc = Popen(command, stdin=PIPE, stdout=PIPE, env=my_env)
    exit_code = proc.wait()
    if exit_code == 0:
        return(imgname)
    else:
        return(False)


def add_delay():
    local_launcher_args = {}
    local_launcher_args['mesg'] = "Choose delay, or write custom one."
    local_launcher_args['prompt'] = "sshot (add delay):"
    local_launcher_args['format'] = "s"
    delay, exit = mbrofi.rofi(["5","4","3","2","1","0"], local_launcher_args)
    if exit == 1:
        return(None)
    else:
        return(delay.strip())


# main function that calls rofi with the settings and entries
def main_function(delay):
    ANSWER, EXIT = mbrofi.rofi(list_entries(delay=delay), launcher_args)
    if EXIT == 1:
        return(False, False, False, 1)
    INDEX, FILTER, SEL = ANSWER.strip().split(';')
    return(INDEX, FILTER, SEL, EXIT)


while True:
    if upload:
        launcher_args['prompt'] = PROMPT + "(upload):"
    else:
        launcher_args['prompt'] = PROMPT + "(noupload):"
    INDEX, FILTER, SEL, EXIT = main_function(delay)
    launcher_args['filter'] = FILTER
    launcher_args['index'] = INDEX
    if (EXIT == 0):
        # This is the case where enter is pressed
        sshot(opts=SEL.split(" "), upload=upload)
        break
    elif (EXIT == 1):
        # This is the case where rofi is escaped (should EXIT)
        break
    elif (EXIT == 10):
        tmp_delay = add_delay()
        if tmp_delay is not None:
            delay = tmp_delay
    elif (EXIT == 11):
        # What to do if second binding is pressed
        upload = (not upload)
    elif (EXIT == 12):
        print("Interactive Mode")
        imgname = sshot(opts=SEL.split(" "), upload=upload)
        if imgname:
            mbrofi.run_mbscript('screenshots.py', [imgname])
        break
    else:
        break
