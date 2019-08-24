sudo docker build -t mediator-db .

sudo docker container stop mediator-container
sudo docker container rm mediator-container
sudo docker run -d --name mediator-container -p 5432:5432  mediator-db