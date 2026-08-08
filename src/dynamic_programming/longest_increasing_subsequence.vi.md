---
tags:
  - Translated
e_maxx_link: longest_increasing_subseq_log
translation:
  source: dynamic_programming/longest_increasing_subsequence.md
  source_commit: 9bed1d327f8ecf8ad9bac02ff2d51dbafb261eb8
  status: draft
  last_synced: 2026-08-08
---

# Dãy con tăng dài nhất

Cho một mảng gồm $n$ số: $a[0 \dots n-1]$.
Bài toán yêu cầu tìm dãy con tăng nghiêm ngặt dài nhất trong $a$.

Nói một cách hình thức, ta cần tìm dãy chỉ số dài nhất $i_1, \dots i_k$ sao cho

$$i_1 < i_2 < \dots < i_k,\quad
a[i_1] < a[i_2] < \dots < a[i_k]$$

Trong bài này, ta sẽ xét nhiều thuật toán để giải bài toán trên.
Ngoài ra, ta cũng sẽ xét một số bài toán khác có thể quy về bài toán này.

## Lời giải $O(n^2)$ bằng quy hoạch động {data-toc-label="Solution in O(n^2) with dynamic programming"}

Quy hoạch động là một kỹ thuật rất tổng quát, có thể giải một lớp bài toán rất rộng.
Ở đây ta áp dụng kỹ thuật này cho bài toán cụ thể của mình.

Trước tiên, ta chỉ tìm **độ dài** của dãy con tăng dài nhất; sau đó mới học cách khôi phục chính dãy con đó.

### Tìm độ dài

Ta định nghĩa mảng $d[0 \dots n-1]$, trong đó $d[i]$ là độ dài của dãy con tăng dài nhất kết thúc tại phần tử có chỉ số $i$.

!!! example

    $$\begin{array}{ll}
    a &= \{8, 3, 4, 6, 5, 2, 0, 7, 9, 1\} \\
    d &= \{1, 1, 2, 3, 3, 1, 1, 4, 5, 2\}
    \end{array}$$

    Dãy con tăng dài nhất kết thúc tại chỉ số 4 là $\{3, 4, 5\}$ với độ dài 3; dãy dài nhất kết thúc tại chỉ số 8 có thể là $\{3, 4, 5, 7, 9\}$ hoặc $\{3, 4, 6, 7, 9\}$, cả hai đều có độ dài 5; còn dãy dài nhất kết thúc tại chỉ số 9 là $\{0, 1\}$ với độ dài 2.

Ta sẽ tính mảng này dần dần: trước hết là $d[0]$, rồi $d[1]$, và cứ thế tiếp tục.
Sau khi tính xong mảng, đáp án của bài toán là giá trị lớn nhất trong mảng $d[]$.

Giả sử chỉ số hiện tại là $i$.
Tức là ta muốn tính $d[i]$ và mọi giá trị trước đó $d[0], \dots, d[i-1]$ đều đã biết.
Khi đó có hai trường hợp:

-   $d[i] = 1$: dãy con cần tìm chỉ gồm phần tử $a[i]$.

-   $d[i] > 1$: Dãy con kết thúc tại $a[i]$, và ngay trước nó là một số $a[j]$ nào đó với $j < i$ và $a[j] < a[i]$.

    Dễ thấy dãy con kết thúc tại $a[j]$ phải là một trong các dãy con tăng dài nhất kết thúc tại $a[j]$.
    Phần tử $a[i]$ chỉ đơn giản là nối thêm một số vào dãy con tăng dài nhất đó.

    Vì vậy ta chỉ cần duyệt mọi $j < i$ thỏa $a[j] < a[i]$, rồi chọn dãy dài nhất thu được khi nối $a[i]$ vào dãy con tăng dài nhất kết thúc tại $a[j]$.
    Dãy con tăng dài nhất kết thúc tại $a[j]$ có độ dài $d[j]$, nên khi nối thêm một phần tử ta được độ dài $d[j] + 1$.
  
    $$d[i] = \max_{\substack{j < i \\\\ a[j] < a[i]}} \left(d[j] + 1\right)$$

Gộp hai trường hợp trên, ta thu được công thức cuối cùng cho $d[i]$:

$$d[i] = \max\left(1, \max_{\substack{j < i \\\\ a[j] < a[i]}} \left(d[j] + 1\right)\right)$$

### Cài đặt

Dưới đây là cài đặt của thuật toán vừa mô tả để tính độ dài dãy con tăng dài nhất.

```{.cpp file=lis_n2}
int lis(vector<int> const& a) {
    int n = a.size();
    vector<int> d(n, 1);
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < i; j++) {
            if (a[j] < a[i])
                d[i] = max(d[i], d[j] + 1);
        }
    }

    int ans = d[0];
    for (int i = 1; i < n; i++) {
        ans = max(ans, d[i]);
    }
    return ans;
}
```

### Khôi phục dãy con

Cho tới đây ta mới biết cách tìm độ dài dãy con, chứ chưa biết cách tìm chính dãy con đó.

Để khôi phục dãy con, ta tạo thêm một mảng phụ $p[0 \dots n-1]$ và tính nó song song với mảng $d[]$.
$p[i]$ là chỉ số $j$ của phần tử đứng ngay trước phần tử cuối cùng trong dãy con tăng dài nhất kết thúc tại $i$.
Nói cách khác, $p[i]$ chính là chỉ số $j$ tại đó ta đạt được giá trị lớn nhất cho $d[i]$.
Có thể xem mảng phụ $p[]$ như các liên kết trỏ về phần tử trước.

Để dựng lại dãy con, ta bắt đầu tại chỉ số $i$ có $d[i]$ lớn nhất rồi lần theo các liên kết này cho tới khi thu được toàn bộ dãy, tức tới phần tử có $d[i] = 1$.

### Cài đặt phần khôi phục

Ta sửa một chút đoạn mã ở phần trước.
Mảng $p[]$ được tính cùng với $d[]$, rồi sau đó dùng để dựng lại dãy con.

Để thuận tiện, ban đầu ta gán các liên kết trước bằng $p[i] = -1$.
Với các phần tử có $d[i] = 1$, giá trị này vẫn là $-1$, nhờ đó việc khôi phục dãy con đơn giản hơn một chút.

```{.cpp file=lis_n2_restore}
vector<int> lis(vector<int> const& a) {
    int n = a.size();
    vector<int> d(n, 1), p(n, -1);
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < i; j++) {
            if (a[j] < a[i] && d[i] < d[j] + 1) {
                d[i] = d[j] + 1;
                p[i] = j;
            }
        }
    }

    int ans = d[0], pos = 0;
    for (int i = 1; i < n; i++) {
        if (d[i] > ans) {
            ans = d[i];
            pos = i;
        }
    }

    vector<int> subseq;
    while (pos != -1) {
        subseq.push_back(a[pos]);
        pos = p[pos];
    }
    reverse(subseq.begin(), subseq.end());
    return subseq;
}
```

### Một cách khác để khôi phục dãy con

Ta cũng có thể khôi phục dãy con mà không cần mảng phụ $p[]$.
Chỉ cần tính lại giá trị hiện tại của $d[i]$ và đồng thời xác định giá trị lớn nhất đã đạt được theo cách nào.

Cách này làm đoạn mã dài hơn một chút, nhưng đổi lại tiết kiệm được một phần bộ nhớ.

## Lời giải $O(n \log n)$ bằng quy hoạch động và tìm kiếm nhị phân {data-toc-label="Solution in O(n log n) with dynamic programming and binary search"}

Để có lời giải nhanh hơn, ta xây dựng một cách quy hoạch động khác chạy trong $O(n^2)$ rồi cải tiến nó thành $O(n \log n)$.

Ta dùng mảng quy hoạch động $d[0 \dots n]$.
Lần này $d[l]$ không tương ứng với phần tử $a[i]$ hay với một tiền tố của mảng.
$d[l]$ sẽ là phần tử nhỏ nhất mà một dãy con tăng độ dài $l$ có thể kết thúc tại đó.

Ban đầu, ta giả sử $d[0] = -\infty$ và với mọi độ dài còn lại $d[l] = \infty$.

Ta lại lần lượt xử lý các số, trước hết $a[0]$, rồi $a[1]$, v.v.; ở mỗi bước ta duy trì mảng $d[]$ sao cho nó luôn phản ánh đúng các phần tử đã xử lý.

!!! example

    Với mảng $a = \{8, 3, 4, 6, 5, 2, 0, 7, 9, 1\}$, dưới đây là mọi tiền tố của nó và mảng quy hoạch động tương ứng.
    Lưu ý rằng các giá trị trong mảng không phải lúc nào cũng thay đổi ở cuối mảng.

    $$
    \begin{array}{ll}
    \text{prefix} = \{\} &\quad d = \{-\infty, \infty, \dots\}\\
    \text{prefix} = \{8\} &\quad d = \{-\infty, 8, \infty, \dots\}\\
    \text{prefix} = \{8, 3\} &\quad d = \{-\infty, 3, \infty, \dots\}\\
    \text{prefix} = \{8, 3, 4\} &\quad d = \{-\infty, 3, 4, \infty, \dots\}\\
    \text{prefix} = \{8, 3, 4, 6\} &\quad d = \{-\infty, 3, 4, 6, \infty, \dots\}\\
    \text{prefix} = \{8, 3, 4, 6, 5\} &\quad d = \{-\infty, 3, 4, 5, \infty, \dots\}\\
    \text{prefix} = \{8, 3, 4, 6, 5, 2\} &\quad d = \{-\infty, 2, 4, 5, \infty, \dots \}\\
    \text{prefix} = \{8, 3, 4, 6, 5, 2, 0\} &\quad d = \{-\infty, 0, 4, 5, \infty, \dots \}\\
    \text{prefix} = \{8, 3, 4, 6, 5, 2, 0, 7\} &\quad d = \{-\infty, 0, 4, 5, 7, \infty, \dots \}\\
    \text{prefix} = \{8, 3, 4, 6, 5, 2, 0, 7, 9\} &\quad d = \{-\infty, 0, 4, 5, 7, 9, \infty, \dots \}\\
    \text{prefix} = \{8, 3, 4, 6, 5, 2, 0, 7, 9, 1\} &\quad d = \{-\infty, 0, 1, 5, 7, 9, \infty, \dots \}\\
    \end{array}
    $$

Khi xử lý $a[i]$, ta tự hỏi:
Điều kiện nào cần thỏa để ghi số hiện tại $a[i]$ vào mảng $d[0 \dots n]$?

Ta đặt $d[l] = a[i]$ nếu tồn tại một dãy con tăng dài nhất độ dài $l$ kết thúc tại $a[i]$, đồng thời không có dãy con tăng dài nhất độ dài $l$ nào kết thúc tại một số nhỏ hơn.
Tương tự cách trước, nếu bỏ $a[i]$ khỏi dãy con tăng dài nhất độ dài $l$, ta thu được một dãy con tăng dài nhất khác có độ dài $l -1$.
Vì vậy ta muốn nối $a[i]$ vào một dãy con tăng dài nhất độ dài $l - 1$; rõ ràng dãy độ dài $l - 1$ có phần tử cuối nhỏ nhất sẽ thuận lợi nhất, tức dãy độ dài $l-1$ kết thúc tại $d[l-1]$.

Tồn tại một dãy con tăng dài nhất độ dài $l - 1$ mà ta có thể nối thêm $a[i]$ khi và chỉ khi $d[l-1] < a[i]$.
Do đó, ta có thể duyệt mọi độ dài $l$ và kiểm tra điều kiện này để xem có thể mở rộng dãy độ dài $l - 1$ hay không.

Ngoài ra, ta cũng phải kiểm tra liệu đã tìm được một dãy con tăng dài nhất độ dài $l$ với phần tử cuối nhỏ hơn hay chưa.
Vì vậy chỉ cập nhật khi $a[i] < d[l]$.

Sau khi xử lý mọi phần tử của $a[]$, độ dài dãy con cần tìm là giá trị $l$ lớn nhất thỏa $d[l] < \infty$.

```{.cpp file=lis_method2_n2}
int lis(vector<int> const& a) {
    int n = a.size();
    const int INF = 1e9;
    vector<int> d(n+1, INF);
    d[0] = -INF;

    for (int i = 0; i < n; i++) {
        for (int l = 1; l <= n; l++) {
            if (d[l-1] < a[i] && a[i] < d[l])
                d[l] = a[i];
        }
    }

    int ans = 0;
    for (int l = 0; l <= n; l++) {
        if (d[l] < INF)
            ans = l;
    }
    return ans;
}
```

Bây giờ ta có hai nhận xét quan trọng.

1.  Mảng $d$ luôn được sắp xếp:
    $d[l-1] < d[l]$ với mọi $i = 1 \dots n$.

    Điều này hiển nhiên vì chỉ cần bỏ phần tử cuối khỏi dãy con tăng độ dài $l$, ta nhận được một dãy con tăng độ dài $l-1$ với phần tử cuối nhỏ hơn.

2.  Phần tử $a[i]$ chỉ cập nhật nhiều nhất một giá trị $d[l]$.

    Điều này suy ra trực tiếp từ cài đặt phía trên.
    Chỉ có thể tồn tại một vị trí trong mảng thỏa $d[l-1] < a[i] < d[l]$.

**Ghi chú bản dịch:** Ở nhận xét thứ nhất, bất đẳng thức được đánh chỉ số theo l nhưng nguồn lại viết “với mọi i”. Ký hiệu đúng trong lượng từ phải là l. Bản dịch giữ nguyên biểu thức của nguồn và chỉ ghi chú lỗi ký hiệu này.

Vì vậy, ta có thể tìm phần tử này trong mảng $d[]$ bằng [tìm kiếm nhị phân](../num_methods/binary_search.md) trong $O(\log n)$.
Thực tế, ta chỉ cần tìm trong $d[]$ số đầu tiên lớn hơn nghiêm ngặt $a[i]$, rồi thử cập nhật phần tử đó giống như trong cài đặt phía trên.

### Cài đặt

Ta thu được cài đặt $O(n \log n)$ nhanh hơn:

```{.cpp file=lis_method2_nlogn}
int lis(vector<int> const& a) {
    int n = a.size();
    const int INF = 1e9;
    vector<int> d(n+1, INF);
    d[0] = -INF;

    for (int i = 0; i < n; i++) {
        int l = upper_bound(d.begin(), d.end(), a[i]) - d.begin();
        if (d[l-1] < a[i] && a[i] < d[l])
            d[l] = a[i];
    }

    int ans = 0;
    for (int l = 0; l <= n; l++) {
        if (d[l] < INF)
            ans = l;
    }
    return ans;
}
```

**Ghi chú bản dịch:** Hai cài đặt của cách tiếp cận này dùng 1e9 và -1e9 làm hai giá trị canh gác nhưng bài không nêu giới hạn giá trị phần tử. Vì đầu vào là int, các giá trị đủ lớn hoặc đủ nhỏ vẫn hợp lệ nhưng có thể làm giả thiết về hai giá trị canh gác không còn đúng. Bản dịch giữ nguyên code nguồn; vấn đề này được tách để đề xuất sửa ở bản tiếng Anh.

### Khôi phục dãy con

Cách tiếp cận này cũng có thể khôi phục dãy con.
Lần này ta cần duy trì hai mảng phụ.
Một mảng cho biết chỉ số của các phần tử trong $d[]$.
Và một lần nữa ta tạo mảng các "phần tử trước" $p[i]$.
$p[i]$ là chỉ số của phần tử trước đó trong dãy con tối ưu kết thúc tại phần tử $i$.

Hai mảng này có thể được duy trì dễ dàng trong khi duyệt mảng $a[]$ song song với quá trình tính $d[]$.
Sau cùng, ta có thể dùng chúng để khôi phục dãy con cần tìm.

## Lời giải $O(n \log n)$ bằng cấu trúc dữ liệu {data-toc-label="Solution in O(n log n) with data structures"}

Thay vì cách tính dãy con tăng dài nhất trong $O(n \log n)$ ở trên, ta cũng có thể giải bài toán theo một hướng khác bằng một số cấu trúc dữ liệu đơn giản.

Quay lại phương pháp đầu tiên.
Nhớ rằng $d[i]$ là giá trị $d[j] + 1$ với $j < i$ và $a[j] < a[i]$.

Vì vậy, nếu định nghĩa thêm một mảng $t[]$ sao cho

$$t[a[i]] = d[i],$$

thì bài toán tính $d[i]$ tương đương với việc tìm **giá trị lớn nhất trên một tiền tố** của mảng $t[]$:

$$d[i] = \max\left(t[0 \dots a[i] - 1] + 1\right)$$

Bài toán tìm giá trị lớn nhất trên một tiền tố của một mảng có thay đổi là bài toán chuẩn có thể giải bằng nhiều cấu trúc dữ liệu khác nhau.
Chẳng hạn, ta có thể dùng [Segment tree](../data_structures/segment_tree.md) hoặc [Fenwick tree](../data_structures/fenwick.md).

Cách này có một số **nhược điểm** rõ ràng:
về độ dài và độ phức tạp cài đặt, nó sẽ tệ hơn phương pháp dùng tìm kiếm nhị phân.
Ngoài ra, nếu các số đầu vào $a[i]$ đặc biệt lớn, ta phải dùng một số kỹ thuật như nén các số (tức đánh lại số từ $0$ đến $n-1$), hoặc dùng segment tree động (chỉ tạo những nhánh cây thực sự cần thiết).
Nếu không, lượng bộ nhớ cần dùng sẽ quá lớn.

Mặt khác, phương pháp này cũng có một số **ưu điểm**:
ta không cần suy luận về các tính chất tinh tế của lời giải quy hoạch động.
Hơn nữa, cách tiếp cận này cho phép tổng quát hóa bài toán rất dễ dàng (xem bên dưới).

## Các bài toán liên quan

Dưới đây là một số bài toán liên hệ chặt chẽ với bài toán dãy con tăng dài nhất.

### Dãy con không giảm dài nhất

Thực chất đây gần như là cùng một bài toán.
Điểm khác biệt duy nhất là bây giờ các số bằng nhau được phép xuất hiện trong dãy con.

Lời giải về cơ bản cũng gần như giống hệt.
Ta chỉ cần đổi dấu bất đẳng thức và điều chỉnh nhẹ phép tìm kiếm nhị phân.

### Số lượng dãy con tăng dài nhất

Ta có thể dùng phương pháp đầu tiên, cả phiên bản $O(n^2)$ lẫn phiên bản dùng cấu trúc dữ liệu.
Chỉ cần lưu thêm số cách tạo ra các dãy con tăng dài nhất kết thúc tại các giá trị $d[i]$.

Số cách tạo một dãy con tăng dài nhất kết thúc tại $a[i]$ bằng tổng số cách của mọi dãy con tăng dài nhất kết thúc tại $j$ mà $d[j]$ đạt giá trị lớn nhất.
Có thể có nhiều chỉ số $j$ như vậy, nên cần cộng tất cả các cách tương ứng.

Dùng Segment tree, cách này cũng có thể được cài đặt trong $O(n \log n)$.

Không thể dùng cách tìm kiếm nhị phân cho bài toán này.

### Số ít nhất các dãy con không tăng để phủ một dãy

Cho một mảng gồm $n$ số $a[0 \dots n - 1]$, ta cần tô màu các số bằng số màu ít nhất sao cho các phần tử cùng màu tạo thành một dãy con không tăng.

Để giải bài toán, ta nhận thấy số màu ít nhất cần dùng bằng độ dài của dãy con tăng dài nhất.

**Chứng minh**:
Ta cần chứng minh tính **đối ngẫu** của hai bài toán này.

Gọi $x$ là độ dài của dãy con tăng dài nhất và $y$ là số dãy con không tăng ít nhất tạo thành một phép phủ.
Ta cần chứng minh $x = y$.

Rõ ràng không thể có $y < x$, bởi nếu có $x$ phần tử tăng nghiêm ngặt thì không có hai phần tử nào trong số đó có thể thuộc cùng một dãy con không tăng.
Vì vậy $y \ge x$.

Bây giờ ta chứng minh bằng phản chứng rằng cũng không thể có $y > x$.
Giả sử $y > x$.
Xét một tập tối ưu bất kỳ gồm $y$ dãy con không tăng.
Ta biến đổi tập này như sau:
chừng nào còn tồn tại hai dãy con sao cho dãy thứ nhất bắt đầu trước dãy thứ hai và phần tử đầu của dãy thứ nhất lớn hơn hoặc bằng phần tử đầu của dãy thứ hai, ta tách phần tử đầu này ra rồi gắn nó vào đầu dãy thứ hai.
Sau hữu hạn bước, ta vẫn có $y$ dãy con và các phần tử đầu của chúng tạo thành một dãy con tăng độ dài $y$.
Vì đã giả sử $y > x$, ta thu được mâu thuẫn.

Do đó $y = x$.

**Khôi phục các dãy**:
Ta có thể dựng phép phân hoạch mong muốn thành các dãy con bằng một chiến lược tham lam.
Cụ thể, duyệt từ trái sang phải và gán số hiện tại vào dãy con đang kết thúc bằng số nhỏ nhất nhưng vẫn lớn hơn hoặc bằng số hiện tại.

## Bài tập luyện tập

- [ACMSGURU - "North-East"](http://codeforces.com/problemsets/acmsguru/problem/99999/521)
- [Codeforces - LCIS](http://codeforces.com/problemset/problem/10/D)
- [Codeforces - Tourist](http://codeforces.com/contest/76/problem/F)
- [SPOJ - DOSA](https://www.spoj.com/problems/DOSA/)
- [SPOJ - HMLIS](https://www.spoj.com/problems/HMLIS/)
- [SPOJ - ONEXLIS](https://www.spoj.com/problems/ONEXLIS/)
- [SPOJ - SUPPER](http://www.spoj.com/problems/SUPPER/)
- [Topcoder - AutoMarket](https://community.topcoder.com/stat?c=problem_statement&pm=3937&rd=6532)
- [Topcoder - BridgeArrangement](https://community.topcoder.com/stat?c=problem_statement&pm=2967&rd=5881)
- [Topcoder - IntegerSequence](https://community.topcoder.com/stat?c=problem_statement&pm=5922&rd=8075)
- [UVA - Back To Edit Distance](https://onlinejudge.org/external/127/12747.pdf)
- [UVA - Happy Birthday](https://onlinejudge.org/external/120/12002.pdf)
- [UVA - Tiling Up Blocks](https://onlinejudge.org/external/11/1196.pdf)
