---
tags:
  - Original
translation:
  source: graph/second_best_mst.md
  source_commit: 3a68ee34ad3ac16b28bca29fe678d005902fa848
  status: draft
  last_synced: 2026-09-30
---

# Cây khung nhỏ nhất thứ hai

Cây khung nhỏ nhất $T$ là một cây của đồ thị đã cho $G$, phủ tất cả các đỉnh của đồ thị và có tổng trọng số các cạnh nhỏ nhất trong số mọi cây khung có thể có.
Cây khung nhỏ nhất thứ hai $T'$ là một cây khung có tổng trọng số các cạnh nhỏ thứ hai trong số mọi cây khung của đồ thị $G$.

## Nhận xét

Gọi $T$ là cây khung nhỏ nhất của đồ thị $G$.
Ta có thể nhận thấy rằng cây khung nhỏ nhất thứ hai chỉ khác $T$ bởi đúng một phép thay thế cạnh. (Để xem chứng minh của mệnh đề này, tham khảo bài 23-1 [tại đây](http://www-bcf.usc.edu/~shanghua/teaching/Spring2010/public_html/files/HW2_Solutions_A.pdf)).

Vì vậy, ta cần tìm một cạnh $e_{new}$ không nằm trong $T$, rồi thay nó cho một cạnh trong $T$ (gọi cạnh đó là $e_{old}$) sao cho đồ thị mới $T' = (T \cup \{e_{new}\}) \setminus \{e_{old}\}$ là một cây khung và độ chênh lệch trọng số ($e_{new} - e_{old}$) là nhỏ nhất.


## Sử dụng thuật toán Kruskal

Ta có thể dùng thuật toán Kruskal để tìm MST trước, rồi lần lượt thử loại một cạnh khỏi MST và thay bằng một cạnh khác.

1. Sắp xếp các cạnh trong $O(E \log E)$, sau đó tìm một MST bằng Kruskal trong $O(E)$.
2. Với mỗi cạnh thuộc MST (MST có $V-1$ cạnh), tạm thời loại cạnh đó khỏi danh sách cạnh để nó không thể được chọn.
3. Sau đó, tiếp tục thử tìm một MST trong $O(E)$ bằng các cạnh còn lại.
4. Thực hiện như vậy với mọi cạnh trong MST và lấy kết quả tốt nhất.

Lưu ý: ở Bước 3, ta không cần sắp xếp lại các cạnh.

Vì vậy, độ phức tạp thời gian tổng thể là $O(E \log V + E + V E)$ = $O(V E)$.


## Mô hình hóa thành bài toán tổ tiên chung gần nhất (LCA)

Trong cách tiếp cận trước, ta thử mọi khả năng loại một cạnh khỏi MST.
Ở đây, ta sẽ làm điều hoàn toàn ngược lại.
Ta thử thêm từng cạnh chưa nằm trong MST.

1. Sắp xếp các cạnh trong $O(E \log E)$, sau đó tìm một MST bằng Kruskal trong $O(E)$.
2. Với mỗi cạnh $e$ chưa nằm trong MST, tạm thời thêm nó vào MST, từ đó tạo ra một chu trình. Chu trình này sẽ đi qua LCA.
3. Tìm cạnh $k$ có trọng số lớn nhất trong chu trình và khác $e$, bằng cách đi theo các đỉnh cha của hai đầu mút của cạnh $e$ cho tới LCA.
4. Tạm thời loại $k$, tạo thành một cây khung mới.
5. Tính độ chênh lệch trọng số $\delta = weight(e) - weight(k)$ và ghi nhớ nó cùng với cạnh đã thay đổi.
6. Lặp lại bước 2 với mọi cạnh còn lại và trả về cây khung có độ chênh lệch trọng số so với MST là nhỏ nhất.

Độ phức tạp thời gian của thuật toán phụ thuộc vào cách ta tính các cạnh $k$, tức các cạnh có trọng số lớn nhất ở bước 2 của thuật toán này.
Một cách tính chúng hiệu quả trong $O(E \log V)$ là chuyển bài toán thành bài toán tổ tiên chung gần nhất (LCA).

Ta sẽ tiền xử lý LCA bằng cách chọn một gốc cho MST, đồng thời tính trọng số cạnh lớn nhất trên đường đi từ mỗi đỉnh tới các tổ tiên của nó.
Việc này có thể thực hiện bằng [nhảy nhị phân (Binary Lifting)](lca_binary_lifting.md) cho LCA.

Độ phức tạp thời gian cuối cùng của cách tiếp cận này là $O(E \log V)$.

Ví dụ:

<div style="text-align: center;">
  <img src="second_best_mst_1.png" alt="MST">
  <img src="second_best_mst_2.png" alt="Second best MST">
  <br />

*Trong hình, bên trái là MST và bên phải là cây khung nhỏ nhất thứ hai.*
</div>


Trong đồ thị đã cho, giả sử ta chọn đỉnh màu xanh ở phía trên làm gốc của MST, rồi chạy thuật toán bằng cách bắt đầu chọn các cạnh không nằm trong MST.
Giả sử cạnh được chọn đầu tiên là cạnh $(u, v)$ có trọng số 36.
Thêm cạnh này vào cây tạo thành chu trình 36 - 7 - 2 - 34.

Bây giờ ta tìm cạnh có trọng số lớn nhất trong chu trình bằng cách tìm $\text{LCA}(u, v) = p$.
Ta tính cạnh có trọng số lớn nhất trên các đường đi từ $u$ tới $p$ và từ $v$ tới $p$.
Lưu ý: trong một số trường hợp, $\text{LCA}(u, v)$ cũng có thể bằng $u$ hoặc $v$.
Trong ví dụ này, ta thu được cạnh có trọng số 34 là cạnh có trọng số lớn nhất trong chu trình.
Bằng cách loại cạnh này, ta thu được một cây khung mới có độ chênh lệch trọng số chỉ là 2.

Sau khi làm tương tự với tất cả các cạnh khác không thuộc MST ban đầu, ta thấy cây khung này cũng chính là cây khung nhỏ nhất thứ hai của toàn bộ đồ thị.
Chọn cạnh có trọng số 14 sẽ làm trọng số của cây tăng 7, chọn cạnh có trọng số 27 làm tăng 14, chọn cạnh có trọng số 28 làm tăng 21, còn chọn cạnh có trọng số 39 sẽ làm cây tăng 5.

## Cài đặt
```cpp
struct edge {
    int s, e, w, id;
    bool operator<(const struct edge& other) { return w < other.w; }
};
typedef struct edge Edge;

const int N = 2e5 + 5;
long long res = 0, ans = 1e18;
int n, m, a, b, w, id, l = 21;
vector<Edge> edges;
vector<int> h(N, 0), parent(N, -1), size(N, 0), present(N, 0);
vector<vector<pair<int, int>>> adj(N), dp(N, vector<pair<int, int>>(l));
vector<vector<int>> up(N, vector<int>(l, -1));

pair<int, int> combine(pair<int, int> a, pair<int, int> b) {
    vector<int> v = {a.first, a.second, b.first, b.second};
    int topTwo = -3, topOne = -2;
    for (int c : v) {
        if (c > topOne) {
            topTwo = topOne;
            topOne = c;
        } else if (c > topTwo && c < topOne) {
            topTwo = c;
        }
    }
    return {topOne, topTwo};
}

void dfs(int u, int par, int d) {
    h[u] = 1 + h[par];
    up[u][0] = par;
    dp[u][0] = {d, -1};
    for (auto v : adj[u]) {
        if (v.first != par) {
            dfs(v.first, u, v.second);
        }
    }
}

pair<int, int> lca(int u, int v) {
    pair<int, int> ans = {-2, -3};
    if (h[u] < h[v]) {
        swap(u, v);
    }
    for (int i = l - 1; i >= 0; i--) {
        if (h[u] - h[v] >= (1 << i)) {
            ans = combine(ans, dp[u][i]);
            u = up[u][i];
        }
    }
    if (u == v) {
        return ans;
    }
    for (int i = l - 1; i >= 0; i--) {
        if (up[u][i] != -1 && up[v][i] != -1 && up[u][i] != up[v][i]) {
            ans = combine(ans, combine(dp[u][i], dp[v][i]));
            u = up[u][i];
            v = up[v][i];
        }
    }
    ans = combine(ans, combine(dp[u][0], dp[v][0]));
    return ans;
}

int main(void) {
    cin >> n >> m;
    for (int i = 1; i <= n; i++) {
        parent[i] = i;
        size[i] = 1;
    }
    for (int i = 1; i <= m; i++) {
        cin >> a >> b >> w; // 1-indexed
        edges.push_back({a, b, w, i - 1});
    }
    sort(edges.begin(), edges.end());
    for (int i = 0; i <= m - 1; i++) {
        a = edges[i].s;
        b = edges[i].e;
        w = edges[i].w;
        id = edges[i].id;
        if (unite_set(a, b)) { 
            adj[a].emplace_back(b, w);
            adj[b].emplace_back(a, w);
            present[id] = 1;
            res += w;
        }
    }
    dfs(1, 0, 0);
    for (int i = 1; i <= l - 1; i++) {
        for (int j = 1; j <= n; ++j) {
            if (up[j][i - 1] != -1) {
                int v = up[j][i - 1];
                up[j][i] = up[v][i - 1];
                dp[j][i] = combine(dp[j][i - 1], dp[v][i - 1]);
            }
        }
    }
    for (int i = 0; i <= m - 1; i++) {
        id = edges[i].id;
        w = edges[i].w;
        if (!present[id]) {
            auto rem = lca(edges[i].s, edges[i].e);
            if (rem.first != w) {
                if (ans > res + w - rem.first) {
                    ans = res + w - rem.first;
                }
            } else if (rem.second != -1) {
                if (ans > res + w - rem.second) {
                    ans = res + w - rem.second;
                }
            }
        }
    }
    cout << ans << "\n";
    return 0;
}
```

## Tài liệu tham khảo

1. Competitive Programming-3, của Steven Halim
2. [web.mit.edu](http://web.mit.edu/6.263/www/quiz1-f05-sol.pdf)

## Bài tập
* [Codeforces - Minimum spanning tree for each edge](https://codeforces.com/problemset/problem/609/E)
