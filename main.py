import json
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import time

def get_first_news(url):
    headers = {
        "User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 YaBrowser/23.3.3.719 Yowser/2.5 Safari/537.36"
    }

    # req = requests.get(url, headers)
    # with open("projects.html", "w") as file:
    #     file.write(req.text)

    url = "https://www.yuga.ru/news/"
    r = requests.get(url=url, headers=headers)

    soup = BeautifulSoup(r.text, "lxml")
    articles_cards = soup.find_all("div", class_="card text-piclist")

    project_urls = []
    news_dict = {}

    for article in articles_cards:
        project_url = article.find("a").get("href")
        project_urls.append(project_url)


    for project_url in project_urls:
        req = requests.get(project_url, headers)

        article_id = project_url.split("/")[-2]
        article_id = int(article_id[:+6])
        # print(article_id)


        with open(f"data/{article_id}.html","w") as file:
            file.write(req.text)

        with open(f"data/{article_id}.html") as file:
            r = file.read()

        soup = BeautifulSoup(r, "lxml")
        article_data = soup.find("time").text.strip()
        article_title = soup.find("h1", class_="h2 mb20").text.strip()

        articles_desc = soup.find_all("div", class_="material-paragraph")

        article_full_desc = []

        for item in articles_desc:
            article_desc = item.text.strip()
            article_full_desc.append(article_desc)


        for i in range(len(article_full_desc)):
            article_full_desc[i] = article_full_desc[i].replace(u'\xa0', u'').strip()
            # print(article_full_desc[i])

        # print(article_full_desc)
        # print(f"{article_data}|{article_title}|{full_desc}|{project_url}")


        news_dict[article_id] = {
            "article_data":article_data,
            "article_title":article_title,
            "article_full_desc":article_full_desc,
            "project_url":project_url
        }


    # print(news_dict)
    with open("news_dict.json", "w",encoding="utf-8") as file:
        json.dump(news_dict, file, indent=4, ensure_ascii=False)

def check_news_update(url):

    with open("news_dict.json", "r",encoding="utf-8") as file:
        news_dict = json.load(file)

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 YaBrowser/23.3.3.719 Yowser/2.5 Safari/537.36"
    }

    # req = requests.get(url, headers)
    # with open("projects.html", "w") as file:
    #     file.write(req.text)

    url = "https://www.yuga.ru/news/"
    r = requests.get(url=url, headers=headers)

    soup = BeautifulSoup(r.text, "lxml")
    articles_cards = soup.find_all("div", class_="card text-piclist")

    project_urls = []
    fresh_news = {}

    for article in articles_cards:
        project_url = article.find("a").get("href")
        project_urls.append(project_url)

    for project_url in project_urls:
        req = requests.get(project_url, headers)

        article_id = project_url.split("/")[-2]
        article_id = article_id[:+6]
        # print(article_id)


        if article_id in news_dict:
            continue
        else:

            with open(f"data/{article_id}.html", "w") as file:
                file.write(req.text)

            with open(f"data/{article_id}.html", "r") as file:
                r = file.read()

            soup = BeautifulSoup(r, "lxml")
            article_data = soup.find("time").text.strip()
            article_title = soup.find("h1", class_="h2 mb20").text.strip()

            articles_desc = soup.find_all("div", class_="material-paragraph")

            article_full_desc = []

            for item in articles_desc:
                article_desc = item.text.strip()
                article_full_desc.append(article_desc)

            for i in range(len(article_full_desc)):
                article_full_desc[i] = article_full_desc[i].replace(u'\xa0', u'').strip()

            news_dict[article_id] = {
                "article_data": article_data,
                "article_title": article_title,
                "article_full_desc": article_full_desc,
                "project_url": project_url
            }

            fresh_news[article_id] = {
                "article_data": article_data,
                "article_title": article_title,
                "article_full_desc": article_full_desc,
                "project_url": project_url
            }



    with open("news_dict.json", "w",encoding="utf-8") as file:
        json.dump(news_dict, file, indent=4, ensure_ascii=False )

    return fresh_news


def main():
    print(check_news_update("https://www.yuga.ru/news/"))
    # get_first_news("https://www.yuga.ru/news/")


if __name__ == "__main__":
    main()












