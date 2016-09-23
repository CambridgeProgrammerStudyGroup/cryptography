#include <stdio.h>
#include <stdlib.h>

// #include "utils.h"

void print_hex(const unsigned char *s){
  while(*s)
    printf("%02x", (unsigned int) *s++);
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
  }
  return length;
}
