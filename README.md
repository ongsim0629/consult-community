24.08.06

# 시작 방법

```
$ py -3 -m venv .venv
$ .venv\Scripts\activate
(.venv) $ pip install flask requests bs4 pymongo python-dotenv PyJWT
(.venv) $ python app.py #서버 실행
(.venv) $ deactivate #가상환경 종료

```

24.08.05

# 주제 [고민 해우소]

## 필수 기능

1. 로그인 jwt
2. 회원정보
3. 게시글 작성 / 읽기 / 수정 / 삭제
   - 익명 / 실명
   - 제목
   - 내용
4. 댓글 기능 (1depth)
5. 리스팅 (조회수)
6. 반응형 - 모웹 only

## 시간 남으면 추가 기능

1. 비로그인 유저 게시판 탐색 가능
2. 리스팅 반응 추가
3. 반응형 - pc
4. 종결여부 (아이 시원해 액션, 지식인처럼 리워드)
5. 게시글 카테고리
6. 댓글 수정 기능
7. Top5 조회수 뿐만 아니라, 반응 및 댓글 수로 리스팅

## 역할분담

1. FE : 수빈님, (+ 선미)
2. BE : 효범님, 선미님

## Framework, Stack

1. FE : VanillaJS, (Bulma, Tailwind 중 택1), SSR
2. BE : Jinja2, JWT
