# Vision-API-Receipt-OCR

사용법

1. 파이선 콘솔로 pip install google-cloud-vision를 설치한다
2. 따로 받은 .json파일 경로를 line 3의 r""에 입력한다
3. line 450으로 영수증의 URL을 입력하거나 line 452로 영수증 이미지 파일 경로를 입력해주고 실행한다


각 Function의 역할

1. is_hangul_character(char)
  input: char
  output: 1/0
  function: 입력받은 글자가 한글이면 1, 아니면 0 출력

2. concaetenator(words)
  input: string
  output: string
  function: 입력받은 문자열에서 연속되고 중복되는 문자들을 하나로 합쳐줌 (예: 0, 0, 0 -> 000)
  Note: 현재 사용하지 않음

3. pricefixer(numbers)
  input: list of strings
  output: string
  function: 입력받은 문자열에서 쉼표, 마침표, 빈칸을 삭제하고 출력
  Note: 인식한 가격을 하나의 숫자로 표기 (예: 4, 500 -> 4500)

4. maxrighter(texts)
  input: TEXT
  output: 없음
  function: 영수증에서 가장 오른쪽에 있는 문자열의 x값을 global variable인 maxright에 저장
  Note: 좀 원시적인 방법이지만, maxright은 price를 인식 시작하는 부분을 정의하는 역할을 함
        인식 방법 때문에 영수증 밖에 다른 문자들이 인식될 경우 나머지 코드가 꼬임
        추후에 영수증만 crop해서 사용하는 방법으로 해결 가능함
  
5. numscanner(texts)
  input: TEXT
  output: list of strings
  function: 영수증에서 쉼표, 마침표, 빈칸 뒤에 숫자가 3개 연속으로 오는 부분을 찾아 그 부분을 finalresult.price에, 그 부분의 index를 finalresult.index에 저장. index의 리스트 출력
  Note: 찾은 숫자의 오른쪽 변의 x값이 maxright에서 x방향으로 40픽셀 내에 있어야 함
        3자리 연속된 숫자를 찾기 때문에 100원 미만의 금액은 인식이 안됨
  
6. pricescanner(texts, indexes)
  input: TEXT, list of strings
  output: 2 lists of strings
  function: numscanner에서 찾은 숫자들이 price의 형태에 부합하는지 확인 후, 맞으면 그 숫자들을 finalresult.price에, index들을 finalresult.index에 저장. price, result 리스트 출력.
  Note: pricescanner 코딩 이후로 global variable인 finalresult를 더 적극적으로 활용함, 그래서 이후 function들은 input이 TEXT밖에 없음


7. authenticator(texts)
  input: TEXT
  output: 없음
  function: pricescanner에서 찾은 숫자들 사이의 문자열을 확인하고, '합계', '금액', '물품'이 들어가면 그 문자열 이하 문자열을 price에서 자름. 
            업데이트된 문자열을 finalresult.price, index에 저장
            총 합계 가격을 finalresult.netprice에 저장 (int)
  Note: 원래 finalresult.price의 마지막 숫자와, 업데이트된 finalresult.price의 가격들의 합을 비교해 1000 이하의 차이가 나면 마지막 숫자를 finalresult.netprice에 저장함
        numscanner의 한계인 100원 미만 숫자 인식 불가를 어느 정도 해결하기 위한 것
        
8. prodname(texts)
  input: TEXT
  output: 없음
  function: finalresult.price에서 숫자들 사이의 문자열을 확인하고, 알파벳/한글/()이 들어가는 문자열을 finalresult.product에 저장함
  Note: price들 사이를 스캔하기 때문에, 가장 첫 price는 y축 방향으로 20픽셀을 스캔하고, 문자열의 아래쪽 변이 price의 왼쪽 변의 y픽셀 + 20개 픽셀 안에 해당되면 price 이름으로 인식(보통 2줄)
  
9. quannum(texts)
  input: TEXT
  output: 없음
  function: finalresult.price에서 숫자와 y축 방향으로 10픽셀 이내에 있는 문자열 중 2자리 이하 숫자를 '개수'로 인식하고 finalresult.quantity에 저장함.
            만약 해당 조건에 부합하는 숫자가 없을 경우 (Vision API에서 인식하지 못한 경우임) 'Not Found'를 해당 finalresult.quantity 자리에 저장함
  Note: prodname과는 다르게 해당 숫자와 같은 줄에 있는 문자열만 인식함(1줄)
  
10. detect_text(path):
  input: string(파일 경로)
  output: product, price, quantity, final price (string)
  function: 입력된 파일 경로에 있는 이미지(영수증)를 스캔하고 product, price, quantity, final price 출력
  
11. detect_text_uri(uri):
  input: string(url)
  output:product, price, quantity, final price (string)
  function: 입력된 url에 있는 이미지(영수증)를 스캔하고 product, price, quantity, final price 출력
  

Vision API 커맨드

1. text[index].description
  text[index]의 글자 출력함
  [index]가 없을 경우 오류
  보통 text in texts로 사용함

2. text[index].bounding_poly.vertice[index].x / y
  text[index] (문자열)의 x 또는 y값 (픽셀) 출력
  vertice[index]에서 index값이 각각 0, 1, 2, 3일때 좌측 상단, 우측 상단, 우측 하단, 좌측 하단의 x/y값 출력
  .x / .y를 안붙이면 해당 꼭지점의 x y값 모두 출력
  vertice[index]에서 [index]가 없으면 4개 꼭지점의 x, y값 모두 출력
  
나머지는 모르겠음 ㅋㅋㄹㅃㅃ~



Issues

1)	영수증이 기울어졌을 때
  A.	심하게 기울어진 영수증은 인식이 어려움. 
  이유:현재 알고리즘은 “금액”의 y좌표 아래로 물품을 스캔하기 때문
2)	영수증을 너무 멀리서 찍어서 글자가 너무 작게 찍혔을 때
  A.	각 줄이 8~10픽셀 아래로 떨어지면 문제 생길 수 있음
3)	100원 미만의 품목이 인식 안됨
  A.	인지하고 있는 문제, 하지만 거의 일어나지 않을 문제이므로 일단 무시
4)	상품 이름에 숫자가 제대로 인식 안되는 경우 있음
  A.	인지함, 고칠 거임’
5)	상품 개수가 Not Found로 뜸
  A.	Vision API에서 문자 자체를 인식 못하거나, 코드 parameter에 문제 있을 수 있음
    	후자의 경우 quannum에서 line 365에서 l + 10에서 10을 늘리면 됨
6)	상품 개수에 이상한 숫자가 찍힘
  A.	영수증이 심하게 기울어져 다음 줄 숫자가 인식되거나, Vision API에서 개수를 올바르게 인식을 못해 엉뚱한 숫자로 인식되는 것일 수 있음
    	두 가지 문제 모두 영수증 사진을 다시 찍어야 함


Troubleshooting

1)	가격에 인식 안되는 문자가 있을 때:
  A.	Prodname()의 끝에서 조금 위에 if char.isalph() or ….에서 or char == ‘’추가하고 ‘’ 사이에 인식 안되는 문자 입력
    	주의! 추가하는 문자로 인해 다른 상품 이름이 꼬일 수 있음
2)	오류가 뜰 때
  A.	영수증이 심하게 기울어지지 않았나 확인
  B.	영수증 밖에 다른 글자들이 보이나 확인
3)	상품 이름 인식 중 여러 상품 이름들이 하나로 뭉쳐서 나옴
  A.	prodname에서 line 331에서 픽셀 개수 조정 필요, l + 10에서 10을 늘려야 함
4)	상품 개수가 Not Found로 뜸
  A.	Vision API에서 개수를 제대로 인식 못한거임, 사진을 다시 찍는거 추천
  
  
Resources
https://codelabs.developers.google.com/codelabs/cloud-vision-api-python#7
https://cloud.google.com/vision/docs/ocr
https://developers.google.com/resources/api-libraries/documentation/vision/v1/python/latest/vision_v1.images.html
