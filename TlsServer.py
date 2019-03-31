#!/usr/bin/env python
# Server Program (TlsServer.py)
# Simulates server-side of TLS handshake.
# Listens for incoming TCP connections on port 50001, then negotiates TLS handshake during connection establishment.
# Successful connections are secured under TLS 1.2, applying encryption/decryption using AES 128 in CBC mode.
# Supports both Diffie-Hellman Ephemeral ("DHE") and RSA key agreements.

import socket
import ssl


# Open a new TCP socket where server listens for incoming connections
def open_tcp_socket():
    server_tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # create new TCP socket supporting IPv4
    server_tcp_socket.bind(('', 50001))  # assign TCP socket to port 50001
    server_tcp_socket.listen(1)  # begin listening for TCP requests on new socket
    return server_tcp_socket


# Establish a dedicated TLS context for secured connection
def create_tls_context():
    cert_path = "server.pem"  # server certificate
    key_path = "server.key"  # server private key
    dh_path = "dh.pem"  # Diffie-Hellman parameters, needed if key exchange mode is DHE
    ciphers = "AES128-SHA256:DHE-RSA-AES128-SHA256"  # cipher suites supported by server
    # DHE-RSA-AES128-SHA256 is OpenSSL equivalent to TLS_DHE_RSA_WITH_AES_128_CBC_SHA256
    # AES128-SHA256 is OpenSSL equivalent to TLS_RSA_WITH_AES_128_CBC_SHA256

    context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)  # sessions use TLS v1.2
    context.load_cert_chain(keyfile=key_path, certfile=cert_path)  # apply server key and certificate to context
    context.set_ciphers(ciphers)  # enable cipher suites at server
    context.load_dh_params(dh_path)  # apply DH params to the context
    context.options = ssl.OP_SINGLE_DH_USE  # use unique DH key for each session (enables DH Ephemeral)
    return context


# Accept incoming TCP connections from clients, then negotiate TLS handshake
# If successful returns dedicated socket secured over TLS, otherwise returns -1
def accept(s_socket):
    print "Server listening..."

    try:  # establish TCP connection with client
        client_socket, client_address = s_socket.accept()  # set up dedicated TCP socket for client connection
    except:  # connection failed to establish
        print "Connection failed..."
        return -1

    try:  # negotiate TLS handshake
        print "Connection succeeded, attempting handshake..."
        context = create_tls_context()  # create dedicated TLS context to be applied to incoming connection
        tls_sock = context.wrap_socket(client_socket, server_side=True)  # wrap connection with TLS context
    except:  # handshake failed to negotiate
        print "Handshake failed..."
        return -1
    else:  # handshake successfully negotiated
        print "Handshake succeeded. Chosen cipher is %s." % str(tls_sock.cipher()[0])
        return tls_sock


server_socket = open_tcp_socket()  # open new TCP socket that listens for incoming client connections

while True:  # server is always on, listening over TCP socket
    tls_socket = accept(server_socket)  # accept incoming connection and assign to dedicated socket
    data = tls_socket.recv(1024)  # receive data from client at socket (socket buffer is 1024 bytes)
    print "Server receives: %s" % data
