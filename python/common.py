from datetime import datetime

class MemoryRepo:
    def __init__(self):
        self.articles = []

    def get_article(self, article_id: int) -> dict:
        for article in self.articles:
            if article['id'] == article_id and article['status'] != 'deleted':
                return article
        raise LookupError

    def get_articles(self) -> list:
        return [a for a in self.articles if not a['status'] == 'deleted']

    def add_article(self, article: dict):
        if self.articles:
            next_id = max(a['id'] for a in self.articles) + 1
        else:
            next_id = 1
        date = datetime.now().replace(microsecond=0).isoformat()
        article = {'id': next_id, 'title': article['title'],
                   'created': date, 'status': 'created'}
        self.articles.append(article)

    def delete_article(self, article_id: int):
        for article in self.articles:
            if article['id'] == article_id:
                article['status'] = 'deleted'
                return
        raise LookupError

    def update_article(self, article_id: int, title: str):
        article = self.get_article(article_id)
        article['title'] = title

    def add_fixtures(self):
        now = datetime.now().replace(microsecond=0).isoformat()
        for article in [
            {'id': 1, 'title': 'One!', 'created': now, 'status': 'created'},
            {'id': 2, 'title': 'Two!', 'created': now, 'status': 'created'},
            {'id': 3, 'title': 'Three!', 'created': now, 'status': 'deleted'}
        ]:
            self.add_article(article)
