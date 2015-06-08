import socket
import sys
import select
from server import HOST
from server import PORT
BUFFER_SIZE = 4096

# TODO:
# 1. socket with context manager

class ChatClient():
    def __init__(self):
        self.socket = None
        self.username = ''
        self._create_socket()

    def _create_socket(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print 'Socket created'
        try:
            s.connect((HOST, PORT))
        except socket.error, msg:
            print 'Connect failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
            sys.exit()
        self.socket = s
        print 'Socket connect complete'

    def _sign_up(self):
        self.socket.send("Sign Up")
        username = ''
        while not username:
            username = raw_input("Please enter your username\n")
        password = ''
        while not password:
            password = raw_input("Please enter your password\n")
        self.socket.send(username)
        self.socket.send(password)

    def _sign_in(self):
        pass

    def start(self):
        print "Welcome to Chat Room!\n"
        option = ''
        while option != '1' and option != '2':
            print "Please choose from:"
            option = raw_input("1: Sign Up; 2: Sign In\n")
        if option == '1':
            self._sign_up()
        else:
            self._sign_in()

        # nickname = raw_input("What is your nickname? > ")
        # self.socket.send(nickname)
        while True:
            socket_list = [sys.stdin, self.socket]
            ready_to_read, ready_to_write, in_error = select.select(socket_list, [], [])
            for sock in ready_to_read:
                # if any([s for s in socket_list if s is None]):
                #     return 0
                if sock == sys.stdin:
                    self.socket.send(sys.stdin.readline())
                elif sock == self.socket:
                    data = self.socket.recv(BUFFER_SIZE)
                    if data != '':
                        print data
                    else:
                        return 0
                else:
                    print sock
        return 0

    def _print_options(self):
        print "Options: 'Sign In', 'Sign Out'"


if __name__ == '__main__':
    c = ChatClient()
    sys.exit(c.start())





