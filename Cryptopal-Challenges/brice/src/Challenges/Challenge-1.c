#include <stdlib.h>
#include <stdio.h>
#include <string.h>

#include "../cryptolib/api.h"
#include "../cryptolib/errors.h"

int main(int argc, char** args){
  ERROR status = OK;

  char* hex = "49276d206b696c6c696e6720796f757220627261696e206c696b65206120706f69736f6e6f7573206d757368726f6f6d";
  char* expected = "SSdtIGtpbGxpbmcgeW91ciBicmFpbiBsaWtlIGEgcG9pc29ub3VzIG11c2hyb29t";

  bytes raw = calloc(256, 1);
  int raw_limit = 256;
  int raw_length = 0;

  if( OK != (status = fromHex((const bytes) hex, strlen((char*)hex), raw, raw_limit, &raw_length))){
    log_error(status); exit(1);
  };

  bytes base64 = calloc(256,1);
  int base64_limit = 256;
  int base64_length = 0;

  if( OK != (status = toBase64(raw, raw_length, base64, base64_limit, &base64_length))){
    log_error(status); exit(1);
  };

  printf("Expected: %s\n", expected);
  printf("Actual: %s\n", base64);

  return 0;
}
