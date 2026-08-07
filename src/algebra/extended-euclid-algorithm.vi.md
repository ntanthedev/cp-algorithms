---
tags:
  - Translated
e_maxx_link: extended_euclid_algorithm
translation:
  source: algebra/extended-euclid-algorithm.md
  source_commit: b884be46589764de16f2484136d0e7a82a656f83
  status: draft
  last_synced: 2026-08-07
---

# Thuật toán Euclid mở rộng

Trong khi [thuật toán Euclid](euclid-algorithm.md) chỉ tính ước chung lớn nhất (UCLN, GCD) của hai số nguyên không âm $a$ và $b$, phiên bản mở rộng còn tìm cách biểu diễn UCLN theo $a$ và $b$, tức tìm các hệ số $x$ và $y$ sao cho:

$$a \cdot x + b \cdot y = \gcd(a, b)$$

Điều quan trọng là theo [đồng nhất thức Bézout](https://en.wikipedia.org/wiki/B%C3%A9zout%27s_identity), ta luôn có thể tìm được một biểu diễn như vậy. Chẳng hạn, $\gcd(55, 80) = 5$, nên có thể biểu diễn $5$ dưới dạng tổ hợp tuyến tính của $55$ và $80$: $55 \cdot 3 + 80 \cdot (-2) = 5$.

Một dạng tổng quát hơn của bài toán này được trình bày trong bài [Phương trình Diophantine tuyến tính](linear-diophantine-equation.md).
Bài đó sẽ xây dựng dựa trên thuật toán này.

## Thuật toán

Trong phần này, ta ký hiệu UCLN của $a$ và $b$ là $g$.

Những thay đổi so với thuật toán gốc rất đơn giản.
Nếu nhớ lại thuật toán Euclid, ta thấy thuật toán kết thúc khi $b = 0$ và $a = g$.
Với các tham số này, ta dễ dàng tìm được các hệ số: $g \cdot 1 + 0 \cdot 0 = g$.

Bắt đầu từ các hệ số $(x, y) = (1, 0)$, ta có thể đi ngược lên qua các lời gọi đệ quy.
Ta chỉ cần xác định cách các hệ số $x$ và $y$ thay đổi khi chuyển từ $(a, b)$ sang $(b, a \bmod b)$.

Giả sử ta đã tìm được các hệ số $(x_1, y_1)$ cho $(b, a \bmod b)$:

$$b \cdot x_1 + (a \bmod b) \cdot y_1 = g$$

và muốn tìm cặp $(x, y)$ cho $(a, b)$:

$$ a \cdot x + b \cdot y = g$$

Ta có thể biểu diễn $a \bmod b$ dưới dạng:

$$ a \bmod b = a - \left\lfloor \frac{a}{b} \right\rfloor \cdot b$$

Thay biểu thức này vào phương trình hệ số của $(x_1, y_1)$, ta được:

$$ g = b \cdot x_1 + (a \bmod b) \cdot y_1 = b \cdot x_1 + \left(a - \left\lfloor \frac{a}{b} \right\rfloor \cdot b \right) \cdot y_1$$

và sau khi sắp xếp lại các hạng tử:

$$g = a \cdot y_1 + b \cdot \left( x_1 - y_1 \cdot \left\lfloor \frac{a}{b} \right\rfloor \right)$$

Ta tìm được các giá trị của $x$ và $y$:

$$\begin{cases}
x = y_1 \\
y = x_1 - y_1 \cdot \left\lfloor \frac{a}{b} \right\rfloor
\end{cases} $$

## Cài đặt

```{.cpp file=extended_gcd}
int gcd(int a, int b, int& x, int& y) {
    if (b == 0) {
        x = 1;
        y = 0;
        return a;
    }
    int x1, y1;
    int d = gcd(b, a % b, x1, y1);
    x = y1;
    y = x1 - y1 * (a / b);
    return d;
}
```

Hàm đệ quy trên trả về UCLN cùng các giá trị hệ số qua `x` và `y` (được truyền vào hàm bằng tham chiếu).

Cài đặt thuật toán Euclid mở rộng này cũng cho kết quả đúng với các số nguyên âm.

## Phiên bản lặp

Ta cũng có thể viết thuật toán Euclid mở rộng theo cách lặp.
Do tránh được đệ quy, đoạn code này sẽ chạy nhanh hơn một chút so với phiên bản đệ quy.

```{.cpp file=extended_gcd_iter}
int gcd(int a, int b, int& x, int& y) {
    x = 1, y = 0;
    int x1 = 0, y1 = 1, a1 = a, b1 = b;
    while (b1) {
        int q = a1 / b1;
        tie(x, x1) = make_tuple(x1, x - q * x1);
        tie(y, y1) = make_tuple(y1, y - q * y1);
        tie(a1, b1) = make_tuple(b1, a1 - q * b1);
    }
    return a1;
}
```

Nếu quan sát kỹ các biến `a1` và `b1`, ta thấy chúng nhận chính xác những giá trị như trong phiên bản lặp của [thuật toán Euclid](euclid-algorithm.md#implementation) thông thường. Vì vậy ít nhất thuật toán sẽ tính đúng UCLN.

Để thấy vì sao thuật toán cũng tính đúng các hệ số, xét các bất biến sau, vốn đúng tại mọi thời điểm (trước khi vòng lặp while bắt đầu và ở cuối mỗi lần lặp):

$$x \cdot a + y \cdot b = a_1$$

$$x_1 \cdot a + y_1 \cdot b = b_1$$

Gọi các giá trị ở cuối một lần lặp bằng ký hiệu phẩy ($'$), và giả sử $q = \frac{a_1}{b_1}$. Từ [thuật toán Euclid](euclid-algorithm.md), ta có:

$$a_1' = b_1$$

$$b_1' = a_1 - q \cdot b_1$$

Để bất biến thứ nhất tiếp tục đúng, ta cần:

$$x' \cdot a + y' \cdot b = a_1' = b_1$$

$$x' \cdot a + y' \cdot b = x_1 \cdot a + y_1 \cdot b$$

Tương tự, với bất biến thứ hai ta cần:

$$x_1' \cdot a + y_1' \cdot b = a_1 - q \cdot b_1$$

$$x_1' \cdot a + y_1' \cdot b = (x - q \cdot x_1) \cdot a + (y - q \cdot y_1) \cdot b$$

Bằng cách so sánh các hệ số của $a$ và $b$, ta suy ra các công thức cập nhật cho từng biến, từ đó bảo đảm các bất biến được duy trì trong suốt thuật toán.

Cuối cùng, ta biết $a_1$ chứa UCLN, nên $x \cdot a + y \cdot b = g$.
Điều đó có nghĩa ta đã tìm được các hệ số cần thiết.

Ta thậm chí có thể tối ưu code thêm bằng cách loại bỏ các biến $a_1$ và $b_1$, rồi dùng lại trực tiếp $a$ và $b$.
Tuy nhiên, nếu làm vậy ta sẽ mất cách lập luận bằng các bất biến ở trên.

## Bài tập luyện tập

* [UVA - 10104 - Euclid Problem](https://uva.onlinejudge.org/index.php?option=com_onlinejudge&Itemid=8&page=show_problem&problem=1045)
* [GYM - (J) Once Upon A Time](http://codeforces.com/gym/100963)
* [UVA - 12775 - Gift Dilemma](https://uva.onlinejudge.org/index.php?option=com_onlinejudge&Itemid=8&page=show_problem&problem=4628)
