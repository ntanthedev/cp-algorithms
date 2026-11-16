---
tags:
  - Translated
e_maxx_link: stoer_wagner_mincut
translation:
  source: graph/stoer_wagner_mincut.md
  source_commit: 3c8b2637e4f35912ecd3a1206cb6a2c95bad5edf
  status: draft
  last_synced: 2026-11-16
---

# Lát cắt cực tiểu - Thuật toán Stoer-Wagner

## Phát biểu bài toán

Cho một đồ thị vô hướng có trọng số $G$ gồm $n$ đỉnh và $m$ cạnh. Một lát cắt $C$ là một tập con khác rỗng và thực sự của tập đỉnh (thực chất lát cắt phân hoạch các đỉnh thành hai tập khác rỗng: các đỉnh thuộc $C$ và các đỉnh còn lại). Trọng số của lát cắt là tổng trọng số các cạnh đi qua lát cắt, tức là các cạnh có đúng một đầu mút thuộc $C$:

$$ w(C) = \sum_{\substack{(v,u) \in E \\ u \in C,\ v \not\in C}} c(v,u), $$

trong đó $E$ là tập tất cả các cạnh của đồ thị $G$, còn $c(v,u)$ là trọng số của cạnh $(v,u)$.

Nhiệm vụ là tìm **lát cắt có trọng số nhỏ nhất**.

Đôi khi bài toán này được gọi là "lát cắt cực tiểu toàn cục", để phân biệt với bài toán cho trước một đỉnh nguồn và một đỉnh đích rồi tìm lát cắt cực tiểu $C$ chứa đỉnh đích nhưng không chứa đỉnh nguồn. Lát cắt cực tiểu toàn cục bằng giá trị nhỏ nhất trong các lát cắt chi phí cực tiểu của mọi cặp nguồn-đích có thể.

Mặc dù có thể giải bài toán bằng thuật toán luồng cực đại (chạy $O(n^2)$ lần cho mọi cặp nguồn và đích), dưới đây ta mô tả một thuật toán đơn giản và nhanh hơn nhiều, do Mechthild Stoer và Frank Wagner đề xuất năm 1994.

Nói chung có thể có khuyên và cạnh song song, dù khuyên rõ ràng không ảnh hưởng đến kết quả và các cạnh song song luôn có thể được thay bằng một cạnh với tổng trọng số của chúng. Do đó, để đơn giản, ta giả sử đồ thị đầu vào không có khuyên hoặc cạnh song song.

**Ghi chú bản dịch:** Nguồn không nêu giả thiết trọng số không âm; cần giả thiết này cho thuật toán và chứng minh dưới đây.

## Mô tả thuật toán

**Ý tưởng cơ bản** của thuật toán rất đơn giản. Ta lặp lại quá trình sau: tìm lát cắt cực tiểu giữa một cặp đỉnh $s$ và $t$ nào đó, rồi gộp hai đỉnh này thành một (nối các danh sách kề của chúng). Cuối cùng, sau $n-1$ lần lặp, đồ thị được co lại thành một đỉnh và quá trình dừng. Khi đó, đáp án là giá trị nhỏ nhất trong $n-1$ lát cắt đã tìm. Thật vậy, ở giai đoạn thứ $i$, lát cắt cực tiểu $C_i$ giữa hai đỉnh $s_i$ và $t_i$ hoặc chính là lát cắt cực tiểu toàn cục cần tìm, hoặc việc đặt $s_i$ và $t_i$ vào hai tập khác nhau không có lợi, nên gộp chúng thành một đỉnh không làm kết quả xấu đi.

Như vậy ta đưa bài toán về dạng sau: với đồ thị cho trước, tìm **lát cắt cực tiểu giữa một cặp đỉnh bất kỳ nào đó** $s$ và $t$. Để giải bài toán này, ta dùng quá trình lặp sau. Xét tập đỉnh $A$, ban đầu chỉ chứa một đỉnh tùy ý. Ở mỗi bước, ta tìm đỉnh **liên kết mạnh nhất** với tập $A$, tức đỉnh $v \not\in A$ sao cho đại lượng sau đạt giá trị lớn nhất:

$$ w(v,A) = \sum_{\substack{(v,u) \in E \\ u \in A}} c(v,u) $$

(tức là tổng trọng số các cạnh có một đầu mút là $v$ và đầu còn lại thuộc $A$ đạt giá trị lớn nhất).

Quá trình này cũng dừng sau $n-1$ lần lặp, khi mọi đỉnh đã được đưa vào tập $A$ (quá trình này rất giống [thuật toán Prim](mst_prim.md)). Theo **định lý Stoer-Wagner**, nếu ký hiệu hai đỉnh cuối cùng được thêm vào $A$ là $s$ và $t$, thì một lát cắt cực tiểu giữa hai đỉnh $s$ và $t$ chỉ gồm một đỉnh — $t$. Phần chứng minh định lý này nằm ở mục tiếp theo (như thường thấy, bản thân chứng minh không giúp hiểu thuật toán).

Vậy **sơ đồ tổng quát của thuật toán Stoer-Wagner** như sau. Thuật toán gồm $n-1$ pha. Ở mỗi pha, ban đầu tập $A$ chứa một đỉnh nào đó và các trọng số ban đầu $w(v,A)$ của các đỉnh được tính. Sau đó thực hiện $n-1$ lần lặp: mỗi lần chọn đỉnh $u$ có giá trị $w(v,A)$ lớn nhất và thêm vào $A$, rồi tính lại các giá trị $w$ cho những đỉnh còn lại (hiển nhiên phải duyệt mọi cạnh trong danh sách kề của đỉnh $u$ được chọn). Sau khi thực hiện tất cả các lần lặp, ta lưu hai đỉnh cuối được thêm vào $s$ và $t$; giá trị $w(t,A \setminus t)$ là chi phí của lát cắt cực tiểu vừa tìm giữa $s$ và $t$. Sau đó ta so sánh lát cắt này với đáp án hiện tại; nếu nhỏ hơn thì cập nhật đáp án và chuyển sang pha tiếp theo.

Nếu không dùng cấu trúc dữ liệu phức tạp, phần quan trọng nhất là tìm đỉnh có giá trị $w$ lớn nhất. Nếu thực hiện việc này trong $O(n)$, do có $n-1$ pha và mỗi pha có $n-1$ lần lặp, **độ phức tạp của thuật toán** là $O(n^3)$.

Nếu dùng **heap Fibonacci** để tìm đỉnh có giá trị $w$ lớn nhất (cho phép tăng giá trị khóa trong $O(1)$ khấu hao và lấy phần tử lớn nhất trong $O(\log n)$ khấu hao), mọi thao tác liên quan đến tập $A$ trong một pha có thể thực hiện trong $O(m + n \log n)$. Khi đó độ phức tạp toàn thuật toán là $O(n m + n^2 \log n)$.

## Chứng minh định lý Stoer-Wagner

Nhắc lại phát biểu của định lý. Nếu ta lần lượt thêm mọi đỉnh vào tập $A$, mỗi lần thêm đỉnh liên kết mạnh nhất với tập này, rồi gọi đỉnh áp chót được thêm vào là $s$ và đỉnh cuối cùng là $t$, thì một lát cắt $s$-$t$ cực tiểu chỉ gồm một đỉnh — $t$.

Để chứng minh, xét một lát cắt $s$-$t$ bất kỳ $C$ và chỉ ra rằng trọng số của nó không thể nhỏ hơn trọng số của lát cắt chỉ gồm đỉnh $t$:

$$ w(\{t\}) \le w(C). $$

Ta sẽ chứng minh điều sau. Gọi $A_v$ là trạng thái của tập $A$ ngay trước khi thêm đỉnh $v$. Gọi $C_v$ là lát cắt của tập $A_v \cup \{v\}$ được cảm sinh bởi lát cắt $C$ (nói đơn giản, $C_v$ là giao của hai tập đỉnh này). Một đỉnh $v$ được gọi là tích cực (đối với lát cắt $C$) nếu $v$ và đỉnh được thêm ngay trước nó thuộc hai phía khác nhau của lát cắt $C$. Khi đó, ta khẳng định bất đẳng thức sau đúng với mọi đỉnh tích cực $v$:

$$ w(v,A_v) \le w(C_v). $$

Đặc biệt, $t$ là đỉnh tích cực (vì đỉnh được thêm ngay trước nó là $s$), và với $v = t$ bất đẳng thức này trở thành phát biểu của định lý:

$$ w(t,A_t) = w(\{t\}) \le w(C_t) = w(C). $$

Ta chứng minh bất đẳng thức này bằng quy nạp toán học.

Với đỉnh tích cực đầu tiên $v$, bất đẳng thức đúng (thậm chí là đẳng thức), vì mọi đỉnh trong $A_v$ thuộc cùng một phía của lát cắt còn $v$ thuộc phía kia.

Giả sử bất đẳng thức đúng với mọi đỉnh tích cực cho đến một đỉnh $v$; ta chứng minh nó đúng với đỉnh tích cực tiếp theo $u$. Trước hết, biến đổi vế trái:

$$ w(u,A_u) \equiv w(u,A_v) + w(u,A_u \setminus A_v). $$

Ta có:

$$ w(u,A_v) \le w(v,A_v), $$

vì khi tập $A$ bằng $A_v$, đỉnh được thêm vào chính là $v$ chứ không phải $u$, nghĩa là nó có giá trị $w$ lớn nhất.

Tiếp theo, theo giả thiết quy nạp, $w(v,A_v) \le w(C_v)$ nên:

$$ w(u,A_v) \le w(C_v), $$

từ đó suy ra:

$$ w(u,A_u) \le w(C_v) + w(u,A_u \setminus A_v). $$

Đỉnh $u$ và mọi đỉnh thuộc $A_u \setminus A_v$ nằm ở hai phía khác nhau của lát cắt $C$, nên đại lượng $w(u,A_u \setminus A_v)$ là tổng trọng số các cạnh được tính trong $w(C_u)$ nhưng chưa được tính trong $w(C_v)$. Do đó:

$$ w(u,A_u) \le w(C_v) + w(u,A_u \setminus A_v) \le w(C_u), $$

đúng như cần chứng minh.

Ta đã chứng minh hệ thức $w(v,A_v) \le w(C_v)$ và như đã nêu, toàn bộ định lý suy ra từ hệ thức này.

## Cài đặt

Với cách cài đặt đơn giản và rõ ràng nhất (có độ phức tạp $O(n^3)$), đồ thị được biểu diễn bằng ma trận kề. Đáp án được lưu trong các biến `best_cost` và `best_cut` (chi phí của lát cắt cực tiểu và các đỉnh thuộc lát cắt đó).

Với mỗi đỉnh, mảng `exist` lưu thông tin đỉnh đó còn tồn tại hay đã được gộp vào một đỉnh khác. Danh sách `v[i]` của mỗi đỉnh đã co $i$ lưu các số hiệu đỉnh ban đầu được co vào đỉnh $i$ này.

Thuật toán gồm $n-1$ pha (vòng lặp theo biến `ph`). Trong mỗi pha, ban đầu mọi đỉnh đều ở ngoài tập $A$, nên mảng `in_a` được điền số 0 và độ liên kết $w$ của mọi đỉnh bằng 0. Trong mỗi lần của $n-\mathrm{ph}$ lần lặp, ta tìm đỉnh `sel` có giá trị $w$ lớn nhất. Nếu đây là lần lặp cuối, ta cập nhật đáp án khi cần và gộp hai đỉnh áp chót `prev` và cuối cùng `sel` được chọn. Nếu chưa phải lần lặp cuối, `sel` được thêm vào tập $A$, rồi trọng số của mọi đỉnh còn lại được tính lại.

Lưu ý thuật toán thay đổi đồ thị `g` trong quá trình hoạt động; do đó, nếu cần dùng lại đồ thị sau này, phải lưu một bản sao trước khi gọi hàm.

```{.cpp file=stoer_wagner_mincut}
const int MAXN = 500;
int n;
long long g[MAXN][MAXN];
long long best_cost = (1LL << 62);
vector<int> best_cut;

void mincut() {
    vector<int> v[MAXN];
    for (int i = 0; i < n; ++i)
        v[i].assign(1, i);
    long long w[MAXN];
    bool exist[MAXN], in_a[MAXN];
    memset(exist, true, sizeof exist);
    for (int ph = 0; ph < n - 1; ++ph) {
        memset(in_a, false, sizeof in_a);
        memset(w, 0, sizeof w);
        for (int it = 0, prev; it < n - ph; ++it) {
            int sel = -1;
            for (int i = 0; i < n; ++i)
                if (exist[i] && !in_a[i] && (sel == -1 || w[i] > w[sel]))
                    sel = i;
            if (it == n - ph - 1) {
                if (w[sel] < best_cost) {
                    best_cost = w[sel];
                    best_cut = v[sel];
                }
                v[prev].insert(v[prev].end(), v[sel].begin(), v[sel].end());
                for (int i = 0; i < n; ++i)
                    g[prev][i] = g[i][prev] += g[sel][i];
                exist[sel] = false;
            } else {
                in_a[sel] = true;
                for (int i = 0; i < n; ++i)
                    w[i] += g[sel][i];
                prev = sel;
            }
        }
    }
}
```

## Tài liệu tham khảo

- [Mechthild Stoer, Frank Wagner. A Simple Min-Cut Algorithm. Journal of the ACM, 44(4):585-591, 1997](https://dl.acm.org/doi/10.1145/263867.263872)
- [Kurt Mehlhorn, Christian Uhrig. The minimum cut algorithm of Stoer and Wagner [1995]](https://www.researchgate.net/publication/2483703_The_minimum_cut_algorithm_of_Stoer_and_Wagner)
