
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

Go

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
