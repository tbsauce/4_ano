from des import *

plaintext = "Hello, World!"
key = "key"

sboxes=sbox_gen(random_gen(key,256))

#Padder
binary_plaintext = plaintext.encode()
padder = padding.PKCS7(512).padder() # 64 bytes = 512 bit
binary_plaintext= padder.update(binary_plaintext)
binary_plaintext += padder.finalize()

#Encrypt
encrypted_text = encrypt_edes(binary_plaintext, sboxes)

# Decrypt
decrypted_text = decrypt_edes(encrypted_text, sboxes)

#Unpadder
unpadder = padding.PKCS7(512).unpadder()
decrypted_text=unpadder.update(decrypted_text)
decrypted_text += unpadder.finalize()
decrypted_text = decrypted_text.decode()

print("Original:", plaintext)
print("Encrypted:", encrypted_text.hex())
print("Decrypted:", decrypted_text)
