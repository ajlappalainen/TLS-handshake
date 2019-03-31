# TLS-handshake

Simulates a TLS handshake over top of a client-server TCP connection. Key agreement modes supported for the handshake are ephemeral Diffie-Hellman and RSA.

Includes six (6) files:

* TlsClient.py : simulates the client side of the connection
* TlsServer.py : simulates the server side of the connection
* client.key : client private key details
* client.pem : client certificate details
* server.key : server private key details
* server.pem : server certificate details

Python scripts are written in *Python 2.7*. 

Client/server keys and certificates were generated using OpenSSL version 1.1.1b (26 Feb 2019).

## Installation

No special installation steps are necessary.

Ensure that all client files (TlsClient.py, client.pem, client.key) are stored in the same folder, and all server files (TlsServer.py, server.pem, server.key) are stored in the same folder. Client and server files can be saved to the same or a different directory.

Python scripts run in Python 2.7 using the pre-installed *socket* and *ssl* modules.

## Running the simulation

Initialize server first:

```bash
python TlsServer.py
```

Initialize client second. By default, client specifies DH ephemeral key exchange, however can be substituted with RSA by swapping comments in main line of code.

```bash
python TlsClient.py
```

Expected output at server:

```bash
Server listening...
Connection succeeded, attempting handshake...
Handshake succeeded. Chosen cipher is <DHE-RSA-AES128-SHA256 OR AES128-SHA256>.
Server receives: test_message
```

Expected output at client:

```bash
Connection succeeded, attempting handshake...
Handshake succeeded. Chosen cipher is DHE-RSA-AES128-SHA256 OR AES128-SHA256>.
Client sends: test_message
```

## License

MIT License

Copyright (c) 2019 Andrew Lappalainen

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.