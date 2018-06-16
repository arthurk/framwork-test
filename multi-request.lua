local counter = 1
local threads = {}

function setup(thread)
   thread:set("id", counter)
   table.insert(threads, thread)
   counter = counter + 1
end

pipeline = {
    {path = "http://localhost:8000/articles", method = "POST", body = "{\"title\": \"this is a new article\"}"},
    -- {path = "http://localhost:8000/articles/%s", method = "DELETE", body = nil},
}

global_counter = 1

function init(args)
  st = {}
end

request = function()
  method = pipeline[counter]["method"]
  url_path = pipeline[counter]["path"]:format(global_counter)
  body = pipeline[counter]["body"]

  counter = counter + 1

  if counter > #pipeline then
    counter = 1
  end

  global_counter = global_counter + 1

  return wrk.format(method, url_path, {}, body)
end

function response(status, headers, body)
  if st[status] == nil then
     st[status] = 0
  end
  st[status] = st[status] + 1
end

function done(summary, latency, requests)
  for index, thread in ipairs(threads) do
    print("**********************************")
    local ss =  thread:get("st")
    for s, n in pairs(ss) do
      msg = "%d: %d"
      print(msg:format(n,s))
    end
  end
end
