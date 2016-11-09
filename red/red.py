#!/usr/bin/python

# @file red.py
# @author cherezov.pavel@gmail.com

import os
import sys
import shutil
import mimetypes

py3 = sys.version_info[0] == 3
if py3:
   from urllib.request import urlopen
   from http.server import HTTPServer
   from http.server import BaseHTTPRequestHandler
else:
   from urllib2 import urlopen
   from BaseHTTPServer import BaseHTTPRequestHandler
   from BaseHTTPServer import HTTPServer

# Change log:
#   0.1 initial version
#   0.2 py3 support added

__version__ = '0.2'

class DownloadProxy(BaseHTTPRequestHandler):
   running = False
   forever = False

   def log_message(self, format, *args):
      pass

   def log_request(self, code='-', size='-'):
      pass

   def response_success(self):
      url = self.path[1:] # replace '/'

      if os.path.exists(url):
         f = open(url)
         content_type = mimetypes.guess_type(url)[0]
      else:
         f = urlopen(url=url)

         if py3:
            content_type = f.getheader("Content-Type")
         else:
            content_type = f.info().getheaders("Content-Type")[0]

      self.send_response(200, "ok")
      self.send_header('Access-Control-Allow-Origin', '*')
      self.send_header('Access-Control-Allow-Methods', 'GET, OPTIONS')
      self.send_header("Access-Control-Allow-Headers", "X-Requested-With")
      self.send_header("Access-Control-Allow-Headers", "Content-Type")
      self.send_header("Content-Type", content_type)
      self.end_headers()

   def do_OPTIONS(self):
      self.response_success()

   def do_HEAD(self):
      self.response_success()

   def do_GET(self):
      url = self.path[1:].strip() # replace leading '/'

      if not url:
         return

      content_type = ''
      if os.path.exists(url):
         f = open(url)
         content_type = mimetypes.guess_type(url)[0]
         size = os.path.getsize(url)
      elif not url.startswith('http'):
         self.response_success()
         return
      else:
         f = urlopen(url=url)

      try:
         if not content_type:
            if py3:
               content_type = f.getheader("Content-Type")
               size = f.getheader("Content-Length")
            else:
               content_type = f.info().getheaders("Content-Type")[0]
               size = f.info().getheaders("Content-Length")[0]

         self.send_response(200)
         self.send_header('Access-Control-Allow-Origin', '*')
         self.send_header("Content-Type", content_type)
         self.send_header("Content-Disposition", 'attachment; filename="{}"'.format(os.path.basename(url)))
         self.send_header("Content-Length", str(size))
         self.end_headers()
         shutil.copyfileobj(f, self.wfile)
      finally:
         f.close()
         DownloadProxy.running = DownloadProxy.forever

   @staticmethod
   def runProxy(forever = False, ip = '', port = 8000):
      """
      """
      DownloadProxy.running = True
      DownloadProxy.forever = forever
      DownloadProxy.protocol_version = "HTTP/1.0"
      httpd = HTTPServer((ip, port), DownloadProxy)
      while True:
         httpd.handle_request()
         if not DownloadProxy.running:
            break

if __name__ == '__main__':
   import sys
   import getopt

   def usage():
      print('{} [--ip <listen interface>] [--port <port value, default 8000>] [--forever]'.format(__file__))

   def version():
      print(__version__)

   try:
      opts, args = getopt.getopt(sys.argv[1:], "hvi:p:f", ['help', 'version', 'ip=', 'port=', 'forever'])
   except getopt.GetoptError:
      usage()
      sys.exit(1)

   ip = ''
   port = 8000
   forever = False
   for opt, arg in opts:
      if opt in ('-h', '--help'):
         usage()
         sys.exit(0)
      elif opt in ('-v', '--version'):
         version()
         sys.exit(0)
      elif opt in ('-i', '--ip'):
         ip = arg
      elif opt in ('-p', '--port'):
         port = int(port)
      elif opt in ('-f', '--forever'):
         forever = True

   DownloadProxy.runProxy(forever=forever, ip=ip, port=port)
