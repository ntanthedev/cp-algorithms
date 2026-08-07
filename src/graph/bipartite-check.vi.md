---
tags:
  - Translated
e_maxx_link: bipartite_checking
translation:
  source: graph/bipartite-check.md
  source_commit: a5af6c1846c9009af5d6d2851d90d1a48b9fd206
  status: draft
  last_synced: 2026-08-07
---

# Kiểm tra đồ thị hai phía

Đồ thị hai phía (bipartite graph) là đồ thị có thể chia tập đỉnh thành hai tập rời nhau sao cho mỗi cạnh đều nối hai đỉnh thuộc hai tập khác nhau; nói cách khác, không có cạnh nào nối hai đỉnh trong cùng một tập. Hai tập này thường được gọi là hai phía của đồ thị.

Cho một đồ thị vô hướng. Hãy kiểm tra đồ thị có phải là đồ thị hai phía hay không và, nếu đúng, hãy xuất hai phía của nó.

## Thuật toán

Có một định lý khẳng định đồ thị là hai phía khi và chỉ khi mọi chu trình của nó có độ dài chẵn. Tuy nhiên, trong thực tế, ta thường dùng một cách phát biểu khác thuận tiện hơn: đồ thị là hai phía khi và chỉ khi các đỉnh của nó có thể được tô bằng hai màu sao cho hai đầu của mỗi cạnh có màu khác nhau.

Ta chạy một chuỗi các lần [tìm kiếm theo chiều rộng](breadth-first-search.md), bắt đầu từ mỗi đỉnh chưa được thăm. Trong mỗi lần tìm kiếm, gán đỉnh xuất phát vào phía 1. Khi đi từ một đỉnh thuộc một phía đến một đỉnh kề chưa được thăm, ta gán đỉnh kề vào phía còn lại. Nếu đỉnh kề đã được thăm, ta kiểm tra nó có thuộc phía đối diện hay không; nếu hai đỉnh thuộc cùng một phía, kết luận đồ thị không phải là đồ thị hai phía. Khi đã thăm mọi đỉnh và gán phía thành công, ta biết đồ thị là hai phía và đồng thời đã xây dựng được cách phân hoạch các đỉnh.

## Cài đặt

```cpp
int n;
vector<vector<int>> adj;

vector<int> side(n, -1);
bool is_bipartite = true;
queue<int> q;
for (int st = 0; st < n; ++st) {
    if (side[st] == -1) {
        q.push(st);
        side[st] = 0;
        while (!q.empty()) {
            int v = q.front();
            q.pop();
            for (int u : adj[v]) {
                if (side[u] == -1) {
                    side[u] = side[v] ^ 1;
                    q.push(u);
                } else {
                    is_bipartite &= side[u] != side[v];
                }
            }
        }
    }
}

cout << (is_bipartite ? "YES" : "NO") << endl;
```

### Bài tập luyện tập:

- [SPOJ - BUGLIFE](http://www.spoj.com/problems/BUGLIFE/)
- [Codeforces - Graph Without Long Directed Paths](https://codeforces.com/contest/1144/problem/F)
- [Codeforces - String Coloring (easy version)](https://codeforces.com/contest/1296/problem/E1)
- [CSES : Building Teams](https://cses.fi/problemset/task/1668)
- [Codeforces - Alternating Path](https://codeforces.com/contest/2204/problem/D)
