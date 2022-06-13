# try:
#     from cheroot.wsgi import Server as WSGIServer, PathInfoDispatcher
# except ImportError:
#     from cherrypy.wsgiserver import CherryPyWSGIServer as WSGIServer, WSGIPathInfoDispatcher as PathInfoDispatcher
from cheroot.wsgi import Server as WSGIServer, PathInfoDispatcher

import geo

d = PathInfoDispatcher({'/': geo})
server = WSGIServer(('0.0.0.0', 2525), d)

if __name__ == '__main__':
   try:
      server.start()
   except KeyboardInterrupt:
      server.stop()