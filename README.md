# SSL Certification
I have implemented a simple file transfer client/server connection over SSL, with optional encryption using SSL on the client and SHA256 hashing to verify file integrity.

## Setup
In order to make sure all the certificates exist
please run
```sh
sh setup.sh
```

## Certificate generation
The self-signed certificates for both the server and client are generated using the
script in gencerts.sh:
```sh
sh gencerts.sh client
sh gencerts.sh server
```
The command in said script use RSA and SHA256 and have been established from:
* https://devcenter.heroku.com/articles/ssl-certificate-self
* http://illumineconsulting.blogspot.de/2014/01/implementing-2-way-ssl-in-java-using.html

## Usage
### Server
The server is run assuming that certificates have already been generated with name server, however files for the server ( and key ) and client certificates can also be provided
Example:
```sh
python server.py port# [server_cert server_key client_cert]
```

### Client
The client is run assuming that certificates have already been generated with name client, however files for the server (and key) and client certificates can also be provided
Example:
```sh
python client.py server_addr port# [client_cert client_key server_cert]
```
