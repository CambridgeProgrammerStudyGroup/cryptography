#ifndef CRYPTOLIB_ERRORS_INCLUDED
#define CRYPTOLIB_ERRORS_INCLUDED

typedef enum {
  OK,
  OPENSSL_ERROR,
  IV_PROVIDED_IN_ERROR,
  LIMIT_TOO_SMALL,
  UNKNOWN_FATAL
} ERROR;

const unsigned char* error_string(ERROR status);
void log_error(ERROR status);

#endif
