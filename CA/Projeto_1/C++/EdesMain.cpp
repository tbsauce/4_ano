#include <iostream>
#include <iomanip>
#include <vector>
#include <random>
#include <ctime>
#include <string>
#include <algorithm>
#include <stdint.h>
#include <openssl/crypto.h>
#include <openssl/evp.h>
#include "Sboxes.h"


int main(){
    
    std::string key = "key";
    std::string text = "Hello, World!";

    Sboxes box = Sboxes::sbox_gen(key);

    std::vector<unsigned char> bytes(text.begin(), text.end());

    //Encrypt
    bytes = addPaddingPKCS7(bytes);
    std::vector<unsigned char> encrypted_text = encryptEDES(bytes, box);

    //Decrypt
    std::vector<unsigned char> decrypted_text = decryptEDES(encrypted_text, box);
    decrypted_text = removePaddingPKCS7(decrypted_text);
    
    
    std::cout << "Original Text -> " + text << std::endl;

    std::cout << "Encrypted Text -> " ;
    for ( int i=0 ; i < encrypted_text.size(); i++){
        std::cout << std::hex << std::setfill('0') << std::setw(2) << (int)encrypted_text[i];
    }
    
    std::cout << std::endl << "Decrypted Text -> " ;
    for ( int i=0 ; i < decrypted_text.size(); i++){
        std::cout << decrypted_text[i] ;
    }
    std::cout << std::endl;
}