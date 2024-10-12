# Library Management Microservice

This project is a library management system developed using microservices architecture. 

### The project consists of four main microservices:

* User Service: User management.
* Book Service: Book management.
* Loan Service: Borrowing and return processes.
* Inventory Service: Inventory control.

Communication between services is provided by an event-driven architecture over Kafka. All services use a common MySQL database and are managed with Docker Compose.

### Technologies Used
* FastAPI: High-performance web framework.
* SQLAlchemy: SQL toolkit and ORM for Python.
* Kafka: Distributed event streaming platform.
* Docker & Docker Compose: Containerization and multi-container management.
* MySQL: Relational database management system.
* Pydantic: Used for data validation and tuning.


This project can be build by simply running this command:

```
docker-compose up --build -d
```
![alt text](image.png)

1. After that you can create user with this command on Postman or from your terminal.

```
curl -X POST "http://localhost:8003/users" -H "Content-Type: application/json" -d '{
    "full_name": "Full Name",
    "email": "full.name@example.com",
    "age": 30
}'
```


2. Also you can create book with this command

```
curl -X POST "http://localhost:8000/books" -H "Content-Type: application/json" -d '{
    "id": 1,
    "title": "New Book",
    "author": "Author Name",
    "published_year": 2023
}'
```

3. Check the database
```
docker exec -it mysql bash
mysql -u root -p
USE library_db
```

* Inventory default quantity is 10

![alt text](image-1.png)

4. Loan the book with this command:

```
curl -X POST "http://localhost:8001/loans" -H "Content-Type: application/json" -d '{
    "user_id": 5,
    "book_id": 1
}'
```
![alt text](image-2.png)

* Inventory decreased 1!

![alt text](image-3.png)

5. Return the book with this command

```
curl -X PUT "http://localhost:8001/loans/4/return"
```


![alt text](image-4.png)


6. Let's check logs of this process

```
docker-compose logs -f inventory-service
```

![alt text](image-5.png)



```
docker-compose logs -f loan-service
```
![alt text](image-7.png)

![alt text](image-8.png)