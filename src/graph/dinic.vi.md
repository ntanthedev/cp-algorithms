---
tags:
  - Translated
e_maxx_link: dinic
translation:
  source: graph/dinic.md
  source_commit: 2947e05b29f489b81c38730932f5eb3ed7d56f02
  status: draft
  last_synced: 2026-08-07
---

# Luồng cực đại - Thuật toán Dinic

Thuật toán Dinic giải bài toán luồng cực đại trong $O(V^2E)$. Bài toán luồng cực đại được định nghĩa trong bài [Luồng cực đại - Ford-Fulkerson và Edmonds-Karp](edmonds_karp.md). Thuật toán này do Yefim Dinitz phát hiện vào năm 1970.

## Định nghĩa

**Mạng thặng dư** $G^R$ của mạng $G$ là một mạng chứa hai cạnh ứng với mỗi cạnh $(v, u)\in G$:<br>

- $(v, u)$ có dung lượng $c_{vu}^R = c_{vu} - f_{vu}$
- $(u, v)$ có dung lượng $c_{uv}^R = f_{vu}$

**Luồng cản** (blocking flow) của một mạng là một luồng sao cho mọi đường đi từ $s$ tới $t$ đều chứa ít nhất một cạnh bị luồng này làm bão hòa. Lưu ý rằng luồng cản không nhất thiết là luồng cực đại.

**Đồ thị phân cấp** (layered network) của một mạng $G$ được xây dựng như sau. Trước hết, với mỗi đỉnh $v$ ta tính `level[v]` — độ dài đường đi ngắn nhất (không trọng số) từ $s$ tới đỉnh đó, chỉ sử dụng các cạnh có dung lượng dương. Sau đó ta chỉ giữ các cạnh $(v, u)$ thỏa mãn $level[v] + 1 = level[u]$. Hiển nhiên đồ thị này không có chu trình.

## Thuật toán

Thuật toán gồm nhiều pha. Ở mỗi pha, ta xây dựng đồ thị phân cấp của mạng thặng dư của $G$. Sau đó, ta tìm một luồng cản bất kỳ trong đồ thị phân cấp và cộng nó vào luồng hiện tại.

## Chứng minh tính đúng đắn

Ta chứng minh rằng nếu thuật toán kết thúc thì nó tìm được luồng cực đại.

Nếu thuật toán đã kết thúc, nó không thể tìm được luồng cản trong đồ thị phân cấp. Điều đó có nghĩa là đồ thị phân cấp không còn đường đi nào từ $s$ tới $t$. Suy ra mạng thặng dư không còn đường đi nào từ $s$ tới $t$. Vì vậy luồng hiện tại là cực đại.

## Số pha

Thuật toán kết thúc sau ít hơn $V$ pha. Để chứng minh điều này, trước hết ta cần hai bổ đề.

**Bổ đề 1.** Khoảng cách từ $s$ tới mỗi đỉnh không giảm sau mỗi lần lặp, tức là $level_{i+1}[v] \ge level_i[v]$.

**Chứng minh.** Cố định một pha $i$ và một đỉnh $v$. Xét một đường đi ngắn nhất bất kỳ $P$ từ $s$ tới $v$ trong $G_{i+1}^R$. Độ dài của $P$ bằng $level_{i+1}[v]$. Lưu ý rằng $G_{i+1}^R$ chỉ có thể chứa các cạnh của $G_i^R$ và các cạnh ngược ứng với cạnh của $G_i^R$. Nếu $P$ không có cạnh ngược nào so với $G_i^R$, thì $level_{i+1}[v] \ge level_i[v]$ vì $P$ cũng là một đường đi trong $G_i^R$. Bây giờ giả sử $P$ có ít nhất một cạnh ngược. Gọi cạnh ngược đầu tiên là $(u, w)$. Khi đó $level_{i+1}[u] \ge level_i[u]$ (theo trường hợp thứ nhất). Cạnh $(u, w)$ không thuộc $G_i^R$, nên cạnh $(w, u)$ đã bị ảnh hưởng bởi luồng cản ở lần lặp trước. Điều này có nghĩa là $level_i[u] = level_i[w] + 1$. Đồng thời, $level_{i+1}[w] = level_{i+1}[u] + 1$. Từ hai đẳng thức này và $level_{i+1}[u] \ge level_i[u]$, ta suy ra $level_{i+1}[w] \ge level_i[w] + 2$. Bây giờ ta có thể áp dụng cùng lập luận cho phần còn lại của đường đi.

**Bổ đề 2.** $level_{i+1}[t] > level_i[t]$

**Chứng minh.** Từ bổ đề trước, $level_{i+1}[t] \ge level_i[t]$. Giả sử $level_{i+1}[t] = level_i[t]$. Lưu ý rằng $G_{i+1}^R$ chỉ có thể chứa các cạnh của $G_i^R$ và các cạnh ngược ứng với cạnh của $G_i^R$. Khi đó tồn tại một đường đi ngắn nhất trong $G_i^R$ chưa bị luồng cản chặn. Đây là một mâu thuẫn.

Từ hai bổ đề trên, ta kết luận rằng có ít hơn $V$ pha vì $level[t]$ tăng sau mỗi pha nhưng không thể lớn hơn $V - 1$.

## Tìm luồng cản

Để tìm luồng cản ở mỗi lần lặp, ta có thể đơn giản thử đẩy luồng bằng DFS từ $s$ tới $t$ trong đồ thị phân cấp chừng nào còn đẩy được. Để làm nhanh hơn, ta cần bỏ qua các cạnh không còn có thể dùng để đẩy luồng. Ta có thể làm điều này bằng cách lưu tại mỗi đỉnh một con trỏ tới cạnh tiếp theo có thể được xét.

Một lần chạy DFS mất $O(k+V)$ thời gian, trong đó $k$ là số lần con trỏ được tăng trong lần chạy đó. Cộng trên tất cả các lần chạy, tổng số lần tăng con trỏ không thể vượt quá $E$. Mặt khác, tổng số lần chạy cũng không vượt quá $E$, vì mỗi lần chạy làm bão hòa ít nhất một cạnh. Do đó, tổng thời gian để tìm một luồng cản là $O(VE)$.

## Độ phức tạp

Có ít hơn $V$ pha, nên tổng độ phức tạp là $O(V^2E)$.

## Mạng đơn vị

Một **mạng đơn vị** (unit network) là một mạng mà với mọi đỉnh ngoại trừ $s$ và $t$, **hoặc cạnh đi vào hoặc cạnh đi ra là duy nhất và có dung lượng đơn vị**. Đây chính là trường hợp của mạng được xây dựng để giải bài toán ghép cặp cực đại bằng luồng.

Trên mạng đơn vị, thuật toán Dinic chạy trong $O(E\sqrt{V})$. Ta chứng minh điều này.

Trước hết, mỗi pha lúc này chạy trong $O(E)$ vì mỗi cạnh chỉ được xét nhiều nhất một lần.

Tiếp theo, giả sử đã có $\sqrt{V}$ pha. Khi đó mọi đường tăng luồng có độ dài $\le\sqrt{V}$ đã được tìm thấy. Gọi $f$ là luồng hiện tại, $f'$ là luồng cực đại. Xét hiệu $f' - f$. Đây là một luồng trong $G^R$ có giá trị $|f'| - |f|$, và trên mỗi cạnh nó chỉ nhận giá trị $0$ hoặc $1$. Ta có thể phân rã nó thành $|f'| - |f|$ đường đi từ $s$ tới $t$ và có thể thêm một số chu trình. Vì mạng là mạng đơn vị, các đường này không thể có đỉnh chung, nên tổng số đỉnh là $\ge (|f'| - |f|)\sqrt{V}$, nhưng đồng thời cũng $\le V$. Vì vậy, trong thêm $\sqrt{V}$ lần lặp nữa, ta chắc chắn tìm được luồng cực đại.

### Mạng có dung lượng đơn vị

Trong trường hợp tổng quát hơn khi mọi cạnh đều có dung lượng đơn vị, _nhưng số cạnh đi vào và đi ra không bị chặn_, các đường không thể có cạnh chung thay vì không thể có đỉnh chung. Lập luận tương tự cho phép chứng minh cận $\sqrt E$ cho số lần lặp, do đó thời gian chạy của Dinic trên các mạng như vậy không vượt quá $O(E \sqrt E)$.

Cuối cùng, cũng có thể chứng minh rằng số pha trên mạng có dung lượng đơn vị không vượt quá $O(V^{2/3})$, từ đó có một cận khác là $O(EV^{2/3})$ cho các mạng có số cạnh đặc biệt lớn.

## Cài đặt

```{.cpp file=dinic}
struct FlowEdge {
    int v, u;
    long long cap, flow = 0;
    FlowEdge(int v, int u, long long cap) : v(v), u(u), cap(cap) {}
};

struct Dinic {
    const long long flow_inf = 1e18;
    vector<FlowEdge> edges;
    vector<vector<int>> adj;
    int n, m = 0;
    int s, t;
    vector<int> level, ptr;
    queue<int> q;

    Dinic(int n, int s, int t) : n(n), s(s), t(t) {
        adj.resize(n);
        level.resize(n);
        ptr.resize(n);
    }

    void add_edge(int v, int u, long long cap) {
        edges.emplace_back(v, u, cap);
        edges.emplace_back(u, v, 0);
        adj[v].push_back(m);
        adj[u].push_back(m + 1);
        m += 2;
    }

    bool bfs() {
        while (!q.empty()) {
            int v = q.front();
            q.pop();
            for (int id : adj[v]) {
                if (edges[id].cap == edges[id].flow)
                    continue;
                if (level[edges[id].u] != -1)
                    continue;
                level[edges[id].u] = level[v] + 1;
                q.push(edges[id].u);
            }
        }
        return level[t] != -1;
    }

    long long dfs(int v, long long pushed) {
        if (pushed == 0)
            return 0;
        if (v == t)
            return pushed;
        for (int& cid = ptr[v]; cid < (int)adj[v].size(); cid++) {
            int id = adj[v][cid];
            int u = edges[id].u;
            if (level[v] + 1 != level[u])
                continue;
            long long tr = dfs(u, min(pushed, edges[id].cap - edges[id].flow));
            if (tr == 0)
                continue;
            edges[id].flow += tr;
            edges[id ^ 1].flow -= tr;
            return tr;
        }
        return 0;
    }

    long long flow() {
        long long f = 0;
        while (true) {
            fill(level.begin(), level.end(), -1);
            level[s] = 0;
            q.push(s);
            if (!bfs())
                break;
            fill(ptr.begin(), ptr.end(), 0);
            while (long long pushed = dfs(s, flow_inf)) {
                f += pushed;
            }
        }
        return f;
    }
};
```

## Bài tập luyện tập

* [SPOJ: FASTFLOW](https://www.spoj.com/problems/FASTFLOW/)