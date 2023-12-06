hex_string = "9c8a41ed236902958aa9807b9196c246bb9988168c08532c741a44ea46534e73324649451b88cb961e6a4ee5feea5b44"

# Remove escape sequences and spaces
hex_string = hex_string.replace("\\x", "").replace(" ", "")

# Try decoding with different encodings
encodings_to_try = ['utf-8', 'latin-1', 'ISO-8859-1']

decoded_string = None
for encoding in encodings_to_try:
    try:
        byte_array = bytes.fromhex(hex_string)
        decoded_string = byte_array.decode(encoding)
        break
    except UnicodeDecodeError:
        pass

if decoded_string is not None:
    print(decoded_string)
else:
    print("Unable to decode with the provided encodings.")
