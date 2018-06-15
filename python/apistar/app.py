from datetime import datetime

from apistar import App, Route, exceptions, http

DATE = datetime.now().replace(microsecond=0).isoformat()
ARTICLES = [
    {'id': 1, 'title': 'One!', 'created': DATE, 'status': 'created'},
    {'id': 2, 'title': 'Two!', 'created': DATE, 'status': 'created'},
    {'id': 3, 'title': 'Three!', 'created': DATE, 'status': 'deleted'},
]

def find_article(id: int) -> dict:
    for article in ARTICLES:
        if article['id'] == id:
            return article

def is_auth(password: str) -> bool:
    return password == 'test'

def list_articles() -> list:
    articles = [a for a in ARTICLES if not a['status'] == 'deleted']
    return articles

def get_article(id: int) -> dict:
    article = find_article(id)
    if article is None or article['status'] == 'deleted':
        raise exceptions.NotFound()
    return article

def create_article(data: http.RequestData, password: http.Header) -> dict:
    if not is_auth(password):
        raise exceptions.BadRequest()

    # title must be set
    if not data['title']:
        raise exceptions.BadRequest()

    # find the next id
    max_id = max([a['id'] for a in ARTICLES])
    next_id = max_id + 1

    # create new article and append to list of articles
    date = datetime.now().replace(microsecond=0).isoformat()
    article = {'id': next_id, 'title': data['title'], 'created': date,
               'status': 'created'}
    ARTICLES.append(article)
    return article

def update_article(id: int, data: http.RequestData, password: http.Header) -> dict:
    if not is_auth(password):
        raise exceptions.BadRequest()

    # title must be set
    if not data['title']:
        raise exceptions.BadRequest()

    # find article
    article = find_article(id)
    if article is None or article['status'] == 'deleted':
        raise exceptions.NotFound()

    # update article title
    article['title'] = data['title']
    return article

def delete_article(id: int, password: http.Header) -> dict:
    if not is_auth(password):
        raise exceptions.BadRequest()

    article = find_article(id)
    if article is None or article['status'] == 'deleted':
        raise exceptions.NotFound()
    article['status'] = 'deleted'


routes = [
    Route('/articles', method='GET', handler=list_articles),
    Route('/articles/{id}', method='GET', handler=get_article),
    Route('/articles', method='POST', handler=create_article),
    Route('/articles/{id}', method='POST', handler=update_article),
    Route('/articles/{id}', method='DELETE', handler=delete_article),
]

app = App(routes=routes)

if __name__ == '__main__':
    app.serve('127.0.0.1', 5000, debug=True)
