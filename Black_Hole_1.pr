import struct
import paq

print("Created by Jurijus Pacalovas.")

def transform_byte(byte, y):
    """Reversible transform: add y + 1 modulo 256"""
    return (byte + y + 1) % 256

def inverse_transform_byte(byte, y):
    """Inverse transform: subtract y + 1 modulo 256"""
    return (byte - y - 1) % 256

def compress_file(input_file, output_file):
    y_values = range(1, 256)
    with open(input_file, 'rb') as f:
        original_data = f.read()

    original_size = len(original_data)
    best_result = None
    best_y = None
    best_size = float('inf')

    for y in y_values:
        transformed = bytes(transform_byte(b, y) for b in original_data)
        compressed = paq.compress(transformed)
        if len(compressed) < best_size:
            best_result = compressed
            best_y = y
            best_size = len(compressed)

    if best_size + 1 < original_size:  # +1 byte for y
        with open(output_file, 'wb') as f:
            f.write(struct.pack('B', best_y))
            f.write(best_result)
        print(f" Compressed with y = {best_y}. Saved as {output_file}.")
        print(f"Original size: {original_size} → Compressed size: {best_size + 1}")
    else:
        print(" Compression not efficient; file not saved.")
        print(f"Original size: {original_size} → Would-be compressed size: {best_size + 1}")

def extract_file(input_file, output_file):
    with open(input_file, 'rb') as f:
        y_byte = f.read(1)
        y = struct.unpack('B', y_byte)[0]
        compressed_data = f.read()

    decompressed = paq.decompress(compressed_data)
    restored = bytes(inverse_transform_byte(b, y) for b in decompressed)

    with open(output_file, 'wb') as f:
        f.write(restored)
    print(f" Extracted with y = {y}. Saved as {output_file}.")

def main():
    print("Choose an option:")
    print("1. Compress")
    print("2. Extract")
    choice = input("Enter 1 or 2: ").strip()

    if choice == '1':
        input_file = input("Enter input filename: ").strip()
        output_file = input_file + ".b"
        compress_file(input_file, output_file)
    elif choice == '2':
        input_file = input("Enter compressed filename (.b): ").strip()
        output_file = input("Enter output filename: ").strip()
        extract_file(input_file, output_file)
    else:
        print("Invalid choice.")

if __name__ == "__main__":
    main()
