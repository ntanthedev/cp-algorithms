---
tags:
  - Translated
e_maxx_link: mst_kruskal
translation:
  source: graph/mst_kruskal.md
  source_commit: 62abfe363065438a459e2fabe63e83fe72882df5
  status: draft
  last_synced: 2026-08-07
---

# Cây khung nhỏ nhất - thuật toán Kruskal

Cho một đồ thị vô hướng có trọng số.
Ta muốn tìm một cây con của đồ thị nối tất cả các đỉnh (tức là một cây khung) và có tổng trọng số nhỏ nhất trong số mọi cây khung có thể có.
Cây khung như vậy được gọi là **cây khung nhỏ nhất** (minimum spanning tree, MST).

Trong hình bên trái là một đồ thị vô hướng có trọng số, còn hình bên phải là cây khung nhỏ nhất tương ứng.

![Đồ thị ngẫu nhiên](MST_before.png) ![Cây khung nhỏ nhất của đồ thị](MST_after.png)

Bài viết này trình bày một số tính chất quan trọng của cây khung nhỏ nhất, sau đó đưa ra cài đặt đơn giản nhất của thuật toán Kruskal để tìm cây khung nhỏ nhất.

## Tính chất của cây khung nhỏ nhất

* Cây khung nhỏ nhất của một đồ thị là duy nhất nếu trọng số của mọi cạnh đều khác nhau. Nếu không, có thể tồn tại nhiều cây khung nhỏ nhất.
  (Một thuật toán cụ thể thường chỉ trả về một trong các cây khung nhỏ nhất có thể có.)
* Cây khung nhỏ nhất cũng là cây có tích trọng số các cạnh nhỏ nhất.
  (Có thể chứng minh dễ dàng bằng cách thay trọng số của mọi cạnh bằng logarit của chúng.)
* Trong một cây khung nhỏ nhất của đồ thị, trọng số lớn nhất của một cạnh là nhỏ nhất có thể khi xét trên mọi cây khung của đồ thị đó.
  (Điều này suy ra từ tính đúng đắn của thuật toán Kruskal.)
* Cây khung lớn nhất (cây khung có tổng trọng số cạnh lớn nhất) có thể được tìm tương tự cây khung nhỏ nhất: đổi dấu trọng số của mọi cạnh rồi áp dụng một thuật toán tìm cây khung nhỏ nhất bất kỳ.

**Ghi chú bản dịch:** Lập luận bằng logarit và mệnh đề về tích trọng số ở trên chỉ áp dụng khi mọi trọng số cạnh đều dương. Với trọng số bằng 0 hoặc âm, logarit không xác định và mệnh đề không còn đúng trong tổng quát. Nguồn tiếng Anh hiện không nêu điều kiện này.

## Thuật toán Kruskal

Thuật toán này được Joseph Bernard Kruskal, Jr. mô tả vào năm 1956.

Ban đầu, thuật toán Kruskal đặt mọi đỉnh của đồ thị gốc tách rời nhau, tạo thành một rừng gồm các cây chỉ có một đỉnh. Sau đó thuật toán dần hợp các cây này lại bằng các cạnh của đồ thị gốc. Trước khi bắt đầu, mọi cạnh được sắp xếp theo trọng số không giảm. Ta lần lượt xét các cạnh theo thứ tự đã sắp xếp; nếu hai đầu của cạnh hiện tại thuộc hai cây con khác nhau, ta hợp hai cây đó và thêm cạnh vào đáp án. Sau khi xét hết các cạnh, mọi đỉnh sẽ thuộc cùng một cây con và ta thu được đáp án.

**Ghi chú bản dịch:** Đoạn mô tả trên giả sử đồ thị liên thông. Nếu đồ thị không liên thông, Kruskal kết thúc với một rừng khung nhỏ nhất (minimum spanning forest), không phải một cây khung nối mọi đỉnh. Nguồn tiếng Anh hiện bỏ qua điều kiện này trong phần mô tả, dù phần chứng minh bên dưới có nêu giả thiết đồ thị ban đầu liên thông.

## Cài đặt đơn giản nhất

Đoạn code sau cài đặt trực tiếp thuật toán đã mô tả và có độ phức tạp thời gian $O(M \log M + N^2)$.
Việc sắp xếp các cạnh cần $O(M \log N)$ phép toán (tương đương $O(M \log M)$).
Thông tin về cây con mà một đỉnh thuộc về được lưu bằng mảng `tree_id[]`: với mỗi đỉnh `v`, `tree_id[v]` lưu số hiệu của cây chứa `v`.
Với mỗi cạnh, ta có thể kiểm tra hai đầu của nó có thuộc hai cây khác nhau hay không trong $O(1)$.
Cuối cùng, việc hợp hai cây được thực hiện trong $O(N)$ bằng một lần duyệt đơn giản qua mảng `tree_id[]`.
Vì tổng số lần hợp là $N-1$, ta thu được độ phức tạp tiệm cận $O(M \log N + N^2)$.

```cpp
struct Edge {
    int u, v, weight;
    bool operator<(Edge const& other) {
        return weight < other.weight;
    }
};

int n;
vector<Edge> edges;

int cost = 0;
vector<int> tree_id(n);
vector<Edge> result;
for (int i = 0; i < n; i++)
    tree_id[i] = i;

sort(edges.begin(), edges.end());
   
for (Edge e : edges) {
    if (tree_id[e.u] != tree_id[e.v]) {
        cost += e.weight;
        result.push_back(e);

        int old_id = tree_id[e.u], new_id = tree_id[e.v];
        for (int i = 0; i < n; i++) {
            if (tree_id[i] == old_id)
                tree_id[i] = new_id;
        }
    }
}
```

## Chứng minh tính đúng đắn

Tại sao thuật toán Kruskal cho kết quả đúng?

Nếu đồ thị ban đầu liên thông thì đồ thị kết quả cũng liên thông.
Nếu không, sẽ tồn tại hai thành phần có thể nối với nhau bằng ít nhất một cạnh. Điều này không thể xảy ra, vì Kruskal hẳn đã chọn một trong các cạnh như vậy khi hai thành phần còn có số hiệu khác nhau.
Đồ thị kết quả cũng không chứa chu trình vì thuật toán đã loại trừ điều đó một cách trực tiếp.
Vì vậy thuật toán tạo ra một cây khung.

Vậy tại sao cây khung đó lại là cây khung nhỏ nhất?

Ta chứng minh bằng quy nạp mệnh đề: "nếu $F$ là tập các cạnh đã được thuật toán chọn ở một thời điểm bất kỳ, thì tồn tại một MST chứa toàn bộ các cạnh của $F$".

Mệnh đề hiển nhiên đúng lúc đầu vì tập rỗng là tập con của mọi MST.

Giả sử ở một bước nào đó $F$ là tập cạnh đã chọn, $T$ là một MST chứa $F$, và $e$ là cạnh mới mà Kruskal đang xét để thêm vào.

Nếu $e$ tạo ra chu trình thì ta không thêm nó, vì vậy mệnh đề vẫn đúng sau bước này.

Nếu $T$ đã chứa $e$, mệnh đề cũng vẫn đúng sau bước này.

Nếu $T$ không chứa cạnh $e$, thì $T + e$ sẽ chứa một chu trình $C$.
Chu trình này chứa ít nhất một cạnh $f$ không thuộc $F$.
Tập cạnh $T - f + e$ cũng là một cây khung.
Lưu ý rằng trọng số của $f$ không thể nhỏ hơn trọng số của $e$, vì nếu vậy Kruskal đã chọn $f$ sớm hơn.
Trọng số của $f$ cũng không thể lớn hơn, vì khi đó tổng trọng số của $T - f + e$ sẽ nhỏ hơn tổng trọng số của $T$, mâu thuẫn với việc $T$ đã là một MST.
Do đó trọng số của $e$ phải bằng trọng số của $f$.
Vì vậy $T - f + e$ cũng là một MST và chứa toàn bộ các cạnh của $F + e$.
Mệnh đề vẫn đúng sau bước này.

Như vậy mệnh đề đã được chứng minh.
Sau khi xét toàn bộ các cạnh, tập cạnh kết quả liên thông và được chứa trong một MST, nên bản thân nó chính là một MST.

## Cài đặt cải tiến

Ta có thể dùng cấu trúc dữ liệu [**Disjoint Set Union** (DSU)](../data_structures/disjoint_set_union.md) để cài đặt Kruskal nhanh hơn, với độ phức tạp khoảng $O(M \log N)$. [Bài viết này](mst_kruskal_with_dsu.md) trình bày chi tiết cách làm đó.

## Bài tập luyện tập

* [SPOJ - Koicost](http://www.spoj.com/problems/KOICOST/)
* [SPOJ - MaryBMW](http://www.spoj.com/problems/MARYBMW/)
* [Codechef - Fullmetal Alchemist](https://www.codechef.com/ICL2016/problems/ICL16A)
* [Codeforces - Edges in MST](http://codeforces.com/contest/160/problem/D)
* [UVA 12176 - Bring Your Own Horse](https://uva.onlinejudge.org/index.php?option=com_onlinejudge&Itemid=8&page=show_problem&problem=3328)
* [UVA 10600 - ACM Contest and Blackout](https://uva.onlinejudge.org/index.php?option=com_onlinejudge&Itemid=8&page=show_problem&problem=1541)
* [UVA 10724 - Road Construction](https://uva.onlinejudge.org/index.php?option=onlinejudge&page=show_problem&problem=1665)
* [Hackerrank - Roads in HackerLand](https://www.hackerrank.com/contests/june-world-codesprint/challenges/johnland/problem)
* [UVA 11710 - Expensive subway](https://uva.onlinejudge.org/index.php?option=com_onlinejudge&Itemid=8&page=show_problem&problem=2757)
* [Codechef - Chefland and Electricity](https://www.codechef.com/problems/CHEFELEC)
* [UVA 10307 - Killing Aliens in Borg Maze](https://uva.onlinejudge.org/index.php?option=com_onlinejudge&Itemid=8&page=show_problem&problem=1248)
* [Codeforces - Flea](http://codeforces.com/problemset/problem/32/C)
* [Codeforces - Igon in Museum](http://codeforces.com/problemset/problem/598/D)
* [Codeforces - Hongcow Builds a Nation](http://codeforces.com/problemset/problem/744/A)
* [UVA - 908 - Re-connecting Computer Sites](https://uva.onlinejudge.org/index.php?option=com_onlinejudge&Itemid=8&page=show_problem&problem=849)
* [UVA 1208 - Oreon](https://uva.onlinejudge.org/index.php?option=com_onlinejudge&Itemid=8&page=show_problem&problem=3649)
* [UVA 1235 - Anti Brute Force Lock](https://uva.onlinejudge.org/index.php?option=com_onlinejudge&Itemid=8&page=show_problem&problem=3676)
* [UVA 10034 - Freckles](https://uva.onlinejudge.org/index.php?option=com_onlinejudge&Itemid=8&page=show_problem&problem=975)
* [UVA 11228 - Transportation system](https://uva.onlinejudge.org/index.php?option=onlinejudge&page=show_problem&problem=2169)
* [UVA 11631 - Dark roads](https://uva.onlinejudge.org/index.php?option=com_onlinejudge&Itemid=8&page=show_problem&problem=2678)
* [UVA 11733 - Airports](https://uva.onlinejudge.org/index.php?option=com_onlinejudge&Itemid=8&page=show_problem&problem=2833)
* [UVA 11747 - Heavy Cycle Edges](https://uva.onlinejudge.org/index.php?option=com_onlinejudge&Itemid=8&page=show_problem&problem=2847)
* [SPOJ - Blinet](http://www.spoj.com/problems/BLINNET/)
* [SPOJ - Help the Old King](http://www.spoj.com/problems/IITKWPCG/)
* [Codeforces - Hierarchy](http://codeforces.com/contest/17/problem/B)
* [SPOJ - Modems](https://www.spoj.com/problems/EC_MODE/)
* [CSES - Road Reparation](https://cses.fi/problemset/task/1675)
* [CSES - Road Construction](https://cses.fi/problemset/task/1676)
