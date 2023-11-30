import ctypes
import os
from des import *

# Define timespec struct
class Timespec(ctypes.Structure):
    _fields_ = [
        ("tv_sec", ctypes.c_long),
        ("tv_nsec", ctypes.c_long)
    ]

# Load the clock_gettime function from the librt.so library
librt = ctypes.CDLL("librt.so.1", use_errno=True)
clock_gettime = librt.clock_gettime
clock_gettime.argtypes = [ctypes.c_int, ctypes.POINTER(Timespec)]

# Constants for clock IDs (use CLOCK_MONOTONIC for elapsed time)
CLOCK_MONOTONIC = 1

# Function to measure elapsed time with nanosecond precision for edes
def measure_time_for_Edes():
    start_time = Timespec()
    end_time = Timespec()
    
    # Fill page with random values
    page_size = 4096  # 4KiB
    buffer = bytearray(page_size)

    # Open /dev/urandom
    with open("/dev/urandom", "rb") as urandom:
        # Read random data into the buffer
        urandom.readinto(buffer)

    
    #Gen Key
    key = os.urandom(256)

    # Measure start time
    clock_gettime(CLOCK_MONOTONIC, ctypes.byref(start_time))
    
    #Sbox Generation
    sboxes=sbox_gen(key)
    
    #Padder
    padder = padding.PKCS7(512).padder() # 64 bytes = 512 bit
    buffer= padder.update(buffer)
    buffer += padder.finalize()

    #Encrypt & Decrypt
    encrypted_text = encrypt_edes(buffer, sboxes)
    decrypted_text = decrypt_edes(encrypted_text, sboxes)

    #Unpadder
    unpadder = padding.PKCS7(512).unpadder()
    decrypted_text=unpadder.update(decrypted_text)
    decrypted_text += unpadder.finalize()
    
    # Measure end time
    clock_gettime(CLOCK_MONOTONIC, ctypes.byref(end_time))
    
    # Calculate elapsed time in nanoseconds
    elapsed_time_ns = (end_time.tv_sec - start_time.tv_sec) * 1e9 + (end_time.tv_nsec - start_time.tv_nsec)
    
    return elapsed_time_ns

# Function to measure elapsed time with nanosecond precision for des
def measure_time_for_Des():
    start_time = Timespec()
    end_time = Timespec()
    
    # Fill page with random values
    page_size = 4096  # 4KiB
    buffer = bytearray(page_size)

    # Open /dev/urandom
    with open("/dev/urandom", "rb") as urandom:
        # Read random data into the buffer
        urandom.readinto(buffer)

    #Gen Key
    key = os.urandom(8)
    cipher = DES.new(key, DES.MODE_ECB)

    # Measure start time
    clock_gettime(CLOCK_MONOTONIC, ctypes.byref(start_time))
    
    #Padder
    padder = padding.PKCS7(512).padder() # 64 bytes = 512 bit
    buffer= padder.update(buffer)
    buffer += padder.finalize()

    #Encrypt & Decrypt
    encrypted_text = cipher.encrypt(buffer)
    decrypted_text = cipher.decrypt(encrypted_text)

    #Unpadder
    unpadder = padding.PKCS7(512).unpadder()
    decrypted_text=unpadder.update(decrypted_text)
    decrypted_text += unpadder.finalize()

    # Measure end time
    clock_gettime(CLOCK_MONOTONIC, ctypes.byref(end_time))
    
    # Calculate elapsed time in nanoseconds
    elapsed_time_ns = (end_time.tv_sec - start_time.tv_sec) * 1e9 + (end_time.tv_nsec - start_time.tv_nsec)
    
    return elapsed_time_ns


measurements = 100000
nano = 1000000000

# Perform the measurement for edes
fastest_time_edes = -1
average_edes = 0
for a in range(measurements):
    elapsed_time = measure_time_for_Edes()
    if fastest_time_edes > elapsed_time or fastest_time_edes == -1:
        fastest_time_edes = elapsed_time
    average_edes +=  elapsed_time
print(f"Fastest Time for Edes: {fastest_time_edes/nano} seconds")
print(f"Average for Edes: {(average_edes/measurements)/nano} seconds")

# Perform the measurement for des
fastest_time_des = -1
average_des = 0
for a in range(measurements):
    elapsed_time = measure_time_for_Des()
    if fastest_time_des > elapsed_time or fastest_time_des == -1:
        fastest_time_des = elapsed_time
    average_des +=  elapsed_time
print(f"Fastest Time for Des: {fastest_time_des/nano} seconds")
print(f"Average for Des: {(average_des/measurements)/nano} seconds")