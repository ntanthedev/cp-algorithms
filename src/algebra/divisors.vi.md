---
tags:
  - Original
translation:
  source: algebra/divisors.md
  source_commit: b426a91f0cab0ac4f1a4836fd90235304c306681
  status: draft
  last_synced: 2026-08-09
---

# Số các ước và tổng các ước

Trong bài viết này, ta sẽ tìm hiểu cách tính số các ước $d(n)$ và tổng các ước $\sigma(n)$ của một số $n$ cho trước.

## Số các ước

Dễ thấy rằng phân tích thừa số nguyên tố của một ước $d$ phải là một phần của phân tích thừa số nguyên tố của $n$; chẳng hạn $6 = 2 \cdot 3$ là một ước của $60 = 2^2 \cdot 3 \cdot 5$.
Vì vậy, ta chỉ cần xét tất cả các cách chọn khác nhau từ phân tích thừa số nguyên tố của $n$.

Thông thường, một tập có $x$ phần tử có $2^x$ tập con.
Tuy nhiên, điều này không còn đúng nếu trong tập có các phần tử lặp lại. Trong trường hợp của ta, một số thừa số nguyên tố có thể xuất hiện nhiều lần trong phân tích thừa số nguyên tố của $n$.

**Ghi chú bản dịch:** Nguồn gọi cấu trúc đang xét là một tập hợp rồi nói rằng nó có thể chứa phần tử lặp. Về mặt toán học, khi cần giữ cả số lần một thừa số xuất hiện, cách gọi chính xác hơn là đa tập.

Nếu một thừa số nguyên tố $p$ xuất hiện $e$ lần trong phân tích thừa số nguyên tố của $n$, ta có thể dùng thừa số $p$ từ 0 đến $e$ lần khi chọn.
Do đó, ta có $e+1$ lựa chọn.

Vì thế, nếu phân tích thừa số nguyên tố của $n$ là $p_1^{e_1} \cdot p_2^{e_2} \cdots p_k^{e_k}$, trong đó $p_i$ là các số nguyên tố đôi một khác nhau, thì số các ước là:

$$d(n) = (e_1 + 1) \cdot (e_2 + 1) \cdots (e_k + 1)$$

Có thể hình dung như sau:

* Nếu chỉ có một ước nguyên tố phân biệt $n = p_1^{e_1}$, thì hiển nhiên có $e_1 + 1$ ước ($1, p_1, p_1^2, \dots, p_1^{e_1}$).

* Nếu có hai ước nguyên tố phân biệt $n = p_1^{e_1} \cdot p_2^{e_2}$, ta có thể sắp xếp tất cả các ước thành một bảng.

$$\begin{array}{c|ccccc}
& 1 & p_2 & p_2^2 & \dots & p_2^{e_2} \\\\\hline
1 & 1 & p_2 & p_2^2 & \dots & p_2^{e_2} \\\\
p_1 & p_1 & p_1 \cdot p_2 & p_1 \cdot p_2^2 & \dots & p_1 \cdot p_2^{e_2} \\\\
p_1^2 & p_1^2 & p_1^2 \cdot p_2 & p_1^2 \cdot p_2^2 & \dots & p_1^2 \cdot p_2^{e_2} \\\\
\vdots & \vdots & \vdots & \vdots & \ddots & \vdots \\\\
p_1^{e_1} & p_1^{e_1} & p_1^{e_1} \cdot p_2 & p_1^{e_1} \cdot p_2^2 & \dots & p_1^{e_1} \cdot p_2^{e_2} \\\\
\end{array}$$

Do đó, số các ước hiển nhiên là $(e_1 + 1) \cdot (e_2 + 1)$.

* Có thể lập luận tương tự khi có nhiều hơn hai thừa số nguyên tố phân biệt.


```cpp
long long numberOfDivisors(long long num) {
    long long total = 1;
    for (int i = 2; (long long)i * i <= num; i++) {
        if (num % i == 0) {
            int e = 0;
            do {
                e++;
                num /= i;
            } while (num % i == 0);
            total *= e + 1;
        }
    }
    if (num > 1) {
        total *= 2;
    }
    return total;
}
```

## Tổng các ước

Ta có thể dùng lập luận tương tự như ở phần trước.

* Nếu chỉ có một ước nguyên tố phân biệt $n = p_1^{e_1}$, thì tổng là:

$$1 + p_1 + p_1^2 + \dots + p_1^{e_1} = \frac{p_1^{e_1 + 1} - 1}{p_1 - 1}$$

* Nếu có hai ước nguyên tố phân biệt $n = p_1^{e_1} \cdot p_2^{e_2}$, ta có thể lập bảng giống như trước.
  Điểm khác biệt duy nhất là bây giờ ta muốn tính tổng thay vì đếm số phần tử.
  Dễ thấy tổng của tất cả các tổ hợp có thể được biểu diễn thành:

$$\left(1 + p_1 + p_1^2 + \dots + p_1^{e_1}\right) \cdot \left(1 + p_2 + p_2^2 + \dots + p_2^{e_2}\right)$$

$$ = \frac{p_1^{e_1 + 1} - 1}{p_1 - 1} \cdot \frac{p_2^{e_2 + 1} - 1}{p_2 - 1}$$

* Tổng quát, với $n = p_1^{e_1} \cdot p_2^{e_2} \cdots p_k^{e_k}$, ta thu được công thức:

$$\sigma(n) = \frac{p_1^{e_1 + 1} - 1}{p_1 - 1} \cdot \frac{p_2^{e_2 + 1} - 1}{p_2 - 1} \cdots \frac{p_k^{e_k + 1} - 1}{p_k - 1}$$

```cpp
long long SumOfDivisors(long long num) {
    long long total = 1;

    for (int i = 2; (long long)i * i <= num; i++) {
        if (num % i == 0) {
            int e = 0;
            do {
                e++;
                num /= i;
            } while (num % i == 0);

            long long sum = 0, pow = 1;
            do {
                sum += pow;
                pow *= i;
            } while (e-- > 0);
            total *= sum;
        }
    }
    if (num > 1) {
        total *= (1 + num);
    }
    return total;
}
```

## Hàm nhân tính

Hàm nhân tính là một hàm $f(x)$ thỏa mãn

$$f(a \cdot b) = f(a) \cdot f(b)$$

khi $a$ và $b$ nguyên tố cùng nhau.

Cả $d(n)$ và $\sigma(n)$ đều là các hàm nhân tính.

Hàm nhân tính có rất nhiều tính chất thú vị và có thể đặc biệt hữu ích trong các bài toán số học.
Chẳng hạn, tích chập Dirichlet của hai hàm nhân tính cũng là một hàm nhân tính.

## Bài tập luyện tập

  - [SPOJ - COMDIV](https://www.spoj.com/problems/COMDIV/)
  - [SPOJ - DIVSUM](https://www.spoj.com/problems/DIVSUM/)
  - [SPOJ - DIVSUM2](https://www.spoj.com/problems/DIVSUM2/)
