---
tags:
  - Translated
e_maxx_link: lca_linear_offline
translation:
  source: graph/lca_tarjan.md
  source_commit: 3706dee30c6320f478215cf20f59e5f55caeb48f
  status: draft
  last_synced: 2026-11-15
---

# Tổ tiên chung thấp nhất – thuật toán offline của Tarjan

Cho cây $G$ có $n$ đỉnh và $m$ truy vấn dạng $(u, v)$.
Với mỗi truy vấn $(u, v)$, ta muốn tìm tổ tiên chung thấp nhất của hai đỉnh $u$ và $v$: đỉnh là tổ tiên của cả $u$ và $v$ và có độ sâu lớn nhất trong cây.
Đỉnh $v$ cũng là tổ tiên của $v$, nên LCA có thể là một trong hai đỉnh.

Bài này giải bài toán offline: giả sử biết trước tất cả truy vấn, do đó ta có thể trả lời chúng theo thứ tự tùy ý.
Thuật toán sau cho phép trả lời cả $m$ truy vấn trong tổng thời gian $O(n + m)$, tức là khi $m$ đủ lớn thì mất $O(1)$ cho mỗi truy vấn.

## Thuật toán

Thuật toán mang tên Robert Tarjan, người phát hiện ra nó năm 1979 và cũng có nhiều đóng góp khác cho cấu trúc dữ liệu [Disjoint Set Union](../data_structures/disjoint_set_union.md), được sử dụng nhiều trong thuật toán này.

Thuật toán trả lời mọi truy vấn bằng một lần duyệt [DFS](depth-first-search.md) trên cây.
Cụ thể, truy vấn $(u, v)$ được trả lời tại đỉnh $u$ nếu đỉnh $v$ đã được thăm trước đó, hoặc ngược lại.

Giả sử hiện ta ở đỉnh $v$, đã thực hiện các lời gọi DFS đệ quy và cũng đã thăm đỉnh còn lại $u$ trong truy vấn $(u, v)$.
Hãy xét cách tìm LCA của hai đỉnh này.

Lưu ý rằng $\text{LCA}(u, v)$ là đỉnh $v$ hoặc một tổ tiên của nó.
Vì vậy cần tìm đỉnh thấp nhất trong các tổ tiên của $v$ (kể cả $v$) mà $u$ là hậu duệ của đỉnh đó. 
Với $v$ cố định, các đỉnh đã thăm của cây được chia thành các tập rời nhau. 
Mỗi tổ tiên $p$ của $v$ có một tập riêng chứa chính nó và mọi cây con gốc tại những con của nó không nằm trên đường từ $v$ đến gốc cây.
Tập chứa đỉnh $u$ xác định $\text{LCA}(u, v)$:
LCA là đại diện của tập, cụ thể là đỉnh nằm trên đường từ $v$ đến gốc cây.

Ta chỉ cần tìm cách duy trì hiệu quả các tập này.
Để làm vậy, ta dùng cấu trúc dữ liệu DSU.
Để có thể hợp nhất theo hạng (union by rank), ta lưu đại diện thực sự của mỗi tập (đỉnh trên đường từ $v$ đến gốc cây) trong mảng `ancestor`.

Hãy xét cách cài đặt DFS.
Giả sử hiện ta đang thăm đỉnh $v$.
Ta đặt đỉnh này vào một tập mới trong DSU, `ancestor[v] = v`.
Như thường lệ, ta xử lý mọi đỉnh con của $v$.
Trước tiên gọi DFS đệ quy từ đỉnh con, rồi thêm đỉnh đó cùng toàn bộ cây con của nó vào tập của $v$.
Có thể thực hiện bằng hàm `union_sets` và phép gán `ancestor[find_set(v)] = v` sau đó (cần thiết vì `union_sets` có thể đổi đại diện của tập).

Cuối cùng, sau khi xử lý mọi đỉnh con, ta có thể trả lời mọi truy vấn dạng $(u, v)$ mà $u$ đã được thăm.
Đáp án, tức LCA của $u$ và $v$, là đỉnh `ancestor[find_set(u)]`.
Dễ thấy một truy vấn chỉ được trả lời một lần.

Hãy xác định độ phức tạp thời gian của thuật toán. 
Trước hết, DFS tốn $O(n)$.
Tiếp theo, `union_sets` được gọi $n$ lần, cũng mất $O(n)$.
Cuối cùng, các lời gọi `find_set` cho mỗi truy vấn mất $O(m)$.
Vậy tổng độ phức tạp là $O(n + m)$, nghĩa là khi $m$ đủ lớn, chi phí tương ứng là $O(1)$ để trả lời một truy vấn.

**Ghi chú bản dịch:** Với DSU thông thường dùng hợp nhất theo hạng và nén đường đi, cận tổng quát là $O((n+m)\alpha(n))$ khấu hao, thay vì coi mỗi thao tác DSU là $O(1)$ như lập luận trên. Trong mã dưới đây, truy vấn có hai đầu mút trùng nhau được thêm hai lần vào cùng danh sách và sẽ được in hai lần. Truy vấn giữa một đỉnh và tổ tiên thực sự của nó cũng bị in hai lần vì tổ tiên đã được đánh dấu thăm khi đi vào DFS; ví dụ cây có cạnh 0–1 và truy vấn (0, 1).

## Cài đặt

Dưới đây là một cách cài đặt thuật toán.
Phần cài đặt DSU không được đưa vào vì có thể sử dụng mà không cần sửa đổi.

```cpp
vector<vector<int>> adj;
vector<vector<int>> queries;
vector<int> ancestor;
vector<bool> visited;

void dfs(int v)
{
    visited[v] = true;
    ancestor[v] = v;
    for (int u : adj[v]) {
        if (!visited[u]) {
            dfs(u);
            union_sets(v, u);
            ancestor[find_set(v)] = v;
        }
    }
    for (int other_node : queries[v]) {
        if (visited[other_node])
            cout << "LCA of " << v << " and " << other_node
                 << " is " << ancestor[find_set(other_node)] << ".\n";
    }
}

void compute_LCAs() {
    // initialize n, adj and DSU
    // for (each query (u, v)) {
    //    queries[u].push_back(v);
    //    queries[v].push_back(u);
    // }

    ancestor.resize(n);
    visited.assign(n, false);
    dfs(0);
}
```
