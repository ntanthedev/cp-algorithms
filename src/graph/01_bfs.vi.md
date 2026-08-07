---
tags:
  - Original
translation:
  source: graph/01_bfs.md
  source_commit: ff481e4614336d073f3032a2d6288141393956b8
  status: draft
  last_synced: 2026-08-07
---

# 0-1 BFS

Ta đã biết có thể tìm đường đi ngắn nhất từ một nguồn đến mọi đỉnh khác trong $O(|E|)$ bằng [tìm kiếm theo chiều rộng](breadth-first-search.md) trên **đồ thị không trọng số**, tức khoảng cách là số cạnh ít nhất cần đi qua từ đỉnh nguồn đến một đỉnh khác.
Ta cũng có thể xem đồ thị này như một đồ thị có trọng số, trong đó mọi cạnh đều có trọng số $1$.
Nếu các cạnh không cùng trọng số, ta cần một thuật toán tổng quát hơn, chẳng hạn [Dijkstra](dijkstra.md), với thời gian chạy $O(|V|^2 + |E|)$ hoặc $O(|E| \log |V|)$.

Tuy nhiên, nếu trọng số bị giới hạn hơn, ta thường có thể làm tốt hơn.
Trong bài này, ta sẽ thấy cách dùng BFS để giải bài toán đường đi ngắn nhất từ một nguồn (single-source shortest path, SSSP) trong $O(|E|)$ khi trọng số mỗi cạnh chỉ có thể là $0$ hoặc $1$.

## Thuật toán

Ta có thể xây dựng thuật toán bằng cách xem kỹ Dijkstra và phân tích hệ quả của điều kiện đặc biệt về trọng số.
Dạng tổng quát của Dijkstra như sau (ở đây dùng một `set` làm hàng đợi ưu tiên):

```cpp
d.assign(n, INF);
d[s] = 0;
set<pair<int, int>> q;
q.insert({0, s});
while (!q.empty()) {
    int v = q.begin()->second;
    q.erase(q.begin());

    for (auto edge : adj[v]) {
        int u = edge.first;
        int w = edge.second;

        if (d[v] + w < d[u]) {
            q.erase({d[u], u});
            d[u] = d[v] + w;
            q.insert({d[u], u});
        }
    }
}
```

Ta nhận thấy hiệu giữa khoảng cách từ nguồn `s` đến hai đỉnh bất kỳ đang nằm trong hàng đợi không vượt quá một.
Cụ thể, với mỗi $u \in Q$, ta có $d[v] \le d[u] \le d[v] + 1$.
Lý do là trong mỗi bước lặp, ta chỉ thêm vào hàng đợi các đỉnh có khoảng cách bằng khoảng cách hiện tại hoặc lớn hơn đúng một đơn vị.
Giả sử tồn tại một đỉnh $u$ trong hàng đợi sao cho $d[u] - d[v] > 1$. Khi đó $u$ phải được đưa vào hàng đợi thông qua một đỉnh khác $t$ với $d[t] \ge d[u] - 1 > d[v]$.
Điều này là không thể vì Dijkstra xử lý các đỉnh theo thứ tự khoảng cách tăng dần.

Do đó, thứ tự của hàng đợi có dạng:

$$Q = \underbrace{v}_{d[v]}, \dots, \underbrace{u}_{d[v]}, \underbrace{m}_{d[v]+1} \dots \underbrace{n}_{d[v]+1}$$

Cấu trúc này đơn giản đến mức ta không cần một hàng đợi ưu tiên thực sự; dùng cây nhị phân cân bằng sẽ là quá mức cần thiết.
Ta chỉ cần một hàng đợi hai đầu: nếu cạnh tương ứng có trọng số $0$, tức $d[u] = d[v]$, ta đưa đỉnh mới vào đầu; nếu cạnh có trọng số $1$, tức $d[u] = d[v] + 1$, ta đưa đỉnh vào cuối.
Nhờ vậy, hàng đợi luôn được giữ theo thứ tự khoảng cách.

```cpp
vector<int> d(n, INF);
d[s] = 0;
deque<int> q;
q.push_front(s);
while (!q.empty()) {
    int v = q.front();
    q.pop_front();
    for (auto edge : adj[v]) {
        int u = edge.first;
        int w = edge.second;
        if (d[v] + w < d[u]) {
            d[u] = d[v] + w;
            if (w == 1)
                q.push_back(u);
            else
                q.push_front(u);
        }
    }
}
```

## Thuật toán Dial

Ta còn có thể mở rộng ý tưởng này khi cho phép trọng số cạnh lớn hơn.
Nếu mọi cạnh của đồ thị có trọng số $\le k$, thì khoảng cách của các đỉnh trong hàng đợi chỉ lệch tối đa $k$ so với khoảng cách từ $v$ đến nguồn.
Vì vậy, ta có thể duy trì $k + 1$ bucket cho các đỉnh trong hàng đợi; mỗi khi bucket ứng với khoảng cách nhỏ nhất trở nên rỗng, ta dịch vòng để chuyển sang bucket có khoảng cách lớn hơn kế tiếp.
Phần mở rộng này được gọi là **thuật toán Dial** (Dial's algorithm).

## Bài tập luyện tập

- [Labyrinth](https://codeforces.com/contest/1063/problem/B)
- [KATHTHI](http://www.spoj.com/problems/KATHTHI/)
- [DoNotTurn](https://community.topcoder.com/stat?c=problem_statement&pm=10337)
- [Ocean Currents](https://onlinejudge.org/index.php?option=onlinejudge&page=show_problem&problem=2620)
- [Olya and Energy Drinks](https://codeforces.com/problemset/problem/877/D)
- [Three States](https://codeforces.com/problemset/problem/590/C)
- [Colliding Traffic](https://onlinejudge.org/index.php?option=com_onlinejudge&Itemid=8&page=show_problem&problem=2621)
- [CHamber of Secrets](https://codeforces.com/problemset/problem/173/B)
- [Spiral Maximum](https://codeforces.com/problemset/problem/173/C)
- [Minimum Cost to Make at Least One Valid Path in a Grid](https://leetcode.com/problems/minimum-cost-to-make-at-least-one-valid-path-in-a-grid)
