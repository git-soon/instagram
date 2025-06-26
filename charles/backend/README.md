# REST API Spec.
- version 0.1 (2025/06/11)

# 사용자 계정

## 사용자 생성
1. Endpoint
   - POST /users

2. Request body

   - nickname (string, required): 사용자 별명 (고유)

   - name     (string, required): 사용자 이름

   - password (string, required): 비밀번호

   - age      (int, optional): 사용자 나이

   - email    (string, optional): 사용자 이메일
~~~json
{
  "nickname": "charles",
  "name": "김창순",
  "password": "1234",
  "email": "soon1234@naver.com",
  "age": 30
}
~~~

3. Description
   - 새로운 사용자 계정을 생성한다.

   - nickname, name, password는 반드시 입력해야 하며, 중복된 nickname이 있을 경우 생성에 실패한다.

4. Response body

   - status (string): "created" 또는 "failed"

   - user_no (int): 생성 성공 시 사용자 고유 번호

   - reason (string): 실패 시 원인

~~~json
// 성공
{
  "status": "created",
  "user_no": 105
}

// 실패
{
  "status": "failed",
  "reason": "nickname 'charles' is already taken"
}
~~~

## 사용자 인증 (로그인)
1. Endpoint
   - POST /users/login

2. Request body
   - nickname (string, required): 가입된 사용자 별명

   - password (string, required): 비밀번호

~~~json
{
  "nickname": "charles",
  "password": "1234"
}
~~~

3. Description
   - 입력된 nickname과 password를 확인하여 로그인 처리한다.

   - 세션 또는 간단한 인증 플래그로 로그인 상태를 유지하며 구현한다.

4. Response body
   - status (string): "success" 또는 "denied"
   
   - user_no (int): 로그인 성공 시 사용자 고유 번호 (페이지 이동용)
   
   - reason (string): 실패 시 오류 메시지

~~~json
// 성공
{
  "status": "success",
  "user_no": 105
}

// 실패
{
  "status": "denied",
  "reason": "잘못된 아이디 또는 비밀번호입니다."
}
~~~

## 사용자 정보 조회
1. Endpoint
   - GET /users/{user_no}

2. Request body
   - 없음

3. Description
   - path의 user_no에 해당하는 사용자 정보를 반환한다.

4. Response body
   - status (string): "success" 또는 "failed"
   - user (object): 사용자 
   
정보
-성공시 

     - user_no (int)
     
     - nickname (string)
     
     - name (string)
     
     - age (int, optional)
     
     - email (string, optional)
     
-실패시 \
    - reason (string): 실패 시 원인

~~~json
// 성공
{
  "status": "success",
  "user": {
    "user_no": 105,
    "nickname": "charles",
    "name": "김창순",
    "age": 30,
    "email": "soon1234@naver.com",
  }
}

// 실패
{
  "status": "failed",
  "reason": "user_no 105 not found"
}
~~~

## 사용자 정보 수정
1. Endpoint
   - PUT /users/{user_no}

2. Request body
   - nickname (string, optional)
   - name     (string, optional)
   - password (string, optional)
   - age      (int, optional)
   - email    (string, optional)

~~~json
{
  "nickname": "charles_new",
  "age": 31
}
~~~

3. Description
   - 기존 사용자 정보를 수정한다. 변경하지 않을 필드는 요청에 포함하지 않는다.

4. Response body
   - status (string): "updated" 또는 "failed"
   - user (object): 수정된 사용자 정보
   - reason (string): 실패 시 원인

~~~json
// 성공
{
  "status": "updated",
  "user": {
    "user_no": 105,
    "nickname": "charles_new",
    "name": "김창순",
    "age": 31,
    "email": "soon1234@naver.com",

  }
}

// 실패
{
  "status": "failed",
  "reason": "user_no 105 not found"
}
~~~

## 사용자 삭제
1. Endpoint
   - DELETE /users/{user_no}

2. Request body
   - 없음

3. Description
   - 지정된 user_no의 사용자 계정을 삭제한다.

4. Response body
   - status (string): "deleted" 또는 "failed"
   
   - reason (string): 실패 시 원인

~~~json
// 성공
{
  "status": "deleted"
}

// 실패
{
  "status": "failed",
  "reason": "user_no 101 doesn't exist"
}
~~~

# 포스팅

## 포스트 올리기
1. Endpoint
   - POST /post/create

2. Request body
   - user_no   (int, required): 작성자 user_no
   - text   (string, optional): 작성자가 쓴글

~~~json
{
  "user_no": 105,
  "text": "날씨 너무 덥다."
}
~~~

3. Description
   - 새로운 포스트를 생성한다.

4. Response body
   - status (string): "created" 또는 "failed"
   - post_id (int): 생성된 포스트 번호
   - reason (string): 실패 시 원인

~~~json
// 성공
{
  "status": "created",
  "post_id": 210
}

// 실패
{
  "status": "failed",
  "reason": "user_no 999 not found"
}
~~~

## 올라온 포스트 조회하기
1. Endpoint
   - GET /posts

2. Request body
   - user_no (int, optional): 특정 사용자의 포스트만 조회
    - post : 모든 포스트 가져오기

3. Description
   - 전체 또는 특정 사용자의 포스트 목록을 조회한다.

4. Response body
   - status (string): "success" 또는 "failed"
   - posts (array of objects):
     - post_id      (int)
     - user_no      (int)
     - text         (string)
     - comment_count(int)
     - like_count   (int)
   - reason (string): 실패 시 원인

~~~json
{
  "status": "success",
  "posts": [ { /* ... */ } ]
}
~~~

## 포스트의 커맨트 조회하기
1. Endpoint
   - GET /posts/{post_id}/comments

2. Request body
   - 없음

3. Description
   - 지정된 post_id의 커맨트 목록을 조회한다.

4. Response body
   - status (string): "success" 또는 "failed"
   - comments (array):
     - post_id      (int)
     - comment_id (int)
     - user_no    (int)
     - text       (string)
   - reason (string): 실패 시 원인

~~~json
{
  "status": "success",
  "comments": [ { /* ... */ } ]
}
~~~

## 특정 포스트에 커맨트 달기
1. Endpoint
   - POST /posts/{post_id}/comments

2. Request body
   - user_no (int, required): 작성자 user_no
   - text    (string, required): 커맨트 내용

~~~json
{
  "user_no": 106,
  "text": "멋진 사진이네요!"
}
~~~

3. Description
   - post_id에 새로운 커맨트를 추가한다.

4. Response body
   - status (string): "created" 또는 "failed"
   - comment_id (int): 생성된 커맨트 번호
   - reason (string): 실패 시 원인

~~~json
{
  "status": "created",
  "comment_id": 502
}
~~~

# 소셜

## 다른 사용자 조회
1. Endpoint
   - GET /users

2. Query parameters
   - search (string, optional): 닉네임 또는 이름 검색어

3. Description
   - 사용자 목록을 조회한다.

4. Response body
   - status (string): "success" 또는 "failed"
   - users (array): [{ user_no, nickname, name, profile_url }]

~~~json
{
  "status": "success",
  "users": [ { /* ... */ } ]
}
~~~

## 팔로우 신청
1. Endpoint
   - POST /follow_requests

2. Request body
   - follower_no( int, required): 요청자 user_no
   - followee_no( int, required): 대상 user_no
~~~json
{
  "follower_no": 105,
  "followee_no": 106
}
~~~

3. Description
   - 팔로우 요청을 생성한다.

4. Response body
   - status (string): "created" 또는 "failed"
   - request_no (int): 생성된 요청 번호
   - reason (string): 실패 시 원인

~~~json
{
  "status": "created",
  "request_no": 50
}
~~~

## 팔로우한 목록 조회
1. Endpoint
   - GET /users/{user_no}/following

2. Request body
   - 없음

3. Description
   - user_no가 팔로우한 사용자 목록을 반환한다.

4. Response body

   - status (string): "success" 또는 "failed"

   - following (array of objects): [{ user_no, nickname, name }]

~~~json
{
  "status": "success",
  "following": [ { /* ... */ } ]
}
~~~

## 자신에게 팔로우 요청한 목록 조회

1. Endpoint

   - GET /users/{user_no}/follow_requests

2. Request body

   - 없음

3. Description
   
   - user_no에게 온 팔로우 
   요청 목록을 반환한다.

4. Response body

   - status (string): "success" 또는 "failed"

   - requests (array of objects): [{ request_no, follower_no, created_at }]

~~~json
{
  "status": "success",
  "requests": [ { /* ... */ } ]
}
~~~

## 팔로우 수락/거절

1. Endpoint

   - PATCH /follow_requests/{request_no}

2. Request body

   - action (string, required): "accept" 또는 "reject"

~~~json
{
  "action": "accept"
}
~~~

3. Description

   - 해당 팔로우 요청을 수락하거나 거절한다.

4. Response body

   - status (string): "updated" 또는 "failed"

   - reason (string): 실패 시 원인

~~~json
{
  "status": "updated"
}
~~~

# 메시지

## DM 보내기

1. Endpoint

   - POST /messages

2. Request body

   - sender_no   (int, required): 발신자 user_no

   - receiver_no (int, required): 수신자 user_no

   - content     (string, required): 메시지 내용

~~~json
{
  "sender_no": 105,
  "receiver_no": 106,
  "content": "안녕하세요!"
}
~~~

3. Description

   - 새로운 DM을 생성하여 전송한다.

4. Response body

   - status (string): "created" 또는 "failed"

   - message_no (int): 생성된 메시지 번호

   - reason (string): 실패 시 원인

~~~json
{
  "status": "created",
  "message_no": 200
}
~~~

## DM 조회하기

1. Endpoint

   - GET /messages

2. Query parameters

   - user_no (int, required): 조회할 사용자 user_no

   - with    (int, optional): 특정 사용자와의 대화 상대 user_no

   - page    (int, optional): 페이지 (default: 1)

   - limit   (int, optional): 페이지당 개수 (default: 50)

3. Description

   - 해당 사용자와 전체 또는 특정 상대방 간 DM 목록을 조회한다.

4. Response body

   - status (string): "success" 또는 "failed"

   - messages (array): [{ message_no, sender_no, receiver_no, content, created_at }]

~~~json
{
  "status": "success",
  "messages": [ { /* ... */ } ]
}
~~~

## DM 삭제하기

1. Endpoint

   - DELETE /messages/{message_no}

2. Request body

   - 없음

3. Description

   - 지정된 message_no의 DM을 삭제한다.

4. Response body

   - status (string): "deleted" 또는 "failed"

   - reason (string): 실패 시 원인

~~~json
{ //성공시
  "status": "deleted"
}
{ // 실패시
  "status": "failed"
}
