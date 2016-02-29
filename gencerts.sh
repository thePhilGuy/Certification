#!/bin/sh
TARGET=$1

openssl genpkey -algorithm RSA -out $TARGET.key -pkeyopt rsa_keygen_bits:2048
openssl req -x509 -sha256 -new -subj '/C=US/ST=NY/L=New York/CN=Netsec 4180' -key $TARGET.key -out $TARGET.csr
openssl x509 -sha256 -days 365 -in $TARGET.csr -signkey $TARGET.key -out $TARGET.crt
rm $TARGET.csr
