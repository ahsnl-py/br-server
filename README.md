## Use Docker to run the application

### Create an Image: 
`smart-api % docker build -t br-serve-img`

### Create a container and run it
`docker run -d --name br-container -p 80:80 br-serve-img`
