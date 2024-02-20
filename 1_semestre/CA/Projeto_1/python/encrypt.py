from des import *
import sys


if __name__ == "__main__":
    if len(sys.argv) < 2 or len(sys.argv) > 3:
        print("Usage: python encrypt.py <password> <mode:optional>")
        sys.exit(1)

    
    key = sys.argv[1]
    mode = "des"

    if len(sys.argv) == 3:
        mode = sys.argv[2]

    plaintext = sys.stdin.read()

    #Padder
    binary_plaintext = plaintext.encode()
    padder = padding.PKCS7(512).padder() # 64 bytes = 512 bit
    binary_plaintext= padder.update(binary_plaintext)
    binary_plaintext += padder.finalize()

    encrypted_text = ""
    #Encrypt
    if(mode == "edes"):
        #GenSbox
        sboxes=sbox_gen(random_gen(key,256))
        encrypted_text = encrypt_edes(binary_plaintext, sboxes)
    else:
        key = random_gen(key,8)
        cipher = DES.new(key, DES.MODE_ECB)
        encrypted_text = cipher.encrypt(binary_plaintext)
    

    sys.stdout.write(encrypted_text.hex())
