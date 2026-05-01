NAME: spider

# gcc -Wall -Werror -Wextra main.c -L/home/tfrily/.brew/lib -lcurl -o test_curlOD


spider-build:
	docker build -t spider -f ./docker/Dockerfile . 
spider-run:
	docker run -it --name spider -v ./src/:/spider spider:latest

.PHONY: spider 

