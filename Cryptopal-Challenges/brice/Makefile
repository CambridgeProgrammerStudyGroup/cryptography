# For OSX, Install openssl with `brew install openssl`

DEBUG=false
CC=gcc

CCOPTS= -Wno-pointer-sign

LIBS= -lssl -lcrypto
INCLUDES= -I/usr/local/opt/openssl/include -I./src/cryptolib
LDFLAGS= -L/usr/local/opt/openssl/lib


ifeq ($(DEBUG),true)
    CFLAGS="-g -O0"
else
    CFLAGS=
endif

BUILD_DIR=./build
TEST_DIR=./test_build

CRYPTOLIB_SRC=$(wildcard src/cryptolib/*.c)
CRYPTOLIB_OBJ=$(patsubst src/cryptolib/%.c,$(BUILD_DIR)/%.o,$(CRYPTOLIB_SRC))
CHALLENGES_SRC=$(wildcard src/Challenges/Challenge-*.c)
CHALLENGES_EXE=$(patsubst src/Challenges/%.c,%.exe,$(CHALLENGES_SRC))

TESTS_SRC=$(wildcard test/test_*.c)
TESTS_EXE=$(patsubst test/%.c,$(TEST_DIR)/%,$(TESTS_SRC))

main: $(CHALLENGES_EXE)

print-%  : ; @echo $* = $($*)

$(BUILD_DIR):
	mkdir -p $@

$(TEST_DIR):
	mkdir -p $@

test: $(TEST_DIR) $(TESTS_EXE)

run-tests : test
	@echo "\n============= BEGIN TESTS =============\n"
	@find $(TEST_DIR) -name "test*" -type file -print0 | xargs -0 -n1 -I% sh -c %

run-challenges : $(CHALLENGES_EXE)
	@echo "\n============= BEGIN CHALLENGES =============\n"
	@find $(BUILD_DIR) -name "Challenge-*" -type file -print0 | xargs -0 -n1 -I% sh -c %


lib: $(BUILD_DIR)/cryptolib.a

$(TEST_DIR)/% : test/%.c test/common.c $(BUILD_DIR)/cryptolib.a
	$(CC) $(CCOPTS) $(CFLAGS) $^ -o $@  $(LIBS) $(LDFLAGS) $(INCLUDES)

Challenge-%.exe : src/Challenges/Challenge-%.c $(BUILD_DIR)/cryptolib.a
	$(CC) $(CCOPTS) $(CFLAGS) $^ -o $@  $(LIBS) $(LDFLAGS) $(INCLUDES)

$(BUILD_DIR)/cryptolib.a: $(CRYPTOLIB_OBJ)
	 ar rcs $@ $^

$(BUILD_DIR)/%.o : src/cryptolib/%.c $(BUILD_DIR)
	$(CC) $(CCOPTS) $(CFLAGS) $< -c -o $@ $(INCLUDES)

clean:
	rm -rf $(BUILD_DIR)
	rm -rf $(TEST_DIR)

.PHONY: clean
