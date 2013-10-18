#!/usr/bin/env python
from gi.repository import Gtk, Wnck
import subprocess
import sys
import glib

#handler for new windows created during script execution
def on_new_window(screen, window):
	if not window.is_pinned():
		workspaces = screen.get_workspaces()
		window.move_to_workspace(workspaces[screen.get_workspace_count()-1])
	        screen.change_workspace_count(screen.get_workspace_count()+1)
		screen.force_update()
		window.maximize()
		Gtk.main_quit()

#function to execute command
def execute(command):
	process = subprocess.Popen(command.split())
	return False

#main
def main():
	while Gtk.events_pending():
		Gtk.main_iteration()

	screen = Wnck.Screen.get_default()
	screen.force_update()
	screen.connect("window-opened", on_new_window)
	screen.change_workspace_count(1)
	screen.force_update()

	config_file = open(sys.argv[1], 'r')

	for line in config_file:
		glib.timeout_add(1000, execute, line)
		Gtk.main()

	Wnck.shutdown()
	screen.force_update()

if __name__ == "__main__":
	main()
