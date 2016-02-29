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
https://devcenter.heroku.com/articles/ssl-certificate-self

http://illumineconsulting.blogspot.de/2014/01/implementing-2-way-ssl-in-java-using.html
