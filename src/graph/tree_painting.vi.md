---
tags:
  - Translated
e_maxx_link: tree_painting
translation:
  source: graph/tree_painting.md
  source_commit: 0b5f10505dc122d4b87bf1d0f99ea7c294274254
  status: draft
  last_synced: 2026-11-16
---

# Tô màu các cạnh của cây

Đây là một bài toán khá thường gặp. Cho cây $G$ có $N$ đỉnh. Có hai loại truy vấn: tô màu một cạnh và hỏi số cạnh được tô màu giữa hai đỉnh.

Ta mô tả một lời giải khá đơn giản (dùng [cây đoạn](../data_structures/segment_tree.md)) để trả lời mỗi truy vấn trong $O(\log N)$ thời gian. Bước tiền xử lý mất $O(N)$ thời gian.

## Thuật toán

Trước hết, ta cần tìm [LCA](lca.md) để đưa mỗi truy vấn loại hai $(i,j)$ về hai truy vấn $(l,i)$ và $(l,j)$, trong đó $l$ là LCA của $i$ và $j$. Kết quả của truy vấn $(i,j)$ là tổng kết quả hai truy vấn con. Hai truy vấn này đều có cấu trúc đặc biệt: đỉnh đầu tiên là tổ tiên của đỉnh thứ hai. Trong phần còn lại, ta chỉ xét các truy vấn đặc biệt này.

Ta bắt đầu bằng bước **tiền xử lý**. Chạy tìm kiếm theo chiều sâu từ gốc cây và ghi lại hành trình Euler của phép tìm kiếm (mỗi đỉnh được thêm vào danh sách khi được thăm lần đầu và mỗi khi ta quay về từ một trong các con của nó). Kỹ thuật tương tự có thể dùng khi tiền xử lý LCA.

Danh sách này chứa mỗi cạnh (nghĩa là nếu $i$ và $j$ là hai đầu cạnh thì có một vị trí trong danh sách mà $i$ và $j$ nằm cạnh nhau), và cạnh xuất hiện đúng hai lần: theo chiều thuận (từ $i$ đến $j$, với đỉnh $i$ gần gốc hơn đỉnh $j$) và theo chiều ngược (từ $j$ đến $i$).

Ta xây dựng hai danh sách cho các cạnh này. Danh sách thứ nhất lưu màu của tất cả các cạnh theo chiều thuận, danh sách thứ hai lưu màu theo chiều ngược. Ta dùng $1$ nếu cạnh được tô màu, và $0$ trong trường hợp ngược lại. Trên mỗi danh sách, xây dựng một cây đoạn (tính tổng và cập nhật một phần tử), gọi chúng là $T1$ và $T2$.

Xét truy vấn dạng $(i,j)$, trong đó $i$ là tổ tiên của $j$. Ta cần xác định số cạnh được tô màu trên đường đi giữa $i$ và $j$. Tìm lần xuất hiện đầu tiên của $i$ và $j$ trong hành trình Euler, lần lượt ở các vị trí $p$ và $q$ (có thể làm trong $O(1)$ nếu tính trước các vị trí này khi tiền xử lý). Khi đó **đáp án** là tổng $T1[p..q-1]$ trừ tổng $T2[p..q-1]$.

**Tại sao?** Xét đoạn $[p;q]$ trong hành trình Euler. Nó chứa mọi cạnh trên đường đi cần tìm từ $i$ đến $j$, nhưng cũng chứa các cạnh thuộc những đường đi khác từ $i$. Có một khác biệt lớn giữa hai nhóm: các cạnh cần tìm chỉ xuất hiện một lần theo chiều thuận, còn mọi cạnh khác xuất hiện hai lần: một lần theo chiều thuận và một lần theo chiều ngược. Vì vậy hiệu $T1[p..q-1] - T2[p..q-1]$ cho đáp án đúng (cần trừ một ở chỉ số cuối vì nếu không ta sẽ lấy thêm một cạnh đi ra từ đỉnh $j$). Truy vấn tổng trên cây đoạn mất $O(\log N)$.

Trả lời **truy vấn loại một** (tô màu một cạnh) còn dễ hơn: ta chỉ cần cập nhật $T1$ và $T2$, cụ thể là cập nhật một phần tử tương ứng với cạnh đó (việc tìm cạnh trong danh sách cũng có thể thực hiện trong $O(1)$ nếu tìm trước khi tiền xử lý). Một lần cập nhật trên cây đoạn mất $O(\log N)$.

## Cài đặt

Sau đây là toàn bộ cài đặt của lời giải, bao gồm cả tính LCA:

Ghi chú bản dịch: Phần xử lý truy vấn trong hàm chính là mã khung chưa hoàn chỉnh: điều kiện rẽ nhánh và các biến truy vấn cần được cung cấp. Việc cập nhật cũng giả định thao tác làm thay đổi trạng thái tô của cạnh.

```cpp
const int INF = 1000 * 1000 * 1000;

typedef vector<vector<int>> graph;

vector<int> dfs_list;
vector<int> edges_list;
vector<int> h;

void dfs(int v, const graph& g, const graph& edge_ids, int cur_h = 1) {
    h[v] = cur_h;
    dfs_list.push_back(v);
    for (size_t i = 0; i < g[v].size(); ++i) {
        if (h[g[v][i]] == -1) {
            edges_list.push_back(edge_ids[v][i]);
            dfs(g[v][i], g, edge_ids, cur_h + 1);
            edges_list.push_back(edge_ids[v][i]);
            dfs_list.push_back(v);
        }
    }
}

vector<int> lca_tree;
vector<int> first;

void lca_tree_build(int i, int l, int r) {
    if (l == r) {
        lca_tree[i] = dfs_list[l];
    } else {
        int m = (l + r) >> 1;
        lca_tree_build(i + i, l, m);
        lca_tree_build(i + i + 1, m + 1, r);
        int lt = lca_tree[i + i], rt = lca_tree[i + i + 1];
        lca_tree[i] = h[lt] < h[rt] ? lt : rt;
    }
}

void lca_prepare(int n) {
    lca_tree.assign(dfs_list.size() * 8, -1);
    lca_tree_build(1, 0, (int)dfs_list.size() - 1);

    first.assign(n, -1);
    for (int i = 0; i < (int)dfs_list.size(); ++i) {
        int v = dfs_list[i];
        if (first[v] == -1)
            first[v] = i;
    }
}

int lca_tree_query(int i, int tl, int tr, int l, int r) {
    if (tl == l && tr == r)
        return lca_tree[i];
    int m = (tl + tr) >> 1;
    if (r <= m)
        return lca_tree_query(i + i, tl, m, l, r);
    if (l > m)
        return lca_tree_query(i + i + 1, m + 1, tr, l, r);
    int lt = lca_tree_query(i + i, tl, m, l, m);
    int rt = lca_tree_query(i + i + 1, m + 1, tr, m + 1, r);
    return h[lt] < h[rt] ? lt : rt;
}

int lca(int a, int b) {
    if (first[a] > first[b])
        swap(a, b);
    return lca_tree_query(1, 0, (int)dfs_list.size() - 1, first[a], first[b]);
}

vector<int> first1, first2;
vector<char> edge_used;
vector<int> tree1, tree2;

void query_prepare(int n) {
    first1.resize(n - 1, -1);
    first2.resize(n - 1, -1);
    for (int i = 0; i < (int)edges_list.size(); ++i) {
        int j = edges_list[i];
        if (first1[j] == -1)
            first1[j] = i;
        else
            first2[j] = i;
    }

    edge_used.resize(n - 1);
    tree1.resize(edges_list.size() * 8);
    tree2.resize(edges_list.size() * 8);
}

void sum_tree_update(vector<int>& tree, int i, int l, int r, int j, int delta) {
    tree[i] += delta;
    if (l < r) {
        int m = (l + r) >> 1;
        if (j <= m)
            sum_tree_update(tree, i + i, l, m, j, delta);
        else
            sum_tree_update(tree, i + i + 1, m + 1, r, j, delta);
    }
}

int sum_tree_query(const vector<int>& tree, int i, int tl, int tr, int l, int r) {
    if (l > r || tl > tr)
        return 0;
    if (tl == l && tr == r)
        return tree[i];
    int m = (tl + tr) >> 1;
    if (r <= m)
        return sum_tree_query(tree, i + i, tl, m, l, r);
    if (l > m)
        return sum_tree_query(tree, i + i + 1, m + 1, tr, l, r);
    return sum_tree_query(tree, i + i, tl, m, l, m) +
           sum_tree_query(tree, i + i + 1, m + 1, tr, m + 1, r);
}

int query(int v1, int v2) {
    return sum_tree_query(tree1, 1, 0, (int)edges_list.size() - 1, first[v1], first[v2] - 1) -
           sum_tree_query(tree2, 1, 0, (int)edges_list.size() - 1, first[v1], first[v2] - 1);
}

int main() {
    // reading the graph
    int n;
    scanf("%d", &n);
    graph g(n), edge_ids(n);
    for (int i = 0; i < n - 1; ++i) {
        int v1, v2;
        scanf("%d%d", &v1, &v2);
        --v1, --v2;
        g[v1].push_back(v2);
        g[v2].push_back(v1);
        edge_ids[v1].push_back(i);
        edge_ids[v2].push_back(i);
    }

    h.assign(n, -1);
    dfs(0, g, edge_ids);
    lca_prepare(n);
    query_prepare(n);

    for (;;) {
        if () {
            // request for painting edge x;
            // if start = true, then the edge is painted, otherwise the painting
            // is removed
            edge_used[x] = start;
            sum_tree_update(tree1, 1, 0, (int)edges_list.size() - 1, first1[x],
                            start ? 1 : -1);
            sum_tree_update(tree2, 1, 0, (int)edges_list.size() - 1, first2[x],
                            start ? 1 : -1);
        } else {
            // query the number of colored edges on the path between v1 and v2
            int l = lca(v1, v2);
            int result = query(l, v1) + query(l, v2);
            // result - the answer to the request
        }
    }
}
```
