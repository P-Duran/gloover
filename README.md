# Gloover

A sentiment analysis tool to monitorize products.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

See deployment for notes on how to deploy the project on a live system.

### Prerequisites

To install and run the project you will need the following:

* python
* Docker & Docker compose


### Installing

#### Clone

Clone this repo to your local machine: <https://github.com/P-Duran/gloover.git>

#### Setup on Windows

* Recomended IDE **Intellij**. Last version can be found [here](https://www.jetbrains.com/idea/download/).

```
    Install the **Python Community Edition** plugin
```
```
    Install **SonarLint** plugin
```

* Download & install **Docker Desktop**. Instructions can be found [here](https://docs.docker.com/docker-for-windows/install/).
  
* Make sure docker is running
  
* Open a terminal in the project's folder
  
* Start and build the project
```sh
$ docker-compose up --build
```

### Configure MongoDb
* Access mongodb container
```sh
$ docker exec -it mongo bash
```
* Once inside the container, log in to the MongoDB root administrative account

*Mongo admin ceredentials can be found here [here](docker-compose.yml)*
```sh
root@893759837:/# mongo -u root -p
```
* Create the gloover_db database
```sh
mongo> use gloover_db
```
* Next, create a new user that will be allowed to access this database

*Gloover app credentials can be found [here](docker-compose.yml)*
```sh
mongo> db.createUser({user: 'gloover_user', pwd: <password>, roles: [{role: 'readWrite', db: <user>}]})
mongo> exit
```
* Log in to the authenticated database:
```sh
$ mongo -u gloover_user -p password1 --authenticationDatabase gloover_db
mongo> exit
```

### Check that it's up and running
```
    GET  http://localhost:5000/info
```
The following response should be returned:
```
    {
        status=True,
        message='Server is running!'
    }
```


## Running the tests
Nothing here

## Contributing

Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct, and the process for submitting pull requests.

## Versioning


Nothing here


## Authoring

Made with <span style="color: #e25555;">&#9829;</span> by [**Pablo Durán**](https://github.com/P-Duran)
