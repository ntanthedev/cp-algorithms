---
tags:
    - Original
translation:
  source: num_methods/binary_search.md
  source_commit: 3fe157184f03f5fe076455209eb1b912c06e1400
  status: draft
  last_synced: 2026-08-06
---

# Tìm kiếm nhị phân

**Tìm kiếm nhị phân** (binary search) là phương pháp tìm kiếm nhanh hơn bằng cách liên tục chia đôi khoảng tìm kiếm. Ứng dụng quen thuộc nhất của nó là tìm một giá trị trong mảng đã sắp xếp, nhưng tư tưởng chia đôi này còn xuất hiện trong rất nhiều bài toán khác.

## Tìm kiếm trong mảng đã sắp xếp

Bài toán điển hình nhất dẫn đến tìm kiếm nhị phân như sau: cho một mảng đã sắp xếp $A_0 \leq A_1 \leq \dots \leq A_{n-1}$, hãy kiểm tra xem $k$ có xuất hiện trong dãy hay không. Cách đơn giản nhất là duyệt lần lượt từng phần tử và so sánh với $k$, tức tìm kiếm tuyến tính. Cách này chạy trong $O(n)$ nhưng chưa tận dụng tính chất mảng đã được sắp xếp.

<center>
<img src="https://upload.wikimedia.org/wikipedia/commons/8/83/Binary_Search_Depiction.svg" width="800px">
<br>
<i>Tìm kiếm nhị phân giá trị $7$ trong một mảng</i>.
<br>
<i><a href="https://commons.wikimedia.org/wiki/File:Binary_Search_Depiction.svg">Hình ảnh</a> của <a href="https://commons.wikimedia.org/wiki/User:AlwaysAngry">AlwaysAngry</a> được phát hành theo giấy phép <a href="https://creativecommons.org/licenses/by-sa/4.0/deed.en">CC BY-SA 4.0</a></i>.
</center>

Giả sử ta biết hai chỉ số $L < R$ sao cho $A_L \leq k \leq A_R$. Vì mảng đã sắp xếp, ta suy ra rằng $k$ hoặc nằm trong các phần tử $A_L, A_{L+1}, \dots, A_R$, hoặc không xuất hiện trong mảng. Chọn một chỉ số $M$ bất kỳ thỏa mãn $L < M < R$ rồi so sánh $k$ với $A_M$. Có hai trường hợp:

1. $A_L \leq k \leq A_M$. Khi đó ta thu hẹp bài toán từ $[L, R]$ xuống $[L, M]$;
1. $A_M \leq k \leq A_R$. Khi đó ta thu hẹp bài toán từ $[L, R]$ xuống $[M, R]$.

Khi không thể chọn thêm $M$, tức là $R = L + 1$, ta so sánh trực tiếp $k$ với $A_L$ và $A_R$. Nếu chưa đến trạng thái này, ta muốn chọn $M$ sao cho trong trường hợp xấu nhất, đoạn đang xét giảm về một phần tử nhanh nhất có thể.

Trong trường hợp xấu nhất, ta luôn phải đi vào đoạn lớn hơn giữa $[L, M]$ và $[M, R]$. Do đó độ dài đoạn giảm từ $R-L$ xuống $\max(M-L, R-M)$. Để giá trị này nhỏ nhất, ta nên chọn $M \approx \frac{L+R}{2}$, khi đó

$$
M-L \approx \frac{R-L}{2} \approx R-M.
$$

Nói cách khác, xét theo trường hợp xấu nhất, lựa chọn tối ưu là luôn lấy $M$ ở giữa $[L, R]$ và chia đôi đoạn. Sau mỗi bước, độ dài đoạn đang xét giảm một nửa cho đến khi chỉ còn kích thước $1$. Nếu quá trình cần $h$ bước, hiệu giữa $R$ và $L$ giảm từ $R-L$ xuống $\frac{R-L}{2^h} \approx 1$, từ đó có phương trình $2^h \approx R-L$.

Lấy $\log_2$ hai vế, ta được $h \approx \log_2(R-L) \in O(\log n)$.

Số bước logarit tốt hơn rất nhiều so với tìm kiếm tuyến tính. Chẳng hạn, với $n \approx 2^{20} \approx 10^6$, tìm kiếm tuyến tính có thể cần khoảng một triệu phép toán, trong khi tìm kiếm nhị phân chỉ cần khoảng $20$ bước.

### Cận dưới và cận trên

Trong nhiều bài toán, thay vì tìm chính xác vị trí của $k$, ta cần tìm vị trí đầu tiên có giá trị lớn hơn hoặc bằng $k$, gọi là cận dưới (lower bound), hoặc vị trí đầu tiên có giá trị lớn hơn $k$, gọi là cận trên (upper bound).

Cận dưới và cận trên tạo thành một nửa khoảng, có thể rỗng, chứa toàn bộ phần tử bằng $k$. Để kiểm tra $k$ có xuất hiện hay không, chỉ cần tìm cận dưới của nó rồi kiểm tra phần tử tại vị trí đó có bằng $k$ không.

### Cài đặt

Phần giải thích trên mới mô tả ý tưởng tổng quát. Khi cài đặt, ta cần phát biểu chính xác hơn.

Ta duy trì một cặp $L < R$ sao cho $A_L \leq k < A_R$. Nghĩa là khoảng tìm kiếm đang xét là đoạn nửa mở $[L, R)$. Dùng đoạn nửa mở thay vì đoạn đóng $[L, R]$ giúp giảm số trường hợp biên cần xử lý.

Khi $R = L+1$, từ định nghĩa trên ta suy ra $R$ là cận trên của $k$. Ta có thể khởi tạo $R$ bằng chỉ số ngay sau phần tử cuối, tức $R=n$, và $L$ bằng chỉ số ngay trước phần tử đầu, tức $L=-1$. Điều này an toàn miễn là thuật toán không truy cập trực tiếp $A_L$ hoặc $A_R$; về mặt hình thức, ta xem $A_L = -\infty$ và $A_R = +\infty$.

Cuối cùng, để xác định cụ thể $M$, ta chọn $M = \lfloor \frac{L+R}{2} \rfloor$.

Khi đó, cài đặt có thể viết như sau:

```cpp
... // a sorted array is stored as a[0], a[1], ..., a[n-1]
int l = -1, r = n;
while (r - l > 1) {
    int m = (l + r) / 2;
    if (k < a[m]) {
        r = m; // a[l] <= k < a[m] <= a[r]
    } else {
        l = m; // a[l] <= a[m] <= k < a[r]
    }
}
```

Trong suốt quá trình chạy, ta không bao giờ truy cập $A_L$ hay $A_R$, vì luôn có $L < M < R$. Khi kết thúc, $L$ là chỉ số của phần tử cuối cùng không lớn hơn $k$, hoặc bằng $-1$ nếu không tồn tại phần tử như vậy; còn $R$ là chỉ số của phần tử đầu tiên lớn hơn $k$, hoặc bằng $n$ nếu không tồn tại.

**Lưu ý.** Tính `m` bằng `m = (r + l) / 2` có thể gây tràn số nếu `l` và `r` là hai số nguyên dương. Lỗi này từng tồn tại khoảng 9 năm trong JDK, như được mô tả trong [bài viết](https://ai.googleblog.com/2006/06/extra-extra-read-all-about-it-nearly.html). Một cách khác là dùng `m = l + (r - l) / 2`, luôn đúng khi `l` và `r` là số nguyên dương, nhưng vẫn có thể tràn nếu `l` âm. Từ C++20, có thể dùng `m = std::midpoint(l, r)`, cách này luôn tính đúng.

## Tìm kiếm trên một vị từ bất kỳ

Cho $f : \{0,1,\dots, n-1\} \to \{0, 1\}$ là một hàm Boolean xác định trên $0,1,\dots,n-1$ và tăng đơn điệu, tức là

$$
f(0) \leq f(1) \leq \dots \leq f(n-1).
$$

Cách tìm kiếm nhị phân ở trên thực chất tìm điểm phân chia của mảng theo vị từ $f(M)$, trong đó $f(M)$ biểu diễn giá trị Boolean của điều kiện $k < A_M$.
Ta có thể thay điều kiện $k < A_M$ bằng một vị từ tăng đơn điệu bất kỳ. Điều này đặc biệt hữu ích khi việc tính $f(k)$ đủ tốn thời gian khiến ta không thể thử mọi giá trị.
Nói cách khác, tìm kiếm nhị phân tìm chỉ số duy nhất $L$ sao cho $f(L) = 0$ và $f(R)=f(L+1)=1$ nếu tồn tại một điểm chuyển như vậy. Nếu $f(0) = \dots = f(n-1) = 0$, thuật toán cho $L = n-1$; còn nếu $f(0) = \dots = f(n-1) = 1$, thuật toán cho $L = -1$.

Chứng minh tính đúng đắn khi điểm chuyển tồn tại, tức $f(0)=0$ và $f(n-1)=1$: cài đặt duy trì bất biến vòng lặp $f(l)=0, f(r)=1$. Khi $r-l>1$, cách chọn $m$ bảo đảm $r-l$ luôn giảm. Vòng lặp dừng khi $r-l=1$, và ta thu được đúng điểm chuyển cần tìm.

```cpp
... // f(i) is a boolean function such that f(0) <= ... <= f(n-1)
int l = -1, r = n;
while (r - l > 1) {
    int m = (l + r) / 2;
    if (f(m)) {
        r = m; // 0 = f(l) < f(m) = 1
    } else {
        l = m; // 0 = f(m) < f(r) = 1
    }
}
```

### Tìm kiếm nhị phân trên đáp án

Dạng bài này thường xuất hiện khi ta cần tính một giá trị, nhưng chỉ có thể kiểm tra liệu giá trị đó có ít nhất bằng $i$ hay không. Chẳng hạn, cho mảng $a_1,\dots,a_n$ và cần tìm giá trị lớn nhất của phần nguyên trung bình

$$
\left \lfloor \frac{a_l + a_{l+1} + \dots + a_r}{r-l+1} \right\rfloor
$$

trên mọi cặp $l,r$ thỏa mãn $r-l \geq x$. Một cách giải là kiểm tra xem đáp án có ít nhất bằng $\lambda$ hay không, tức liệu có cặp $l,r$ sao cho

$$
\frac{a_l + a_{l+1} + \dots + a_r}{r-l+1} \geq \lambda.
$$

Biến đổi tương đương, ta được

$$
(a_l - \lambda) + (a_{l+1} - \lambda) + \dots + (a_r - \lambda) \geq 0,
$$

vì vậy bài toán trở thành kiểm tra xem trong mảng mới $a_i-\lambda$ có đoạn con độ dài ít nhất $x+1$ và tổng không âm hay không. Điều này có thể thực hiện bằng tổng tiền tố.

## Tìm kiếm liên tục

Cho $f : \mathbb R \to \mathbb R$ là một hàm thực liên tục trên đoạn $[L, R]$.

Không mất tính tổng quát, giả sử $f(L) \leq f(R)$. Theo [định lý giá trị trung gian](https://en.wikipedia.org/wiki/Intermediate_value_theorem), với mọi $y \in [f(L), f(R)]$, tồn tại $x \in [L, R]$ sao cho $f(x) = y$. Khác với các phần trước, ở đây hàm không bắt buộc phải đơn điệu.

Với một $\delta$ cho trước, giá trị $x$ có thể được xấp xỉ với sai số $\pm\delta$ trong thời gian $O\left(\log \frac{R-L}{\delta}\right)$. Ý tưởng vẫn tương tự: chọn $M \in (L,R)$ rồi thu hẹp khoảng về $[L,M]$ hoặc $[M,R]$ tùy theo $f(M)$ lớn hơn hay nhỏ hơn $y$. Một ví dụ quen thuộc là tìm nghiệm của đa thức bậc lẻ.

Chẳng hạn, xét $f(x)=x^3 + ax^2 + bx + c$. Khi $L \to -\infty$ và $R \to +\infty$, ta có $f(L) \to -\infty$ và $f(R) \to +\infty$. Vì vậy luôn có thể chọn $L$ đủ nhỏ và $R$ đủ lớn để $f(L)<0$ và $f(R)>0$. Sau đó, tìm kiếm nhị phân có thể tìm một khoảng nhỏ tùy ý chứa nghiệm $x$ sao cho $f(x)=0$.

## Tìm kiếm theo lũy thừa của 2

Một cách đáng chú ý khác là không duy trì đoạn đang xét, mà duy trì con trỏ hiện tại $i$ và số mũ hiện tại $k$. Ban đầu $i=L$. Ở mỗi bước, ta kiểm tra vị từ tại vị trí $i+2^k$. Nếu giá trị vẫn bằng $0$, con trỏ được tăng từ $i$ lên $i+2^k$; nếu không, con trỏ giữ nguyên. Sau đó giảm $k$ đi $1$.

Mô hình này được dùng nhiều trong các bài toán trên cây, chẳng hạn tìm tổ tiên chung thấp nhất hoặc tìm một tổ tiên có độ cao nhất định. Nó cũng có thể được điều chỉnh để tìm phần tử khác $0$ thứ $k$ trong Fenwick tree.

## Bài tập luyện tập

* [LeetCode -  Find First and Last Position of Element in Sorted Array](https://leetcode.com/problems/find-first-and-last-position-of-element-in-sorted-array/)
* [LeetCode -  Search Insert Position](https://leetcode.com/problems/search-insert-position/)
* [LeetCode -  First Bad Version](https://leetcode.com/problems/first-bad-version/)
* [LeetCode -  Valid Perfect Square](https://leetcode.com/problems/valid-perfect-square/)
* [LeetCode -  Find Peak Element](https://leetcode.com/problems/find-peak-element/)
* [LeetCode -  Search in Rotated Sorted Array](https://leetcode.com/problems/search-in-rotated-sorted-array/)
* [LeetCode -  Find Right Interval](https://leetcode.com/problems/find-right-interval/)
* [Codeforces - Interesting Drink](https://codeforces.com/problemset/problem/706/B/)
* [Codeforces - Magic Powder - 1](https://codeforces.com/problemset/problem/670/D1)
* [Codeforces - Another Problem on Strings](https://codeforces.com/problemset/problem/165/C)
* [Codeforces - Frodo and pillows](https://codeforces.com/problemset/problem/760/B)
* [Codeforces - GukiZ hates Boxes](https://codeforces.com/problemset/problem/551/C)
* [Codeforces - Enduring Exodus](https://codeforces.com/problemset/problem/645/C)
* [Codeforces - Chip 'n Dale Rescue Rangers](https://codeforces.com/problemset/problem/590/B)
* [Codeforces - Points on Line](https://codeforces.com/problemset/problem/251/A)
