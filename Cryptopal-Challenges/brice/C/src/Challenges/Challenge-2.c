#include <stdlib.h>
#include <stdio.h>
#include <string.h>

#include "../cryptolib/api.h"
#include "../cryptolib/errors.h"
#include "../../test/common.h"

int main(int argc, char** args){
  int challenge_status = FAIL;

  printf("=== Challenge-2: blockwide xor ===\n");
  ERROR status = OK;

  char* Ah = "1c0111001f010100061a024b53535009181c";
  char* Bh = "686974207468652062756c6c277320657965";
  char* expected = "746865206b696420646f6e277420706c6179";


  int limit = 256;
  int length = 0;

  bytes A = calloc(limit, 1);
  if( OK != (status = fromHex((const bytes) Ah, strlen(Ah), A, limit, &length))){
    log_error(status); exit(1);
  };

  bytes B = calloc(limit, 1);
  if( OK != (status = fromHex((const bytes) Bh, strlen(Bh), B, limit, &length))){
    log_error(status); exit(1);
  };

  bytes AxB = calloc(limit,1);
  if( OK != (status = xor((const bytes) A, (const bytes) B, length, AxB))){
    log_error(status); exit(1);
  };

  bytes AxBh = calloc(limit,1);
  if( OK != (status = toHex(AxB, length, AxBh, limit, &length))){
    log_error(status); exit(1);
  };

  printf("Expected: %s (%lu)\n", expected, strlen(expected));
  printf("Actual:   %s (%i)\n", AxBh, length);

  if(strcmp(expected, AxBh) == 0){
    challenge_status = SUCCESS;
  }
  free(A);
  free(B);
  free(AxB);
  free(AxBh);
  return challenge_status;
}
