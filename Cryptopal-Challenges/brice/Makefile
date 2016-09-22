# For OSX, Install openssl with `brew install openssl`

DEBUG=false
CC=gcc

LIBS= -lssl -lcrypto
INCLUDES= -I/usr/local/opt/openssl/include
LDFLAGS= -L/usr/local/opt/openssl/lib


ifeq ($(DEBUG),true)
    CFLAGS="-g -O0"
else
    CFLAGS=""
endif

main:
	$(CC) $(CFLAGS) src/try.c src/utils.c -o try.out -I./src/ $(LIBS) $(LDFLAGS) $(INCLUDES)
