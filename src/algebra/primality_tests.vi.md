---
tags:
    - Original
translation:
  source: algebra/primality_tests.md
  source_commit: fa8a705993b450d7cb68cfba5b1a229d5acddffd
  status: draft
  last_synced: 2026-09-29
---

# Kiểm tra tính nguyên tố

Bài viết này trình bày nhiều thuật toán để xác định một số có phải số nguyên tố hay không.

## Chia thử

Theo định nghĩa, một số nguyên tố không có ước nào ngoài $1$ và chính nó.
Một hợp số có ít nhất một ước khác, gọi là $d$.
Hiển nhiên $\frac{n}{d}$ cũng là một ước của $n$.
Dễ thấy $d \le \sqrt{n}$ hoặc $\frac{n}{d} \le \sqrt{n}$, vì vậy một trong hai ước $d$ và $\frac{n}{d}$ thỏa $\le \sqrt{n}$.
Ta có thể dùng nhận xét này để kiểm tra tính nguyên tố.

Ta thử tìm một ước không tầm thường bằng cách kiểm tra xem có số nào từ $2$ đến $\sqrt{n}$ là ước của $n$ hay không.
Nếu tìm được một ước như vậy thì $n$ chắc chắn không phải số nguyên tố; nếu không, số đó là số nguyên tố.

```cpp
bool isPrime(int x) {
    for (int d = 2; d * d <= x; d++) {
        if (x % d == 0)
            return false;
    }
    return x >= 2;
}
```

Đây là dạng đơn giản nhất của phép kiểm tra số nguyên tố.
Có thể tối ưu hàm này khá nhiều, chẳng hạn trong vòng lặp chỉ kiểm tra các số lẻ vì số nguyên tố chẵn duy nhất là 2.
Nhiều tối ưu kiểu này được trình bày trong bài [phân tích thừa số nguyên](factorization.md).

## Kiểm tra tính nguyên tố Fermat

Đây là một phép kiểm tra xác suất.

Định lý nhỏ Fermat (xem thêm [phi hàm Euler](phi-function.md)) nói rằng với một số nguyên tố $p$ và một số nguyên $a$ nguyên tố cùng nhau với số đó, ta có:

$$a^{p-1} \equiv 1 \bmod p$$

Trong tổng quát, định lý này không đúng với hợp số.

Ta có thể dùng điều đó để xây dựng một phép kiểm tra tính nguyên tố.
Ta chọn một số nguyên $2 \le a \le p - 2$ rồi kiểm tra đẳng thức trên có đúng hay không.
Nếu không đúng, tức $a^{p-1} \not\equiv 1 \bmod p$, ta biết $p$ không thể là số nguyên tố.
Trong trường hợp này, cơ số $a$ được gọi là một *chứng nhân Fermat* (Fermat witness) cho tính hợp số của $p$.

Tuy nhiên, đẳng thức vẫn có thể đúng với một hợp số.
Vì vậy, nếu đẳng thức đúng thì ta chưa có chứng minh rằng số đó là nguyên tố.
Ta chỉ có thể nói $p$ *có khả năng là số nguyên tố* (probably prime).
Nếu sau đó phát hiện số này thực ra là hợp số, cơ số $a$ được gọi là một *cơ số đánh lừa Fermat* (Fermat liar).

Nếu chạy phép kiểm tra với mọi cơ số $a$ có thể, ta thực sự có thể chứng minh một số là nguyên tố.
Tuy nhiên, trong thực tế người ta không làm vậy vì tốn công hơn nhiều so với *chia thử*.
Thay vào đó, phép kiểm tra được lặp lại nhiều lần với các lựa chọn ngẫu nhiên cho $a$.
Nếu không tìm thấy chứng nhân cho tính hợp số, xác suất số đó thực sự là số nguyên tố sẽ rất cao.

```cpp
bool probablyPrimeFermat(int n, int iter=5) {
    if (n < 4)
        return n == 2 || n == 3;

    for (int i = 0; i < iter; i++) {
        int a = 2 + rand() % (n - 3);
        if (binpower(a, n - 1, n) != 1)
            return false;
    }
    return true;
}
```

Ta dùng [Lũy thừa nhị phân](binary-exp.md) để tính hiệu quả lũy thừa $a^{p-1}$.

Tuy nhiên có một vấn đề:
tồn tại một số hợp số sao cho $a^{n-1} \equiv 1 \bmod n$ đúng với mọi $a$ nguyên tố cùng nhau với $n$, chẳng hạn $561 = 3 \cdot 11 \cdot 17$.
Những số như vậy được gọi là *số Carmichael*.
Phép kiểm tra Fermat chỉ có thể nhận ra các số này nếu ta cực kỳ may mắn và chọn được cơ số $a$ sao cho $\gcd(a, n) \ne 1$.

Phép kiểm tra Fermat vẫn được dùng trong thực tế vì nó rất nhanh và các số Carmichael rất hiếm.
Ví dụ, chỉ có 646 số như vậy nhỏ hơn $10^9$.

## Kiểm tra tính nguyên tố Miller-Rabin

Phép kiểm tra Miller-Rabin mở rộng ý tưởng của phép kiểm tra Fermat.

Với một số lẻ $n$, $n-1$ là số chẵn và ta có thể tách hết các thừa số 2.
Ta viết:

$$n - 1 = 2^s \cdot d,~\text{with}~d~\text{odd}.$$

Điều này cho phép ta phân tích đẳng thức từ định lý nhỏ Fermat:

$$\begin{array}{rl}
a^{n-1} \equiv 1 \bmod n &\Longleftrightarrow a^{2^s d} - 1 \equiv 0 \bmod n \\\\
&\Longleftrightarrow (a^{2^{s-1} d} + 1) (a^{2^{s-1} d} - 1) \equiv 0 \bmod n \\\\
&\Longleftrightarrow (a^{2^{s-1} d} + 1) (a^{2^{s-2} d} + 1) (a^{2^{s-2} d} - 1) \equiv 0 \bmod n \\\\
&\quad\vdots \\\\
&\Longleftrightarrow (a^{2^{s-1} d} + 1) (a^{2^{s-2} d} + 1) \cdots (a^{d} + 1) (a^{d} - 1) \equiv 0 \bmod n \\\\
\end{array}$$

Nếu $n$ là số nguyên tố thì $n$ phải chia hết một trong các thừa số trên.
Và trong phép kiểm tra Miller-Rabin, ta kiểm tra chính mệnh đề đó; đây là một phiên bản chặt hơn so với điều kiện của phép kiểm tra Fermat.
Với một cơ số $2 \le a \le n-2$, ta kiểm tra xem một trong hai điều kiện sau có đúng hay không:

$$a^d \equiv 1 \bmod n$$

hoặc

$$a^{2^r d} \equiv -1 \bmod n$$

đúng với một giá trị $0 \le r \le s - 1$ nào đó.

Nếu tìm được cơ số $a$ không thỏa bất kỳ đẳng thức nào ở trên, ta đã tìm được một *chứng nhân* cho tính hợp số của $n$.
Khi đó ta đã chứng minh được $n$ không phải số nguyên tố.

Tương tự phép kiểm tra Fermat, tập các đẳng thức trên vẫn có thể được thỏa mãn bởi một hợp số.
Trong trường hợp đó, cơ số $a$ được gọi là một *cơ số đánh lừa mạnh* (strong liar).
Nếu một cơ số $a$ thỏa một trong các đẳng thức, $n$ mới chỉ là một *số có khả năng nguyên tố mạnh* (strong probable prime).
Tuy nhiên, không tồn tại các số tương tự số Carmichael mà mọi cơ số không tầm thường đều đánh lừa phép kiểm tra.
Thực tế có thể chứng minh rằng nhiều nhất $\frac{1}{4}$ số cơ số có thể là các cơ số đánh lừa mạnh.
Nếu $n$ là hợp số, một cơ số ngẫu nhiên có xác suất $\ge 75\%$ cho ta biết nó là hợp số; vì vậy, lặp phép kiểm tra với các cơ số ngẫu nhiên giúp giảm xác suất sai xuống nhỏ tùy ý.

Trên một miền bị chặn, ta có thể bỏ hoàn toàn tính ngẫu nhiên: một tập nhỏ các cơ số cố định, tìm được bằng vét cạn, quyết định chính xác tính nguyên tố của mọi số trong miền đó.
Miller chỉ ra rằng kiểm tra mọi cơ số $\le O((\ln n)^2)$ làm phép kiểm tra trở thành tất định, và Bach đưa ra cận cụ thể $a \le 2\ln(n)^2$.
Đó vẫn là nhiều cơ số, nên người ta đã dành đáng kể tài nguyên tính toán để tìm các tập nhỏ hơn.
Với số nguyên 64 bit, bảy cơ số là đủ: 2, 325, 9375, 28178, 450775, 9780504 và 1795265022.

Dưới đây là một cài đặt cho số nguyên 64 bit.

```cpp
using u64 = uint64_t;
using u128 = __uint128_t;

u64 binpower(u64 base, u64 e, u64 mod) {
    u64 result = 1;
    base %= mod;
    while (e) {
        if (e & 1)
            result = (u128)result * base % mod;
        base = (u128)base * base % mod;
        e >>= 1;
    }
    return result;
}

bool check_composite(u64 n, u64 a, u64 d, int s) {
    a %= n;
    if (a == 0) // n divides the base, so this base can say nothing about n
        return false;
    u64 x = binpower(a, d, n);
    if (x == 1 || x == n - 1)
        return false;
    for (int r = 1; r < s; r++) {
        x = (u128)x * x % n;
        if (x == n - 1)
            return false;
    }
    return true;
};

bool MillerRabin(u64 n) { // returns true if n is prime, else returns false.
    if (n < 2)
        return false;

    int s = 0;
    u64 d = n - 1;
    while ((d & 1) == 0) {
        d >>= 1;
        s++;
    }

    for (u64 a : {2, 325, 9375, 28178, 450775, 9780504, 1795265022})
        if (check_composite(n, a, d, s))
            return false;
    return true;
}
```

Ngoài $2$, không cơ số nào trong bảy cơ số là số nguyên tố, nên một cơ số có thể là bội của chính $n$ đang kiểm tra; chẳng hạn $5$ là ước của $9375$ và $13$ là ước của $325$.
Cơ số như vậy có phần dư bằng $0$ và không cho biết gì về $n$, nên `check_composite` bỏ qua nó và để các cơ số còn lại quyết định.

Điều này hẹp hơn việc bỏ qua mọi phần dư bằng không, và đó là chủ đích.
Nếu $n$ không phải ước của $a$ nhưng lại là ước của $a^d$ thì $n$ không thể là số nguyên tố, vì một số nguyên tố là ước của $a^d$ phải là ước của $a$.
Trong trường hợp này, giá trị không là bằng chứng về tính hợp số chứ không phải thiếu thông tin, và hàm sẽ kết luận tương ứng.
Chỉ nhánh đầu tiên bỏ qua thông tin, vì vậy cùng hàm `check_composite` vẫn đúng nếu nhận các cơ số ngẫu nhiên thay cho tập cố định này.

Dùng 12 số nguyên tố đầu tiên làm cơ số, 2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31 và 37, cũng đúng cho số nguyên 64 bit, nhưng tốn thêm năm vòng kiểm tra.
Với số nguyên 32 bit, bốn cơ số nguyên tố đầu tiên 2, 3, 5 và 7 là đủ; hợp số nhỏ nhất vượt qua chúng là $3\,215\,031\,751 = 151 \cdot 751 \cdot 28351$.

Có thể giảm số vòng hơn nữa bằng cách chọn cơ số từ một bảng nhỏ được đánh chỉ số bằng giá trị băm của $n$, nhờ đó chỉ cần ba phép kiểm tra cho một số 64 bit bất kỳ.
Xem [`cp-algo/number_theory/primality.hpp`](https://lib.cp-algorithms.com/cp-algo/number_theory/primality.hpp.html), mặc định dùng bảy cơ số trên và chuyển sang bảng băm khi có sẵn, đồng thời dùng bộ cơ số quen thuộc 2, 7 và 61 cho các số nhỏ hơn $2^{32}$ khi không dùng bảng.
Các bảng do [Bradley Berg](https://www.techneon.com/) xây dựng, mở rộng một phép kiểm tra 32 bit trước đó của Steve Worley.

## Bài tập luyện tập

- [SPOJ - Prime or Not](https://www.spoj.com/problems/PON/)
- [Project euler - Investigating a Prime Pattern](https://projecteuler.net/problem=146)
