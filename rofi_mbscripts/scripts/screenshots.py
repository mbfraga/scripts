#!/bin/env python3

import sys
import mbrofi
import os
import requests
from subprocess import Popen, PIPE

# user variables
screenshot_directory='~/Pictures/screenshots/'

# application variables
bindings = ["alt+u"]
bindings += ["alt+p"]
bindings += ["alt+r"]
bindings += ["alt+1"]
bindings += ["alt+2"]
bindings += ["alt+3"]

# launcher variables
MSG = "Enter to open, " + \
        bindings[0] + " to upload, "  + \
        bindings[1] + " to preview, " + \
        bindings[2] + " to rename, " + \
        bindings[3] + '/' + bindings[4]  + '/' + bindings[5] + \
        " to sort by name/date/size."
PROMPT = "screenshots:"
ANSWER = ""
SEL = ""
FILTER = ""
INDEX = 0
BINDINGS = bindings
SCREENSHOT_DIRECTORY = os.path.expanduser(screenshot_directory)

if not (os.path.isdir(SCREENSHOT_DIRECTORY)):
    print('Creating ' + SCREENSHOT_DIRECTORY + '...')
    os.makedir(SCREENSHOT_DIRECTORY)

# run correct launcher with prompt and help message
launcher_args = {}
launcher_args['prompt'] = PROMPT
launcher_args['mesg'] = MSG
launcher_args['filter'] = FILTER
launcher_args['bindings'] = BINDINGS
launcher_args['index'] = INDEX


# upload image and notify via notify-send
def upload(filename):
    filepath = os.path.join(SCREENSHOT_DIRECTORY, filename)
    url = "https://ptpb.pw"
    files = {'c': open(filepath, 'rb')}
    values = {'p':'1', 'sunset':'432000'}

    s = requests.Session()
    a = requests.adapters.HTTPAdapter(max_retries=3)
    s.mount('https://', a)

    try:
        rh = s.get(url)
    except requests.exceptions.RequestException as e:
        print("Error: Failed to connect to " + url)
        mbrofi.notify("Screenshot:", 
                      "Screenshot " + filename + "could not be uploaded."
                        + " Failed to connect to " + url)
        return False

    if not (rh.status_code == 200):
        print("Error: Failed to connect to " + url)
        print(rh.status_code)
        mbrofi.notify("Screenshot:", 
                      "Screenshot " + filename + "could not be uploaded."
                        + " Failed to connect to " + url)
        return False

    r = s.post(url + "/?u=1", files = files, data = values)
    if (r.status_code == 200):
        pasteurl = r.text
        mbrofi.notify("Screenshot:",
                        "Screenshot " + filename + " uploaded to:"
                        + " " + url)
    else:
        mbrofi.notify("Screenshot:",
                        "Screenshot " + filename + "could not be uploaded."
                        + " Status code: " + r.status_code)
        print("Error: Upload was unsuccessful.")
        print(r.status_code)
        return False

    return(pasteurl)

def rename_screenshot(filename):
    filepath=os.path.join(SCREENSHOT_DIRECTORY, filename)
    if not os.path.isfile(filepath):
        print("Screenshot " + filepath + " not found...")

    MSG2 = "Rename " + filepath + ". Write new name and press enter."
    PROMPT2 = "screenshots (rename):"
    NEWSEL, EXT = filename.split('.')
    COMMAND = ['rofi', '-dmenu', '-p', PROMPT2, '-mesg', MSG2, '-format', 'f',
                '-filter', NEWSEL]

    proc = Popen(COMMAND, stdout=PIPE)
    ans = proc.stdout.read().decode("utf-8")
    exit_code = proc.wait()

    if ans == '':
        return(False)
    if exit_code == 1:
        return(False)
    if ans.strip():
        newname = ans.strip() + '.' + EXT
        newpath = os.path.join(SCREENSHOT_DIRECTORY, newname)
        if os.path.isfile(newpath):
            emsg = "file '" + filepath + "' exists, can't rename '" + filename
            emsg += "' to '" + newname + "'."
            print(emsg)
            mbrofi.rofi_warn(emsg)
        else:
            print("   " + filename + " to " + newname + ".")
            os.rename(filepath, newpath)
            return(True)


# main function that calls rofi with the settings and entries
def main_rofi_function(list):
    ANSWER, EXIT = mbrofi.rofi(list, launcher_args)
    if EXIT == 1:
        return(False, False, False, 1)
    INDEX, FILTER, SEL = ANSWER.strip().split(';')
    return(INDEX, FILTER, SEL, EXIT)


def main():
    SFR = mbrofi.FileRepo(dirpath=SCREENSHOT_DIRECTORY)
    SFR.scan_files(recursive=False)
    sortby="cdate"
    sortrev=False
    sortchar=""
    SFR.sort(sortby, sortrev)
    while True:
        if sortrev:
            sortchar = "^"
        else:
            sortchar = "v"
        launcher_args['mesg'] =  MSG + " Sorted by: " + \
                                sortby + "[" + sortchar + ']'
        INDEX, FILTER, SEL, EXIT = main_rofi_function(SFR.filenames())
        print("Index:", str(INDEX))
        print("Filter:", FILTER)
        print("Selection:", SEL)
        print("Exit:", str(EXIT))
        print("------------------")

        launcher_args['filter'] = FILTER
        launcher_args['index'] = INDEX

        if (EXIT == 0):
            filepath=os.path.join(SCREENSHOT_DIRECTORY, SEL)
            # This is the case where enter is pressed
            if os.path.isfile(filepath):
                mbrofi.xdg_open(filepath)
            break
        elif (EXIT == 1):
            # This is the case where rofi is escaped (should EXIT)
            break
        elif (EXIT == 10):
            print('Uploading ' + SEL)
            pasteurl = upload(SEL)
            if pasteurl:
                mbrofi.clip(pasteurl)
            break
        elif (EXIT == 11):
            filepath=os.path.join(SCREENSHOT_DIRECTORY, SEL)
            print('Previewing' + filepath)
            if os.path.isfile(filepath):
                mbrofi.xdg_open(filepath)
            SFR.scan_files(recursive=False)
            SFR.sort(sortby, sortrev)
        elif (EXIT == 12):
            print('Renaming ' + SEL)
            rename_success = rename_screenshot(SEL)
            if rename_success:
                SFR.scan_files(recursive=False)
                SFR.sort(sortby, sortrev)
            else:
                print("meh")
        elif (EXIT == 13):
            if sortby == "name":
                sortrev = (not sortrev)
            else:
                sortby = "name"
                sortrev = True
            SFR.sort(sortby, sortrev)
        elif (EXIT == 14):
            if sortby == "cdate":
                sortrev = (not sortrev)
            else:
                sortby = "cdate"
                sortrev = False
            SFR.sort(sortby, sortrev)
        elif (EXIT == 15):
            if sortby == "size":
                sortrev = (not sortrev)
            else:
                sortby = "size"
                sortrev = True
            SFR.sort(sortby, sortrev)
        else:
            break

if __name__ == "__main__":
    if (len(sys.argv) > 1):
        launcher_args['filter'] = sys.argv[1]
    main()

