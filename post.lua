-- for testing POST requests with wrk
-- wrk -d20s -t10 -c200 -s post.lua http://localhost:8000/articles

wrk.method = "POST"
wrk.body   = "{\"title\": \"123\"}"
wrk.headers["Content-Type"] = "application/json"
