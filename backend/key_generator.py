from public_backend import *
import random
import string

def repeat_key_to_length(key, length):
    repetitions = (length // len(key)) + 1
    repeated_key = (key * repetitions)[:length]
    return repeated_key

def generate_random_string(length=50):
    characters = string.ascii_letters + string.digits + string.punctuation
    random_string = ''.join(random.choice(characters) for _ in range(length))
    return random_string

def generate_random_integer(length=8):
    integers = string.digits
    random_int = ''.join(random.choice(integers) for _ in range(length))
    return random_int

def encrypt_string(message, key):
    key = repeat_key_to_length(key, len(message))
    encrypted = []
    for char, key_char in zip(message, key):
        encrypted_char = chr(ord(char) ^ ord(key_char))
        encrypted.append(encrypted_char)
    return ''.join(encrypted)

random_string = generate_random_string()
random_integer = generate_random_integer()

# Encrypt the random string using the random integer
encrypted_string = encrypt_string(random_string, random_integer)

# log file path + new file name
key_absolute_dir = temp_db_dir + "/do_not_delete.key"

# Check if the file exists, and create it if necessary
if not os.path.exists(key_absolute_dir):
    with open(key_absolute_dir, 'w') as file:
        file.write(f"{random_integer} {encrypted_string}")

print("Original String:", random_string)
print("Encrypted String:", encrypted_string)

def decrypt_string(encrypted_message, key):
    key = repeat_key_to_length(key, len(encrypted_message))
    decrypted = []
    for encrypted_char, key_char in zip(encrypted_message, key):
        decrypted_char = chr(ord(encrypted_char) ^ ord(key_char))
        decrypted.append(decrypted_char)
    return ''.join(decrypted)

# Decrypt the encrypted string using the random integer
decrypted_string = decrypt_string(encrypted_string, random_integer)
print("Decrypted String:", decrypted_string)