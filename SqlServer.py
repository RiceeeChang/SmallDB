# -------------------------------------------
#
# 
#
# -------------------------------------------


from http.server import BaseHTTPRequestHandler, HTTPServer
from socketserver import ThreadingMixIn
import threading
import argparse
import re
import json
import cgi

from SqlYacc import parser

class HTTPRequestHandler(BaseHTTPRequestHandler):
	def do_POST(self):

		ctype, pdict = cgi.parse_header(self.headers.get_all('content-type')[0])
		print(ctype, ', ',pdict)
		if ctype == 'application/x-www-form-urlencoded':
			length = int(self.headers.get_all('content-length')[0])
			data = cgi.parse_qs(self.rfile.read(length), keep_blank_values=1)
			command = data[b'command'][0].decode('utf8')
			print(type(command))

			# do command
			print(('cmd = ', command))
			result = parser.parse(command)
			if result == None:
				result = {'response' : 'Syntax error.'}

			# input json data to 
			self.send_response(200)
			self.send_header('Content-Type', 'application/json')
			self.end_headers()
			self.wfile.write(json.dumps(result, ensure_ascii=False).encode('utf8'))

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