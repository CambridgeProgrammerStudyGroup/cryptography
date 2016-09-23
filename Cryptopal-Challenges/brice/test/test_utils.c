#include <stdlib.h>
#include <stdio.h>
#include <string.h>

#include "../cryptolib/api.h"

#include "common.h"

typedef struct {
  char* hex;
  char* expected;
} Test ;

Test tests[] = {
  {"01", "\x01"},
  {NULL, NULL}
};

int main(){
  for (int i = 0; tests[i].hex != NULL; i++){
    ERROR status = OK;
    char buffer[256] = {0};
    int len = 0;

    status = fromHex(tests[i].hex, strlen(tests[i].hex), buffer, 256, &len);
    if(status != OK){
      log_error(status); exit(1);
    }
    printf("fromHex(%s) -> x(", tests[i].hex);print_hex(buffer);printf(")\n");
  }
  return 0;
}
