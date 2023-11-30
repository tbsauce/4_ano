#include <iostream>
#include <openssl/des.h>
#include <vector>
#include "Sboxes.h"


int main() {

    //Key Generation
    std::string password = "key"; // The password
    std::array<unsigned char, 8> key = generate_key(password);
    DES_key_schedule keysched;
    DES_set_key((const_DES_cblock*)key.data(), &keysched);


    std::string plaintext = "Hello, World!";
    std::vector<unsigned char> bytes(plaintext.begin(), plaintext.end());

    // Encrypt
    bytes = addPaddingPKCS7(bytes);
    std::vector<unsigned char> encrypted = encryptDES(bytes, keysched);

    // Decrypt
    std::vector<unsigned char> decrypted = decryptDES(encrypted, keysched);
    decrypted = removePaddingPKCS7(decrypted);


    std::cout << "Original Text -> " + plaintext << std::endl;

    std::cout << "Encrypted Text -> " ;
    for ( int i=0 ; i < encrypted.size(); i++){
        std::cout << std::hex << std::setfill('0') << std::setw(2) << (int)encrypted[i];
    }

    std::cout << std::endl <<  "Decrypted Text -> " ;
    for ( int i=0 ; i < decrypted.size(); i++){
        std::cout << decrypted[i] ;
    }
    std::cout << std::endl;

    return 0;
}
