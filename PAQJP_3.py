import os
from time import time
import binascii
from qiskit import QuantumCircuit

print("Created by Jurijus Pacalovas.")
print("Quantum-Inspired Compression Algorithm")

class Compression:
    def cryptography_compression4(self):
        def quantum_transform(number, num_qubits=8):
            """Generate a deterministic value using QuantumCircuit structure."""
            try:
                # Create circuit to mimic quantum structure
                circuit = QuantumCircuit(num_qubits, num_qubits)
                binary = format(number % (2**num_qubits), f'0{num_qubits}b')
                for i, bit in enumerate(reversed(binary)):
                    if bit == '1':
                        circuit.x(i)
                circuit.h(range(num_qubits))
                for i in range(num_qubits):
                    circuit.rx(0.7853981633974483, i)  # π/4 radians
                for i in range(num_qubits - 1):
                    circuit.cx(i, i + 1)
                circuit.measure(range(num_qubits), range(num_qubits))

                # Deterministic output based on input and circuit structure
                seed = 42
                gate_count = len(circuit.data)  # Number of gates
                value = (number * 1664525 + gate_count * 1013904223 + seed) & 0xFFFF  # 16-bit to reduce memory
                return value
            except Exception as e:
                print(f"Warning: Transformation failed: {e}. Using original number.")
                return number

        # Constants
        max_elements = 2**16  # Reduced to 65,536 for memory efficiency
        max_file_size = 2**30  # 1 GB limit for compression

        # Validate input
        name_input = input("c, compress or e, extract? ").lower()
        if name_input not in ['c', 'e']:
            print("Error: Invalid input. Choose 'c' for compression or 'e' for extraction.")
            raise SystemExit(1)

        is_compression = name_input == 'c'
        filename = input("Enter input file name: ")
        filename = os.path.normpath(os.path.abspath(filename))  # Normalize and resolve path

        # Prompt for output filename
        if is_compression:
            output_file = filename + ".bin"
        else:
            output_file = input("Enter output file name for extraction: ")
            if not output_file:
                print("Error: Output file name cannot be empty.")
                raise SystemExit(1)
            output_file = os.path.normpath(os.path.abspath(output_file))  # Normalize and resolve path
            # Validate output file path
            try:
                output_dir = os.path.dirname(output_file) or '.'
                if not os.path.exists(output_dir):
                    print(f"Error: Output directory '{output_dir}' does not exist.")
                    raise SystemExit(1)
                if os.path.exists(output_file):
                    if not os.access(output_file, os.W_OK):
                        print(f"Error: Output file '{output_file}' exists but is not writable.")
                        raise SystemExit(1)
                    overwrite = input(f"Output file '{output_file}' exists. Overwrite? (y/n): ").lower()
                    if overwrite != 'y':
                        print("Operation cancelled.")
                        raise SystemExit(1)
            except OSError as e:
                print(f"Error: Invalid output file path '{output_file}': {e}")
                raise SystemExit(1)

        # Check input file
        try:
            if not os.path.exists(filename):
                print(f"Error: Input file '{filename}' not found.")
                raise SystemExit(1)
            if not os.access(filename, os.R_OK):
                print(f"Error: Input file '{filename}' is not readable (permission denied).")
                raise SystemExit(1)
            file_size = os.path.getsize(filename)
            if file_size == 0:
                print(f"Error: Input file '{filename}' is empty.")
                raise SystemExit(1)
            if is_compression and file_size > max_file_size:
                print(f"Error: Input file '{filename}' is too large ({file_size} bytes). Maximum size is {max_file_size} bytes.")
                raise SystemExit(1)
        except OSError as e:
            print(f"Error: Failed to access input file '{filename}': {e}")
            raise SystemExit(1)

        start_time = time()
        x1 = 0  # Counter for unique transformed values
        x4 = set()  # Tracks unique transformed values (closed when reset or deallocated)
        counts = 0  # Counts transformations
        output_binary = ""

        try:
            with open(filename, "rb") as file:
                data = file.read()
                binary_data = bin(int(binascii.hexlify(data), 16))[2:]
                binary_data = '0' * ((file_size * 8) - len(binary_data)) + binary_data
                if len(binary_data) != file_size * 8:
                    print(f"Error: Binary data length mismatch (expected {file_size * 8} bits, got {len(binary_data)})")
                    raise SystemExit(1)

                if is_compression:
                    # Generate deterministic metadata
                    data_hash = sum(ord(c) if isinstance(c, str) else c for c in data)
                    transformed_value = quantum_transform(data_hash)
                    if transformed_value not in x4:
                        if len(x4) >= max_elements:
                            print("Info: Resetting X4 to manage memory.")
                            x4.clear()  # X4 closed (reset) to manage memory
                            x1 = 0  # Reset X1
                        x4.add(transformed_value)
                        x1 += 1
                    counts += 1

                    # Encode metadata with fixed-length fields
                    file_size_bits = bin(file_size * 8)[2:].zfill(32)  # 32-bit file size (bits)
                    x1_bits = bin(x1)[2:].zfill(8)  # 8-bit x1
                    counts_bits = bin(counts)[2:].zfill(8)  # 8-bit counts
                    transformed_bits = bin(transformed_value)[2:].zfill(16)  # 16-bit transformed value

                    # Combine metadata and full binary data
                    output_binary = (
                        "1" + x1_bits + file_size_bits + counts_bits + transformed_bits + binary_data
                    )
                    output_binary = '0' * (8 - len(output_binary) % 8) + output_binary
                else:  # Extraction
                    working_binary = binary_data
                    try:
                        while working_binary.startswith('0'):
                            working_binary = working_binary[1:]
                        if not working_binary.startswith('1'):
                            raise ValueError("Invalid .bin file: Missing start bit")
                        working_binary = working_binary[1:]
                        if len(working_binary) < 8:
                            raise ValueError("Invalid .bin file: Insufficient data for x1")
                        x1_ref = int(working_binary[:8], 2)
                        if x1_ref < 0 or x1_ref > max_elements:
                            raise ValueError(f"Invalid .bin file: X1 out of range (got {x1_ref}, max {max_elements})")
                        working_binary = working_binary[8:]
                        if len(working_binary) < 32:
                            raise ValueError("Invalid .bin file: Insufficient data for file size")
                        file_size = int(working_binary[:32], 2) // 8
                        if file_size > max_file_size:
                            raise ValueError(f"Invalid .bin file: File size too large (got {file_size} bytes)")
                        working_binary = working_binary[32:]
                        if len(working_binary) < 8:
                            raise ValueError("Invalid .bin file: Insufficient data for counts")
                        counts_ref = int(working_binary[:8], 2)
                        if counts_ref < 0:
                            raise ValueError(f"Invalid .bin file: Counts negative (got {counts_ref})")
                        working_binary = working_binary[8:]
                        if len(working_binary) < 16:
                            raise ValueError("Invalid .bin file: Insufficient data for transformed value")
                        transformed_ref = int(working_binary[:16], 2)
                        working_binary = working_binary[16:]

                        # Generate transformed value for verification
                        data_hash = sum(ord(c) if isinstance(c, str) else c for c in data)
                        transformed_value = quantum_transform(data_hash)
                        if transformed_value not in x4:
                            if len(x4) >= max_elements:
                                print("Info: Resetting X4 to manage memory.")
                                x4.clear()  # X4 closed (reset) to manage memory
                                x1 = 0  # Reset X1
                            x4.add(transformed_value)
                            x1 += 1
                        counts += 1

                        # Verify metadata
                        if x1 != x1_ref:
                            raise ValueError(f"Invalid .bin file: X1 mismatch (expected {x1_ref}, got {x1})")
                        if counts != counts_ref:
                            raise ValueError(f"Invalid .bin file: Counts mismatch (expected {counts_ref}, got {counts})")
                        if transformed_value != transformed_ref:
                            raise ValueError(f"Invalid .bin file: Transformed value mismatch (expected {transformed_ref}, got {transformed_value})")

                        # Extract original data
                        if len(working_binary) < file_size * 8:
                            raise ValueError(f"Invalid .bin file: Data length mismatch (expected {file_size * 8} bits, got {len(working_binary)})")
                        output_binary = working_binary[:file_size * 8]
                    except ValueError as e:
                        print(f"Error: {e}")
                        raise SystemExit(1)

            # Write output
            try:
                n = int(output_binary, 2)
                output_bytes = binascii.unhexlify(f'%0{(len(output_binary) // 8) * 2}x' % n)
                with open(output_file, "wb") as f:
                    f.write(output_bytes)
            except (binascii.Error, OSError) as e:
                print(f"Error writing output file '{output_file}': {e}")
                raise SystemExit(1)

        except Exception as e:
            print(f"Error during processing: {e}")
            raise SystemExit(1)

        # X4 and X1 closed (deallocated) here when function returns
        return str(time() - start_time)

try:
    d = Compression()
    execution_time = d.cryptography_compression4()
    print(f"Execution time: {execution_time} seconds")
except SystemExit as e:
    exit(e.code)
except Exception as e:
    print(f"Unexpected error: {e}")
    exit(1)
