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

Clone this repo to your local machine: <https://github.com/P-Duran/sentiment_analysis.git>

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
  
* Open a terminal
  
* Build the project
```sh
$ docker-compose build
```
* Start the project
```sh
$ docker-compose up
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

We use [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://gitlab.local.corunet.com/jlopez/mntee/-/tags).


## Authoring

Made with <span style="color: #e25555;">&#9829;</span> by [**Pablo Durán**](https://github.com/P-Duran)
