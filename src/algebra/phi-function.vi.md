---
tags:
  - Translated
e_maxx_link: euler_function
translation:
  source: algebra/phi-function.md
  source_commit: 8c6fb03460ee8509d86d43eaf359205164573df3
  status: draft
  last_synced: 2026-08-07
---

# Hàm phi Euler

Hàm phi Euler, còn gọi là **hàm phi** $\phi (n)$, đếm số lượng số nguyên từ 1 đến $n$ (kể cả hai đầu) nguyên tố cùng nhau với $n$. Hai số nguyên tố cùng nhau nếu ước chung lớn nhất của chúng bằng $1$; số $1$ được xem là nguyên tố cùng nhau với mọi số.

Dưới đây là các giá trị $\phi(n)$ của một số số nguyên dương đầu tiên:

$$\begin{array}{|c|c|c|c|c|c|c|c|c|c|c|c|c|c|c|c|c|c|c|c|c|c|}
\hline
n & 1 & 2 & 3 & 4 & 5 & 6 & 7 & 8 & 9 & 10 & 11 & 12 & 13 & 14 & 15 & 16 & 17 & 18 & 19 & 20 & 21 \\\\ \hline
\phi(n) & 1 & 1 & 2 & 2 & 4 & 2 & 6 & 4 & 6 & 4 & 10 & 4 & 12 & 6 & 8 & 8 & 16 & 6 & 18 & 8 & 12 \\\\ \hline
\end{array}$$

## Tính chất

Các tính chất sau của hàm phi Euler là đủ để tính nó cho một số bất kỳ:

  - Nếu $p$ là số nguyên tố thì $\gcd(p, q) = 1$ với mọi $1 \le q < p$. Vì vậy:
  
$$\phi (p) = p - 1.$$

  - Nếu $p$ là số nguyên tố và $k \ge 1$, thì trong các số từ $1$ đến $p^k$ có đúng $p^k / p$ số chia hết cho $p$.
    Do đó:
    
$$\phi(p^k) = p^k - p^{k-1}.$$

  - Nếu $a$ và $b$ nguyên tố cùng nhau thì:
    
    \[\phi(a b) = \phi(a) \cdot \phi(b).\]
    
    Quan hệ này không hiển nhiên. Nó suy ra từ [Định lý số dư Trung Hoa](chinese-remainder-theorem.md). Định lý số dư Trung Hoa bảo đảm rằng với mỗi $0 \le x < a$ và mỗi $0 \le y < b$, tồn tại duy nhất $0 \le z < a b$ sao cho $z \equiv x \pmod{a}$ và $z \equiv y \pmod{b}$. Không khó để chứng minh $z$ nguyên tố cùng nhau với $a b$ khi và chỉ khi $x$ nguyên tố cùng nhau với $a$ và $y$ nguyên tố cùng nhau với $b$. Vì vậy số lượng số nguyên nguyên tố cùng nhau với $a b$ bằng tích số lượng tương ứng của $a$ và $b$.

  - Tổng quát hơn, khi $a$ và $b$ không nguyên tố cùng nhau, ta có

    \[\phi(ab) = \phi(a) \cdot \phi(b) \cdot \dfrac{d}{\phi(d)}\]

    với $d = \gcd(a, b)$.

Do đó, dùng ba tính chất đầu tiên, ta có thể tính $\phi(n)$ thông qua phân tích $n$ thành thừa số nguyên tố.
Nếu $n = {p_1}^{a_1} \cdot {p_2}^{a_2} \cdots {p_k}^{a_k}$, trong đó $p_i$ là các thừa số nguyên tố của $n$, thì

$$\begin{align}
\phi (n) &= \phi ({p_1}^{a_1}) \cdot \phi ({p_2}^{a_2}) \cdots  \phi ({p_k}^{a_k}) \\\\
&= \left({p_1}^{a_1} - {p_1}^{a_1 - 1}\right) \cdot \left({p_2}^{a_2} - {p_2}^{a_2 - 1}\right) \cdots \left({p_k}^{a_k} - {p_k}^{a_k - 1}\right) \\\\
&= p_1^{a_1} \cdot \left(1 - \frac{1}{p_1}\right) \cdot p_2^{a_2} \cdot \left(1 - \frac{1}{p_2}\right) \cdots p_k^{a_k} \cdot \left(1 - \frac{1}{p_k}\right) \\\\
&= n \cdot \left(1 - \frac{1}{p_1}\right) \cdot \left(1 - \frac{1}{p_2}\right) \cdots \left(1 - \frac{1}{p_k}\right)
\end{align}$$

## Cài đặt

Dưới đây là cài đặt dựa trên phân tích thừa số trong $O(\sqrt{n})$:

```cpp
int phi(int n) {
    int result = n;
    for (int i = 2; i * i <= n; i++) {
        if (n % i == 0) {
            while (n % i == 0)
                n /= i;
            result -= result / i;
        }
    }
    if (n > 1)
        result -= result / n;
    return result;
}
```

## Hàm phi Euler từ $1$ đến $n$ trong $O(n \log\log{n})$ { #etf_1_to_n data-toc-label="Euler totient function from 1 to n in <script type=\"math/tex\">O(n log log n)</script>" }

Nếu cần tính hàm phi của mọi số từ $1$ đến $n$, việc phân tích thừa số riêng từng số là không hiệu quả.
Ta có thể dùng cùng ý tưởng với [Sàng Eratosthenes](sieve-of-eratosthenes.md).
Phương pháp vẫn dựa trên tính chất ở trên, nhưng thay vì cập nhật kết quả tạm thời theo từng thừa số nguyên tố của từng số, ta tìm tất cả số nguyên tố rồi với mỗi số nguyên tố cập nhật kết quả tạm thời của mọi số chia hết cho nó.

Vì cách này về bản chất giống Sàng Eratosthenes, độ phức tạp cũng là $O(n \log \log n)$.

```cpp
void phi_1_to_n(int n) {
    vector<int> phi(n + 1);
    for (int i = 0; i <= n; i++)
        phi[i] = i;
    
    for (int i = 2; i <= n; i++) {
        if (phi[i] == i) {
            for (int j = i; j <= n; j += i)
                phi[j] -= phi[j] / i;
        }
    }
}
```

### Tìm hàm phi từ $L$ đến $R$ bằng [sàng phân đoạn](sieve-of-eratosthenes.md#segmented-sieve) { data-toc-label="Finding the totient from L to R using the segmented sieve" }

Nếu cần hàm phi của mọi số từ $L$ đến $R$, ta có thể dùng cách tiếp cận [sàng phân đoạn](sieve-of-eratosthenes.md#segmented-sieve).

Thuật toán trước hết tính sẵn mọi số nguyên tố đến $\sqrt{R}$ bằng [sàng tuyến tính](prime-sieve-linear.md) trong thời gian và bộ nhớ $O(\sqrt{R})$. Với mỗi số trong đoạn $[L, R]$, ta áp dụng công thức $\phi$ dựa trên phân tích thừa số bằng cách duyệt các số nguyên tố này. Ta duy trì một mảng phần dư để theo dõi phần chưa được phân tích của mỗi số. Nếu sau khi xử lý mọi số nguyên tố nhỏ mà phần dư vẫn lớn hơn 1, nó biểu thị một thừa số nguyên tố lớn hơn $\sqrt{R}$ và được xử lý ở lượt cuối. Độ phức tạp tổng cộng cho cả đoạn là $O((R - L + 1) \log \log R) + \sqrt{R}$.


```cpp
const long long MAX_RANGE = 1e6 + 6;
vector<long long> primes;
long long phi[MAX_RANGE], rem[MAX_RANGE];

vector<int> linear_sieve(int n) { 
    vector<bool> composite(n + 1, 0);
    vector<int> prime;

    // 0 and 1 are not composite (nor prime)
    composite[0] = composite[1] = 1;

    for(int i = 2; i <= n; i++) {
        if(!composite[i]) prime.push_back(i);
        for(int j = 0; j < prime.size() && i * prime[j] <= n; j++) {
            composite[i * prime[j]] = true;
            if(i % prime[j] == 0) break;
        }
    }
    return prime;
}

// To get the value of phi(x) for L <= x <= R, use phi[x - L].
void segmented_phi(long long L, long long R) { 
    for(long long i = L; i <= R; i++) {
        rem[i - L] = i;
        phi[i - L] = i;
    }

    for(long long i : primes) {
        for(long long j = max(i * i, (L + i - 1) / i * i); j <= R; j += i) {
            phi[j - L] -= phi[j - L] / i;
            while(rem[j - L] % i == 0) rem[j - L] /= i;
        }
    }

    for(long long i = 0; i < R - L + 1; i++) {
        if(rem[i] > 1) phi[i] -= phi[i] / rem[i];
    }
}
```

## Tính chất tổng trên các ước { #divsum}

Gauss đã thiết lập tính chất thú vị sau:

$$ \sum_{d|n} \phi{(d)} = n$$

Ở đây tổng được lấy trên mọi ước dương $d$ của $n$.

Chẳng hạn, các ước của 10 là 1, 2, 5 và 10.
Do đó $\phi{(1)} + \phi{(2)} + \phi{(5)} + \phi{(10)} = 1 + 1 + 4 + 4 = 10$.

### Tìm hàm phi từ 1 đến $n$ bằng tính chất tổng trên các ước { data-toc-label="Finding the totient from 1 to n using the divisor sum property" }

Tính chất tổng trên các ước cũng cho phép tính hàm phi của mọi số từ 1 đến $n$.
Cài đặt này đơn giản hơn một chút so với cách dựa trên Sàng Eratosthenes ở trên, nhưng có độ phức tạp kém hơn đôi chút: $O(n \log n)$.

```cpp
void phi_1_to_n(int n) {
    vector<int> phi(n + 1);
    phi[0] = 0;
    phi[1] = 1;
    for (int i = 2; i <= n; i++)
        phi[i] = i - 1;
    
    for (int i = 2; i <= n; i++)
        for (int j = 2 * i; j <= n; j += i)
              phi[j] -= phi[i];
}
```

## Ứng dụng trong định lý Euler { #application }

Tính chất nổi tiếng và quan trọng nhất của hàm phi Euler được biểu diễn qua **định lý Euler**:

$$a^{\phi(m)} \equiv 1 \pmod m \quad \text{if } a \text{ and } m \text{ are relatively prime.}$$

Trong trường hợp riêng khi $m$ là số nguyên tố, định lý Euler trở thành **định lý nhỏ Fermat**:

$$a^{m - 1} \equiv 1 \pmod m$$

Định lý Euler và hàm phi Euler xuất hiện rất thường xuyên trong thực tế; chẳng hạn cả hai đều được dùng để tính [nghịch đảo nhân mô-đun](module-inverse.md).

Một hệ quả trực tiếp khác là tương đương:

$$a^n \equiv a^{n \bmod \phi(m)} \pmod m$$

Điều này cho phép tính $x^n \bmod m$ khi $n$ rất lớn, đặc biệt nếu $n$ là kết quả của một phép tính khác, vì ta có thể tính $n$ theo một mô-đun.

### Lý thuyết nhóm
$\phi(n)$ là [cấp của nhóm nhân modulo n](https://en.wikipedia.org/wiki/Multiplicative_group_of_integers_modulo_n) $(\mathbb Z / n\mathbb Z)^\times$, tức nhóm các đơn vị — các phần tử có nghịch đảo nhân. Những phần tử có nghịch đảo nhân chính xác là những phần tử nguyên tố cùng nhau với $n$.

[Bậc nhân](https://en.wikipedia.org/wiki/Multiplicative_order) của phần tử $a$ modulo $n$, ký hiệu $\operatorname{ord}_n(a)$, là số $k>0$ nhỏ nhất sao cho $a^k \equiv 1 \pmod n$. $\operatorname{ord}_n(a)$ là kích thước của nhóm con sinh bởi $a$, nên theo định lý Lagrange, bậc nhân của mọi $a$ phải chia hết $\phi(n)$. Nếu bậc nhân của $a$ bằng $\phi(n)$, tức lớn nhất có thể, thì $a$ là một [căn nguyên thủy](primitive-root.md) và theo định nghĩa nhóm là cyclic.

## Tổng quát hóa

Có một phiên bản ít được biết đến hơn của tương đương cuối cùng, cho phép tính $x^n \bmod m$ hiệu quả ngay cả khi $x$ và $m$ không nguyên tố cùng nhau.
Với $x, m$ bất kỳ và $n \geq \log_2 m$:

$$x^{n}\equiv x^{\phi(m)+[n \bmod \phi(m)]} \mod m$$

Chứng minh:

Gọi $p_1, \dots, p_t$ là các ước nguyên tố chung của $x$ và $m$, và $k_i$ là số mũ tương ứng của chúng trong $m$.
Từ đó đặt $a = p_1^{k_1} \dots p_t^{k_t}$, khi đó $\frac{m}{a}$ nguyên tố cùng nhau với $x$.
Và gọi $k$ là số nhỏ nhất sao cho $a$ chia hết $x^k$.
Giả sử $n \ge k$, ta có thể viết:

$$\begin{align}x^n \bmod m &= \frac{x^k}{a}ax^{n-k}\bmod m \\
&= \frac{x^k}{a}\left(ax^{n-k}\bmod m\right) \bmod m \\
&= \frac{x^k}{a}\left(ax^{n-k}\bmod a \frac{m}{a}\right) \bmod m \\
&=\frac{x^k}{a} a \left(x^{n-k} \bmod \frac{m}{a}\right)\bmod m \\
&= x^k\left(x^{n-k} \bmod \frac{m}{a}\right)\bmod m
\end{align}$$

Sự tương đương giữa dòng thứ ba và thứ tư suy ra từ $ab \bmod ac = a(b \bmod c)$.
Thật vậy, nếu $b = cd + r$ với $r < c$ thì $ab = acd + ar$ với $ar < ac$.

Vì $x$ và $\frac{m}{a}$ nguyên tố cùng nhau, ta có thể áp dụng định lý Euler và nhận công thức hiệu quả sau (vì $k$ rất nhỏ; thực tế $k \le \log_2 m$):

$$x^n \bmod m = x^k\left(x^{n-k \bmod \phi(\frac{m}{a})} \bmod \frac{m}{a}\right)\bmod m.$$

Công thức này khó áp dụng trực tiếp, nhưng có thể dùng để phân tích hành vi của $x^n \bmod m$. Ta thấy dãy lũy thừa $(x^1 \bmod m, x^2 \bmod m, x^3 \bmod m, \dots)$ đi vào một chu kỳ có độ dài $\phi\left(\frac{m}{a}\right)$ sau $k$ phần tử đầu tiên hoặc ít hơn.
$\phi\left(\frac{m}{a}\right)$ chia hết $\phi(m)$ (vì $a$ và $\frac{m}{a}$ nguyên tố cùng nhau nên $\phi(a) \cdot \phi\left(\frac{m}{a}\right) = \phi(m)$), vì vậy cũng có thể nói chu kỳ có độ dài $\phi(m)$.
Và vì $\phi(m) \ge \log_2 m \ge k$, ta suy ra công thức đơn giản hơn mong muốn:

$$ x^n \equiv x^{\phi(m)} x^{(n - \phi(m)) \bmod \phi(m)} \bmod m \equiv x^{\phi(m)+[n \bmod \phi(m)]} \mod m.$$

## Bài tập luyện tập  

* [SPOJ #4141 "Euler Totient Function" [Difficulty: CakeWalk]](http://www.spoj.com/problems/ETF/)
* [UVA #10179 "Irreducible Basic Fractions" [Difficulty: Easy]](http://uva.onlinejudge.org/index.php?option=onlinejudge&page=show_problem&problem=1120)
* [UVA #10299 "Relatives" [Difficulty: Easy]](http://uva.onlinejudge.org/index.php?option=onlinejudge&page=show_problem&problem=1240)
* [UVA #11327 "Enumerating Rational Numbers" [Difficulty: Medium]](http://uva.onlinejudge.org/index.php?option=com_onlinejudge&Itemid=8&page=show_problem&problem=2302)
* [TIMUS #1673 "Admission to Exam" [Difficulty: High]](http://acm.timus.ru/problem.aspx?space=1&num=1673)
* [UVA 10990 - Another New Function](https://uva.onlinejudge.org/index.php?option=onlinejudge&page=show_problem&problem=1931)
* [Codechef - Golu and Sweetness](https://www.codechef.com/problems/COZIE)
* [SPOJ - LCM Sum](http://www.spoj.com/problems/LCMSUM/)
* [GYM - Simple Calculations  (F)](http://codeforces.com/gym/100975)
* [UVA 13132 - Laser Mirrors](https://uva.onlinejudge.org/index.php?option=com_onlinejudge&Itemid=8&page=show_problem&problem=5043)
* [SPOJ - GCDEX](http://www.spoj.com/problems/GCDEX/)
* [UVA 12995 - Farey Sequence](https://uva.onlinejudge.org/index.php?option=com_onlinejudge&Itemid=8&page=show_problem&problem=4878)
* [SPOJ - Totient in Permutation (easy)](http://www.spoj.com/problems/TIP1/)
* [LOJ - Mathematically Hard](http://lightoj.com/volume_showproblem.php?problem=1007)
* [SPOJ - Totient Extreme](http://www.spoj.com/problems/DCEPCA03/)
* [SPOJ - Playing with GCD](http://www.spoj.com/problems/NAJPWG/)
* [SPOJ - G Force](http://www.spoj.com/problems/DCEPC12G/)
* [SPOJ - Smallest Inverse Euler Totient Function](http://www.spoj.com/problems/INVPHI/)
* [Codeforces - Power Tower](http://codeforces.com/problemset/problem/906/D)
* [Kattis - Exponial](https://open.kattis.com/problems/exponial)
* [LeetCode - 372. Super Pow](https://leetcode.com/problems/super-pow/)
* [Codeforces - The Holmes Children](http://codeforces.com/problemset/problem/776/E)
* [Codeforces - Small GCD](https://codeforces.com/contest/1900/problem/D)