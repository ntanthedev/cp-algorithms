---
title: Finding articulation points in a graph in O(N+M)
tags:
  - Translated
e_maxx_link: cutpoints
translation:
  source: graph/cutpoints.md
  source_commit: 46f7676b7be8ba8bb558c535eed2459371fb106d
  status: draft
  last_synced: 2026-08-07
---
# Tìm đỉnh khớp trong đồ thị trong $O(N+M)$

Cho một đồ thị vô hướng. **Đỉnh khớp** (articulation point, còn gọi là cut vertex) là một đỉnh mà khi xóa đỉnh đó cùng các cạnh kề với nó sẽ làm đồ thị mất liên thông (chính xác hơn là làm tăng số thành phần liên thông của đồ thị). Bài toán yêu cầu tìm tất cả các đỉnh khớp trong đồ thị đã cho.

Thuật toán được trình bày ở đây dựa trên [tìm kiếm theo chiều sâu](depth-first-search.md) và có độ phức tạp $O(N+M)$, trong đó $N$ là số đỉnh và $M$ là số cạnh của đồ thị.

## Thuật toán

Chọn một đỉnh bất kỳ $root$ của đồ thị và chạy [tìm kiếm theo chiều sâu](depth-first-search.md) từ đó. Ta có nhận xét sau (khá dễ chứng minh):

- Giả sử trong DFS ta đang xét các cạnh đi ra từ đỉnh $v\ne root$.
Nếu cạnh hiện tại $(v, to)$ có tính chất rằng không có đỉnh nào trong số $to$ hoặc các hậu duệ của nó trên cây duyệt DFS có cạnh ngược tới một tổ tiên của $v$, thì $v$ là một đỉnh khớp. Nếu không, $v$ không phải là đỉnh khớp.

- Xét trường hợp còn lại $v=root$.
Đỉnh này là đỉnh khớp khi và chỉ khi nó có nhiều hơn một đỉnh con trong cây DFS.

Bây giờ ta cần kiểm tra nhận xét này một cách hiệu quả với từng đỉnh. Ta sẽ sử dụng "thời điểm vào đỉnh" được tính trong quá trình tìm kiếm theo chiều sâu.

Gọi $tin[v]$ là thời điểm vào đỉnh $v$. Ta xây dựng mảng $low[v]$ để kiểm tra nhận xét trên cho từng đỉnh $v$. $low[v]$ là giá trị nhỏ nhất trong $tin[v]$, các thời điểm vào $tin[p]$ với mỗi đỉnh $p$ được nối với $v$ bởi một cạnh ngược $(v, p)$, và các giá trị $low[to]$ với mỗi đỉnh $to$ là hậu duệ trực tiếp của $v$ trong cây DFS:

$$low[v] = \min \begin{cases} tin[v] \\ tin[p] &\text{ for all }p\text{ for which }(v, p)\text{ is a back edge} \\ low[to]& \text{ for all }to\text{ for which }(v, to)\text{ is a tree edge} \end{cases}$$

Khi đó, tồn tại một cạnh ngược từ đỉnh $v$ hoặc một hậu duệ của nó tới một tổ tiên của $v$ khi và chỉ khi $v$ có một đỉnh con $to$ sao cho $low[to] < tin[v]$. Nếu $low[to] = tin[v]$ thì cạnh ngược đi thẳng về $v$; nếu không, cạnh ngược đi tới một tổ tiên của $v$.

Do đó, đỉnh $v$ trong cây DFS là một đỉnh khớp khi và chỉ khi $low[to] \geq tin[v]$.

## Cài đặt

Cài đặt cần phân biệt ba trường hợp: khi ta đi xuống theo một cạnh của cây DFS, khi gặp một cạnh ngược tới tổ tiên của đỉnh hiện tại, và khi quay về đỉnh cha. Ba trường hợp là:

- $visited[to] = false$ - cạnh thuộc cây DFS;
- $visited[to] = true$ && $to \neq parent$ - cạnh là cạnh ngược tới một tổ tiên;
- $to = parent$ - cạnh dẫn ngược về đỉnh cha trên cây DFS.

Để cài đặt, ta cần một hàm tìm kiếm theo chiều sâu nhận thêm đỉnh cha của đỉnh hiện tại.

```cpp
int n; // number of nodes
vector<vector<int>> adj; // adjacency list of graph

vector<bool> visited;
vector<int> tin, low;
int timer;
 
void dfs(int v, int p = -1) {
    visited[v] = true;
    tin[v] = low[v] = timer++;
    int children=0;
    for (int to : adj[v]) {
        if (to == p) continue;
        if (visited[to]) {
            low[v] = min(low[v], tin[to]);
        } else {
            dfs(to, v);
            low[v] = min(low[v], low[to]);
            if (low[to] >= tin[v] && p!=-1)
                IS_CUTPOINT(v);
            ++children;
        }
    }
    if(p == -1 && children > 1)
        IS_CUTPOINT(v);
}
 
void find_cutpoints() {
    timer = 0;
    visited.assign(n, false);
    tin.assign(n, -1);
    low.assign(n, -1);
    for (int i = 0; i < n; ++i) {
        if (!visited[i])
            dfs (i);
    }
}
```

Hàm chính là `find_cutpoints`; hàm này thực hiện các bước khởi tạo cần thiết rồi bắt đầu tìm kiếm theo chiều sâu trong từng thành phần liên thông của đồ thị.

Hàm `IS_CUTPOINT(a)` là một hàm dùng để xử lý việc đỉnh $a$ là một đỉnh khớp, chẳng hạn như in đỉnh đó ra (lưu ý hàm này có thể được gọi nhiều lần với cùng một đỉnh).

## Bài tập luyện tập

- [UVA #10199 "Tourist Guide"](http://uva.onlinejudge.org/index.php?option=com_onlinejudge&Itemid=8&category=13&page=show_problem&problem=1140) [difficulty: low]
- [UVA #315 "Network"](http://uva.onlinejudge.org/index.php?option=com_onlinejudge&Itemid=8&category=5&page=show_problem&problem=251) [difficulty: low]
- [SPOJ - Submerging Islands](http://www.spoj.com/problems/SUBMERGE/)
- [Codeforces - Cutting Figure](https://codeforces.com/problemset/problem/193/A)