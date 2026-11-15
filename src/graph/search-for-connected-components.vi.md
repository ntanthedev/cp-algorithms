---
tags:
  - Translated
e_maxx_link: connected_components
translation:
  source: graph/search-for-connected-components.md
  source_commit: d50c88e054475c92ee9ab58d16425d2d32c56d39
  status: draft
  last_synced: 2026-09-30
---

# Tìm các thành phần liên thông trong đồ thị

Cho một đồ thị vô hướng $G$ có $n$ đỉnh và $m$ cạnh. Ta cần tìm tất cả các thành phần liên thông của nó, tức là các nhóm đỉnh sao cho trong mỗi nhóm, từ một đỉnh bất kỳ đều có thể đi tới mọi đỉnh khác, và không tồn tại đường đi giữa hai nhóm khác nhau.

## Thuật toán giải bài toán

* Để giải bài toán, ta có thể dùng tìm kiếm theo chiều sâu (Depth First Search) hoặc tìm kiếm theo chiều rộng (Breadth First Search).

* Cụ thể, ta sẽ thực hiện nhiều lượt DFS: lượt đầu tiên bắt đầu từ đỉnh thứ nhất và duyệt (tìm) tất cả các đỉnh thuộc thành phần liên thông đầu tiên. Sau đó, ta tìm đỉnh chưa được thăm đầu tiên trong số các đỉnh còn lại và chạy tìm kiếm theo chiều sâu từ đỉnh đó, qua đó tìm được thành phần liên thông thứ hai. Tiếp tục như vậy cho đến khi mọi đỉnh đều đã được thăm.

* Tổng thời gian chạy tiệm cận của thuật toán là $O(n + m)$: thuật toán không xử lý cùng một đỉnh hai lần, vì vậy mỗi cạnh sẽ được xét đúng hai lần (một lần ở mỗi đầu mút).

## Cài đặt

``` cpp
int n;
vector<vector<int>> adj;
vector<bool> used;
vector<int> comp;

void dfs(int v) {
    used[v] = true;
    comp.push_back(v);
    for (int u : adj[v]) {
        if (!used[u])
            dfs(u);
    }
}

void find_comps() {
    used.assign(n, false);
    for (int v = 0; v < n; ++v) {
        if (!used[v]) {
            comp.clear();
            dfs(v);
            cout << "Component:" ;
            for (int u : comp)
                cout << ' ' << u;
            cout << endl ;
        }
    }
}
```

* Hàm quan trọng nhất được sử dụng là `find_comps()`, có nhiệm vụ tìm và hiển thị các thành phần liên thông của đồ thị.

* Đồ thị được lưu dưới dạng danh sách kề, tức là `adj[v]` chứa danh sách các đỉnh có cạnh nối với đỉnh `v`.

* Vector `comp` chứa danh sách các đỉnh thuộc thành phần liên thông hiện tại.

## Cài đặt dạng lặp

Các hàm đệ quy quá sâu nhìn chung không tốt.
Mỗi lời gọi đệ quy đều cần một lượng nhỏ bộ nhớ trên ngăn xếp, trong khi mặc định chương trình chỉ có dung lượng ngăn xếp hữu hạn.
Vì vậy, nếu chạy DFS đệ quy trên một đồ thị liên thông có hàng triệu đỉnh, ta có thể gặp lỗi tràn ngăn xếp.

Ta luôn có thể chuyển một chương trình đệ quy thành chương trình dạng lặp bằng cách tự duy trì một cấu trúc dữ liệu ngăn xếp.
Vì cấu trúc dữ liệu này được cấp phát trên heap nên sẽ không xảy ra tràn ngăn xếp.

```cpp
int n;
vector<vector<int>> adj;
vector<bool> used;
vector<int> comp;

void dfs(int v) {
    stack<int> st;
    st.push(v);
    
    while (!st.empty()) {
        int curr = st.top();
        st.pop();
        if (!used[curr]) {
            used[curr] = true;
            comp.push_back(curr);
            for (int i = adj[curr].size() - 1; i >= 0; i--) {
                st.push(adj[curr][i]);
            }
        }
    }
}

void find_comps() {
    used.assign(n, false);
    for (int v = 0; v < n ; ++v) {
        if (!used[v]) {
            comp.clear();
            dfs(v);
            cout << "Component:" ;
            for (int u : comp)
                cout << ' ' << u;
            cout << endl ;
        }
    }
}
```

## Bài tập luyện tập
 - [SPOJ: CT23E](http://www.spoj.com/problems/CT23E/)
 - [CODECHEF: GERALD07](https://www.codechef.com/MARCH14/problems/GERALD07)
 - [CSES : Building Roads](https://cses.fi/problemset/task/1666)
