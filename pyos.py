import os
import curses
import pyarch
import pycmds
from pyarch import load_binary_into_memory
from pyarch import cpu_t

class os_t:
	def __init__ (self, cpu, memory, terminal):
		self.cpu = cpu
		self.memory = memory
		self.terminal = terminal

		self.terminal.enable_curses()

		self.console_str = ""
		self.terminal.console_print("this is the console, type the commands here\n")

	def printk(self, msg):
		self.terminal.kernel_print("kernel: " + msg + "\n")

	def panic (self, msg):
		self.terminal.end()
		self.terminal.dprint("kernel panic: " + msg)
		self.cpu.cpu_alive = False
		#cpu.cpu_alive = False

	def interrupt_keyboard (self):
		key = self.terminal.get_key_buffer()
		is_common_key = (
			(key >= ord('a')) and (key <= ord('z'))) \
			or ((key >= ord('A')) and (key <= ord('Z'))) \
			or ((key >= ord('0')) and (key <= ord('9'))) \
			or (key == ord(' ')) \
			or (key == ord('-')) \
			or (key == ord('_')) \
			or (key == ord('.') \
		)

		if is_common_key:
			strchar = chr(key)
			self.console_str += strchar
			self.terminal.console_print(strchar)
		elif key == curses.KEY_BACKSPACE:
			return
		elif (key == curses.KEY_ENTER) or (key == ord('\n')):
			self.verify_comand()
			return

	def handle_interrupt (self, interrupt):
		if interrupt == pyarch.INTERRUPT_KEYBOARD:
			self.interrupt_keyboard()
			return
		return

	def syscall (self):
		#self.terminal.app_print(msg)		
		return

	# NOTE: custom functions
	def exit_terminal(self):
		self.terminal.end()		
		self.cpu.cpu_alive = False

	def verify_comand(self):
		self.printk(self.console_str)
		if self.console_str == pycmds.EXIT_CMD:
			self.exit_terminal()
			return



		
