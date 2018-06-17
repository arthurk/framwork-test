import http from "k6/http";
import { check, group } from "k6";

const baseUrl = "http://0.0.0.0:8000";

export default function() {
  // Create a new article
  var url = `${baseUrl}/articles`;
  var payload = JSON.stringify({title: "article"});
  var res = http.post(url, payload);
  check(res, {
    "status was 201": (r) => r.status === 201,
    "location header is set": (r) => 'Location' in r.headers
  });

  // url of the article needed for further tests
  var location = baseUrl + res.headers['Location'];

  // Get article details -> check title
  res = http.get(location);
  check(res, {
    "status was 200": (r) => r.status === 200,
    "title was correct": (r) => r.json()["title"] === "article",
    "content type is json": (r) => res.headers['Content-Type'] === "application/json; charset=utf-8",
  });

  // update article -> new title
  payload = JSON.stringify({title: "new-article"});
  res = http.post(location, payload);
  check(res, {
    "status was 200": (r) => r.status === 200,
  });

  // get article details -> check new title
  res = http.get(location);
  check(res, {
    "status was 200": (r) => r.status === 200,
    "title was correct": (r) => r.json()["title"] === "new-article",
  });

  // delete article -> 204
  res = http.del(location);
  check(res, {
    "status was 204": (r) => r.status === 204,
  });

  // get article details -> 404
  res = http.get(location);
  check(res, {
    "status was 404": (r) => r.status === 404,
  });
};
