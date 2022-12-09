## Use Docker to run the application

### Create an Image: 
`smart-api % docker build -t br-serve-img`

### Create a container and run it
`docker run -d --name br-container -p 80:80 br-serve-img`

## Code Behaviour
| TimeoutTest (s) | Request (s) | Concurrency (s) | TimeTest (s) | RPS  (s) |
| --------------- | ----------- | --------------- | ------------ | -------- |
| Default (30)    | 100         | 10              | 43.345       | 2,31     |
| Default (30)    | 400         | 40              | 174.340      | 2,29     |
| Default (30)    | 800         | 1               | 330.838      | 2,42     |
| Default (30)    | 800         | 40              | 320.302      | 2,50     |
| Default (30)    | 800         | 80              | 321.508      | 2,49     |
| Default (30)    | 1000        | 100             | 59.155       | 1,71     |
| 60              | 1000        | 200             | 400.302      | 2,50     |
| 60              | 1600        | 160             | 652.000      | 2,45     |

The load test of the server application was done with [ApacheBenchmark](https://httpd.apache.org/docs/2.4/programs/ab.html). The server was hosted locally using a docker container. So, connection time on average is almost 0. On the other hand, the Timeout test is the `ab` timeout default value which is 30 seconds. RPS is the Request per seconds which could indicate how fast each request take for each per visitor. In this case, from the results above, we could see that the increase value of con-currency request per seconds remains stable although the test took comparatively longer after each concurrent request increases. This could be the case with the default timeout set on the server app itself. For each timeout, another request is fire up to three attempts. In addition, I must increase the default timeout for `ab` in order to be able to pass the 100 concurrent requests. Still, request remain comparatively reasonable, averaging 2,3 s regardless of increasing load. 

In conclusion, after passing the default connection timeout for `ab` (Default 30 seconds), it seems the benchmark for this application server is set to be around a *100 con-current request per seconds* before receiving timeout from `ab`. It could be the API call from EXPONEA is so unstable that I could not even do a normal testing under normal condition. Looking at the resource of my OS during the test, it seems under heavy load, the CPU and memory usage remain stable. Ideally speaking, it would be better to test the server remotely and having a second remote connection in private network where I could measure the latency such as connection time (it was measured 0 across different config) and all the necessary load without the effect of local hardware resources allocation. 
