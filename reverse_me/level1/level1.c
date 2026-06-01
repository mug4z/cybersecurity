
#include <stdio.h>
#include <string.h>
int main()
{
  const char *password = "__stack_check";
  char tmp[100];
  printf("Please enter key: ");
  scanf("%s",tmp);
  if(!strcmp(tmp, password))
    printf("Good job.\n");
  printf("Nope.\n");
  return 0;
}
