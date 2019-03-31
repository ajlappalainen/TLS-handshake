#!/usr/bin/env python
# Client Program (TlsClient.py)
# Simulates client-side of TLS handshake.
# Attempts to establish TCP connection with server, then negotiates TLS handshake during connection establishment.
# Successful connections are secured under TLS 1.2, applying encryption/decryption using AES 128 in CBC mode.
# Key agreement must be specified as either Diffie-Hellman Ephemeral ("DHE") or RSA.

import socket
import ssl


# Establish a dedicated TLS context for secured connection
def create_tls_context(key_exchange):
    cert_path = "client.pem"  # client certificate
    key_path = "client.key"  # client private key

    if key_exchange == "DHE":  # cipher suite specified by client for the given key exchange mode
        ciphers = "DHE-RSA-AES128-SHA256"  # OpenSSL equivalent to TLS_DHE_RSA_WITH_AES_128_CBC_SHA256
    elif key_exchange == "RSA":
        ciphers = "AES128-SHA256"  # OpenSSL equivalent to TLS_RSA_WITH_AES_128_CBC_SHA256

    context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)  # sessions use TLS v1.2
    context.load_cert_chain(keyfile=key_path, certfile=cert_path)  # apply client key and certificate to context
    context.set_ciphers(ciphers)  # enable specified cipher suite at client
    return context


# Attempt to establish TCP connection with server, then negotiate TLS handshake
# If successful returns dedicated socket secured over TLS, otherwise returns -1
def connect(s_address, s_port, key_exchange):
    try:  # establish TCP connection with server
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # create new TCP socket supporting IPv4
        context = create_tls_context(key_exchange)  # create dedicated TLS context to be applied to connection
        tls_sock = context.wrap_socket(client_socket, do_handshake_on_connect=False)  # wrap connection with TLS context
        tls_sock.connect((s_address, s_port))  # attempt connection to server
    except:  # connection failed to establish
        print "Connection failed."
        return -1
    try:  # negotiate TLS handshake
        print "Connection succeeded, attempting handshake..."
        tls_sock.do_handshake()  # perform TLS handshake with server
    except:  # handshake failed to negotiate
        print "Handshake failed."
        return -1
    else:  # tls handshake successfully established
        print "Handshake succeeded. Chosen cipher is %s." % str(tls_sock.cipher()[0])
        return tls_sock


server_address, server_port = '127.0.0.1', 50001

# key authentication: Diffie-Hellman Ephemeral or RSA, uncomment one
key_exchange_mode = "DHE"
# key_exchange_mode = "RSA"

tls_socket = connect(server_address, server_port, key_exchange_mode)  # connect to server over dedicated socket

data = 'test_message'
print 'Client sends: %s' % data
tls_socket.send(data)  # send data to server
tls_socket.close()  # close TCP connection with server
