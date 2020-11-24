## 10000 запросов с балансировкой

```
$ ab -c 10 -n 10000 http://127.0.0.1/api/v1/articles/
This is ApacheBench, Version 2.3 <$Revision: 1843412 $>
Copyright 1996 Adam Twiss, Zeus Technology Ltd, http://www.zeustech.net/
Licensed to The Apache Software Foundation, http://www.apache.org/

Benchmarking 127.0.0.1 (be patient)
Completed 1000 requests
Completed 2000 requests
Completed 3000 requests
Completed 4000 requests
Completed 5000 requests
Completed 6000 requests
Completed 7000 requests
Completed 8000 requests
Completed 9000 requests
Completed 10000 requests
Finished 10000 requests


Server Software:        blog
Server Hostname:        127.0.0.1
Server Port:            80

Document Path:          /api/v1/articles/
Document Length:        8081 bytes

Concurrency Level:      10
Time taken for tests:   113.543 seconds
Complete requests:      10000
Failed requests:        0
Total transferred:      83790000 bytes
HTML transferred:       80810000 bytes
Requests per second:    88.07 [#/sec] (mean)
Time per request:       113.543 [ms] (mean)
Time per request:       11.354 [ms] (mean, across all concurrent requests)
Transfer rate:          720.66 [Kbytes/sec] received

Connection Times (ms)
              min  mean[+/-sd] median   max
Connect:        0    0   0.2      0      11
Processing:    14  113  95.6    112     649
Waiting:       14  113  95.6    112     648
Total:         14  113  95.6    112     649

Percentage of the requests served within a certain time (ms)
  50%    112
  66%    163
  75%    177
  80%    188
  90%    230
  95%    281
  98%    346
  99%    383
 100%    649 (longest request)
```

```
$ ab -c 10 -n 10000 http://127.0.0.1/api/v1/articles/1/
This is ApacheBench, Version 2.3 <$Revision: 1843412 $>
Copyright 1996 Adam Twiss, Zeus Technology Ltd, http://www.zeustech.net/
Licensed to The Apache Software Foundation, http://www.apache.org/

Benchmarking 127.0.0.1 (be patient)
Completed 1000 requests
Completed 2000 requests
Completed 3000 requests
Completed 4000 requests
Completed 5000 requests
Completed 6000 requests
Completed 7000 requests
Completed 8000 requests
Completed 9000 requests
Completed 10000 requests
Finished 10000 requests


Server Software:        blog
Server Hostname:        127.0.0.1
Server Port:            80

Document Path:          /api/v1/articles/1/
Document Length:        905 bytes

Concurrency Level:      10
Time taken for tests:   55.546 seconds
Complete requests:      10000
Failed requests:        0
Total transferred:      12160000 bytes
HTML transferred:       9050000 bytes
Requests per second:    180.03 [#/sec] (mean)
Time per request:       55.546 [ms] (mean)
Time per request:       5.555 [ms] (mean, across all concurrent requests)
Transfer rate:          213.79 [Kbytes/sec] received

Connection Times (ms)
              min  mean[+/-sd] median   max
Connect:        0   14 417.5      0   13192
Processing:     5   41  51.1     32    1033
Waiting:        5   41  51.1     32    1033
Total:          5   55 420.1     33   13263

Percentage of the requests served within a certain time (ms)
  50%     33
  66%     57
  75%     63
  80%     67
  90%     79
  95%     94
  98%    135
  99%    205
 100%  13263 (longest request)
```

## 10000 запросов без балансировки

```
$ ab -c 10 -n 10000 http://127.0.0.1/api/v1/articles/
This is ApacheBench, Version 2.3 <$Revision: 1843412 $>
Copyright 1996 Adam Twiss, Zeus Technology Ltd, http://www.zeustech.net/
Licensed to The Apache Software Foundation, http://www.apache.org/

Benchmarking 127.0.0.1 (be patient)
Completed 1000 requests
Completed 2000 requests
Completed 3000 requests
Completed 4000 requests
Completed 5000 requests
Completed 6000 requests
Completed 7000 requests
Completed 8000 requests
Completed 9000 requests
Completed 10000 requests
Finished 10000 requests


Server Software:        blog
Server Hostname:        127.0.0.1
Server Port:            80

Document Path:          /api/v1/articles/
Document Length:        8081 bytes

Concurrency Level:      10
Time taken for tests:   178.027 seconds
Complete requests:      10000
Failed requests:        0
Total transferred:      83650000 bytes
HTML transferred:       80810000 bytes
Requests per second:    56.17 [#/sec] (mean)
Time per request:       178.027 [ms] (mean)
Time per request:       17.803 [ms] (mean, across all concurrent requests)
Transfer rate:          458.86 [Kbytes/sec] received

Connection Times (ms)
              min  mean[+/-sd] median   max
Connect:        0    0   0.4      0      24
Processing:    53  178  43.9    169     551
Waiting:       52  178  43.9    169     551
Total:         53  178  43.9    169     551

Percentage of the requests served within a certain time (ms)
  50%    169
  66%    182
  75%    192
  80%    199
  90%    227
  95%    263
  98%    314
  99%    347
 100%    551 (longest request)
```

```
$ ab -c 10 -n 10000 http://127.0.0.1/api/v1/articles/1/
This is ApacheBench, Version 2.3 <$Revision: 1843412 $>
Copyright 1996 Adam Twiss, Zeus Technology Ltd, http://www.zeustech.net/
Licensed to The Apache Software Foundation, http://www.apache.org/

Benchmarking 127.0.0.1 (be patient)
Completed 1000 requests
Completed 2000 requests
Completed 3000 requests
Completed 4000 requests
Completed 5000 requests
Completed 6000 requests
Completed 7000 requests
Completed 8000 requests
Completed 9000 requests
Completed 10000 requests
Finished 10000 requests


Server Software:        blog
Server Hostname:        127.0.0.1
Server Port:            80

Document Path:          /api/v1/articles/1/
Document Length:        905 bytes

Concurrency Level:      10
Time taken for tests:   62.833 seconds
Complete requests:      10000
Failed requests:        0
Total transferred:      12020000 bytes
HTML transferred:       9050000 bytes
Requests per second:    159.15 [#/sec] (mean)
Time per request:       62.833 [ms] (mean)
Time per request:       6.283 [ms] (mean, across all concurrent requests)
Transfer rate:          186.82 [Kbytes/sec] received

Connection Times (ms)
              min  mean[+/-sd] median   max
Connect:        0    0   5.6      0     561
Processing:     7   62  30.0     57     627
Waiting:        6   62  29.9     57     627
Total:          7   63  30.5     57     627

Percentage of the requests served within a certain time (ms)
  50%     57
  66%     64
  75%     68
  80%     72
  90%     85
  95%    103
  98%    148
  99%    192
 100%    627 (longest request)
```
