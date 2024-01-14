import requests

from bs4 import BeautifulSoup
from pymongo import MongoClient           # pymongo를 임포트 하기(패키지 인스톨 먼저 해야겠죠?)

client = MongoClient('localhost', 27017)  # mongoDB는 27017 포트로 돌아갑니다.
db = client.dbjungle                      # 'dbjungle'라는 이름의 db를 만듭니다.


def insert_all():
    # URL을 읽어서 HTML를 받아오고,
    headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
    data = requests.get('https://movie.daum.net/ranking/boxoffice/yearly', headers=headers)

    # HTML을 BeautifulSoup이라는 라이브러리를 활용해 검색하기 용이한 상태로 만듦
    soup = BeautifulSoup(data.text, 'html.parser')
    # select를 이용해서, li들을 불러오기
    movies = soup.select('#morColl > div.coll_cont > div > ol > li')
    print(len(movies))

    # movies (li들) 의 반복문을 돌리기
    for movie in movies:
        # movie 안에 a 가 있으면,
        # (조건을 만족하는 첫 번째 요소, 없으면 None을 반환한다.)
        tag_element = movie.select_one('.wrap_cont > .info_tit > a')
        if not tag_element:
            continue
        title = tag_element.text  # a 태그 사이의 텍스트를 가져오기
        print("제목 : " ,title)

        tag_element = movie.select_one('.wrap_cont > .dl_comm:nth-child(3) > .cont')
        if not tag_element:
            continue
        open_date = tag_element.text[:-1]
        print("개봉일자 : " ,open_date)

        # 년도.월.일 형태에서 년도, 월, 일을 추출하기
        # (각각이 . 으로 구분되어있으므로 . 을 기준으로 split 한 뒤 각각을 문자형태에서 숫자형태로 변경해준다.)
        (open_year, open_month, open_day) = [int(element) for element in open_date.split('.')]

        # 누적 관객수를 얻어낸다. "783,567명" 과 같은 형태가 된다.
        tag_element = movie.select_one('.wrap_cont > .dl_comm:nth-child(4) > .cont')
        if not tag_element:
            continue
        viewers = tag_element.findChild(string=True, recursive=False)
        viewers = int(''.join([c for c in viewers if c.isdigit()]))
        print("관객수 : " ,viewers)

        doc = { 
            'title': title,
            'open_year': open_year,
            'open_month': open_month,
            'open_day': open_day,
            'viewers': viewers,
        }   
        db.movies.insert_one(doc)
        print('완료: ', title, open_year, open_month, open_day, viewers)


if __name__ == '__main__':
    # 기존의 movies 콜렉션을 삭제하기
    db.movies.drop()

    # 영화 사이트를 scraping 해서 db 에 채우기
    insert_all()