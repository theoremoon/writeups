/*
    Modified version of Matthew Darnell code
*/
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <lfsr.h>
#include <cipher.h>

int main(int argc, char *argv[])
{
    if(argc < 5){
        fprintf(stderr, "Usage:\n./scss </path/to/plaintext> </path/to/output-encrypted> <encrypt> <mode>\nValid Modes: [ecb, cbc, ofb, cfb]\n");
        return -1;
    }

    const char  *inputFile   = argv[1],
                *outputFile  = argv[2],
                *operation   = argv[3],
                *mode        = argv[4];

    if(strcmp(operation, "encrypt") != 0) {
      fprintf(stderr, "Invalid Operation. Valid Modes: [encrypt]\n");
      return -2;
    }

    if(strcmp(mode, "ecb") != 0 && strcmp(mode, "cbc") != 0 && strcmp(mode, "ofb") != 0 && strcmp(mode, "cfb") != 0) {
      fprintf(stderr, "Invalid Mode. Valid Modes: [ecb, cbc, ofb, cfb]\n");
      return -3;
    }

    int dMode = 0; //default ecb
    if(strcmp(mode, "cbc") == 0){
      dMode = 1;
    }
    else if(strcmp(mode, "ofb") == 0){
      dMode = 2;
    }
    else if(strcmp(mode, "cfb") == 0){
      dMode = 3;
    }
    struct lfsr l_17, l_25;
    int num_bits_1 = 17,
    num_bits_2 = 25;
    int taps_1[17] = { 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1 }, //x^17 + x^2 + 1
    taps_2[25] = { 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 1 }; //x^25 + x^21 + x^20 + x^10 + 1
    setup_lfsr(&l_17, &num_bits_1, taps_1);
    setup_lfsr(&l_25, &num_bits_2, taps_2);

    //Some random 40-bit Key
    // TODO: redact key

    BYTE key[40] = {0};


    //some i.v.
    unsigned char initialization_vector = 0xa2;


    struct lfsr *init_arr[2] = { &l_17, &l_25 };
    init_with_key(init_arr, 2, key);
    encrypt_file(inputFile, &l_17, &l_25, outputFile, &dMode, initialization_vector);

    return 0;
}
