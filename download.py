import requests
import gzip
import shutil
import os

# Path to the file
file_path = r"C:\Users\ASUS\PycharmProjects\ProteinContactMap\links.txt"

# Open and read the file
with open(file_path, 'r') as file:
    content = file.read()

for file_path in content.split('\n')[:5]:
    url = f"https://files.rcsb.org/pub/pdb/data/structures/all/pdb/{file_path}"
    save_dir = 'Training set'

    # Make sure the save directory exists
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    # Download the .gz file
    response = requests.get(url)
    if response.status_code == 200:
        gz_file_path = os.path.join(save_dir, file_path)

        # Save the .gz file
        with open(gz_file_path, 'wb') as file:
            file.write(response.content)

        # Decompress the .gz file
        decompressed_file_path = os.path.join(save_dir, file_path[:-3])  # Remove '.gz' from the file name
        with gzip.open(gz_file_path, 'rb') as f_in:
            with open(decompressed_file_path, 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)
        os.remove(gz_file_path)
        t = False
        with open(decompressed_file_path, 'rb') as f_in:
            content = f_in.read().decode('utf-8')
            if 'DNA' in content[:20] or 'RNA' in content[:20]:
                t = True
        if t:
            os.remove(decompressed_file_path)
        print(f"Decompressed file saved as '{decompressed_file_path}'.")
