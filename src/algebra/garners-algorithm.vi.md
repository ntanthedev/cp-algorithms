---
translation:
  source: algebra/garners-algorithm.md
  source_commit: 4e435ebd89fa31b09b20fd9afac713e8b45397c3
  status: draft
  last_synced: 2026-11-16
---

# Thuật toán Garner

Một hệ quả của [Định lý phần dư Trung Hoa](chinese-remainder-theorem.md) là ta có thể biểu diễn các số lớn bằng một mảng số nguyên nhỏ.
Ví dụ, gọi $p$ là tích của $1000$ số nguyên tố đầu tiên. $p$ có khoảng $3000$ chữ số.

Mọi số $a$ nhỏ hơn $p$ đều có thể biểu diễn bằng mảng $a_1, \ldots, a_k$, trong đó $a_i \equiv a \pmod{p_i}$.
Tuy nhiên, để làm được điều này, ta cần biết cách khôi phục số $a$ từ biểu diễn đó.
Một cách được trình bày trong bài về Định lý phần dư Trung Hoa.

Trong bài này, ta xét một cách khác cũng có thể dùng để khôi phục số: thuật toán Garner.

## Biểu diễn cơ số hỗn hợp

Ta có thể biểu diễn số $a$ dưới dạng **cơ số hỗn hợp**:

$$a = x_1 + x_2 p_1 + x_3 p_1 p_2 + \ldots + x_k p_1 \cdots p_{k-1} \text{ with }x_i \in [0, p_i)$$

Biểu diễn cơ số hỗn hợp là một hệ đếm theo vị trí, tổng quát hóa các hệ đếm quen thuộc như hệ nhị phân và hệ thập phân.
Chẳng hạn, hệ thập phân là hệ đếm theo vị trí với cơ số 10.
Mỗi số được biểu diễn bằng một dãy chữ số $d_1 d_2 d_3 \dots d_n$ từ $0$ đến $9$. Ví dụ, dãy $415$ biểu diễn số $4 \cdot 10^2 + 1 \cdot 10^1 + 5 \cdot 10^0$.
Tổng quát, dãy chữ số $d_1 d_2 d_3 \dots d_n$ biểu diễn số $d_1 b^{n-1} + d_2 b^{n-2} + \cdots + d_n b^0$ trong hệ đếm theo vị trí với cơ số $b$.

Trong hệ cơ số hỗn hợp, ta không còn dùng một cơ số duy nhất. Cơ số thay đổi theo từng vị trí.

## Thuật toán Garner

Thuật toán Garner tính các chữ số $x_1, \ldots, x_k$.
Lưu ý rằng các chữ số này tương đối nhỏ.
Chữ số $x_i$ là một số nguyên từ $0$ đến $p_i - 1$.

Gọi $r_{ij}$ là nghịch đảo của $p_i$ theo modulo $p_j$

$$r_{ij} = (p_i)^{-1} \pmod{p_j}$$

Ta có thể tìm giá trị này bằng thuật toán trong bài [Nghịch đảo modulo](module-inverse.md).

Thay biểu diễn cơ số hỗn hợp của $a$ vào phương trình đồng dư thứ nhất, ta được

$$a_1 \equiv x_1 \pmod{p_1}.$$

Thay vào phương trình thứ hai, ta được

$$a_2 \equiv x_1 + x_2 p_1 \pmod{p_2},$$

trừ $x_1$ rồi chia cho $p_1$ cho ta

$$\begin{array}{rclr}
    a_2 - x_1 &\equiv& x_2 p_1 &\pmod{p_2} \\
    (a_2 - x_1) r_{12} &\equiv& x_2 &\pmod{p_2} \\
    x_2 &\equiv& (a_2 - x_1) r_{12} &\pmod{p_2}
\end{array}$$

Tương tự, ta được

$$x_3 \equiv ((a_3 - x_1) r_{13} - x_2) r_{23} \pmod{p_3}.$$

Ta có thể thấy quy luật và biểu diễn nó bằng đoạn mã sau:

```cpp
for (int i = 0; i < k; ++i) {
    x[i] = a[i];
    for (int j = 0; j < i; ++j) {
        x[i] = r[j][i] * (x[i] - x[j]);

        x[i] = x[i] % p[i];
        if (x[i] < 0)
            x[i] += p[i];
    }
}
```

Như vậy ta đã tính được các chữ số $x_i$ trong thời gian $O(k^2)$. Giờ có thể tính số $a$ bằng công thức đã nêu

$$a = x_1 + x_2 \cdot p_1 + x_3 \cdot p_1 \cdot p_2 + \ldots + x_k \cdot p_1 \cdots p_{k-1}$$

Trong thực tế, gần như chắc chắn ta phải dùng [số học độ chính xác tùy ý](big-integer.md) để tính kết quả $a$. Tuy nhiên, các chữ số $x_i$ thường tính được bằng kiểu dữ liệu có sẵn vì chúng nhỏ, do đó thuật toán Garner rất hiệu quả.

## Cài đặt thuật toán Garner

Java thuận tiện để cài đặt thuật toán này vì hỗ trợ số lớn thông qua lớp `BigInteger`.

Dưới đây là một cài đặt lưu số lớn dưới dạng một hệ phương trình đồng dư.
Cài đặt hỗ trợ phép cộng, trừ và nhân.
Ta có thể dùng thuật toán Garner để chuyển hệ phương trình thành số nguyên duy nhất tương ứng.
Trong mã này, ta dùng 100 số nguyên tố lớn hơn $10^9$, cho phép biểu diễn các số lớn tới $10^{900}$.

```java
final int SZ = 100;
int pr[] = new int[SZ];
int r[][] = new int[SZ][SZ];

void init() {
    for (int x = 1000 * 1000 * 1000, i = 0; i < SZ; ++x)
        if (BigInteger.valueOf(x).isProbablePrime(100))
            pr[i++] = x;

    for (int i = 0; i < SZ; ++i)
        for (int j = i + 1; j < SZ; ++j)
            r[i][j] =
                BigInteger.valueOf(pr[i]).modInverse(BigInteger.valueOf(pr[j])).intValue();
}

class Number {
    int a[] = new int[SZ];

    public Number() {
    }

    public Number(int n) {
        for (int i = 0; i < SZ; ++i)
            a[i] = n % pr[i];
    }

    public Number(BigInteger n) {
        for (int i = 0; i < SZ; ++i)
            a[i] = n.mod(BigInteger.valueOf(pr[i])).intValue();
    }

    public Number add(Number n) {
        Number result = new Number();
        for (int i = 0; i < SZ; ++i)
            result.a[i] = (a[i] + n.a[i]) % pr[i];
        return result;
    }

    public Number subtract(Number n) {
        Number result = new Number();
        for (int i = 0; i < SZ; ++i)
            result.a[i] = (a[i] - n.a[i] + pr[i]) % pr[i];
        return result;
    }

    public Number multiply(Number n) {
        Number result = new Number();
        for (int i = 0; i < SZ; ++i)
            result.a[i] = (int)((a[i] * 1l * n.a[i]) % pr[i]);
        return result;
    }

    public BigInteger bigIntegerValue(boolean can_be_negative) {
        BigInteger result = BigInteger.ZERO, mult = BigInteger.ONE;
        int x[] = new int[SZ];
        for (int i = 0; i < SZ; ++i) {
            x[i] = a[i];
            for (int j = 0; j < i; ++j) {
                long cur = (x[i] - x[j]) * 1l * r[j][i];
                x[i] = (int)((cur % pr[i] + pr[i]) % pr[i]);
            }
            result = result.add(mult.multiply(BigInteger.valueOf(x[i])));
            mult = mult.multiply(BigInteger.valueOf(pr[i]));
        }

        if (can_be_negative)
            if (result.compareTo(mult.shiftRight(1)) >= 0)
                result = result.subtract(mult);

        return result;
    }
}
```

**Ghi chú bản dịch:** Hệ các số dư chỉ xác định số nguyên theo modulo tích các số nguyên tố; để có đại diện duy nhất không âm, cần xét số từ 0 đến nhỏ hơn tích đó. Trong mã Java, phép lấy dư với số nguyên âm không được chuẩn hóa: ví dụ khởi tạo từ âm một rồi khôi phục ở chế độ không âm cho kết quả âm một thay vì đại diện không âm tương ứng.
