import logging
import socket
import os
import globals

try:
	from jeedom.jeedom import *
except ImportError:
	print "Error: importing module jeedom.jeedom"
	sys.exit(1)

def shutdown_server():
	func = request.environ.get('werkzeug.server.shutdown')
	if func is None:
		raise RuntimeError('Not running with the Werkzeug Server')
	func()

def check_start_server():
	if globals.device is None or len(globals.device) == 0:
		logging.error('Dongle Key is not specified. Please check your Z-Wave (openzwave) configuration plugin page')
		sys.exit(1)

	logging.info("Check if the port REST server available")
	_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	port_available = _sock.connect_ex(('127.0.0.1', int(globals.port_server)))
	if port_available == 0:
		logging.error('The port %s is already in use. Please check your Z-Wave (openzwave) configuration plugin page' % (
		globals.port_server,), 'error')
		sys.exit(1)
	logging.info("--> pass")

	logging.info("Check OpenZWave Devices Database")
	if not os.path.isfile(globals.config_folder + "/manufacturer_specific.xml"):
		logging.debug(globals.config_folder + "/manufacturer_specific.xml")
		logging.error('OpenZWave Devices Database is not found. Please execute Devices Configuration update, from Plugin Configuration page')
		sys.exit(1)
	logging.info("--> pass")

	if globals.device == 'auto':
		for stick in globals.know_sticks:
			globals.device = jeedom_utils.find_tty_usb(stick['idVendor'], stick['idProduct'])
			if globals.device is not None:
				logging.info('USB Z-Wave Stick found : ' + stick['name'] + ' at ' + globals.device)
				break
		if globals.device is None:
			logging.error('No USB Z-Wave Stick detected')
			sys.exit(1)

def set_log_level():
	jeedom_utils.set_log_level(globals.log_level)

def init_jeedom_com():
	globals.jeedom_com = jeedom_com(apikey=globals.apikey, url=globals.callback, cycle=globals.cycle)

def write_pid():
	jeedom_utils.write_pid(str(globals.pidfile))