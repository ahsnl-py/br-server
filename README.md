## Use Docker to run the application

### Clone and create an Image: 
`docker build -t br-serve-img .`

### Create a container and run it
`docker run -d --name br-container -p 80:80 br-serve-img`

### Run Test
`pytest`

## Code Behaviour
| Worker | TimeoutTest (s) | Request (s) | Concurrency (s) | TimeTest (s) | TimePerRequest-1 (ms) | TimePerRequest-2 (ms) | RPS  (s) |
| ------ | --------------- | ----------- | --------------- | ------------ | ---------------- | ----------------- | -------- |
| 1      | Default (30)    | 100         | 10              | 43.345       | 4334.490         | 433.449           | 2.31000  |
| 1      | Default (30)    | 400         | 40              | 174.340      | 17433.990        | 435.850           | 2.29000  |
| 1      | Default (30)    | 800         | 1               | 330.838      | 413.547          | 413.547           | 2.42000  |
| 1      | Default (30)    | 800         | 40              | 320.302      | 16015.082        | 400.377           | 2.50000  |
| 1      | Default (30)    | 800         | 80              | 321.508      | 32150.837        | 401.885           | 2.49000  |
| 1      | Default (30)    | 1000        | 100             | 59.155       | 58569.481        | 585.695           | 1.71000  |
| 1      | 60              | 1000        | 200             | 400.302      | 80060.489        | 400.302           | 2.50000  |
| 1      | 60              | 1600        | 160             | 652.000      | 65200.019        | 407.500           | 2.45000  |
| 4      | Default (30)    | 100         | 10              | 13.779       | 1377.883         | 137.788           | 7.26000  |
| 4      | Default (30)    | 400         | 40              | 64.651       | 6465.143         | 161.629           | 6.19000  |
| 4      | Default (30)    | 800         | 80              | 113.902      | 11390.160        | 142.377           | 7.02000  |
| 4      | Default (30)    | 1000        | 200             | 153.199      | 30639.731        | 153.199           | 6.53000  |
| 4      | Default (30)    | 2400        | 300             | 353.633      | 44204.180        | 147.347           | 6.79000  |

The load test of the server application was done with [ApacheBenchmark](https://httpd.apache.org/docs/2.4/programs/ab.html). The server was hosted locally using a docker container. So, connection time on average is almost 0. On the other hand, the Timeout test is the `ab` timeout default value which is 30 seconds. RPS is the Request per seconds which measures the throughput of the server. I have set no worker for the first benchmark testing. This is to get an idea how single threaded proxy handle heavy load request. As we could see that the as we increase the concurrency value the average time taken for request also increase significantly. This is also proven by the signigicant jump of time taken per request for two consecutive test of 1000  requests (1 worker) at 100 and 200 each concurrently, it takes **59** to **400** seconds to complete respectively. Still, request per second remain comparatively reasonable, averaging 2,3 s regardless of increasing load. 

In summary, there is a definite correlation between increasing of thread worker and RPS. For each worker increase, the RPS increase by 1-2 seconds. The most intersting finding is how the average `Time per request-2` which is account for the number of concurrent connections remain relatively stable during heavy load work. We could use this information to handle high traffic of request during a busy session of the application by increasing the number of workers and reduce back to normal when traffic is normal. In addition, looking at the resource of my OS during the test, it seems under heavy load, the CPU and memory only spike during the final termination of each concurrent request and remain stable if not request is terminated or reaches timeout. Ideally speaking, it would be better to test the server remotely and having a second remote connection in private network where I could measure the latency such as connection time (it was measured 0 across different config) and all the necessary load without the effect of local hardware resources allocation. For now, I could limit my core up to 4 worker. Each worker can only handle 100 concurrent request per thread before the server side application completely shutdown. 
