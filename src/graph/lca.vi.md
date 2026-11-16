---
title: Lowest Common Ancestor - O(sqrt(N)) and O(log N) with O(N) preprocessing
tags:
  - Translated
e_maxx_link: lca
translation:
  source: graph/lca.md
  source_commit: 77882aa99fc7f07239448b66ff683e6d9fa2db8b
  status: draft
  last_synced: 2026-11-16
---
# Tổ tiên chung gần nhất - $O(\sqrt{N})$ và $O(\log N)$ với tiền xử lý $O(N)$

Cho một cây $G$ và các truy vấn dạng $(v_1, v_2)$. Với mỗi truy vấn, cần tìm tổ tiên chung gần nhất (lowest common ancestor, LCA), tức là đỉnh $v$ nằm trên cả đường đi từ gốc đến $v_1$ lẫn đường đi từ gốc đến $v_2$, đồng thời nằm thấp nhất. Nói cách khác, đỉnh $v$ cần tìm là tổ tiên ở thấp nhất của $v_1$ và $v_2$. Rõ ràng tổ tiên chung gần nhất của chúng nằm trên đường đi ngắn nhất từ $v_1$ đến $v_2$. Nếu $v_1$ là tổ tiên của $v_2$ thì $v_1$ chính là tổ tiên chung gần nhất của hai đỉnh.

### Ý tưởng thuật toán

Trước khi trả lời truy vấn, ta cần **tiền xử lý** cây.
Ta duyệt [DFS](depth-first-search.md) từ gốc và xây dựng danh sách $\text{euler}$ lưu thứ tự các đỉnh được thăm (một đỉnh được thêm vào danh sách khi được thăm lần đầu và sau khi DFS trở về từ mỗi con của nó).
Cách duyệt này còn được gọi là hành trình Euler trên cây.
Rõ ràng danh sách có kích thước $O(N)$.
Ta cũng cần xây dựng mảng $\text{first}[0..N-1]$ lưu lần xuất hiện đầu tiên của mỗi đỉnh $i$ trong $\text{euler}$.
Đó là vị trí đầu tiên trong $\text{euler}$ sao cho $\text{euler}[\text{first}[i]] = i$.
Bằng DFS, ta cũng có thể tìm độ cao của mỗi đỉnh (khoảng cách từ gốc đến đỉnh đó) và lưu vào mảng $\text{height}[0..N-1]$.

Vậy làm thế nào để trả lời truy vấn bằng hành trình Euler và hai mảng bổ sung?
Giả sử truy vấn là cặp $v_1$ và $v_2$.
Xét các đỉnh được thăm trong hành trình Euler từ lần thăm đầu tiên của $v_1$ đến lần thăm đầu tiên của $v_2$.
Dễ thấy $\text{LCA}(v_1, v_2)$ là đỉnh có độ cao nhỏ nhất trên đoạn hành trình này.
Ta đã nhận thấy LCA phải thuộc đường đi ngắn nhất giữa $v_1$ và $v_2$.
Rõ ràng nó cũng phải là đỉnh có độ cao nhỏ nhất.
Hành trình Euler về cơ bản đi theo đường đi ngắn nhất đó, chỉ khác là còn thăm thêm tất cả cây con gặp trên đường.
Nhưng mọi đỉnh trong những cây con này đều nằm thấp hơn LCA và do đó có độ cao lớn hơn.
Vì vậy, có thể xác định duy nhất $\text{LCA}(v_1, v_2)$ bằng cách tìm đỉnh có độ cao nhỏ nhất trong hành trình Euler giữa $\text{first}(v_1)$ và $\text{first}(v_2)$.

Ta minh họa ý tưởng này.
Xét đồ thị sau cùng hành trình Euler và các độ cao tương ứng:
<div style="text-align: center;">
  <img src="LCA_Euler.png" alt="Hành trình Euler tìm LCA">
</div>

$$\begin{array}{|l|c|c|c|c|c|c|c|c|c|c|c|c|c|}
\hline
\text{Vertices:}   & 1 & 2 & 5 & 2 & 6 & 2 & 1 & 3 & 1 & 4 & 7 & 4 & 1 \\ \hline
\text{Heights:} & 1 & 2 & 3 & 2 & 3 & 2 & 1 & 2 & 1 & 2 & 3 & 2 & 1 \\ \hline
\end{array}$$

Trên hành trình bắt đầu tại đỉnh $6$ và kết thúc tại $4$, ta thăm các đỉnh $[6, 2, 1, 3, 1, 4]$.
Trong số đó, đỉnh $1$ có độ cao nhỏ nhất, do đó $\text{LCA(6, 4) = 1}$.

Tóm lại:
để trả lời một truy vấn, ta chỉ cần **tìm đỉnh có độ cao nhỏ nhất** trong mảng $\text{euler}$ trên đoạn từ $\text{first}[v_1]$ đến $\text{first}[v_2]$.
Vậy **bài toán LCA được quy về bài toán RMQ** (tìm giá trị nhỏ nhất trên đoạn).

Với [chia căn](../data_structures/sqrt_decomposition.md), ta có thể trả lời mỗi truy vấn trong $O(\sqrt{N})$ sau khi tiền xử lý trong thời gian $O(N)$.

Với [cây phân đoạn](../data_structures/segment_tree.md), ta có thể trả lời mỗi truy vấn trong $O(\log N)$ sau khi tiền xử lý trong thời gian $O(N)$.

Do các giá trị được lưu hầu như không bao giờ cần cập nhật, [Sparse Table](../data_structures/sparse-table.md) có thể là lựa chọn tốt hơn, cho phép trả lời truy vấn trong $O(1)$ với thời gian xây dựng $O(N\log N)$.

### Cài đặt

Trong đoạn cài đặt thuật toán LCA sau đây, ta sử dụng cây phân đoạn.

```{.cpp file=lca}
struct LCA {
    vector<int> height, euler, first, segtree;
    vector<bool> visited;
    int n;

    LCA(vector<vector<int>> &adj, int root = 0) {
        n = adj.size();
        height.resize(n);
        first.resize(n);
        euler.reserve(n * 2);
        visited.assign(n, false);
        dfs(adj, root);
        int m = euler.size();
        segtree.resize(m * 4);
        build(1, 0, m - 1);
    }

    void dfs(vector<vector<int>> &adj, int node, int h = 0) {
        visited[node] = true;
        height[node] = h;
        first[node] = euler.size();
        euler.push_back(node);
        for (auto to : adj[node]) {
            if (!visited[to]) {
                dfs(adj, to, h + 1);
                euler.push_back(node);
            }
        }
    }

    void build(int node, int b, int e) {
        if (b == e) {
            segtree[node] = euler[b];
        } else {
            int mid = (b + e) / 2;
            build(node << 1, b, mid);
            build(node << 1 | 1, mid + 1, e);
            int l = segtree[node << 1], r = segtree[node << 1 | 1];
            segtree[node] = (height[l] < height[r]) ? l : r;
        }
    }

    int query(int node, int b, int e, int L, int R) {
        if (b > R || e < L)
            return -1;
        if (b >= L && e <= R)
            return segtree[node];
        int mid = (b + e) >> 1;

        int left = query(node << 1, b, mid, L, R);
        int right = query(node << 1 | 1, mid + 1, e, L, R);
        if (left == -1) return right;
        if (right == -1) return left;
        return height[left] < height[right] ? left : right;
    }

    int lca(int u, int v) {
        int left = first[u], right = first[v];
        if (left > right)
            swap(left, right);
        return query(1, 0, euler.size() - 1, left, right);
    }
};

```

## Bài tập
 - [SPOJ: LCA](http://www.spoj.com/problems/LCA/)
 - [SPOJ: DISQUERY](http://www.spoj.com/problems/DISQUERY/)
 - [TIMUS: 1471. Distance in the Tree](http://acm.timus.ru/problem.aspx?space=1&num=1471)
 - [CODEFORCES: Design Tutorial: Inverse the Problem](http://codeforces.com/problemset/problem/472/D)
 - [CODECHEF: Lowest Common Ancestor](https://www.codechef.com/problems/TALCA)
 * [SPOJ - Lowest Common Ancestor](http://www.spoj.com/problems/LCASQ/)
 * [SPOJ - Ada and Orange Tree](http://www.spoj.com/problems/ADAORANG/)
 * [DevSkill - Motoku (archived)](http://web.archive.org/web/20200922005503/https://devskill.com/CodingProblems/ViewProblem/141)
 * [UVA 12655 - Trucks](https://uva.onlinejudge.org/index.php?option=onlinejudge&page=show_problem&problem=4384)
 * [Codechef - Pishty and Tree](https://www.codechef.com/problems/PSHTTR)
 * [UVA - 12533 - Joining Couples](https://uva.onlinejudge.org/index.php?option=com_onlinejudge&Itemid=8&category=441&page=show_problem&problem=3978)
 * [Codechef - So close yet So Far](https://www.codechef.com/problems/CLOSEFAR)
 * [Codeforces - Drivers Dissatisfaction](http://codeforces.com/contest/733/problem/F)
 * [UVA 11354 - Bond](https://uva.onlinejudge.org/index.php?option=com_onlinejudge&Itemid=8&page=show_problem&problem=2339)
 * [SPOJ - Query on a tree II](http://www.spoj.com/problems/QTREE2/)
 * [Codeforces - Best Edge Weight](http://codeforces.com/contest/828/problem/F)
 * [Codeforces - Misha, Grisha and Underground](http://codeforces.com/contest/832/problem/D)
 * [SPOJ - Nlogonian Tickets](http://www.spoj.com/problems/NTICKETS/)
 * [Codeforces - Rowena Rawenclaws Diadem](http://codeforces.com/contest/855/problem/D)
