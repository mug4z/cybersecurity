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

void ___syscall_malloc(){
  printf("Nope\n");

}

void ____syscall_malloc(){
  printf("Good Job\n");
}
int main()
{
  char *fmt = "%23s";
  char tmp[24];
  char password[24] = "********";
  printf("Please enter key: ");
  if (scanf("%23s", tmp) != 1 || tmp[1] != '2' || tmp[0] != '4') {
        ___syscall_malloc();
        return (0);
    }
  
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
      switch (strcmp(str, password)) {
          case (0):
              ____syscall_malloc();
              break;
          case (-2):
          case (-1):
          case (1):
          case (2):
          case (3):
          case (4):
          case (5):
          case (115):
          default:
              ___syscall_malloc();
      }
    }
  }
  return (0);
}
