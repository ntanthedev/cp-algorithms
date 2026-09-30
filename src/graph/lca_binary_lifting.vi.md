---
tags:
  - Translated
e_maxx_link: lca_simpler
translation:
  source: graph/lca_binary_lifting.md
  source_commit: 867cc92d7a96fb6e7444288c6d5d2550b32a8f60
  status: draft
  last_synced: 2026-09-29
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
## Nhảy nhị phân trên cây động

Đây là một phương pháp tìm LCA khác, cũng hỗ trợ thêm một đỉnh lá vào đỉnh `v`.

Phương pháp trước gặp khó khăn với các cập nhật này vì thêm một lá có thể làm thay đổi thời điểm vào và ra của toàn bộ đồ thị.

Ta tạo mảng `depth[u]`, chứa khoảng cách từ đỉnh `u` tới gốc. Có thể tính bằng một lượt DFS trên cây. Tương tự cách trước, ta tiền xử lý mảng `up[u][j]`.

Ta xử lý truy vấn LCA như sau: gọi `(u, v)` là cặp đỉnh cần tìm đáp án. Từ đây giả sử `depth[u] ≥ depth[v]` (nếu `depth[v] > depth[u]`, chỉ cần đổi chỗ `u` và `v`). Ta đưa `u` lên một tổ tiên để đạt `depth[u] = depth[v]`.
Tổ tiên của `u` thỏa điều kiện này nằm cao hơn đúng `depth[u]-depth[v]` đỉnh. Vì vậy, dùng bảng `up[u][j]` và biểu diễn nhị phân của `depth[u]-depth[v]`, ta đổi `u` thành tổ tiên đó.

Bây giờ ta có bài toán tìm LCA của hai đỉnh `(u, v)` có cùng độ sâu. Trước hết xét trường hợp đơn giản `u = v`, khi đó LCA là `u`. Nếu không, ta tìm đỉnh cao nhất chưa phải tổ tiên chung của `(u, v)`.

Giả sử `L=ceil(log(N))`, trong đó `N` là số đỉnh tối đa của đồ thị. Đặt `i = L`. Nếu `up[u][i]=up[v][i]`, chỉ giảm `i`. Ngược lại, đặt `u = up[u][i]` và `v = up[v][i]`, rồi giảm `i`.
Sau tất cả các bước này, ta có hai đỉnh `u` và `v` chưa phải LCA của cặp ban đầu, nhưng `up[u][0]` và `up[v][0]` thì chính là LCA. Độ phức tạp tiền xử lý vẫn là $O(N \log N)$, còn truy vấn là $O( \log N)$.

Vì sao cách này phù hợp với cây động? Trong thuật toán, ta chỉ cần mảng `up[u][j]` cho mọi đỉnh và khoảng cách từ mỗi đỉnh tới gốc; cả hai đều dễ dàng tính được từ truy vấn thêm lá trong $O(\log n)$.

Đổi lại là tốc độ truy vấn. Phương pháp trước xử lý một truy vấn bằng một vòng lặp giảm dần, vì phép kiểm tra tổ tiên đồng thời xử lý chênh lệch độ sâu và vị trí tách nhánh. Phương pháp này cần hai vòng lặp, vòng thứ hai đưa cả hai đỉnh lên trên, nên đọc `up` nhiều hơn khoảng ba lần: trên cây có $10^6$ đỉnh, mỗi truy vấn đọc 64 lần so với 22 lần.

### Cài đặt

```cpp
int n, l;
vector<vector<int>> adj;

vector<int> depth;
vector<vector<int>> up;

void dfs(int v, int p, int dist)
{
    depth[v]=dist;
    up[v][0] = p;
    for (int i = 1; i <= l; ++i)
        up[v][i] = up[up[v][i-1]][i-1];

    for (int u : adj[v]) {
        if (u != p)
            dfs(u, v, dist+1);
    }
}

int lca(int u, int v)
{
    if (depth[u] < depth[v]) swap(u,v);
    for (int j = l; j >= 0; --j) {
        if (depth[up[u][j]] >= depth[v]) {
            u = up[u][j];
        }
    }

    if(u == v) return u;

    for (int i = l; i >= 0; --i) {
        if (up[u][i] != up[v][i]) {
            u = up[u][i];
            v = up[v][i];
        }
    }
    return up[u][0];
}

void add_leaf(int to)
{
    int v = adj.size();
    adj[to].push_back(v);
    adj.push_back({to});
    depth.push_back(depth[to]+1);
    up.push_back(vector<int>(l + 1));
    up[v][0] = to;
    for (int i = 1; i <= l; ++i)
        up[v][i] = up[up[v][i-1]][i-1];
}

//Set max_nodes to the maximum size of the graph
void preprocess(int root, int max_nodes)
{
    depth.resize(n);
    l = ceil(log2(max_nodes));
    up.assign(n, vector<int>(l + 1));
    dfs(root, root, 0);
}
```

## LCA với bộ nhớ và thời gian tiền xử lý $O(n)$

Phương pháp này cho phép tính LCA chỉ dùng bộ nhớ $O(n)$. Ta cũng có thể mở rộng để dùng trên cây động. Phương pháp được Harel và Tarjan đề xuất lần đầu vào năm 1984.

Tạo mảng `depth[]` lưu độ sâu của mỗi đỉnh trong cây.
Với mỗi đỉnh, ta chỉ định nghĩa bước nhảy **nhỏ** và **lớn**. Bước nhảy nhỏ luôn trỏ tới cha trực tiếp (trừ gốc trỏ tới chính nó). Bước nhảy lớn được định nghĩa phức tạp hơn. Ký hiệu `big[v]` là đỉnh đến sau một bước nhảy lớn từ đỉnh `v`. Đặt `big[root] = root`.

Sau đó ta định nghĩa đệ quy. Đặt $\ell(v) = \mathtt{depth}[v] - \mathtt{depth}[\mathtt{big}[v]]$ là độ dài bước nhảy lớn từ $v$, và gọi $p$ là cha của $u$.

$$\mathtt{big}[u] = \begin{cases} \mathtt{big}[\mathtt{big}[p]] & \text{if } \ell(p) = \ell(\mathtt{big}[p]) \\
p & \text{otherwise}\end{cases}$$

<figure style="margin:1.2em auto">
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 26 700 134" width="700" height="134" style="max-width:100%;height:auto" font-family="Georgia,'Times New Roman',serif" role="img" aria-label="Hai bước nhảy lớn bằng nhau từ p và big của p được ghép thành một bước nhảy dài hai ell cộng một cho u">
  <defs>
    <marker id="lcaA" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="#9575cd"/></marker>
    <marker id="lcaB" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="#ec407a"/></marker>
  </defs>
  <g stroke="currentColor" fill="currentColor">
    <line x1="60" y1="100" x2="660" y2="100" stroke-width="2" opacity=".4"/>
    <g stroke="none" opacity=".62"><circle cx="140" cy="100" r="4"/><circle cx="260" cy="100" r="4"/><circle cx="320" cy="100" r="4"/><circle cx="440" cy="100" r="4"/><circle cx="500" cy="100" r="4"/></g>
    <g stroke="none"><circle cx="200" cy="100" r="6.5"/><circle cx="380" cy="100" r="6.5"/><circle cx="560" cy="100" r="6.5"/><circle cx="620" cy="100" r="6.5"/></g>
    <g font-size="16" text-anchor="middle" stroke="none" font-family="ui-monospace,'DejaVu Sans Mono',monospace">
      <text x="200" y="152">big[big[p]]</text><text x="380" y="152">big[p]</text><text x="560" y="152">p</text><text x="620" y="152">u</text>
    </g>
  </g>
  <g fill="none" stroke-width="2.2">
    <path d="M556 110 Q470 162 388 110" stroke="#9575cd" marker-end="url(#lcaA)"/>
    <path d="M376 110 Q290 162 208 110" stroke="#9575cd" marker-end="url(#lcaA)"/>
    <path d="M618 90 Q410 22 206 90" stroke="#ec407a" marker-end="url(#lcaB)"/>
  </g>
  <g font-size="17" font-style="italic" text-anchor="middle">
    <text x="470" y="127" fill="#9575cd">&#8467;</text><text x="290" y="127" fill="#9575cd">&#8467;</text>
    <text x="410" y="46" fill="#ec407a">2&#8467; + 1</text>
  </g>
</svg>
<figcaption>Hai bước nhảy bằng nhau được gộp lại, nên độ dài mỗi bước nhảy bằng một lũy thừa của hai trừ một.</figcaption>
</figure>

Ta phải tính mảng này theo thứ tự sao cho khi xét một đỉnh, giá trị của mọi tổ tiên của nó đã được tính. Có thể dùng thứ tự preorder vì thứ tự này thỏa tính chất đó.

Bây giờ, sau phần tiền xử lý, trả lời truy vấn khá đơn giản. Trước hết ta cân bằng hai đỉnh về cùng độ sâu rồi tìm đỉnh thấp nhất chưa phải tổ tiên chung. Cách này rất giống thuật toán LCA động ở trên, nhưng bây giờ ta chỉ kiểm tra xem có thể thực hiện bước nhảy lớn hay không; nếu không thì thực hiện bước nhảy nhỏ. Độ phức tạp thời gian là logarit, vì Harel và Tarjan đã chứng minh trong bài báo rằng ta dùng nhiều nhất $6\lfloor{\log(d+1)}\rfloor-4$ bước nhảy. Độ phức tạp bộ nhớ là tuyến tính.

<figure style="margin:1.2em auto">
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 12 700 200" width="700" height="200" style="max-width:100%;height:auto" font-family="Georgia,'Times New Roman',serif" role="img" aria-label="Bước nhảy lớn của mỗi đỉnh trên đường đi gồm 17 đỉnh; các độ dài 1, 3, 7 và 15 xen kẽ phía trên và dưới đường đi">
  <g stroke="currentColor" fill="currentColor">
    <line x1="46" y1="134" x2="654" y2="134" stroke-width="2" opacity=".4"/>
    <g stroke="none"><circle cx="46" cy="134" r="4.5"/><circle cx="84" cy="134" r="4.5"/><circle cx="122" cy="134" r="4.5"/><circle cx="160" cy="134" r="4.5"/><circle cx="198" cy="134" r="4.5"/><circle cx="236" cy="134" r="4.5"/><circle cx="274" cy="134" r="4.5"/><circle cx="312" cy="134" r="4.5"/><circle cx="350" cy="134" r="4.5"/><circle cx="388" cy="134" r="4.5"/><circle cx="426" cy="134" r="4.5"/><circle cx="464" cy="134" r="4.5"/><circle cx="502" cy="134" r="4.5"/><circle cx="540" cy="134" r="4.5"/><circle cx="578" cy="134" r="4.5"/><circle cx="616" cy="134" r="4.5"/><circle cx="654" cy="134" r="4.5"/></g>
  </g>
  <g fill="none" stroke="#9575cd" stroke-width="1.8">
    <path d="M46 141 A19 14 0 0 0 84 141"/>
    <path d="M84 141 A19 14 0 0 0 122 141"/>
    <path d="M46 127 A57 34 0 0 1 160 127"/>
    <path d="M160 141 A19 14 0 0 0 198 141"/>
    <path d="M198 141 A19 14 0 0 0 236 141"/>
    <path d="M160 127 A57 34 0 0 1 274 127"/>
    <path d="M46 141 A133 46 0 0 0 312 141"/>
    <path d="M312 141 A19 14 0 0 0 350 141"/>
    <path d="M350 141 A19 14 0 0 0 388 141"/>
    <path d="M312 127 A57 34 0 0 1 426 127"/>
    <path d="M426 141 A19 14 0 0 0 464 141"/>
    <path d="M464 141 A19 14 0 0 0 502 141"/>
    <path d="M426 127 A57 34 0 0 1 540 127"/>
    <path d="M312 141 A133 46 0 0 0 578 141"/>
    <path d="M46 127 A285 92 0 0 1 616 127"/>
    <path d="M616 141 A19 14 0 0 0 654 141"/>
  </g>
  <g fill="#9575cd" font-size="15" font-style="italic" text-anchor="middle"><text x="179" y="205">7</text><text x="483" y="85">3</text><text x="331" y="27">15</text><text x="635" y="173">1</text></g>
</svg>
<figcaption>Các bước nhảy lớn trên một đường đi. Các kích thước lồng nhau, nên chỉ cần ít bước nhảy để đến gốc từ bất kỳ vị trí nào.</figcaption>
</figure>

Thêm một lá ở đây rẻ hơn so với phần trước. Cả hai con trỏ của đỉnh mới đều được xác định chỉ từ cha của nó, và không đỉnh cũ nào thay đổi, nên mỗi lần thêm mất $O(1)$ và không có bảng nào cần mở rộng.

### Cài đặt

```cpp
int n, l;
vector<vector<int>> adj;

vector<int> depth;
vector<int> small, big;

void dfs(int v, int p, int dist)
{
    depth[v] = dist;
    small[v] = p;
    
    if(depth[p] - depth[big[p]] == depth[big[p]] - depth[big[big[p]]]){
        big[v]= big[big[p]];
    }
    else{
        big[v]=p;
    }

    for (int u : adj[v]) {
        if (u != p)
            dfs(u, v, dist+1);
    }
}

int lca(int u, int v)
{
    if (depth[u] < depth[v]) swap(u,v);
    while(depth[u] != depth[v]) {
        if (depth[big[u]] >= depth[v]) {
            u = big[u];
        }
        else{
            u = small[u];
        }
    }

    while(u != v) {
        if (big[u] != big[v]) {
            u = big[u];
            v = big[v];
        }
        else{
            u = small[u];
            v = small[v];
        }
    }
    return u;
}

void add_leaf(int to)
{
    int v = adj.size();
    adj[to].push_back(v);
    adj.push_back({to});
    depth.push_back(depth[to] + 1);
    small.push_back(to);

    if(depth[to] - depth[big[to]] == depth[big[to]] - depth[big[big[to]]]){
        big.push_back(big[big[to]]);
    }
    else{
        big.push_back(to);
    }
}

void preprocess(int root)
{
    depth.resize(n);
    small.resize(n);
    big.resize(n);
    big[root] = root;
    dfs(root, root, 0);
}
```

## Bài tập luyện tập

* [LeetCode -  Kth Ancestor of a Tree Node](https://leetcode.com/problems/kth-ancestor-of-a-tree-node)
* [Codechef - Longest Good Segment](https://www.codechef.com/problems/LGSEG)
* [HackerEarth - Optimal Connectivity](https://www.hackerearth.com/practice/algorithms/graphs/graph-representation/practice-problems/algorithm/optimal-connectivity-c6ae79ca/)