import string

from bayes import NaiveBayesClassifier
from bottle import redirect, request, route, run, template
from db import News, session
from scraputils import get_news



@route("/news")
def news_list():
    s = session()
    rows = s.query(News).filter(News.label == None).all()
    return template("news_template", rows=rows)



@route("/add_label/")
def add_label():
    query = request.query.decode()
    identifier = int(query["id"])
    label = query["label"]
    s = session()
    update_label(s, identifier, label)
    s.commit()
    redirect("/news")


def update_label(session, news_id, label) -> None:
    session.query(News.id).filter(News.id == news_id).update({News.label: label})


def has(ses: session, author: str, title: str) -> bool:
    return (
        len(ses.query(News.author).filter_by(author=author).all()) == 0
        or len(ses.query(News.title).filter_by(title=title).all()) == 0
    )



@route("/update")
def update_news():
    news = get_news("https://news.ycombinator.com/", 3)
    s = session()
    update_news_db(s, news)
    s.commit()
    redirect("/news")


def update_news_db(session: session, news: tp.List[tp.Dict[str, tp.Union[str, int]]]) -> None:
    for n in news:
        if has(session, n["author"], n["title"]):
            session.add(
                News(
                    title=n["title"],
                    author=n["author"],
                    url=n["url"],
                    points=n["points"],
                    comments=n["comments"],
                )
            )




@route("/classify")
def classify_news():
    ...




if __name__ == "__main__":
    run(host="localhost", port=8080)

