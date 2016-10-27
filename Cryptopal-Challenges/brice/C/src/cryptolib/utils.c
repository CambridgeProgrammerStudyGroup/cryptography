#include <stdlib.h>
#include <stdbool.h>

#include "common.h"
#include "errors.h"

/* FROM RFC 4648

The Base 64 encoding is designed to represent arbitrary sequences of
octets in a form that allows the use of both upper- and lowercase
letters but that need not be human readable.

A 65-character subset of US-ASCII is used, enabling 6 bits to be
represented per printable character.  (The extra 65th character, "=",
is used to signify a special processing function.)

The encoding process represents 24-bit groups of input bits as output
strings of 4 encoded characters.  Proceeding from left to right, a
24-bit input group is formed by concatenating 3 8-bit input groups.
These 24 bits are then treated as 4 concatenated 6-bit groups, each
of which is translated into a single character in the base 64
alphabet.

Each 6-bit group is used as an index into an array of 64 printable
characters.  The character referenced by the index is placed in the
output string.

                   Table 1: The Base 64 Alphabet

  Value Encoding  Value Encoding  Value Encoding  Value Encoding
      0 A            17 R            34 i            51 z
      1 B            18 S            35 j            52 0
      2 C            19 T            36 k            53 1
      3 D            20 U            37 l            54 2
      4 E            21 V            38 m            55 3
      5 F            22 W            39 n            56 4
      6 G            23 X            40 o            57 5
      7 H            24 Y            41 p            58 6
      8 I            25 Z            42 q            59 7
      9 J            26 a            43 r            60 8
     10 K            27 b            44 s            61 9
     11 L            28 c            45 t            62 +
     12 M            29 d            46 u            63 /
     13 N            30 e            47 v
     14 O            31 f            48 w         (pad) =
     15 P            32 g            49 x
     16 Q            33 h            50 y

Special processing is performed if fewer than 24 bits are available
at the end of the data being encoded.  A full encoding quantum is
always completed at the end of a quantity.  When fewer than 24 input
bits are available in an input group, bits with value zero are added
(on the right) to form an integral number of 6-bit groups.  Padding
at the end of the data is performed using the '=' character.  Since
all base 64 input is an integral number of octets, only the following
cases can arise:

(1) The final quantum of encoding input is an integral multiple of 24
    bits; here, the final unit of encoded output will be an integral
    multiple of 4 characters with no "=" padding.

(2) The final quantum of encoding input is exactly 8 bits; here, the
    final unit of encoded output will be two characters followed by
    two "=" padding characters.

(3) The final quantum of encoding input is exactly 16 bits; here, the
    final unit of encoded output will be three characters followed by
    one "=" padding character.
*/

ERROR toBase64(
  const bytes raw,
  const int raw_length,
  OUT unsigned char* base64,
  const int base64_limit,
  OUT int* out_length
){
  /* Note, there's a clean way of only testing the raw_length once
   * instead of for every character in the input:
   *
   *     raw_length/3; raw_length%3
   *
   * Then it's straight forward to loop, and handle the special cases
   * once at the end.
   */
  char b64c[] = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/";

  int b64_index = 0;
  for(int i = 0; i < raw_length; i+=3){
    unsigned char i0,i1,i2;
    unsigned char out[4] = {0};

    i0 = raw[i];
    if(i+1<raw_length){ i1 = raw[i+1]; } else { i1 = 0;}
    if(i+2<raw_length){ i2 = raw[i+2]; } else { i2 = 0;}

    out[0] = b64c[i0>>2];
    out[1] = b64c[(i0 & 0b00000011)<<4 ^ i1>>4];
    if(i+1<raw_length){
      out[2] = b64c[(i1 & 0b00001111)<<2 ^ i2>>6];
    } else { out[2]='='; }

    if(i+2<raw_length){
      out[3] = b64c[i2 & 0b00111111];
    } else { out[3]='='; }

    for(int j = 0; j < 4; j++){
        if(b64_index >= base64_limit){
          return LIMIT_TOO_SMALL;
        }
        base64[b64_index] = out[j];
        b64_index++;
    }
  }
  *out_length = b64_index;
  return OK;
};

ERROR fromBase64(
  const unsigned char* base64,
  const int base64_length,
  OUT bytes raw,
  const int raw_limit,
  OUT int* out_length
);

ERROR toHex(
  const bytes raw,
  const int raw_length,
  OUT unsigned char* hex,
  const int hex_limit,
  OUT int* out_length
){
  char* hc = "0123456789abcdef";
  int hi = 0;
  for(int i = 0; i < raw_length; i++){
    hi = i<<1; /* twice as many hex chars as input bytes */
    if(hi >= hex_limit){ return LIMIT_TOO_SMALL; }
    hex[hi] = hc[raw[i]>>4];
    hex[hi+1] = hc[raw[i] & 0x0f];
  }
  *out_length = hi+2;
  return OK;
};

bool isHex(c){
  return ('0' <= c && c <= '9') || ( 'A' <= c && c <= 'F' ) || ('a' <= c && c <= 'f');
}


ERROR fromHex(
  const unsigned char* hex,
  const int hex_length,
  OUT bytes raw,
  const int raw_limit,
  OUT int* out_length
){
  /* input should consist of entire bytes. */
  if((hex_length%2) != 0){return BAD_INPUT;}

  int raw_index = 0;
  for (int i = 0; i < (hex_length-1); i+=2){

    /* input should be exclusively hex characters */
    if(!isHex(hex[i]) || !isHex(hex[i+1])){ return BAD_INPUT; }

    char aByte[3] = {hex[i],hex[i+1],0};
    long c = strtol(aByte, NULL, 16);

    /* We don't have enough space to write the output */
    if(raw_index>=raw_limit){ return LIMIT_TOO_SMALL; }

    raw[raw_index] = (char) c;
    raw_index++;
  }
  *out_length = raw_index;
  return OK;
};

ERROR xor(const bytes A, const bytes B, const int len, OUT bytes out){
  for(int i = 0; i < len; i++){
    out[i] = A[i]^B[i];
  }
  return OK;
}
