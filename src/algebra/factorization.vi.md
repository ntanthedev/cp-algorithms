---
tags:
  - Original
translation:
  source: algebra/factorization.md
  source_commit: 14715605fc16528ad58cc63f883f28b057336697
  status: draft
  last_synced: 2026-08-07
---

# Phân tích thừa số nguyên tố

Trong bài viết này, ta trình bày một số thuật toán phân tích số nguyên thành thừa số nguyên tố. Tùy dữ liệu đầu vào, mỗi thuật toán có thể chạy nhanh hoặc chậm ở những mức độ khác nhau.

Lưu ý rằng nếu số cần phân tích thực ra là một số nguyên tố, phần lớn các thuật toán sẽ chạy rất chậm. Điều này đặc biệt đúng với các phương pháp phân tích Fermat, Pollard p-1 và Pollard rho.
Vì vậy, trước khi cố phân tích một số, hợp lý nhất là chạy một [phép kiểm tra tính nguyên tố](primality_tests.md) xác suất (hoặc một phép kiểm tra tất định đủ nhanh).

## Chia thử

Đây là thuật toán cơ bản nhất để tìm phân tích thừa số nguyên tố.

Ta lần lượt thử chia cho mọi ước khả dĩ $d$.
Có thể thấy không thể xảy ra việc mọi thừa số nguyên tố của một hợp số $n$ đều lớn hơn $\sqrt{n}$.
Do đó, ta chỉ cần thử các ước $2 \le d \le \sqrt{n}$, nhờ đó thu được phân tích thừa số nguyên tố trong $O(\sqrt{n})$.
(Đây là [thời gian giả đa thức](https://en.wikipedia.org/wiki/Pseudo-polynomial_time), tức đa thức theo giá trị đầu vào nhưng mũ theo số bit biểu diễn đầu vào.)

Ước nhỏ nhất phải là một số nguyên tố.
Ta chia bỏ thừa số vừa tìm được rồi tiếp tục quá trình.
Nếu không tìm thấy ước nào trong đoạn $[2; \sqrt{n}]$, thì bản thân số còn lại phải là số nguyên tố.

```{.cpp file=factorization_trial_division1}
vector<long long> trial_division1(long long n) {
    vector<long long> factorization;
    for (long long d = 2; d * d <= n; d++) {
        while (n % d == 0) {
            factorization.push_back(d);
            n /= d;
        }
    }
    if (n > 1)
        factorization.push_back(n);
    return factorization;
}
```

### Phân tích theo bánh xe

Đây là một cách tối ưu chia thử.
Khi đã biết số không chia hết cho 2, ta không cần kiểm tra các số chẵn khác.
Như vậy chỉ còn $50\%$ số cần thử.
Sau khi tách hết thừa số 2 và thu được một số lẻ, ta có thể bắt đầu từ 3 rồi chỉ xét các số lẻ tiếp theo.

```{.cpp file=factorization_trial_division2}
vector<long long> trial_division2(long long n) {
    vector<long long> factorization;
    while (n % 2 == 0) {
        factorization.push_back(2);
        n /= 2;
    }
    for (long long d = 3; d * d <= n; d += 2) {
        while (n % d == 0) {
            factorization.push_back(d);
            n /= d;
        }
    }
    if (n > 1)
        factorization.push_back(n);
    return factorization;
}
```

Có thể mở rộng cách này thêm nữa.
Nếu số không chia hết cho 3, ta cũng có thể bỏ qua mọi bội khác của 3 trong các phép thử sau.
Khi đó ta chỉ cần kiểm tra các số $5, 7, 11, 13, 17, 19, 23, \dots$.
Ta có thể nhận ra quy luật của các số còn lại.
Ta cần kiểm tra mọi số có $d \bmod 6 = 1$ và $d \bmod 6 = 5$.
Như vậy chỉ còn khoảng $33.3\%$ số cần thử.
Ta có thể cài đặt bằng cách tách hết các thừa số nguyên tố 2 và 3 trước, sau đó bắt đầu từ 5 và chỉ xét các số có số dư $1$ hoặc $5$ modulo $6$.

Dưới đây là một cài đặt dùng các số nguyên tố 2, 3 và 5.
Ta có thể lưu các bước nhảy cần bỏ qua trong một mảng.

```{.cpp file=factorization_trial_division3}
vector<long long> trial_division3(long long n) {
    vector<long long> factorization;
    for (int d : {2, 3, 5}) {
        while (n % d == 0) {
            factorization.push_back(d);
            n /= d;
        }
    }
    static array<int, 8> increments = {4, 2, 4, 2, 4, 6, 2, 6};
    int i = 0;
    for (long long d = 7; d * d <= n; d += increments[i++]) {
        while (n % d == 0) {
            factorization.push_back(d);
            n /= d;
        }
        if (i == 8)
            i = 0;
    }
    if (n > 1)
        factorization.push_back(n);
    return factorization;
}
```

Nếu tiếp tục mở rộng phương pháp này với nhiều số nguyên tố hơn, ta có thể giảm thêm tỉ lệ số phải thử, nhưng danh sách bước nhảy cũng sẽ lớn hơn.

### Các số nguyên tố tính trước

Nếu mở rộng phân tích theo bánh xe mãi, cuối cùng chỉ còn các số nguyên tố cần kiểm tra.
Một cách tốt để làm điều này là tính trước mọi số nguyên tố bằng [Sàng Eratosthenes](sieve-of-eratosthenes.md) đến $\sqrt{n}$ rồi thử từng số.

```{.cpp file=factorization_trial_division4}
vector<long long> primes;

vector<long long> trial_division4(long long n) {
    vector<long long> factorization;
    for (long long d : primes) {
        if (d * d > n)
            break;
        while (n % d == 0) {
            factorization.push_back(d);
            n /= d;
        }
    }
    if (n > 1)
        factorization.push_back(n);
    return factorization;
}
```

## Phương pháp phân tích Fermat

Ta có thể viết một hợp số lẻ $n = p \cdot q$ dưới dạng hiệu hai số chính phương $n = a^2 - b^2$:

$$n = \left(\frac{p + q}{2}\right)^2 - \left(\frac{p - q}{2}\right)^2$$

Phương pháp phân tích Fermat khai thác nhận xét này bằng cách đoán số chính phương thứ nhất $a^2$, rồi kiểm tra phần còn lại $b^2 = a^2 - n$ có cũng là một số chính phương hay không.
Nếu đúng, ta đã tìm được hai thừa số $a - b$ và $a + b$ của $n$.

```cpp
int fermat(int n) {
    int a = ceil(sqrt(n));
    int b2 = a*a - n;
    int b = round(sqrt(b2));
    while (b * b != b2) {
        a = a + 1;
        b2 = a*a - n;
        b = round(sqrt(b2));
    }
    return a - b;
}
```

Phương pháp này có thể rất nhanh khi chênh lệch giữa hai thừa số $p$ và $q$ nhỏ.
Thuật toán chạy trong $O(|p - q|)$ thời gian.
Tuy nhiên trong thực tế phương pháp này ít được dùng. Khi hai thừa số cách xa nhau, nó trở nên cực kỳ chậm.

Dù vậy, vẫn có nhiều cách tối ưu hướng tiếp cận này.
Bằng cách xét các số chính phương $a^2$ modulo một số nhỏ cố định, ta có thể nhận ra một số giá trị $a$ không cần xét vì chúng không thể tạo ra một số chính phương $a^2 - n$.


## Phương pháp Pollard $p - 1$ { data-toc-label="Pollard's <script type='math/tex'>p - 1</script> method" }

Một số $n$ thường có ít nhất một thừa số nguyên tố $p$ sao cho $p - 1$ là $\mathrm{B}$**-powersmooth** với $\mathrm{B}$ nhỏ. Một số nguyên $m$ được gọi là $\mathrm{B}$-powersmooth nếu mọi lũy thừa nguyên tố là ước của $m$ đều không vượt quá $\mathrm{B}$. Chính xác hơn, cho $\mathrm{B} \geqslant 1$ và số nguyên dương $m$. Giả sử phân tích thừa số nguyên tố của $m$ là $m = \prod {q_i}^{e_i}$, trong đó mỗi $q_i$ là số nguyên tố và $e_i \geqslant 1$. Khi đó $m$ là $\mathrm{B}$-powersmooth nếu với mọi $i$, ${q_i}^{e_i} \leqslant \mathrm{B}$.
Ví dụ, phân tích thừa số nguyên tố của $4817191$ là $1303 \cdot 3697$.
Các giá trị $1303 - 1$ và $3697 - 1$ lần lượt là $31$-powersmooth và $16$-powersmooth, vì $1303 - 1 = 2 \cdot 3 \cdot 7 \cdot 31$ và $3697 - 1 = 2^4 \cdot 3 \cdot 7 \cdot 11$.
Năm 1974, John Pollard đưa ra một phương pháp tách thừa số $p$ sao cho $p-1$ là $\mathrm{B}$-powersmooth khỏi một hợp số.

Ý tưởng xuất phát từ [định lý nhỏ Fermat](phi-function.md#application).
Giả sử $n = p \cdot q$ là một phân tích của $n$.
Định lý nói rằng nếu $a$ nguyên tố cùng nhau với $p$, ta có:

$$a^{p - 1} \equiv 1 \pmod{p}$$

Điều này cũng có nghĩa là

$${\left(a^{(p - 1)}\right)}^k \equiv a^{k \cdot (p - 1)} \equiv 1 \pmod{p}.$$

Vì vậy, với mọi $M$ thỏa $p - 1 ~|~ M$, ta biết $a^M \equiv 1$.
Suy ra $a^M - 1 = p \cdot r$, và do đó $p ~|~ \gcd(a^M - 1, n)$.

Vì vậy, nếu $p - 1$ của một thừa số $p$ của $n$ là ước của $M$, ta có thể tách được một thừa số bằng [thuật toán Euclid](euclid-algorithm.md).

Rõ ràng $M$ nhỏ nhất là bội của mọi số $\mathrm{B}$-powersmooth chính là $\text{lcm}(1,~2~,3~,4~,~\dots,~B)$.
Hoặc tương đương:

$$M = \prod_{\text{prime } q \le B} q^{\lfloor \log_q B \rfloor}$$

Lưu ý rằng nếu $p-1$ là ước của $M$ với mọi thừa số nguyên tố $p$ của $n$, thì $\gcd(a^M - 1, n)$ sẽ bằng chính $n$.
Khi đó ta không thu được thừa số nào.
Vì vậy, trong khi xây dựng $M$, ta sẽ tính $\gcd$ nhiều lần.

Một số hợp số không có thừa số $p$ sao cho $p-1$ là $\mathrm{B}$-powersmooth với $\mathrm{B}$ nhỏ.
Chẳng hạn, với hợp số $100~000~000~000~000~493 = 763~013 \cdot 131~059~365~961$, các giá trị $p-1$ tương ứng là $190~753$-powersmooth và $1~092~161~383$-powersmooth.
Ta phải chọn $B \geq 190~753$ mới có thể phân tích số này.

Trong cài đặt sau, ta bắt đầu với $\mathrm{B} = 10$ rồi tăng $\mathrm{B}$ sau mỗi vòng lặp.

```{.cpp file=factorization_p_minus_1}
long long pollards_p_minus_1(long long n) {
    int B = 10;
    long long g = 1;
    while (B <= 1000000 && g < n) {
        long long a = 2 + rand() %  (n - 3);
        g = gcd(a, n);
        if (g > 1)
            return g;

        // compute a^M
        for (int p : primes) {
            if (p >= B)
                continue;
            long long p_power = 1;
            while (p_power * p <= B)
                p_power *= p;
            a = power(a, p_power, n);

            g = gcd(a - 1, n);
            if (g > 1 && g < n)
                return g;
        }
        B *= 2;
    }
    return 1;
}

```

Đây là một thuật toán xác suất.
Vì thế, có khả năng thuật toán hoàn toàn không tìm được thừa số nào.

Độ phức tạp là $O(B \log B \log^2 n)$ cho mỗi vòng lặp.

## Thuật toán rho của Pollard

Thuật toán rho của Pollard là một thuật toán phân tích thừa số khác của John Pollard.

Giả sử phân tích thừa số nguyên tố của một số là $n = p q$.
Thuật toán xét một dãy giả ngẫu nhiên $\{x_i\} = \{x_0,~f(x_0),~f(f(x_0)),~\dots\}$, trong đó $f$ là một hàm đa thức; thường người ta chọn $f(x) = (x^2 + c) \bmod n$ với $c = 1$.

Ở đây ta không thực sự quan tâm tới dãy $\{x_i\}$.
Ta quan tâm nhiều hơn tới dãy $\{x_i \bmod p\}$.
Vì $f$ là hàm đa thức và mọi giá trị nằm trong đoạn $[0;~p)$, dãy này cuối cùng sẽ đi vào một chu trình.
**Nghịch lý ngày sinh** cho thấy số phần tử kỳ vọng trước khi bắt đầu lặp là $O(\sqrt{p})$.
Nếu $p$ nhỏ hơn $\sqrt{n}$, sự lặp lại nhiều khả năng sẽ bắt đầu sau $O(\sqrt[4]{n})$ bước.

Dưới đây là hình minh họa một dãy $\{x_i \bmod p\}$ như vậy với $n = 2206637$, $p = 317$, $x_0 = 2$ và $f(x) = x^2 + 1$.
Nhìn vào hình dạng của dãy, ta có thể thấy rõ vì sao thuật toán được gọi là thuật toán $\rho$ của Pollard.

<div style="text-align: center;">
  <img src="pollard_rho.png" alt="Minh họa thuật toán rho của Pollard">
</div>

Tuy nhiên vẫn còn một câu hỏi.
Làm thế nào tận dụng được tính chất của dãy $\{x_i \bmod p\}$ mà thậm chí không cần biết chính số $p$?

Thực ra khá đơn giản.
Dãy $\{x_i \bmod p\}_{i \le j}$ có chu trình khi và chỉ khi tồn tại hai chỉ số $s, t \le j$ sao cho $x_s \equiv x_t \bmod p$.
Ta có thể viết lại đẳng thức này thành $x_s - x_t \equiv 0 \bmod p$, tương đương $p ~|~ \gcd(x_s - x_t, n)$.

Vì vậy, nếu tìm được hai chỉ số $s$ và $t$ sao cho $g = \gcd(x_s - x_t, n) > 1$, ta vừa phát hiện một chu trình, vừa tìm được một thừa số $g$ của $n$.
Có thể xảy ra $g = n$.
Khi đó ta chưa tìm được thừa số thực sự, nên phải lặp lại thuật toán với tham số khác (giá trị bắt đầu $x_0$ khác, hoặc hằng số $c$ khác trong hàm đa thức $f$).

Để phát hiện chu trình, ta có thể dùng bất kỳ thuật toán phát hiện chu trình thông dụng nào.

### Thuật toán tìm chu trình của Floyd

Thuật toán này phát hiện chu trình bằng hai con trỏ di chuyển trên dãy với tốc độ khác nhau.
Ở mỗi vòng lặp, con trỏ thứ nhất tiến một phần tử, còn con trỏ thứ hai tiến hai phần tử.
Từ đó dễ thấy nếu có chu trình, đến một lúc nào đó con trỏ nhanh sẽ vòng quanh và gặp con trỏ chậm trong chu trình.
Nếu độ dài chu trình là $\lambda$ và $\mu$ là chỉ số đầu tiên nơi chu trình bắt đầu, thuật toán chạy trong $O(\lambda + \mu)$ thời gian.

Thuật toán này còn được gọi là [thuật toán Rùa và Thỏ](../others/tortoise_and_hare.md), dựa trên câu chuyện trong đó một con rùa (con trỏ chậm) và một con thỏ (con trỏ nhanh) chạy đua.

Ta cũng có thể xác định hai tham số $\lambda$ và $\mu$ bằng thuật toán này (vẫn trong $O(\lambda + \mu)$ thời gian và $O(1)$ bộ nhớ).
Khi phát hiện chu trình, thuật toán trả về 'True'.
Nếu dãy không có chu trình, hàm sẽ lặp vô hạn.
Tuy nhiên, khi dùng trong thuật toán rho của Pollard, ta có thể tránh được vấn đề này.

```text
function floyd(f, x0):
    tortoise = x0
    hare = f(x0)
    while tortoise != hare:
        tortoise = f(tortoise)
        hare = f(f(hare))
    return true
```

### Cài đặt

Trước hết là cài đặt dùng **thuật toán tìm chu trình của Floyd**.
Thuật toán thường chạy trong $O(\sqrt[4]{n} \log(n))$ thời gian.

```{.cpp file=pollard_rho}
long long mult(long long a, long long b, long long mod) {
    return (__int128)a * b % mod;
}

long long f(long long x, long long c, long long mod) {
    return (mult(x, x, mod) + c) % mod;
}

long long rho(long long n, long long x0=2, long long c=1) {
    long long x = x0;
    long long y = x0;
    long long g = 1;
    while (g == 1) {
        x = f(x, c, n);
        y = f(y, c, n);
        y = f(y, c, n);
        g = gcd(abs(x - y), n);
    }
    return g;
}
```

Bảng sau cho thấy các giá trị của $x$ và $y$ trong quá trình chạy thuật toán với $n = 2206637$, $x_0 = 2$ và $c = 1$.

$$
\newcommand\T{\Rule{0pt}{1em}{.3em}}
\begin{array}{|l|l|l|l|l|l|}
\hline
i & x_i \bmod n & x_{2i} \bmod n & x_i \bmod 317 & x_{2i} \bmod 317 & \gcd(x_i - x_{2i}, n) \\
\hline
0   & 2       & 2       & 2       & 2       & -   \\
1   & 5       & 26      & 5       & 26      & 1   \\
2   & 26      & 458330  & 26      & 265     & 1   \\
3   & 677     & 1671573 & 43      & 32      & 1   \\
4   & 458330  & 641379  & 265     & 88      & 1   \\
5   & 1166412 & 351937  & 169     & 67      & 1   \\
6   & 1671573 & 1264682 & 32      & 169     & 1   \\
7   & 2193080 & 2088470 & 74      & 74      & 317 \\
\hline
\end{array}$$

Cài đặt dùng hàm `mult` để nhân hai số nguyên $\le 10^{18}$ mà không bị tràn, bằng kiểu `__int128` của GCC cho số nguyên 128 bit.
Nếu không dùng GCC, ta có thể dùng ý tưởng tương tự [lũy thừa nhị phân](binary-exp.md).

```{.cpp file=pollard_rho_mult2}
long long mult(long long a, long long b, long long mod) {
    long long result = 0;
    while (b) {
        if (b & 1)
            result = (result + a) % mod;
        a = (a + a) % mod;
        b >>= 1;
    }
    return result;
}
```

Ngoài ra, ta cũng có thể cài đặt [phép nhân Montgomery](montgomery_multiplication.md).

Như đã nói, nếu $n$ là hợp số nhưng thuật toán trả về $n$ làm thừa số, ta phải lặp lại với các tham số $x_0$ và $c$ khác.
Chẳng hạn lựa chọn $x_0 = c = 1$ sẽ không phân tích được $25 = 5 \cdot 5$.
Thuật toán sẽ trả về $25$.
Tuy nhiên, lựa chọn $x_0 = 1$, $c = 2$ sẽ phân tích được nó.

### Thuật toán Brent

Brent dùng một phương pháp tương tự Floyd với hai con trỏ.
Điểm khác biệt là thay vì cho hai con trỏ tiến lần lượt một và hai vị trí, chúng được tiến theo các lũy thừa của hai.
Ngay khi $2^i$ lớn hơn $\lambda$ và $\mu$, ta sẽ phát hiện được chu trình.

```text
function floyd(f, x0):
    tortoise = x0
    hare = f(x0)
    l = 1
    while tortoise != hare:
        tortoise = hare
        repeat l times:
            hare = f(hare)
            if tortoise == hare:
                return true
        l *= 2
    return true
```

Thuật toán Brent cũng chạy trong thời gian tuyến tính, nhưng nhìn chung nhanh hơn Floyd vì cần ít lần tính hàm $f$ hơn.

### Cài đặt

Có thể tăng tốc cài đặt trực tiếp của Brent bằng cách bỏ qua các hạng $x_l - x_k$ nếu $k < \frac{3 \cdot l}{2}$.
Ngoài ra, thay vì tính $\gcd$ ở mọi bước, ta nhân các hạng lại với nhau, chỉ thực sự kiểm tra $\gcd$ sau vài bước và quay lui nếu đã đi quá xa.

```{.cpp file=pollard_rho_brent}
long long brent(long long n, long long x0=2, long long c=1) {
    long long x = x0;
    long long g = 1;
    long long q = 1;
    long long xs, y;

    int m = 128;
    int l = 1;
    while (g == 1) {
        y = x;
        for (int i = 1; i < l; i++)
            x = f(x, c, n);
        int k = 0;
        while (k < l && g == 1) {
            xs = x;
            for (int i = 0; i < m && i < l - k; i++) {
                x = f(x, c, n);
                q = mult(q, abs(y - x), n);
            }
            g = gcd(q, n);
            k += m;
        }
        l *= 2;
    }
    if (g == n) {
        do {
            xs = f(xs, c, n);
            g = gcd(abs(xs - y), n);
        } while (g == 1);
    }
    return g;
}
```

Kết hợp chia thử cho các số nguyên tố nhỏ với phiên bản thuật toán rho của Pollard dùng Brent tạo nên một thuật toán phân tích thừa số rất mạnh.

## Bài tập luyện tập

- [SPOJ - FACT0](https://www.spoj.com/problems/FACT0/)
- [SPOJ - FACT1](https://www.spoj.com/problems/FACT1/)
- [SPOJ - FACT2](https://www.spoj.com/problems/FACT2/)
- [GCPC 15 - Divisions](https://codeforces.com/gym/100753)
