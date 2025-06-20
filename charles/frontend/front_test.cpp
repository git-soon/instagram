#include "httplib.h"
#include <iostream>
#include <string>

using namespace std;

int main() {
    httplib::Client cli("http://3.36.140.3:5000"); // 실제 서버 주소로 변경
    auto res = cli.Get("/");
    // 사용자 생성
    {
    string body = R"({
        "nickname": "charles1975",
        "password": "1234",
        "name" : "순순"
    })";
    res = cli.Post("/users", body, "application/json");
    
    if (res) {
        cout << res->body << endl;
    } else {
        cout << res.error() << endl;
    }
    }

    // 실습 1
    //  사용자 정보 가져오기
    // • Get() 사용
    // • request body가 없는 경우, endpoint만 만들어서 호출 하면 됨
    {
        int user_id = 1;
        string endpoint = "/users/" + to_string(user_id);
        res = cli.Get(endpoint);

        if (res) {
            cout << res->body << endl;
        } else {
            cout << res.error() << endl;
        }
    }

    // 실습 2
    // 사용자 삭제하기
    {
        int user_id = 1;
        string endpoint = "/users/" + to_string(user_id);
        res = cli.Delete(endpoint);

        if (res) {
            cout << res->body << endl;
        } else {
            cout << res.error() << endl;
        }
    }
        
    return 0;
}

// int main() {
//     // ── 사용자 생성 ──
//     {
//         httplib::Client cli("http://3.36.140.3");
//         auto res = cli.Post("/users", /* JSON body */);
//         if (res) cout << res->body << "\n";
//     }

//     // ── 사용자 조회 ──
//     {
//         httplib::Client cli("http://3.36.140.3");
//         int user_id = 1;
//         string endpoint = "/users/" + to_string(user_id);
//         auto res = cli.Get(endpoint);
//         if (res) cout << res->body << "\n";
//     }

//     // ── 사용자 삭제 ──
//     {
//         httplib::Client cli("http://3.36.140.3");
//         int user_id = 1;
//         string endpoint = "/users/" + to_string(user_id);
//         auto res = cli.Delete(endpoint);
//         if (res) cout << res->body << "\n";
//     }

//     return 0;
// }
