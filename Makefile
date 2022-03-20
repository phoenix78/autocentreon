include docker.ini

all: build start

build:
	$(info Make: Building environment images.)
	@TAG=$(TAG) docker-compose build --no-cache
 
start:
	$(info Make: Starting environment containers.)
	@TAG=$(TAG) docker-compose $(COMPOSE_FILE_PATH) up -d
 
stop:
	$(info Make: Stopping "$(ENV)" environment containers.)
	@docker-compose stop
 
restart:
	$(info Make: Restarting "$(ENV)" environment containers.)
	@make -s stop
	@make -s start
 
clean:
	@docker system prune --volumes --force
 
login:
	$(info Make: Login to Docker Hub.)
	@docker login -u $(DOCKER_USER) -p $(DOCKER_PASS)