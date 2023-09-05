import base64
import hashlib
import os

def generate_key():
    return os.urandom(32)  

def initialize_cipher(key):
    return hashlib.sha256(key).digest()

def pad_data(data, block_size):
    padding_size = block_size - (len(data) % block_size)
    padding = bytes([padding_size]) * padding_size
    return data + padding

def unpad_data(data):
    padding_size = data[-1]
    return data[:-padding_size]

def encrypt_data(data):
    key = generate_key()
    block_size = 16  
    cipher_key = initialize_cipher(key)
    padded_data = pad_data(data.encode('utf-8'), block_size)
    
    encrypted_data = bytearray()
    previous_block = cipher_key
    
    for i in range(0, len(padded_data), block_size):
        block = bytes(x ^ y for x, y in zip(padded_data[i:i + block_size], previous_block))
        encrypted_data.extend(block)
        previous_block = block
    
    return key, encrypted_data

def decrypt_data(key, encrypted_data):
    block_size = 16 
    cipher_key = initialize_cipher(key)
    
    decrypted_data = bytearray()
    previous_block = cipher_key
    
    for i in range(0, len(encrypted_data), block_size):
        block = bytes(x ^ y for x, y in zip(encrypted_data[i:i + block_size], previous_block))
        decrypted_data.extend(block)
        previous_block = encrypted_data[i:i + block_size]
    
    return unpad_data(decrypted_data).decode('utf-8')

def save_credentials(website, username, password, file_path='passwords.txt'):
    key, encrypted_password = encrypt_data(password)
    
    with open(file_path, 'a') as f:
        f.write(f"{website},{username},{base64.b64encode(encrypted_password).decode('utf-8')},{base64.b64encode(key).decode('utf-8')}\n")
        
    print("Data saved to passwords.txt, password encrypted")

def retrieve_credentials(website, username, file_path='passwords.txt'):
    with open(file_path, 'r') as f:
        lines = f.readlines()
        
    for line in lines:
        parts = line.strip().split(',')
        site = parts[0]
        user = parts[1]
        encrypted_password = base64.b64decode(parts[2].encode('utf-8'))
        key = base64.b64decode(parts[3].encode('utf-8'))
        
        if site == website and user == username:
            decrypted_password = decrypt_data(key, encrypted_password)
            print(f"Decrypted password for {website} and username {username} is: {decrypted_password}")
            return
    
    print("No matching credentials found")

def main():
    choice = input("Would you like to add a new entry or retrieve a password? (add/retrieve): ")
    
    if choice.lower() == 'add':
        website = input("Enter the website: ")
        username = input("Enter the username: ")
        password = input("Enter the password: ")
        
        save_credentials(website, username, password)
        
    elif choice.lower() == 'retrieve':
        website = input("Enter the website: ")
        username = input("Enter the username: ")
        
        retrieve_credentials(website, username)
        
    else:
        print("Invalid choice. Exiting.")

if __name__ == "__main__":
    main()
