'''__author__ == mmm5fd, Monique Mezher'''
'''code based mainly off concepts read during lab at
 http://www.laurentluce.com/posts/python-and-cryptography-with-pycrypto/'''
from Crypto import Random
from Crypto.PublicKey import RSA
from Crypto.Cipher import AES
import os.path
#from simplecrypt import encrypt, decrypt
from Crypto.Hash import SHA

def secret_string(string, public_key):
    '''This returns a byte string encryption of the original string.
    Decrypting will return a byte string (considered valid from Piazza post)'''
    bstring = bytes(string, 'utf-8')
    enc_string = public_key.encrypt(bstring, 32)
    return enc_string

def priv_hash(private_hash, user_id):
    new_word= ""
    private_hash = str(private_hash)
    for letter in private_hash:
        letter= chr(ord(letter) + user_id)
        new_word+=letter
    return new_word
def decr_hash(ciphertext, user_id):
    new_word = ""
    for letter in ciphertext:
        letter= chr(ord(str(letter)) - user_id)
        new_word+=letter
    return str(new_word)

def read_encrypted(password, filename, string=True):
    with open(filename, 'rb') as input:
        ciphertext = input.read()
        plaintext = decrypt(password, ciphertext)
        if string:
            return plaintext.decode('utf8')
        else:
            return plaintext

def write_encrypted(password, filename, plaintext):
    with open(filename, 'wb') as output:
        ciphertext = encrypt(password, plaintext)
        output.write(ciphertext)


def encrypt_file(filename, sym_key):
    '''This will check for valid file (if it exists) and if the key is valid (16
    bytes, or handled accordingly). It returns True for valid encryption.'''
    if not os.path.isfile(filename):
        print("File does not exist.")
        return False
    if len(sym_key) > 16:
        sym_key = sym_key[:16]
        # takes only first 16 parts of sym_key
    elif len(sym_key) < 16:
        sym_key = sym_key + (16 - len(sym_key))*"x"
    iv = 16 * '\x01' #initialization vector. Arbitrary.
    key = AES.new(sym_key,  AES.MODE_CBC, iv)
    outfile = filename + ".enc"
    with open(filename, 'rb') as file:
        with open(outfile, 'wb') as encr_file:
            while True:
                chunk = file.read(16)
                if len(chunk) == 0:
                    break
                if len(chunk) %16 !=0:
                    chunk += b' ' * (16 - len(chunk) % 16)
                encr_file.write(key.encrypt(chunk))
    return True
def decrypt_file(filename, sym_key):
    '''This will check for valid file (if it exists, if name is .enc) and if the key is valid (16
        bytes, or handled accordingly). It returns True for valid decryption.'''
    #if not filename.endswith('.enc'):
        #print("File is not properly named for decryption.")
        #return False
    if not os.path.isfile(filename):
        print("File does not exist.")
        return False
    if len(sym_key) > 16:
        sym_key = sym_key[:16]
        # takes only first 16 parts of sym_key
    elif len(sym_key) < 16:
        sym_key = sym_key + (16 - len(sym_key)) * "x"
    iv = 16 * '\x01'  # initialization vector. Arbitrary.
    key = AES.new(sym_key, AES.MODE_CBC, iv)
    outfile = "decrypt_" + filename
    with open(filename, 'rb') as file:
        with open(outfile, 'wb') as decr_file:
            while True:
                chunk = file.read(16)
                if len(chunk) == 0:
                    break
                decr_file.write(key.decrypt(chunk))
    return True

def decrypt_file_file(filename, sym_key_file):
    '''This will check for valid file (if it exists, if name is .enc) and if the key is valid (16
        bytes, or handled accordingly). It returns True for valid decryption.'''
    #if not filename.endswith('.enc'):
        #print("File is not properly named for decryption.")
        #return False
    if not os.path.isfile(filename) or not os.path.isfile(sym_key_file):
        print("File does not exist.")
        return False
    sym_key_f = open(sym_key_file, 'rb')
    sym_key = sym_key_f.read()
    if len(sym_key) > 16:
        sym_key = sym_key[:16]
        # takes only first 16 parts of sym_key
    elif len(sym_key) < 16:
        sym_key = sym_key + (16 - len(sym_key)) * "x"
    iv = 16 * '\x01'  # initialization vector. Arbitrary.
    key = AES.new(sym_key, AES.MODE_CBC, iv)
    outfile = "decrypt_" + filename[4:]
    with open(filename, 'rb') as file:
        with open(outfile, 'wb') as decr_file:
            while True:
                chunk = file.read(16)
                if len(chunk) == 0:
                    break
                decr_file.write(key.decrypt(chunk))
    return True


def encrypt_file_file(filename, sym_key_file):
    '''This will check for valid file (if it exists) and if the key is valid (16
    bytes, or handled accordingly). It returns True for valid encryption.'''
    if not os.path.isfile(filename) or not os.path.isfile(sym_key_file):
        print("File does not exist.")
        return False
    sym_key_f = open(sym_key_file, 'rb')
    sym_key = sym_key_f.read()
    if len(sym_key) > 16:
        sym_key = sym_key[:16]
        # takes only first 16 parts of sym_key
    elif len(sym_key) < 16:
        sym_key = sym_key + (16 - len(sym_key))*"x"
    iv = 16 * '\x01' #initialization vector. Arbitrary.
    key = AES.new(sym_key,  AES.MODE_CBC, iv)
    outfile = "enc_" +filename
    with open(filename, 'rb') as file:
        with open(outfile, 'wb') as encr_file:
            while True:
                chunk = file.read(16)
                if len(chunk) == 0:
                    break
                if len(chunk) %16 !=0:
                    chunk += b' ' * (16 - len(chunk) % 16)

                encr_file.write(key.encrypt(chunk))
    return True
if __name__ == "__main__":
    print("Works")
    #encrypt_file_file("happy.txt", "bhjknll.txt")
    #decrypt_file_file("enc_happy.txt", "bhjknll.txt")