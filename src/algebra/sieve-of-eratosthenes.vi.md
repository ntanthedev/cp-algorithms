---
tags:
  - Translated
e_maxx_link: eratosthenes_sieve
translation:
  source: algebra/sieve-of-eratosthenes.md
  source_commit: 560d176e7575ee833fe5610406d9bdab1d431e72
  status: draft
  last_synced: 2026-08-06
---

# Sàng Eratosthenes

Sàng Eratosthenes là thuật toán tìm tất cả số nguyên tố trong đoạn $[1;n]$ bằng $O(n \log \log n)$ phép toán.

Thuật toán rất đơn giản:
ban đầu, ta liệt kê tất cả các số từ 2 đến $n$.
Ta đánh dấu mọi bội thực sự của 2 là hợp số, vì 2 là số nguyên tố nhỏ nhất.
Bội thực sự của một số $x$ là một số lớn hơn $x$ và chia hết cho $x$.
Sau đó, ta tìm số tiếp theo chưa bị đánh dấu là hợp số; trong trường hợp này là 3.
Điều đó có nghĩa 3 là số nguyên tố, nên ta đánh dấu mọi bội thực sự của 3 là hợp số.
Số chưa bị đánh dấu tiếp theo là 5, tức số nguyên tố kế tiếp, và ta tiếp tục đánh dấu các bội thực sự của nó.
Ta lặp lại quy trình cho đến khi đã xử lý hết các số trong dãy.

Hình dưới đây minh họa thuật toán khi tìm tất cả số nguyên tố trong đoạn $[1; 16]$. Có thể thấy một hợp số thường bị đánh dấu nhiều lần.

<div style="text-align: center;">
  <img src="sieve_eratosthenes.png" alt="Sieve of Eratosthenes">
</div>

Ý tưởng cốt lõi như sau:
một số là số nguyên tố nếu không có số nguyên tố nhỏ hơn nào chia hết nó.
Vì ta xét các số nguyên tố theo thứ tự tăng dần, mọi số chia hết cho ít nhất một số nguyên tố nhỏ hơn đã được đánh dấu là hợp số.
Do đó, khi đi đến một vị trí chưa bị đánh dấu, số đó không chia hết cho bất kỳ số nguyên tố nhỏ hơn nào và vì thế phải là số nguyên tố.

## Cài đặt

```cpp
int n;
vector<bool> is_prime(n+1, true);
is_prime[0] = is_prime[1] = false;
for (int i = 2; i <= n; i++) {
    if (is_prime[i] && (long long)i * i <= n) {
        for (int j = i * i; j <= n; j += i)
            is_prime[j] = false;
    }
}
```

Đoạn mã trước hết xem mọi số trừ 0 và 1 là ứng viên số nguyên tố, rồi bắt đầu loại các hợp số.
Thuật toán duyệt qua tất cả các số từ $2$ đến $n$.
Nếu số hiện tại $i$ là số nguyên tố, thuật toán đánh dấu mọi bội của $i$ là hợp số, bắt đầu từ $i^2$.
Đây là một tối ưu so với cách cài đặt ngây thơ: mọi bội của $i$ nhỏ hơn $i^2$ đều có một thừa số nguyên tố nhỏ hơn $i$, nên chúng đã bị loại ở các bước trước.
Vì $i^2$ có thể dễ dàng làm tràn kiểu `int`, điều kiện bổ sung được kiểm tra bằng kiểu `long long` trước khi chạy vòng lặp lồng bên trong.

Với cách cài đặt này, thuật toán dùng $O(n)$ bộ nhớ và thực hiện $O(n \log \log n)$ phép toán, như sẽ được phân tích ở phần tiếp theo.

## Phân tích tiệm cận

Không cần biết gì về phân bố số nguyên tố, ta vẫn dễ dàng chứng minh cận thời gian $O(n \log n)$. Nếu bỏ qua điều kiện `is_prime`, vòng lặp trong chạy nhiều nhất $n/i$ lần với $i = 2, 3, 4, \dots$. Tổng số phép toán của vòng lặp trong vì thế có dạng tổng điều hòa $n(1/2 + 1/3 + 1/4 + \cdots)$, được chặn bởi $O(n \log n)$.

Bây giờ ta chứng minh thời gian chạy của thuật toán là $O(n \log \log n)$.
Với mỗi số nguyên tố $p \le n$, vòng lặp trong thực hiện khoảng $\frac{n}{p}$ phép toán.
Do đó, ta cần đánh giá biểu thức sau:

$$\sum_{\substack{p \le n, \\\ p \text{ prime}}} \frac n p = n \cdot \sum_{\substack{p \le n, \\\ p \text{ prime}}} \frac 1 p.$$

Ta nhắc lại hai kết quả đã biết:

  - Số lượng số nguyên tố nhỏ hơn hoặc bằng $n$ xấp xỉ $\frac n {\ln n}$.
  - Số nguyên tố thứ $k$ xấp xỉ $k \ln k$; kết quả này suy ra từ nhận xét trước.

Vì vậy, có thể viết tổng trên dưới dạng:

$$\sum_{\substack{p \le n, \\\ p \text{ prime}}} \frac 1 p \approx \frac 1 2 + \sum_{k = 2}^{\frac n {\ln n}} \frac 1 {k \ln k}.$$

Ta tách số nguyên tố đầu tiên là 2 khỏi tổng vì khi $k = 1$, biểu thức xấp xỉ $k \ln k$ bằng $0$ và gây chia cho không.

Tiếp theo, ta đánh giá tổng này bằng tích phân của cùng hàm số theo $k$ từ $2$ đến $\frac n {\ln n}$. Đây là một phép xấp xỉ hợp lý vì tổng có thể được xem như phép xấp xỉ tích phân bằng phương pháp hình chữ nhật:

$$\sum_{k = 2}^{\frac n {\ln n}} \frac 1 {k \ln k} \approx \int_2^{\frac n {\ln n}} \frac 1 {k \ln k} dk.$$

Nguyên hàm của hàm dưới dấu tích phân là $\ln \ln k$. Sau khi đổi biến và bỏ các hạng bậc thấp, ta thu được:

$$\int_2^{\frac n {\ln n}} \frac 1 {k \ln k} dk = \ln \ln \frac n {\ln n} - \ln \ln 2 = \ln(\ln n - \ln \ln n) - \ln \ln 2 \approx \ln \ln n.$$

Quay lại tổng ban đầu, ta có đánh giá gần đúng:

$$\sum_{\substack{p \le n, \\\ p\ is\ prime}} \frac n p \approx n \ln \ln n + o(n).$$

Một chứng minh chặt chẽ hơn, đồng thời cho đánh giá chính xác hơn đến một hệ số hằng, có thể được tìm thấy trong sách "An Introduction to the Theory of Numbers" của Hardy và Wright, trang 349.

## Các cách tối ưu Sàng Eratosthenes

Điểm yếu lớn nhất của thuật toán là nó quét qua vùng nhớ nhiều lần nhưng mỗi lần chỉ thao tác trên từng phần tử riêng lẻ.
Cách truy cập này không thân thiện với bộ nhớ đệm.
Vì vậy, hằng số ẩn trong $O(n \log \log n)$ tương đối lớn.

Bên cạnh đó, lượng bộ nhớ sử dụng cũng trở thành nút thắt khi $n$ lớn.

Các phương pháp dưới đây giúp giảm số phép toán cũng như giảm đáng kể bộ nhớ cần dùng.

### Chỉ sàng đến căn bậc hai

Để tìm mọi số nguyên tố không vượt quá $n$, ta chỉ cần thực hiện sàng bằng các số nguyên tố không vượt quá căn bậc hai của $n$.

```cpp
int n;
vector<bool> is_prime(n+1, true);
is_prime[0] = is_prime[1] = false;
for (int i = 2; i * i <= n; i++) {
    if (is_prime[i]) {
        for (int j = i * i; j <= n; j += i)
            is_prime[j] = false;
    }
}
```

Tối ưu này không làm thay đổi độ phức tạp. Thật vậy, lặp lại chứng minh trên cho ta đánh giá $n \ln \ln \sqrt n + o(n)$, tương đương về mặt tiệm cận theo các tính chất của logarit. Tuy nhiên, số phép toán thực tế giảm đáng kể.

### Chỉ sàng các số lẻ

Vì mọi số chẵn trừ $2$ đều là hợp số, ta có thể bỏ qua hoàn toàn các số chẵn và chỉ làm việc với số lẻ.

Cách này vừa giảm một nửa lượng bộ nhớ cần dùng, vừa giảm xấp xỉ một nửa số phép toán của thuật toán.

### Mức dùng bộ nhớ và tốc độ thao tác

Cần lưu ý rằng hai cách cài đặt Sàng Eratosthenes ở trên sử dụng $n$ bit bộ nhớ nhờ cấu trúc dữ liệu `vector<bool>`.
`vector<bool>` không phải container thông thường lưu một dãy giá trị `bool`, bởi trên phần lớn kiến trúc máy tính, một `bool` chiếm một byte.
Đây là một chuyên biệt hóa tiết kiệm bộ nhớ của `vector<T>`, chỉ dùng $\frac{N}{8}$ byte.

Các bộ xử lý hiện đại làm việc với byte hiệu quả hơn nhiều so với bit vì thường không thể truy cập trực tiếp từng bit.
Ở bên dưới, `vector<bool>` lưu các bit trong một vùng nhớ liên tục lớn, đọc vùng nhớ theo từng khối vài byte rồi trích xuất hoặc thiết lập bit bằng các phép toán như mặt nạ bit và dịch bit.

Vì vậy, việc đọc hoặc ghi bit qua `vector<bool>` có một phần chi phí phụ; trong nhiều trường hợp, `vector<char>` nhanh hơn dù mỗi phần tử chiếm một byte, tức tốn bộ nhớ gấp 8 lần.

Tuy nhiên, với cách cài đặt Sàng Eratosthenes đơn giản, `vector<bool>` lại thường nhanh hơn.
Nút thắt nằm ở tốc độ nạp dữ liệu vào bộ nhớ đệm, nên dùng ít bộ nhớ mang lại lợi thế lớn.
Một phép đo hiệu năng ([link](https://gist.github.com/jakobkogler/e6359ea9ced24fe304f1a8af3c9bee0e)) cho thấy `vector<bool>` nhanh hơn `vector<char>` từ khoảng 1,4 đến 1,7 lần.

Các nhận xét tương tự cũng áp dụng cho `bitset`.
Đây cũng là cách lưu bit hiệu quả, tương tự `vector<bool>`, nên chỉ chiếm $\frac{N}{8}$ byte, nhưng truy cập phần tử chậm hơn một chút.
Trong phép đo trên, `bitset` có kết quả kém hơn `vector<bool>` đôi chút.
Một nhược điểm khác là kích thước của `bitset` phải được biết tại thời điểm biên dịch.

### Sàng phân đoạn

Từ tối ưu "chỉ sàng đến căn bậc hai", ta thấy không cần giữ toàn bộ mảng `is_prime[1...n]` trong bộ nhớ mọi lúc.
Để sàng, chỉ cần lưu các số nguyên tố đến căn bậc hai của $n$, tức `prime[1... sqrt(n)]`, chia toàn bộ đoạn thành các khối và sàng từng khối riêng biệt.

Gọi $s$ là hằng số xác định kích thước khối. Khi đó có tổng cộng $\lceil {\frac n s} \rceil$ khối, và khối $k$ ($k = 0 ... \lfloor {\frac n s} \rfloor$) chứa các số trong đoạn $[ks; ks + s - 1]$.
Ta xử lý lần lượt từng khối: với mỗi khối $k$, duyệt qua mọi số nguyên tố từ $1$ đến $\sqrt n$ và dùng chúng để sàng khối đó.
Cần điều chỉnh chiến lược một chút khi xử lý các số đầu tiên: thứ nhất, các số nguyên tố trong $[1; \sqrt n]$ không được tự loại chính mình; thứ hai, 0 và 1 phải được đánh dấu là không nguyên tố.
Khi xử lý khối cuối, cũng phải nhớ rằng số cuối cần xét là $n$ không nhất thiết nằm ở cuối khối.

Như đã phân tích, cách cài đặt Sàng Eratosthenes thông thường bị giới hạn bởi tốc độ nạp dữ liệu vào bộ nhớ đệm CPU.
Bằng cách chia đoạn ứng viên $[1; n]$ thành các khối nhỏ hơn, ta không cần giữ nhiều khối trong bộ nhớ cùng lúc và mọi thao tác trở nên thân thiện với bộ nhớ đệm hơn.
Vì lúc này tốc độ bộ nhớ đệm không còn là giới hạn chính, ta có thể thay `vector<bool>` bằng `vector<char>` và tăng thêm hiệu năng: bộ xử lý có thể đọc ghi byte trực tiếp mà không cần thao tác bit để trích xuất từng phần tử.
Phép đo hiệu năng ([link](https://gist.github.com/jakobkogler/e6359ea9ced24fe304f1a8af3c9bee0e)) cho thấy trong trường hợp này `vector<char>` nhanh hơn `vector<bool>` khoảng 3 lần.
Cần thận trọng vì kết quả cụ thể có thể thay đổi tùy kiến trúc, trình biên dịch và mức tối ưu hóa.

Dưới đây là một cách cài đặt đếm số lượng số nguyên tố nhỏ hơn hoặc bằng $n$ bằng sàng theo khối.

```cpp
int count_primes(int n) {
    const int S = 10000;

    vector<int> primes;
    int nsqrt = sqrt(n);
    vector<char> is_prime(nsqrt + 2, true);
    for (int i = 2; i <= nsqrt; i++) {
        if (is_prime[i]) {
            primes.push_back(i);
            for (int j = i * i; j <= nsqrt; j += i)
                is_prime[j] = false;
        }
    }

    int result = 0;
    vector<char> block(S);
    for (int k = 0; k * S <= n; k++) {
        fill(block.begin(), block.end(), true);
        int start = k * S;
        for (int p : primes) {
            int start_idx = (start + p - 1) / p;
            int j = max(start_idx, p) * p - start;
            for (; j < S; j += p)
                block[j] = false;
        }
        if (k == 0)
            block[0] = block[1] = false;
        for (int i = 0; i < S && start + i <= n; i++) {
            if (block[i])
                result++;
        }
    }
    return result;
}
```

Thời gian chạy của sàng theo khối giống Sàng Eratosthenes thông thường, trừ khi kích thước khối quá nhỏ. Bộ nhớ cần dùng giảm xuống $O(\sqrt{n} + S)$ và hiệu quả bộ nhớ đệm tốt hơn.
Đổi lại, ta phải thực hiện một phép chia cho mỗi cặp gồm một khối và một số nguyên tố trong $[1; \sqrt{n}]$; chi phí này trở nên rất lớn khi khối quá nhỏ.
Vì vậy, cần cân bằng khi chọn hằng số $S$.
Trong thử nghiệm được nêu ở bài gốc, kích thước khối từ $10^4$ đến $10^5$ cho kết quả tốt nhất.

## Tìm số nguyên tố trong một đoạn

Đôi khi ta cần tìm tất cả số nguyên tố trong một đoạn $[L,R]$ có độ dài nhỏ, chẳng hạn $R - L + 1 \approx 1e7$, trong khi $R$ có thể rất lớn, chẳng hạn $1e12$.

Ta có thể giải bài toán bằng ý tưởng của sàng phân đoạn.
Trước hết, sinh tất cả số nguyên tố không vượt quá $\sqrt R$, sau đó dùng chúng để đánh dấu mọi hợp số trong đoạn $[L, R]$.

```cpp
vector<char> segmentedSieve(long long L, long long R) {
    // generate all primes up to sqrt(R)
    long long lim = sqrt(R);
    vector<char> mark(lim + 1, false);
    vector<long long> primes;
    for (long long i = 2; i <= lim; ++i) {
        if (!mark[i]) {
            primes.emplace_back(i);
            for (long long j = i * i; j <= lim; j += i)
                mark[j] = true;
        }
    }

    vector<char> isPrime(R - L + 1, true);
    for (long long i : primes)
        for (long long j = max(i * i, (L + i - 1) / i * i); j <= R; j += i)
            isPrime[j - L] = false;
    if (L == 1)
        isPrime[0] = false;
    return isPrime;
}
```
Độ phức tạp thời gian của cách này là $O((R - L + 1) \log \log (R) + \sqrt R \log \log \sqrt R)$.

Ta cũng có thể không sinh trước toàn bộ số nguyên tố:

```cpp
vector<char> segmentedSieveNoPreGen(long long L, long long R) {
    vector<char> isPrime(R - L + 1, true);
    long long lim = sqrt(R);
    for (long long i = 2; i <= lim; ++i)
        for (long long j = max(i * i, (L + i - 1) / i * i); j <= R; j += i)
            isPrime[j - L] = false;
    if (L == 1)
        isPrime[0] = false;
    return isPrime;
}
```

Hiển nhiên, độ phức tạp khi đó kém hơn, bằng $O((R - L + 1) \log (R) + \sqrt R)$. Dù vậy, cách này vẫn chạy rất nhanh trong thực tế.

## Biến thể thời gian tuyến tính

Ta có thể sửa thuật toán để đạt độ phức tạp thời gian tuyến tính.
Cách tiếp cận này được trình bày trong bài [Sàng tuyến tính](prime-sieve-linear.md).
Tuy nhiên, thuật toán đó cũng có những điểm yếu riêng.

## Bài tập luyện tập

* [Leetcode - Four Divisors](https://leetcode.com/problems/four-divisors/)
* [Leetcode - Count Primes](https://leetcode.com/problems/count-primes/)
* [SPOJ - Printing Some Primes](http://www.spoj.com/problems/TDPRIMES/)
* [SPOJ - A Conjecture of Paul Erdos](http://www.spoj.com/problems/HS08PAUL/)
* [SPOJ - Primal Fear](http://www.spoj.com/problems/VECTAR8/)
* [SPOJ - Primes Triangle (I)](http://www.spoj.com/problems/PTRI/)
* [Codeforces - Almost Prime](http://codeforces.com/contest/26/problem/A)
* [Codeforces - Sherlock And His Girlfriend](http://codeforces.com/contest/776/problem/B)
* [SPOJ - Namit in Trouble](http://www.spoj.com/problems/NGIRL/)
* [SPOJ - Bazinga!](http://www.spoj.com/problems/DCEPC505/)
* [Project Euler - Prime pair connection](https://www.hackerrank.com/contests/projecteuler/challenges/euler134)
* [SPOJ - N-Factorful](http://www.spoj.com/problems/NFACTOR/)
* [SPOJ - Binary Sequence of Prime Numbers](http://www.spoj.com/problems/BSPRIME/)
* [UVA 11353 - A Different Kind of Sorting](https://uva.onlinejudge.org/index.php?option=com_onlinejudge&Itemid=8&page=show_problem&problem=2338)
* [SPOJ - Prime Generator](http://www.spoj.com/problems/PRIME1/)
* [SPOJ - Printing some primes (hard)](http://www.spoj.com/problems/PRIMES2/)
* [Codeforces - Nodbach Problem](https://codeforces.com/problemset/problem/17/A)
* [Codeforces - Colliders](https://codeforces.com/problemset/problem/154/B)