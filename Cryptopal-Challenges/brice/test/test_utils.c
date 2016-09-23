#include <stdlib.h>
#include <stdio.h>
#include <string.h>

#include "../cryptolib/api.h"

#include "common.h"

typedef struct {
  char* in;
  char* expected;
  ERROR status;
} Test ;


#define FAIL 1;
#define SUCCESS 0;

int test_utils_fromHex(void){
  Test tests[] = {
    {"00", "\x00", OK},
    {"01", "\x01", OK},
    {"ff", "\xff", OK},
    {"000x", "", BAD_INPUT},
    {"00 00", "", BAD_INPUT},
    {"111", "", BAD_INPUT},
    {"0102030405060708090a0b0c0d0e0f10", "\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0a\x0b\x0c\x0d\x0e\x0f\x10", OK},
    {NULL, NULL}
  };
  int test_status = SUCCESS;

  printf("TESTING: fromHex()\n");
  for (int i = 0; tests[i].in != NULL; i++){
    ERROR status = OK;
    const bytes in = (const bytes) tests[i].in;
    const bytes expected = (const bytes) tests[i].expected;
    ERROR expected_status = tests[i].status;
    char buffer[256] = {0};
    int len = 0;

    status = fromHex(in, strlen(in), (bytes) buffer, 256, &len);

    if(status != expected_status){
      printf("    FAIL: h(%s) unexpected status (got=%s, expected=%s)\n", in, error_string(status), error_string(expected_status));
      printf("        got:      x(");print_hex((const bytes) buffer);printf(")%lu \n",strlen(buffer));
      test_status = FAIL;
    }else if((strcmp(expected, buffer) !=0) || (strlen(expected) != strlen(buffer))){
      printf("    FAIL: h(%s)\n", in);
      printf("        expected: x(");print_hex(expected);printf(")%lu\n", strlen(expected));
      printf("        got:      x(");print_hex((const bytes) buffer);printf(")%lu \n",strlen(buffer));
      test_status = FAIL;
    }else{
      printf("    pass: h(%s)\n", in);
    }

  }
  return test_status;
}



int main(){
  return test_utils_fromHex();
    // || test_utils_toBase64();
}
