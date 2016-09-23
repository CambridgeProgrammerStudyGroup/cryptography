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
CHALLENGES_EXE=$(patsubst src/Challenges/%.c,$(BUILD_DIR)/%.exe,$(CHALLENGES_SRC))

TESTS_SRC=$(wildcard test/test_*.c)
TESTS_EXE=$(patsubst test/%.c,$(TEST_DIR)/%,$(TESTS_SRC))

main: run-tests run-challenges

print-%  : ; @echo $* = $($*)

$(BUILD_DIR):
	mkdir -p $@

$(TEST_DIR):
	mkdir -p $@

tests: $(TEST_DIR) $(TESTS_EXE)

test : tests
	@echo "\n============= BEGIN TESTS =============\n"
	@find $(TEST_DIR) -name "test*" -type file -print0 | xargs -0 -n1 -I% sh -c "% && echo ''"
	@echo "\n============= END TESTS =============\n"

challenges : $(CHALLENGES_EXE)
	@echo "\n============= BEGIN CHALLENGES =============\n"
	@find $(BUILD_DIR) -name "Challenge-*" -type file -print0 | xargs -0 -n1 -I% sh -c "% && echo ''"
	@echo "\n============= END CHALLENGES =============\n"

lib: $(BUILD_DIR)/cryptolib.a

$(TEST_DIR)/% : test/%.c test/common.c $(BUILD_DIR)/cryptolib.a
	$(CC) $(CCOPTS) $(CFLAGS) $^ -o $@  $(LIBS) $(LDFLAGS) $(INCLUDES)

$(BUILD_DIR)/Challenge-%.exe : src/Challenges/Challenge-%.c test/common.c $(BUILD_DIR)/cryptolib.a
	$(CC) $(CCOPTS) $(CFLAGS) $^ -o $@  $(LIBS) $(LDFLAGS) $(INCLUDES)

$(BUILD_DIR)/cryptolib.a: $(CRYPTOLIB_OBJ)
	 ar rcs $@ $^

$(BUILD_DIR)/%.o : src/cryptolib/%.c $(BUILD_DIR)
	$(CC) $(CCOPTS) $(CFLAGS) $< -c -o $@ $(INCLUDES)

clean:
	rm -rf $(BUILD_DIR)
	rm -rf $(TEST_DIR)

.PHONY: clean
