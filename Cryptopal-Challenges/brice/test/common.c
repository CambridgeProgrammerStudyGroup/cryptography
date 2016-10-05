#include <stdio.h>
#include <stdlib.h>

// #include "utils.h"

void print_hex(const unsigned char *s){
  while(*s)
    printf("%02x", (unsigned int) *s++);
}

void print_hex_c(const unsigned char *s, int len){
  for(int i = 0; i <len; i++){
    printf("%02x", (unsigned int) s[i]);
  }
}

long read_to_buffer(const char* filename, unsigned char** buffer){
  long length = 0;
  FILE * f = fopen (filename, "rb");

  if (f){
    fseek (f, 0, SEEK_END);
    length = ftell (f);
    fseek (f, 0, SEEK_SET);
    *buffer = malloc (length);
    if (*buffer)
    {
      fread (*buffer, 1, length, f);
    }
    fclose (f);
  }else{
    fprintf(stderr, "[FATAL]: File '%s' could not be opened.\n", filename);
    exit(1);
  }
  return length;
}
