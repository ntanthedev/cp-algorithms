---
tags:
  - Translated
e_maxx_link: negative_cycle
translation:
  source: graph/finding-negative-cycle-in-graph.md
  source_commit: e29927fcc2fb7f6a44ff1f8894ede9d6fd293e1c
  status: draft
  last_synced: 2026-08-07
---

# Tìm chu trình âm trong đồ thị

Cho một đồ thị có hướng, có trọng số $G$ gồm $N$ đỉnh và $M$ cạnh. Hãy tìm một chu trình có tổng trọng số âm nếu chu trình như vậy tồn tại.

Ở một cách phát biểu khác, bài toán yêu cầu tìm mọi cặp đỉnh mà giữa chúng có thể tạo các đường đi với trọng số nhỏ tùy ý.

Hai biến thể này thuận tiện hơn khi giải bằng những thuật toán khác nhau, vì vậy bài viết sẽ trình bày cả hai.

## Sử dụng thuật toán Bellman-Ford

Bellman-Ford cho phép kiểm tra đồ thị có tồn tại chu trình âm hay không và, nếu có, tìm một chu trình như vậy.

Chi tiết thuật toán được trình bày trong bài [Bellman-Ford](bellman_ford.md).
Ở đây ta chỉ xét cách áp dụng nó cho bài toán này.

Cài đặt Bellman-Ford tiêu chuẩn tìm chu trình âm có thể đi tới từ một đỉnh xuất phát $v$; tuy nhiên, ta có thể sửa thuật toán để tìm một chu trình âm bất kỳ trong toàn đồ thị.
Để làm vậy, đặt mọi khoảng cách $d[i]$ bằng $0$ thay vì vô cực — có thể xem như ta đang đồng thời tìm đường đi ngắn nhất từ mọi đỉnh. Việc phát hiện chu trình âm vẫn đúng.

Chạy Bellman-Ford trong $N$ vòng lặp. Nếu ở vòng cuối không có giá trị nào thay đổi, đồ thị không có chu trình âm. Ngược lại, lấy một đỉnh có khoảng cách bị thay đổi và lần theo các đỉnh cha của nó cho đến khi đi vào một chu trình. Chu trình thu được chính là một chu trình âm cần tìm.

### Cài đặt

```cpp
struct Edge {
    int a, b, cost;
};
 
int n;
vector<Edge> edges;
const int INF = 1000000000;
 
void solve() {
    vector<int> d(n, 0);
    vector<int> p(n, -1);
    int x;
 
    for (int i = 0; i < n; ++i) {
        x = -1;
        for (Edge e : edges) {
            if (d[e.a] + e.cost < d[e.b]) {
                d[e.b] = max(-INF, d[e.a] + e.cost);
                p[e.b] = e.a;
                x = e.b;
            }
        }
    }
 
    if (x == -1) {
        cout << "No negative cycle found.";
    } else {
        for (int i = 0; i < n; ++i)
            x = p[x];
 
        vector<int> cycle;
        for (int v = x;; v = p[v]) {
            cycle.push_back(v);
            if (v == x && cycle.size() > 1)
                break;
        }
        reverse(cycle.begin(), cycle.end());
 
        cout << "Negative cycle: ";
        for (int v : cycle)
            cout << v << ' ';
        cout << endl;
    }
}
```

## Sử dụng thuật toán Floyd-Warshall

Floyd-Warshall cho phép giải biến thể thứ hai: tìm mọi cặp đỉnh $(i, j)$ không tồn tại đường đi ngắn nhất giữa chúng, tức có thể tạo các đường đi với trọng số nhỏ tùy ý.

Chi tiết thuật toán nằm trong bài [Floyd-Warshall](all-pair-shortest-path-floyd-warshall.md); ở đây ta chỉ mô tả cách áp dụng.

Chạy Floyd-Warshall trên đồ thị.
Ban đầu đặt $d[v][v] = 0$ với mỗi $v$.
Sau khi thuật toán chạy xong, $d[v][v]$ sẽ nhỏ hơn $0$ nếu tồn tại một đường đi có tổng trọng số âm từ $v$ quay lại chính $v$.
Ta có thể dùng tính chất này để tìm mọi cặp đỉnh không có đường đi ngắn nhất.
Ta duyệt mọi cặp đỉnh $(i, j)$ và kiểm tra từng cặp.
Với mỗi cặp, thử mọi khả năng của đỉnh trung gian $t$.
Cặp $(i,j)$ không có đường đi ngắn nhất nếu tồn tại một đỉnh $t$ sao cho $d[t][t] < 0$ (tức $t$ nằm trên một chu trình âm), có thể đi từ $i$ đến $t$, và có thể đi từ $t$ đến $j$.
Khi đó, trọng số đường đi từ $i$ đến $j$ có thể giảm nhỏ tùy ý.
Ta ký hiệu trường hợp này bằng `-INF`.

### Cài đặt

```cpp
for (int i = 0; i < n; ++i) {
    for (int j = 0; j < n; ++j) {
        for (int t = 0; t < n; ++t) {
            if (d[i][t] < INF && d[t][t] < 0 && d[t][j] < INF)
                d[i][j] = - INF; 
        }
    }
}
```

## Bài tập luyện tập

- [UVA: Wormholes](https://uva.onlinejudge.org/index.php?option=com_onlinejudge&Itemid=8&page=show_problem&problem=499)
- [SPOJ: Alice in Amsterdam, I mean Wonderland](http://www.spoj.com/problems/UCV2013B/)
- [SPOJ: Johnsons Algorithm](http://www.spoj.com/problems/JHNSN/)
