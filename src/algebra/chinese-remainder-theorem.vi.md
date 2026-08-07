---
tags:
  - Translated
e_maxx_link: chinese_theorem
translation:
  source: algebra/chinese-remainder-theorem.md
  source_commit: 5fb6b73fe4ef5605bc9064b41bc8fb845a9ca617
  status: draft
  last_synced: 2026-08-07
---

# Định lý Thặng dư Trung Hoa

Định lý Thặng dư Trung Hoa (Chinese Remainder Theorem, viết tắt là CRT trong phần còn lại của bài; cũng thường được gọi là Định lý số dư Trung Hoa) được phát hiện bởi nhà toán học Trung Quốc Tôn Tử (Sun Zi).

## Phát biểu

Gọi $m = m_1 \cdot m_2 \cdots m_k$, trong đó các $m_i$ đôi một nguyên tố cùng nhau. Ngoài các $m_i$, ta còn được cho một hệ đồng dư

$$\left\{\begin{array}{rcl}
    a & \equiv & a_1 \pmod{m_1} \\
    a & \equiv & a_2 \pmod{m_2} \\
      & \vdots & \\
    a & \equiv & a_k \pmod{m_k}
\end{array}\right.$$

trong đó $a_i$ là các hằng số đã cho. Dạng cổ điển của CRT khẳng định hệ đồng dư này luôn có *một và chỉ một* nghiệm theo mô-đun $m$.

Ví dụ, hệ đồng dư

$$\left\{\begin{array}{rcl}
    a & \equiv & 2 \pmod{3} \\
    a & \equiv & 3 \pmod{5} \\
    a & \equiv & 2 \pmod{7}
\end{array}\right.$$

có nghiệm $23$ theo mô-đun $105$, vì $23 \bmod{3} = 2$, $23 \bmod{5} = 3$, và $23 \bmod{7} = 2$.
Ta có thể viết mọi nghiệm dưới dạng $23 + 105\cdot k$ với $k \in \mathbb{Z}$.


### Hệ quả

Một hệ quả của CRT là phương trình

$$x \equiv a \pmod{m}$$

tương đương với hệ phương trình

$$\left\{\begin{array}{rcl}
    x & \equiv & a_1 \pmod{m_1} \\
      & \vdots & \\
    x & \equiv & a_k \pmod{m_k}
\end{array}\right.$$

(Như trên, giả sử $m = m_1 m_2 \cdots m_k$ và các $m_i$ đôi một nguyên tố cùng nhau.)

## Lời giải cho hai mô-đun

Xét hệ hai phương trình với $m_1, m_2$ nguyên tố cùng nhau:

$$
\left\{\begin{align}
    a &\equiv a_1 \pmod{m_1} \\
    a &\equiv a_2 \pmod{m_2} \\
\end{align}\right.
$$

Ta muốn tìm nghiệm $a \pmod{m_1 m_2}$. Dùng [thuật toán Euclid mở rộng](extended-euclid-algorithm.md), ta tìm được các hệ số Bézout $n_1, n_2$ sao cho

$$n_1 m_1 + n_2 m_2 = 1.$$

Thực tế, $n_1$ và $n_2$ chính là các [nghịch đảo mô-đun](module-inverse.md) của $m_1$ và $m_2$ theo mô-đun $m_2$ và $m_1$ tương ứng.
Ta có $n_1 m_1 \equiv 1 \pmod{m_2}$ nên $n_1 \equiv m_1^{-1} \pmod{m_2}$, và tương tự $n_2 \equiv m_2^{-1} \pmod{m_1}$.

Với hai hệ số này, ta có thể xác định một nghiệm:

$$a = a_1 n_2 m_2 + a_2 n_1 m_1 \bmod{m_1 m_2}$$

Dễ kiểm tra đây thực sự là nghiệm bằng cách tính $a \bmod{m_1}$ và $a \bmod{m_2}$.

$$
\begin{array}{rcll}
a & \equiv & a_1 n_2 m_2 + a_2 n_1 m_1 & \pmod{m_1}\\
  & \equiv & a_1 (1 - n_1 m_1) + a_2 n_1 m_1 & \pmod{m_1}\\
  & \equiv & a_1 - a_1 n_1 m_1 + a_2 n_1 m_1 & \pmod{m_1}\\
  & \equiv & a_1 & \pmod{m_1}
\end{array}
$$

Lưu ý rằng Định lý Thặng dư Trung Hoa còn bảo đảm chỉ tồn tại một nghiệm theo mô-đun $m_1 m_2$.
Điều này cũng dễ chứng minh.

Giả sử có hai nghiệm khác nhau $x$ và $y$.
Vì $x \equiv a_i \pmod{m_i}$ và $y \equiv a_i \pmod{m_i}$, suy ra $x − y \equiv 0 \pmod{m_i}$, do đó $x − y \equiv 0 \pmod{m_1 m_2}$, hay tương đương $x \equiv y \pmod{m_1 m_2}$.
Vậy $x$ và $y$ thực chất là cùng một nghiệm.

## Lời giải cho trường hợp tổng quát

### Lời giải quy nạp

Vì $m_1 m_2$ nguyên tố cùng nhau với $m_3$, ta có thể lặp lại lời giải cho hai mô-đun theo quy nạp với số lượng mô-đun bất kỳ.
Đầu tiên tính $b_2 := a \pmod{m_1 m_2}$ từ hai đồng dư đầu tiên,
sau đó tính $b_3 := a \pmod{m_1 m_2 m_3}$ bằng hai đồng dư $a \equiv b_2 \pmod{m_1 m_2}$ và $a \equiv a_3 \pmod {m_3}$, rồi tiếp tục tương tự.

### Xây dựng trực tiếp

Có thể xây dựng nghiệm trực tiếp theo cách tương tự nội suy Lagrange.

Gọi $M_i := \prod_{i \neq j} m_j$, là tích của mọi mô-đun trừ $m_i$, và $N_i$ là nghịch đảo mô-đun $N_i := M_i^{-1} \bmod{m_i}$.

**Ghi chú bản dịch:** Ký hiệu tích trong nguồn được viết là $\prod_{i \neq j} m_j$; ý nghĩa theo câu văn và các công thức phía sau là lấy tích trên mọi chỉ số $j \neq i$.

Khi đó một nghiệm của hệ đồng dư là:

$$a \equiv \sum_{i=1}^k a_i M_i N_i \pmod{m_1 m_2 \cdots m_k}$$

Ta kiểm tra đây là nghiệm bằng cách tính $a \bmod{m_i}$ với mọi $i$.
Vì $M_j$ là bội của $m_i$ khi $i \neq j$, ta có

$$\begin{array}{rcll}
a & \equiv & \sum_{j=1}^k a_j M_j N_j & \pmod{m_i} \\
  & \equiv & a_i M_i N_i              & \pmod{m_i} \\
  & \equiv & a_i M_i M_i^{-1}         & \pmod{m_i} \\
  & \equiv & a_i                      & \pmod{m_i}
\end{array}$$

### Cài đặt

```{.cpp file=chinese_remainder_theorem}
struct Congruence {
    long long a, m;
};

long long chinese_remainder_theorem(vector<Congruence> const& congruences) {
    long long M = 1;
    for (auto const& congruence : congruences) {
        M *= congruence.m;
    }

    long long solution = 0;
    for (auto const& congruence : congruences) {
        long long a_i = congruence.a;
        long long M_i = M / congruence.m;
        long long N_i = mod_inv(M_i, congruence.m);
        solution = (solution + a_i * M_i % M * N_i) % M;
    }
    return solution;
}
```

## Lời giải khi các mô-đun không nguyên tố cùng nhau

Như đã nói, thuật toán trên chỉ hoạt động khi các mô-đun $m_1, m_2, \dots m_k$ nguyên tố cùng nhau.

Trong trường hợp không nguyên tố cùng nhau, một hệ đồng dư hoặc có đúng một nghiệm theo mô-đun $\text{lcm}(m_1, m_2, \dots, m_k)$, hoặc hoàn toàn không có nghiệm.

Ví dụ, trong hệ sau, đồng dư thứ nhất yêu cầu nghiệm là số lẻ, còn đồng dư thứ hai yêu cầu nghiệm là số chẵn.
Một số không thể đồng thời vừa lẻ vừa chẵn, nên rõ ràng hệ không có nghiệm.

$$\left\{\begin{align}
    a & \equiv 1 \pmod{4} \\
    a & \equiv 2 \pmod{6}
\end{align}\right.$$

Việc xác định hệ có nghiệm hay không khá đơn giản.
Nếu có nghiệm, ta có thể dùng thuật toán ban đầu để giải một hệ đồng dư đã được biến đổi đôi chút.

Một đồng dư $a \equiv a_i \pmod{m_i}$ tương đương với hệ các đồng dư $a \equiv a_i \pmod{p_j^{n_j}}$, trong đó $p_1^{n_1} p_2^{n_2}\cdots p_k^{n_k}$ là phân tích thừa số nguyên tố của $m_i$.

Từ đó, ta có thể biến đổi hệ đồng dư thành một hệ chỉ có các lũy thừa nguyên tố làm mô-đun.
Ví dụ, hệ ở trên tương đương với:

$$\left\{\begin{array}{ll}
    a \equiv 1          & \pmod{4} \\
    a \equiv 2 \equiv 0 & \pmod{2} \\
    a \equiv 2          & \pmod{3}
\end{array}\right.$$

Vì ban đầu một số mô-đun có thừa số chung, ta sẽ nhận được một số đồng dư có mô-đun là các lũy thừa khác nhau của cùng một số nguyên tố.

Ta có thể nhận thấy đồng dư có mô-đun là lũy thừa nguyên tố cao nhất sẽ là điều kiện mạnh nhất trong số các đồng dư dựa trên cùng số nguyên tố.
Nó hoặc mâu thuẫn với một đồng dư khác, hoặc đã suy ra tất cả các đồng dư còn lại.

Trong ví dụ này, đồng dư đầu tiên $a \equiv 1 \pmod{4}$ suy ra $a \equiv 1 \pmod{2}$, và vì vậy mâu thuẫn với đồng dư thứ hai $a \equiv 0 \pmod{2}$.
Do đó hệ đồng dư này không có nghiệm.

Nếu không có mâu thuẫn thì hệ phương trình có nghiệm.
Ta có thể bỏ qua mọi đồng dư trừ những đồng dư có mô-đun là lũy thừa nguyên tố cao nhất.
Các mô-đun còn lại giờ đôi một nguyên tố cùng nhau, nên có thể giải hệ bằng thuật toán ở các phần trước.

Ví dụ, hệ sau có nghiệm theo mô-đun $\text{lcm}(10, 12) = 60$.

$$\left\{\begin{align}
    a & \equiv 3 \pmod{10} \\
    a & \equiv 5 \pmod{12}
\end{align}\right.$$

Hệ đồng dư này tương đương với:

$$\left\{\begin{align}
    a & \equiv 3 \equiv 1 \pmod{2} \\
    a & \equiv 3 \equiv 3 \pmod{5} \\
    a & \equiv 5 \equiv 1 \pmod{4} \\
    a & \equiv 5 \equiv 2 \pmod{3}
\end{align}\right.$$

Hai đồng dư duy nhất có mô-đun dựa trên cùng số nguyên tố là $a \equiv 1 \pmod{4}$ và $a \equiv 1 \pmod{2}$.
Đồng dư thứ nhất đã suy ra đồng dư thứ hai, nên ta có thể bỏ đồng dư thứ hai và giải hệ có các mô-đun nguyên tố cùng nhau sau:

$$\left\{\begin{align}
    a & \equiv 3 \equiv 3 \pmod{5} \\
    a & \equiv 5 \equiv 1 \pmod{4} \\
    a & \equiv 5 \equiv 2 \pmod{3}
\end{align}\right.$$

Hệ này có nghiệm $53 \pmod{60}$, và đúng là $53 \bmod{10} = 3$ và $53 \bmod{12} = 5$.

## Thuật toán Garner

Một hệ quả khác của CRT là ta có thể biểu diễn các số lớn bằng một mảng các số nguyên nhỏ.

Thay vì thực hiện nhiều phép tính với các số cực lớn — có thể rất tốn kém, chẳng hạn phép chia số có 1000 chữ số — ta có thể chọn một số mô-đun nguyên tố cùng nhau, biểu diễn số lớn thành một hệ đồng dư rồi thực hiện các phép toán trên hệ đó.
Mọi số $a$ nhỏ hơn $m_1 m_2 \cdots m_k$ có thể được biểu diễn bằng một mảng $a_1, \ldots, a_k$, trong đó $a \equiv a_i \pmod{m_i}$.

Dùng thuật toán trên, ta có thể khôi phục lại số lớn khi cần.

Ngoài ra, ta có thể viết số đó dưới **biểu diễn cơ số hỗn hợp**:

$$a = x_1 + x_2 m_1 + x_3 m_1 m_2 + \ldots + x_k m_1 \cdots m_{k-1} \text{ with }x_i \in [0, m_i)$$

Thuật toán Garner, được trình bày trong bài riêng [Garner's algorithm](garners-algorithm.md), tính các hệ số $x_i$.
Từ các hệ số này ta có thể khôi phục toàn bộ số ban đầu.

## Bài tập luyện tập:

* [Google Code Jam - Golf Gophers](https://github.com/google/coding-competitions-archive/blob/main/codejam/2019/round_1a/golf_gophers/statement.pdf)
* [Hackerrank - Number of sequences](https://www.hackerrank.com/contests/w22/challenges/number-of-sequences)
* [Codeforces - Remainders Game](http://codeforces.com/problemset/problem/687/B)