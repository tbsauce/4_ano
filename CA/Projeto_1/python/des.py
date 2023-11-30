
from Crypto.Cipher import DES
from cryptography . hazmat . primitives import hashes
from cryptography . hazmat . primitives . kdf . pbkdf2 import PBKDF2HMAC
from cryptography . hazmat . backends import default_backend
from cryptography.hazmat.primitives import padding

def sboxes( bytes_variable):
    current_inner_array =[]
    sboxes_matrix=[]

    for i in range(0, len(bytes_variable)):
        byte_pair = bytes_variable[i]
        current_inner_array.append(byte_pair)

        # If the current inner array has 256 pairs (512 bytes), create a new one
        if len(current_inner_array) == 256:
            sboxes_matrix.append(current_inner_array)
            current_inner_array = []

    return sboxes_matrix

def sbox_gen( sub_keystream): 
    boxes= sboxes(random_gen(sub_keystream,4096))
    return boxes

def sbox_result( sbox,plaintext):
    cyphertext=b''
    
    array=[]
    for i in  range(0,len(plaintext)):
        subarray=plaintext[i].to_bytes(1,byteorder="big")
        array.append(subarray)
    
    for i in range(0,len(array)-3,4):
        byte1=array[i]
        byte2=array[i+1]
        byte3=array[i+2]
        byte4=array[i+3]

        result1=sbox[int.from_bytes(byte4,byteorder='big')].to_bytes(1,byteorder="big")
        result2=sbox[(byte3[0]+byte4[0])%256].to_bytes(1,byteorder="big")
        result3=sbox[(byte2[0]+byte3[0]+byte4[0])%256].to_bytes(1,byteorder="big")
        result4=sbox[(byte1[0]+byte2[0]+byte3[0]+byte4[0])%256].to_bytes(1,byteorder="big")

        cyphertext+=result1+result2+result3+result4
    return cyphertext
        
    
# Transformar para blocos de 64 bytes
def bytesToArraybytes( bytesOriginal):
    blocksize=64
    byte_array=[]
    for i in range(0,len(bytesOriginal),blocksize):
        subarray=bytesOriginal[i:i+blocksize]
        byte_array.append(subarray)
    return byte_array

def random_gen(pwd,len):
    if(isinstance(pwd, str)):
        pwd = pwd.encode()
    salt = b'\x00'
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA1(),
        length=len,
        iterations=1000,
        salt=salt,
    )
    key = kdf.derive( pwd )
    return key

def encrypt_edes( binary_plaintext, sboxes):

    #Encrypt
    array_binarys_plaintext=bytesToArraybytes(binary_plaintext)
    encrypted_text = b''
    for k in range(len(array_binarys_plaintext)):
        binary_plaintext=array_binarys_plaintext[k]

        #Separate L and R
        midPoint = len(binary_plaintext) // 2
        Li = binary_plaintext[:midPoint]
        Ri = binary_plaintext[midPoint:]
        for l in range(16):
            sbox_xor_li = bytes(x ^ y for x, y in zip(sbox_result(sboxes[l],Ri), Li))
            Li = Ri
            Ri = sbox_xor_li

        encrypted_text += Li + Ri

    return encrypted_text

def decrypt_edes( encrypted_text, sboxes):

    #Decrypt
    array_encrypted_text=bytesToArraybytes(encrypted_text)

    decrypted_text = b''
    for k in range(len(array_encrypted_text)):
        encrypted_text=array_encrypted_text[k]
        midPoint = len(encrypted_text) // 2
        Li = encrypted_text[:midPoint]
        Ri = encrypted_text[midPoint:]

        for l in range(15, -1, -1):
            sbox_xor_ri = bytes(x ^ y for x, y in zip(sbox_result(sboxes[l],Li), Ri))
            Ri = Li
            Li = sbox_xor_ri

        decrypted_text += Li + Ri

    return decrypted_text