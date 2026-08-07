---
tags:
  - Translated
e_maxx_link: reverse_element
translation:
  source: algebra/module-inverse.md
  source_commit: 2cea59afbd60bb513aa5612b162ca5e22b916c2b
  status: draft
  last_synced: 2026-08-07
---

# Nghịch đảo nhân mô-đun

## Định nghĩa

[Nghịch đảo nhân mô-đun](http://en.wikipedia.org/wiki/Modular_multiplicative_inverse) của một số nguyên $a$ là một số nguyên $x$ sao cho $a \cdot x$ đồng dư với $1$ theo một mô-đun $m$ nào đó.
Viết một cách hình thức, ta muốn tìm số nguyên $x$ sao cho

$$a \cdot x \equiv 1 \mod m.$$

Ta cũng ký hiệu $x$ đơn giản là $a^{-1}$.

Cần lưu ý rằng nghịch đảo mô-đun không phải lúc nào cũng tồn tại. Chẳng hạn, lấy $m = 4$, $a = 2$.
Bằng cách kiểm tra mọi giá trị có thể theo mô-đun $m$, ta sẽ thấy không thể tìm được $a^{-1}$ thỏa mãn phương trình trên.
Có thể chứng minh nghịch đảo mô-đun tồn tại khi và chỉ khi $a$ và $m$ nguyên tố cùng nhau, tức $\gcd(a, m) = 1$.

Trong bài này, ta trình bày hai phương pháp tìm nghịch đảo mô-đun khi nó tồn tại, cùng một phương pháp tìm nghịch đảo mô-đun cho mọi số trong thời gian tuyến tính.

## Tìm nghịch đảo mô-đun bằng thuật toán Euclid mở rộng

Xét phương trình sau với hai ẩn $x$ và $y$:

$$a \cdot x + m \cdot y = 1$$

Đây là một [phương trình Diophantine tuyến tính hai ẩn](linear-diophantine-equation.md).
Như trình bày trong bài được liên kết, khi $\gcd(a, m) = 1$, phương trình có nghiệm và có thể tìm nghiệm bằng [thuật toán Euclid mở rộng](extended-euclid-algorithm.md).
Lưu ý rằng $\gcd(a, m) = 1$ cũng chính là điều kiện để nghịch đảo mô-đun tồn tại.

Bây giờ, nếu lấy hai vế theo mô-đun $m$, hạng tử $m \cdot y$ biến mất và phương trình trở thành:

$$a \cdot x \equiv 1 \mod m$$

Do đó nghịch đảo mô-đun của $a$ chính là $x$.

Cài đặt như sau:

```cpp
int x, y;
int g = extended_euclidean(a, m, x, y);
if (g != 1) {
    cout << "No solution!";
}
else {
    x = (x % m + m) % m;
    cout << x << endl;
}
```

Hãy chú ý cách ta điều chỉnh `x`.
Giá trị `x` thu được từ thuật toán Euclid mở rộng có thể âm, nên `x % m` cũng có thể âm; vì vậy trước hết ta phải cộng `m` để đưa nó về giá trị dương.

<div id="fermat-euler"></div>
## Tìm nghịch đảo mô-đun bằng lũy thừa nhị phân

Một cách khác để tìm nghịch đảo mô-đun là dùng định lý Euler, phát biểu rằng đồng dư sau đúng khi $a$ và $m$ nguyên tố cùng nhau:

$$a^{\phi (m)} \equiv 1 \mod m$$

$\phi$ là [hàm phi Euler](phi-function.md).
Một lần nữa, điều kiện $a$ và $m$ nguyên tố cùng nhau cũng chính là điều kiện để nghịch đảo mô-đun tồn tại.

Nếu $m$ là số nguyên tố, công thức rút gọn thành [định lý nhỏ Fermat](http://en.wikipedia.org/wiki/Fermat's_little_theorem):

$$a^{m - 1} \equiv 1 \mod m$$

Nhân cả hai vế của các phương trình trên với $a^{-1}$, ta được:

* Với mô-đun $m$ bất kỳ nhưng nguyên tố cùng nhau với $a$: $a ^ {\phi (m) - 1} \equiv a ^{-1} \mod m$
* Với mô-đun nguyên tố $m$: $a ^ {m - 2} \equiv a ^ {-1} \mod m$

Từ các kết quả này, ta dễ dàng tìm nghịch đảo mô-đun bằng [thuật toán lũy thừa nhị phân](binary-exp.md), chạy trong $O(\log m)$.

Mặc dù phương pháp này dễ hiểu hơn phương pháp ở phần trước, khi $m$ không phải số nguyên tố ta cần tính hàm phi Euler, việc này đòi hỏi phân tích $m$ ra thừa số nguyên tố và có thể rất khó. Nếu đã biết phân tích thừa số nguyên tố của $m$, độ phức tạp của phương pháp này là $O(\log m)$.

<div id="finding-the-modular-inverse-using-euclidean-division"></div>
## Tìm nghịch đảo mô-đun với mô-đun nguyên tố bằng phép chia Euclid

Cho mô-đun nguyên tố $m > a$ (hoặc ta có thể lấy modulo để làm $a$ nhỏ hơn trong một bước). Theo [phép chia Euclid](https://en.wikipedia.org/wiki/Euclidean_division),

$$m = k \cdot a + r$$

trong đó $k = \left\lfloor \frac{m}{a} \right\rfloor$ và $r = m \bmod a$, khi đó

$$
\begin{align*}
& \implies & 0          & \equiv k \cdot a + r   & \mod m \\
& \iff & r              & \equiv -k \cdot a      & \mod m \\
& \iff & r \cdot a^{-1} & \equiv -k              & \mod m \\
& \iff & a^{-1}         & \equiv -k \cdot r^{-1} & \mod m
\end{align*}
$$

Lưu ý rằng lập luận này không đúng khi $m$ không nguyên tố, vì trong trường hợp tổng quát việc $a^{-1}$ tồn tại không kéo theo $r^{-1}$ tồn tại.
Để thấy điều này, thử tính $5^{-1}$ theo mô-đun $12$ bằng công thức trên. Ta mong nhận được $5$, vì $5 \cdot 5 \equiv 1 \bmod 12$. Tuy nhiên, $12 = 2 \cdot 5 + 2$, nên $k=2$ và $r=2$, trong khi $2$ không khả nghịch theo mô-đun $12$.

Nếu mô-đun là số nguyên tố thì mọi $a$ với $0 < a < m$ đều khả nghịch theo mô-đun $m$, và ta có thể dùng hàm đệ quy C++ sau để tính nghịch đảo mô-đun của số $a$ theo $m$:

```{.cpp file=modular_inverse_euclidean_division}
int inv(int a) {
  return a <= 1 ? a : m - (long long)(m/a) * inv(m % a) % m;
}
```

Độ phức tạp thời gian chính xác của phép đệ quy này chưa được biết. Nó nằm đâu đó giữa $O(\frac{\log m}{\log\log m})$ và $O(m^{\frac{1}{3} - \frac{2}{177} + \epsilon})$.
Xem [On the length of Pierce expansions](https://arxiv.org/abs/2211.08374).
Trong thực tế, cài đặt này rất nhanh; chẳng hạn với mô-đun $10^9 + 7$, nó luôn kết thúc trong ít hơn 50 lần lặp.

<div id="mod-inv-all-num"></div>
Áp dụng công thức này, ta cũng có thể tính trước nghịch đảo mô-đun cho mọi số trong khoảng $[1, m-1]$ trong $O(m)$.

```{.cpp file=modular_inverse_euclidean_division_all}
inv[1] = 1;
for(int a = 2; a < m; ++a)
    inv[a] = m - (long long)(m/a) * inv[m%a] % m;
```

## Tìm nghịch đảo mô-đun cho một mảng số theo mô-đun $m$

Giả sử ta có một mảng và muốn tìm nghịch đảo mô-đun của mọi số trong đó, với giả thiết tất cả đều khả nghịch.
Thay vì tính nghịch đảo cho từng số, ta có thể mở rộng phân số bằng tích tiền tố (không gồm chính nó) và tích hậu tố (không gồm chính nó), nhờ đó cuối cùng chỉ cần tính đúng một nghịch đảo.

$$
\begin{align}
x_i^{-1} &= \frac{1}{x_i} = \frac{\overbrace{x_1 \cdot x_2 \cdots x_{i-1}}^{\text{prefix}_{i-1}} \cdot ~1~ \cdot \overbrace{x_{i+1} \cdot x_{i+2} \cdots x_n}^{\text{suffix}_{i+1}}}{x_1 \cdot x_2 \cdots x_{i-1} \cdot x_i \cdot x_{i+1} \cdot x_{i+2} \cdots x_n} \\
&= \text{prefix}_{i-1} \cdot \text{suffix}_{i+1} \cdot \left(x_1 \cdot x_2 \cdots x_n\right)^{-1}
\end{align}
$$

Trong code, ta chỉ cần tạo một mảng tích tiền tố (không gồm chính phần tử đó, bắt đầu từ phần tử đơn vị), tính nghịch đảo mô-đun của tích tất cả các số rồi nhân nó với tích tiền tố và tích hậu tố tương ứng (không gồm chính phần tử đó).
Tích hậu tố được tính bằng cách duyệt từ cuối mảng về đầu.

```cpp
std::vector<int> invs(const std::vector<int> &a, int m) {
    int n = a.size();
    if (n == 0) return {};
    std::vector<int> b(n);
    int v = 1;
    for (int i = 0; i != n; ++i) {
        b[i] = v;
        v = static_cast<long long>(v) * a[i] % m;
    }
    int x, y;
    extended_euclidean(v, m, x, y);
    x = (x % m + m) % m;
    for (int i = n - 1; i >= 0; --i) {
        b[i] = static_cast<long long>(x) * b[i] % m;
        x = static_cast<long long>(x) * a[i] % m;
    }
    return b;
}
```

## Bài tập luyện tập

* [UVa 11904 - One Unit Machine](https://uva.onlinejudge.org/index.php?option=com_onlinejudge&Itemid=8&page=show_problem&problem=3055)
* [Hackerrank - Longest Increasing Subsequence Arrays](https://www.hackerrank.com/contests/world-codesprint-5/challenges/longest-increasing-subsequence-arrays)
* [Codeforces 300C - Beautiful Numbers](http://codeforces.com/problemset/problem/300/C)
* [Codeforces 622F - The Sum of the k-th Powers](http://codeforces.com/problemset/problem/622/F)
* [Codeforces 717A - Festival Organization](http://codeforces.com/problemset/problem/717/A)
* [Codeforces 896D - Nephren Runs a Cinema](http://codeforces.com/problemset/problem/896/D)
