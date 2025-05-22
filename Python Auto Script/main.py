"""
Image Encryption and RSA Signature Project

This script:
1. Converts PNG to BMP for better handling of encrypted images
2. Encrypts an image using AES-128 in ECB, CBC, CFB, and OFB modes
3. Saves encrypted images in viewable BMP format
4. Generates and saves keys for each encryption method
5. Generates RSA keys (private and public)
6. Creates a hash of the CBC-encrypted image using SHA1
7. Signs the hash using the RSA private key
8. Verifies the signature using the RSA public key
9. Displays the original and encrypted images for comparison
"""

import os
import io
import secrets
import hashlib
import base64
import struct
import matplotlib.pyplot as plt
from PIL import Image
from Crypto.Cipher import AES
from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA1
from Crypto.Util.Padding import pad, unpad
import numpy as np

def generate_aes_key(key_size=16):  # 16 bytes = 128 bits
    """Generate a random AES-128 key."""
    return secrets.token_bytes(key_size)

def png_to_bmp(png_path, bmp_path):
    """Convert PNG to BMP format."""
    img = Image.open(png_path)
    img.save(bmp_path, format="BMP")
    return bmp_path

def encrypt_image_to_bmp(image_path, key, mode, mode_name, output_dir):
    """Encrypt image using specified AES mode and save as viewable BMP."""
    # Read the image
    with open(image_path, 'rb') as f:
        img_data = f.read()
    
    # Parse BMP header (typically 54 bytes, but can vary)
    # Extract header to preserve it
    header_size = 54  # Standard BMP header size
    header = img_data[:header_size]
    image_data = img_data[header_size:]
    
    # Pad the image data to be a multiple of the block size
    block_size = AES.block_size
    padded_image_data = pad(image_data, block_size)
    
    iv = None
    if mode != AES.MODE_ECB:  # ECB doesn't use IV
        iv = secrets.token_bytes(block_size)
    
    # Setup cipher based on the mode
    if mode == AES.MODE_ECB:
        cipher = AES.new(key, AES.MODE_ECB)
    else:
        cipher = AES.new(key, mode, iv=iv)
    
    # Encrypt only the image data (not the header)
    encrypted_data = cipher.encrypt(padded_image_data)
    
    # Create encrypted BMP by combining original header with encrypted data
    encrypted_bmp = header + encrypted_data
    
    # Save encrypted image
    encrypted_path = os.path.join(output_dir, f"encrypted_{mode_name}.bmp")
    with open(encrypted_path, 'wb') as f:
        f.write(encrypted_bmp)
    
    # Save key
    key_path = os.path.join(output_dir, f"key_{mode_name}.bin")
    with open(key_path, 'wb') as f:
        f.write(key)
    
    # Save IV if applicable
    if iv:
        iv_path = os.path.join(output_dir, f"iv_{mode_name}.bin")
        with open(iv_path, 'wb') as f:
            f.write(iv)
    
    # Also save the raw encrypted data for the RSA signing (CBC mode only)
    if mode == AES.MODE_CBC:
        raw_path = os.path.join(output_dir, f"raw_encrypted_{mode_name}.bin")
        with open(raw_path, 'wb') as f:
            f.write(encrypted_data)
    
    return encrypted_path, iv

def display_images(original_path, encrypted_paths, mode_names):
    """Display the original image alongside the encrypted ones."""
    original = Image.open(original_path)
    
    # Create a figure with subplots
    fig, axs = plt.subplots(1, len(encrypted_paths) + 1, figsize=(15, 5))
    
    # Display original image
    axs[0].imshow(original)
    axs[0].set_title("Original Image")
    axs[0].axis('off')
    
    # Display encrypted images
    for i, (path, mode) in enumerate(zip(encrypted_paths, mode_names)):
        try:
            encrypted_img = Image.open(path)
            axs[i+1].imshow(encrypted_img)
            axs[i+1].set_title(f"AES-{mode}")
            axs[i+1].axis('off')
        except Exception as e:
            axs[i+1].text(0.5, 0.5, f"Error displaying {mode} encrypted image:\n{str(e)}", 
                         horizontalalignment='center', verticalalignment='center')
            axs[i+1].axis('off')
    
    plt.tight_layout()
    plt.savefig("comparison.png")
    plt.show()

def generate_rsa_keypair(key_size=2048):
    """Generate an RSA key pair."""
    key = RSA.generate(key_size)
    private_key = key.export_key()
    public_key = key.publickey().export_key()
    
    # Save keys to files
    with open("private_key.pem", "wb") as f:
        f.write(private_key)
    
    with open("public_key.pem", "wb") as f:
        f.write(public_key)
    
    return private_key, public_key

def create_hash(file_path):
    """Create SHA1 hash of a file."""
    h = SHA1.new()
    with open(file_path, "rb") as f:
        chunk = f.read(8192)
        while chunk:
            h.update(chunk)
            chunk = f.read(8192)
    return h

def sign_hash(hash_obj, private_key):
    """Sign a hash using RSA private key."""
    key = RSA.import_key(private_key)
    signer = pkcs1_15.new(key)
    signature = signer.sign(hash_obj)
    
    # Save signature to file
    with open("signature.bin", "wb") as f:
        f.write(signature)
    
    return signature

def verify_signature(hash_obj, signature, public_key):
    """Verify a signature using RSA public key."""
    key = RSA.import_key(public_key)
    verifier = pkcs1_15.new(key)
    
    try:
        verifier.verify(hash_obj, signature)
        return True
    except (ValueError, TypeError):
        return False

def main():
    # Set paths
    image_path = "12345.PNG"  # Replace with your image path
    outputs_dir = "outputs2"
    os.makedirs(outputs_dir, exist_ok=True)
    
    # Task 1: AES Encryption
    print("Task 1: AES-128 Encryption of Image")
    
    # Convert PNG to BMP for better handling
    bmp_path = os.path.join(outputs_dir, "input_image.bmp")
    png_to_bmp(image_path, bmp_path)
    print(f"Converted PNG to BMP: {bmp_path}")
    
    # Step 1-2: Generate AES-128 key
    aes_key = generate_aes_key()
    print(f"Generated 128-bit AES key: {aes_key.hex()}")
    
    # Save the master AES key
    with open(os.path.join(outputs_dir, "master_aes_key.bin"), 'wb') as f:
        f.write(aes_key)
    
    # Step 3: Encrypt using different modes
    modes = [AES.MODE_ECB, AES.MODE_CBC, AES.MODE_CFB, AES.MODE_OFB]
    mode_names = ["ECB", "CBC", "CFB", "OFB"]
    encrypted_paths = []
    
    for mode, mode_name in zip(modes, mode_names):
        print(f"\nEncrypting with AES-{mode_name} mode...")
        
        # Use the same key for all methods or generate new ones for each
        # mode_key = generate_aes_key()  # Uncomment if you want unique keys per mode
        mode_key = aes_key  # Using the same key for all modes
        
        # Encrypt and save the image
        encrypted_path, iv = encrypt_image_to_bmp(bmp_path, mode_key, mode, mode_name, outputs_dir)
        encrypted_paths.append(encrypted_path)
        
        print(f"Saved encrypted image to {encrypted_path}")
        print(f"Saved encryption key to {os.path.join(outputs_dir, f'key_{mode_name}.bin')}")
        
        if iv:
            print(f"Saved IV to {os.path.join(outputs_dir, f'iv_{mode_name}.bin')}")
    
    # Step 4: Display the encrypted images
    print("\nDisplaying original and encrypted images...")
    display_images(bmp_path, encrypted_paths, mode_names)
    
    # Task 2: RSA Signature
    print("\nTask 2: RSA Signature Generation and Verification")
    
    # Step 1: Generate RSA key pair
    print("Generating 2048-bit RSA key pair...")
    private_key, public_key = generate_rsa_keypair()
    print("RSA keys generated and saved to private_key.pem and public_key.pem")
    
    # Step 2: Create hash of CBC-encrypted image
    # Use the raw encrypted data for hashing (without BMP header)
    cbc_raw_encrypted_path = os.path.join(outputs_dir, "raw_encrypted_CBC.bin")
    print(f"\nCreating SHA1 hash of {cbc_raw_encrypted_path}...")
    hash_obj = create_hash(cbc_raw_encrypted_path)
    print(f"SHA1 hash: {hash_obj.hexdigest()}")
    
    # Save the hash
    with open(os.path.join(outputs_dir, "cbc_image_hash.txt"), 'w') as f:
        f.write(hash_obj.hexdigest())
    
    # Step 3: Sign the hash
    print("\nSigning the hash with RSA private key...")
    signature = sign_hash(hash_obj, private_key)
    print(f"Signature created and saved to signature.bin")
    print(f"Signature (hex): {signature.hex()[:64]}...")
    
    # Step 4: Verify the signature
    print("\nVerifying the signature using RSA public key...")
    is_valid = verify_signature(hash_obj, signature, public_key)
    print(f"Signature verification result: {is_valid}")
    
    print("\nAll tasks completed successfully!")
    print(f"All files saved to {outputs_dir}/")

if __name__ == "__main__":
    main()

if __name__ == "__main__":
    main()