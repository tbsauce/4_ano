#include <iostream>
#include <fstream>
#include <chrono>
#include <cstring>
#include <vector>
#include <openssl/des.h>
#include <openssl/rand.h>
#include <openssl/evp.h>
#include <openssl/pem.h>
#include <openssl/err.h>
#include "Sboxes.h"

using namespace std;

// Load the clock_gettime function from the librt.so library
extern "C" {
#include <time.h>
}

// Constants for clock IDs (use MY_CLOCK_MONOTONIC for elapsed time)
const int MY_CLOCK_MONOTONIC = 1;

// Function to measure elapsed time with nanosecond precision for Edes
long long measure_time_for_Edes() {
    struct timespec start_time, end_time; // Use struct timespec

    const int page_size = 4096; // 4KiB
    std::vector<unsigned char> buffer(page_size);

    // Open /dev/urandom
    ifstream urandom("/dev/urandom", ios::binary);
    urandom.read(reinterpret_cast<char*>(buffer.data()), page_size);
    urandom.close();


    // Generate Key
    const int key_size = 16;
    std::string key;
    key.resize(key_size);

    // Generate a random key
    RAND_bytes(reinterpret_cast<unsigned char*>(&key[0]), key_size);

    // Measure start time
    clock_gettime(MY_CLOCK_MONOTONIC, &start_time);

    // Sbox Generation
    Sboxes box = Sboxes::sbox_gen(key);
    
    // Padder
    std::vector<unsigned char> bytes = addPaddingPKCS7(buffer);

    // Encrypt & Decrypt
    std::vector<unsigned char> encrypted_text = encryptEDES(bytes, box);
    std::vector<unsigned char> decrypted_text = decryptEDES(encrypted_text, box);

    // Unpadder
    decrypted_text = removePaddingPKCS7(decrypted_text);

    // Measure end time
    clock_gettime(MY_CLOCK_MONOTONIC, &end_time);

    // Calculate elapsed time in nanoseconds
    long long elapsed_time_ns = (end_time.tv_sec - start_time.tv_sec) * 1e9 + (end_time.tv_nsec - start_time.tv_nsec);

    return elapsed_time_ns;
}

// Function to measure elapsed time with nanosecond precision for Des
long long measure_time_for_Des() {
    struct timespec start_time, end_time; // Use struct timespec

    // Fill page with random values
    const int page_size = 4096; // 4KiB
    std::vector<unsigned char> buffer(page_size);

    // Open /dev/urandom
    ifstream urandom("/dev/urandom", ios::binary);
    urandom.read(reinterpret_cast<char*>(buffer.data()), page_size);
    urandom.close();

    // Generate Key
    DES_cblock key;

    // Generate a random key
    if (!RAND_bytes(key, sizeof(key))) {
        std::cerr << "Error generating random key" << std::endl;
        return 1;
    }

    DES_key_schedule keysched;
    DES_set_key(&key, &keysched);


    // Measure start time
    clock_gettime(MY_CLOCK_MONOTONIC, &start_time);

    // Padder
    std::vector<unsigned char> paddedInput = addPaddingPKCS7(buffer);

    // Encrypt & Decrypt
    std::vector<unsigned char> encrypted = encryptDES(paddedInput, keysched);
    std::vector<unsigned char> decrypted = decryptDES(encrypted, keysched);
    
    // Unpadder
    decrypted = removePaddingPKCS7(decrypted);

    // Measure end time
    clock_gettime(MY_CLOCK_MONOTONIC, &end_time);

    // Calculate elapsed time in nanoseconds
    long long elapsed_time_ns = (end_time.tv_sec - start_time.tv_sec) * 1e9 + (end_time.tv_nsec - start_time.tv_nsec);

    return elapsed_time_ns;
}

int main() {
    const int measurements = 100000;
    const long long nano = 1000000000;

    // Perform the measurement for Edes
    long long fastest_time_edes = -1;
    long long average_edes = 0;
    for (int a = 0; a < measurements; a++) {
        long long elapsed_time = measure_time_for_Edes();
        if (fastest_time_edes > elapsed_time || fastest_time_edes == -1) {
            fastest_time_edes = elapsed_time;
        }
        average_edes += elapsed_time;
    }
    
    // Perform the measurement for Des
    long long fastest_time_des = -1;
    long long average_des = 0;
    for (int a = 0; a < measurements; a++) {
        long long elapsed_time = measure_time_for_Des();
        if (fastest_time_des > elapsed_time || fastest_time_des == -1) {
            fastest_time_des = elapsed_time;
        }
        average_des += elapsed_time;
    }

    std::cout << "Fastest Time for Edes: " << static_cast<double>(fastest_time_edes) / nano << " seconds" << std::endl;
    std::cout << "Average for Edes: " << static_cast<double>(average_edes / measurements) / nano << " seconds" << std::endl;

    std::cout << "Fastest Time for Des: " << static_cast<double>(fastest_time_des) / nano << " seconds" << std::endl;
    std::cout << "Average for Des: " << static_cast<double>(average_des / measurements) / nano << " seconds" << std::endl;

    return 0;
}
