NAME: spider

gcc -Wall -Werror -Wextra main.c -L/home/tfrily/.brew/lib -lcurl -o test_curlOD

all:			$(LIBS) $(NAME)

$(name):	$(objs)
			$(cc) $(cflags) $(objs) $(link_libs) -o $@
			@printf "created executable: $(green)$(name)$(reset)\n"
%.o:	%.c 
				$(CC) $(CFLAGS) $(DFLAGS) $(DEP_FILE) $(INCLUDES) -c $< -o $@

.PHONY: all clean fclean re debug cleanLibs cleanLogs

