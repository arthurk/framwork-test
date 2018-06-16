
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

All benchmarks with Python 3.6
cmd `$ wrk -d20s -t10 -c200 http://localhost:8000/articles`

### apistar

```
# Built-in server
Running 20s test @ http://localhost:8000/articles
  10 threads and 200 connections
  Thread Stats   Avg      Stdev     Max   +/- Stdev
    Latency    63.98ms    9.21ms  92.91ms   88.35%
    Req/Sec   186.19     97.98   400.00     61.66%
  4764 requests in 20.04s, 1.70MB read
  Socket errors: connect 0, read 192, write 0, timeout 0
Requests/sec:    237.78
Transfer/sec:     87.08KB

# Gunicorn
$ pipenv run gunicorn app:app
Running 20s test @ http://localhost:8000/articles
  10 threads and 200 connections
  Thread Stats   Avg      Stdev     Max   +/- Stdev
    Latency   105.37ms   12.16ms 122.94ms   95.96%
    Req/Sec   116.62     43.37   200.00     60.36%
  4605 requests in 20.10s, 1.67MB read
  Socket errors: connect 0, read 357, write 0, timeout 0
Requests/sec:    229.07
Transfer/sec:     85.23KB

# Gunicorn + Meinheld
$ pipenv run gunicorn app:app --worker-class="egg:meinheld#gunicorn_worker"
Running 20s test @ http://localhost:8000/articles
  10 threads and 200 connections
  Thread Stats   Avg      Stdev     Max   +/- Stdev
    Latency    16.41ms    2.86ms 146.08ms   97.55%
    Req/Sec     1.23k    58.04     1.57k    83.90%
  244771 requests in 20.04s, 89.87MB read
  Socket errors: connect 0, read 103, write 0, timeout 0
Requests/sec:  12215.75
Transfer/sec:      4.49MB
```

##### ASyncApp
```
# app.serve
Running 20s test @ http://localhost:8000/articles
  10 threads and 200 connections
  Thread Stats   Avg      Stdev     Max   +/- Stdev
    Latency     1.34ms    1.76ms   8.15ms   88.43%
    Req/Sec   101.18    199.43   535.00     81.82%
  121 requests in 20.01s, 44.31KB read
Requests/sec:      6.05
Transfer/sec:      2.21KB

# uvicorn
$ pipenv run uvicorn app:app
Running 20s test @ http://localhost:8000/articles
  10 threads and 200 connections
  Thread Stats   Avg      Stdev     Max   +/- Stdev
    Latency    21.67ms    7.78ms  66.69ms   65.02%
    Req/Sec     0.93k    98.14     1.19k    72.36%
  185254 requests in 20.09s, 62.54MB read
  Socket errors: connect 0, read 83, write 0, timeout 0
Requests/sec:   9222.12
Transfer/sec:      3.11MB

# daphne
$ pipenv run daphne app:app
Running 20s test @ http://localhost:8000/articles
  10 threads and 200 connections
  Thread Stats   Avg      Stdev     Max   +/- Stdev
    Latency   149.25ms   40.05ms 268.05ms   67.29%
    Req/Sec   121.09     42.48   280.00     68.64%
  24209 requests in 20.10s, 6.93MB read
  Socket errors: connect 0, read 374, write 0, timeout 0
Requests/sec:   1204.29
Transfer/sec:    352.82KB
```


### Go + gorilla mux

```
$ wrk -d20s -t10 -c200 http://localhost:8000/articles
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

### aiohttp

```
$ wrk -d20s -t10 -c200 http://localhost:8000/articles
Running 20s test @ http://localhost:8000/articles
  10 threads and 200 connections
  Thread Stats   Avg      Stdev     Max   +/- Stdev
    Latency    39.58ms    3.32ms  94.33ms   85.10%
    Req/Sec   507.09     68.58   760.00     58.74%
  101242 requests in 20.10s, 39.49MB read
  Socket errors: connect 0, read 62, write 0, timeout 0
Requests/sec:   5036.81
Transfer/sec:      1.96MB

# Gunicorn (aiohttp.GunicornWebWorker)
$ pipenv run gunicorn app:app --worker-class aiohttp.GunicornWebWorker
Running 20s test @ http://localhost:8000/articles
  10 threads and 200 connections
  Thread Stats   Avg      Stdev     Max   +/- Stdev
    Latency    39.46ms    3.35ms  77.94ms   90.59%
    Req/Sec   508.58     66.43   606.00     64.01%
  101492 requests in 20.08s, 39.59MB read
  Socket errors: connect 0, read 59, write 0, timeout 0
Requests/sec:   5053.40
Transfer/sec:      1.97MB

# Gunicorn (aiohttp.GunicornUVLoopWebWorker)
➤ pipenv run gunicorn app:app --worker-class aiohttp.GunicornUVLoopWebWorker
Running 20s test @ http://localhost:8000/articles
  10 threads and 200 connections
  Thread Stats   Avg      Stdev     Max   +/- Stdev
    Latency    30.17ms   10.76ms  90.47ms   62.66%
    Req/Sec   665.82     91.66     0.92k    70.61%
  132738 requests in 20.04s, 51.77MB read
  Socket errors: connect 0, read 66, write 0, timeout 0
Requests/sec:   6622.75
Transfer/sec:      2.58MB
```

### quart

```
# hypercorn-h11
$ pipenv run app.py
Running 20s test @ http://localhost:8000/articles
  10 threads and 200 connections
  Thread Stats   Avg      Stdev     Max   +/- Stdev
    Latency   206.62ms   11.27ms 383.00ms   92.86%
    Req/Sec    96.44     52.92   200.00     60.36%
  19298 requests in 20.10s, 6.59MB read
  Socket errors: connect 0, read 116, write 0, timeout 0
Requests/sec:    960.29
Transfer/sec:    335.73KB

# uvicorn
$ pipenv run uvicorn app:app
Running 20s test @ http://localhost:8000/articles
  10 threads and 200 connections
  Thread Stats   Avg      Stdev     Max   +/- Stdev
    Latency   110.43ms   67.73ms 315.18ms   83.87%
    Req/Sec   216.81     83.22   380.00     68.82%
  39012 requests in 20.10s, 13.17MB read
  Socket errors: connect 0, read 83, write 0, timeout 0
Requests/sec:   1941.08
Transfer/sec:    671.04KB

# gunicorn
$ gunicorn --worker-class quart.worker.GunicornWorker app:app
Running 20s test @ http://localhost:8000/
  10 threads and 200 connections
  Thread Stats   Avg      Stdev     Max   +/- Stdev
    Latency   215.47ms   32.36ms 325.33ms   79.76%
    Req/Sec    91.82     56.57   202.00     56.95%
  18059 requests in 20.06s, 3.89MB read
  Socket errors: connect 0, read 185, write 0, timeout 0
  Non-2xx or 3xx responses: 18059
Requests/sec:    900.47
Transfer/sec:    198.75KB

# hypercorn
$ pipenv run hypercorn app:app -b 0.0.0.0:8000
Running 20s test @ http://localhost:8000/
  10 threads and 200 connections
  Thread Stats   Avg      Stdev     Max   +/- Stdev
    Latency   167.63ms   24.68ms 309.61ms   75.80%
    Req/Sec   114.99     48.89   202.00     65.09%
  22951 requests in 20.09s, 4.95MB read
  Socket errors: connect 0, read 181, write 0, timeout 0
  Non-2xx or 3xx responses: 22951
Requests/sec:   1142.57
Transfer/sec:    252.18KB
```
