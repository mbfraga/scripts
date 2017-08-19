#!/bin/env python3

import sys
from subprocess import Popen, PIPE
from operator import itemgetter

import mbrofi

# user variables

# application variables
bindings = ["alt+v"]
bindings += ["alt+n"]
bindings += ["alt+a"]

# launcher variables
MSG = "Enter to open in browser. " + \
        bindings[0] + " to switch view, " +  \
        bindings[1]  + " to create new bookmark, " + \
        bindings[2]  + " for actions."
PROMPT = "buku:"
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


class Bookmarks:
    def __init__(self):
        self.__bookmarks = []
        #self.sorttype = "none" ##Trivial to implement, but not worth imo.
        #self.sortrev = False
        self.__bm_count = 0
        self.__tags = []

        # used for line formatting
        self.__lineformat = ['number', 'url', 'tags']
        self.__linebs = {}
        self.__linebs['number'] = 4
        self.__linebs['url'] = 40
        self.__linebs['tags'] = 20

        self.get_bookmarks()

    def get_bookmarks(self):
        proc = Popen(['buku', '-p', '-f', '2'], stdout=PIPE)
        answer = proc.stdout.read().decode('utf-8').strip()
        exit_code = proc.wait()
        if not (exit_code == 0):
            print("Something went wrong with buku. Couldn't get bookmarks")
            sys.exit(1)
        for line in answer.split('\n'):
            temp_entry = line.split()
            if (len(temp_entry) == 2):
                temp_entry.append("NOTAG")
            bookmark = {}
            bookmark['number'] = temp_entry[0]
            bookmark['url'] = temp_entry[1]
            bookmark['tags'] = temp_entry[2]
            for tag in temp_entry[2].split(','):
                if tag not in self.__tags:
                    self.__tags.append(tag)
            self.__bookmarks.append(bookmark)

    def get_tags(self):
        proc = Popen(['buku', '--np', '--st'], stdout=PIPE)
        answer = proc.stdout.read().decode('utf-8').strip()
        exit_code = proc.wait()
        if not (exit_code == 0):
            print("Something went wrong with buku. Couldn't get tags.")
            sys.exit(1)
        for tag in answer.split('\n'):
            self.__tags.append(tag.strip().split()[1])

    def get_property(self, index, prop='url'):
        return(self.__bookmarks[index]['url'])

    def get_property_list(self, prop='url'):
        plist = list(itemgetter(prop)(bm) for bm in self.__bookmarks)
        return(plist)

    def set_lineformat(self, new_lineformat):
        self.__lineformat = new_lineformat

    def lines(self, format_list=None, tag=''):
        lines = []
        if not format_list:
            format_list = self.__lineformat
        for bm in self.__bookmarks:
            if tag not in bm['tags']:
                continue
            line = ''
            for formatn in format_list:
                block = str(bm[formatn])
                blocksize = self.__linebs[formatn]
                if len(block) >= blocksize:
                    block = block[:blocksize-2] + '…'

                block = block.ljust(blocksize)
                line += block
            lines.append(line)
        return(lines)

    def tags(self):
        return(self.__tags)

def list_tags():
    pass

# main function that calls rofi with the settings and entries
def main_function(entries):
    ANSWER, EXIT = mbrofi.rofi(entries, launcher_args)
    if EXIT == 1:
        return(False, False, False, 1)
    INDEX, FILTER, SEL = ANSWER.strip().split(';')
    return(INDEX, FILTER, SEL, EXIT)

bm = Bookmarks()
while True:
    INDEX, FILTER, SEL, EXIT = main_function(bm.lines())
    launcher_args['filter'] = FILTER
    launcher_args['index'] = INDEX
    if (EXIT == 0):
        mbrofi.xdg_open(bm.get_property(int(INDEX), 'url'))
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
    elif (EXIT == 12):
        print(bindings[2] + " was pressed!")

    else:
        break
