# TLS-handshake

Simulates a TLS handshake over top of a client-server TCP connection. Key agreement modes supported for the handshake are ephemeral Diffie-Hellman and RSA.

Includes six (9) files:

* TlsClient.py : simulates the client side of the connection
* TlsServer.py : simulates the server side of the connection
* TlsClient_p3.py : python3 version of client file
* TlsServer_p3.py : python3 version of server file
* client.key : client private key details - unused in current version
* client.pem : client certificate details - unused in current version
* server.key : server private key details
* server.pem : server certificate details
* dh.pem : server Diffie-Hellman parameters

Python scripts are written in *Python 2.7*.

New: Alternative Python 3 scripts included.

Client/server keys and certificates were generated using OpenSSL version 1.1.1b (26 Feb 2019).

## Installation

No special installation steps are necessary.

Ensure that all client files (TlsClient.py, client.pem, client.key) are stored in the same folder, and all server files (TlsServer.py, server.pem, server.key) are stored in the same folder. Client and server files can be saved to the same or a different directory.

Scripts run in Python 2.7 or Python 3 (see initialization steps below) using the pre-installed *socket*, *ssl*, and *sys* modules.

## Running the simulation

Initialize server first:

Python 2.7:
```bash
python TlsServer.py
```
Python 3:
```bash
python3 TlsServer_p3.py
```

Initialize client second. Requires one argument, <key_mode>, corresponding to the key agreement mode: DHE or RSA.

Python 2.7:
```bash
python TlsClient.py DHE
python TlsClient.py RSA
```
Python 3:
```bash
python3 TlsClient_p3.py DHE
python3 TlsClient_p3.py RSA
```

Expected output at server:

```bash
Server listening...
Connection succeeded, attempting handshake...
Handshake succeeded. Chosen cipher is (DHE-RSA-AES128-SHA256 OR AES128-SHA256).
Server receives: test_message
```

Expected output at client:

```bash
Connection succeeded, attempting handshake...
Handshake succeeded. Chosen cipher is (DHE-RSA-AES128-SHA256 OR AES128-SHA256).
Client sends: test_message
```

## License

MIT License

Copyright (c) 2019 Andrew Lappalainen

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
