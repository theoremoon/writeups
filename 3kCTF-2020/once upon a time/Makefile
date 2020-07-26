CC ?= gcc make
CFLAGS = -Wall -O3
DEFS =
INCLUDES = -Isrc -Isrc/include
LIBS = -lm
TARGET = scss
SRCS =	src/main.c \
        src/lfsr.c \
		src/adder.c \
		src/cipher.c

all: $(SRCS)
	 $(CC) $(CFLAGS) $(DEFS) $(INCLUDES) $(SRCS) $(LIBS) -o $(TARGET)

clean:
	rm $(TARGET)
