import pymysql
from flask import Flask, request

app = Flask(__name__)

def get_connection():
    return pymysql.connect(
        host='database-1.cts2qeeg0ot5.ap-northeast-2.rds.amazonaws.com',
        user='kevin',
        password='spreatics*',
        db='instagram_sohee',
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )
# 사용자 생성
@app.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()

    # 입력값 추출
    nickname = data['nickname']
    name = data['name']
    password = data['password']
    age = data.get('age')
    email = data.get('email')

    conn = get_connection()
    with conn.cursor() as cursor:
        try:
            sql = """
            INSERT INTO users (nickname, name, password, age, email) 
                values (%s, %s, %s, %s, %s)
            """
            cursor.execute(sql, (nickname, name, password, age, email))
            conn.commit()

            cursor.execute("SELECT user_id FROM users WHERE nickname = %s", (nickname,))
            result = cursor.fetchone()
            user_id = result['user_id']

        except pymysql.err.IntegrityError as e:
            return { "status": "failed", "reason": str(e) }
    conn.close()

    return {
        "status": "created",
        "user_id": user_id
    }

# 사용자 로그인
@app.route('/users/login', methods=['POST'])
def user_login():
    data = request.get_json()
    nickname = data['nickname']
    password = data['password']

    conn = get_connection()
    with conn.cursor() as cursor:
        sql = "SELECT user_id FROM users WHERE nickname = %s AND password = %s"
        cursor.execute(sql, (nickname, password))
        result = cursor.fetchone()

    conn.close()

    if result:
        user_id = result['user_id']
        return {
            'status': 'success',
            'user_id': user_id
        }
    else:
        return {
            'status': 'failed',
            'reason': 'nickname or password ERROR'
        }
    
# 사용자 정보 조회
@app.route('/users/<int:user_id>', methods=['GET'])
def get_user_info(user_id):
    conn = get_connection()
    with conn.cursor() as cursor:
        sql = "SELECT user_id, nickname, name, email FROM users WHERE user_id = %s"
        cursor.execute(sql, (user_id,))
        result = cursor.fetchone()
    conn.close()

    if result:
        return {
            "status": "success",
            "user": result
        }
    else:
        return {
            "status": "failed",
            "reason": "User not found"
        }
    
# 사용자 정보 수정

# 사용자 삭제
@app.route('/users/<int:user_id>', methods = ['DELETE'])
def del_user(user_id):
    conn = get_connection()
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM users WHERE user_id = %s", (user_id,))
        result = cursor.fetchone()

        if not result:
            conn.close()
            return {
                "status" : "failed",
                "reason" :"User not found"
            }

        cursor.execute("DELETE FROM users WHERE user_id = %s", (user_id,))
        conn.commit()

    conn.close()
    return {
        "status" : "deleted"
    }

app.run(debug=True, host='0.0.0.0', port=5001)