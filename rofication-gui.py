#!/usr/bin/env python3
import sys
import re
import struct
import subprocess
import json

msg = "<span><i>Alt-h</i>:\tShow Help.</span>"
rofi_command = [ 'rofi' , '-dmenu', '-p', 'Notifications:', '-markup', '-mesg', msg]

def strip_tags(value):
  "Return the given HTML with all tags stripped."
  return re.sub(r'<[^>]*?>', '', value)

def rofi_message(message):
    proc = subprocess.Popen(['rofi', '-e', message])

def call_rofi(notifications, additional_args=[]):
    additional_args.extend([
        '-kb-custom-1', 'Alt+r',
        '-kb-custom-2', 'Alt-d',
        '-kb-custom-3', 'Alt-Shift-d',
        '-kb-custom-4', 'Alt+c',
        '-kb-custom-5', 'Alt+h',
        '-kb-custom-6', 'Alt+y',
        '-kb-custom-7', 'Alt+o',
        '-markup-rows',
        '-sep', '\\0',
        '-format', 'i',
        '-columns', '1',
        '-lines', '6',
        '-eh', '2'
        ])
    proc = subprocess.Popen(rofi_command+ additional_args,
                            stdin=subprocess.PIPE,
                            stdout=subprocess.PIPE)
    for n in notifications:
        proc.stdin.write((n['entry']).encode('utf-8'))
        proc.stdin.write(struct.pack('B', 0))
    proc.stdin.close()
    answer = proc.stdout.read().decode("utf-8")
    exit_code = proc.wait()
    # trim whitespace
    if answer == '':
        return None,exit_code
    else:
        return int(answer),exit_code

def show_help():
    msg = "<i>Alt+h</i>:\t To go back to rofication."
    help_list=[]
    help_list.append("Enter/alt-d:\tDismiss notification")
    help_list.append("Alt+r:\t\tReload")
    help_list.append("Alt+Shift+d:\tDelete application notification")
    help_list.append("Alt+c:\t\tClear Notifications")
    help_list.append("Alt+y:\t\tSend notification to clipboard.")
    help_list.append("Alt+o:\t\tOpen url in notifiation (naive).")
    print(help_list)

    additional_args = [msg]
    additional_args.extend([
        '-kb-custom-1', 'Alt+h',
        '-markup-rows',
        '-sep', '\\0',
        '-columns', '1',
        '-lines', '6',
        '-eh', '1'
        ])
    proc = subprocess.Popen(rofi_command+ additional_args,
                            stdin=subprocess.PIPE,
                            stdout=subprocess.PIPE)
    for h in help_list:
        proc.stdin.write((h).encode('utf-8'))
        proc.stdin.write(struct.pack('B', 0))
    proc.stdin.close()
    answer = proc.stdout.read().decode("utf-8")
    exit_code = proc.wait()
    # trim whitespace
    if answer == '':
        return False
    else:
        return True


def yank_message(notification):

    message = notification['message']
    yank_primary_command = ['xclip', '-i', '-selection', 'primary']
    yank_clipboard_command = ['xclip', '-i', '-selection', 'clipboard']
    proc1 = subprocess.Popen(yank_primary_command,
                            stdin=subprocess.PIPE,
                            stdout=subprocess.PIPE)

    proc1.stdin.write((message).encode('utf-8'))
    proc1.stdin.close()
    exit_code1=proc1.wait()
    proc2 = subprocess.Popen(yank_clipboard_command,
                            stdin=subprocess.PIPE,
                            stdout=subprocess.PIPE)

    proc2.stdin.write((message).encode('utf-8'))
    proc2.stdin.close()
    exit_code2=proc2.wait()


def open_url(notification):
    message = notification['message']
    if not message:
        return
    url=message
    open_url_command = ['firefox', '-new-tab', url]
    proc = subprocess.Popen(open_url_command, stdout=subprocess.PIPE)
    exit_code = proc.wait()

    if exit_code != 1:
        rofi_message("Error: could not open : `" + message + "'")


def notifications_write(notifications):
    print("DEBUG", len(notifications))
    new_file = open("/tmp/rofi_notification_daemon", 'w')
    for n in notifications:
        new_file.write(json.dumps(n)+'\n')
    new_file.close()

def notification_remove_add(notifications, app):
    file = open("/tmp/rofi_notification_daemon", 'r')
    new_file = open("/tmp/rofi_notification_daemon.tmp", 'w')
    for l in file:
        if id != 0:
            new_file.write(l+'\n')
        id -= 1
    new_file.close()

did = None
while True:
    file = open("/tmp/rofi_notification_daemon", 'r')
    notifications=[]
    urgent=[]
    low=[]
    for l in file:
        n = json.loads(l)
        n['entry'] = (
            "<b>{title}</b> <small>({client})</small>\n<i>{message}</i>".format(
                title   = (strip_tags(n.get('title'))),
                client  = (strip_tags(n.get('client'))),
                message = (strip_tags(n.get('message').replace("\n"," ")))
            )
        )
        if n.get('urgency') == 2:
            urgent.append(str(len(notifications)))
        elif n.get('urgency') == 0:
            low.append(str(len(notifications)))
        notifications.append(n)

    file.close()

    args=[]

    if len(urgent):
        args.append("-u")
        args.append(",".join(urgent))
    #if len(low):
    #    args.append("-a")
    #    args.append(",".join(low))

    # Select previous selected row.
    if did != None:
        args.append("-selected-row")
        args.append(str(did))

    # Show rofi
    did,code = call_rofi(notifications,args)
    print("{a},{b}".format(a=did,b=code))

    if did == None:
        break
    if code == 10: # Reload
        continue
    elif code == 11: # Remove
        print(len(notifications))
        notifications.pop(did)
        notifications_write(notifications)
    elif code == 12: # Remove app
        client = notifications[did]['client']
        new_notifications = []
        for n in notifications:
            if n['client'] != client:
                new_notifications.append(n)
        notifications = new_notifications
    elif code == 13: #Clear Notifications
        notifications_write([])
    elif code == 14:
        if not show_help():
            break
    elif code == 15:
        yank_message(notifications[did])
        break
    elif code == 16:
        open_url(notifications[did])
        break
    else:
        break
