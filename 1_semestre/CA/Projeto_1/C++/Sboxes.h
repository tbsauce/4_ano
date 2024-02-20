#ifndef SBOXES_H
#define SBOXES_H
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
#include <openssl/des.h>


# define KEY_LEN 32 // bytes
// To run g++ -o Output Sboxes.cpp -lssl -lcrypto
// To run ./Output
class Sboxes{
public:
    std::vector<std::vector<unsigned char>> sboxes;

    Sboxes(std::vector<unsigned char> inBytes){ // Constructor, takes in a vector of bytes and creates the sboxes
        std::vector<unsigned char> current_inner_array;

        for (size_t i = 0; i < inBytes.size(); ++i) {
            unsigned char byte_pair = inBytes[i];
            current_inner_array.push_back(byte_pair);

            // If the current inner array has 256 pairs (512 bytes), create a new one
            if (current_inner_array.size() == 256) {
                sboxes.push_back(current_inner_array);
                current_inner_array.clear();
            }
        }
    }

    static std::vector<unsigned char> sbox_result(std::vector<unsigned char> sbox, std::vector<unsigned char> plaintext) {
        std::vector<unsigned char> cyphertext;

        for (int i = 0; i < plaintext.size() - 3; i += 4) {
            unsigned char byte1 = plaintext[i];
            unsigned char byte2 = plaintext[i + 1];
            unsigned char byte3 = plaintext[i + 2];
            unsigned char byte4 = plaintext[i + 3];

            unsigned char res1 = byte4;
            unsigned char res2 = (byte3 + byte4);
            unsigned char res3 = (byte2 + byte3 + byte4);
            unsigned char res4 = (byte1 + byte2 + byte3 + byte4);

            unsigned char result1 = sbox[res1];
            unsigned char result2 = sbox[res2];
            unsigned char result3 = sbox[res3];
            unsigned char result4 = sbox[res4];

            cyphertext.push_back(result1);
            cyphertext.push_back(result2);
            cyphertext.push_back(result3);
            cyphertext.push_back(result4);
        }
        return cyphertext;
    }

    static Sboxes sbox_gen(std::string pwd) {
        unsigned char salt = 0;
        uint8_t key_256[256];
        PKCS5_PBKDF2_HMAC_SHA1(pwd.c_str(), pwd.length(), &salt, 1, 1000, sizeof (key_256), key_256);
        uint8_t key_4096[4096];
        PKCS5_PBKDF2_HMAC_SHA1(reinterpret_cast<const char*>(key_256), sizeof(key_256), &salt, 1, 1000, sizeof(key_4096), key_4096);
        int arr_size = sizeof(key_4096) / sizeof(key_4096[0]);
        std::vector<unsigned char> vec(key_4096,key_4096 + arr_size);
        Sboxes box(vec);
        return box;
    }
};

std::vector<unsigned char> addPaddingPKCS7(const std::vector<unsigned char>& input) {
    size_t block_size =64;
    size_t padding_value = block_size - (input.size() % block_size);
    std::vector<unsigned char> output = input;
    for (size_t i = 0; i < padding_value; i++) {
        output.push_back(static_cast<unsigned char>(padding_value));
    }
    return output;
}

// Function to remove PKCS#7 padding from a block
std::vector<unsigned char> removePaddingPKCS7(const std::vector<unsigned char>& input) {
    if (input.empty()) {
        throw std::runtime_error("Input vector is empty.");
    }
    unsigned char last_byte = input.back();
    if (last_byte > input.size()) {
        throw std::runtime_error("Invalid padding.");
    }
    for (size_t i = input.size() - last_byte; i < input.size(); i++) {
        if (input[i] != last_byte) {
            throw std::runtime_error("Invalid padding.");
        }
    }
    return std::vector<unsigned char>(input.begin(), input.end() - last_byte);
}

std::vector<std::vector<unsigned char>> splitIntoBlocks(const std::vector<unsigned char>& bytes, int blockSize) {
    std::vector<std::vector<unsigned char>> byteBlocks;
    
    for (size_t i = 0; i < bytes.size(); i += blockSize) {
        byteBlocks.push_back(std::vector<unsigned char>(bytes.begin() + i, bytes.begin() + std::min(i + blockSize, bytes.size())));
    }
    
    return byteBlocks;
}

// Function to convert a hexadecimal string to bytes
std::vector<unsigned char> hexStringToBytes(const std::string& hex) {
    std::vector<unsigned char> bytes;
    for (size_t i = 0; i < hex.length(); i += 2) {
        unsigned int byte;
        std::istringstream(hex.substr(i, 2)) >> std::hex >> byte;
        bytes.push_back(static_cast<unsigned char>(byte));
    }
    return bytes;
}

std::array<unsigned char, 8> generate_key(const std::string& password) {
    unsigned char salt[1] = {0}; // The salt
    std::array<unsigned char, 8> key;

    // Generate a key from the password
    if (!PKCS5_PBKDF2_HMAC_SHA1(password.c_str(), password.size(), salt, sizeof(salt), 1000, key.size(), key.data())) {
        std::cerr << "Error generating key from password" << std::endl;
        exit(1);
    }

    return key;
}

std::vector<unsigned char> encryptEDES(std::vector<unsigned char> bytes, Sboxes box){

    std::vector<std::vector<unsigned char>> byteBlocks = splitIntoBlocks(bytes, 64);

    //after add a for to go through each 64 block
    std::vector<unsigned char> encrypted_text;
    for (int j = 0; j < byteBlocks.size(); j++)
    {
        bytes = byteBlocks[j];
        
        //Devide into 2 equal parts 
        int midPoint = 64/2;
        std::vector<unsigned char> Li(bytes.begin(), bytes.begin() + midPoint);
        std::vector<unsigned char> Ri(bytes.begin() + midPoint, bytes.end());
        for (int i = 0; i < 16; i++) {
        
            std::vector<unsigned char> box_result = Sboxes::sbox_result(box.sboxes[i], Ri);

            std::vector<unsigned char> xor_box_li;
            for (int f = 0; f < 32; f++) {
                xor_box_li.push_back(box_result[f] ^ Li[f]);
            }
        
            Li = Ri;
            Ri = xor_box_li;
        }

        // Accumulate Li and Ri in the encrypted_text
        encrypted_text.insert(encrypted_text.end(), Li.begin(), Li.end());
        encrypted_text.insert(encrypted_text.end(), Ri.begin(), Ri.end());

    }

    return encrypted_text;
}

std::vector<unsigned char> decryptEDES(std::vector<unsigned char> encrypted_text, Sboxes box){
    std::vector<unsigned char> decrypted_text;

    std::vector<std::vector<unsigned char>> encryptedByteBlocks = splitIntoBlocks(encrypted_text, 64);
    
    for (int l = 0; l < encryptedByteBlocks.size(); l++)
    {
        encrypted_text = encryptedByteBlocks[l];
        int midPoint = 64/2;
        std::vector<unsigned char> Li(encrypted_text.begin(), encrypted_text.begin() + midPoint);
        std::vector<unsigned char> Ri(encrypted_text.begin() + midPoint, encrypted_text.end());


        //after add a for to go through each 64 block
        for (int i = 15; i >= 0; i--) {
            std::vector<unsigned char> box_result = Sboxes::sbox_result(box.sboxes[i], Li);

            std::vector<unsigned char> xor_box_ri;
            for (int j = 0; j < box_result.size(); j++) {
                xor_box_ri.push_back(box_result[j] ^ Ri[j]);
            }

            Ri = Li;
            Li = xor_box_ri;

        }

        // Accumulate Li and Ri in the decrypted_text
        decrypted_text.insert(decrypted_text.end(), Li.begin(), Li.end());
        decrypted_text.insert(decrypted_text.end(), Ri.begin(), Ri.end());
    }

    return decrypted_text;
}

std::vector<unsigned char> encryptDES(std::vector<unsigned char> paddedInput, DES_key_schedule keysched){
    // Split into blocks
    std::vector<std::vector<unsigned char>> blocks = splitIntoBlocks(paddedInput, 8);

    // Encrypt each block
    std::vector<unsigned char> encrypted;
    for (const auto& block : blocks) {
        unsigned char encryptedBlock[8];
        DES_ecb_encrypt((DES_cblock*)block.data(), (DES_cblock*)encryptedBlock, &keysched, DES_ENCRYPT);
        encrypted.insert(encrypted.end(), encryptedBlock, encryptedBlock + 8);
    }

    return encrypted;
}

std::vector<unsigned char> decryptDES(std::vector<unsigned char> encrypted, DES_key_schedule keysched){

    //Split into blocks
    std::vector<std::vector<unsigned char>> blocks = splitIntoBlocks(encrypted, 8);

    // Decrypt each block
    std::vector<unsigned char> decrypted;
    for (const auto& block : blocks) {
        unsigned char decryptedBlock[8];
        DES_ecb_encrypt((DES_cblock*)block.data(), (DES_cblock*)decryptedBlock, &keysched, DES_DECRYPT);
        decrypted.insert(decrypted.end(), decryptedBlock, decryptedBlock + 8);
    }
    return decrypted;
}



#endif // SBOXES_H