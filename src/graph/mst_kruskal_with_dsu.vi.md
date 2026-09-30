---
tags:
  - Translated
e_maxx_link: mst_kruskal_with_dsu
translation:
  source: graph/mst_kruskal_with_dsu.md
  source_commit: e1637545a38553a93c2733c4b358f7824645ae5a
  status: draft
  last_synced: 2026-09-30
---

# Cây khung nhỏ nhất - Kruskal với Hợp các tập rời nhau

Để tìm hiểu bài toán MST và thuật toán Kruskal, trước tiên hãy xem [bài viết chính về thuật toán Kruskal](mst_kruskal.md).

Trong bài viết này, ta sẽ xét cấu trúc dữ liệu ["Hợp các tập rời nhau" (Disjoint Set Union)](../data_structures/disjoint_set_union.md) để cài đặt thuật toán Kruskal, nhờ đó thuật toán đạt độ phức tạp thời gian $O(M \log N)$.

## Mô tả

Tương tự phiên bản đơn giản của thuật toán Kruskal, ta sắp xếp tất cả các cạnh của đồ thị theo thứ tự trọng số không giảm.
Sau đó, đưa mỗi đỉnh vào một cây riêng (tức là tập riêng của nó) bằng các lời gọi hàm `make_set` - tổng cộng mất $O(N)$.
Ta duyệt tất cả các cạnh (theo thứ tự đã sắp xếp) và với mỗi cạnh, xác định xem hai đầu mút có thuộc hai cây khác nhau hay không (bằng hai lời gọi `find_set`, mỗi lời gọi mất $O(1)$).
Cuối cùng, ta cần hợp hai cây (hai tập), khi đó hàm `union_sets` của DSU được gọi - cũng mất $O(1)$.
Vì vậy, tổng độ phức tạp thời gian là $O(M \log N + N + M)$ = $O(M \log N)$.

## Cài đặt

Dưới đây là một cài đặt thuật toán Kruskal sử dụng hợp theo hạng (Union by Rank).

```cpp
vector<int> parent, rank;

void make_set(int v) {
    parent[v] = v;
    rank[v] = 0;
}

int find_set(int v) {
    if (v == parent[v])
        return v;
    return parent[v] = find_set(parent[v]);
}

void union_sets(int a, int b) {
    a = find_set(a);
    b = find_set(b);
    if (a != b) {
        if (rank[a] < rank[b])
            swap(a, b);
        parent[b] = a;
        if (rank[a] == rank[b])
            rank[a]++;
    }
}

struct Edge {
    int u, v, weight;
    bool operator<(Edge const& other) {
        return weight < other.weight;
    }
};

int n;
vector<Edge> edges;

int cost = 0;
vector<Edge> result;
parent.resize(n);
rank.resize(n);
for (int i = 0; i < n; i++)
    make_set(i);

sort(edges.begin(), edges.end());

for (Edge e : edges) {
    if (find_set(e.u) != find_set(e.v)) {
        cost += e.weight;
        result.push_back(e);
        union_sets(e.u, e.v);
    }
}
```

Lưu ý: vì MST chứa đúng $N-1$ cạnh, ta có thể dừng vòng lặp for ngay khi đã tìm đủ số cạnh này.

## Bài tập luyện tập

Xem [bài viết chính về thuật toán Kruskal](mst_kruskal.md) để xem danh sách bài tập luyện tập về chủ đề này.
