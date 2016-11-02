import unittest
from utils import pkcs7_pad


class TestPadding(unittest.TestCase):
    def test_padding_should_work_with_one_byte_to_pad(self):
        pt = bytearray("YELLOW SUBMARIN")
        blocksize = 16

        padded = pkcs7_pad(pt, blocksize)

        self.assertEquals(16, len(padded))

    def test_padding_bytes_will_be_size_of_padding_when_padding_one_byte(self):
        pt = bytearray("YELLOW SUBMARIN")
        blocksize = 16

        padded = pkcs7_pad(pt, blocksize)

        self.assertEquals(1, padded[-1])

    def test_when_padding_two_bytes_they_should_have_value_of_3(self):
        pt = bytearray("YELLOW SUBMAR")
        blocksize = 16

        padded = pkcs7_pad(pt, blocksize)

        self.assertEquals(3, padded[-1])
        self.assertEquals(3, padded[-2])
        self.assertEquals(3, padded[-3])

    def test_padding_multiple_of_blocksize_should_have_correct_padding_bytes(self):
        pt = bytearray("XXXX----XXXX----YELLOW SUBMARIN")
        blocksize = 16

        padded = pkcs7_pad(pt, blocksize)

        self.assertEquals(1, padded[-1])

    def test_padding_should_work_when_padding_a_block_of_right_length(self):
        pt = bytearray("YELLOW SUBMARINE")
        blocksize = 16

        padded = pkcs7_pad(pt, blocksize)

        self.assertEquals(32, len(padded))

if __name__ == "__main__":
    print("PKCS7 padding implemented successfully if all tests pass.")
    unittest.main()
