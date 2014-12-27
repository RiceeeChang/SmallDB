# -------------------------------------------
#
# 
#
# -------------------------------------------


from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from SocketServer import ThreadingMixIn
import threading
import argparse
import re
import cgi

import SqlYacc.yacc as yacc

parser = yacc.yacc()


class HTTPRequestHandler(BaseHTTPRequestHandler):
	def do_POST(self):
		ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
			
		print(ctype)
		if ctype == 'application/x-www-form-urlencoded':
			length = int(self.headers.getheader('content-length'))
			data = cgi.parse_qs(self.rfile.read(length), keep_blank_values=1)
			command = data['command'][0]
			
			# input json data to 
			print('cmd = ', command)
			self.send_response(200)
			self.send_header('Content-Type', 'application/json')
			self.end_headers()
			self.wfile.write({'response': 'ok'})

		else:
			self.send_response(403)
			self.send_header('Content-Type', 'application/json')
			self.end_headers()

		return

	def do_GET(self):

		return

class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
	allow_reuse_address = True

	def shutdown(self):
		self.socket.close()
		HTTPServer.shutdown(self)

class SimpleHttpServer():
	def __init__(self, ip, port):
		self.server = ThreadedHTTPServer((ip, port), HTTPRequestHandler)

	def start(self):
		self.server_thread = threading.Thread(target=self.server.serve_forever)
		self.server_thread.daemon = True
		self.server_thread.start()

	def waitForThread(self):
		self.server_thread.join()

	def addRecord(self, recordID, jsonEncodedRecord):
		LocalData.records[recordID] = jsonEncodedRecord

	def stop(self):
		self.server.shutdown()
		self.waitForThread()

if __name__ == '__main__':
	#parser = argparse.ArgumentParser(description='HTTP Server')
	#parser.add_argument('port', type=int, help='Listening port for HTTP Server')
	#parser.add_argument('ip', help='HTTP Server IP')
	#args = parser.parse_args()

	server = SimpleHttpServer('127.0.0.1', 5566)
	print('HTPP Server Running..........')
	server.start()
	server.waitForThread()