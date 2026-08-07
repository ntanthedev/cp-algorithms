---
tags:
    - Original
translation:
  source: algebra/primality_tests.md
  source_commit: f10f24adac42be2b45bcbcff6cb4facad6f7b0c0
  status: draft
  last_synced: 2026-08-07
---

# Kiểm tra tính nguyên tố

Bài viết này trình bày nhiều thuật toán để xác định một số có phải số nguyên tố hay không.

## Chia thử

Theo định nghĩa, một số nguyên tố không có ước nào ngoài $1$ và chính nó.
Một hợp số có ít nhất một ước khác, gọi là $d$.
Hiển nhiên $\frac{n}{d}$ cũng là một ước của $n$.
Dễ thấy $d \le \sqrt{n}$ hoặc $\frac{n}{d} \le \sqrt{n}$, vì vậy một trong hai ước $d$ và $\frac{n}{d}$ không vượt quá $\sqrt{n}$.
Ta có thể dùng nhận xét này để kiểm tra tính nguyên tố.

Ta thử tìm một ước không tầm thường bằng cách kiểm tra xem có số nào từ $2$ đến $\sqrt{n}$ là ước của $n$ hay không.
Nếu tìm được một ước như vậy thì $n$ chắc chắn không phải số nguyên tố; nếu không, $n$ là số nguyên tố.

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

Định lý nhỏ Fermat (xem thêm [phi hàm Euler](phi-function.md)) nói rằng với một số nguyên tố $p$ và một số nguyên $a$ nguyên tố cùng nhau với $p$, ta có:

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
Nếu $n$ là hợp số, một cơ số ngẫu nhiên có xác suất $\ge 75\%$ cho ta biết nó là hợp số.
Bằng cách thực hiện nhiều vòng lặp với các cơ số ngẫu nhiên khác nhau, ta có thể xác định với xác suất rất cao một số thực sự là nguyên tố hay là hợp số.

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

bool MillerRabin(u64 n, int iter=5) { // returns true if n is probably prime, else returns false.
    if (n < 4)
        return n == 2 || n == 3;

    int s = 0;
    u64 d = n - 1;
    while ((d & 1) == 0) {
        d >>= 1;
        s++;
    }

    for (int i = 0; i < iter; i++) {
        int a = 2 + rand() % (n - 3);
        if (check_composite(n, a, d, s))
            return false;
    }
    return true;
}
```

Trước khi chạy Miller-Rabin, ta có thể kiểm tra thêm xem một vài số nguyên tố nhỏ đầu tiên có phải ước hay không.
Điều này có thể tăng tốc đáng kể vì phần lớn hợp số có thừa số nguyên tố rất nhỏ.
Ví dụ, $88\%$ mọi số có một thừa số nguyên tố nhỏ hơn $100$.

### Phiên bản tất định

Miller chứng minh rằng có thể làm thuật toán trở thành tất định bằng cách chỉ kiểm tra mọi cơ số $\le O((\ln n)^2)$.
Sau đó Bach đưa ra một cận cụ thể: chỉ cần kiểm tra mọi cơ số $a \le 2 \ln(n)^2$.

Đây vẫn là một số lượng cơ số khá lớn.
Vì vậy, người ta đã dành nhiều tài nguyên tính toán để tìm các cận nhỏ hơn.
Hóa ra, để kiểm tra một số nguyên 32 bit, chỉ cần kiểm tra bốn cơ số nguyên tố đầu tiên: 2, 3, 5 và 7.
Hợp số nhỏ nhất vượt qua phép kiểm tra này là $3,215,031,751 = 151 \cdot 751 \cdot 28351$.
Còn để kiểm tra một số nguyên 64 bit, chỉ cần kiểm tra 12 cơ số nguyên tố đầu tiên: 2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31 và 37.

Từ đó ta có cài đặt tất định sau:

```cpp
bool MillerRabin(u64 n) { // returns true if n is prime, else returns false.
    if (n < 2)
        return false;

    int r = 0;
    u64 d = n - 1;
    while ((d & 1) == 0) {
        d >>= 1;
        r++;
    }

    for (int a : {2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37}) {
        if (n == a)
            return true;
        if (check_composite(n, a, d, r))
            return false;
    }
    return true;
}
```

Cũng có thể kiểm tra chỉ với 7 cơ số: 2, 325, 9375, 28178, 450775, 9780504 và 1795265022.
Tuy nhiên, vì các số này (trừ 2) không phải số nguyên tố, ta cần kiểm tra thêm xem số đang xét có bằng bất kỳ thừa số nguyên tố nào của các cơ số đó hay không: 2, 3, 5, 13, 19, 73, 193, 407521, 299210837.

## Bài tập luyện tập

- [SPOJ - Prime or Not](https://www.spoj.com/problems/PON/)
- [Project euler - Investigating a Prime Pattern](https://projecteuler.net/problem=146)
