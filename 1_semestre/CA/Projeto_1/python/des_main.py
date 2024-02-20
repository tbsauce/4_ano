from des import *

plaintext = "Hello, World!"

#key Generation
key = "key"
key = random_gen(key,8)
cipher = DES.new(key, DES.MODE_ECB)

#Padder
binary_plaintext = plaintext.encode()
padder = padding.PKCS7(512).padder() # 64 bytes = 512 bit
binary_plaintext= padder.update(binary_plaintext)
binary_plaintext += padder.finalize()

#Encrypt
encrypted_text = cipher.encrypt(binary_plaintext)

# Decrypt
decrypted_text = cipher.decrypt(encrypted_text)

#Unpadder
unpadder = padding.PKCS7(512).unpadder()
decrypted_text=unpadder.update(decrypted_text)
decrypted_text += unpadder.finalize()
decrypted_text = decrypted_text.decode()

print("Original:", plaintext)
print("Encrypted:", encrypted_text.hex())
print("Decrypted:", decrypted_text)
