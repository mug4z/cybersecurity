#include <stdio.h>
#include <stdlib.h>
#include <string.h>

void wt(){
  printf("********");
}
void nice(){
  printf("nice");
}

void try(){
  printf("try");
}

void but(){
  printf("but");
}

void this(){
  printf("this");
}

void it(){
  printf("it");
}

void not(){
  printf("not");
}

void that(){
  printf("that");
}

void easy(){
  printf("easy");
}

int main()
{
  char *fmt = "%23s";
  char tmp[24];
  char password[24] = "********";
  printf("Please enter key: ");
  scanf(fmt, tmp); 

  // ********
  // 42042042042042042042042
  // 42042042042042042042042

  if (tmp[1] == '2') {
    if (tmp[0] == '4') {

      fflush(stdin);
      int idx = 2;
      char str[9];
      int pos = 1;
      memset(str, 0, 9);
      str[0] = '*';

      while(strlen(str) < 8 && idx < strlen(tmp) ){

        str[pos++] = atoi((char[4]){tmp[idx], tmp[idx + 1],tmp[idx + 2], '\0'});
        idx+=3;
      }
      printf("%s\n",strcmp(password, str) ? "Nope." : "Good job." );
      exit(1);

    }
  }
  printf("Nope.\n");

}
