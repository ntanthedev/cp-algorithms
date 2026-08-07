---
tags:
  - Translated
e_maxx_link: heavy_light
translation:
  source: graph/hld.md
  source_commit: cb3d94c520c1fadd62e46ecc7d2c71468b1e3e1e
  status: draft
  last_synced: 2026-08-07
---

# Heavy-Light Decomposition

**Heavy-Light Decomposition** (HLD) là một kỹ thuật khá tổng quát, cho phép ta giải hiệu quả nhiều bài toán quy về **truy vấn trên cây**.


## Mô tả

Xét một cây $G$ có $n$ đỉnh và chọn một gốc bất kỳ.

Ý tưởng cốt lõi của phép phân rã này là **chia cây thành nhiều đường đi** sao cho từ bất kỳ đỉnh $v$ nào, ta có thể đi tới gốc bằng cách đi qua nhiều nhất $\log n$ đường đi. Đồng thời, các đường đi này không giao nhau.

Rõ ràng, nếu xây dựng được cách phân rã như vậy cho mọi cây, ta có thể biến một số truy vấn dạng *“tính một đại lượng nào đó trên đường đi từ $a$ tới $b$”* thành nhiều truy vấn dạng *“tính đại lượng đó trên đoạn $[l, r]$ của đường đi thứ $k^{th}$”*.


### Thuật toán xây dựng

Với mỗi đỉnh $v$, ta tính kích thước cây con của nó là $s(v)$, tức số đỉnh trong cây con gốc $v$, tính cả chính $v$.

Tiếp theo, xét tất cả các cạnh nối từ một đỉnh $v$ tới các đỉnh con của nó. Ta gọi một cạnh là **cạnh nặng** (heavy) nếu nó dẫn tới một đỉnh $c$ thỏa mãn:

$$
s(c) \ge \frac{s(v)}{2} \iff \text{edge }(v, c)\text{ is heavy}
$$

Tất cả các cạnh còn lại được gọi là **cạnh nhẹ** (light).

Hiển nhiên, từ một đỉnh chỉ có nhiều nhất một cạnh nặng đi xuống. Nếu không, đỉnh $v$ sẽ có ít nhất hai đỉnh con có kích thước $\ge \frac{s(v)}{2}$, kéo theo kích thước cây con của $v$ phải quá lớn: $s(v) \ge 1 + 2 \frac{s(v)}{2} > s(v)$, mâu thuẫn.

Bây giờ ta phân rã cây thành các đường đi rời nhau. Xét tất cả các đỉnh mà từ đó không có cạnh nặng nào đi xuống. Từ mỗi đỉnh như vậy, ta đi ngược lên cho tới khi gặp gốc của cây hoặc vừa đi qua một cạnh nhẹ. Kết quả là nhiều đường đi gồm không hoặc nhiều cạnh nặng cộng với một cạnh nhẹ. Riêng đường đi có một đầu là gốc sẽ không có cạnh nhẹ. Ta gọi chúng là **đường nặng** (heavy path) — đây chính là các đường đi cần có trong Heavy-Light Decomposition.


### Chứng minh tính đúng đắn

Trước hết, các đường nặng do thuật toán tạo ra là **rời nhau**. Thật vậy, nếu hai đường như vậy có một cạnh chung thì điều đó sẽ dẫn tới việc có hai cạnh nặng đi ra từ cùng một đỉnh, điều không thể xảy ra.

Tiếp theo, ta chứng minh rằng khi đi từ gốc xuống một đỉnh bất kỳ, ta sẽ **đổi đường nặng không quá $\log n$ lần**. Khi đi xuống theo một cạnh nhẹ, kích thước cây con hiện tại giảm còn một nửa hoặc nhỏ hơn:

$$
s(c) < \frac{s(v)}{2} \iff \text{edge }(v, c)\text{ is light}
$$


Do đó, trước khi kích thước cây con giảm xuống còn một, ta chỉ có thể đi qua nhiều nhất $\log n$ cạnh nhẹ.

Vì ta chỉ có thể chuyển từ một đường nặng sang đường nặng khác qua một cạnh nhẹ (mỗi đường nặng, ngoại trừ đường bắt đầu tại gốc, có một cạnh nhẹ), nên trên đường từ gốc tới một đỉnh bất kỳ, số lần đổi đường nặng không vượt quá $\log n$, đúng như yêu cầu.


Hình dưới đây minh họa cách phân rã một cây mẫu. Cạnh nặng được vẽ dày hơn cạnh nhẹ. Các đường nặng được bao bởi đường nét đứt.

<div style="text-align: center;">
  <img src="hld.png" alt="Image of HLD">
</div>


## Các bài toán mẫu

Khi giải bài, đôi lúc sẽ thuận tiện hơn nếu xem Heavy-Light Decomposition là một tập các đường đi **rời nhau theo đỉnh** thay vì rời nhau theo cạnh. Để làm vậy, chỉ cần bỏ cạnh cuối của mỗi đường nặng nếu cạnh đó là cạnh nhẹ. Khi ấy không tính chất nào bị phá vỡ, đồng thời mỗi đỉnh thuộc đúng một đường nặng.

Dưới đây là một số dạng bài điển hình có thể giải bằng Heavy-Light Decomposition.

Riêng bài toán **tổng các giá trị trên một đường đi** đáng được chú ý vì đây là ví dụ có thể giải bằng những kỹ thuật đơn giản hơn.


### Giá trị lớn nhất trên đường đi giữa hai đỉnh

Cho một cây, mỗi đỉnh được gán một giá trị. Có các truy vấn dạng $(a, b)$, trong đó $a$ và $b$ là hai đỉnh của cây; yêu cầu tìm giá trị lớn nhất trên đường đi giữa $a$ và $b$.

Ta xây dựng trước Heavy-Light Decomposition của cây. Trên mỗi đường nặng, ta xây dựng một [Segment Tree](../data_structures/segment_tree.md), nhờ đó có thể tìm đỉnh có giá trị lớn nhất trên một đoạn đã cho của một đường nặng cụ thể trong $\mathcal{O}(\log n)$. Mặc dù số đường nặng trong Heavy-Light Decomposition có thể lên tới $n - 1$, tổng kích thước của tất cả các đường vẫn bị chặn bởi $\mathcal{O}(n)$, do đó tổng kích thước của các Segment Tree cũng là tuyến tính.

Để trả lời truy vấn $(a, b)$, ta tìm [tổ tiên chung gần nhất](https://en.wikipedia.org/wiki/Lowest_common_ancestor) của $a$ và $b$, gọi là $l$, bằng bất kỳ phương pháp phù hợp nào. Khi đó bài toán được tách thành hai truy vấn $(a, l)$ và $(b, l)$. Với mỗi truy vấn con, ta làm như sau: xác định đường nặng chứa đỉnh thấp hơn, thực hiện truy vấn trên đường đó, di chuyển tới đầu trên của đường, tiếp tục xác định đường nặng hiện tại và truy vấn trên nó, cứ như vậy cho tới khi tới đường chứa $l$.

Cần cẩn thận với trường hợp, chẳng hạn, $a$ và $l$ nằm trên cùng một đường nặng: khi đó truy vấn giá trị lớn nhất trên đường này không được thực hiện trên một tiền tố bất kỳ mà phải trên đoạn bên trong nằm giữa $a$ và $l$.

Mỗi truy vấn con $(a, l)$ và $(b, l)$ cần đi qua $\mathcal{O}(\log n)$ đường nặng; trên mỗi đường, ta thực hiện một truy vấn giá trị lớn nhất trên một đoạn, mất thêm $\mathcal{O}(\log n)$ thao tác trên Segment Tree.
Vì vậy, một truy vấn $(a, b)$ mất $\mathcal{O}(\log^2 n)$ thời gian.

Nếu tính trước và lưu giá trị lớn nhất của mọi tiền tố trên mỗi đường nặng, ta có lời giải $\mathcal{O}(\log n)$, bởi mọi truy vấn giá trị lớn nhất đều nằm trên một tiền tố, ngoại trừ nhiều nhất một lần khi ta tới tổ tiên $l$.


###  Tổng các giá trị trên đường đi giữa hai đỉnh

Cho một cây, mỗi đỉnh được gán một giá trị. Có các truy vấn dạng $(a, b)$, trong đó $a$ và $b$ là hai đỉnh; yêu cầu tìm tổng các giá trị trên đường đi giữa $a$ và $b$. Một biến thể khác còn có các thao tác cập nhật làm thay đổi giá trị gán cho một hoặc nhiều đỉnh.

Bài toán này có thể được giải tương tự bài toán giá trị lớn nhất ở trên bằng Heavy-Light Decomposition và các Segment Tree trên đường nặng. Nếu không có cập nhật, ta có thể dùng tổng tiền tố. Tuy nhiên, bài toán này cũng có những cách giải đơn giản hơn.

Nếu không có cập nhật, ta có thể tính tổng trên đường đi giữa hai đỉnh song song với quá trình tìm LCA bằng [nhảy nhị phân](lca_binary_lifting.md) — khi tiền xử lý, ngoài tổ tiên thứ $2^k$ của mỗi đỉnh, ta còn lưu tổng trên đường đi tới các tổ tiên đó.

Có một cách tiếp cận hoàn toàn khác: xét [Euler tour](https://en.wikipedia.org/wiki/Euler_tour_technique) của cây và xây dựng Segment Tree trên đó. Thuật toán này được trình bày trong một [bài về bài toán tương tự](tree_painting.md). Một lần nữa, nếu không có cập nhật thì chỉ cần lưu tổng tiền tố, không cần Segment Tree.

Cả hai phương pháp đều cho lời giải tương đối đơn giản với thời gian $\mathcal{O}(\log n)$ cho mỗi truy vấn.

### Tô lại các cạnh trên đường đi giữa hai đỉnh

Cho một cây, ban đầu mỗi cạnh được tô màu trắng. Có các thao tác cập nhật dạng $(a, b, c)$, trong đó $a$ và $b$ là hai đỉnh còn $c$ là một màu; thao tác yêu cầu tô lại tất cả các cạnh trên đường đi từ $a$ tới $b$ bằng màu $c$. Sau khi thực hiện toàn bộ các lần tô lại, cần báo số cạnh của mỗi màu thu được.

Tương tự các bài toán trên, lời giải là áp dụng Heavy-Light Decomposition và xây dựng một [Segment Tree](../data_structures/segment_tree.md) trên mỗi đường nặng.

Mỗi lần tô lại trên đường $(a, b)$ được tách thành hai cập nhật $(a, l)$ và $(b, l)$, với $l$ là tổ tiên chung gần nhất của $a$ và $b$.   
$\mathcal{O}(\log n)$ cho mỗi đường trên $\mathcal{O}(\log n)$ đường dẫn tới độ phức tạp $\mathcal{O}(\log^2 n)$ cho mỗi lần cập nhật.

## Cài đặt

Một số phần trong cách tiếp cận trên có thể được điều chỉnh để cài đặt dễ hơn mà không làm giảm hiệu quả.

* Định nghĩa **cạnh nặng** có thể đổi thành **cạnh dẫn tới đỉnh con có cây con lớn nhất**, nếu hòa thì chọn tùy ý. Điều này có thể khiến một số cạnh nhẹ trở thành cạnh nặng, nghĩa là một số đường nặng sẽ hợp lại thành một đường duy nhất, nhưng mọi đường nặng vẫn rời nhau. Đồng thời vẫn bảo đảm rằng khi đi xuống một cạnh nhẹ, kích thước cây con giảm còn một nửa hoặc ít hơn.
* Thay vì xây dựng một Segment Tree cho từng đường nặng, ta có thể dùng một Segment Tree duy nhất và cấp cho mỗi đường nặng một đoạn rời nhau trên cây này.
* Như đã nói, trả lời truy vấn cần tính LCA. Ta có thể tính LCA riêng, hoặc tích hợp việc tính LCA ngay trong quá trình trả lời truy vấn.

Để thực hiện Heavy-Light Decomposition:

```cpp
vector<int> parent, depth, heavy, head, pos;
int cur_pos;

int dfs(int v, vector<vector<int>> const& adj) {
    int size = 1;
    int max_c_size = 0;
    for (int c : adj[v]) {
        if (c != parent[v]) {
            parent[c] = v, depth[c] = depth[v] + 1;
            int c_size = dfs(c, adj);
            size += c_size;
            if (c_size > max_c_size)
                max_c_size = c_size, heavy[v] = c;
        }
    }
    return size;
}

void decompose(int v, int h, vector<vector<int>> const& adj) {
    head[v] = h, pos[v] = cur_pos++;
    if (heavy[v] != -1)
        decompose(heavy[v], h, adj);
    for (int c : adj[v]) {
        if (c != parent[v] && c != heavy[v])
            decompose(c, c, adj);
    }
}

void init(vector<vector<int>> const& adj) {
    int n = adj.size();
    parent = vector<int>(n);
    depth = vector<int>(n);
    heavy = vector<int>(n, -1);
    head = vector<int>(n);
    pos = vector<int>(n);
    cur_pos = 0;

    dfs(0, adj);
    decompose(0, 0, adj);
}
```

Danh sách kề của cây phải được truyền vào hàm `init`, và phép phân rã được thực hiện với giả thiết đỉnh `0` là gốc.

Hàm `dfs` được dùng để tính `heavy[v]`, tức đỉnh con nằm ở đầu bên kia của cạnh nặng đi từ `v`, cho mọi đỉnh `v`. Ngoài ra, `dfs` còn lưu cha và độ sâu của từng đỉnh để dùng về sau khi trả lời truy vấn.

Hàm `decompose` gán cho mỗi đỉnh `v` hai giá trị `head[v]` và `pos[v]`, lần lượt là đầu của đường nặng chứa `v` và vị trí của `v` trên Segment Tree duy nhất bao phủ toàn bộ các đỉnh.

Để trả lời truy vấn trên đường đi, chẳng hạn truy vấn giá trị lớn nhất đã nói ở trên, ta có thể làm như sau:

```cpp
int query(int a, int b) {
    int res = 0;
    for (; head[a] != head[b]; b = parent[head[b]]) {
        if (depth[head[a]] > depth[head[b]])
            swap(a, b);
        int cur_heavy_path_max = segment_tree_query(pos[head[b]], pos[b]);
        res = max(res, cur_heavy_path_max);
    }
    if (depth[a] > depth[b])
        swap(a, b);
    int last_heavy_path_max = segment_tree_query(pos[a], pos[b]);
    res = max(res, last_heavy_path_max);
    return res;
}
```

**Ghi chú bản dịch:** Đoạn truy vấn giá trị lớn nhất trong nguồn khởi tạo kết quả bằng 0. Cách này chỉ đúng khi giá trị cần lấy lớn nhất không âm; nếu mọi giá trị trên đường đi đều âm, kết quả 0 là sai. Bản dịch giữ nguyên code nguồn và lỗi này được tách riêng để đề xuất sửa upstream.

## Bài tập luyện tập

- [SPOJ - QTREE - Query on a tree](https://www.spoj.com/problems/QTREE/)
- [CSES - Path Queries II](https://cses.fi/problemset/task/2134)
- [Codeforces - Subway Lines](https://codeforces.com/gym/101908/problem/L)
- [Codeforces - Tree Queries](https://codeforces.com/contest/1254/problem/D)
- [Codeforces - Tree or not Tree](https://codeforces.com/contest/117/problem/E)
- [Codeforces - The Tree](https://codeforces.com/contest/1017/problem/G)
- [Balkan OI 2018 - Min-max tree](https://oj.uz/problem/view/BOI18_minmaxtree)