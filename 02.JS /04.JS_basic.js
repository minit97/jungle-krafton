// 모든 알파벳을 대문자로 바꾸기
let myname = 'jungle'

myname.toUpperCase() // JUNGLE


// 특정 문자를 기준으로 문자열을 나누고 싶은 경우
let myemail = 'test@gmail.com'

let result = myemail.split('@') // ['test','gmail.com'] (뒤에 배울 '리스트'라는 자료형이다)

result[0] // test (리스트의 첫번째 요소)
result[1] // gmail.com (리스트의 두 번째 요소

let result2 = result[1].split('.') // ['gmail','com']

result2[0] // gmail -> 우리가 알고 싶었던 것
result2[1] // com

// 한 줄로 쓸 수도 있다.
myemail.split('@')[1].split('.')[0]


// 특정 문자를 기준으로 문자열을 나누고 싶은 경우
let txt = '서울시-마포구-망원동'
let names = txt.split('-'); // ['서울시','마포구','망원동']
let result = names.join('>'); // '서울시>마포구>망원동'