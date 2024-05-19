# Host Web Flask App locally and on EC2

## Getting Started
Follow these instructions to get a copy of the project up and running on your local machine for development and testing purposes.

#### Prerequisites
If you want to install locally:

- Install docker and docker-compose

If you want to host on AWS:

- Need AWS account

#### Installation locally 
1. **Clone the repository**
2. **Navigate into the project directory**
3. **Create .env and .env-mongo files for MongoDb authentication**

  ##### **.env example**
  ```
  MONGO_USER=flask_user
  MONGO_PASSWORD=flask_password
  MONGO_DB=flask_database

  #Admin creds
  MONGO_ADMIN_USER=admin
  MONGO_ADMIN_EMAIL=admin@mail.com
  MONGO_ADMIN_PASS=1111
  ```

  ##### .env-mongo example
  ```
  MONGO_INITDB_ROOT_USERNAME=rootUsername
  MONGO_INITDB_ROOT_PASSWORD=rootPassword
  MONGO_INITDB_DATABASE=admin
  ```
4. **Start up the docker-compose**
  ```
  docker compose up
  ```
5. **After the application starts, navigate to https://localhost**

**To rebuild container:**
  ```
  docker-compose up -d --build
  ```

6. **Stop and remove containers**
  ```
  docker compose down
  ```
 
7. **NGINX as a reverse-proxy (now works with self signed cert):**
  ```
  https://localhost
  ```
#### Installation on EC2 AWS

1. **Stored your MongoDB credentials on AWS Secret Manager**

   Set secret names as follows:

   .env (for Flask App)

   .env-mongo (root user for MongoDB)
    
3. **Build EC2 with CloudFormation using e2.yaml file**
4. **Connect to EC2 and navigate into the project directory**
5. **Start up the docker-compose to generate your certificates**

   docker-compose -f docker-compose-cert.yml up --build
7. **Navigate to the folder with your certificates, copy them, and paste them into AWS Secret Manager**

    /etc/letsencrypt/live/<domain> - path to your secrets
   
   Set secret names as follows:
   
   prod/flaskapp for privkey.pem

   prod/flaskapp2 for fullchain.pem
8. **Run python script**

   python3 get_cred.py

9. **Restart docker-compose**
   
   docker-compose --file docker-compose.yml down
   
   docker-compose --file docker-compose.yml build
   
   docker-compose --file docker-compose.yml up

10. **Please note you should update DNS name with your new IP address**
11. **Your App is now available with chosen domain name** 
  
## Swagger
**Uses route /docs by default**

Example URL
```
 http://localhost/docs
```
**You can use Swagger UI to test your endpoints**

Swagger OpenAPI file location
```
~/backend/static/swagger.json
```
**Modify this file if you do some changes in any declared endpoints**
