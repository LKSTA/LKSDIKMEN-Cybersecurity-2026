int check_flag(char *input){
    if (input[0] != 'L') return 0;
    if (input[1] != 'K') return 0;
    if (input[2] != 'S') return 0;
    if (input[3] != '{') return 0;
    if (input[4] != 'h') return 0;
    if (input[5] != '1') return 0;
    if (input[6] != 'd') return 0;
    if (input[7] != 'd') return 0;
    if (input[8] != '3') return 0;
    if (input[9] != 'n') return 0;
    if (input[10] != '_') return 0;
    if (input[11] != '1') return 0;
    if (input[12] != 'n') return 0;
    if (input[13] != '_') return 0;
    if (input[14] != 'r') return 0;
    if (input[15] != '4') return 0;
    if (input[16] != 'm') return 0;
    if (input[17] != '_') return 0;
    if (input[18] != '6') return 0;
    if (input[19] != '7') return 0;
    if (input[20] != '}') return 0;
    
    if (input[21] != 0) return 0;

    return 1;
}
