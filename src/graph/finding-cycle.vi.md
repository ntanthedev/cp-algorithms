---
title: Checking a graph for acyclicity and finding a cycle in O(M)
tags:
  - Translated
e_maxx_link: finding_cycle
translation:
  source: graph/finding-cycle.md
  source_commit: af0ebda9f978bfefd545f19e7b14e7f3e1bc4571
  status: draft
  last_synced: 2026-08-08
---
# Kiểm tra đồ thị không có chu trình và tìm một chu trình trong $O(M)$

Xét một đồ thị có hướng hoặc vô hướng không có cạnh khuyên và cạnh song song. Ta cần kiểm tra đồ thị có không chứa chu trình hay không; nếu có chu trình, hãy tìm một chu trình bất kỳ.

Ta có thể giải bài toán bằng [duyệt theo chiều sâu](depth-first-search.md) trong $O(M)$, với $M$ là số cạnh.

**Ghi chú bản dịch:** Nguồn tiếng Anh ghi độ phức tạp là $O(M)$. Nếu tính cả bước duyệt qua các đỉnh để khởi động DFS cho từng thành phần, với $N$ là số đỉnh, cách viết tổng quát chặt hơn là $O(N+M)$. Bản dịch giữ ký hiệu của nguồn và tách correction này để đề xuất sửa upstream.

## Thuật toán

Ta thực hiện một chuỗi các lượt DFS trên đồ thị. Ban đầu, mọi đỉnh được tô trắng (0). Với mỗi đỉnh chưa thăm (màu trắng), bắt đầu DFS từ đỉnh đó; khi đi vào một đỉnh thì tô nó màu xám (1), và khi rời khỏi đỉnh thì tô màu đen (2). Nếu DFS đi tới một đỉnh màu xám, ta đã tìm thấy một chu trình (với đồ thị vô hướng, không xét cạnh nối về đỉnh cha).
Có thể truy vết chính chu trình đó bằng mảng cha.

## Cài đặt

Dưới đây là cài đặt cho đồ thị có hướng.

```cpp
int n;
vector<vector<int>> adj;
vector<char> color;
vector<int> parent;
int cycle_start, cycle_end;

bool dfs(int v) {
    color[v] = 1;
    for (int u : adj[v]) {
        if (color[u] == 0) {
            parent[u] = v;
            if (dfs(u))
                return true;
        } else if (color[u] == 1) {
            cycle_end = v;
            cycle_start = u;
            return true;
        }
    }
    color[v] = 2;
    return false;
}

void find_cycle() {
    color.assign(n, 0);
    parent.assign(n, -1);
    cycle_start = -1;

    for (int v = 0; v < n; v++) {
        if (color[v] == 0 && dfs(v))
            break;
    }

    if (cycle_start == -1) {
        cout << "Acyclic" << endl;
    } else {
        vector<int> cycle;
        cycle.push_back(cycle_start);
        for (int v = cycle_end; v != cycle_start; v = parent[v])
            cycle.push_back(v);
        cycle.push_back(cycle_start);
        reverse(cycle.begin(), cycle.end());

        cout << "Cycle found: ";
        for (int v : cycle)
            cout << v << " ";
        cout << endl;
    }
}
```

Dưới đây là cài đặt cho đồ thị vô hướng.
Lưu ý rằng trong phiên bản vô hướng, nếu một đỉnh `v` đã được tô đen thì DFS sẽ không bao giờ thăm lại đỉnh đó.
Lý do là ngay ở lần thăm đầu tiên, ta đã duyệt toàn bộ các cạnh kề với `v`.
Nếu DFS đã xử lý xong `v` mà không tìm thấy chu trình, thành phần liên thông chứa `v` (sau khi bỏ cạnh giữa `v` và đỉnh cha của nó) phải là một cây.
Vì vậy, ta thậm chí không cần phân biệt trạng thái xám và đen.
Do đó có thể thay vector ký tự `color` bằng vector boolean `visited`.

```cpp
int n;
vector<vector<int>> adj;
vector<bool> visited;
vector<int> parent;
int cycle_start, cycle_end;

bool dfs(int v, int par) { // passing vertex and its parent vertex
    visited[v] = true;
    for (int u : adj[v]) {
        if(u == par) continue; // skipping edge to parent vertex
        if (visited[u]) {
            cycle_end = v;
            cycle_start = u;
            return true;
        }
        parent[u] = v;
        if (dfs(u, parent[u]))
            return true;
    }
    return false;
}

void find_cycle() {
    visited.assign(n, false);
    parent.assign(n, -1);
    cycle_start = -1;

    for (int v = 0; v < n; v++) {
        if (!visited[v] && dfs(v, parent[v]))
            break;
    }

    if (cycle_start == -1) {
        cout << "Acyclic" << endl;
    } else {
        vector<int> cycle;
        cycle.push_back(cycle_start);
        for (int v = cycle_end; v != cycle_start; v = parent[v])
            cycle.push_back(v);
        cycle.push_back(cycle_start);

        cout << "Cycle found: ";
        for (int v : cycle)
            cout << v << " ";
        cout << endl;
    }
}
```
### Bài tập luyện tập:

- [AtCoder : Reachability in Functional Graph](https://atcoder.jp/contests/abc357/tasks/abc357_e)
- [CSES : Round Trip](https://cses.fi/problemset/task/1669)
- [CSES : Round Trip II](https://cses.fi/problemset/task/1678/)
