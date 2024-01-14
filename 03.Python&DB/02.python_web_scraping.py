import requests
from bs4 import BeautifulSoup

# 타겟 URL을 읽어서 HTML를 받아오고,
headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
data = requests.get('https://movie.daum.net/ranking/boxoffice/yearly', headers=headers)

# HTML을 BeautifulSoup이라는 라이브러리를 활용해 검색하기 용이한 상태로 만듦
# soup이라는 변수에 "파싱 용이해진 html"이 담긴 상태가 됨
# 이제 코딩을 통해 필요한 부분을 추출하면 된다.
soup = BeautifulSoup(data.text, 'html.parser')
# print(soup)  # HTML을 받아온 것을 확인할 수 있다.

# select를 이용해서, li들을 불러오기
movies = soup.select('.kakao_article > .section_ranking > .box_boxoffice > .list_movieranking > li')

print(len(movies)) # 50

for movie in movies:
    print(movie)
    
# movies (li들) 의 반복문을 돌리기
for movie in movies:
    # movie 안에 a 가 있으면,
    # (조건을 만족하는 첫 번째 요소, 없으면 None을 반환한다.)
    tag_element = movie.select_one('.tit_item > a')
    print(tag_element)
    
# movies (li들) 의 반복문을 돌리기
for movie in movies:
    # movie 안에 a 가 있으면,
    tag_element = movie.select_one('.tit_item > a')
    if not tag_element:
        continue

    # a의 text를 찍어본다.
    print (tag_element.text)