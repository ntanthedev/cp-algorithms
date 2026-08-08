---
tags:
  - Translated
e_maxx_link: binomial_coeff
translation:
  source: combinatorics/binomial-coefficients.md
  source_commit: 9f065c1a7d66dfb4c89737ca0cf1bf4137d951c9
  status: draft
  last_synced: 2026-08-08
---

# Hệ số nhị thức

Hệ số nhị thức $\binom n k$ là số cách chọn một tập gồm $k$ phần tử từ $n$ phần tử phân biệt mà không xét thứ tự sắp xếp của các phần tử đó (tức số tập con không có thứ tự).

Hệ số nhị thức cũng là các hệ số trong khai triển của $(a + b) ^ n$ (định lý nhị thức):

$$ (a+b)^n = \binom n 0 a^n + \binom n 1 a^{n-1} b + \binom n 2 a^{n-2} b^2 + \cdots + \binom n k a^{n-k} b^k + \cdots + \binom n n b^n $$

Người ta thường gắn công thức này, cũng như tam giác cho phép tính các hệ số một cách hiệu quả, với Blaise Pascal ở thế kỷ 17. Tuy nhiên, nhà toán học Trung Quốc Yang Hui đã biết đến kết quả này từ thế kỷ 13; học giả Ba Tư Omar Khayyam cũng có thể đã phát hiện ra nó. Trước đó nữa, nhà toán học Ấn Độ Pingala sống vào khoảng thế kỷ 3 TCN đã có những kết quả tương tự. Đóng góp của Newton là tổng quát hóa công thức này cho các số mũ không nhất thiết là số tự nhiên.

## Cách tính

**Công thức giải tích** để tính hệ số nhị thức:

$$ \binom n k = \frac {n!} {k!(n-k)!} $$

Có thể suy ra công thức này dễ dàng từ bài toán chọn có thứ tự (số cách chọn $k$ phần tử phân biệt từ $n$ phần tử phân biệt có xét thứ tự). Trước hết, hãy đếm số cách chọn có thứ tự $k$ phần tử. Có $n$ cách chọn phần tử thứ nhất, $n-1$ cách chọn phần tử thứ hai, $n-2$ cách chọn phần tử thứ ba, v.v. Do đó, số cách sắp có thứ tự là $n (n-1) (n-2) \cdots (n - k + 1) = \frac {n!} {(n-k)!}$. Để chuyển sang trường hợp không xét thứ tự, lưu ý rằng mỗi cách chọn không thứ tự tương ứng với đúng $k!$ cách sắp có thứ tự ($k!$ là số hoán vị của $k$ phần tử). Chia $\frac {n!} {(n-k)!}$ cho $k!$ ta thu được công thức cuối cùng.

**Công thức truy hồi** (gắn với "tam giác Pascal" nổi tiếng):

$$ \binom n k = \binom {n-1} {k-1} + \binom {n-1} k $$

Có thể suy ra công thức này trực tiếp từ công thức giải tích.

Lưu ý rằng khi $n \lt k$, ta quy ước $\binom n k$ bằng không.

## Tính chất

Hệ số nhị thức có nhiều tính chất. Dưới đây là một số tính chất cơ bản nhất:

*   Tính đối xứng:

    \[ \binom n k = \binom n {n-k} \]

*   Hệ thức hấp thụ:

    \[ \binom n k = \frac n k \binom {n-1} {k-1} \]

*   Tổng theo $k$:

    \[ \sum_{k = 0}^n \binom n k = 2 ^ n \]

*   Tổng theo $n$:

    \[ \sum_{m = 0}^n \binom m k = \binom {n + 1} {k + 1} \]

*   Tổng theo cả $n$ và $k$:

    \[ \sum_{k = 0}^m  \binom {n + k} k = \binom {n + m + 1} m \]

*   Tổng các bình phương:

    \[ {\binom n 0}^2 + {\binom n 1}^2 + \cdots + {\binom n n}^2 = \binom {2n} n \]

*   Tổng có trọng số:

    \[ 1 \binom n 1 + 2 \binom n 2 + \cdots + n \binom n n = n 2^{n-1} \]

*   Liên hệ với [dãy Fibonacci](../algebra/fibonacci-numbers.md):

    \[ \binom n 0 + \binom {n-1} 1 + \cdots + \binom {n-k} k + \cdots + \binom 0 n = F_{n+1} \]

## Cách tính

### Tính trực tiếp bằng công thức giải tích

Công thức trực tiếp đầu tiên rất dễ cài đặt, nhưng phương pháp này có thể bị tràn số ngay cả với các giá trị $n$ và $k$ tương đối nhỏ (kể cả khi đáp án cuối cùng vẫn vừa kiểu dữ liệu, các giai thừa trung gian có thể đã tràn). Vì vậy, phương pháp này thường chỉ phù hợp khi dùng [số học số nguyên lớn](../algebra/big-integer.md):

```cpp
int C(int n, int k) {
    int res = 1;
    for (int i = n - k + 1; i <= n; ++i)
        res *= i;
    for (int i = 2; i <= k; ++i)
        res /= i;
    return res;
}
```

### Cài đặt cải tiến

Trong cài đặt trên, tử số và mẫu số đều có cùng số lượng thừa số ($k$), và mỗi thừa số đều không nhỏ hơn 1. Vì vậy, ta có thể thay phân số ban đầu bằng tích của $k$ phân số, mỗi phân số được tính bằng số thực. Tuy nhiên, sau mỗi bước nhân đáp án hiện tại với phân số tiếp theo, kết quả vẫn là số nguyên (điều này suy ra từ hệ thức hấp thụ).

Cài đặt C++:

```cpp
int C(int n, int k) {
    double res = 1;
    for (int i = 1; i <= k; ++i)
        res = res * (n - k + i) / i;
    return (int)(res + 0.01);
}
```

Ở đây ta ép kiểu số thực về số nguyên một cách cẩn thận, vì sai số tích lũy có thể làm giá trị tính được nhỏ hơn giá trị thật một chút (chẳng hạn $2.99999$ thay vì $3$).

### Tam giác Pascal

Dùng công thức truy hồi, ta có thể xây dựng bảng các hệ số nhị thức (tam giác Pascal) rồi lấy kết quả từ bảng. Ưu điểm của phương pháp này là các kết quả trung gian không bao giờ vượt quá đáp án và mỗi phần tử mới của bảng chỉ cần một phép cộng. Nhược điểm là nếu chỉ cần một giá trị duy nhất thì cách này chậm với $n$ và $k$ lớn, bởi để tính $\binom n k$ ta phải dựng bảng của tất cả $\binom i j, 1 \le i \le n, 1 \le j \le n$, hoặc ít nhất tới $1 \le j \le \min (i, 2k)$. Có thể xem độ phức tạp thời gian là $\mathcal{O}(n^2)$.

Cài đặt C++:

```cpp
const int maxn = ...;
int C[maxn + 1][maxn + 1];
C[0][0] = 1;
for (int n = 1; n <= maxn; ++n) {
    C[n][0] = C[n][n] = 1;
    for (int k = 1; k < n; ++k)
        C[n][k] = C[n - 1][k - 1] + C[n - 1][k];
}
```

Nếu không cần toàn bộ bảng giá trị, chỉ cần lưu hai hàng cuối cùng là đủ (hàng thứ $n$ hiện tại và hàng thứ $n-1$ trước đó).

### Tính trong $O(1)$ {data-toc-label="Calculation in O(1)"}

Cuối cùng, trong một số tình huống ta có thể tính trước tất cả giai thừa để sau đó lấy bất kỳ hệ số nhị thức nào chỉ với hai phép chia. Cách này có lợi khi dùng [số học số nguyên lớn](../algebra/big-integer.md) nhưng bộ nhớ không đủ để tính trước toàn bộ tam giác Pascal.


## Tính hệ số nhị thức theo mô-đun $m$ {data-toc-label="Computing binomial coefficients modulo m"}

Ta thường gặp bài toán tính hệ số nhị thức theo một mô-đun $m$ nào đó.

### Hệ số nhị thức với $n$ nhỏ {data-toc-label="Binomial coefficient for small n"}

Có thể dùng tam giác Pascal đã trình bày ở trên để tính tất cả giá trị $\binom{n}{k} \bmod m$ khi $n$ đủ nhỏ, với độ phức tạp thời gian $\mathcal{O}(n^2)$. Cách này dùng được với mọi mô-đun vì chỉ thực hiện phép cộng.


### Hệ số nhị thức theo mô-đun số nguyên tố lớn

Công thức của hệ số nhị thức là

$$\binom n k = \frac {n!} {k!(n-k)!},$$

nên nếu muốn tính nó theo một số nguyên tố $m > n$, ta có

$$\binom n k \equiv n! \cdot (k!)^{-1} \cdot ((n-k)!)^{-1} \mod m.$$

Trước hết, tính trước mọi giai thừa theo mô-đun $m$ tới $\text{MAXN}!$ trong thời gian $O(\text{MAXN})$.

```cpp
factorial[0] = 1;
for (int i = 1; i <= MAXN; i++) {
    factorial[i] = factorial[i - 1] * i % m;
}
```

Sau đó có thể tính hệ số nhị thức trong thời gian $O(\log m)$.

```cpp
long long binomial_coefficient(int n, int k) {
    return factorial[n] * inverse(factorial[k] * factorial[n - k] % m) % m;
}
```

Ta thậm chí có thể tính mỗi hệ số nhị thức trong $O(1)$ nếu tính trước nghịch đảo của mọi giai thừa trong $O(\text{MAXN} \log m)$ bằng cách tính nghịch đảo thông thường, hoặc thậm chí trong $O(\text{MAXN})$ bằng đồng dư $(x!)^{-1} \equiv ((x-1)!)^{-1} \cdot x^{-1}$ và phương pháp [tính trước mọi nghịch đảo](../algebra/module-inverse.md#mod-inv-all-num) trong $O(n)$.

```cpp
long long binomial_coefficient(int n, int k) {
    return factorial[n] * inverse_factorial[k] % m * inverse_factorial[n - k] % m;
}
```

### Hệ số nhị thức theo mô-đun lũy thừa nguyên tố  { #mod-prime-pow}

Ở đây ta muốn tính hệ số nhị thức theo một lũy thừa nguyên tố, tức $m = p^b$ với $p$ là số nguyên tố.
Nếu $p > \max(k, n-k)$, ta có thể dùng cùng phương pháp như phần trước.
Nhưng nếu $p \le \max(k, n-k)$ thì ít nhất một trong $k!$ và $(n-k)!$ không nguyên tố cùng nhau với $m$, vì vậy không thể tính các nghịch đảo — chúng không tồn tại.
Dù vậy, ta vẫn có thể tính hệ số nhị thức.

Ý tưởng như sau:
Với mỗi $x!$, ta tính số mũ lớn nhất $c$ sao cho $p^c$ chia hết $x!$, tức $p^c ~|~ x!$.
Gọi $c(x)$ là số đó.
Và đặt $g(x) := \frac{x!}{p^{c(x)}}$.
Khi đó, ta có thể viết hệ số nhị thức dưới dạng:

$$\binom n k = \frac {g(n) p^{c(n)}} {g(k) p^{c(k)} g(n-k) p^{c(n-k)}} = \frac {g(n)} {g(k) g(n-k)}p^{c(n) - c(k) - c(n-k)}$$

Điểm quan trọng là $g(x)$ lúc này không còn chứa thừa số nguyên tố $p$.
Vì vậy $g(x)$ nguyên tố cùng nhau với m, và ta có thể tính nghịch đảo mô-đun của $g(k)$ và $g(n-k)$.

Sau khi tính trước mọi giá trị $g$ và $c$ bằng quy hoạch động trong $\mathcal{O}(n)$, ta có thể tính hệ số nhị thức trong $O(\log m)$.
Hoặc tính trước mọi nghịch đảo và mọi lũy thừa của $p$, rồi tính mỗi hệ số trong $O(1)$.

Lưu ý rằng nếu $c(n) - c(k) - c(n-k) \ge b$ thì $p^b ~|~ p^{c(n) - c(k) - c(n-k)}$, và hệ số nhị thức bằng $0$ theo mô-đun m.

### Hệ số nhị thức theo một mô-đun bất kỳ

Bây giờ ta tính hệ số nhị thức theo một mô-đun bất kỳ $m$.

Gọi phân tích thừa số nguyên tố của $m$ là $m = p_1^{e_1} p_2^{e_2} \cdots p_h^{e_h}$.
Ta có thể tính hệ số nhị thức theo từng $p_i^{e_i}$ với mọi $i$.
Khi đó ta thu được $h$ đồng dư khác nhau.
Vì mọi mô-đun $p_i^{e_i}$ đôi một nguyên tố cùng nhau, ta có thể áp dụng [Định lý Thặng dư Trung Hoa](../algebra/chinese-remainder-theorem.md) để tính hệ số nhị thức theo tích các mô-đun, chính là hệ số cần tìm theo mô-đun $m$.

### Hệ số nhị thức với $n$ lớn và mô-đun nhỏ {data-toc-label="Binomial coefficient for large n and small modulo"}

Khi $n$ quá lớn, các thuật toán $\mathcal{O}(n)$ nói trên trở nên không thực tế. Tuy nhiên, nếu mô-đun $m$ nhỏ thì vẫn có các cách tính $\binom{n}{k} \bmod m$.

Khi $m$ là số nguyên tố, có 2 lựa chọn:

* Có thể áp dụng [định lý Lucas](https://en.wikipedia.org/wiki/Lucas's_theorem), phân rã bài toán tính $\binom{n}{k} \bmod m$ thành $\log_m n$ bài toán dạng $\binom{x_i}{y_i} \bmod m$ với $x_i, y_i < m$. Nếu mỗi hệ số nhỏ được tính bằng các giai thừa và nghịch đảo giai thừa đã chuẩn bị trước, độ phức tạp là $\mathcal{O}(m + \log_m n)$.
* Có thể dùng phương pháp tính [giai thừa theo mô-đun P](../algebra/factorial-modulo.md) để thu được các giá trị $g$ và $c$ cần thiết, rồi dùng chúng như phần [mô-đun lũy thừa nguyên tố](#mod-prime-pow). Cách này mất $\mathcal{O}(m \log_m n)$.

Khi $m$ không phải số nguyên tố nhưng square-free (không chia hết cho bình phương của bất kỳ số nguyên tố nào), ta có thể phân tích $m$ thành các thừa số nguyên tố, tính hệ số theo từng thừa số bằng một trong hai cách trên rồi ghép đáp án bằng Định lý Thặng dư Trung Hoa.

Khi $m$ không square-free, có thể dùng [một tổng quát hóa của định lý Lucas cho lũy thừa nguyên tố](https://web.archive.org/web/20170202003812/http://www.dms.umontreal.ca/~andrew/PDF/BinCoeff.pdf) thay cho định lý Lucas.


## Bài tập luyện tập
* [Codechef - Number of ways](https://www.codechef.com/LTIME24/problems/NWAYS/)
* [Codeforces - Curious Array](http://codeforces.com/problemset/problem/407/C)
* [LightOj - Necklaces](http://www.lightoj.com/volume_showproblem.php?problem=1419)
* [HACKEREARTH: Binomial Coefficient](https://www.hackerearth.com/problem/algorithm/binomial-coefficient-1/description/)
* [SPOJ - Ada and Teams](http://www.spoj.com/problems/ADATEAMS/)
* [SPOJ - Greedy Walking](http://www.spoj.com/problems/UCV2013E/)
* [UVa 13214 - The Robot's Grid](https://uva.onlinejudge.org/index.php?option=com_onlinejudge&Itemid=8&page=show_problem&problem=5137)
* [SPOJ - Good Predictions](http://www.spoj.com/problems/GOODB/)
* [SPOJ - Card Game](http://www.spoj.com/problems/HC12/)
* [SPOJ - Topper Rama Rao](http://www.spoj.com/problems/HLP_RAMS/)
* [UVa 13184 - Counting Edges and Graphs](https://uva.onlinejudge.org/index.php?option=onlinejudge&page=show_problem&problem=5095)
* [Codeforces - Anton and School 2](http://codeforces.com/contest/785/problem/D)
* [Codeforces - Bacterial Melee](http://codeforces.com/contest/760/problem/F)
* [Codeforces - Points, Lines and Ready-made Titles](http://codeforces.com/contest/872/problem/E)
* [SPOJ - The Ultimate Riddle](https://www.spoj.com/problems/DCEPC13D/)
* [CodeChef - Long Sandwich](https://www.codechef.com/MAY17/problems/SANDWICH/)
* [Codeforces - Placing Jinas](https://codeforces.com/problemset/problem/1696/E)

## Tài liệu tham khảo
* [Blog fishi.devtail.io](https://fishi.devtail.io/weblog/2015/06/25/computing-large-binomial-coefficients-modulo-prime-non-prime/)
* [Question on Mathematics StackExchange](https://math.stackexchange.com/questions/95491/n-choose-k-bmod-m-using-chinese-remainder-theorem)
* [Question on CodeChef Discuss](https://discuss.codechef.com/questions/98129/your-approach-to-solve-sandwich)