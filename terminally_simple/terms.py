#!/usr/bin/env python

import gi

# Specify versions before import
gi.require_version('Gtk', '3.0')
gi.require_version('Vte', '2.91')

from gi.repository import Gtk
from gi.repository import Vte
from gi.repository import GLib
from os import environ

class TerminalWindow(Gtk.Window):
	"""
	This class defines 2 by 3 window that holds six terminals.
	"""
	
	def __init__(self):
		"""
		Initiate window with six terminals in a 2 by 3 grid.
		"""
		Gtk.Window.__init__(self, title='Terminally Simple')
		
		# Initiate grid, set rows and columns to fill the whole window
		self.grid = Gtk.Grid()
		
		self.grid.set_column_homogeneous(homogeneous=True)
		self.grid.set_row_homogeneous(homogeneous=True)
		
		self.grid.set_column_spacing(spacing=2)
		self.grid.set_row_spacing(spacing=2)
		
		self.add(self.grid)
		#self.maximize()
		#self.set_border_width(2) -> ugly
		
		terminal = self.construct_terminals()
		self.spawn_sync_for_each_terminal(terminal)

		# First row
		self.grid.attach(terminal[0], 0, 0, 1, 1)
		self.grid.attach(terminal[1], 1, 0, 1, 1)
		self.grid.attach(terminal[2], 2, 0, 1, 1)

		# Second row
		self.grid.attach(terminal[3], 0, 1, 1, 1)
		self.grid.attach(terminal[4], 1, 1, 1, 1)
		self.grid.attach(terminal[5], 2, 1, 1, 1)
		
	def construct_terminals(self):
		"""
		Construct six terminals that will be attached to the grid.
		"""
		terminals = {}
		for key in range(6):
			terminals[key] = Vte.Terminal()
		return terminals
		
	def spawn_sync_for_each_terminal(self, terminals):
		"""
		Make a terminal widget same as bash.
		"""
		for terminal in terminals.values():
			terminal.spawn_sync(
				Vte.PtyFlags.DEFAULT,
				environ['HOME'],
				['/bin/bash'],
				[],
				GLib.SpawnFlags.DO_NOT_REAP_CHILD,
				None,
				None,
			)

if __name__ == '__main__':

	win = TerminalWindow()
	win.connect('delete-event', Gtk.main_quit)
	win.show_all()

	Gtk.main()
