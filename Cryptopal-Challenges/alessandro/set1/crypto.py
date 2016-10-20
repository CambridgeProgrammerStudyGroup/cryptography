import string

HEX_VALS = list('0123456789abcdef')
BASE64_VALS = list(string.uppercase + string.lowercase + '0123456789+/')
LETTERS = string.uppercase + string.lowercase


def bit(int, offset):
    return 1 if int & (1 << offset) else 0


def bits_to_int(bits):
    result = 0
    power = 1
    for bit in bits[::-1]:
        result += bit * power
        power *= 2
    return result
        

def hex_to_words(hex_string):
    return [HEX_VALS.index(hex) for hex in hex_string]


def words_to_bits(words):
    return [bit(w, offset) for w in words for offset in range(4)[::-1]]


def hex_to_bits(hex_string):
    return words_to_bits(hex_to_words(hex_string))


def chunkify(string, size):
    chunks = [string[i:i + size] for i in range(0, len(string), size)]
    return chunks
    
    
def bits_to_base64(bit_string):
    return "".join([BASE64_VALS[bits_to_int(s)] for s in chunkify(bit_string, 6)])
    
    
def xor(first, second):
    return [one ^ two for (one, two) in zip(first, second)]


def words_to_hex(word_string):
    return "".join([HEX_VALS[word] for word in word_string])


def bits_to_ascii(bit_string):
    return "".join([chr(bits_to_int(s)) for s in chunkify(bit_string, 8)])
  
  
def ascii_to_bits(ascii):
    return [bit(ord(c), offset) for c in ascii for offset in range(8)[::-1]]
    
    
def xor_with_char(hex_string, char):
    char_string = char * (len(hex_string) / 2)
    char_bits = ascii_to_bits(char_string)
    string_bits = hex_to_bits(hex_string)
    xored = xor(string_bits, char_bits)
    return bits_to_ascii(xored)


def count_letters(str):
    count = 0
    for c in str:
        if c in LETTERS:
            count += 1
    return count