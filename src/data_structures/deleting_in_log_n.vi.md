---
title: Deleting from a data structure in O(T(n) log n)
tags:
  - Original
translation:
  source: data_structures/deleting_in_log_n.md
  source_commit: debc9a83afd9dffaf5f88c0c4a87b88ec9746d94
  status: draft
  last_synced: 2026-11-15
---
# Xóa khỏi cấu trúc dữ liệu trong $O(T(n)\log n)$

Giả sử ta có một cấu trúc dữ liệu cho phép thêm phần tử với độ phức tạp **thực sự** $O(T(n))$.
Bài viết này mô tả một kỹ thuật cho phép xóa phần tử ngoại tuyến với độ phức tạp $O(T(n)\log n)$.

## Thuật toán

Mỗi phần tử tồn tại trong cấu trúc dữ liệu qua một số khoảng thời gian giữa lúc được thêm vào và lúc bị xóa.
Ta xây dựng một cây phân đoạn trên các truy vấn.
Mỗi khoảng thời gian mà một phần tử còn tồn tại được phân rã thành $O(\log n)$ nút của cây.
Ta đặt mỗi truy vấn cần lấy thông tin về cấu trúc dữ liệu vào lá tương ứng.
Để xử lý tất cả truy vấn, ta duyệt DFS trên cây phân đoạn.
Khi vào một nút, ta thêm tất cả phần tử được gán cho nút đó.
Sau đó, ta đi tiếp xuống các nút con hoặc trả lời truy vấn nếu đang ở nút lá.
Khi rời khỏi một nút, ta phải hoàn tác các thao tác thêm.
Lưu ý rằng nếu một thay đổi trên cấu trúc dữ liệu tốn $O(T(n))$, ta có thể hoàn tác thay đổi đó với chi phí $O(T(n))$ bằng cách lưu các thay đổi vào một ngăn xếp.
Lưu ý rằng thao tác hoàn tác làm mất hiệu lực của phân tích độ phức tạp khấu hao.

## Ghi chú

Ý tưởng tạo cây phân đoạn trên các khoảng thời gian mà một đối tượng còn tồn tại có thể được dùng cho nhiều bài toán khác, không chỉ các bài toán về cấu trúc dữ liệu.
Xem một số bài toán bên dưới.

## Cài đặt

Cài đặt sau giải bài toán [liên thông động](https://en.wikipedia.org/wiki/Dynamic_connectivity).
Nó có thể thêm cạnh, xóa cạnh và đếm số thành phần liên thông.

```{.cpp file=dynamic-conn}
struct dsu_save {
    int v, rnkv, u, rnku;

    dsu_save() {}

    dsu_save(int _v, int _rnkv, int _u, int _rnku)
        : v(_v), rnkv(_rnkv), u(_u), rnku(_rnku) {}
};

struct dsu_with_rollbacks {
    vector<int> p, rnk;
    int comps;
    stack<dsu_save> op;

    dsu_with_rollbacks() {}

    dsu_with_rollbacks(int n) {
        p.resize(n);
        rnk.resize(n);
        for (int i = 0; i < n; i++) {
            p[i] = i;
            rnk[i] = 0;
        }
        comps = n;
    }

    int find_set(int v) {
        return (v == p[v]) ? v : find_set(p[v]);
    }

    bool unite(int v, int u) {
        v = find_set(v);
        u = find_set(u);
        if (v == u)
            return false;
        comps--;
        if (rnk[v] > rnk[u])
            swap(v, u);
        op.push(dsu_save(v, rnk[v], u, rnk[u]));
        p[v] = u;
        if (rnk[u] == rnk[v])
            rnk[u]++;
        return true;
    }

    void rollback() {
        if (op.empty())
            return;
        dsu_save x = op.top();
        op.pop();
        comps++;
        p[x.v] = x.v;
        rnk[x.v] = x.rnkv;
        p[x.u] = x.u;
        rnk[x.u] = x.rnku;
    }
};

struct query {
    int v, u;
    bool united;
    query(int _v, int _u) : v(_v), u(_u) {
    }
};

struct QueryTree {
    vector<vector<query>> t;
    dsu_with_rollbacks dsu;
    int T;

    QueryTree() {}

    QueryTree(int _T, int n) : T(_T) {
        dsu = dsu_with_rollbacks(n);
        t.resize(4 * T + 4);
    }

    void add_to_tree(int v, int l, int r, int ul, int ur, query& q) {
        if (ul > ur)
            return;
        if (l == ul && r == ur) {
            t[v].push_back(q);
            return;
        }
        int mid = (l + r) / 2;
        add_to_tree(2 * v, l, mid, ul, min(ur, mid), q);
        add_to_tree(2 * v + 1, mid + 1, r, max(ul, mid + 1), ur, q);
    }

    void add_query(query q, int l, int r) {
        add_to_tree(1, 0, T - 1, l, r, q);
    }

    void dfs(int v, int l, int r, vector<int>& ans) {
        for (query& q : t[v]) {
            q.united = dsu.unite(q.v, q.u);
        }
        if (l == r)
            ans[l] = dsu.comps;
        else {
            int mid = (l + r) / 2;
            dfs(2 * v, l, mid, ans);
            dfs(2 * v + 1, mid + 1, r, ans);
        }
        for (query q : t[v]) {
            if (q.united)
                dsu.rollback();
        }
    }

    vector<int> solve() {
        vector<int> ans(T);
        dfs(1, 0, T - 1, ans);
        return ans;
    }
};
```

**Ghi chú bản dịch:** Cài đặt này giả sử T > 0. Nếu không có truy vấn, cần xử lý riêng và trả về kết quả rỗng trước khi gọi solve().

## Bài toán

- [Codeforces - Connect and Disconnect](https://codeforces.com/gym/100551/problem/A)
- [Codeforces - Addition on Segments](https://codeforces.com/contest/981/problem/E)
- [Codeforces - Extending Set of Points](https://codeforces.com/contest/1140/problem/F)
