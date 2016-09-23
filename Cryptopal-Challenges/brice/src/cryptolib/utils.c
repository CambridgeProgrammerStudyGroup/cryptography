#include <stdlib.h>

#include "common.h"
#include "errors.h"


ERROR toBase64(
  const bytes raw,
  const int raw_length,
  OUT unsigned char* base64,
  const int base64_limit,
  OUT int* out_length
);

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
);

ERROR fromHex(
  const unsigned char* hex,
  const int hex_length,
  OUT bytes raw,
  const int raw_limit,
  OUT int* out_length
){
  int raw_index = 0;
  for (int i = 0; i < (hex_length-1); i+=2){
    // grab two hex chars from string
    char aByte[3] = {hex[i],hex[i+1],0};
    long c = strtol(aByte, NULL, 16);

    if(raw_index>raw_limit){ return LIMIT_TOO_SMALL; }
    raw[raw_index] = (char) c;

  }
  return OK;
};
