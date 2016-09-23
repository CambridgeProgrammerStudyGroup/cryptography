#include <stdlib.h>
#include <stdio.h>
#include <string.h>

#include "../cryptolib/api.h"
#include "../cryptolib/errors.h"
#include "../../test/common.h"

int main(int argc, char** args){
  int challenge_status = FAIL;

  printf("=== Challenge-1: hex decoding & base64 encoding ===\n");
  ERROR status = OK;

  char* hex = "49276d206b696c6c696e6720796f757220627261696e206c696b65206120706f69736f6e6f7573206d757368726f6f6d";
  char* expected = "SSdtIGtpbGxpbmcgeW91ciBicmFpbiBsaWtlIGEgcG9pc29ub3VzIG11c2hyb29t";

  bytes raw = calloc(256, 1);
  int raw_limit = 256;
  int raw_length = 0;

  if( OK != (status = fromHex((const bytes) hex, strlen(hex), raw, raw_limit, &raw_length))){
    log_error(status); exit(1);
  };

  bytes base64 = calloc(256,1);
  int base64_limit = 256;
  int base64_length = 0;

  // print_hex(raw);printf(" (hex:%lu, raw:%lu)\n", strlen(hex), strlen(raw));

  if( OK != (status = toBase64(raw, raw_length, base64, base64_limit, &base64_length))){
    log_error(status); exit(1);
  };

  printf("Expected: %s (%lu)\n", expected, strlen(expected));
  printf("Actual:   %s (%i)\n", base64, base64_length);

  if(strcmp(expected, base64) == 0){
    challenge_status = SUCCESS;
  }
  free(raw);
  free(base64);

  return challenge_status;
}
