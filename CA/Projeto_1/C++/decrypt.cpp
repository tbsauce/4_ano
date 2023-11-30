#include "Sboxes.h"
#include <iostream>
#include <vector>

int main(int argc, char* argv[]){

    if (argc < 2 || argc > 3) {
        std::cout << "Usage: ./encrypt <password> <mode:optional>" << std::endl;
        return 1;
    }

    std::string key_string = argv[1];
    std::string mode = "des";

    if (argc == 3) {
        mode = argv[2];
    }

    std::string hexInput;
    std::vector<unsigned char> encrypted_text;

    // Read hexadecimal input from stdin
    while (std::cin >> hexInput) {
        // Convert the hexadecimal string to bytes
        std::vector<unsigned char> bytes = hexStringToBytes(hexInput);
        encrypted_text.insert(encrypted_text.end(), bytes.begin(), bytes.end());
    }

    //Decrypt
    std::vector<unsigned char> decrypted_text;
    if (mode == "edes")
    {
        //Sbox Generation
        Sboxes box = Sboxes::sbox_gen(key_string);
        //Decrypt Edes
        decrypted_text = decryptEDES(encrypted_text, box);
    }
    else
    {
        //Key Generation
        std::array<unsigned char, 8> key = generate_key(key_string);
        DES_key_schedule keysched;
        DES_set_key((const_DES_cblock*)key.data(), &keysched);
        //Decrypt Des
        decrypted_text = decryptDES(encrypted_text, keysched);
    }

    //Unpadder
    decrypted_text = removePaddingPKCS7(decrypted_text);

    for ( int i=0 ; i < decrypted_text.size(); i++){
        std::cout << decrypted_text[i] ;
    }
}