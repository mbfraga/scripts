#!/bin/env python3

import sys
from subprocess import Popen, PIPE
from operator import itemgetter

import mbrofi

# user variables

# application variables
bindings = ["alt+t"]
bindings += ["alt+n"]
bindings += ["alt+d"]
bindings += ["alt+a"]

# launcher variables
msg = "Enter to open in browser. " + \
        bindings[0] + " to filter by tags, " +  \
        bindings[1]  + " to create new bookmark, " + \
        bindings[2]  + " to remove bookmark, " + \
        bindings[3]  + " for actions."
prompt = "buku:"
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


class Bookmarks:
    def __init__(self):
        self.__bookmarks = []
        #self.sorttype = "none" ##Trivial to implement, but not worth imo.
        #self.sortrev = False
        self.__bm_count = 0
        self.__tags = []

        # used for line formatting
        self.__lineformat = ['number', 'url', 'ftags']
        self.__linebs = {}
        self.__linebs['number'] = 4
        self.__linebs['url'] = 40
        self.__linebs['tags'] = 20
        self.__linebs['ftags'] = 20

        self.get_bookmarks()

    def get_bookmarks(self):
        self.__bookmarks = []
        self.__tags = []
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
            bookmark['ftags'] = temp_entry[2]
            tags = temp_entry[2].split(',')
            bookmark['tags'] = tags
            for tag in tags:
                if (tag not in self.__tags) and (tag != "NOTAG"):
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
            if (tag) and (tag not in bm['tags']):
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

    def bookmarks(self):
        return(self.__bookmarks)

def add_bookmark(rofi_abort_key, tags_list=[]):
    url_msg = "Use url from clipboard below, or enter manually. Press '"
    url_msg += rofi_abort_key + "' to abort."
    url_prompt = "buku add:"
    url_opts = mbrofi.get_clip().strip().split('\n')
    url,uexit = mbrofi.rofi_enter(url_msg, prompt=url_prompt, options=url_opts
                            ,bindings=[rofi_abort_key])
    if url is None or uexit == 1:
        return(False)

    tag = edit_tags(rofi_abort_key, tags_list, url)

    proc = Popen(['buku', '-a', url, tag], stdout=PIPE)
    exit = proc.wait()

    if exit == 0:
        return(True)
    else:
        return(False)


def rm_bookmark(abort_key, bm):
    rm_msg = "Are you sure you want to delete this bookmark? Press '"
    rm_msg += abort_key + "' to abort. Bookmark: " + bm['url']
    rm_prompt = "buku remove:"
    rs = mbrofi.rofi_ask(rm_msg, prompt=rm_prompt, abort_key=abort_key)
    if not rs:
        return(False)
    command = ['buku', '-d', bm['number']]
    proc = Popen(command, stdout=PIPE)
    exit = proc.wait()
    if exit == 0:
        return(True)
    else:
        return(False)

def filter_bookmarks(abort_key, tags_list):
    fb_msg = "Select a tag with which to filter bookmarks. '"
    fb_msg += abort_key + " to abort."
    fb_prompt = "buku filter:"
    fb, fexit = mbrofi.rofi_enter(fb_msg, prompt=fb_prompt, options=tags_list
                           , bindings = [abort_key])
    if fexit == 1: 
        sys.exit(0)
    elif (fexit == 10) or (not fb.strip()) or fb not in tags_list:
        return(False)
    else:
        return(fb)

def edit_tags(abort_key, tags_list, bm_url, bm_tags=[]):
    binds = [abort_key, 'alt-i', 'alt-r']
    tag_msg = "Add some tags for '" + bm_url + "'."
    tag_msg += " Press 'Enter' to apply selection,"
    tag_msg += " 'Alt-Enter' to apply filter,"
    tag_msg += " '" + binds[1] + "' to append,"
    tag_msg += " '" + binds[2] + "' to remove,"
    tag_msg += " '" + binds[0] + "' to abort."
    tag_prompt = "buku edit tag:"
    tags = []
    seltags = []
    for tt in tags_list:
        if tt in bm_tags:
            seltags.append(tt)
        else:
            tags.append(tt)
    while True:
        mtag = ""
        for st in seltags:
            mtag += st + ","
        if mtag:
            opts = [mtag]
        else:
            opts = []
        for tag in tags:
            opts.append(mtag + tag)

        tag, texit = mbrofi.rofi_enter(tag_msg, prompt=tag_prompt
                                 , options=opts, bindings=binds, dfilter=mtag)
        if tag is not None:
            tmptags = tag.split(',')
            ctag = tmptags[-1]
        else:
            ctag = None
        if texit == 12:
            if (not ctag) or (ctag not in tags_list):
                continue
            if ctag not in seltags:
                seltags.append(ctag)
                tags.remove(ctag)
        elif texit == 13:
            if seltags:
                ctag = seltags[-1]
                tags.append(ctag)
                seltags.pop(-1)
        elif texit == 0:
            if (not ctag) or (ctag not in tags_list):
                break
            if ctag not in seltags:
                seltags.append(ctag)
                tags.remove(ctag)
            break
        elif texit == 10:
            break

        else:
            return(False)
    if tag is None:
        tag = ''
    return(tag)

def update_tag(bm, newtags):
    command = ['buku', '-u', bm['number'], '--tag', newtags]
    proc = Popen(command, stdout=PIPE)
    exit = proc.wait()
    if exit == 1:
        return(False)
    else:
        return(True)

def edit_url(abort_key, bm):
    url_msg = "Edit url. 'Alt-Enter' to force apply selection, '"
    url_msg += abort_key + "' to abort."
    url_prompt = "buku edit url:"
    url_filter = bm['url']
    url_opts = [bm['url']]
    url,uexit = mbrofi.rofi_enter(url_msg, prompt=url_prompt, options=url_opts
                            ,bindings=[abort_key], dfilter=url_filter)
    if url is None or uexit == 1:
        return(False)
    else:
        command = ['buku', '-u', bm['number'], '--url', url]
        proc = Popen(command, stdout=PIPE)
        exit = proc.wait()
        if exit == 1:
            return(False)
        else:
            return(True)

def action_menu(abort_key, bm, tags_list):
    am_args = {}
    am_args['mesg'] = "Select an action. '" + abort_key + "' to abort."
    am_args['mesg'] += " Bookmark: (" + bm['number'] + ") " + bm['url']
    am_args['prompt'] = "buku action:"
    am_args['format'] = 'i'
    am_args['bindings'] = [abort_key]
    entries = ['edit url: ' + bm['url'], 'edit tags: ' + bm['ftags']]
    am_ans, am_exit = mbrofi.rofi(entries, am_args)
    if am_exit == 1:
        return(False)
    elif am_exit == 10:
        return(False)
    elif am_exit == 0:
        if am_ans == "1":
            nt = edit_tags(abort_key, tags_list, bm['url'], bm['tags'])
            if nt:
                us = update_tag(bm, nt)
                if us:
                    return(True)
                else:
                    return(False)
            else:
                return(False)
        elif am_ans == "0":
            eu = edit_url(abort_key, bm)
            if eu:
                return(True)
            else:
                return(False)
        else:
            return(False)
    else:
        return(False)


def main_rofi_function(launcher_args, entries):
    """Call main rofi function and return the selection, filter, selection
    index, and exit code. Don't return any of these in case of rofi being 
    escaped.
    """
    answer, exit = mbrofi.rofi(entries, launcher_args)
    if exit == 1:
        return(False, False, False, 1)
    index, filt, sel = answer.strip().split(';')
    return(index, filt, sel, exit)

def main(launcher_args):
    """Main function."""
    bms = Bookmarks()
    ftag = ""
    while True:
        index, filt, sel, exit = main_rofi_function(launcher_args
                                                      , bms.lines(tag=ftag))
        launcher_args['filter'] = filt
        launcher_args['index'] = index
        if (exit == 0):
            num = int(sel.split()[0]) - 1
            print(bms.bookmarks()[num])
            mbrofi.xdg_open(bms.get_property(num, 'url'))
            break
        elif (exit == 1):
            # this is the case where rofi is escaped (should exit)
            break
        elif (exit == 10):
            # what to do if first bindings is pressed
            # remove if nothing should be done
            if ftag:
                ftag = ""
            else:
                fb = filter_bookmarks(launcher_args['bindings'][0], bms.tags())
                if fb:
                    ftag = fb
        elif (exit == 11):
            # what to do if second binding is pressed
            ss = add_bookmark(launcher_args['bindings'][1], bms.tags())
            if ss:
                bms.get_bookmarks()
        elif (exit == 12):
            num = int(sel.split()[0]) - 1
            rs = rm_bookmark(launcher_args['bindings'][2]
                             , bms.bookmarks()[int(num)])
            if rs:
                bms.get_bookmarks()
        elif (exit == 13):
            num = int(sel.split()[0]) - 1
            book = bms.bookmarks()[num]
            am = action_menu(launcher_args['bindings'][3], book, bms.tags())
            if am:
                bms.get_bookmarks()


        else:
            break

if __name__ == "__main__":
    main(launcher_args)
