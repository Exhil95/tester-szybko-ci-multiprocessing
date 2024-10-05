import multiprocessing
from PIL import Image, ImageOps, ImageFilter
import os
import time
import random

# Funkcja przetwarzająca obraz
def process_image(image_path_output):
    image_path, output_dir = image_path_output
    try:
        with Image.open(image_path) as img:
            # Nakładanie filtra skali szarości
            grayscale_image = ImageOps.grayscale(img)
            # Nakładanie filtra rozmycia
            blurred_image = grayscale_image.filter(ImageFilter.BLUR)
            output_path = os.path.join(output_dir, os.path.basename(image_path))
            blurred_image.save(output_path)
    except Exception as e:
        print(f"Failed to process {image_path}: {e}")

# Generowanie przykładowych obrazów
def generate_sample_images(input_dir, num_images):
    if not os.path.exists(input_dir):
        os.makedirs(input_dir)
    for i in range(num_images):
        img = Image.new('RGB', (1920, 1080), (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))
        img.save(os.path.join(input_dir, f'image_{i}.jpg'))

# Funkcja przetwarzająca obrazy sekwencyjnie
def process_images_sequentially(input_dir, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    image_paths = [os.path.join(input_dir, fname) for fname in os.listdir(input_dir) if fname.endswith(('png', 'jpg', 'jpeg'))]
    for image_path in image_paths:
        process_image((image_path, output_dir))

# Funkcja przetwarzająca obrazy równolegle z użyciem Pool
def process_images_in_parallel(input_dir, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    image_paths = [os.path.join(input_dir, fname) for fname in os.listdir(input_dir) if fname.endswith(('png', 'jpg', 'jpeg'))]
    # Tworzenie puli procesów
    pool = multiprocessing.Pool(processes=multiprocessing.cpu_count())
    pool.map(process_image, [(image_path, output_dir) for image_path in image_paths])
    pool.close()
    pool.join()

if __name__ == '__main__':
    input_dir = 'input_images'  # Katalog z obrazami wejściowymi
    output_dir_seq = 'output_images_seq'  # Katalog na obrazy wyjściowe (sekwencyjnie)
    output_dir_par = 'output_images_par'  # Katalog na obrazy wyjściowe (równolegle)

    # Generowanie przykładowych obrazów
    print("Generating sample images...")
    generate_sample_images(input_dir, 1000)

    # Przetwarzanie sekwencyjne
    print("Starting sequential processing...")
    start_time_seq = time.time()
    process_images_sequentially(input_dir, output_dir_seq)
    end_time_seq = time.time()
    seq_time = end_time_seq - start_time_seq
    print(f"Time taken for sequential processing: {seq_time} seconds")

    # Przetwarzanie równoległe
    print("Starting parallel processing...")
    start_time_par = time.time()
    process_images_in_parallel(input_dir, output_dir_par)
    end_time_par = time.time()
    par_time = end_time_par - start_time_par
    print(f"Time taken for parallel processing: {par_time} seconds")

    # Różnica w czasie
    print(f"Difference in time: {seq_time - par_time} seconds")
