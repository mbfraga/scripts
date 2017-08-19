#!/bin/env python3

from subprocess import Popen, PIPE, call
import struct
import os
import sys
from stat import ST_CTIME, ST_ATIME, ST_MTIME, ST_SIZE
from operator import itemgetter


def rofi(entries, launcher_arguments=False, additional_args=[]):

    if not launcher_arguments:
        command_args = ["rofi", "-dmenu", "-sep", "\\0", "-format", "i;f;s"]
    else:
        command_args = ["rofi", "-dmenu", "-sep", "\\0"]
        if 'prompt' in launcher_arguments:
            command_args += ["-p", launcher_arguments['prompt']]
        if 'mesg' in launcher_arguments:
            if launcher_arguments['mesg']:
                command_args += ["-mesg", launcher_arguments['mesg']]
        if 'filter' in launcher_arguments:
            command_args += ["-filter", launcher_arguments['filter']]
        if 'index' in launcher_arguments:
            command_args += ["-selected-row", str(launcher_arguments['index'])]
        if 'format' in launcher_arguments:
            command_args += ["-format", launcher_arguments['format']]
        else:
            command_args += ["-format", "i;f;s"]
        if 'bindings' in launcher_arguments:
            kb_ct = 1
            for bind in launcher_arguments['bindings']:
                keyentry = "-kb-custom-" + str(kb_ct)
                command_args += [keyentry, bind]
                kb_ct += 1

    proc = Popen(command_args + additional_args, stdin=PIPE, stdout=PIPE)
    for e in entries:
        proc.stdin.write((e).encode('utf-8'))
        proc.stdin.write(struct.pack('B', 0))
    proc.stdin.close()
    answer = proc.stdout.read().decode('utf-8')
    exit_code = proc.wait()

    if (answer == ''):
        return(None, exit_code)

    return(answer, exit_code)


def rofi_warn(message):

    Popen(['rofi', '-e', message])

def notify(title, message, duration=4000):

    Popen(['notify-send', '-t', str(duration), title,  message])


def clip(clipstring):


    proc = Popen(['xclip', '-i', '-selection', 'primary'], stdin=PIPE)
    proc.stdin.write((clipstring.encode('utf-8')))
    proc.stdin.close()
    proc.wait()

    proc = Popen(['xclip', '-i', '-selection', 'clipboard'], stdin=PIPE)
    proc.stdin.write((clipstring.encode('utf-8')))
    proc.stdin.close()
    proc.wait()


def xdg_open(application, wait=True):

    proc = Popen(['xdg-open', application], stdout=PIPE)
    if wait:
        proc.communicate()


def run_mbscript(scriptpath, arguments=[]):

    if not os.path.isfile(scriptpath):
        print("Script '" + scriptpath + "' not found...")
        sys.exit(1)

    proc = Popen(['python3 ' + scriptpath] + arguments, shell=True)
    proc.communicate()



# Get mime type using bash (python libraries have been unreliable)
def get_mime_type(filepath):

    proc = Popen(['xdg-mime', 'query', 'filetype', filepath], stdout=PIPE)
    mtype = proc.stdout.read().decode('utf-8')
    exit_code = proc.wait()

    if (exit_code != 0):
        sys.exit(1)

    if not mtype:
        mtype = 'None/None'

    return(mtype)


class FileRepo:
    def __init__(self, dirpath=None):
        self.__path = os.path.join(dirpath, "")
        self.__path_len = len(self.__path)
        self.__file_list = []    # list of files - dicts
        self.sorttype = "none"
        self.sortrev = False

        self.__filecount = 0

        self.__tags = None

        self.__lineformat = ['name', 'cdate']
        self.__linebs = {}
        self.__linebs['name'] = 40
        self.__linebs['adate'] = 18
        self.__linebs['cdate'] = 18
        self.__linebs['mdate'] = 18
        self.__linebs['size'] = 15
        self.__linebs['misc'] = 100
        self.__linebs['tags'] = 50


    # Scans the directory for files and populates the file list and linebs
    def scan_files(self, recursive=True):
        self.__filecount = 0
        self.__file_list = []

        if recursive:
            for root, dirs, files in os.walk(self.__path, topdown=True):
                for name in files:
                    fp = os.path.join(root, name)
                    fp_rel = fp[self.__path_len:]

                    if (fp_rel[0] == '.'):
                        continue
                    try:
                        stat = os.stat(fp)
                    except:
                        continue

                    file_props = {}
                    file_props['size'] = stat[ST_SIZE]
                    file_props['adate'] = stat[ST_ATIME]
                    file_props['mdate'] = stat[ST_MTIME]
                    file_props['cdate'] = stat[ST_CTIME]
                    file_props['name'] = fp_rel
                    file_props['fullpath'] = fp
                    file_props['misc'] = None
                    file_props['tags'] = None

                    self.__file_list.append(file_props)
                    self.__filecount += 1
        else:
            for f in os.scandir(self.__path):

                fp_rel = f.name
                fp = os.path.join(self.__path, fp_rel)
                if (fp_rel[0] == '.'):
                    continue
                if f.is_dir():
                    continue
                #try:
                #    stat = os.stat(fp)
                #except:
                #    continue

                file_props = {}
                file_props['size'] = f.stat()[ST_SIZE]
                file_props['adate'] = f.stat()[ST_ATIME]
                file_props['mdate'] = f.stat()[ST_MTIME]
                file_props['cdate'] = f.stat()[ST_CTIME]
                file_props['name'] = fp_rel
                file_props['fullpath'] = fp
                file_props['misc'] = None
                file_props['tags'] = None

                self.__file_list.append(file_props)
                self.__filecount += 1


    def add_file(self, filepath, misc_prop=None):
        if not os.path.isfile(filepath):
            print(filepath + " is not a file.")
            return

        fp_rel = filepath[self.__path_len:]

        try:
            stat = os.stat(filepath)
        except:
            return

        file_props = {}
        file_props['size'] = stat[ST_SIZE]
        file_props['adate'] = stat[ST_ATIME]
        file_props['mdate'] = stat[ST_MTIME]
        file_props['cdate'] = stat[ST_CTIME]
        file_props['name'] = fp_rel
        file_props['fullpath'] = filepath
        file_props['misc'] = misc_prop

        self.__file_list.append(file_props)
        self.__filecount += 1


    def sort(self, sortby='name', sortrev=False):
        if sortby not in ['size', 'adate', 'mdate', 'cdate', 'name']:
            print("Key '" + sortby + "' is not valid.")
            print("Choose between size, adate, mdate, cdate or name.")

        self.__file_list = sorted(self.__file_list, 
                            key=itemgetter(sortby), reverse=not sortrev)
        self.sorttype=sortby
        self.sortrev=sortrev

    def get_property_list(self, prop='name'):
        plist = list(itemgetter(prop)(filen) for filen in self.__file_list)
        return(plist)

    def filenames(self):
        return(self.get_property_list('name'))

    def filepaths(self):
        return(self.get_property_list('fullpath'))

    def filecount(self, include_normal=True):
        return(self.__filecount + self.__pfilecount)
        
    def set_lineformat(self, new_lineformat):
        self.__lineformat = new_lineformat

    def lines(self, format_list=None):
        lines = []
        if not format_list:
            format_list = self.__lineformat
        for filen in self.__file_list:
            line = ""
            for formatn in format_list:
                if formatn in ['adate', 'mdate', 'cdate']:
                    block = datetime.utcfromtimestamp(filen[formatn])
                    block = block.strftime('%d/%m/%Y %H:%M')
                elif formatn == 'size':
                    size=filen[formatn]
                    block = sizeof_fmt(size)
                else:
                    block = str(filen[formatn])

                blocksize = self.__linebs[formatn]
                if len(block) >= blocksize:
                    block = block[:blocksize-2] + '…'

                block = block.ljust(blocksize)
                line += block

            lines.append(line)

        return(lines)


    def grep_files(self, filters_string):
        if not self.__file_list:
            print("No files added to file repo")
            return(1)

        proc = Popen(['grep', '-i', '-I', filters_string] + self.filepaths() 
                     , stdout=PIPE)
        answer = proc.stdout.read().decode('utf-8')
        exit_code = proc.wait()

        grep_file_repo = FileRepo(self.__path)
        temp_files = []
        if answer == '':
            return(None)

        for ans in answer.split("\n"):
            if ans:
                ans = ans.split(':', 1)
                if not ans[0] in temp_files:
                    grep_file_repo.add_file(ans[0], ans[1])
                    temp_files.append(ans[0])

        return(grep_file_repo)


