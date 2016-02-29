# Network Security - Programming Assignment 2

I have implemented programming assignment 2 using python 2.

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
The server is run assuming that certificates have already been generated with name server
Example:
```sh
python server.py 4180
```

### Client
The client is run assuming that certificates have already been generated with name client
Example:
```sh
python client.py brussels.clic.cs.columbia.edu 4180
```
