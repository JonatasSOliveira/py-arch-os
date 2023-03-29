import os
import curses
import pyarch
import pycmds
import pycfg
import pymsgs
import pykmsgs
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
			self.delete_last_char()
			return
		elif (key == curses.KEY_ENTER) or (key == ord('\n')):
			self.verify_command()
			self.clean_console()
			return

	def handle_interrupt (self, interrupt):
		if interrupt == pycfg.INTERRUPT_KEYBOARD:
			self.interrupt_keyboard()
			return
		if interrupt == pycfg.INTERRUPT_MEMORY_PROTECTION_FAULT:
			self.printk(pykmsgs.INTERRUPT_MEMORY_PROTECTION_FAULT_NOT_IMPLEMENT)
			return
		if interrupt == pycfg.INTERRUPT_TIMER:
			self.printk(pykmsgs.INTERRUPT_TIMER_NOT_IMPLEMENT)
			return

		return

	def syscall (self):
		#self.terminal.app_print(msg)		
		return

	# NOTE: custom functions
	def clean_console(self):
		self.console_str = ''
		console_message = ''
		self.terminal.console_print(console_message)

	def delete_last_char(self):
		self.console_str = self.console_str[0:-1]
		self.terminal.console_print('\r')
		self.terminal.console_print(self.console_str)

	def exit_terminal(self):
		self.terminal.end()		
		self.cpu.cpu_alive = False

	def cmd_not_found_handler(self):
		self.terminal.console_print('\n' + self.console_str + ':' + pymsgs.COMMAND_NOT_FOUND + '\n\n')		

	def load_process(self):
		process_name = self.console_str[len(pycmds.LOAD_PROCESS) + 1:].strip()		

		if process_name:
			console_message = '\n' + process_name + ':' + pymsgs.PROCESS_LOADED + '\n\n'
		else:
			console_message = '\n' + pycmds.LOAD_PROCESS + ' ' + pymsgs.REQUIRE_PROCESS_NAME + '\n\n'		

	def verify_command(self):
		self.printk(pykmsgs.EXEC_FUNCTION + 'verify_comand')
		if self.console_str == pycmds.EXIT_TERMINAL:
			self.exit_terminal()
			return
		if self.console_str == pycmds.LOAD_PROCESS or self.console_str.startswith(pycmds.LOAD_PROCESS + ' '):
			self.load_process()
			return

		self.cmd_not_found_handler()		
