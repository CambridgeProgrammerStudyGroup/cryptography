#ifndef CRYPTOLIB_COMMON_INCLUDED
#define CRYPTOLIB_COMMON_INCLUDED

#define OUT /**/

#include "errors.h"

typedef unsigned char* bytes;

typedef ERROR (ENCRYPT_BLOCK)(
  const bytes key,
  const bytes plainblock,
  OUT bytes cipherblock
);

typedef ERROR (DECRYPT_BLOCK)(
  const bytes key,
  const bytes cipherblock,
  OUT bytes plainblock
);

typedef ERROR (PAD_FN)(
  const int block_size,
  const int text_length, /*The length of the text to be padded*/
  OUT bytes text, /* Pointer to the text buffer, which should be allocated as a multiple of block_size */
  const int text_limit
);

typedef ERROR (DEPAD_FN)(
  const int block_size,
  OUT bytes text, /* Pointer to the text buffer, We're going to 'depad' by overwriting the padding with '\0' */
  const int text_limit
);

typedef struct {
  int block_size;
  int key_size;
  ENCRYPT_BLOCK* encrypt;
  DECRYPT_BLOCK* decrypt;
} Primitive;

typedef struct {
  PAD_FN* pad;
  DEPAD_FN* depad;
} Padding;

typedef ERROR (MODE_ENCRYPT)(
  const Primitive* cipher,
  const Padding* padding,
  const bytes key,
  const bytes iv,
  const bytes plaintext,
  const int plaintext_length,
  OUT bytes ciphertext,
  const int ciphertext_limit
);

typedef ERROR (MODE_DECRYPT)(
  const Primitive* cipher,
  const Padding* padding,
  const bytes key,
  const bytes iv,
  const bytes ciphertext,
  const int ciphertext_length,
  OUT bytes plaintext,
  const int plaintext_limit
);

typedef struct {
  MODE_ENCRYPT* encrypt;
  MODE_DECRYPT* decrypt;
} Mode;

#endif
