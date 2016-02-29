from Crypto.Cipher import AES
from Crypto.PublicKey import RSA
from Crypto.Hash import SHA256
from Crypto import Random

# ==============================================================================
# CRYPTO
# ==============================================================================
# Pad to multiple of 16 using PKCS7 scheme
def pad(data):
    extras = AES.block_size - (len(data) % AES.block_size)
    # Each added character is the number of extras
    return data + chr(extras)*extras

# Unpad message
def unpad(data):
    # data without number of padded elements
    return data[:-ord(data[-1])]

# Encrypt with AES CBC
def AES_encrypt(plaintext, key):
    iv = Random.new().read(AES.block_size)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    ciphertext = iv + cipher.encrypt(pad(plaintext))
    return ciphertext

# Decrypt with AES CBC
def AES_decrypt(ciphertext, key):
    iv = ciphertext[:AES.block_size]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    plaintext = unpad(cipher.decrypt(ciphertext[AES.block_size:]))
    return plaintext

# Hash using SHA256
def SHA256_hash(plaintext):
    return SHA256.new(plaintext).hexdigest()

# Sign a hash with RSA
def RSA_sign(hash, key_filename):
    key_file = open(key_filename, 'r')
    key = RSA.importKey(key_file.read())
    # Last parameter of sign() is not used in implementation
    return key.sign(hash, "")

# Verify signature of hash using RSA
def RSA_verify(hash, signature, key_filename):
    key_file = open(key_filename, 'r')
    key = RSA.importKey(key_file.read())
    return key.verify(hash, signature)

# Encrypt with RSA
def RSA_encrypt(plaintext, key_filename):
    key_file = open(key_filename, 'r')
    key = RSA.importKey(key_file.read())
    return key.encrypt(plaintext, "")

# Decrypt with RSA
def RSA_decrypt(ciphertext, key_filename):
    key_file = open(key_filename, 'r')
    key = RSA.importKey(key_file.read())
    return key.decrypt(ciphertext)
# ==============================================================================
