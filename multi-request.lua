local counter = 1
local threads = {}
--local article_location = ""

function setup(thread)
  thread:set("id", counter)
  table.insert(threads, thread)
end

function init(args)
  st = {}
  pipeline = {
    {path = "http://localhost:8000/articles", method = "POST", body = "{\"title\": \"new article\"}"},
    {path = "http://localhost:8000/%s", method = "GET", body = nil},
    {path = "http://localhost:8000/%s", method = "POST", body = "{\"title\": \"updated title\"}"},
    {path = "http://localhost:8000/%s", method = "DELETE", body = nil},
  }
end

function request()
  -- skip first run because response() isn't called, messing up the pipeline
  if article_location == nil then
    article_location = ""
    return wrk.format('GET', 'http://localhost:8000/articles')
  end

  method = pipeline[counter]["method"]
  path = pipeline[counter]["path"]:format(article_location)
  body = pipeline[counter]["body"]

  counter = counter + 1
  if counter > #pipeline then
    counter = 1
  end

  return wrk.format(method, path, {}, body)
end

function response(status, headers, body)
  -- save the location header of the request (to be used in the next requests)
  if status == 201 then
    article_location = headers["location"]:sub(2)
  end

  -- track status codes
  if st[status] == nil then
     st[status] = 0
  end
  st[status] = st[status] + 1
end

function done(summary, latency, requests)
  -- print summary of status codes
  for index, thread in ipairs(threads) do
    print("**********************************")
    local ss = thread:get("st")
    for s, n in pairs(ss) do
      msg = "status %d: %d"
      print(msg:format(s, n))
    end
  end
end
