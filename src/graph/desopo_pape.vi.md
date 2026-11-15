---
tags:
  - Translated
e_maxx_link: levit_algorithm
translation:
  source: graph/desopo_pape.md
  source_commit: 1635999b5141c1b6b57f352867bdf0b5ce22ca4c
  status: draft
  last_synced: 2026-11-15
---

# Thuật toán D´Esopo-Pape

Cho đồ thị có $n$ đỉnh và $m$ cạnh, trong đó cạnh thứ i có trọng số $w_i$, cùng với đỉnh xuất phát $v_0$.
Bài toán yêu cầu tìm đường đi ngắn nhất từ đỉnh $v_0$ đến mọi đỉnh còn lại.

Trong hầu hết trường hợp, thuật toán D´Esopo-Pape chạy nhanh hơn [thuật toán Dijkstra](dijkstra.md) và [thuật toán Bellman-Ford](bellman_ford.md); thuật toán cũng xử lý được các cạnh có trọng số âm.
Tuy nhiên, thuật toán không xử lý được chu trình âm.

## Mô tả

Mảng $d$ lưu độ dài đường đi ngắn nhất hiện tại, tức $d_i$ là độ dài đường đi ngắn nhất hiện biết từ đỉnh $v_0$ đến đỉnh $i$.
Ban đầu, mọi phần tử của mảng đều bằng vô cực, ngoại trừ $d_{v_0} = 0$.
Sau khi thuật toán kết thúc, mảng này lưu các khoảng cách ngắn nhất.

Mảng $p$ lưu các đỉnh tiền nhiệm hiện tại, tức $p_i$ là đỉnh ngay trước $i$ trên đường đi ngắn nhất hiện tại từ $v_0$ đến $i$.
Giống như mảng $d$, mảng $p$ thay đổi trong quá trình thuật toán chạy và nhận giá trị cuối cùng khi thuật toán kết thúc.

Ở mỗi bước, thuật toán duy trì ba tập đỉnh:

- $M_0$ — các đỉnh đã được xử lý (dù khoảng cách của chúng có thể chưa phải kết quả cuối cùng).
- $M_1$ — các đỉnh đang được xử lý.
- $M_2$ — các đỉnh chưa được xử lý.

Các đỉnh trong tập $M_1$ được lưu trong một hàng đợi hai đầu (deque).

Mỗi bước, ta lấy một đỉnh ở đầu hàng đợi, thuộc tập $M_1$.
Gọi đỉnh đó là $u$.
Ta chuyển $u$ vào tập $M_0$.
Sau đó, ta duyệt mọi cạnh đi ra từ u.
Gọi $v$ là đầu mút còn lại của cạnh đang xét và $w$ là trọng số của cạnh đó.

- Nếu $v$ thuộc $M_2$, ta thêm $v$ vào cuối hàng đợi và chuyển nó vào $M_1$.
$d_v$ được đặt bằng $d_u + w$.
- Nếu $v$ thuộc $M_1$, ta thử cải thiện $d_v$: $d_v = \min(d_v, d_u + w)$.
Vì $v$ đã thuộc $M_1$, ta không cần thêm lại nó vào $M_1$ hay hàng đợi.
- Nếu $v$ thuộc $M_0$ và có thể cải thiện $d_v$ (tức $d_v > d_u + w$), ta cập nhật $d_v$ rồi đưa $v$ trở lại tập $M_1$, đồng thời thêm nó vào đầu hàng đợi.

Mỗi khi cập nhật một phần tử trong mảng $d$, ta cũng phải cập nhật phần tử tương ứng trong mảng $p$.

## Cài đặt

Ta dùng mảng $m$ để lưu mỗi đỉnh hiện thuộc tập nào.

```{.cpp file=desopo_pape}
struct Edge {
    int to, w;
};

int n;
vector<vector<Edge>> adj;

const int INF = 1e9;

void shortest_paths(int v0, vector<int>& d, vector<int>& p) {
    d.assign(n, INF);
    d[v0] = 0;
    vector<int> m(n, 2);
    deque<int> q;
    q.push_back(v0);
    p.assign(n, -1);

    while (!q.empty()) {
        int u = q.front();
        q.pop_front();
        m[u] = 0;
        for (Edge e : adj[u]) {
            if (d[e.to] > d[u] + e.w) {
                d[e.to] = d[u] + e.w;
                p[e.to] = u;
                if (m[e.to] == 2) {
                    m[e.to] = 1;
                    q.push_back(e.to);
                } else if (m[e.to] == 0) {
                    m[e.to] = 1;
                    q.push_front(e.to);
                }
            }
        }
    }
}

```

## Độ phức tạp

Thuật toán thường chạy khá nhanh — trong hầu hết trường hợp, nó còn nhanh hơn Dijkstra.
Tuy nhiên, có những trường hợp thuật toán cần thời gian theo hàm mũ, nên không phù hợp khi cần bảo đảm thời gian chạy trong trường hợp xấu nhất.
Xem thêm các thảo luận trên [Stack Overflow](https://stackoverflow.com/a/67642821) và [Codeforces](https://codeforces.com/blog/entry/3793).
