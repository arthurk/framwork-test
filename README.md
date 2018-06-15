
Implementation of the same project in different languages/frameworks.

A simple REST API that retrieves, creates, updates and deletes articles.

Article Resource Schema:
- id (int)
- title (string) required
- created (string: datetime in ISO8601 format)
- status (string: created, deleted)

The REST API should have the following Routes:

- GET /articles -> List all articles
- GET /articles/{id} -> Article details
- POST /articles -> create new article
- POST /articles/{id} -> update
- DELETE /articles/{id} -> delete

Notes:
- Exclude deleted articles
- Requests that modify data need to have authentication
- Make sure to return different error codes e.g. 400/404/405
- Creating an article should auto-increment the id
- Datetime should exclude microseconds
- Initial data with 3 articles should be available

Benchmarks
----------

Apistar with Python 3.6

```
➤ wrk -d20s -t10 -c200 http://localhost:8000/articles
Running 20s test @ http://localhost:8000/articles
  10 threads and 200 connections
  Thread Stats   Avg      Stdev     Max   +/- Stdev
    Latency    67.23ms    8.62ms  94.21ms   85.43%
    Req/Sec   184.58     85.45   370.00     64.98%
  4749 requests in 20.09s, 1.35MB read
  Socket errors: connect 0, read 197, write 0, timeout 0
Requests/sec:    236.36
Transfer/sec:     68.78KB
```

Apistar + Python 3.6 + Gunicorn + Meinheld

```
➤ wrk -d20s -t10 -c200 http://localhost:8000/articles
Running 20s test @ http://localhost:8000/articles
  10 threads and 200 connections
  Thread Stats   Avg      Stdev     Max   +/- Stdev
    Latency    15.89ms    2.75ms 155.59ms   95.06%
    Req/Sec     1.25k   100.27     2.48k    95.94%
  249003 requests in 20.02s, 73.14MB read
Requests/sec:  12436.50
Transfer/sec:      3.65MB
```

Apistar with PyPy 6.0

```
➤ wrk -d20s -t10 -c200 http://localhost:8000/articles
Running 20s test @ http://localhost:8000/articles
  10 threads and 200 connections
  Thread Stats   Avg      Stdev     Max   +/- Stdev
    Latency    91.63ms   62.66ms 271.72ms   60.46%
    Req/Sec    78.64     56.65   303.00     65.05%
  4722 requests in 20.10s, 1.34MB read
  Socket errors: connect 0, read 222, write 0, timeout 0
Requests/sec:    234.91
Transfer/sec:     68.36KB
```

Go stdlib

```
➤ wrk -d20s -t10 -c200 http://localhost:8000/articles
Running 20s test @ http://localhost:8000/articles
  10 threads and 200 connections
  Thread Stats   Avg      Stdev     Max   +/- Stdev
    Latency     6.11ms    2.05ms  26.60ms   87.45%
    Req/Sec     3.29k   149.80     4.02k    74.20%
  658107 requests in 20.10s, 182.01MB read
  Socket errors: connect 0, read 42, write 0, timeout 0
Requests/sec:  32737.06
Transfer/sec:      9.05MB
```

Python 3.6 + aiohttp

```
➤ wrk -d20s -t10 -c200 http://localhost:8000/articles
Running 20s test @ http://localhost:8000/articles
  10 threads and 200 connections
  Thread Stats   Avg      Stdev     Max   +/- Stdev
    Latency    52.06ms    3.23ms 101.00ms   78.33%
    Req/Sec   384.99     29.57   727.00     85.35%
  76777 requests in 20.08s, 29.95MB read
  Socket errors: connect 0, read 120, write 0, timeout 0
Requests/sec:   3822.67
Transfer/sec:      1.49MB
```

Python 3.6 + aiohttp + Gunicorn (aiohttp.GunicornWebWorker)

```
Running 20s test @ http://localhost:8000/articles
  10 threads and 200 connections
  Thread Stats   Avg      Stdev     Max   +/- Stdev
    Latency    38.80ms    3.75ms 100.60ms   87.65%
    Req/Sec   516.84     68.94   790.00     58.43%
  103175 requests in 20.10s, 15.55MB read
  Socket errors: connect 0, read 121, write 0, timeout 0
Requests/sec:   5132.94
Transfer/sec:    792.02KB
```


Python 3.6 + aiohttp + Gunicorn (aiohttp.GunicornUVLoopWebWorker)

```
➤ wrk -d20s -t10 -c200 http://localhost:8000/articles
Running 20s test @ http://localhost:8000/articles
  10 threads and 200 connections
  Thread Stats   Avg      Stdev     Max   +/- Stdev
    Latency    29.56ms   10.48ms  70.62ms   58.78%
    Req/Sec   675.60     80.06     0.87k    70.35%
  134549 requests in 20.02s, 20.27MB read
  Socket errors: connect 0, read 133, write 0, timeout 0
Requests/sec:   6721.69
Transfer/sec:      1.01MB
```
