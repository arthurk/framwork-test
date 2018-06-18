import http from "k6/http";
import { check, group, sleep } from "k6";

const baseUrl = "http://0.0.0.0:8000";

// article url for this VU
let articleUrl = null;

// randomly generated article title
let articleTitle = null;

function thinktime() {
    sleep(1 * Math.random());
}

export default function() {
  group("1. create", function() {
    var url = `${baseUrl}/articles`;
    articleTitle = Math.random().toString(36).substring(2, 15);
    var payload = JSON.stringify({title: articleTitle});
    var res = http.post(url, payload);
    check(res, {
      "status is 201": (r) => r.status === 201,
      "content-type is application/json": (r) => res.headers['Content-Type'].includes("application/json"),
      "location header is OK": (r) => 'Location' in r.headers
    });
    // save url of newly created article to be used by other tests
    articleUrl = baseUrl + res.headers['Location'];
    thinktime();
  });
  group("2. get-after-create", function() {
    var res = http.get(articleUrl);
    check(res, {
      "status is 200": (r) => r.status === 200,
      "content-type is application/json": (r) => res.headers['Content-Type'].includes("application/json"),
      "title is OK": (r) => r.json()["title"] === articleTitle,
    });
    thinktime();
  });
  group("3. update", function() {
    articleTitle = Math.random().toString(36).substring(2, 15);
    var payload = JSON.stringify({title: articleTitle});
    var res = http.post(articleUrl, payload);
    check(res, {
      "status is 200": (r) => r.status === 200,
      "content-type is application/json": (r) => res.headers['Content-Type'].includes("application/json"),
    });
    thinktime();
  });
  group("4. get-after-update", function() {
    var res = http.get(articleUrl);
    check(res, {
      "status is 200": (r) => r.status === 200,
      "content-type is application/json": (r) => res.headers['Content-Type'].includes("application/json"),
      "title is OK": (r) => r.json()["title"] === articleTitle,
    });
    thinktime();
  });
  group("5. delete", function() {
    var res = http.del(articleUrl);
    check(res, {
      "status is 204": (r) => r.status === 204,
      "content-type is application/json": (r) => res.headers['Content-Type'].includes("application/json"),
    });
    thinktime();
  });
  group("6. get-after-delete", function() {
    var res = http.get(articleUrl);
    check(res, {
      "status is 404": (r) => r.status === 404,
      "content-type is application/json": (r) => res.headers['Content-Type'].includes("application/json"),
    });
    thinktime();
  });
};
