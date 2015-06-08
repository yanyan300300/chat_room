import socket
import Queue
import sys
import threading
from db.user import User
from contextlib import contextmanager

HOST = ''       # Symbolic name meaning all available interfaces
PORT = 8888     # Arbitrary non-privileged port
BUFFER_SIZE = 1024


class Message:
    def __init__(self, t, nickname, content):
        self.type = t            # Sign In, Sign Out, Chat
        self.nickname = nickname
        self.content = content


class ChatServer:
    def __init__(self, name):
        self.socket = None
        # stores ip:port, connection pair
        self.name = name
        self.clients = {}
        self.messages = Queue.Queue()

    def _run(self, max_number_of_connections):
        # Start listening on socket
        self.socket.listen(max_number_of_connections)
        print 'Socket now listening'
        m = threading.Thread(target=self._broadcast)
        m.setDaemon(True)
        m.start()
        print "Started a socket to broadcast messages"
        while True:
            # wait to accept a connection - blocking call
            # sleep(5)
            conn, addr = self.socket.accept()
            self.clients[addr] = conn
            print 'Connected with ' + addr[0] + ':' + str(addr[1])
            # start new thread takes 1st argument as a function name to be run,
            # second is the tuple of arguments to the function.
            t = threading.Thread(target=self._clientthread, args=(conn, addr))
            t.start()

    @staticmethod
    @contextmanager
    def socketcontext(*args, **kwargs):
        s = socket.socket(*args, **kwargs)
        yield s
        s.close()

    def start(self, max_number_of_connections):
        with ChatServer.socketcontext(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            print 'Socket created'
            # Bind socket to local host and port
            try:
                s.bind((HOST, PORT))
            except socket.error, msg:
                print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
                sys.exit()
            self.socket = s
            print 'Socket bind to ' + str(HOST) + ':' + str(PORT)
            self._run(max_number_of_connections)

    def _sign_up_user(self, username, password):
        """
        To store (username, password) in the database
        Need to handle:
        1. username exists
        2. invalid password (later)
        :return:
        """
        print username, password
        User.create(username, password)
        print "New user created"


    def _sign_in_user(self):
        """
        Authentication of user
        :return:
        """

    # Function for handling connections. This will be used to create threads
    def _clientthread(self, conn, addr):
        # Sending message to connected client
        # conn.send('Welcome to the Chat Room...\n')
        # conn.send('Please enter your nickname...\n')
        # nickname = conn.recv(BUFFER_SIZE).rstrip()
        # self.messages.put(Message('Sign In', nickname, ''))
        # conn.send('Please say something...\n')
        # conn.send("Enter 'Leave' to quit...\n")
        # infinite loop so that function do not terminate and thread do not end.
        option = conn.recv(BUFFER_SIZE).rstrip()
        username, password = '', ''
        if option == 'Sign Up':
            username = conn.recv(BUFFER_SIZE).rstrip()
            password = conn.recv(BUFFER_SIZE).rstrip()
            self._sign_up_user(username, password)
        elif option == 'Sign In':
            self._sign_in_user()
        else:
            raise NotImplementedError
        while True:
            # Receiving from client
            data = conn.recv(BUFFER_SIZE).rstrip()
            print data
            # TODO: more elegant way to deal with Sign Out???
            if data == "Leave":
                del self.clients[addr]
                self.messages.put(Message('Sign Out', username, ''))
                break
            self.messages.put(Message('Chat', username, data))
        # came out of loop
        conn.close()

    def _broadcast(self):
        while True:
            message = self.messages.get()
            for addr, conn in self.clients.iteritems():
                if message.type == 'Sign In':
                    conn.send("{} enters the room".format(message.nickname))
                elif message.type == 'Sign Out':
                    conn.send("{} left the room".format(message.nickname))
                elif message.type == 'Chat':
                    conn.send("{} : {}".format(message.nickname, message.content))
            self.messages.task_done()
    #
    # def _test_db(self):


if __name__ == "__main__":
    server = ChatServer('Room 1')
    server.start(10)

