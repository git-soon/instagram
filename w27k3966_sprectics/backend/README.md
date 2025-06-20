# REST API Spec.
- version 0.1 (2025/6/11)
# 사용자 계정
## 사용자 생성
1. Endpoint
   - POST /users
2. Request body 
   - nickname (string): 사용자 nickname, 필수
   - name (string): 사용자 이름, 필수
   - password (string): 비밀번호, 필수
   - age (int, optional): 사용자 나이
   - email (string, optional): 사용자 email 주소
~~~
{
  "nickname": "sohee",
  "name": "shinsohee",
  "password": "1234",
  "email": "sohee.spreatics@gmail.com"
}
~~~
4. Description
   - 사용자 계정을 생성한다. nickname과 name, password는 필수 입력값이다.
   - nickname은 고유한 값이며 기존 사용자와 중복되면 생성이 실패한다.
5. Response body
   - status (string): created, failed
   - user_id (int): 생성 성공 시, user_id 반환
   - reason (string): 실패 시, 실패 원인
~~~
{
  "status": "created",
  "user_id": 105
}

{
  "status": "failed",
  "reason": "nickname, sohee is duplicated"
}
~~~
## 사용자 인증 (로그인)

1. Endpoint
   - POST /users/login

2. Request body
   - nickname (string): 사용자 nickname, 필수
   - password (string): 비밀번호, 필수
~~~
{
  "nickname": "sohee",
  "password": "1234"
}
~~~

3. Description
   - 사용자 nickname과 password 입력
   - 틀릴 경우 Error
   - 
4. Response body
   - status (string): success, failed
   - user_id (int) : 로그인 성공한 사용자 id
   - reason (string): 실패 시, 실패 원인
   
~~~
{
 "status" : "success",
 "user_id" : 105
}
{
 "status": "failed",
 "reason": "nickname or password ERROR"
}

~~~

## 사용자 정보 조회
1. Endpoint
   - GET /users/<user_id>

2. Request Body
   -user_id (int) : 조회하려는 사용자 id

3. Description
   - 특정 user_id에 해당하는 사용자의 정보를 조회
   - 
4. Response body
   - status (string): success, failed
   - user (object) : 사용자 정보 객체 
   - reason (string): 실패 시, 실패 원인

~~~
{
 "status" : "success",
 "user" : {
    "user_id": 105,
    "nickname": "sohee",
    "name": "shinsohee",
    "email": "sohee.spreatics@gmail.com"
  }
}
{
  "status": "failed",
  "reason": "User not found"
}

~~~

## 사용자 정보 수정
1. Endpoint
   - PUT /users/<user_id>
   
2. Request params
   -user_id (int) : 수정하려는 사용자 id
   
3. Request body  
   - nickname (string, optional): 새로운 nickname  
   - name (string, optional): 새로운 이름  
   - password (string, optional): 새로운 비밀번호  
   - email (string, optional): 이메일 변경

4. Description  
   - 특정 user_id에 해당하는 사용자의 정보를 수정 
   - body에 포함된 항목만 수정되며, 입력하지 않은 필드는 유지
~~~
{
 "nickname" : "newsohee",
  "password" : "13579"
}
~~~
5. Response body
   - status (string): success, failed
   - reason (string): 실패 시, 실패 원인

~~~
{
  "status": "success"
}
{
  "status": "failed",
  "reason": "User not found"
}
~~~
## 사용자 삭제
1. Endpoint
   - DELETE /users/<user_id>
     - user_id (int): 삭제할 사용자 id
2. Request body 
   - 없음
4. Description
   - user_id에 해당하는 사용자 계정을 삭제
   - user_id가 없으면 삭제가 실패
5. Response body
   - status (string): deleted, failed
   - reason (string): 실패시, 실패 원인
~~~
{
  "status": "failed",
  "reason": "user_id, User not found"
}
{
  "status": "failed",
  "reason": "Invalid password format"
}
~~~

# 포스팅
## 게시글 생성

1. Endpoint  
   - POST /posts

2. Request body  
   - title (string): 게시글 제목, 필수  
   - text (string): 게시글 본문 내용, 필수  
   - user_id (int): 작성자 ID, 필수

3. Description  
   - 사용자가 새 게시글을 작성
   - 요청한 `user_id`의 사용자가 작성자로 기록

~~~
{
  "title": "오늘의 일기",
  "text": "우래옥 웨이팅 내앞에 40팀",
  "user_id": 105
}
~~~

4. response body
   - status(string) : updated, failed
   - post_id(int) : 생성된 게시글
   - reason(string) : 실패 원인
   
~~~  
{
  "status": "created",
  "post_id": 101
}
{
  "status": "failed",
  "reason": "Missing required field: text"
}
{
  "status": "failed",
  "reason": "User_id not found"
}
~~~
## 올라온 포스트 조회하기

1. Endpoint  
   - GET /posts
2. Request body
   - 없음
3. Description
   - 전체 또는 특정 사용자의 포스트 목록을 조회
   - 각 게시글에 user정보 포함
  
4. Response body

   - status (string): "success" 또는 "failed"
   - posts (array): 게시글 목록
   - reason (string): 실패 시 원인

~~~
{
  "status": "success",
  "posts": [
    {
      "post_id": 101,
      "title": "오늘의 일기",
      "text": "우래옥 웨이팅 내앞에 40팀",
      "posting_date": "2025-06-13 10:20:00",
      "user": {
        "user_id": 105,
        "nickname": "sohee",
        "name": "shinsohee"
      }
    }
~~~

## 포스트의 커맨드 조회하기
1. Endpoint
   - GET /posts/<post_id>/comments
2. Request parmas
   - post_id (int):  댓글을 조회할 게시물 ID
3. Description
   - 지정된 post_id의 커맨트 목록을 조회
   - 각 댓글에 user정보 포함
   
4. Response body
   - status (string): "success" 또는 "failed"
   - comments(arry):
     {
      post_id (int)
      comment_id (int)
      user_id (int)
      text (string)
     }
   - reason (string): 실패 시 원인
~~~
{
  "status": "success",
  "comments": [
          {
         "post_id": 101,
         "comment_id": 202,
         "user_id": 106,
         "text": "헉 진짜 맛있겠다"
       }
   ]
}
{
  "status": "failed",
  "reason": "Post not found"
}

~~~

## 특정 포스트의 커맨드 달기
1. Endpoint
   - POST /posts/<post_id>/comments
2. Request body
   - user_id (string) : post 작성한 사용자의 id, 필수
   - text (string) : 댓글 내용 (필수)
~~~
{
  "user_id": 105,
  "text": "저도 가봤어요! 진짜 맛있죠"
}
~~~
3. Description
   - 지정된 post_id의 커맨트 작성
   - user_id와 text 필수, 유효하지않은 경우 실패
   - 작성된 댓글은 ID와 함께 저장
   
4. Response body
   - status (string): "success" 또는 "failed"
   - comments(array):
     {
      post_id (int)
      comment_id (int)
      user_id (int)
      text (string)
     }
   - reason (string): 실패 시 원인
~~~
{
  "status": "success",
  "comments": [
    {
      "post_id": 101,
      "comment_id": 201,
      "user_id": 105,
      "text": "저도 가봤어요."
    }
  ]
}
{
  "status": "failed",
  "reason": "Missing required field: user_id"
}
{
  "status": "failed",
  "reason": "Post not found"
}
{
  "status": "failed",
  "reason": "User_id not found"
}

~~~

# 소셜
## 다른 사용자 조회

1. Endpoint
   - GET /users
2. Query parameters
   - user_id (int, optional): 조회할 대상 사용자 ID
   - nickname(string, optional) : 조회할 닉네임
     
3. Description
   - 사용자 또는 닉네임을 이용해 정보를 조회
   - 두 파라미터 중 하나 이상이 필요
   - 두 파라미터를 동시에 제공하면, AND로 조회
   - 조회 결과 없으면 실패
4. Response body
   - status (string): "success" 또는 "failed"
   - user (object): 사용자 정보 객체
   - reason (string): 실패 시 원인
  
~~~
{
  "status": "success",
  "user": {
    "user_id": 105,
    "nickname": "sohee",
    "name": "shinsohee"
  }
}
{
  "status": "failed",
  "reason": "User not found"
}
{
  "status": "failed",
  "reason": "Missing query: user_id or nickname required"
}

~~~

## 팔로우 신청

1. Endpoint
   - POST /follow

2. Request body
   - follower_no( int, 필수): 요청자 user_id
   - followee_no( int, 필수): 대상 user_id
~~~
{
  "follower_no": 105,
  "followee_no": 110
}
~~~
3. Description
   - 팔로우 요청을 생성한다.
4. Response body
   - status (string): "success" 또는 "failed"
   - request_no (int): 생성된 요청 번호
   - reason (string): 실패 시 원인
  
~~~
{
  "status": "succes",
  "request_no": 55
}
{
  "status": "failed",
  "reason": "User not found"
}
~~~


## 팔로우한 목록 조회

1. Endpoint
   - GET /users/<user_id>/followee
2. Request params
   - user_id (int): 팔로우 목록을 조회할 사용자 ID
3. Description
   - user_id가 팔로우한 사용자 목록을 반환
   - follow 테이블에서 follower_no = user_id 조건으로 조회
   - 상태가 accepted인 팔로우 관계만 조회
4. Response body
   - status (string): "success" 또는 "failed"
   - following (array):
     {
      user_id (int)
      name (string)
      nickname (string)
     }
   - reason (string): 실패 시 원인

  
~~~
{
  "status": "success",
  "followees": [
    {
      "user_id": 110,
      "nickname": "ming",
      "name": "민지"
    }
  ]
}
{
  "status": "failed",
  "reason": "User not found"
}
{
  "status": "failed",
  "reason": "No accepted followees"
}

~~~

## 자신에게 팔로우 요청한 목록 조회

1. Endpoint
   - GET /users/<user_id>/follow_requests
2. Request params
   - user_id (int): 요청을 받은 사용자 ID (= followee_no)
3. Description
   - user_id에게 온 팔로우 요청 목록을 조회
4. Response body
   - status (string): "success" 또는 "failed"
   - requests (array ): [
        {request_no (int): 팔로우 요청 ID
         follower_id (int): 팔로우 요청자 ID
         nickname (string): 요청자 닉네임
         name (string): 요청자 이름
        }
   - reason (string): 실패 시 원인
  
~~~
{
  "status": "success",
  "requests": [
    {
      "request_no": 301,
      "follower_id": 105,
      "nickname": "sohee",
      "name": "신소희"
    },
    {
      "request_no": 302,
      "follower_id": 108,
      "nickname": "jay",
      "name": "제이"
    }
  ]
}
{
  "status": "failed",
  "reason": "User not found"
}
{
  "status": "failed",
  "reason": "nothing"
}


~~~

## 팔로우 수락/거절

1. Endpoint
   - PATCH /follow_requests/<request_no>
2. Request body
   - action (string, required): "accept" 또는 "reject"
~~~
{
  "action": "accept"
}
~~~
3. Description
   - 해당 팔로우 요청을 수락하거나 거절한다.
   - status (string): "accepted" 또는 "rejected"
4. Response body
   - status (string): "success" 또는 "failed"
   - updated_status (string): 적용된 상태 ("accepted", "rejected")
   - reason (string): 실패 시 원인
  
~~~
{
  "status": "success",
  "updated_status": "accepted"
}
{
  "status": "success",
  "updated_status": "rejected"
}
{
  "status": "failed",
  "reason": "Request not found"
}
{
  "status": "failed",
  "reason": "Request already processed"
}
~~~

# 메세지
## DM 보내기

1. Endpoint
   - POST /messages
2. Request body
   - sender_id (int, required): 발신자 user_id
   - receiver_id (int, required): 수신자 user_id
   - text (string, required): 메시지 내용 
~~~
{
  "sender_no": 105,
  "receiver_no": 110,
  "text": "안녕"
}
~~~
3. Description
   - 새로운 DM을 생성하여 전송한다.
   - 빈 메세지를 보내는 것은 허용되지 않는다.

4. Response body
   - status (string): "success" 또는 "failed"
   - message_id (int): 생성된 메시지 번호(성공 시)
   - reason (string): 실패 시 원인
  
~~~
{
  "status": "success",
  "message_id": 200
}
{
  "status": "failed",
  "reason": "User not found"
}
{
  "status": "failed",
  "reason": "Text is required"
}
~~~

## DM 조회하기
1. Endpoint
   - GET /messages
2. Query parameters
   - receiver_id (int, 필수): 받은 메시지를 조회할 사용자 ID
3. Description
- 해당 사용자와 전체 또는 특정 상대방 간 DM 목록을 조회한다.
4. Response body
   - status (string): "success" 또는 "failed"
   - messages (array): [{ message_id, sender_id, text, send_at }]
~~~
{
  "status": "success",
  "messages": [
    {
      "message_id": 203,
      "sender_id": 110,
      "text": "안녕! 사진 잘 봤어 :)",
      "sent_at": "2025-06-13T13:50:00"
    }
   {
     "status": "failed",
     "reason": "User not found"
   }
   {
     "status": "failed",
     "reason": "Missing query parameter: receiver_id"
   }
}
~~~

#DM 삭제하기
1. Endpoint
   - DELETE /messages/<message_id>
2. Request params
   - messgae_id(int) : 삭제할 메세지
3. Request body
   - user_id (int) : 메세지를 삭제하려는 사용자 ID
4. Description
   - 해당 메세지를 보낸 사용자만 삭제 가능
   - 존재하지 않거나, 본인이 보낸 메세지가 아니면 실패
   
5. Response body
   - status (string): "deleted" 또는 "failed"
   - reason (string): 실패 시 원인
~~~
{
  "status": "success"
}
{
  "status": "failed",
  "reason": "Message not found"
}
{
  "status": "failed",
  "reason": "Permission denied"
}
{
  "status": "failed",
  "reason": "Missing required field: user_id"
}

~~~

