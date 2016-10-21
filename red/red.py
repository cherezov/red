#!/usr/bin/python

# @file red.py
# @author cherezov.pavel@gmail.com

import os
import shutil
import urllib2
import BaseHTTPServer

# Change log:
#   0.1 initial version
__version__ = 0.1

class DownloadProxy(BaseHTTPServer.BaseHTTPRequestHandler):
   def do_GET(self):
      url = self.path[1:] # replace '/'

      if not url or not url.startswith('http'):
         self.send_response(404)
         self.send_header("Content-Length", '0')
         self.end_headers()
         return

      f = urllib2.urlopen(url=url)
      try:
         size = f.info().getheaders("Content-Length")[0]
         content_type = f.info().getheaders("Content-Type")[0]

         self.send_response(200)
         self.send_header("Content-Type", content_type)
         self.send_header("Content-Disposition", 'attachment; filename="{}"'.format(os.path.basename(url)))
         self.send_header("Content-Length", str(size))
         self.end_headers()
         shutil.copyfileobj(f, self.wfile)
      finally:
         f.close()

def runDownloadProxy(ip = '', port = 8000):
   DownloadProxy.protocol_version = "HTTP/1.0"
   httpd = BaseHTTPServer.HTTPServer((ip, port), DownloadProxy)
   httpd.serve_forever()

if __name__ == '__main__':
   import sys
   import getopt

   def usage():
      print('{} [--ip <listen interface>] [--port <port value, default 8000>]'.format(__file__))

   def version():
      print(__version__)

   try:
      opts, args = getopt.getopt(sys.argv[1:], "hvi:p:", ['help', 'version', 'ip=', 'port='])
   except getopt.GetoptError:
      usage()
      sys.exit(1)

   ip = ''
   port =  8000
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

   runDownloadProxy(ip=ip, port=port)
