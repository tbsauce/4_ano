#include "Sboxes.h"


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

    std::string text;
    std::getline(std::cin, text);
    std::vector<unsigned char> bytes(text.begin(), text.end());
    bytes.push_back('\n');

    //Padder
    bytes = addPaddingPKCS7(bytes);

    std::vector<unsigned char> encrypted_text;
    if (mode == "edes")
    {   
        //Sbox Generation
        Sboxes box = Sboxes::sbox_gen(key_string);
        //Encrypt Edes
        encrypted_text = encryptEDES(bytes, box);
    }
    else
    {   
        //Key Generation
        std::array<unsigned char, 8> key = generate_key(key_string);
        DES_key_schedule keysched;
        DES_set_key((const_DES_cblock*)key.data(), &keysched);
        //Encrypt Des
        encrypted_text = encryptDES(bytes, keysched);
    }
    
    

    //Convert to hexadecimal
    for (int i = 0; i < encrypted_text.size(); i++) {
        std::cout << std::hex << std::setfill('0') << std::setw(2) << (int)encrypted_text[i];
    }
}