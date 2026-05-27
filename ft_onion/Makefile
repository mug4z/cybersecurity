tor-browser:
	docker run -d -p 5800:5800 domistyle/tor-browser
up:
	docker compose up -d --build
down:
	docker compose down

hostname:
	docker exec ft_onion-ft_onion-1  cat /var/lib/tor/hidden_service/hostname

.PHONY: up down tor-browser hostname
