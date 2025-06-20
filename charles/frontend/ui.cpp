#include <iostream>
#include <string>
#include <stdlib.h>
#include "httplib.h"
#include "json.hpp"

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
            m_2_1_1_ser_user(); // "1. 사용자 자신 정보조회"
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

void m_2_1_1_ser_user() {

}

void m_2_1_2_change_inf() {

}

void m_2_1_3_follow_m() {

}

void m_2_1_4_post_m() {

}

void m_2_1_5_del_user() {

}



void m_2_2_others() {
    cout << "다른 사용자 메뉴 처리" << endl;
}

void m_3_post() {
    while (2) {
        // 메뉴 출력
        cout << "[2. 사용자]" << endl;
        cout << "1. 본인" << endl;
        cout << "2. 다른 유저" << endl;
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