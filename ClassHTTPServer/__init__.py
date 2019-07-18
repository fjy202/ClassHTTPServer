import wsgiref.simple_server as serv
import _thread
from cgi import parse_qs
import traceback
class app:
    def __init__(self,handleClass):
        self.handleClass=handleClass
    def run(self,host,port,debug=True):
        self.debug=debug
        print("• Serving HTTP on %s:%d"%(host,port))
        print("\033[5;41;33m• This is just a development server. Please do not use in production.\033[0m")
        with serv.make_server(host,port,self) as server:
            server.serve_forever()
    def __call__(self,environ,start_response):
        try:
            function=getattr(self.handleClass,parse_qs(environ['QUERY_STRING'])["method"][0])
        except:
            start_response("404 Not Found",[])
            return[b"<h1>404</h1>"]
        query=parse_qs(environ['QUERY_STRING'])
        del query["method"]
        query={x:query[x][0] for x in query}
        try:
            res=function(environ,*environ['PATH_INFO'].split("/")[1:],**query)
            start_response("200 OK",res[1])
        except Exception as e:
            if self.debug:
                res=[traceback.format_exc().encode()]
                start_response("500 Server Error",[])
        return [res[0].encode()]
