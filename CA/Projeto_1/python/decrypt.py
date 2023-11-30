from des import *
import sys

if __name__ == "__main__":
    if len(sys.argv) < 2 or len(sys.argv) > 3:
        print("Usage: python decrypt.py <password> <mode:optional>")
        sys.exit(1)

    mode = ""
    key = ""
    if len(sys.argv) == 2:
        key = sys.argv[1]
        mode = "des"
    elif len(sys.argv) == 3:
        key = sys.argv[1]
        mode = sys.argv[2]

    binary_string = sys.stdin.read()
    encrypted_text = bytes.fromhex(binary_string)

    decrypted_text = ""
    #Decrypt
    if(mode == "edes"):
        #GenSbox
        sboxes=sbox_gen(random_gen(key,256))
        decrypted_text = decrypt_edes(encrypted_text, sboxes)
    else:
        key = random_gen(key,8)
        cipher = DES.new(key, DES.MODE_ECB)
        decrypted_text = cipher.decrypt(encrypted_text)
    
    #Unpadder
    unpadder = padding.PKCS7(512).unpadder()
    decrypted_text=unpadder.update(decrypted_text)
    decrypted_text += unpadder.finalize()
    decrypted_text = decrypted_text.decode()

    sys.stdout.write(decrypted_text)
