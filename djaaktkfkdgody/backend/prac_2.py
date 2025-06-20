# Flask: 웹 프레임워크
from flask import Flask, request, jsonify

# 비밀번호 해싱 및 검증을 위한 werkzeug 보안 도구
from werkzeug.security import generate_password_hash, check_password_hash

# MySQL과의 연결을 위한 라이브러리
import pymysql

# Flask 애플리케이션 인스턴스 생성
app = Flask(__name__)

# ✅ DB 연결 함수
def get_connection():
    # 매 요청마다 새 DB 연결 생성 (RDS MySQL 연결 정보 포함)
    return pymysql.connect(
        host='database-1.cts2qeeg0ot5.ap-northeast-2.rds.amazonaws.com',
        user='pdohee',
        password='gamzagoguma',
        db='instagram_gamza',
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor  # 결과를 dict로 반환
    )

# ✅ 사용자 생성 및 검색
@app.route('/users', methods=['GET', 'POST'])
def users():
    if request.method == 'POST':
        # 클라이언트에서 보낸 JSON 파싱
        data = request.get_json()

        # 필수 필드 체크
        if not all(field in data for field in ['nickname', 'name', 'password', 'email']):
            return jsonify({"status": "failed", "reason": "Missing fields"})

        # DB 연결 및 사용자 중복 확인 + 등록
        conn = get_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute("SELECT * FROM users WHERE nickname=%s", (data['nickname'],))
                if cursor.fetchone():
                    return jsonify({"status": "failed", "reason": "Nickname already exists"})

                # 비밀번호 해싱 후 사용자 등록
                hashed = generate_password_hash(data['password'])
                cursor.execute(
                    "INSERT INTO users (nickname, name, password, email) VALUES (%s, %s, %s, %s)",
                    (data['nickname'], data['name'], hashed, data['email'])
                )
                conn.commit()
                return jsonify({"status": "created", "user_id": cursor.lastrowid})
        finally:
            conn.close()

    # GET 요청: 닉네임 또는 이름으로 사용자 검색
    keyword = request.args.get('keyword', '')
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            like = f"%{keyword}%"
            cursor.execute("SELECT user_id, nickname FROM users WHERE nickname LIKE %s OR name LIKE %s", (like, like))
            result = cursor.fetchall()
            for user in result:
                user['profile_image'] = "https://cdn.example.com/profiles/default.jpg"
    finally:
        conn.close()
    return jsonify(result)

# ✅ 로그인 기능
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    nickname = data.get("nickname")
    password = data.get("password")

    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            # 닉네임으로 사용자 검색
            cursor.execute("SELECT * FROM users WHERE nickname=%s", (nickname,))
            user = cursor.fetchone()
            if not user:
                return jsonify({"status": "failed", "reason": "User not found"})

            # 비밀번호 검증
            if check_password_hash(user['password'], password):
                return jsonify({"status": "login success", "user_id": user['user_id'], "nickname": user['nickname']})
            else:
                return jsonify({"status": "failed", "reason": "Invalid credentials"})
    finally:
        conn.close()

# ✅ 사용자 상세 조회 / 수정 / 삭제
@app.route('/users/<int:user_id>', methods=['GET', 'PUT', 'DELETE'])
def user_detail(user_id):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            if request.method == 'GET':
                # 특정 사용자 정보 조회
                cursor.execute("SELECT user_id, nickname, name, email FROM users WHERE user_id=%s", (user_id,))
                user = cursor.fetchone()
                if user:
                    return jsonify(user)
                return jsonify({"status": "failed", "reason": "User not found"})

            elif request.method == 'PUT':
                # 사용자 정보 수정 (입력된 항목만 수정)
                data = request.json
                fields = []
                values = []
                for k in ['name', 'password', 'email']:
                    if k in data:
                        val = generate_password_hash(data[k]) if k == 'password' else data[k]
                        fields.append(f"{k}=%s")
                        values.append(val)
                values.append(user_id)
                if fields:
                    cursor.execute(f"UPDATE users SET {', '.join(fields)} WHERE user_id=%s", values)
                    conn.commit()
                return jsonify({"status": "updated"})

            elif request.method == 'DELETE':
                # 사용자 삭제
                cursor.execute("DELETE FROM users WHERE user_id=%s", (user_id,))
                conn.commit()
                return jsonify({"status": "deleted"})
    finally:
        conn.close()

# ✅ 게시물 등록 및 조회
@app.route('/posts', methods=['POST', 'GET'])
def posts():
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            if request.method == 'POST':
                # 게시물 등록
                data = request.get_json()
                cursor.execute(
                    "INSERT INTO posts (user_id, title, text) VALUES (%s, %s, %s)",
                    (data['user_id'], data['title'], data['text'])
                )
                conn.commit()
                return jsonify({"status": "post created", "post_id": cursor.lastrowid})

            # 게시물 조회: 전체 또는 특정 사용자 기준
            user_id = request.args.get('user_id')
            if user_id:
                cursor.execute("SELECT * FROM posts WHERE user_id=%s", (user_id,))
            else:
                cursor.execute("SELECT * FROM posts")
            return jsonify(cursor.fetchall())
    finally:
        conn.close()

# ✅ 댓글 작성
@app.route('/posts/<int:post_id>/comment', methods=['POST'])
def add_comment(post_id):
    data = request.json
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                "INSERT INTO comments (post_id, user_id, text) VALUES (%s, %s, %s)",
                (post_id, data['user_id'], data['comment'])
            )
            conn.commit()
            return jsonify({"status": "created", "comment_id": cursor.lastrowid})
    finally:
        conn.close()

# ✅ 댓글 목록 조회
@app.route('/posts/<int:post_id>/comments', methods=['GET'])
def get_comments(post_id):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM comments WHERE post_id=%s", (post_id,))
            return jsonify(cursor.fetchall())
    finally:
        conn.close()

# ✅ 팔로우 요청 보내기
@app.route('/follow/request', methods=['POST'])
def follow_request():
    data = request.json
    follower_id = data['from_user_id']
    followee_id = data['to_user_id']

    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            # 이미 팔로우 요청이 있는지 확인
            cursor.execute("SELECT * FROM follows WHERE follower_id=%s AND followee_id=%s", (follower_id, followee_id))
            if cursor.fetchone():
                return jsonify({"status": "already_requested_or_following"})

            # 팔로우 요청 생성
            cursor.execute("INSERT INTO follows (follower_id, followee_id) VALUES (%s, %s)", (follower_id, followee_id))
            conn.commit()
            return jsonify({"status": "requested"})
    finally:
        conn.close()

# ✅ 내가 받은 팔로우 요청 목록 조회
@app.route('/follow/requests', methods=['GET'])
def get_follow_requests():
    user_id = int(request.args.get('user_id'))

    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT f.follow_id, f.follower_id, u.nickname
                FROM follows f
                JOIN users u ON f.follower_id = u.user_id
                WHERE f.followee_id=%s AND f.status='pending'
            """, (user_id,))
            requests = cursor.fetchall()
            for r in requests:
                r['profile_image'] = "https://cdn.example.com/profiles/default.jpg"
            return jsonify(requests)
    finally:
        conn.close()

# ✅ 팔로우 요청 수락 / 거절
@app.route('/follow/respond', methods=['POST'])
def follow_respond():
    data = request.json
    follow_id = data['request_id']
    action = data['action']

    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            if action == "accept":
                cursor.execute("UPDATE follows SET status='accepted' WHERE follow_id=%s", (follow_id,))
                conn.commit()
                return jsonify({"status": "accepted"})
            elif action == "reject":
                cursor.execute("DELETE FROM follows WHERE follow_id=%s", (follow_id,))
                conn.commit()
                return jsonify({"status": "rejected"})
            else:
                return jsonify({"status": "failed", "reason": "invalid action"})
    finally:
        conn.close()

# ✅ 내가 팔로우한 사용자 목록
@app.route('/follow/list', methods=['GET'])
def get_following():
    user_id = int(request.args.get('user_id'))

    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT u.user_id, u.nickname
                FROM follows f
                JOIN users u ON f.followee_id = u.user_id
                WHERE f.follower_id = %s AND f.status='accepted'
            """, (user_id,))
            result = cursor.fetchall()
            for r in result:
                r['profile_image'] = "https://cdn.example.com/profiles/default.jpg"
            return jsonify(result)
    finally:
        conn.close()

# ✅ DM 보내기
@app.route('/dm', methods=['POST'])
def send_dm():
    data = request.json
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                "INSERT INTO messages (sender_id, receiver_id, text) VALUES (%s, %s, %s)",
                (data['from_user_id'], data['to_user_id'], data['message'])
            )
            conn.commit()
            return jsonify({"status": "sent", "dm_id": cursor.lastrowid})
    finally:
        conn.close()

# ✅ 특정 사용자 간 DM 대화 조회
@app.route('/dm/conversation', methods=['GET'])
def get_dm_conversation():
    uid1 = int(request.args.get("user1_id"))
    uid2 = int(request.args.get("user2_id"))

    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT * FROM messages
                WHERE (sender_id=%s AND receiver_id=%s)
                   OR (sender_id=%s AND receiver_id=%s)
                ORDER BY created_at
            """, (uid1, uid2, uid2, uid1))
            return jsonify(cursor.fetchall())
    finally:
        conn.close()

# ✅ DM 삭제
@app.route('/dm/<int:dm_id>', methods=['DELETE'])
def delete_dm(dm_id):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("DELETE FROM messages WHERE message_id=%s", (dm_id,))
            conn.commit()
            return jsonify({"status": "deleted"})
    finally:
        conn.close()

# ✅ 서버 실행 (개발용)
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
