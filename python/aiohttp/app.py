from aiohttp import web
from datetime import datetime

"""
Repo
"""

articles = []

def db_get_article(article_id: int) -> dict:
    for article in articles:
        if article['id'] == article_id and article['status'] != 'deleted':
            return article
    raise LookupError

def db_get_articles() -> list:
    return [a for a in articles if not a['status'] == 'deleted']

def db_add_article(article: dict):
    if articles:
        next_id = max(a['id'] for a in articles) + 1
    else:
        next_id = 1
    date = datetime.now().replace(microsecond=0).isoformat()
    article = {'id': next_id, 'title': article['title'],
               'created': date, 'status': 'created'}
    articles.append(article)

def db_delete_article(article_id: int):
    for article in articles:
        if article['id'] == article_id:
            article['status'] = 'deleted'
            return
    raise LookupError

def db_update_article(article_id: int, title: str):
    article = db_get_article(article_id)
    article['title'] = title

"""
Views
"""

async def list_articles(request):
    return web.json_response(db_get_articles())

async def get_article(request):
    article_id = int(request.match_info['id'])
    try:
        article = db_get_article(article_id)
    except LookupError:
        raise web.HTTPNotFound()
    return web.json_response(article)

async def create_article(request):
    data = await request.json()
    if data['title'] == '':
        return web.HTTPBadRequest()

    db_add_article({'title': data['title']})
    return web.json_response()

async def update_article(request):
    data = await request.json()
    if data['title'] == '':
        return web.HTTPBadRequest()

    article_id = int(request.match_info['id'])
    try:
        db_update_article(article_id, data['title'])
    except LookupError:
        raise web.HTTPNotFound()
    return web.json_response()

async def delete_article(request):
    article_id = int(request.match_info['id'])
    try:
        db_delete_article(article_id)
    except LookupError:
        raise web.HTTPNotFound()
    return web.json_response()

"""
App
"""

app = web.Application()
app.add_routes([
    web.get('/articles', list_articles),
    web.get('/articles/{id:[0-9]+}', get_article),
    web.post('/articles', create_article),
    web.post('/articles/{id:[0-9]+}', update_article),
    web.delete('/articles/{id:[0-9]+}', delete_article),
])

if __name__ == '__main__':
    # add fixtures
    now = datetime.now().replace(microsecond=0).isoformat()
    for article in [
        {'id': 1, 'title': 'One!', 'created': now, 'status': 'created'},
        {'id': 2, 'title': 'Two!', 'created': now, 'status': 'created'},
        {'id': 3, 'title': 'Three!', 'created': now, 'status': 'deleted'}
    ]:
        db_add_article(article)

    web.run_app(app, port=8000)
