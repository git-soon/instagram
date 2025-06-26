#include <iostream>
#include <string>
#include <stdlib.h>
#include "httplib.h"
#include "json.hpp"
#include <my_sql.h>

using namespace std;
using namespace httplib;
using namespace nlohmann;
using json = nlohmann::json;

Client cli("http://3.36.140.3:5000");

// 0. 메인
//      1. 로그인
//      2. 사용자
//          2-1. 본인
//          2-2. 다른 유저
//      3. 소셜
//      4. DM 

// 모든곳에 로그인 안했으면 로그인 페이지로 보낼수 있도록 할까?

void m_0_mainMenu() {
    
    while (1) {
        // 메뉴 출력
        cout << "[홈메뉴]" << endl;
        cout << "1. 로그인" << endl;
        cout << "2. 사용자" << endl;
        cout << "3. 포스팅?" << endl;
        cout << "4. DM" << endl;
        cout << "5. 종료" << endl;
        
        // 사용자 입력 처리
        int input;
        cin >> input;
        switch(input) {
            case 1:
            m_0_1_login_select(); // 로그인과 회원가입 창으로
            break;

            case 2:
            m_2_user();
            break;
            
            case 3:
            cout <<  "not yet" ;
            break;
            
            case 4:
            cout <<  "not yet" ;
            break;
            case 5:
            cout <<  "Quit program" ;
            return exit(0);
            break;

            default:
            // ?
            break;
        }
    }
}

void m_0_1_login_select() {
    // 로그인과 유저생성 선택창
    int input;
    cin >> input;
    
    switch(input) {
        cout << "\n[1. 로그인]\n";
        cout << "\n[2. 회원 가입]\n";
        
        case 1:
        m_1_1_login();
        break;
        
        case 2:
        m_1_1_create_user();
        break;
        
    }
}

void m_1_1_login() {
    // 로그인창
    string nickname, password;
    
    cout << "  nickname: ";
    cin >> nickname;
    cout << "  password: ";
    cin >> password;

    // 2) JSON body 에 dict 처럼 담기
    json body;
    body["nickname"] = nickname;
    body["password"] = password;

    // 3) HTTP POST
    auto res = cli.Post(
        "/login",             // 로그인용 엔드포인트
        body.dump(),          // string 으로 변환된 JSON
        "application/json"    // Content-Type
    );

    if (nickname & password == db) {
       cout << "로그인 성공! 사용자 메뉴로 이동합니다.\n\n";
       return m_2_user();
    }

    else {
        cout << "로그인 실패. 다시 시도하세요.\n\n";
        return m_1_1_login();
    }



}

void m_1_1_create_user() {
    string nickname;
    string name;
    string password;
    string email;
    int age;

    // --- 사용자 입력 받기 
    cout << "Nickname: ";
    getline(cin, nickname);

    cout << "Name: ";
    getline(cin, name);

    cout << "Password: ";
    getline(cin, password);

    cout << "Email: ";
    getline(cin, email);

    cout << "Age: ";
    cin >> age;
    cin.ignore(numeric_limits<streamsize>::max(), '\n');  // 남은 개행문자 제거

    // --- json 객체에 dict처럼 키-값 쌍 할당 ---
    json body;
    body["nickname"] = nickname;
    body["name"]     = name;
    body["password"] = password;
    body["email"]    = email;
    body["age"]      = age;

    //  dump()가 string을 리턴하므로, httplib.Post() 에 바로 넘길 수 있습니다.
    string payload = body.dump(/* indent= */ 2);  // indent를 주면 사람이 보기 좋게 pretty print

    cout << "\n=== POST /users 요청 바디 (pretty) ===\n";
    cout << payload << "\n";

    // --- 실제 HTTP 요청 예시 ---
    auto res = cli.Post(
      "/create_users",
      payload,
      "application/json"

    );

    if (res && res->status == 200) {
        cout << "회원가입 성공: " << res->body << endl;
    } else {
        cout << "요청 실패: HTTP status="
             << (res ? res->status : 0) << endl;
    }
    }
    
    void m_2_user() {
        while (1) {
            // 메뉴 출력
            cout << "[2. 사용자]" << endl;
            cout << "1. 본인" << endl;
            cout << "2. 다른 유저" << endl;
            cout << "3. 뒤로가기" << endl;
    
            // 사용자 입력 처리
            int input;
            cin >> input;
    
            switch(input) {
                case 1:
                    m_2_1_self(); // 1. 본인 정보 조회
                    break;
                case 2:
                    m_2_2_others(); // 2. 다른 유저
                    break;
                case 3:
                    return m_0_mainMenu(); // 3. 뒤로가기
                    break;
    
            }
        }
    }
    
    void m_2_1_self() { 
    // 본인 정보 조회
    while (2){

        cout << "[본인 메뉴 처리]" << endl;
        cout << "1. 사용자 자신 정보조회" << endl;
        cout << "2. 정보변경" << endl;
        cout << "3. 팔로워 관리" << endl;
        cout << "4. 포스트 관리" << endl;
        cout << "5. 유저 삭제" << endl;

        // 사용자 입력 처리
        int input;
        cin >> input;
        switch(input) {
            case 1:
            m_2_1_1_user_info(); // "1. 사용자 자신 정보조회"
            break;

            case 2:
            m_2_1_2_change_inf(); //"2. 정보변경"
            break;
            
            case 3:
            m_2_1_3_follow_m(); //3. 팔로워 관리
            break;
            
            case 4:
            m_2_1_4_post_m();// "4. 포스트 관리"
            break;

            case 5:
            m_2_1_5_del_user();; // "5. 유저 삭제"
            return exit(0);
            break;

            default:
            // ?
            break;
        }
        
    }
    
}

void m_2_1_1_user_info() {
    // 사용자 정보 조회
   get("/user/<user_id>/info", [](const Request& req, Request& res)){
    // 사용자 정보 조회 로직
    // 사용자 정보를 json.hpp 라이브러리 사용하여 딕셔너리 형태로 반환
    return json user_info{
        {"nickname", nickname},
        {"name", name},
        {"age", age},
        {"email", email},
        {"password", password},
        {"followers", followers},
        {"followees", followees},
        {"posts", posts_id}
    };


};
}
void m_2_1_2_change_inf() {
    // 사용자 정보 변경
    put("/user/<user_id>/change",[](const Request& req, Request& res)){
        // 사용자 정보 변경 로직
        json body = json::parse(req.body());
        string nickname = body["nickname"];
        string name = body["name"];
        int age = body["age"];

        // DB 업데이트 로직
        db.update_user_info({
            {"nickname", nickname},
            {"name", name},
            {"age", age},
        })

    };
}

void m_2_1_3_follow_m() {
    //팔로우 관리
    while (2) {
        // 메뉴 출력
        cout << "[팔로우 관리]" << endl;
        cout << "1. 팔로우" << endl;
        cout << "2. 언팔로우" << endl;
        cout << "3. 팔로워 목록" << endl;
        cout << "4. 팔로잉 목록" << endl;
        cout << "5. 뒤로가기" << endl;

        // 사용자 입력 처리
        int input; 
        cin >> input;

        switch(input) {
            case 1:
                // 팔로우 로직
                cout << "팔로우할 사용자의 ID를 입력하세요: ";
                int follow_id;
                cin >> follow_id;
                // 팔로우 로직 구현
                json follow_body;
                follow_body["follow_id"] = follow_id; 
                auto follow_res = cli.Post(
                    "/follow", 
                    follow_body.dump(), 
                    "application/json"
                );
                break;
                
            case 2:
                // 언팔로우 로직
                cout << "언팔로우할 사용자의 ID를 입력하세요: ";
                int unfollow_id;
                cin >> unfollow_id;
                // 언팔로우 로직 구현
                json unfollow_body;
                unfollow_body["unfollow_id"] = unfollow_id;
                auto unfollow_res = cli.Post(
                    "/unfollow", 
                    unfollow_body.dump(), 
                    "application/json"
                );

                break;

            case 3:
                // 팔로워 목록 조회 로직
                cout << "팔로워 목록 조회 로직" << endl;
                auto followers_res = cli.Get("/followers");
                if (followers_res && followers_res->status == 200) {
                    json followers = json::parse(followers_res->body);
                    cout << "팔로워 목록: " << followers.dump(2) << endl;
                } else {
                    cout << "팔로워 목록 조회 실패." << endl;
                }
                // 팔로워 목록 조회 로직 구현
                // 예시로 팔로워 목록을 출력
                // json followers = {{"user1", "User One"}, {"user2", "User Two"}};
                // cout << "팔로워 목록: " << followers.dump(2) << endl;
                // 실제로는 서버에서 팔로워 목록을 받아와서 출력해야 함 
                break;

            case 4:
                // 팔로잉 목록 조회 로직
                cout << "팔로잉 목록 조회 로직" << endl;
                auto following_res = cli.Get("/following");
                if (following_res && following_res->status == 200) {
                    json following = json::parse(following_res->body);
                    cout << "팔로잉 목록: " << following.dump(2) << endl;
                } else {
                    cout << "팔로잉 목록 조회 실패." << endl;
                }   
                // 팔로잉 목록 조회 로직 구현
                // 예시로 팔로잉 목록을 출력    
                // json following = {{"user1", "User One"}, {"user2", "User Two}};
                // cout << "팔로잉 목록: " << following.dump(2) << endl;
                // 실제로는 서버에서 팔로잉 목록을 받아와서 출력해야 함
                break;
            case 5:
                return m_2_user(); // 뒤로가기
                break;
            default:
                cout << "잘못된 입력입니다." << endl;
                break;
        }
    }

}

void m_2_1_4_post_m() {
    // 포스트 관리
    while (2) {
        // 메뉴 출력
        cout << "[포스트 관리]" << endl;
        cout << "1. 포스트 작성" << endl;
        cout << "2. 포스트 수정" << endl;
        cout << "3. 포스트 삭제" << endl;
        cout << "4. 내 포스트 목록" << endl;
        cout << "5. 뒤로가기" << endl;

        // 사용자 입력 처리
        int input; 
        cin >> input;

        switch(input) {
            case 1:
                // 포스트 작성 로직
                cout << "포스트 내용을 입력하세요: ";
                string post_content;
                cin.ignore(); // 개행 문자 제거
                getline(cin, post_content);
                json post_body;
                post_body["content"] = post_content; 
                auto post_res = cli.Post(
                    "/posts", 
                    post_body.dump(), 
                    "application/json"
                );
                break;
            case 2:
                // 포스트 수정 로직
                cout << "수정할 포스트의 ID를 입력하세요: ";
                int post_id;
                cin >> post_id;
                cout << "새로운 포스트 내용을 입력하세요: ";
                cin.ignore(); // 개행 문자 제거
                getline(cin, post_content);
                json update_body;
                update_body["post_id"] = post_id; 
                update_body["content"] = post_content; 
                auto update_res = cli.Put(
                    "/posts/" + to_string(post_id), 
                    update_body.dump(), 
                    "application/json"
                );
                break;
            case 3:
                // 포스트 삭제 로직
                cout << "삭제할 포스트의 ID를 입력하세요: ";
                int delete_post_id;
                cin >> delete_post_id;
                auto delete_res = cli.Delete("/posts/" + to_string(delete_post_id));
                break;
            case 4:
                // 내 포스트 목록 조회 로직
                auto posts_res = cli.Get("/posts");
                if (posts_res && posts_res->status == 200) {
                    json posts = json::parse(posts_res->body);
                    cout << "내 포스트 목록: " << posts.dump(2) << endl;
                } else {
                    cout << "포스트 목록 조회 실패." << endl;
                }
                
            case 5:
            return m_2_user(); // 뒤로
}

void m_2_1_5_del_user() {
    // 유저 삭제
    cout << "정말로 유저를 삭제하시겠습니까? (y/n): ";
    char confirm;
    cin >> confirm;
    if (confirm == 'y' || confirm == 'Y') {
        // 유저 삭제 로직
        auto res = cli.Delete("/user/<user_id>");
        if (res && res->status == 200) {
            cout << "유저 삭제 성공." << endl;
        } else {
            cout << "유저 삭제 실패." << endl;
        }
    } else {
        cout << "유저 삭제 취소." << endl;
    }
}



void m_2_2_others() {
    cout << "다른 사용자 메뉴 처리" << endl;
}

void m_3_post() {
    while (2) {
        // 메뉴 출력
        cout << "[포스팅]" << endl;

        cout << "3. 뒤로가기" << endl;

        // 사용자 입력 처리
        int input; 
        cin << input;

        switch(input) {
            case 1:
                m_2_1_self();
                break;
            case 2:
                m_2_2_others();
                break;
            case 3:
                return m_0_mainMenu();
                break;
            }
    }
}

int main() {

    m_0_mainMenu();

    return 1;
}