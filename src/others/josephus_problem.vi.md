---
tags:
  - Translated
e_maxx_link: joseph_problem
translation:
  source: others/josephus_problem.md
  source_commit: 5200d0ad4fd9cc8f25d6fc7bca3964226249d1ee
  status: draft
  last_synced: 2026-11-16
---

# Bài toán Josephus

## Đề bài

Cho hai số tự nhiên $n$ và $k$. Viết các số tự nhiên từ $1$ đến $n$ thành một vòng tròn. Trước tiên, đếm từ số đầu tiên và xóa số thứ $k$. Sau đó tiếp tục đếm $k$ số từ số kế tiếp rồi lại xóa số thứ $k$, cứ thế tiếp tục. Quá trình dừng khi chỉ còn một số. Hãy tìm số cuối cùng đó.

Bài toán do **Flavius Josephus** đặt ra vào thế kỷ thứ nhất, dù dưới dạng hẹp hơn một chút: $k = 2$.

Ta có thể giải bằng cách mô phỏng quá trình. Mô phỏng trực tiếp mất $O(n^{2})$. Dùng [cây đoạn](../data_structures/segment_tree.md), ta có thể cải thiện xuống $O(n \log n)$. Tuy nhiên, ta muốn một cách tốt hơn.

## Xây dựng lời giải $O(n)$

Ta thử tìm quy luật biểu diễn đáp án của bài toán $J_{n, k}$ thông qua lời giải của các bài toán trước.

Bằng mô phỏng trực tiếp, ta có thể lập bảng giá trị, chẳng hạn:

$$\begin{array}{ccccccccccc}
n\setminus k & 1 & 2 & 3 & 4 & 5 & 6 & 7 & 8 & 9 & 10 \\
1 & 1 & 1 & 1 & 1 & 1 & 1 & 1 & 1 & 1 & 1 \\
2 & 2 & 1 & 2 & 1 & 2 & 1 & 2 & 1 & 2 & 1 \\
3 & 3 & 3 & 2 & 2 & 1 & 1 & 3 & 3 & 2 & 2 \\
4 & 4 & 1 & 1 & 2 & 2 & 3 & 2 & 3 & 3 & 4 \\
5 & 5 & 3 & 4 & 1 & 2 & 4 & 4 & 1 & 2 & 4 \\
6 & 6 & 5 & 1 & 5 & 1 & 4 & 5 & 3 & 5 & 2 \\
7 & 7 & 7 & 4 & 2 & 6 & 3 & 5 & 4 & 7 & 5 \\
8 & 8 & 1 & 7 & 6 & 3 & 1 & 4 & 4 & 8 & 7 \\
9 & 9 & 3 & 1 & 1 & 8 & 7 & 2 & 3 & 8 & 8 \\
10 & 10 & 5 & 4 & 5 & 3 & 3 & 9 & 1 & 7 & 8 \\
\end{array}$$

Từ đó ta thấy rõ **quy luật** sau:

$$J_{n,k} = \left( (J_{n-1,k} + k - 1) \bmod n \right) + 1$$

$$J_{1,k} = 1$$

Việc đánh số từ 1 khiến công thức hơi rườm rà; nếu đánh số từ 0, ta thu được công thức gọn hơn:

$$J_{n,k} = (J_{n-1,k} + k) \bmod n$$

Vậy ta đã tìm được lời giải bài toán Josephus với $O(n)$ phép toán.

## Cài đặt

**Cài đặt đệ quy** đơn giản (đánh số từ 1)

```{.cpp file=josephus_rec}
int josephus(int n, int k) {
    return n > 1 ? (josephus(n-1, k) + k - 1) % n + 1 : 1;
}
```

**Dạng không đệ quy**:

```{.cpp file=josephus_iter}
int josephus(int n, int k) {
    int res = 0;
    for (int i = 1; i <= n; ++i)
  	  res = (res + k) % i;
    return res + 1;
}
```

Ta cũng có thể tìm công thức này bằng phân tích. Ở đây tiếp tục giả sử các chỉ số bắt đầu từ 0. Sau khi xóa số đầu tiên, còn lại $n-1$ số. Khi lặp lại quá trình, ta sẽ bắt đầu từ số ban đầu có chỉ số $k \bmod n$. $J_{n-1, k}$ là đáp án trên vòng tròn còn lại nếu bắt đầu đếm từ $0$, nhưng thực tế ta bắt đầu từ $k$, nên ta có $J_{n, k} = (J_{n-1,k} + k) \ \bmod n$.

## Xây dựng lời giải $O(k \log n)$

Với $k$ tương đối nhỏ, ta có thể tìm lời giải tốt hơn lời giải đệ quy $O(n)$ ở trên. Nếu $k$ nhỏ hơn nhiều so với $n$, ta có thể xóa nhiều số ($\lfloor \frac{n}{k} \rfloor$) trong một lượt mà không cần duyệt từng số. Sau đó còn lại $n - \lfloor \frac{n}{k} \rfloor$ số và ta bắt đầu từ số thứ $(\lfloor \frac{n}{k} \rfloor \cdot k)$. Do đó ta cần dịch đi tương ứng. Ta có thể nhận thấy $\lfloor \frac{n}{k} \rfloor \cdot k$ chính là $-n \bmod k$. Vì đã xóa mỗi số thứ $k$, ta phải cộng thêm số lượng các số đã xóa trước chỉ số kết quả; số này tính được bằng cách chia chỉ số kết quả cho $k - 1$.

**Ghi chú bản dịch:** Khẳng định hai đại lượng ở trên bằng nhau không đúng nói chung. Chẳng hạn, với mười số và bước nhảy ba, đại lượng thứ nhất bằng chín, còn phần dư không âm của âm mười theo mô-đun ba bằng hai. Cách dịch chỉ số trong mã cần được xét riêng.

Ta cũng cần xử lý trường hợp $n$ nhỏ hơn $k$. Khi đó phép tối ưu trên sẽ gây vòng lặp vô hạn.

**Cài đặt** (đánh số từ 0 cho thuận tiện):

```{.cpp file=josephus_fast0}
int josephus(int n, int k) {
    if (n == 1)
        return 0;
    if (k == 1)
        return n-1;
    if (k > n)
        return (josephus(n-1, k) + k) % n;
    int cnt = n / k;
    int res = josephus(n - cnt, k);
    res -= n % k;
    if (res < 0)
        res += n;
    else
        res += res / (k - 1);
    return res;
}
```

Ta hãy ước lượng **độ phức tạp** của thuật toán. Trước hết, trường hợp $n < k$ được xử lý bằng lời giải cũ, mất $O(k)$. Giờ xét phần thuật toán còn lại. Sau mỗi vòng lặp, thay vì $n$ số, ta còn $n \left( 1 - \frac{1}{k} \right)$ số, do đó số vòng lặp $x$ có thể được ước lượng từ phương trình sau:

$$ n \left(1 - \frac{1}{k} \right) ^ x = 1, $$

Lấy logarit hai vế, ta được:

$$\ln n + x \ln \left(1 - \frac{1}{k} \right) = 0,$$ 
$$x = - \frac{\ln n}{\ln \left(1 - \frac{1}{k} \right)},$$

Khai triển logarit thành chuỗi Taylor, ta được ước lượng gần đúng:

$$x \approx k \ln n$$

Do đó, độ phức tạp của thuật toán là $O (k \log n)$.

## Lời giải giải tích cho $k = 2$

Trong trường hợp riêng này, cũng là dạng Josephus Flavius nêu ra, bài toán được giải dễ hơn nhiều.

Với $n$ chẵn, tất cả các số chẵn bị xóa và còn lại bài toán kích thước $\frac{n}{2}$. Khi đó, đáp án cho $n$ được tính từ đáp án cho $\frac{n}{2}$ bằng cách nhân hai rồi trừ một để dịch vị trí.

$$ J_{2n, 2} = 2 J_{n, 2} - 1 $$

Tương tự, với $n$ lẻ, tất cả số chẵn rồi số đầu tiên bị xóa, để lại bài toán kích thước $\frac{n-1}{2}$; tính đến việc dịch vị trí, ta có công thức thứ hai:

$$J_{2n+1,2} = 2 J_{n, 2} + 1 $$

Ta có thể dùng trực tiếp hệ thức truy hồi này khi cài đặt. Quy luật còn có thể được viết dưới dạng khác: $J_{n, 2}$ biểu diễn dãy các số lẻ, bắt đầu lại từ một mỗi khi $n$ là lũy thừa của hai. Ta viết thành công thức duy nhất:

$$J_{n, 2} = 1 + 2 \left(n-2^{\lfloor \log_2 n \rfloor} \right)$$

## Lời giải giải tích cho $k > 2$

Dù bài toán có dạng đơn giản và có nhiều bài viết về nó cùng các bài toán liên quan, vẫn chưa tìm được biểu diễn giải tích đơn giản cho lời giải Josephus. Với các giá trị nhỏ của $k$, một số công thức đã được suy ra nhưng dường như khó áp dụng trong thực tế (chẳng hạn, xem Halbeisen, Hungerbuhler "The Josephus Problem" và Odlyzko, Wilf "Functional iteration and the Josephus problem").
