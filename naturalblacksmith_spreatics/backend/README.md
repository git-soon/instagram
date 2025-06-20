# REST API Spec.
- version 0.1 (2025/6/11)
## user 
## 사용자 생성
1. Endpoint
   - POST /user/create
2. Request body 
   - nickname (string): 사용자 nickname, 필수
   - name (string): 사용자 이름, 필수
   - pw (string): 비밀번호, 필수
   - age (int, optional): 사용자 나이
   - email (string, optional): 사용자 email 주소
~~~
{
  "nickname": "lemon",
  "pw": "1234",
  "name": "이승학",
  "email": "kevin.spreatics@gmail.com"
}
~~~
4. Description
   - 사용자 계정을 생성한다. nickname과 name, password는 필수 입력값이다.
   - nickname은 고유한 값이며 기존 사용자와 중복되면 생성이 실패한다.
5. Response body
   - status (string): user create success, user create failed
   - new user id(int): 생성 성공 시, user_id 반환
   - reason (string): 실패 시, 실패 원인
~~~
{
"status" : "user create success",
"new user id" : new_user_id
}

{
"status" : "failed",
"reason" : "nickname, password, name is mandatory."
}

{
"status": "user create failed", 
"reason": str(e) #Integrity error
}
~~~
## 로그인 
1. Endpoint
   - POST /user/login
2. Request body 
   - nickname: 사용자 nickname 
   - pw: 사용자 비밀번호
4. Description
   - nickname과 pw로 user_id가 존재하는지 조회한다 
   - user_id가 있다면 로그인 성공 
   - 없다면 nickname, pw 중 입력하지 않았거나 부정확한 입력 
5. Response body
   - status (string): login success, login failed
   - login user: 성공시, 로그인한 유저의 유저 id
   - reason (string): 실패시, 실패 원인
{
"status" : "login success",
"login user" : row['user_id']
}

{
"status" : "login error",
"reason" : "nickname and password required"
}

{
 "status": "login failed",
"reason": "incorrect nickname or password"
}

## 사용자 비밀번호 변경
1. Endpoint
   - PATCH /user/<int:user_id>/password_change
2. Request body 
   - pw: 사용자 비밀번호
   - new_pw: 새 비밀번호
4. Description
   - endpoint로 받은 user id의 비밀번호를 확인한다
   - json으로 받아온 pw와 user_id 일치 시 비밀번호를 변경한다 
5. Response body
   - status (string): password change success, password change failed
   - reason (string): 실패시, 실패 원인
~~~
{
"status" : "password change success"
}

{
"status": "password change failed",
"reason": "password and new password required"
}
{
"status" : "password change failed",
"reason" : "incorrect password"
}

~~~
## 사용자 삭제 (id 사용)
1. Endpoint
   - DELETE /user/<int:user_id>/delete
2. Request body 
   없음
4. Description
   - user_id에 해당하는 사용자 계정을 삭제한다.
   - user_id가 없으면 삭제가 실패한다.
5. Response body
   - status (string): delete success, delete failed
   - deleted user (int) : 성공시, 삭제된 user_id
   - reason (string): 실패시, 실패 원인
~~~
{
"status" : "delete success",
"deleted user" : user_id
}
{
"status" : "delete fail",
"error" : "user not found"
}

~~~
## 사용자 삭제 (nickname 사용)
1. Endpoint
   - DELETE /user/<string:nickname>/delete
2. Request body 
   없음
4. Description
   - nickname에 해당하는 사용자 계정을 삭제한다.
   - nickname이 없으면 삭제가 실패한다.
5. Response body
   - status (string): delete success, delete failed
   - deleted user (int) : 성공시, 삭제된 user_id
   - reason (string): 실패시, 실패 원인
~~~
{
"status" : "delete success",
"deleted user" : user_id
}
{
"status" : "delete fail",
"error" : "user not found"
}

~~~
## 포스팅
1. Endpoint
    - POST /posting/create
    - user_id: 로그인한 user_id 

2. Request body
- post title: 포스팅 제목 (required)
- post_text: 포스팅 내용 (required)

3. Description
- posting title, text를 입력하여 로그인한 user_id로 post 하나를 생성

5. Response body
 - status: posting success, posting failed
 - reason: 실패시, 실패 요인 

# 포스팅 삭제 


#코멘트
1. Endpoint
    - POST /comment/<user_id>/<post_id>/<text>
    - user_id (int): 포스팅 올리는 user_id

2. Request body
- post title: 포스팅 제목 (required)
- post_text: 포스팅 내용 (required)
- posting date: 포스팅 한 날짜 (required)

3. Description 
- posting date, post_text은 필수 입력 
- post title는 선택 

5. Response body


# 소셜
1. Endpoint
    - POST /follow/
    - user_id (int): 포스팅 올리는 user_id

2. Request body
- post title: 포스팅 제목 (required)
- post_text: 포스팅 내용 (required)
- posting date: 포스팅 한 날짜 (required)

3. Description 
- posting date, post_text은 필수 입력 
- post title는 선택 

5. Response body


# 메시지
1. Endpoint
    - POST /DM/
    - user_id (int): 포스팅 올리는 user_id

2. Request body
- post title: 포스팅 제목 (required)
- post_text: 포스팅 내용 (required)
- posting date: 포스팅 한 날짜 (required)

3. Description 
- posting date, post_text은 필수 입력 
- post title는 선택 

5. Response body

