import socket , sys
s= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
port = sys.argv[1]
s.bind(("0.0.0.0", int(port)))
s.listen(1)
print "Listening on port "+str(port)+"..."
(client, (ip, port)) = s.accept()
print " Received connection from : ", ip
while True:
    data = client.recv(1024)
    if data == "hello":
        print "Enter Your Command..."
    command = raw_input('~$ ')
    if "q" == command:
        client.send("quit")
        client.close()
        s.close()
        exit(0)
    client.send(command)
    while True:
        data = client.recv(1024)
        if data != None and data != "":
            print data
            break
        else:
            print "something wrong..."
            break
client.close()
s.close()

