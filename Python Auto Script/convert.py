import os

def img_to_bin(input_file, output_file):
    with open(input_file, "rb") as f:
        data = f.read()
    with open(output_file, "w") as f:
        for byte in data:
            f.write(f"{byte:08b}")

def process_images_in_folder(folder_path):
    # Loop through all files in the folder
    for filename in os.listdir(folder_path):
        if filename.lower().endswith('.bmp'):  # Process only .bmp files
            input_file = os.path.join(folder_path, filename)
            output_file = os.path.join(folder_path, f"{os.path.splitext(filename)[0]}_binary.txt")
            
            # Call img_to_bin to convert BMP to binary and save it
            img_to_bin(input_file, output_file)
            print(f"Converted {filename} to binary and saved as {output_file}")

# Example usage:
folder_path = '//home/tmsa7/Downloads/test/outputs2'  # Replace with your folder path
process_images_in_folder(folder_path)
