CC      := clang
CFLAGS  := -std=c11 -Wall -Wextra -Wpedantic -g
SRC     := $(wildcard src/*.c)
BIN     := build/db

.PHONY: all test clean

all: $(BIN)

$(BIN): $(SRC) $(wildcard src/*.h)
	@mkdir -p build
	$(CC) $(CFLAGS) $(SRC) -o $(BIN)

test: all
	python3 tests/run_tests.py

clean:
	rm -rf build *.db
