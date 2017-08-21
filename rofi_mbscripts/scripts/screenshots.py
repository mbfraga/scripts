#!/bin/env python3

import os
import sys
from subprocess import Popen, PIPE

import mbrofi

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
msg = "Enter to open, " + \
        bindings[0] + " to upload, "  + \
        bindings[1] + " to preview, " + \
        bindings[2] + " to rename, " + \
        bindings[3] + '/' + bindings[4]  + '/' + bindings[5] + \
        " to sort by name/date/size."
prompt = "screenshots:"
answer = ""
sel = ""
filt = ""
index = 0
bindings = bindings
SCREENSHOT_DIRECTORY = os.path.expanduser(screenshot_directory)

if not (os.path.isdir(SCREENSHOT_DIRECTORY)):
    print('Creating ' + SCREENSHOT_DIRECTORY + '...')
    os.makedir(SCREENSHOT_DIRECTORY)

# run correct launcher with prompt and help message
launcher_args = {}
launcher_args['prompt'] = prompt
launcher_args['mesg'] = msg
launcher_args['filter'] = filt
launcher_args['bindings'] = bindings
launcher_args['index'] = index


# upload image and notify via notify-send
def upload(filename):
    from requests import Session, adapters, exceptions
    """Upload image to ptpb.pw and notify via notify-send."""
    filepath = os.path.join(SCREENSHOT_DIRECTORY, filename)
    url = "https://ptpb.pw"
    files = {'c': open(filepath, 'rb')}
    values = {'p':'1', 'sunset':'432000'}

    s = Session()
    a = adapters.HTTPAdapter(max_retries=3)
    s.mount('https://', a)
    try:
        rh = s.get(url)
    except exceptions.RequestException as e:
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
    """Rename screenshot."""
    filepath=os.path.join(SCREENSHOT_DIRECTORY, filename)
    if not os.path.isfile(filepath):
        print("Screenshot " + filepath + " not found...")

    msg2 = "Rename " + filepath + ". Write new name and press enter."
    prompt2 = "screenshots (rename):"
    newsel, ext = filename.split('.')
    command = ['rofi', '-dmenu', '-p', prompt2, '-mesg', msg2, '-format', 'f',
                '-filter', newsel]

    proc = Popen(command, stdout=PIPE)
    ans = proc.stdout.read().decode("utf-8")
    exit_code = proc.wait()

    if ans == '':
        return(False)
    if exit_code == 1:
        return(False)
    if ans.strip():
        newname = ans.strip() + '.' + ext
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


def main_rofi_function(elist):
    """Call main rofi function and return the selection, filter, selection
    index, and exit code. Don't return any of these in case of rofi being 
    escaped.
    """
    answer, exit = mbrofi.rofi(elist, launcher_args)
    if exit == 1:
        return(False, False, False, 1)
    index, filt, sel = answer.strip().split(';')
    return(index, filt, sel, exit)


def main():
    """Main function."""
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
        launcher_args['mesg'] =  msg + " sorted by: " + \
                                sortby + "[" + sortchar + ']'
        index, filter, sel, exit = main_rofi_function(SFR.filenames())
        print("index:", str(index))
        print("filter:", filt)
        print("selection:", sel)
        print("exit:", str(exit))
        print("------------------")

        launcher_args['filter'] = filt
        launcher_args['index'] = index

        if (exit == 0):
            filepath=os.path.join(SCREENSHOT_DIRECTORY, sel)
            # This is the case where enter is pressed
            if os.path.isfile(filepath):
                mbrofi.xdg_open(filepath)
            break
        elif (exit == 1):
            # this is the case where rofi is escaped (should exit)
            break
        elif (exit == 10):
            print('uploading ' + sel)
            pasteurl = upload(sel)
            pasteurl = pasteurl.strip()
            if pasteurl:
                mbrofi.clip(pasteurl)
            break
        elif (exit == 11):
            filepath=os.path.join(SCREENSHOT_DIRECTORY, sel)
            print('Previewing' + filepath)
            if os.path.isfile(filepath):
                mbrofi.xdg_open(filepath)
            SFR.scan_files(recursive=False)
            SFR.sort(sortby, sortrev)
        elif (exit == 12):
            print('renaming ' + sel)
            rename_success = rename_screenshot(sel)
            if rename_success:
                SFR.scan_files(recursive=False)
                SFR.sort(sortby, sortrev)
            else:
                print("meh")
        elif (exit == 13):
            if sortby == "name":
                sortrev = (not sortrev)
            else:
                sortby = "name"
                sortrev = True
            SFR.sort(sortby, sortrev)
        elif (exit == 14):
            if sortby == "cdate":
                sortrev = (not sortrev)
            else:
                sortby = "cdate"
                sortrev = False
            SFR.sort(sortby, sortrev)
        elif (exit == 15):
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
