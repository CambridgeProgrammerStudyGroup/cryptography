import string

class MisuseOfStringifyBinary(Exception):
    pass

def reverse_string(input_string):
    return input_string[::-1]

def chunk_string(input_string, chunk_size):
    return [input_string[i:i+chunk_size] for i in range(0, len(input_string), chunk_size)]

def make_binary_encoding_dict(character_set_string):
    base = len(character_set_string)
    return {k:bin(v) for k,v in zip(character_set_string, range(base))}

def stringify_binary(binary, string_length):
    binary_str = str(binary)[2:]
    if len(binary_str) > string_length:
        raise MisuseOfStringifyBinary()
    padding = (string_length - len(binary_str))*'0'
    return padding + binary_str

def something_to_binary(hex_string, encoding_string='0123456789abcdef'):
    lookup = make_binary_encoding_dict(encoding_string)
    return "".join([stringify_binary(lookup[c],4) for c in list(hex_string)])

def binary_to_base64(binary_str):
    lookup = make_binary_encoding_dict(string.uppercase+string.lowercase+'0123456789+/')
    lookup = {v:k for k, v in lookup.items}
