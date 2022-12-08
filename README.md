## Use Docker to run the application

### Run application
#### Create an Image from command line
`smart-api % docker build -t br-serve-img`

#### Create a container and run it
`docker run -d --name br-container -p 80:80 br-serve-img`

### Run Test
`pytest`
