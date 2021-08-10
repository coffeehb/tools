import os, random, string

from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer


length = 8
chars = string.ascii_letters + string.digits
random.seed = (os.urandom(1024))


FTP_ROOT = '/home'
USER = os.getenv('USER', 'user')
PASSWORD = os.getenv('PASSWORD', ''.join(random.choice(chars) for i in range(length)))
HOST =  os.getenv('HOST','0.0.0.0')
PORT = 21
PASSIVE_PORTS = '3000-3010'
ANONYMOUS = os.getenv('ANONYMOUS', False)

def main():
    user_dir = os.path.join(FTP_ROOT, USER)
    if not os.path.isdir(user_dir):
        os.mkdir(user_dir)
    authorizer = DummyAuthorizer()
    authorizer.add_user(USER, PASSWORD, user_dir, perm="elradfmw")
    if ANONYMOUS:
        authorizer.add_anonymous("/ftp_root/nobody")

    handler = FTPHandler
    handler.authorizer = authorizer
    handler.permit_foreign_addresses = True

    passive_ports = map(int, PASSIVE_PORTS.split('-'))
    handler.passive_ports = range(passive_ports[0], passive_ports[1])

    print('*************************************************')
    print('*                                               *')
    print('*    Docker image: mikatux                      *')
    print('*    https://github.com/mikatux/ftp-server      *')
    print('*                                               *')
    print('*************************************************')
    print('SERVER SETTINGS')
    print('---------------')
    print "FTP User: ",USER
    print "FTP Password: ",PASSWORD
    server = FTPServer((HOST, PORT), handler)
    server.serve_forever()

if __name__ == '__main__':
    main()
