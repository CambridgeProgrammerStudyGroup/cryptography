


#define FAIL 1;
#define SUCCESS 0;

void print_hex(const unsigned char *s);
void print_hex_c(const unsigned char *s, int len);

long read_to_buffer(
  const char* filename,
  unsigned char** buffer
);
