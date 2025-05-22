def img_to_bin(input_file, output_file):
    with open(input_file, "rb") as f:
        data = f.read()
    with open(output_file, "w") as f:
        for byte in data:
            f.write(f"{byte:08b}")

# Example usage:
img_to_bin("12345.PNG", "input_binary.txt")
img_to_bin("encrypted_cbc.png", "cbc_binary.txt")
img_to_bin("encrypted_ofb.png", "ofb_binary.txt")
img_to_bin("encrypted_cfb.png", "cfb_binary.txt")
img_to_bin("encrypted_ecb.png", "ecb_binary.txt")

