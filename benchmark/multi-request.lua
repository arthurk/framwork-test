-- run `max_requests` number of requests per path

function init(args)
  counter = 1
  max_requests = 1000
  current_path = 1
  paths = {
    {path = "http://localhost:8000/articles", method = "POST", body = "{\"title\": \"new article\"}"},
    {path = "http://localhost:8000/articles/%s", method = "GET", body = nil},
    {path = "http://localhost:8000/articles/%s", method = "POST", body = "{\"title\": \"updated title\"}"},
    {path = "http://localhost:8000/articles/%s", method = "DELETE", body = nil},
  }
end

function request()
  method = paths[current_path]["method"]
  path = paths[current_path]["path"]:format(counter)
  body = paths[current_path]["body"]

  print(counter, method, path, body)

  counter = counter + 1
  if counter > max_requests then
    counter = 1
    if current_path == #paths then
      current_path = 1
    else
      current_path = current_path + 1
    end
  end

  return wrk.format(method, path, {}, body)
end
