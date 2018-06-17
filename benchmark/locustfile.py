from locust import HttpLocust, TaskSet, task
import random

all_ids = []

def get_id_from_header(headers):
    # HTTP header names are case-insensitive
    # some frameworks force lowercase
    location = headers.get("location")
    if location is None:
        location = headers.get("Location")
    return location.rsplit('/', 1)[1]

class ArticleApi(TaskSet):
    @task(10)
    def list_articles(self):
        self.client.get("/articles", name='List Articles')

    @task(20)
    def get_article(self):
        if all_ids:
            url = "/articles/" + random.choice(all_ids)
            with self.client.get(url, catch_response=True, name='Get Article') as response:
                if response.status_code == 404:
                    response.success()

    @task(1)
    def create_article(self):
        resp = self.client.post("/articles", {"title": "this is a test"}, name="Create Article")
        if resp.status_code == 201:
            article_id = get_id_from_header(resp.headers)
            all_ids.append(article_id)

    @task(1)
    def delete_article(self):
        if all_ids:
            url = "/articles/" + random.choice(all_ids)
            with self.client.delete(url, catch_response=True, name='Delete Article') as response:
                if response.status_code == 404:
                    response.success()

    @task(1)
    def update_article(self):
        if all_ids:
            url = "/articles/" + random.choice(all_ids)
            data = {"title": "update"}
            with self.client.post(url, data, catch_response=True, name='Update Article') as response:
                if response.status_code == 404:
                    response.success()

class ApiUser(HttpLocust):
    task_set = ArticleApi
    host = "http://localhost:8000"
