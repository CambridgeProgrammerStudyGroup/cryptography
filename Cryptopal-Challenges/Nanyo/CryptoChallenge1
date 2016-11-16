#include <iostream>
#include <vector>
#include <string>

using namespace std;

//49276d206b696c6c696e6720796f757220627261696e206c696b65206120706f69736f6e6f7573206d757368726f6f6d

//SSdtIGtpbGxpbmcgeW91ciBicmFpbiBsaWtlIGEgcG9pc29ub3VzIG11c2hyb29t


typedef unsigned char byte;
typedef char character;

template<typename T>
ostream& operator<< (ostream& out, const vector<T>& v) {
	size_t last = v.size() - 1;
	for (size_t i = 0; i < v.size(); ++i) {
		out << v[i];
	}
	return out;
}

byte toNumber(character a) {
	string hexChars("0123456789abcdef");

	byte ret = (byte)hexChars.find(a);

	return ret;
}

vector<byte> hexTobin(vector<character> hexString) {
	vector<byte> binString;

	if (hexString.size() % 2 != 0) {
		throw invalid_argument("Ivalid hexadecimal string.");
	}

	// Ask what an iterator is and how it works
	for (vector<character>::iterator it = hexString.begin(); it != hexString.end(); it++) {
		character first = toNumber(*it);

		it++;
		character second = toNumber(*it);

		binString.push_back(second ^ (first << 4));

	}

	return binString;
}

character base64Value(int a) {
	string base64Chars("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/");

	return base64Chars[a];
}


vector<character> toBase64(vector<byte> raw) {
	vector<character> base64string;

	for (int i = 0; i < raw.size(); ++i) {
		character B1, B2, B3, B4;
		const char bitmask = 0b00111111;
		byte first, second, third;

		first = raw[i];
		B1 = base64Value(bitmask & (first >> 2));
		base64string.push_back(B1);

		++i;
		if (i < raw.size()) {

			second = raw[i];
			B2 = base64Value(bitmask & ((first << 4) ^ (second >> 4)));
			base64string.push_back(B2);

			++i;
			if (i < raw.size()) {

				third = raw[i];

				B3 = base64Value(bitmask & ((second << 2) ^ (third >> 6)));
				B4 = base64Value(bitmask & third);
				base64string.push_back(B3);
				base64string.push_back(B4);
			}
			else {
				third = 0;
				B3 = base64Value(bitmask & ((second << 2) ^ (third >> 6)));
				base64string.push_back(B3);
				base64string.push_back('=');
			}
		}
		else {
			second = 0;
			B2 = base64Value(bitmask & ((first << 4) ^ (second >> 4)));
			base64string.push_back(B2);
			base64string.push_back('=');
			base64string.push_back('=');
		}

	}

	return base64string;
}

string characterVectorToString(vector<character> v) {
	string s(v.begin(), v.end());
	return s;
}

string byteVectorToString(vector<byte> v) {
	string s(v.begin(), v.end());
	return s;
}

vector<byte> stringToByteVector(string s) {
	vector<byte> v(s.begin(), s.end());
	return v;
}

vector<character> stringToCharacterVector(string s) {
	vector<character> v(s.begin(), s.end());
	return v;
}

bool testBase64(string input, string expected) {
	vector<byte> in = stringToByteVector(input);
	vector<character> cs = toBase64(in);
	string actual = characterVectorToString(cs);

	bool isCorrect = expected.compare(actual) == 0;

	cout << ((isCorrect) ? "OK:" : "FAIL") << endl;
	cout << "    input: " << input << endl;
	cout << "    expected: " << expected << endl;
	cout << "    actual:   " << actual << endl << endl;
	return isCorrect;
}

int main() {
	// testing base64
	testBase64("any carnal pleasure.", "YW55IGNhcm5hbCBwbGVhc3VyZS4=");
	testBase64("any carnal pleasure", "YW55IGNhcm5hbCBwbGVhc3VyZQ==");
	testBase64("any carnal pleasur", "YW55IGNhcm5hbCBwbGVhc3Vy");
	testBase64("any carnal pleasu", "YW55IGNhcm5hbCBwbGVhc3U=");

	// Challenge 1
	string hex = "49276d206b696c6c696e6720796f757220627261696e206c696b65206120706f69736f6e6f7573206d757368726f6f6d";
	vector<character> hexInput(hex.begin(), hex.end());
	vector<byte> raw = hexTobin(hexInput);
	vector<character> base64 = toBase64(raw);

	testBase64(byteVectorToString(raw), "SSdtIGtpbGxpbmcgeW91ciBicmFpbiBsaWtlIGEgcG9pc29ub3VzIG11c2hyb29t");

	system("Pause");
	return 0;
}

