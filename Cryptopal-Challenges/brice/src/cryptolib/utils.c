#include <stdlib.h>
#include <stdbool.h>

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
  if((hex_length%2) != 0){return BAD_INPUT;}
  int raw_index = 0;
  for (int i = 0; i < (hex_length-1); i+=2){

    if(!isHex(hex[i]) || !isHex(hex[i+1])){ return BAD_INPUT; }

    char aByte[3] = {hex[i],hex[i+1],0};
    long c = strtol(aByte, NULL, 16);

    if(raw_index>raw_limit){ return LIMIT_TOO_SMALL; }
    raw[raw_index] = (char) c;
    raw_index++;

  }

  return OK;
};
