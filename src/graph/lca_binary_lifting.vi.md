---
tags:
  - Translated
e_maxx_link: lca_simpler
translation:
  source: graph/lca_binary_lifting.md
  source_commit: 139b6a65390ba2efda88c1ae0b3ba007fb827f0e
  status: draft
  last_synced: 2026-08-07
---

# Tổ tiên chung gần nhất - Nhảy nhị phân

Cho $G$ là một cây.
Với mỗi truy vấn dạng `(u, v)`, ta muốn tìm tổ tiên chung gần nhất của hai đỉnh `u` và `v`. Cụ thể, ta cần tìm một đỉnh `w` vừa nằm trên đường đi từ `u` tới đỉnh gốc, vừa nằm trên đường đi từ `v` tới đỉnh gốc; nếu có nhiều đỉnh như vậy, ta chọn đỉnh xa gốc nhất.
Nói cách khác, đỉnh cần tìm `w` là tổ tiên thấp nhất của `u` và `v`.
Đặc biệt, nếu `u` là tổ tiên của `v` thì `u` chính là tổ tiên chung gần nhất của chúng.

Thuật toán trong bài cần $O(N \log N)$ để tiền xử lý cây, sau đó mỗi truy vấn LCA được trả lời trong $O(\log N)$.

## Thuật toán

Với mỗi đỉnh, ta tiền xử lý tổ tiên ngay phía trên nó, tổ tiên cách hai mức, cách bốn mức, v.v.
Ta lưu các tổ tiên này trong mảng `up`, nghĩa là `up[i][j]` là tổ tiên thứ `2^j` phía trên đỉnh `i`, với `i=1...N`, `j=0...ceil(log(N))`.
Thông tin này cho phép ta nhảy từ một đỉnh bất kỳ tới một tổ tiên của nó trong $O(\log N)$.
Ta có thể tính mảng này bằng một lượt [DFS](depth-first-search.md) trên cây.

Với mỗi đỉnh, ta cũng lưu thời điểm đỉnh đó được thăm lần đầu (tức thời điểm DFS phát hiện đỉnh) và thời điểm rời khỏi nó (tức sau khi đã thăm toàn bộ các con và thoát khỏi hàm DFS).
Nhờ thông tin này, ta có thể kiểm tra trong thời gian hằng số xem một đỉnh có phải là tổ tiên của đỉnh khác hay không.

Giả sử ta nhận được truy vấn `(u, v)`.
Ta có thể kiểm tra ngay xem một trong hai đỉnh có phải là tổ tiên của đỉnh còn lại hay không.
Nếu có, đỉnh đó chính là LCA.
Nếu `u` không phải tổ tiên của `v`, đồng thời `v` cũng không phải tổ tiên của `u`, ta đi dần lên các tổ tiên của `u` cho tới khi tìm được đỉnh cao nhất (tức gần gốc nhất) nhưng vẫn không phải tổ tiên của `v` (nghĩa là một đỉnh `x` sao cho `x` không phải tổ tiên của `v`, nhưng `up[x][0]` thì có).
Ta có thể tìm đỉnh `x` này trong $O(\log N)$ bằng mảng `up`.

Ta mô tả quá trình này chi tiết hơn.
Đặt `L = ceil(log(N))`.
Ban đầu giả sử `i = L`.
Nếu `up[u][i]` không phải là tổ tiên của `v`, ta gán `u = up[u][i]` rồi giảm `i` đi một.
Nếu `up[u][i]` là tổ tiên, ta chỉ giảm `i` đi một.
Rõ ràng sau khi xử lý mọi `i` không âm, đỉnh `u` sẽ chính là đỉnh cần tìm: `u` vẫn chưa phải tổ tiên của `v`, nhưng `up[u][0]` thì đã thỏa điều kiện này.

Khi đó, hiển nhiên đáp án LCA là `up[u][0]`, tức đỉnh thấp nhất trong các tổ tiên của đỉnh `u` mà đồng thời cũng là tổ tiên của `v`.

Vì vậy, để trả lời một truy vấn LCA, ta duyệt `i` từ `ceil(log(N))` xuống `0` và ở mỗi bước kiểm tra quan hệ tổ tiên giữa các đỉnh.
Do đó, mỗi truy vấn được trả lời trong $O(\log N)$.

## Cài đặt

```cpp
int n, l;
vector<vector<int>> adj;

int timer;
vector<int> tin, tout;
vector<vector<int>> up;

void dfs(int v, int p)
{
    tin[v] = ++timer;
    up[v][0] = p;
    for (int i = 1; i <= l; ++i)
        up[v][i] = up[up[v][i-1]][i-1];

    for (int u : adj[v]) {
        if (u != p)
            dfs(u, v);
    }

    tout[v] = ++timer;
}

bool is_ancestor(int u, int v)
{
    return tin[u] <= tin[v] && tout[u] >= tout[v];
}

int lca(int u, int v)
{
    if (is_ancestor(u, v))
        return u;
    if (is_ancestor(v, u))
        return v;
    for (int i = l; i >= 0; --i) {
        if (!is_ancestor(up[u][i], v))
            u = up[u][i];
    }
    return up[u][0];
}

void preprocess(int root) {
    tin.resize(n);
    tout.resize(n);
    timer = 0;
    l = ceil(log2(n));
    up.assign(n, vector<int>(l + 1));
    dfs(root, root);
}
```
## Bài tập luyện tập

* [LeetCode -  Kth Ancestor of a Tree Node](https://leetcode.com/problems/kth-ancestor-of-a-tree-node)
* [Codechef - Longest Good Segment](https://www.codechef.com/problems/LGSEG)
* [HackerEarth - Optimal Connectivity](https://www.hackerearth.com/practice/algorithms/graphs/graph-representation/practice-problems/algorithm/optimal-connectivity-c6ae79ca/)