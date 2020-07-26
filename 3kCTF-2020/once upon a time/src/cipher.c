/*
    Modified version of Matthew Darnell code
*/
#include <stdio.h>
#include <stdlib.h>
#include <memory.h>
#include <math.h>
#include <cipher.h>
#include "include/adder.h"

typedef enum {
    ECB = 0,
    CBC = 1,
    OFB = 2,
    CFB = 3
} MODE;

void xor(BIT *input_1, BIT *input_2, BIT *out)
{
    int i;
    for(i=0; i<8; i++){
        out[i] = input_1[i] ^ input_2[i];
    }
}

int encrypt_file(const char *file, struct lfsr *l_17, struct lfsr *l_25, const char *outfile, int *dMode, unsigned char initialization_vector)
{
    //File Manipulation
    FILE *inFile = fopen(file, "rb");
    if(inFile == NULL){
        fprintf(stderr, "Error Opening File For Reading <%s>\n", file);
        return -1;
    }
    FILE *oFile = fopen(outfile, "wb+");
    if(oFile == NULL){
        fprintf(stderr, "Error Opening File For Writing <%s>\n", outfile);
        fclose(inFile);
        return -2;
    }

    long lSize;
    unsigned char *buffer = NULL;
    size_t result;

    fseek (inFile , 0 , SEEK_END);
    lSize = ftell (inFile);
    rewind (inFile);

    buffer = (unsigned char*) malloc( sizeof(unsigned char) * lSize);
    if (buffer == NULL) {
        fprintf(stderr, "Memory Error While Reading File <%s>\n", file);
        return -3;
    }

    result = fread (buffer, sizeof(unsigned char), lSize, inFile);
    if (result != lSize) {
        fprintf(stderr, "Error reading File into Memory <%s>\n", file);
        return -4;
    }

    //Encryption
    BIT byte_17[8], byte_25[8];
    BIT carry = ZERO;
    BIT sumArray[8] = {ZERO, ZERO, ZERO, ZERO,ZERO, ZERO, ZERO, ZERO};

    int i;
    unsigned char temp_keystream,
                  temp_plaintext,
                  temp_ciphertext;

    /* MODES OF OPERATION:
        ECB: mode = 0
        CBC: 1
        OFB: 2
        CFB: 3
    */

    MODE _mode = *dMode;

    for(i=0; i<lSize; i++){
        get_next_byte(l_17, byte_17);
        get_next_byte(l_25, byte_25);
        sum_bytes(byte_17, byte_25, carry, sumArray, &carry);
        bit_array_to_unsigned_char(sumArray, &temp_keystream);
        memcpy(&temp_plaintext, buffer+i, sizeof(unsigned char));
        switch (_mode) {
          case ECB:
              temp_ciphertext = temp_keystream ^ temp_plaintext;
              break;
          case CBC:
              temp_plaintext ^= initialization_vector;
              temp_ciphertext = temp_keystream ^ temp_plaintext;
              initialization_vector = temp_ciphertext;
              break;
          case OFB:
              temp_ciphertext = temp_keystream ^ initialization_vector;
              initialization_vector = temp_ciphertext;
              temp_ciphertext ^= temp_plaintext;
              break;
          case CFB:
              temp_ciphertext = temp_keystream ^ initialization_vector;
              temp_ciphertext ^= temp_plaintext;
              initialization_vector = temp_ciphertext;
              break;
        }
        //Output the ciphertext to the File
        if(fwrite (&temp_ciphertext , sizeof(unsigned char), 1, oFile) < 1){
            fprintf(stderr, "Error Writing (%c) at index.(%d) to Output File <%s>, Aborting.\n", temp_ciphertext, i, outfile);
            return -5;
        }
    }
    fclose(inFile);
    fclose(oFile);
    return 0;
}



void bit_array_to_unsigned_char(BIT *bits, unsigned char *u8)
{
    memset(u8, 0, sizeof(unsigned char));
    int i;
    int8_t sum = 0;
    for(i=7; i>=0; i--){
        BIT lsb = bits[i];
        sum += lsb * pow(2, 7-i);
    }
    *u8 = sum;
}
