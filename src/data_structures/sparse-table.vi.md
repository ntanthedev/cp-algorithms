---
tags:
  - Original
translation:
  source: data_structures/sparse-table.md
  source_commit: 0a145284a6387b2b0bc4e979615224108fbb3057
  status: draft
  last_synced: 2026-08-07
---

# Sparse Table

Sparse Table là một cấu trúc dữ liệu cho phép trả lời các truy vấn trên đoạn.
Nó có thể trả lời phần lớn truy vấn đoạn trong $O(\log n)$, nhưng điểm mạnh thực sự là truy vấn giá trị nhỏ nhất trên đoạn (hoặc tương đương là truy vấn giá trị lớn nhất trên đoạn).
Với các truy vấn này, đáp án có thể được tính trong $O(1)$ thời gian.

Nhược điểm duy nhất của cấu trúc dữ liệu này là nó chỉ dùng được với các mảng _bất biến_.
Điều đó có nghĩa là mảng không được thay đổi giữa hai truy vấn.
Nếu bất kỳ phần tử nào trong mảng thay đổi, toàn bộ cấu trúc dữ liệu phải được tính lại.

## Trực giác

Mọi số không âm đều có thể được biểu diễn duy nhất thành tổng của các lũy thừa của hai giảm dần.
Đây chỉ là một cách nhìn khác của biểu diễn nhị phân một số.
Ví dụ $13 = (1101)_2 = 8 + 4 + 1$.
Với một số $x$, ta cần nhiều nhất $\lceil \log_2 x \rceil$ số hạng.

Tương tự, mọi đoạn đều có thể được biểu diễn duy nhất thành hợp của các đoạn có độ dài là các lũy thừa của hai giảm dần.
Ví dụ $[2, 14] = [2, 9] \cup [10, 13] \cup [14, 14]$, trong đó đoạn đầy đủ có độ dài 13, còn các đoạn thành phần lần lượt có độ dài 8, 4 và 1.
Ở đây hợp cũng gồm nhiều nhất $\lceil \log_2(\text{length of interval}) \rceil$ đoạn.

Ý tưởng chính của Sparse Table là tính trước đáp án cho mọi truy vấn trên các đoạn có độ dài là lũy thừa của hai.
Sau đó, một truy vấn đoạn khác có thể được trả lời bằng cách tách đoạn thành các đoạn có độ dài là lũy thừa của hai, lấy các đáp án đã tính trước rồi kết hợp chúng để thu được đáp án đầy đủ.

## Tiền xử lý

Ta dùng một mảng hai chiều để lưu đáp án của các truy vấn đã tính trước.
$\text{st}[i][j]$ lưu đáp án cho đoạn $[j, j + 2^i - 1]$ có độ dài $2^i$.
Kích thước mảng hai chiều là $(K + 1) \times \text{MAXN}$, trong đó $\text{MAXN}$ là độ dài mảng lớn nhất có thể có.
$\text{K}$ phải thỏa $\text{K} \ge \lfloor \log_2 \text{MAXN} \rfloor$, vì $2^{\lfloor \log_2 \text{MAXN} \rfloor}$ là độ dài lớn nhất dạng lũy thừa của hai mà ta cần hỗ trợ.
Với các mảng có độ dài hợp lý ($\le 10^7$ phần tử), $K = 25$ là một giá trị phù hợp.

Chiều $\text{MAXN}$ được đặt thứ hai để các lần truy cập bộ nhớ liên tiếp tận dụng cache tốt hơn.

```{.cpp file=sparsetable_definition}
int st[K + 1][MAXN];
```

Vì đoạn $[j, j + 2^i - 1]$ có độ dài $2^i$ được tách gọn thành hai đoạn $[j, j + 2^{i - 1} - 1]$ và $[j + 2^{i - 1}, j + 2^i - 1]$, đều có độ dài $2^{i - 1}$, ta có thể xây dựng bảng hiệu quả bằng quy hoạch động:

```{.cpp file=sparsetable_generation}
std::copy(array.begin(), array.end(), st[0]);

for (int i = 1; i <= K; i++)
    for (int j = 0; j + (1 << i) <= N; j++)
        st[i][j] = f(st[i - 1][j], st[i - 1][j + (1 << (i - 1))]);
```

Hàm $f$ phụ thuộc vào loại truy vấn.
Với truy vấn tổng đoạn, nó tính tổng; với truy vấn giá trị nhỏ nhất trên đoạn, nó tính giá trị nhỏ nhất.

Độ phức tạp thời gian của bước tiền xử lý là $O(\text{N} \log \text{N})$.

## Truy vấn tổng trên đoạn

Với loại truy vấn này, ta muốn tìm tổng của mọi giá trị trên một đoạn.
Vì vậy định nghĩa tự nhiên của hàm $f$ là $f(x, y) = x + y$.
Ta có thể xây dựng cấu trúc dữ liệu như sau:

```{.cpp file=sparsetable_sum_generation}
long long st[K + 1][MAXN];

std::copy(array.begin(), array.end(), st[0]);

for (int i = 1; i <= K; i++)
    for (int j = 0; j + (1 << i) <= N; j++)
        st[i][j] = st[i - 1][j] + st[i - 1][j + (1 << (i - 1))];
```

Để trả lời truy vấn tổng trên đoạn $[L, R]$, ta duyệt mọi lũy thừa của hai, bắt đầu từ lũy thừa lớn nhất.
Ngay khi một lũy thừa của hai $2^i$ không lớn hơn độ dài đoạn ($= R - L + 1$), ta xử lý phần đầu tiên $[L, L + 2^i - 1]$, rồi tiếp tục với đoạn còn lại $[L + 2^i, R]$.

```{.cpp file=sparsetable_sum_query}
long long sum = 0;
for (int i = K; i >= 0; i--) {
    if ((1 << i) <= R - L + 1) {
        sum += st[i][L];
        L += 1 << i;
    }
}
```

Độ phức tạp thời gian của một truy vấn tổng đoạn là $O(K) = O(\log \text{MAXN})$.

## Truy vấn giá trị nhỏ nhất trên đoạn (RMQ)

Đây là loại truy vấn mà Sparse Table phát huy rõ nhất ưu thế.
Khi tìm giá trị nhỏ nhất trên một đoạn, việc một giá trị trong đoạn được xét một lần hay hai lần không ảnh hưởng kết quả.
Vì vậy, thay vì tách một đoạn thành nhiều đoạn, ta có thể chỉ tách nó thành hai đoạn chồng lấn có độ dài là lũy thừa của hai.
Ví dụ, ta có thể tách đoạn $[1, 6]$ thành $[1, 4]$ và $[3, 6]$.
Giá trị nhỏ nhất trên $[1, 6]$ hiển nhiên bằng giá trị nhỏ nhất giữa giá trị nhỏ nhất của $[1, 4]$ và của $[3, 6]$.
Do đó, ta có thể tính giá trị nhỏ nhất trên đoạn $[L, R]$ bằng:

$$\min(\text{st}[i][L], \text{st}[i][R - 2^i + 1]) \quad \text{ where } i = \log_2(R - L + 1)$$

Cách này yêu cầu ta tính nhanh $\log_2(R - L + 1)$.
Ta có thể làm điều đó bằng cách tính trước mọi logarit:

```{.cpp file=sparse_table_log_table}
int lg[MAXN+1];
lg[1] = 0;
for (int i = 2; i <= MAXN; i++)
    lg[i] = lg[i/2] + 1;
```
Ngoài ra, logarit có thể được tính trực tiếp với thời gian và bộ nhớ hằng số:
```c++
// C++20
#include <bit>
int log2_floor(unsigned long i) {
    return std::bit_width(i) - 1;
}

// pre C++20
int log2_floor(unsigned long long i) {
    return i ? __builtin_clzll(1) - __builtin_clzll(i) : -1;
}
```
[Benchmark này](https://quick-bench.com/q/Zghbdj_TEkmw4XG2nqOpD3tsJ8U) cho thấy dùng mảng `lg` chậm hơn do cache miss.

Sau đó ta cần tiền xử lý cấu trúc Sparse Table. Lần này ta định nghĩa $f$ là $f(x, y) = \min(x, y)$.

```{.cpp file=sparse_table_minimum_generation}
int st[K + 1][MAXN];

std::copy(array.begin(), array.end(), st[0]);

for (int i = 1; i <= K; i++)
    for (int j = 0; j + (1 << i) <= N; j++)
        st[i][j] = min(st[i - 1][j], st[i - 1][j + (1 << (i - 1))]);
```

Và giá trị nhỏ nhất trên đoạn $[L, R]$ được tính bằng:

```{.cpp file=sparse_table_minimum_query}
int i = lg[R - L + 1];
int minimum = min(st[i][L], st[i][R - (1 << i) + 1]);
```

Độ phức tạp thời gian của một truy vấn giá trị nhỏ nhất trên đoạn là $O(1)$.

## Các cấu trúc dữ liệu tương tự hỗ trợ nhiều loại truy vấn hơn

Một trong những điểm yếu chính của cách làm $O(1)$ ở phần trước là nó chỉ hỗ trợ truy vấn với các [hàm lũy đẳng](https://en.wikipedia.org/wiki/Idempotence).
Nói cách khác, nó hoạt động rất tốt cho truy vấn giá trị nhỏ nhất trên đoạn, nhưng không thể dùng cách này để trả lời truy vấn tổng trên đoạn.

Có những cấu trúc dữ liệu tương tự có thể xử lý mọi loại hàm có tính kết hợp và trả lời truy vấn đoạn trong $O(1)$.
Một cấu trúc như vậy là [Disjoint Sparse Table](https://discuss.codechef.com/questions/117696/tutorial-disjoint-sparse-table).
Một lựa chọn khác là [Sqrt Tree](sqrt-tree.md).

## Bài tập luyện tập

* [SPOJ - RMQSQ](http://www.spoj.com/problems/RMQSQ/)
* [SPOJ - THRBL](http://www.spoj.com/problems/THRBL/)
* [Codechef - MSTICK](https://www.codechef.com/problems/MSTICK)
* [Codechef - SEAD](https://www.codechef.com/problems/SEAD)
* [Codeforces - CGCDSSQ](http://codeforces.com/contest/475/problem/D)
* [Codeforces - R2D2 and Droid Army](http://codeforces.com/problemset/problem/514/D)
* [Codeforces - Maximum of Maximums of Minimums](http://codeforces.com/problemset/problem/872/B)
* [SPOJ - Miraculous](http://www.spoj.com/problems/TNVFC1M/)
* [DevSkill - Multiplication Interval (archived)](http://web.archive.org/web/20200922003506/https://devskill.com/CodingProblems/ViewProblem/19)
* [Codeforces - Animals and Puzzles](http://codeforces.com/contest/713/problem/D)
* [Codeforces - Trains and Statistics](http://codeforces.com/contest/675/problem/E)
* [SPOJ - Postering](http://www.spoj.com/problems/POSTERIN/)
* [SPOJ - Negative Score](http://www.spoj.com/problems/RPLN/)
* [SPOJ - A Famous City](http://www.spoj.com/problems/CITY2/)
* [SPOJ - Diferencija](http://www.spoj.com/problems/DIFERENC/)
* [Codeforces - Turn off the TV](http://codeforces.com/contest/863/problem/E)
* [Codeforces - Map](http://codeforces.com/contest/15/problem/D)
* [Codeforces - Awards for Contestants](http://codeforces.com/contest/873/problem/E)
* [Codeforces - Longest Regular Bracket Sequence](http://codeforces.com/contest/5/problem/C)
* [CSES - Static Range Minimum Queries](https://cses.fi/problemset/task/1647)
* [Codeforces - Array Stabilization (GCD version)](http://codeforces.com/problemset/problem/1547/F)