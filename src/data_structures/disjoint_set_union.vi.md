---
tags:
  - Translated
e_maxx_link: dsu
translation:
  source: data_structures/disjoint_set_union.md
  source_commit: bd6b2c210c27f27d6c35571904c236aed4b802a1
  status: draft
  last_synced: 2026-08-07
---

# Hợp các tập rời nhau

Bài viết này trình bày cấu trúc dữ liệu **Disjoint Set Union** hay **DSU** (hợp các tập rời nhau).
Cấu trúc này cũng thường được gọi là **Union Find** theo tên hai thao tác chính của nó.

Cấu trúc dữ liệu này cung cấp các khả năng sau.
Ta có nhiều phần tử, ban đầu mỗi phần tử thuộc một tập riêng biệt.
DSU hỗ trợ thao tác hợp hai tập bất kỳ và cho biết một phần tử cụ thể đang thuộc tập nào.
Phiên bản cổ điển còn có thao tác thứ ba: tạo một tập mới từ một phần tử mới.

Vì vậy giao diện cơ bản của cấu trúc chỉ gồm ba thao tác:

- `make_set(v)` - tạo một tập mới chỉ chứa phần tử `v`
- `union_sets(a, b)` - hợp hai tập được chỉ định (tập chứa phần tử `a` và tập chứa phần tử `b`)
- `find_set(v)` - trả về phần tử đại diện (cũng gọi là leader) của tập chứa phần tử `v`.
Phần tử đại diện là một phần tử thuộc chính tập tương ứng.
Nó được cấu trúc dữ liệu tự chọn cho mỗi tập và có thể thay đổi theo thời gian, cụ thể là sau các lần gọi `union_sets`.
Ta có thể dùng phần tử đại diện để kiểm tra hai phần tử có thuộc cùng một tập hay không.
`a` và `b` thuộc cùng một tập khi và chỉ khi `find_set(a) == find_set(b)`.
Nếu không, chúng thuộc hai tập khác nhau.

Như sẽ trình bày kỹ hơn ở phần sau, cấu trúc dữ liệu cho phép thực hiện mỗi thao tác với thời gian trung bình gần $O(1)$.

Một mục khác cũng trình bày một cách lưu DSU thay thế có độ phức tạp trung bình chậm hơn, $O(\log n)$, nhưng có thể mạnh hơn DSU thông thường trong một số bài toán.

## Xây dựng cấu trúc dữ liệu hiệu quả

Ta lưu các tập dưới dạng **cây**: mỗi cây tương ứng với một tập.
Gốc của cây là phần tử đại diện của tập đó.

Hình dưới minh họa cách biểu diễn các tập bằng cây.

![Ví dụ biểu diễn các tập bằng cây](DSU_example.png)

Ban đầu, mỗi phần tử là một tập riêng nên mỗi đỉnh tự tạo thành một cây.
Sau đó ta hợp tập chứa phần tử 1 với tập chứa phần tử 2.
Tiếp theo hợp tập chứa phần tử 3 với tập chứa phần tử 4.
Cuối cùng hợp tập chứa phần tử 1 với tập chứa phần tử 3.

Trong cài đặt, điều này có nghĩa ta cần duy trì một mảng `parent` lưu tham chiếu đến cha trực tiếp của mỗi đỉnh trong cây.

### Cài đặt ngây thơ

Ta đã có thể viết cài đặt đầu tiên cho cấu trúc Disjoint Set Union.
Ban đầu cài đặt này khá kém hiệu quả, nhưng sau đó ta sẽ cải tiến bằng hai tối ưu để mỗi lần gọi hàm có thời gian gần như hằng số.

Như đã nói, toàn bộ thông tin về các tập phần tử được lưu trong mảng `parent`.

Để tạo một tập mới (thao tác `make_set(v)`), ta chỉ cần tạo một cây có gốc tại đỉnh `v`, nghĩa là chính nó là cha của nó.

Để hợp hai tập (thao tác `union_sets(a, b)`), trước tiên ta tìm phần tử đại diện của tập chứa `a` và phần tử đại diện của tập chứa `b`.
Nếu hai đại diện giống nhau thì không cần làm gì vì hai tập đã được hợp.
Nếu khác nhau, ta chỉ cần đặt một trong hai phần tử đại diện làm cha của phần tử đại diện còn lại, từ đó hợp hai cây.

Cuối cùng là thao tác tìm phần tử đại diện (thao tác `find_set(v)`):
ta lần theo các đỉnh cha của `v` cho đến khi tới gốc, tức một đỉnh có tham chiếu cha trỏ về chính nó.
Thao tác này có thể cài đặt đệ quy rất đơn giản.

```cpp
void make_set(int v) {
    parent[v] = v;
}

int find_set(int v) {
    if (v == parent[v])
        return v;
    return find_set(parent[v]);
}

void union_sets(int a, int b) {
    a = find_set(a);
    b = find_set(b);
    if (a != b)
        parent[b] = a;
}
```

Tuy nhiên cài đặt này không hiệu quả.
Ta dễ dàng xây dựng trường hợp các cây suy biến thành những chuỗi dài.
Khi đó mỗi lần gọi `find_set(v)` có thể mất $O(n)$ thời gian.

Điều này còn rất xa mục tiêu gần như hằng số.
Vì vậy ta sẽ xét hai tối ưu giúp tăng tốc đáng kể.

### Tối ưu nén đường đi

Tối ưu này nhằm tăng tốc `find_set`.

Khi gọi `find_set(v)` cho một đỉnh `v`, thực tế ta tìm được phần tử đại diện `p` cho mọi đỉnh đi qua trên đường từ `v` đến đại diện thật sự `p`.
Ý tưởng là rút ngắn đường đi của tất cả các đỉnh đó bằng cách đặt cha của mỗi đỉnh đã thăm trực tiếp thành `p`.

Hình dưới minh họa thao tác này.
Bên trái là cây ban đầu; bên phải là cây đã được nén sau khi gọi `find_set(7)`, làm ngắn đường đi của các đỉnh 7, 5, 3 và 2.

![Nén đường đi khi gọi find_set(7)](DSU_path_compression.png)

Cài đặt mới của `find_set` như sau:

```cpp
int find_set(int v) {
    if (v == parent[v])
        return v;
    return parent[v] = find_set(parent[v]);
}
```

Cài đặt ngắn gọn này thực hiện đúng ý tưởng:
trước hết tìm phần tử đại diện của tập (đỉnh gốc), rồi trong quá trình tháo ngăn xếp đệ quy, gắn trực tiếp các đỉnh đã thăm vào phần tử đại diện.

Chỉ riêng thay đổi này đã giúp thao tác đạt độ phức tạp trung bình $O(\log n)$ mỗi lần gọi (ở đây không chứng minh).
Ta còn một tối ưu thứ hai để làm cấu trúc nhanh hơn nữa.

### Hợp theo kích thước / hạng
Trong tối ưu này ta thay đổi thao tác `union_set`.
Cụ thể, ta thay đổi việc cây nào sẽ được gắn vào cây nào.
Trong cài đặt ngây thơ, cây thứ hai luôn được gắn vào cây thứ nhất.
Trong thực tế, điều này có thể tạo ra các cây chứa chuỗi dài $O(n)$.
Với tối ưu mới, ta tránh điều đó bằng cách chọn cẩn thận cây nào được gắn vào cây còn lại.

Có nhiều heuristic có thể dùng.
Hai cách phổ biến nhất là:
cách thứ nhất dùng kích thước cây làm hạng; cách thứ hai dùng độ sâu của cây (chính xác hơn là một cận trên của độ sâu, vì độ sâu sẽ giảm khi áp dụng nén đường đi).

Bản chất của cả hai cách giống nhau: gắn cây có hạng nhỏ hơn vào cây có hạng lớn hơn.

Dưới đây là cài đặt hợp theo kích thước:

```cpp
void make_set(int v) {
    parent[v] = v;
    size[v] = 1;
}

void union_sets(int a, int b) {
    a = find_set(a);
    b = find_set(b);
    if (a != b) {
        if (size[a] < size[b])
            swap(a, b);
        parent[b] = a;
        size[a] += size[b];
    }
}
```

Và đây là cài đặt hợp theo hạng dựa trên độ sâu của cây:

```cpp
void make_set(int v) {
    parent[v] = v;
    rank[v] = 0;
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
```
Hai tối ưu tương đương nhau về độ phức tạp thời gian và bộ nhớ, nên trong thực tế có thể dùng bất kỳ cách nào.

### Độ phức tạp thời gian

Như đã nói, nếu kết hợp cả hai tối ưu — nén đường đi với hợp theo kích thước / hạng — ta sẽ đạt thời gian truy vấn gần như hằng số.
Độ phức tạp khấu hao cuối cùng là $O(\alpha(n))$, trong đó $\alpha(n)$ là hàm Ackermann nghịch đảo, tăng cực kỳ chậm.
Thực tế nó tăng chậm đến mức không vượt quá $4$ với mọi $n$ hợp lý (xấp xỉ $n < 10^{600}$).

Độ phức tạp khấu hao là thời gian trên mỗi thao tác khi đánh giá trên cả một chuỗi nhiều thao tác.
Ý tưởng là bảo đảm tổng thời gian của toàn bộ chuỗi, dù một thao tác riêng lẻ có thể chậm hơn đáng kể so với mức khấu hao.
Ví dụ trong trường hợp này, một lần gọi riêng lẻ có thể mất $O(\log n)$ trong trường hợp xấu nhất, nhưng nếu thực hiện liên tiếp $m$ lần gọi thì thời gian trung bình là $O(\alpha(n))$.

Ta không trình bày chứng minh cho độ phức tạp này vì chứng minh khá dài và phức tạp.

Cũng cần lưu ý rằng DSU dùng hợp theo kích thước / hạng nhưng không dùng nén đường đi có thời gian $O(\log n)$ cho mỗi truy vấn.

### Nối theo chỉ số / nối bằng tung đồng xu

Cả hợp theo hạng và hợp theo kích thước đều yêu cầu lưu thêm dữ liệu cho mỗi tập và duy trì dữ liệu đó trong mỗi thao tác hợp.
Ngoài ra còn có một thuật toán ngẫu nhiên giúp đơn giản hóa thao tác hợp đôi chút: nối theo chỉ số.

Ta gán cho mỗi tập một giá trị ngẫu nhiên gọi là chỉ số, rồi gắn tập có chỉ số nhỏ hơn vào tập có chỉ số lớn hơn.
Một tập lớn có xu hướng có chỉ số lớn hơn tập nhỏ, nên cách này có quan hệ gần với hợp theo kích thước.
Có thể chứng minh thao tác này có cùng độ phức tạp như hợp theo kích thước.
Tuy nhiên trong thực tế nó chậm hơn một chút.

Có thể xem chứng minh độ phức tạp và thêm nhiều kỹ thuật hợp khác [tại đây](http://www.cis.upenn.edu/~sanjeev/papers/soda14_disjoint_set_union.pdf).

```cpp
void make_set(int v) {
    parent[v] = v;
    index[v] = rand();
}

void union_sets(int a, int b) {
    a = find_set(a);
    b = find_set(b);
    if (a != b) {
        if (index[a] < index[b])
            swap(a, b);
        parent[b] = a;
    }
}
```

Một hiểu nhầm phổ biến là chỉ cần tung đồng xu để quyết định tập nào gắn vào tập nào thì cũng có cùng độ phức tạp.
Điều này không đúng.
Bài báo được liên kết ở trên phỏng đoán rằng nối bằng tung đồng xu kết hợp nén đường đi có độ phức tạp $\Omega\left(n \frac{\log n}{\log \log n}\right)$.
Trong benchmark, cách này cũng kém hơn đáng kể so với hợp theo kích thước/hạng hoặc nối theo chỉ số.

```cpp
void union_sets(int a, int b) {
    a = find_set(a);
    b = find_set(b);
    if (a != b) {
        if (rand() % 2)
            swap(a, b);
        parent[b] = a;
    }
}
```

## Ứng dụng và các cải tiến khác

Trong phần này ta xét nhiều ứng dụng của cấu trúc dữ liệu, từ các ứng dụng trực tiếp đến một số mở rộng của DSU.

### Thành phần liên thông trong đồ thị

Đây là một trong những ứng dụng rõ ràng nhất của DSU.

Bài toán được phát biểu như sau:
Ban đầu ta có một đồ thị rỗng.
Ta cần thêm các đỉnh và cạnh vô hướng, đồng thời trả lời truy vấn dạng $(a, b)$: "hai đỉnh $a$ và $b$ có nằm trong cùng một thành phần liên thông của đồ thị hay không?"

Có thể áp dụng trực tiếp DSU và thu được lời giải xử lý việc thêm một đỉnh, thêm một cạnh hoặc trả lời một truy vấn trong thời gian trung bình gần như hằng số.

Ứng dụng này rất quan trọng vì gần như cùng một bài toán xuất hiện trong [thuật toán Kruskal để tìm cây khung nhỏ nhất](../graph/mst_kruskal.md).
Dùng DSU, ta có thể [cải tiến](../graph/mst_kruskal_with_dsu.md) độ phức tạp từ $O(m \log n + n^2)$ xuống $O(m \log n)$.

### Tìm thành phần liên thông trong ảnh

Một ứng dụng khác của DSU là bài toán sau:
có một ảnh gồm $n \times m$ pixel.
Ban đầu tất cả đều màu trắng, sau đó một số pixel đen được tô vào.
Ta muốn xác định kích thước của từng thành phần liên thông màu trắng trong ảnh cuối cùng.

Để giải, ta duyệt tất cả pixel trắng; với mỗi ô, duyệt bốn ô kề và nếu ô kề màu trắng thì gọi `union_sets`.
Như vậy ta có một DSU với $n m$ nút tương ứng với các pixel của ảnh.
Các cây thu được trong DSU chính là các thành phần liên thông cần tìm.

Bài toán cũng có thể giải bằng [DFS](../graph/depth-first-search.md) hoặc [BFS](../graph/breadth-first-search.md), nhưng cách DSU có một ưu điểm:
nó có thể xử lý ma trận theo từng hàng (khi xử lý một hàng, chỉ cần hàng trước và hàng hiện tại, đồng thời chỉ cần một DSU cho các phần tử của một hàng), nhờ đó dùng $O(\min(n, m))$ bộ nhớ.

### Lưu thêm thông tin cho mỗi tập

DSU cho phép lưu thêm thông tin trong các tập một cách thuận tiện.

Ví dụ đơn giản là kích thước của tập:
việc lưu kích thước đã được mô tả ở phần hợp theo kích thước, với thông tin được lưu tại phần tử đại diện hiện tại.

Tương tự, bằng cách lưu dữ liệu ở các nút đại diện, ta có thể lưu nhiều loại thông tin khác về từng tập.

### Nén bước nhảy trên đoạn / Tô các đoạn con offline

Một ứng dụng phổ biến khác của DSU là:
ta có một tập đỉnh, mỗi đỉnh có một cạnh đi ra tới một đỉnh khác.
Với DSU, có thể tìm điểm cuối đạt được sau khi liên tục đi theo các cạnh từ một đỉnh bắt đầu cho trước trong thời gian gần như hằng số.

Một ví dụ điển hình là **bài toán tô các đoạn con**.
Ta có một đoạn dài $L$, ban đầu mọi phần tử có màu 0.
Với mỗi truy vấn $(l, r, c)$, ta phải tô lại đoạn con $[l, r]$ bằng màu $c$.
Cuối cùng ta muốn biết màu sau cùng của mỗi ô.
Giả sử ta biết trước toàn bộ truy vấn, tức đây là bài toán offline.

Ta có thể xây một DSU trong đó mỗi ô lưu liên kết tới ô chưa được tô tiếp theo.
Ban đầu mỗi ô trỏ tới chính nó.
Sau khi xử lý một yêu cầu tô đoạn, mọi ô trong đoạn đó sẽ trỏ tới ô ngay sau đoạn.

Để giải bài toán, ta xét các truy vấn **theo thứ tự ngược**: từ cuối về đầu.
Khi đó khi thực hiện một truy vấn, ta chỉ cần tô đúng những ô chưa từng được tô trong đoạn $[l, r]$.
Các ô khác đã chứa màu cuối cùng của chúng.
Để duyệt nhanh các ô chưa tô, ta dùng DSU.
Ta tìm ô chưa tô bên trái nhất trong đoạn, tô nó rồi dùng con trỏ để chuyển sang ô trống tiếp theo bên phải.

Ở đây ta có thể dùng DSU với nén đường đi nhưng không thể dùng hợp theo hạng / kích thước, vì việc phần tử nào trở thành đại diện sau khi hợp là quan trọng.
Do đó độ phức tạp là $O(\log n)$ cho mỗi phép hợp, vẫn đủ nhanh.

Cài đặt:

```cpp
for (int i = 0; i <= L; i++) {
    make_set(i);
}

for (int i = m-1; i >= 0; i--) {
    int l = query[i].l;
    int r = query[i].r;
    int c = query[i].c;
    for (int v = find_set(l); v <= r; v = find_set(v)) {
        answer[v] = c;
        parent[v] = v + 1;
    }
}
```

Có một tối ưu:
ta có thể dùng hợp theo hạng / kích thước nếu lưu ô chưa được tô tiếp theo trong một mảng bổ sung `end[]`.
Khi đó có thể hợp hai tập theo heuristic của chúng và đạt độ phức tạp $O(\alpha(n))$.

### Hỗ trợ khoảng cách tới phần tử đại diện

Trong một số ứng dụng cụ thể của DSU, ta cần duy trì khoảng cách giữa một đỉnh và phần tử đại diện của tập, tức độ dài đường đi trong cây từ nút hiện tại đến gốc.

Nếu không dùng nén đường đi, khoảng cách chỉ là số lần gọi đệ quy.
Nhưng cách này kém hiệu quả.

Ta vẫn có thể dùng nén đường đi nếu lưu **khoảng cách tới cha** làm thông tin bổ sung cho mỗi nút.

Trong cài đặt, thuận tiện nhất là dùng mảng các cặp cho `parent[]`, và hàm `find_set` giờ trả về hai giá trị: phần tử đại diện của tập và khoảng cách tới nó.

```cpp
void make_set(int v) {
    parent[v] = make_pair(v, 0);
    rank[v] = 0;
}

pair<int, int> find_set(int v) {
    if (v != parent[v].first) {
        int len = parent[v].second;
        parent[v] = find_set(parent[v].first);
        parent[v].second += len;
    }
    return parent[v];
}

void union_sets(int a, int b) {
    a = find_set(a).first;
    b = find_set(b).first;
    if (a != b) {
        if (rank[a] < rank[b])
            swap(a, b);
        parent[b] = make_pair(a, 1);
        if (rank[a] == rank[b])
            rank[a]++;
    }
}
```

### Hỗ trợ tính chẵn lẻ của độ dài đường đi / Kiểm tra đồ thị hai phía online

Tương tự việc tính độ dài đường đi tới đại diện, ta có thể duy trì tính chẵn lẻ của độ dài đường đi đó.
Tại sao ứng dụng này cần một mục riêng?

Yêu cầu lưu tính chẵn lẻ xuất hiện trong bài toán sau:
ban đầu ta có một đồ thị rỗng, các cạnh được thêm dần, và ta cần trả lời truy vấn dạng "thành phần liên thông chứa đỉnh này có còn là **đồ thị hai phía** hay không?".

Để giải, ta dùng DSU lưu các thành phần và với mỗi đỉnh lưu tính chẵn lẻ của đường đi tới phần tử đại diện.
Nhờ vậy ta có thể nhanh chóng kiểm tra việc thêm một cạnh có làm mất tính hai phía hay không:
nếu hai đầu cạnh nằm trong cùng thành phần liên thông và có cùng tính chẵn lẻ về độ dài đường đi tới đại diện, việc thêm cạnh sẽ tạo ra một chu trình lẻ và thành phần không còn là đồ thị hai phía.

Khó khăn duy nhất là tính giá trị chẵn lẻ trong phương thức `union_find`.

Nếu thêm cạnh $(a, b)$ nối hai thành phần liên thông, khi gắn một cây vào cây kia ta phải điều chỉnh tính chẵn lẻ.

Ta suy ra công thức tính tính chẵn lẻ cần gán cho đại diện của tập sẽ được gắn vào tập kia.
Gọi $x$ là tính chẵn lẻ của độ dài đường đi từ đỉnh $a$ tới đại diện $A$, $y$ là tính chẵn lẻ từ đỉnh $b$ tới đại diện $B$, và $t$ là giá trị cần gán cho $B$ sau khi hợp.
Đường đi gồm ba phần:
từ $B$ tới $b$, từ $b$ tới $a$ qua đúng một cạnh nên có parity $1$, và từ $a$ tới $A$.
Do đó ta có công thức ($\oplus$ là phép XOR):

$$t = x \oplus y \oplus 1$$

Như vậy, dù thực hiện bao nhiêu lần hợp, tính chẵn lẻ của các cạnh vẫn được truyền từ đại diện này sang đại diện khác.

Dưới đây là cài đặt DSU hỗ trợ parity. Như phần trước, ta dùng một cặp để lưu đỉnh cha và parity. Ngoài ra, với mỗi tập ta lưu trong mảng `bipartite[]` xem tập đó còn hai phía hay không.

```cpp
void make_set(int v) {
    parent[v] = make_pair(v, 0);
    rank[v] = 0;
    bipartite[v] = true;
}

pair<int, int> find_set(int v) {
    if (v != parent[v].first) {
        int parity = parent[v].second;
        parent[v] = find_set(parent[v].first);
        parent[v].second ^= parity;
    }
    return parent[v];
}

void add_edge(int a, int b) {
    pair<int, int> pa = find_set(a);
    a = pa.first;
    int x = pa.second;

    pair<int, int> pb = find_set(b);
    b = pb.first;
    int y = pb.second;

    if (a == b) {
        if (x == y)
            bipartite[a] = false;
    } else {
        if (rank[a] < rank[b])
            swap (a, b);
        parent[b] = make_pair(a, x^y^1);
        bipartite[a] &= bipartite[b];
        if (rank[a] == rank[b])
            ++rank[a];
    }
}

bool is_bipartite(int v) {
    return bipartite[find_set(v).first];
}
```

### RMQ offline (truy vấn giá trị nhỏ nhất trên đoạn) trong $O(\alpha(n))$ trung bình / mẹo Arpa { #arpa data-toc-label="Offline RMQ / Arpa's trick"}

Ta có một mảng `a[]` và cần tính giá trị nhỏ nhất trên một số đoạn đã cho của mảng.

Ý tưởng giải bằng DSU như sau:
ta duyệt mảng và khi đang ở phần tử thứ `i`, ta trả lời tất cả truy vấn `(L, R)` có `R == i`.
Để làm hiệu quả, ta duy trì một DSU trên `i` phần tử đầu với cấu trúc: cha của một phần tử là phần tử nhỏ hơn kế tiếp ở bên phải nó.
Khi đó đáp án cho truy vấn là `a[find_set(L)]`, tức số nhỏ nhất ở bên phải `L`.

Cách này hiển nhiên chỉ hoạt động offline, nghĩa là ta biết trước mọi truy vấn.

Dễ thấy có thể áp dụng nén đường đi.
Ta cũng có thể dùng hợp theo hạng nếu lưu đại diện thực sự trong một mảng riêng.

```cpp
struct Query {
    int L, R, idx;
};

vector<int> answer;
vector<vector<Query>> container;
```

`container[i]` chứa mọi truy vấn có `R == i`.

```cpp
stack<int> s;
for (int i = 0; i < n; i++) {
    while (!s.empty() && a[s.top()] > a[i]) {
        parent[s.top()] = i;
        s.pop();
    }
    s.push(i);
    for (Query q : container[i]) {
        answer[q.idx] = a[find_set(q.L)];
    }
}
```

Ngày nay thuật toán này được biết đến với tên mẹo Arpa.
Nó được đặt theo tên AmirReza Poorakhavan, người đã độc lập phát hiện và phổ biến kỹ thuật này.
Tuy nhiên thuật toán đã tồn tại từ trước phát hiện của anh ấy.

### LCA offline (tổ tiên chung gần nhất trong cây) trong $O(\alpha(n))$ trung bình {data-toc-label="Offline LCA"}

Thuật toán tìm LCA được trình bày trong bài [Lowest Common Ancestor - Tarjan's off-line algorithm](../graph/lca_tarjan.md).
Thuật toán này có ưu điểm so với nhiều thuật toán LCA khác ở tính đơn giản, đặc biệt khi so với một thuật toán tối ưu như [Farach-Colton and Bender](../graph/lca_farachcoltonbender.md).

### Lưu DSU tường minh bằng danh sách tập / Ứng dụng khi hợp nhiều cấu trúc dữ liệu

Một cách lưu DSU khác là giữ mỗi tập dưới dạng **danh sách tường minh các phần tử của nó**.
Đồng thời mỗi phần tử cũng lưu tham chiếu tới đại diện của tập mình.

Thoạt nhìn đây có vẻ là một cấu trúc dữ liệu kém hiệu quả:
khi hợp hai tập, ta phải nối một danh sách vào cuối danh sách kia và cập nhật đại diện cho mọi phần tử của một trong hai danh sách.

Tuy nhiên, dùng một **heuristic theo trọng số** tương tự hợp theo kích thước có thể giảm đáng kể độ phức tạp tiệm cận:
$O(m + n \log n)$ cho $m$ truy vấn trên $n$ phần tử.

Heuristic ở đây là luôn **thêm tập nhỏ hơn vào tập lớn hơn**.
Việc thêm một tập vào tập kia dễ cài đặt trong `union_sets` và mất thời gian tỉ lệ với kích thước tập được thêm.
Còn việc tìm đại diện trong `find_set` mất $O(1)$ với cách lưu này.

Ta chứng minh **độ phức tạp thời gian** $O(m + n \log n)$ cho $m$ truy vấn.
Cố định một phần tử bất kỳ $x$ và đếm số lần nó bị tác động trong thao tác hợp `union_sets`.
Lần đầu $x$ bị tác động, kích thước tập mới ít nhất là $2$.
Lần thứ hai, kích thước tập kết quả ít nhất là $4$, vì tập nhỏ hơn luôn được thêm vào tập lớn hơn.
Và cứ tiếp tục như vậy.
Do đó $x$ chỉ có thể bị di chuyển trong tối đa $\log n$ thao tác hợp.
Cộng trên tất cả các đỉnh ta được $O(n \log n)$, cộng thêm $O(1)$ cho mỗi truy vấn.

Cài đặt:

```cpp
vector<int> lst[MAXN];
int parent[MAXN];

void make_set(int v) {
    lst[v] = vector<int>(1, v);
    parent[v] = v;
}

int find_set(int v) {
    return parent[v];
}

void union_sets(int a, int b) {
    a = find_set(a);
    b = find_set(b);
    if (a != b) {
        if (lst[a].size() < lst[b].size())
            swap(a, b);
        while (!lst[b].empty()) {
            int v = lst[b].back();
            lst[b].pop_back();
            parent[v] = a;
            lst[a].push_back (v);
        }
    }
}
```

Ý tưởng thêm phần nhỏ hơn vào phần lớn hơn còn có thể dùng trong nhiều lời giải không liên quan trực tiếp đến DSU.

Ví dụ xét **bài toán** sau:
ta có một cây, mỗi lá được gán một số (cùng một số có thể xuất hiện ở nhiều lá khác nhau).
Ta muốn tính số lượng giá trị khác nhau trong cây con của mỗi nút.

Áp dụng cùng ý tưởng, có thể xây dựng lời giải như sau:
ta cài đặt một [DFS](../graph/depth-first-search.md) trả về con trỏ tới một tập số nguyên — danh sách các số trong cây con đó.
Để tính đáp án cho nút hiện tại (trừ khi nó là lá), gọi DFS cho tất cả các con rồi hợp các tập nhận được.
Kích thước của tập kết quả chính là đáp án cho nút hiện tại.
Để hợp nhiều tập hiệu quả, ta chỉ cần áp dụng nguyên tắc trên: thêm các tập nhỏ hơn vào tập lớn hơn.
Cuối cùng thu được lời giải $O(n \log^2 n)$ vì mỗi số chỉ được thêm vào một tập tối đa $O(\log n)$ lần.

### Lưu DSU đồng thời duy trì cấu trúc cây rõ ràng / Tìm cầu online trong $O(\alpha(n))$ trung bình  {data-toc-label="Storing the DSU by maintaining a clear tree structure / Online bridge finding"}

Một trong những ứng dụng mạnh nhất của DSU là cho phép lưu đồng thời cây ở dạng **đã nén và chưa nén**.
Dạng nén dùng để hợp cây và kiểm tra hai đỉnh có thuộc cùng một cây hay không; dạng chưa nén có thể dùng, chẳng hạn, để tìm đường giữa hai đỉnh hoặc thực hiện các phép duyệt khác trên cấu trúc cây.

Trong cài đặt, ngoài mảng cha đã nén `parent[]`, ta cần giữ thêm mảng cha chưa nén `real_parent[]`.
Rõ ràng việc duy trì mảng bổ sung này không làm xấu độ phức tạp:
nó chỉ thay đổi khi hợp hai cây và mỗi lần chỉ thay đổi một phần tử.

Mặt khác, trong thực tế ta thường cần nối hai cây bằng một cạnh được chỉ định thay vì nối trực tiếp hai gốc.
Khi đó ta không còn lựa chọn nào khác ngoài việc đổi gốc của một trong hai cây, đưa một đầu của cạnh thành gốc mới.

Thoạt nhìn việc đổi gốc có vẻ rất tốn kém và sẽ làm xấu đáng kể độ phức tạp.
Đúng là để đặt gốc cây tại đỉnh $v$, ta phải đi từ đỉnh này tới gốc cũ và đảo hướng trong `parent[]` và `real_parent[]` cho mọi nút trên đường đi.

Tuy nhiên thực tế không quá tệ: tương tự các ý tưởng ở phần trước, chỉ cần đổi gốc cây nhỏ hơn trong hai cây thì đạt $O(\log n)$ trung bình.

Chi tiết hơn, bao gồm chứng minh độ phức tạp, có trong bài [Finding Bridges Online](../graph/bridge-searching-online.md).

## Lược sử

Cấu trúc dữ liệu DSU đã được biết đến từ lâu.

Cách lưu cấu trúc dưới dạng **một rừng cây** dường như lần đầu được Galler và Fisher mô tả vào năm 1964 (Galler, Fisher, "An Improved Equivalence Algorithm), nhưng phân tích đầy đủ về độ phức tạp xuất hiện muộn hơn nhiều.

Hai tối ưu nén đường đi và hợp theo hạng được McIlroy và Morris phát triển, đồng thời Tritter cũng độc lập phát triển chúng.

Hopcroft và Ullman chứng minh vào năm 1973 độ phức tạp $O(\log^\star n)$ (Hopcroft, Ullman "Set-merging algorithms") — ở đây $\log^\star$ là **logarit lặp**, một hàm tăng chậm nhưng vẫn nhanh hơn hàm Ackermann nghịch đảo.

Lần đầu cận $O(\alpha(n))$ được chứng minh là vào năm 1975 (Tarjan, "Efficiency of a Good But Not Linear Set Union Algorithm").
Sau đó vào năm 1985, Tarjan cùng Leeuwen công bố nhiều phân tích độ phức tạp cho các heuristic hạng khác nhau và nhiều cách nén đường đi (Tarjan, Leeuwen, "Worst-case Analysis of Set Union Algorithms").

Cuối cùng, năm 1989 Fredman và Sachs chứng minh rằng trong mô hình tính toán được xét, **mọi** thuật toán cho bài toán hợp các tập rời nhau đều phải mất ít nhất $O(\alpha(n))$ thời gian trung bình (Fredman, Saks, "The cell probe complexity of dynamic data structures").

## Bài tập

* [TIMUS - Anansi's Cobweb](http://acm.timus.ru/problem.aspx?space=1&num=1671)
* [Codeforces - Roads not only in Berland](http://codeforces.com/contest/25/problem/D)
* [TIMUS - Parity](http://acm.timus.ru/problem.aspx?space=1&num=1003)
* [SPOJ - Strange Food Chain](http://www.spoj.com/problems/CHAIN/)
* [SPOJ - COLORFUL ARRAY](https://www.spoj.com/problems/CLFLARR/)
* [SPOJ - Consecutive Letters](https://www.spoj.com/problems/CONSEC/)
* [Toph - Unbelievable Array](https://toph.co/p/unbelievable-array)
* [HackerEarth - Lexicographically minimal string](https://www.hackerearth.com/practice/data-structures/disjoint-data-strutures/basics-of-disjoint-data-structures/practice-problems/algorithm/lexicographically-minimal-string-6edc1406/description/)
* [HackerEarth - Fight in Ninja World](https://www.hackerearth.com/practice/algorithms/graphs/breadth-first-search/practice-problems/algorithm/containers-of-choclates-1/)
