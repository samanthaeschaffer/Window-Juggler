#!/usr/bin/env python
import sys
import gtk
import subprocess
import time

#function to get list of windows from wmctrl
def get_windows():
    wmctrl_process = subprocess.Popen('wmctrl -l', stdout=subprocess.PIPE, shell=True)
    wmctrl_output = wmctrl_process.communicate()
    return wmctrl_output[0].split("\n")

#function to get id of most recently launched window
def move_to_workspace(workspace):
    list_of_windows = get_windows()

    number_of_windows = len(list_of_windows)
    if number_of_windows > 0:
        most_recent_window = list_of_windows[number_of_windows-2].split()
        if most_recent_window[1] >=0:
            move_process = subprocess.Popen(['wmctrl', '-i', '-r', str(most_recent_window[0]), '-t', str(workspace)])

#function to move all windows to specific workspace
def move_all_to_workspace(workspace):
    while gtk.events_pending():
        gtk.main_iteration()

    list_of_windows = get_windows()
    number_of_windows = len(list_of_windows)

    for w in range(0, number_of_windows-1):
        current_window = list_of_windows[w].split()

        if int(current_window[1]) >= 0:
            move_process = subprocess.Popen(['wmctrl', '-i', '-r', current_window[0], '-t', workspace])

#function to execute line from file
def execute_command(command):
    subprocess.Popen(command.split())
    time.sleep(1)

#MAIN
if len(sys.argv) < 2:
    sys.exit("No file named specified")

config_file = open(sys.argv[1], 'r')
workspace = -1

for line in config_file:
    if workspace >= 0:
        print line
        execute_command(line)
        move_to_workspace(workspace)
    else:
        wmctrl_process = subprocess.Popen(['wmctrl', '-n', line])
        move_all_to_workspace(line)
    workspace += 1
