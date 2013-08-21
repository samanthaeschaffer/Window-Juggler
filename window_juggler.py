#!/usr/bin/env python
from gi.repository import Gtk, Wnck
import subprocess
import sys
import glib

#handler for new windows created during script execution
def on_new_window(screen, window):
	screen.change_workspace_count(screen.get_workspace_count()+1)
	workspaces = screen.get_workspaces()
	window.move_to_workspace(workspaces[screen.get_workspace_count()-1])
	window.maximize()

#function for timeout
def execute(command):
	process = subprocess.Popen(command.split())
	return False

#called after all windows -should- have launched and been arranged
def quit(screen):
	screen.change_workspace_count(screen.get_workspace_count()-1)
	screen.force_update()
	Gtk.main_quit()
	return False

#main
def main():
	while Gtk.events_pending():
		Gtk.main_iteration()

	screen = Wnck.Screen.get_default()
	screen.force_update()
	screen.connect("window-opened", on_new_window)
	screen.change_workspace_count(2)

	config_file = open(sys.argv[1], 'r')

	for line in config_file:
		glib.timeout_add(5000, execute, line)

	glib.timeout_add(8000, quit, screen)

	Gtk.main()

if __name__ == "__main__":
	main()
