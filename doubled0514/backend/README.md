# REST API Spec.
- version 0.1 (2025/6/13)
# 사용자 계정
## 사용자 생성
1. Endpoint
   - POST /users
2. Request body 
   - nickname (string): 사용자 nickname, 필수
   - password(string) : 비밀번호,필수
   - name (string): 사용자 이름, 필수
   - age (int, optional): 사용자 나이
   - email (string, optional): 사용자 email 주소
~~~
{
  "nickname": "double_d_eo",
  "name": "김현서",
  "email": "doubled0514@gmail.com"
}
~~~
4. Description
   - 사용자 계정을 생성한다. 
   - nickname은 고유한 값이며 기존 사용자와 중복되면 생성이 실패한다.
5. Response body
   - status (string): created, failed
   - nickname: 생성 성공 시, nickname 반환
   - reason (string): 실패 시, 실패 원인
~~~
{
  "status": "created",
  "nickname": "double_d_eo"
}

{
  "status": "failed",
  "reason": "nickname is duplicated"
}
~~~
## 사용자 인증 (로그인)
1. Endpoint
  - POST/users/login
2. Requset body
  - nickname (string,필수) 
  - password(string,필수) : 사용자 비밀번호
~~~
{
   "nickname":"double_d_eo",
   "password" : "qwerty1234"
}
~~~
3. Description
  - 사용자 인증하여 로그인한다
  - 존재하지 않는 nickname이거나 password가 틀리면 로그인에 실패
4. Response Body
  - status(string) : success, failed
  - user_id(int): 로그인 성공시 user_id 반환
  - reason(string) : 실패시 실패 원인
~~~~
{
   "status" : "success",
   "user_id" : 105
}
{
   "status" : "failed",
   "reason" : "nickname or password is wrong"
}
~~~~
## 사용자 정보 조회
1.Endpoint
   - Get/users

2.Request body
   - user_id(int)
   - nickname(string)
   - email(string)

3.Description
   - 각 정보에 대응하는 사용자 정보를 조회한다

4.Response body
   - status : 성공,실패
   - nickname(string)
   - name(string)
   - age(int)
   - email(string)
   - reason : 실패시 이유 반환
~~~~
{
   "nickname" : "double_d_eo",
   "name" : "김현서",
   "age": "" ,
   "email" : "doubled0514@gamil.com"
}
~~~~
## 사용자 정보 수정
1. Endpoint
   - PUT/users/<user_id>/<password>
2. Request body
   - password(string,opt)
   - nickname(string,opt)
   - name(string,opt)
   - age(int,opt)
   - email(string,opt)
~~~
{
   "password":"qwerty123",
   "age" : 25
}
~~~  
3. description
   - 사용자 정보를 수정한다.
4. response body
   - status : success, failed
   - reason : 실패시, 실패 원인
~~~
{
   "status" : "success"
}
{
   "status" :"failed",
   "reason" : "invalid user_id or password"
}
~~~
## 사용자 삭제
1. Endpoint
   - DELETE/users/<user_id>/<password>
2. Request body 
   - 없음
4. Description
   - user_id에 해당하는 사용자 계정을 삭제한다.
   - user_id나 password가 틀리면 삭제 실패
5. Response body
   - status (string): deleted, failed
   - reason (string): 실패시, 실패 원인
~~~
{
  "status": "failed",
  "reason": "user_id, 101 doesn't exist"
}
~~~


# 포스팅
## 포스트 올리기
1. Endpoint
   - POST/posts
2. Request body
   - user_id(int,필수) 
   - title(string,필수)
   - text(string,필수)
3. Description
   - user_id 의 사용자가 포스트 작성
4. Resopnse body
   - stauts : success, failed
   - post_id(int) : 성공시 post id 반환
   - created_at(string) : 성공시 작성 시간 반환
   - reason(string) : 실패시 실패 이유

## 올라온 포스트 조회하기
1. Endpoint
   - GET/post
2. Request body
   - post_id(int,opt)
   - user_id(int,opt)
   - nickname(string,opt)
   - title(string,opt) : 문자 포함된 제목 조회
   - created_at(string,opt) : 날짜 범위로 조회
4. descriptionn
   - 전체 포스트를 조회한다
   - post_id, user_id, nickname,created_at에 기반해 조회할 수 있다
5. response body
   - [{"nickname":nickname, "title":title, "text":text,"created_at":created_at},
      {"nickname":nickname, "title":title, "text":text,"created_at":created_at}, ...]
   - status : success , failed
   - reason : 실패시 실패 원인
     
## 특정 포스트에 커멘트 달기
1. Endpoint
   -POST/posts/<post_id>/comment/<user_id>
2. Request body
   -text(string) : 커멘트
3. Description 
4. Response body
   - status(string) :성공, 실패
   - comment_id(int): 성공시 커멘트 ID 반환
   - reason(string): 실패시 이유


## 포스트의 코멘트 조회하기
1. Endpoint
   - GET/posts/<post_id>/comment
2. Request body
3. Description
   - post_id에 대응하는 사용자의 포스트의 코멘트 조회
   - users 테이블과 조인하여 글쓴이와 댓쓴이의 닉네임 조회
4. Respond body
   - status (string) : 실패,성공
   - reason (string) : 실패시 이유
   - [{"title":p.title,"text":p.text,"글쓴이":writer.nickname(string),"댓쓴이":commenter.nickname(string), "댓글":c.text},{"title":p.title,"text":p.text,"글쓴이":writer.nickname(string),"댓쓴이":commenter.nickname(string), "댓글":c.text}]

# 소셜
## 다른 사용자 조회 - #[사용자]의 사용자조회와 다른 기능인가?
1. Endpoint
   - GET/users
2. Request body
   - user_id(int,opt)
   - nickname(string,opt)
3. Description
   - 모든 user를 조회한다 
   - user_id 또는 nickname으로 조회할 수 있다
5. Response body
   - status(string) : 성공,실패
   - user_id
   - nickname
   - email
   - age(int)
  

## 팔로우 신청
1. Endpoint
   - Post/follow/<follower_id>/<followee_id>
2. Request body
3. Description
   - follower_id가 followee_id에게 팔로우 신청
4. response body
   - status (string) : pending
   - message (string) : 팔로우 신청 완료
   - reason (string) : 실패시 이유 
     
## 팔로우한 목록 조회
1. Endpoint
   - GEt/follow/following/<follower_id>
2. request body
3. description
   - user_id가 follower_id인 사용자가 팔로잉하고 있는 목록을 리스트로 조회
   - status가 accepted인 사용자만 조회
4. response body
   - followee_id (int)
   - nickname (string) : 팔로우 중인 유저 닉네임 조회
   - name(string) : 팔로우 중인 유저 이름
   - email(string) : 팔로우 중인 유저 이메일
  
## 자신에게 팔로우 요청한 목록 조회
1. Endpoint
   - GET/follow/request/<followee_id>
2. request body
3. description
   - followee_id가 user_id인 사용자를 팔로우 요청을 보낸 목록을 조회한다
   - status가 팔로우 요청 상태(pending)인 목록만 조회
4. response body
   - user_id(int) : 팔로우 요청한 유저의 id
   - nickname(string) : 팔로워 닉네임 조회
   - name (string) : 팔로워 이름
   - email (string) : 팔로워 이메일
  
## 팔로우를 수락/거절
1. Endpoint
   -PUT/follow/request/<followee_id>
2. request body
   - status(string) : 수락 or 거절
   - folower_id(int) : 팔로우 신청을 건 팔로워의 id
3. description
   - follower_id가 user_id인 사용자에게 걸려온 팔로우 신청을 수락할지 거절할지 결정
   - status가 pending인 상태만 
4. response body
   - status : 성공/실패
   - reason : 실패 시 이유
   
# 메시지
## DM 보내기
1. Endpoint
   - Post/message/<sender_id>/<receiver_id>
2. request body
   - text(string)
3. description
   - sender가 receiver에게 메시지 보냄
4. response body
   - message : 성공시 메시지 아이디 반환
   - status : 성공,실패
   - reason : 실패 이유 
## DM 조회하기
1. Endpoint
   - GET/message/<receiver_id>
2. request body
   - sender_id(int,opt)
   - created_at(string,opt)
   - message_id(int,opt)
   - text(string,opt)
3. description
   - receiver_id에게 온 모든 메시지를 조회한다
   - sender_id, message_id에 따라 조회 가능
   - text를 포함한 메시지 조회 (가능한가? like 써서 구현)
   - created_at으로 특정 시기부터 특정 시기까지의 메시지 조회
4. response body
   - sender_id
   - created_at
   - message_id
   - text

## DM 삭제하기
1. Endpoint
   - DELETE/message/<receiver_id>
2. request body
   - sender_id(int,opt)
   - message_id(int,opt)
   - created_at(str,opt)
   - text(string,opt)
3. description
   - receiver_id에게 온 모든 메시지를 삭제한다
   - sender_id,message_id에 해당하는 메시지만 지울 수 있다
   - created_at으로 특정 시기부터 특정 시기까지의 메시지를 삭제할 수 있다.
   - text를 포함한 메시지 조회 (가능한가? like 써서 구현)
4. response body
   - status : 삭제 성공, 실패
   - reason : 실패시 이유
