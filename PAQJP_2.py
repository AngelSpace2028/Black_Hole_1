import os
import struct

print("Created by Jurijus Pacalovas.")

def geometric_series_sum():
    return 1.0  # 1/2 + 1/4 + 1/8 + 1/16 + ... = 1

def transform_byte(byte, y):
    """Applies transformation: x/y + 1 (approx)"""
    return int((byte / y) + geometric_series_sum()) % 256

def inverse_transform_byte(byte, y):
    """Reverses transformation: (byte - 1) * y"""
    return int((byte - geometric_series_sum()) * y) % 256

def compress_file(input_file, output_file):
    y_values = list(range(1, 256))  # Try all y values from 1 to 255
    with open(input_file, 'rb') as f:
        original_data = f.read()

    best_result = None
    best_y = None

    for y in y_values:
        transformed = bytes([transform_byte(b, y) for b in original_data])
        if best_result is None or len(transformed) < len(best_result):
            best_result = transformed
            best_y = y

    # Save the best result + y value as metadata
    with open(output_file, 'wb') as f:
        f.write(struct.pack('B', best_y))  # Save y as 1 byte
        f.write(best_result)

    print(f"Compressed using y = {best_y}. Saved as {output_file}.")

def extract_file(input_file, output_file):
    with open(input_file, 'rb') as f:
        y_byte = f.read(1)
        y = struct.unpack('B', y_byte)[0]
        compressed_data = f.read()

    restored = bytes([inverse_transform_byte(b, y) for b in compressed_data])

    with open(output_file, 'wb') as f:
        f.write(restored)

    print(f"Extracted with y = {y}. Saved as {output_file}.")

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
