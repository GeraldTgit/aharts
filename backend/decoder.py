from public_backend import *
import random
import string

# log file path + new file name
key_absolute_dir = temp_db_dir + "/do_not_delete.key"

def repeat_key_to_length(key, length):
    repetitions = (length // len(key)) + 1
    repeated_key = (key * repetitions)[:length]
    return repeated_key

def decrypt_string(encrypted_message, key):
    key = repeat_key_to_length(key, len(encrypted_message))
    decrypted = []
    for encrypted_char, key_char in zip(encrypted_message, key):
        decrypted_char = chr(ord(encrypted_char) ^ ord(key_char))
        decrypted.append(decrypted_char)
    return ''.join(decrypted)

# Task with a file saved on c:/path/to/do_not_delete.py
# Read the file then
# Assign the first 8 digit/chars to the random_integer variable
# and assign the rest of the characters to the encrypted_string variable
'''Example:
57666318 mScpPUEau~}h`jai_\]HI
SYX[SQmvgEPjOV

random_integer = 57666318
encrypted_string = mScpPUEau~}h`jai_\]HI
SYX[SQmvgEPjOV
'''

# Decrypt the encrypted string using the random integer
decrypted_string = decrypt_string(encrypted_string, random_integer)
print("Decrypted String:", decrypted_string)