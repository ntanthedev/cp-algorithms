---
tags:
  - Original
translation:
  source: num_methods/binary_search.md
  source_commit: 80463b8247a7426f060aa1b7f06245e3dd500416
  status: draft
  last_synced: 2026-09-29
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

Cận dưới và cận trên tạo thành một nửa khoảng, có thể rỗng, chứa toàn bộ phần tử bằng $k$. Để kiểm tra $k$ có xuất hiện hay không, chỉ cần tìm cận dưới của $k$ rồi kiểm tra phần tử tại vị trí đó có bằng $k$ không.

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

Cách tìm kiếm nhị phân ở trên thực chất tìm điểm phân chia của mảng theo vị từ $f(M)$, trong đó vị từ này biểu diễn giá trị Boolean của điều kiện $k < A_M$.
Ta có thể thay điều kiện $k < A_M$ bằng một vị từ tăng đơn điệu bất kỳ. Điều này đặc biệt hữu ích khi việc tính $f(k)$ đủ tốn thời gian khiến ta không thể thử mọi giá trị.
Nói cách khác, tìm kiếm nhị phân tìm chỉ số duy nhất $L$ sao cho $f(L) = 0$ và $f(R)=f(L+1)=1$ nếu tồn tại một điểm chuyển như vậy. Nếu $f(0) = \dots = f(n-1) = 0$, thuật toán cho $L = n-1$; còn nếu $f(0) = \dots = f(n-1) = 1$, thuật toán cho $L = -1$.

Chứng minh tính đúng đắn khi điểm chuyển tồn tại, tức $f(0)=0$ và $f(n-1)=1$: cài đặt duy trì bất biến vòng lặp $f(l)=0, f(r)=1$. Khi $r - l > 1$, cách chọn $m$ bảo đảm $r-l$ luôn giảm. Vòng lặp dừng khi $r - l = 1$, và ta thu được đúng điểm chuyển cần tìm.

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

trên mọi cặp $l, r$ thỏa mãn $r-l \geq x$. Một cách giải là kiểm tra xem đáp án có ít nhất bằng $\lambda$ hay không, tức liệu có cặp $l,r$ sao cho

$$
\frac{a_l + a_{l+1} + \dots + a_r}{r-l+1} \geq \lambda.
$$

Biến đổi tương đương, ta được

$$
(a_l - \lambda) + (a_{l+1} - \lambda) + \dots + (a_r - \lambda) \geq 0,
$$

vì vậy bài toán trở thành kiểm tra xem trong mảng mới $a_i - \lambda$ có đoạn con độ dài ít nhất $x+1$ và tổng không âm hay không. Điều này có thể thực hiện bằng tổng tiền tố.

## Tìm kiếm liên tục

Cho $f : \mathbb R \to \mathbb R$ là một hàm thực liên tục trên đoạn $[L, R]$.

Không mất tính tổng quát, giả sử $f(L) \leq f(R)$. Theo [định lý giá trị trung gian](https://en.wikipedia.org/wiki/Intermediate_value_theorem), với mọi $y \in [f(L), f(R)]$, tồn tại $x \in [L, R]$ sao cho $f(x) = y$. Khác với các phần trước, ở đây hàm không bắt buộc phải đơn điệu.

Với một $\delta$ cho trước, giá trị $x$ có thể được xấp xỉ với sai số $\pm\delta$ trong thời gian $O\left(\log \frac{R-L}{\delta}\right)$. Ý tưởng vẫn tương tự: chọn $M \in (L, R)$ rồi thu hẹp khoảng về $[L, M]$ hoặc $[M, R]$ tùy theo $f(M)$ lớn hơn hay nhỏ hơn $y$. Một ví dụ quen thuộc là tìm nghiệm của đa thức bậc lẻ.

Chẳng hạn, xét $f(x)=x^3 + ax^2 + bx + c$. Khi $L \to -\infty$ và $R \to +\infty$, ta có $f(L) \to -\infty$ và $f(R) \to +\infty$. Vì vậy luôn có thể chọn $L$ đủ nhỏ và $R$ đủ lớn để $f(L) < 0$ và $f(R) > 0$. Sau đó, tìm kiếm nhị phân có thể tìm một khoảng nhỏ tùy ý chứa nghiệm $x$ sao cho $f(x)=0$.

## Tìm kiếm theo lũy thừa của 2

Một cách đáng chú ý khác là không duy trì đoạn đang xét, mà duy trì con trỏ hiện tại $i$ và số mũ hiện tại $k$. Ban đầu $i=L$. Ở mỗi bước, ta kiểm tra vị từ tại vị trí $i+2^k$. Nếu giá trị vẫn bằng $0$, con trỏ được tăng từ $i$ lên $i+2^k$; nếu không, con trỏ giữ nguyên. Sau đó giảm $k$ đi $1$.

Mô hình này được dùng nhiều trong các bài toán trên cây, chẳng hạn tìm tổ tiên chung thấp nhất hoặc tìm một tổ tiên có độ cao nhất định. Nó cũng có thể được điều chỉnh để tìm phần tử khác không thứ $k$ trong Fenwick tree.

## Tìm kiếm nhị phân song song

Khi có nhiều truy vấn mà mỗi truy vấn có thể được giải bằng tìm kiếm nhị phân, xử lý từng truy vấn riêng rẽ đôi khi quá chậm. Tìm kiếm nhị phân song song (Parallel Binary Search) cho phép xử lý đồng thời tất cả các truy vấn, thường giúp cải thiện đáng kể hiệu năng. Ý tưởng chính là thực hiện từng bước tìm kiếm nhị phân cho tất cả truy vấn cùng lúc. Cách này đặc biệt hiệu quả khi hàm kiểm tra tốn kém và có thể tối ưu bằng cách xử lý truy vấn theo nhóm.

Giả sử có $Q$ truy vấn; với mỗi truy vấn $q$, ta cần tìm giá trị $x$ nhỏ nhất thỏa điều kiện $P(q, x)$. Nếu $P(q, x)$ đơn điệu theo $x$, ta có thể tìm kiếm nhị phân cho từng truy vấn. Tổng độ phức tạp khi đó là $O(Q \cdot \log(range) \cdot T_{check})$, trong đó $T_{check}$ là thời gian tính $P(q, x)$.

Tìm kiếm nhị phân song song tối ưu bằng cách đổi thứ tự thực hiện. Thay vì xử lý độc lập mỗi truy vấn, ta xử lý từng bước của tất cả truy vấn cùng lúc. Ở mỗi bước tìm kiếm nhị phân, ta tính các điểm giữa $m_i$ cho mọi truy vấn và nhóm các truy vấn theo điểm giữa. Cách này đặc biệt hữu ích khi hàm kiểm tra $P(q, x)$ có cấu trúc cho phép xử lý theo nhóm hoặc cập nhật hiệu quả.

Cụ thể, lợi ích hiệu năng chính đến từ hai tình huống:

1. **Gom các phép kiểm tra tốn kém:** Nếu nhiều truy vấn cần kiểm tra cùng giá trị $m$ trong một bước, ta chỉ thực hiện phần tốn kém một lần rồi dùng lại kết quả.
2. **Phép kiểm tra có thể cập nhật hiệu quả:** Thường thì kiểm tra giá trị $m$ (chẳng hạn "xử lý $m$ sự kiện đầu tiên") nhanh hơn nhiều nếu đã tính trạng thái cho $m-1$. Bằng cách xử lý các giá trị kiểm tra $m$ theo thứ tự tăng dần, ta cập nhật trạng thái từ phép kiểm tra này sang phép kiểm tra kế tiếp thay vì tính lại từ đầu. Đây là dạng thường gặp trong các bài toán liên quan tới thời gian hoặc một chuỗi cập nhật.

Cách xử lý truy vấn "offline", trong đó thu thập tất cả truy vấn rồi trả lời chung theo thứ tự thuận tiện cho cấu trúc dữ liệu, là ý tưởng cốt lõi của tìm kiếm nhị phân song song.

### Cài đặt

Giả sử ta muốn trả lời $Z$ truy vấn về chỉ số của giá trị lớn nhất không vượt quá $X_i$ nào đó (với $i=1,2,\ldots,Z$) trong mảng đã sắp xếp $A$ đánh chỉ số từ 0. Hiển nhiên, mỗi truy vấn có thể được trả lời bằng tìm kiếm nhị phân.

Cụ thể, xét mảng $A = [1,3,5,7,9,9,13,15]$
với các truy vấn $X = [8,11,4,5]$. Ta có thể tìm kiếm nhị phân lần lượt cho từng truy vấn.

| Truy vấn      |                            \( X_1 = 8 \)                             |                            \( X_2 = 11 \)                            |                            \( X_3 = 4 \)                             |                            \( X_4 = 5 \)                             |
| ---------- | :------------------------------------------------------------------: | :------------------------------------------------------------------: | :------------------------------------------------------------------: | :------------------------------------------------------------------: |
| **Bước 1** |  Đáp án trong \([0,8)\) <br> Kiểm tra \( A_4 \) <br> \( X_1 < A_4 = 9 \)   | Đáp án trong \([0,8)\) <br> Kiểm tra \( A_4 \) <br> \( X_2 \geq A_4 = 9 \) |  Đáp án trong \([0,8)\) <br> Kiểm tra \( A_4 \) <br> \( X_3 < A_4 = 9 \)   |  Đáp án trong \([0,8)\) <br> Kiểm tra \( A_4 \) <br> \( X_4 < A_4 = 9 \)   |
| **Bước 2** | Đáp án trong \([0,4)\) <br> Kiểm tra \( A_2 \) <br> \( X_1 \geq A_2 = 5 \) |  Đáp án trong \([4,8)\) <br> Kiểm tra \( A_6 \) <br> \( X_2 < A_6 = 13 \)  |  Đáp án trong \([0,4)\) <br> Kiểm tra \( A_2 \) <br> \( X_3 < A_2 = 5 \)   | Đáp án trong \([0,4)\) <br> Kiểm tra \( A_2 \) <br> \( X_4 \geq A_2 = 5 \) |
| **Bước 3** | Đáp án trong \([2,4)\) <br> Kiểm tra \( A_3 \) <br> \( X_1 \geq A_3 = 7 \) | Đáp án trong \([4,6)\) <br> Kiểm tra \( A_5 \) <br> \( X_2 \geq A_5 = 9 \) | Đáp án trong \([0,2)\) <br> Kiểm tra \( A_1 \) <br> \( X_3 \geq A_1 = 3 \) |  Đáp án trong \([2,4)\) <br> Kiểm tra \( A_3 \) <br> \( X_4 < A_3 = 7 \)   |
| **Bước 4** |               Đáp án trong \([3,4)\) <br> \( index = 3 \)               |               Đáp án trong \([5,6)\) <br> \( index = 5 \)               |               Đáp án trong \([1,2)\) <br> \( index = 1 \)               |               Đáp án trong \([2,3)\) <br> \( index = 2 \)               |

Thông thường ta xử lý bảng này theo cột (truy vấn), nhưng trong mỗi hàng, việc truy cập một số giá trị mảng bị lặp lại. Để hạn chế số lần truy cập đó, ta có thể xử lý theo hàng (bước). Trong ví dụ nhỏ này, sự khác biệt không lớn vì mọi phần tử đều được truy cập trong $O(1)$, nhưng với các bài toán phức tạp hơn, khi tính các giá trị đó tốn kém hơn, cách này có thể quyết định hiệu quả của lời giải. Hơn nữa, ta có thể tùy ý chọn thứ tự trả lời các truy vấn trong một hàng. Dưới đây là code thực hiện cách tiếp cận này.

```{.cpp file=parallel_binary_search}
// Computes the index of the largest value in a sorted array A less than or equal to X_i for all i.
vector<int> parallel_binary_search(vector<int>& A, vector<int>& X) {
    int N = A.size();
    int Z = X.size();
    vector<int> l(Z, -1), r(Z, N);

    for (int step = 1; step <= ceil(log2(N + 1)); ++step) {
        // A vector of vectors to store indices of queries for each middle point.
        vector<vector<int>> m_to_queries(N);

        // Group queries by their middle point.
        for (int i = 0; i < Z; ++i) {
            if (l[i] < r[i] - 1) {
                int m = l[i] + (r[i] - l[i]) / 2;
                m_to_queries[m].push_back(i);
            }
        }

        // Process each group of queries.
        for (int m = 0; m < N; ++m) {
            if (m_to_queries[m].empty()) {
                continue;
            }
            for (int query : m_to_queries[m]) {
                if (X[query] < A[m]) {
                    r[query] = m;
                } else {
                    l[query] = m;
                }
            }
        }
    }
    return l;
}
```

??? note "Ví dụ lời giải: Meteors"

    Một bài toán khá nổi tiếng sử dụng phương pháp này là "Meteors", được liệt kê trong phần bài tập. Ta có $N$ quốc gia, mỗi quốc gia có một số thiên thạch mục tiêu cần thu thập. Ta cũng có một chuỗi $K$ trận mưa thiên thạch, mỗi trận tác động tới một đoạn các quốc gia. Mục tiêu là tìm thời điểm sớm nhất (tức trận mưa thiên thạch nào) mà mỗi quốc gia đạt mục tiêu.

    Với một quốc gia, ta có thể tìm kiếm nhị phân đáp án từ $1$ đến $K$. Kiểm tra thời điểm $t$ đòi hỏi cộng số thiên thạch từ $t$ trận mưa đầu tiên cho quốc gia đó. Kiểm tra trực tiếp mất $O(t)$, dẫn tới tổng độ phức tạp $O(K \log K)$ cho một quốc gia và $O(N \cdot K \log K)$ cho tất cả, quá chậm.

    Với tìm kiếm nhị phân song song, ta tìm đáp án cho cả $N$ quốc gia cùng lúc. Trong mỗi bước của $O(\log K)$ bước, ta có các giá trị cần kiểm tra $t_i$ của các quốc gia. Ta xử lý các $t_i$ theo thứ tự tăng dần. Để kiểm tra thời điểm $t$, có thể dùng cây Fenwick hoặc cây phân đoạn lưu số thiên thạch cho mọi quốc gia. Khi chuyển từ kiểm tra $t_i$ sang $t_{i+1}$, ta chỉ cần thêm tác động của các trận mưa từ $t_i+1$ đến $t_{i+1}$ vào cấu trúc dữ liệu. Cách "cập nhật" này nhanh hơn nhiều so với tính lại từ đầu. Tổng độ phức tạp trở thành $O((N+K)\log N \log K)$.

## Bài tập luyện tập

### Tìm kiếm nhị phân

- [LeetCode - Find First and Last Position of Element in Sorted Array](https://leetcode.com/problems/find-first-and-last-position-of-element-in-sorted-array/)
- [LeetCode - Search Insert Position](https://leetcode.com/problems/search-insert-position/)
- [LeetCode - First Bad Version](https://leetcode.com/problems/first-bad-version/)
- [LeetCode - Valid Perfect Square](https://leetcode.com/problems/valid-perfect-square/)
- [LeetCode - Find Peak Element](https://leetcode.com/problems/find-peak-element/)
- [LeetCode - Search in Rotated Sorted Array](https://leetcode.com/problems/search-in-rotated-sorted-array/)
- [LeetCode - Find Right Interval](https://leetcode.com/problems/find-right-interval/)
- [Codeforces - Interesting Drink](https://codeforces.com/problemset/problem/706/B/)
- [Codeforces - Magic Powder - 1](https://codeforces.com/problemset/problem/670/D1)
- [Codeforces - Another Problem on Strings](https://codeforces.com/problemset/problem/165/C)
- [Codeforces - Frodo and pillows](https://codeforces.com/problemset/problem/760/B)
- [Codeforces - GukiZ hates Boxes](https://codeforces.com/problemset/problem/551/C)
- [Codeforces - Enduring Exodus](https://codeforces.com/problemset/problem/645/C)
- [Codeforces - Chip 'n Dale Rescue Rangers](https://codeforces.com/problemset/problem/590/B)
- [Codeforces - Points on Line](https://codeforces.com/problemset/problem/251/A)

### Tìm kiếm nhị phân song song

- [Szkopul - Meteors](https://szkopul.edu.pl/problemset/problem/7JrCYZ7LhEK4nBR5zbAXpcmM/site/?key=statement)
- [AtCoder - Stamp Rally](https://atcoder.jp/contests/agc002/tasks/agc002_d)
