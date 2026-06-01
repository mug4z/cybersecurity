#include <alloca.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
int main()
{
  char *fmt = "%23s";
  char tmp[24];
  char password[24] = "delabere";
  printf("Please enter key: ");
  scanf(fmt,tmp);
  if(tmp[0] == '0'){

    if(tmp[1] == '0'){
      fflush(stdin);
      int idx = 2;
      char str[9];
      int pos = 1;
      memset(str, 0, 9);
      str[0] = 'd';

      while(strlen(str) < 8 && idx < strlen(tmp) ){

        str[pos++] = atoi((char[4]){tmp[idx], tmp[idx + 1],tmp[idx + 2], '\0'});
        idx+=3;
      }
      printf("%s\n",strcmp(password, str) ? "Nope." : "Good job." );

    }
  }
}

// NOTE: Check le deuxieme character
//       Check le premier character
//
//   elabere 
// 00 101 108 097 098 101 114 101
// 00101108097098101114101
