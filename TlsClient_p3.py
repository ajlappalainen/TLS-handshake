#!/usr/bin/env python
# Client Program (TlsClient.py)
# Simulates client-side of TLS handshake.
# Attempts to establish TCP connection with server, then negotiates TLS handshake during connection establishment.
# Successful connections are secured under TLS 1.2, applying encryption/decryption using AES 128 in CBC mode.
# Key agreement must be specified as either Diffie-Hellman Ephemeral ("DHE") or RSA.

import socket
import ssl
import sys


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
        tls_sock.settimeout(100)
        tls_sock.connect((s_address, s_port))  # attempt connection to server
    except:  # connection failed to establish
        print("Connection failed.")
        return -1
    try:  # negotiate TLS handshake
        print("Connection succeeded, attempting handshake...")
        tls_sock.do_handshake()  # perform TLS handshake with server
    except:  # handshake failed to negotiate
        print("Handshake failed.")
        return -1
    else:  # tls handshake successfully established
        print("Handshake succeeded. Chosen cipher is %s." % str(tls_sock.cipher()[0]))
        return tls_sock


# Get key exchange mode from user input, either DHE or RSA
def get_key_mode(arg_list):
    # sys.argv should return 2 arguments:
    # argv[0] contains the file name (TlsClient.py) and argv[1] contains key_mode
    if len(arg_list) != 2:  # if expected arguments are not specified, throw index error
        raise IndexError("Require 1 argument but %d were given. Only accept following argument: "
                         "<key_exchange_mode> = DHE or RSA" % (len(arg_list)-1))
    try:  # verify that key_mode is DHE or RSA, else throw value error
        key_mode = str(arg_list[1]).upper()
        if key_mode != "RSA" and key_mode != "DHE":  # throw value error if invalid key_mode
            raise ValueError("key_exchange_mode must be either DHE or RSA, not %s." % arg_list[1])
    except ValueError:
        raise ValueError("key_exchange_mode must be either DHE or RSA, not %s." % arg_list[1])
    else:
        return key_mode  # return key_mode to TlsClient if error checks pass


server_address, server_port = '127.0.0.1', 50001

key_exchange_mode = get_key_mode(sys.argv)  # key exchange mode: input either DHE or RSA

tls_socket = connect(server_address, server_port, key_exchange_mode)  # connect to server over dedicated socket

data = 'test_message'
print('Client sends: %s' % data)
tls_socket.send(data.encode())  # send data to server
tls_socket.close()  # close TCP connection with server
