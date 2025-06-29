import json
import pymysql
import traceback
import bcrypt
from flask import Flask, request, jsonify, session
from pymysql.cursors import DictCursor


app = Flask(__name__)

# MySQL 연결 함수


def get_connection():
    with open('connect_data.json', encoding='utf-8') as f:
        config = json.load(f)
        cd = config['connect_data']
    return pymysql.connect(
        host=cd['host'],
        user=cd['user'],
        password=cd['password'],
        db=cd['db'],
        charset=cd.get('charset', 'utf8mb4'),
        cursorclass=pymysql.cursors.DictCursor    # ← 클래스 객체로 지정
    )


@app.route('/connect', methods=['GET'])
def connect_db():
    try:
        with open('connect_data.json', encoding='utf-8') as f:
            config = json.load(f)
            cd = config['connect_data']
        conn = pymysql.connect(
            host=cd['host'],
            user=cd['user'],
            password=cd['password'],
            db=cd['db'],
            charset=cd.get('charset', 'utf8mb4'),
            cursorclass=DictCursor
        )
        return {'status': 'success', 'message': 'Database connection successful'}, 200
    except Exception as e:
        return {'status': 'error', 'message': str(e)}, 500


# 사용자 생성

@app.route('/users', methods=['POST'])
def create_user():
    # 1. Content-Type 체크 (클라이언트가 application/json 으로 보냈는지)
    if not request.is_json:
        return jsonify({'error': 'Content-Type must be application/json'}), 415

    data = request.get_json()
    nickname = data.get('nickname')
    name = data.get('name')
    password = data.get('password')
    age = data.get('age')    # optional
    email = data.get('email')  # optional

    if not nickname or not name or not password:
        return jsonify({'error': 'Nickname, name, and password are required.'}), 400

    # 4. 비밀번호 해싱
    hashed_pw = bcrypt.hashpw(password.encode(
        'utf-8'), bcrypt.gensalt()).decode('utf-8')

    # 5. DB에 저장
    conn = get_connection()
    with conn.cursor() as cursor:
        try:
            sql = """
            INSERT INTO users (nickname, name, password, age, email)
            VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute(sql, (nickname, name, hashed_pw, age, email))
            conn.commit()

        # user_id = cursor.lastrowid #지금 뭔가 설계한거랑 이거 다른거 같은데...... 아닌가? user_id = user_no, nickname = id로 하는거였나?

        except pymysql.err.IntegrityError as ie:  # 닉네임 중복 등 UNIQUE 위반
            return jsonify({'error': 'Nickname already exists.'}), 409

        except Exception as e:  # 전체 스택 트레이스 문자열로 가져오기
            tb = traceback.format_exc()
            return jsonify({
                'error': str(e),
                'trace': tb.splitlines()
            }), 500

    # 6. 생성 성공 응답
    return jsonify({
        'status':   'created',
        'user_id':  cursor.fetchone,
        'nickname': nickname
    }), 201


# # 사용자 인증 (로그인)

@app.route('/users/login', methods=['POST'])
def login_user():
    if not request.is_json:
        return jsonify({'error': 'Content-Type must be application/json'}), 415

    data = request.get_json()
    nickname = data.get('nickname')
    password = data.get('password')

    if not nickname or not password:
        return jsonify({'error': 'Nickname and password are required.'}), 400

    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                "SELECT user_id, password FROM users WHERE nickname = %s",
                (nickname,)
            )
            user = cursor.fetchone()

        if not user:
            return jsonify({'status': 'denied', 'reason': 'Invalid nickname or password.'}), 401

        # DB에 저장된 해시 (문자열) → 바이트로 변환
        stored_hash = user['password'].encode('utf-8')
        # 입력한 비밀번호(str) → 바이트
        raw_pw_bytes = password.encode('utf-8')

        if not bcrypt.checkpw(raw_pw_bytes, stored_hash):
            return jsonify({'status': 'denied', 'reason': 'Invalid nickname or password.'}), 401

        return jsonify({'status': 'success', 'user_id': user['user_id']}), 200

    except Exception as e:
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500


# # 사용자 정보 조회


@app.route('/users/<int:user_no>', methods=['GET'])
def get_user(user_no):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            sql = """
            SELECT user_id, nickname, name, age, email 
            FROM users 
            WHERE user_id = %s
            """

            cursor.execute(sql, (user_no,))
            user = cursor.fetchone()

            if not user:
                return jsonify({'status': 'failed', 'reason': f'user_no {user_no} not found'}), 404

            return jsonify({
                'status': 'success',
                'user': {
                    'user_no': user['user_id'],
                    'nickname': user['nickname'],
                    'name': user['name'],
                    'age': user.get('age'),
                    'email': user.get('email')
                }
            }), 200

    except Exception as e:
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500


# # 사용자 정보 수정


@app.route('/users/<int:user_no>', methods=['PUT'])
def update_user(user_no):
    if not request.is_json:
        return jsonify({'error': 'Content-Type must be application/json'}), 415

    data = request.get_json()
    nickname = data.get('nickname')
    name = data.get('name')
    password = data.get('password')
    age = data.get('age')
    email = data.get('email')

    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            sql = """
            UPDATE users 
            SET nickname = COALESCE(%s, nickname),
                name = COALESCE(%s, name),
                password = COALESCE(%s, password),
                age = COALESCE(%s, age),
                email = COALESCE(%s, email)
            WHERE user_id = %s
            """
            hashed_pw = bcrypt.hashpw(password.encode(
                'utf-8'), bcrypt.gensalt()).decode('utf-8') if password else None
            cursor.execute(
                sql, (nickname, name, hashed_pw, age, email, user_no))
            if cursor.rowcount == 0:
                return jsonify({'status': 'failed', 'reason': f'user_no {user_no} not found'}), 404

        conn.commit()

        # 수정된 사용자 정보 조회
        cursor.execute(
            "SELECT user_id, nickname, name, age, email FROM users WHERE user_id = %s", (user_no,))
        user = cursor.fetchone()

        return jsonify({
            'status': 'updated',
            'user': {
                'user_no': user['user_id'],
                'nickname': user['nickname'],
                'name': user['name'],
                'age': user.get('age'),
                'email': user.get('email')
            }
        }), 200

    except pymysql.err.IntegrityError as ie:
        return jsonify({'error': str(ie)}), 409

    except Exception as e:
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500


# # 사용자 삭제

@app.route('/users/<int:user_no>', methods=['DELETE'])
def delete_user(user_no):
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            sql = "DELETE FROM users WHERE user_id = %s"
            cursor.execute(sql, (user_no,))
            if cursor.rowcount == 0:
                return jsonify({'status': 'failed', 'reason': f'user_no {user_no} doesn\'t exist'}), 404

        conn.commit()
        return jsonify({'status': 'deleted'}), 200

    except Exception as e:
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500


# 포스트 생성

@app.route('/post/create', methods=['POST'])
def create_post():
    user_id = session.get('user_id')
    # 로그인 해야 접근가능
    # 1) Content-Type 체크
    if not request.is_json:
        return jsonify({'status': 'failed', 'reason': 'Content-Type must be application/json'}), 415

    # 2) JSON 파싱
    data = request.get_json()
    user_no = data.get('user_no')
    text = data.get('text')    # optional

    # 3) 필수 필드 검증
    if user_no is None:
        return jsonify({'status': 'failed', 'reason': 'user_no is required'}), 400

    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            sql = """
            INSERT INTO posts (user_no, text)
            VALUES (%s, %s)
            """
            cursor.execute(sql, (user_no, text))
            conn.commit()
            post_id = cursor.lastrowid

        return jsonify({'status': 'created', 'post_id': post_id}), 201

    except pymysql.err.IntegrityError as ie:
        # 예: 외래키(user_no) 제약 위반
        return jsonify({'status': 'failed', 'reason': str(ie)}), 409

    except Exception as e:
        traceback.print_exc()
        return jsonify({'status': 'failed', 'reason': 'Internal server error'}), 500

# 올라온 포스트 조회하기


@app.route('/post', methods=['GET'])
def view_post():
    data = request.get_json()
    try:
        user_id = data.get('user_id')
        post = data.get('text')

        if not title or not content or not user_id:
            return jsonify({'error': 'Missing required fields'}), 400

        connection = get_connection()

        with connection.cursor() as cursor:
            sql = "INSERT INTO posts (title, content, user_id, text) VALUES (%s, %s, %s, %s)"
            cursor.execute(sql, (title, content, user_id, text))
            connection.commit()

        return jsonify({'message': 'Post created successfully', 'post_id': cursor.lastrowid}), 201

    # 4. Response body
    # - status(string): "created" 또는 "failed"
    # - post_id(int): 생성된 포스트 번호
    # - reason(string): 실패 시 원인

    except Exception as e:
        traceback.print_exc()
        return jsonify({'error': 'Failed to create post'}), 500

 # 포스트의 커맨트 조회하기


@app.route('/posts/<int:post_id>/comments', methods=['GET'])
def get_comments(post_id):
    try:
        Connection = get_connection()
        with Connection.cursor() as cursor:
            sql = """
            SELECT *
            FROM comments
            WHERE post_id = %s"""

        cursor.execute(sql, (post_id,))
        comments = cursor.fetchall()
        return jsonify({'status': 'success', 'comments': comments}), 200

    except Exception as e:
        traceback.print_exc()
        return jsonify({'error': 'Failed to retrieve comments'}), 500

    ...  # 이거 구현하려면 특정인원 검색한 포스트, 특정 단어가 들어간 포스트 이렇게 구성해야되지 않나?


# 특정 포스트에 커맨트 달기
# 2. Request body
# - user_no(int, required): 작성자 user_no
# - text(string, required): 커맨트 내용

@app.route('/posts/<int:post_id>/comments', methods=['POST'])
def create_comment(post_id):
    data = request.get_json()
    post_id = post_id  # URL 파라미터로 가져옴? 이게 아니라 포스트 에 작성하는거니까 필요하지 않나?
    user_id = data.get('user_id')
    text = data.get('text')

    if not user_id or not text:
        return jsonify({'error': 'Missing required fields'}), 400

    try:
        connection = get_connection()
        with connection.cursor() as cursor:
            sql = "INSERT INTO comments (post_id, user_id, text) VALUES (%s, %s, %s)"
            cursor.execute(sql, (post_id, user_id, text))
            connection.commit()

        return jsonify({'message': 'Comment created successfully', 'comment_id': cursor.lastrowid}), 201

    except Exception as e:
        traceback.print_exc()
        return jsonify({'error': 'Failed to create comment'}), 500


# ===================================================================================
if __name__ == '__main__':
    print("registered routes:", app.url_map)  # URL 경로 확인
    app.run(debug=True, use_reloader=False, host='0.0.0.0', port=5000)
