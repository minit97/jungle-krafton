import random
import requests

from bs4 import BeautifulSoup
from pymongo import MongoClient           # pymongo를 임포트 하기(패키지 인스톨 먼저 해야겠죠?)

client = MongoClient('localhost', 27017)  # mongoDB는 27017 포트로 돌아갑니다.
db = client.dbjungle                      # 'dbjungle'라는 이름의 db를 만듭니다.


def insert_all():
    headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
    data = requests.get('https://search.daum.net/search?w=tot&m=&q=2022%EB%85%84%20%EC%98%81%ED%99%94%20%ED%9D%A5%ED%96%89%EC%88%9C%EC%9C%84&nzq=%EC%97%B0%EA%B0%84%EC%98%81%ED%99%94%EC%88%9C%EC%9C%84&DA=NSJ', headers=headers)
    soup = BeautifulSoup(data.text, 'html.parser')

    movies = soup.select('#morColl > div.coll_cont > div > ol > li')
    print(len(movies))

    for movie in movies:
        tag_element = movie.select_one('.wrap_cont > .info_tit > a')
        if not tag_element:
            continue
        title = tag_element.text
        print("제목 : ", title)

        tag_element = movie.select('.dl_comm')

        open_date_tag = tag_element[1].select_one('.cont')
        if not open_date_tag:
            continue
        open_date = open_date_tag.text[:-1]
        print("개봉일자 : ", open_date)
        (open_year, open_month, open_day) = [int(element) for element in open_date.split('.')]

        viewers_tag = tag_element[3].select_one('.cont')
        if not viewers_tag:
            continue
        viewers = viewers_tag.findChild(string=True, recursive=False)
        viewers = int(''.join([c for c in viewers if c.isdigit()]))
        print("누적관객수 : ", viewers)

        # 영화 포스터 이미지 URL 을 추출한다.
        movie_img_tag = movie.select_one('.wrap_thumb > .thumb > img')
        if not movie_img_tag:
            continue
        poster_url = movie_img_tag['data-original-src']
        if not poster_url:
            continue

        # 영화 정보 URL 을 추출한다.
        movie_url_tag = movie.select_one('.wrap_cont > .info_tit > a')
        if not movie_url_tag:
            continue
        info_url = movie_url_tag['href']
        if not info_url:
            continue
        info_url = 'https://search.daum.net/search' + info_url

        found = list(db.movies.find({'title': title}))
        if found:
            continue

        likes = random.randrange(0, 100)

        doc = {
            'title': title,
            'open_year': open_year,
            'open_month': open_month,
            'open_day': open_day,
            'viewers': viewers,
            'poster_url': poster_url,
            'info_url': info_url,
            'likes': likes,
            'trashed': False,
        }
        db.movies.insert_one(doc)
        print('완료: ', title, open_year, open_month, open_day, viewers, poster_url, info_url)

if __name__ == '__main__':
    db.movies.drop()
    insert_all()