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
    # def get_host_port(self,url):

    # connects with a host on a port and returns a socket
    def connect(self, host, port):
        # use sockets!
        if (port is None):
            # default to port 80 if none is given
            port = 80
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((host, port))
        return s

    # parses out the three digit code that the server returns
    def get_code(self, data):
        return data.split()[1]

    # parses out the header content that the server returns
    def get_headers(self, data):
        return data.split("\r\n\r\n")[0]

    # parses out the body content that the server returns
    def get_body(self, data):
        return data.split("\r\n\r\n")[1]

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
    def parse_response(self, data):
        code = self.get_code(data)
        body = self.get_body(data)
        return (code, body)

    # issues a GET request to the URL
    def GET(self, url, args=None):
        # sets default values
        code = 500
        body = ""

        # parse the URL to get data from it
        parsed = urlparse(url)
        path = parsed.path

        # catch for empty paths
        if (path == ""):
            path = "/"

        # connects to the host at some port
        s = self.connect(parsed.hostname, parsed.port)

        # create the GET request
        request = "GET " + path + " HTTP/1.1\r\n"
        request += "Host: " + parsed.hostname + "\r\n"
        request += "Accept: */*\r\n"  # not even sure if I need this
        request += "Connection: close\r\n"  # gets request data faster
        request += "\r\n"

        # send the request, get the response, and parse it
        s.sendall(request)
        response = self.recvall(s)
        (code, body) = self.parse_response(response)

        return HTTPRequest(int(code), body)

    # issues a POST request to the URL
    def POST(self, url, args=None):
        # sets default values
        code = 500
        body = ""

        # parse the URL to get data from it
        parsed = urlparse(url)
        path = parsed.path

        # catch for empty paths
        if (path == ""):
            path = "/"

        # connects to the host at some port
        s = self.connect(parsed.hostname, parsed.port)

        # figure out the legth and content of the post arguments
        length = 0
        post_data = ""
        if (args is not None):
            post_data = urllib.urlencode(args)
            length = len(post_data)

        # create the POST request
        request = "POST " + path + " HTTP/1.1\r\n"
        request += "Host: " + parsed.hostname + "\r\n"
        request += "Accept: */*\r\n"  # not even sure if I need this
        request += "Content-Length: " + str(length) + "\r\n"
        if (length > 0):
            request += "Content-Type: application/x-www-form-urlencoded\r\n"
        request += "Connection: close\r\n"  # gets request data faster
        request += "\r\n"

        # add the post data to the request
        if (length > 0):
            request += post_data

        # send the request, get the response, and parse it
        s.sendall(request)
        response = self.recvall(s)
        (code, body) = self.parse_response(response)

        return HTTPRequest(int(code), body)

    # determines if the request is either a post or get request
    def command(self, url, command="GET", args=None):
        if (command == "POST"):
            return self.POST(url, args)
        else:
            return self.GET(url, args)

if __name__ == "__main__":
    client = HTTPClient()
    command = "GET"
    if (len(sys.argv) <= 1):
        help()
        sys.exit(1)
    # accepts the form "httpclient.py URL"
    elif (len(sys.argv) == 2):
        print client.command(sys.argv[1], command)
    # accepts the form "httpclient.py COMMAND URL"
    elif (len(sys.argv) == 3):
        print client.command(sys.argv[2], sys.argv[1])
    # accepts the form "httpclient.py COMMAND URL ARGS"
    elif (len(sys.argv) == 4):
        print client.command(sys.argv[2], sys.argv[1], sys.argv[3])
