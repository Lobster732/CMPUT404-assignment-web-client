#!/usr/bin/env python
# coding: utf-8
# Copyright 2013 Abram Hindle
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Do not use urllib's HTTP GET and POST mechanisms.
# Write your own HTTP GET and POST
# The point is to understand what you have to send and get experience with it

import sys
import socket
import re
# you may use urllib to encode data appropriately
import urllib
from urlparse import urlparse

def help():
    print "httpclient.py [GET/POST] [URL]\n"

class HTTPRequest(object):
    def __init__(self, code=200, body=""):
        self.code = code
        self.body = body

class HTTPClient(object):
    #def get_host_port(self,url):

    def connect(self, host, port):
        # use sockets!
        if (port == None):
            port = 80
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((host, port))
        return s

    def get_code(self, data):
        return None

    def get_headers(self,data):
        return None

    def get_body(self, data):
        return None

    # read everything from the socket
    def recvall(self, sock):
        buffer = bytearray()
        done = False
        while not done:
            part = sock.recv(1024)
            if (part):
                buffer.extend(part)
            else:
                done = not part
        return str(buffer)

    # parse out the code and the body from the response
    def parse_response(self, response):
        code = 500
        body = ""
        return (code, body)

    def GET(self, url, args=None):
        print "" # TODO: Remove
        print "In function 'GET'" # TODO: Remove
        code = 500
        body = ""

        parsed = urlparse(url)
        path = parsed.path

        if (path == ""):
            path = "/"

        print parsed # TODO: Remove
        print "hostname = ", parsed.hostname, "| port = ", parsed.port, "| path = ", path # TODO: Remove
        print "" # TODO: Remove

        s = self.connect(parsed.hostname, parsed.port)

        request = "GET " + path + " HTTP/1.1\r\n"
        request += "Host: " + parsed.hostname + "\r\n"
        request += "Accept: */*\r\n" # not even sure if I need this
        request += "Connection: close\r\n" # gets request data faster
        request += "\r\n"

        print request # TODO: Remove

        s.sendall(request)
        response = self.recvall(s)
        (code, body) = self.parse_response(response)
        print response # TODO: Remove

        return HTTPRequest(code, body)

    def POST(self, url, args=None):
        code = 500
        body = ""
        return HTTPRequest(code, body)

    def command(self, url, command="GET", args=None):
        print "" # TODO: Remove
        print "In function 'command'" # TODO: Remove
        print "url = ", url, "| command = ", command, "| args = ", args # TODO: Remove
        if (command == "POST"):
            return self.POST( url, args )
        else:
            return self.GET( url, args )
    
if __name__ == "__main__":
    print "" # TODO: Remove
    print "In function 'main'" # TODO: Remove
    client = HTTPClient()
    command = "GET"
    if (len(sys.argv) <= 1):
        help()
        sys.exit(1)
    elif (len(sys.argv) == 3):
        print "argv[1] = ", sys.argv[1], "| argv[2] = ", sys.argv[2] # TODO: Remove
        #print client.command( sys.argv[1], sys.argv[2] ) # TODO: Fix Maybe
        print client.command( sys.argv[2], sys.argv[1])
    else:
        print "command", command, "| argv[1] = ", sys.argv[1] # TODO: Remove
        #print client.command( command, sys.argv[1] ) # TODO: Fix Maybe
        print client.command( sys.argv[1], command )
