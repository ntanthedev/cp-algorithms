---
tags:
  - Original
translation:
  source: algebra/montgomery_multiplication.md
  source_commit: 549208780a6c51d78661ad3246f1321ab6ce14b8
  status: draft
  last_synced: 2026-11-16
---

# Phép nhân Montgomery

Nhiều thuật toán trong lý thuyết số như [kiểm tra số nguyên tố](primality_tests.md), [phân tích thừa số nguyên](factorization.md), và trong mật mã như RSA, cần thực hiện nhiều phép toán modulo một số lớn.
Phép nhân như $x y \bmod{n}$ tính khá chậm bằng các thuật toán thông thường, vì cần phép chia để biết phải trừ $n$ khỏi tích bao nhiêu lần.
Phép chia là một phép toán rất tốn kém, nhất là với số lớn.

**Phép nhân Montgomery (theo modulo)** là phương pháp giúp tính các phép nhân như vậy nhanh hơn.
Thay vì chia tích và trừ $n$ nhiều lần, phương pháp này cộng các bội của $n$ để triệt tiêu các bit thấp rồi bỏ các bit thấp đó.

## Biểu diễn Montgomery

Tuy nhiên, phép nhân Montgomery cũng có chi phí.
Thuật toán chỉ hoạt động trong **không gian Montgomery**.
Ta cần chuyển các số vào không gian đó trước khi bắt đầu nhân.

Để xây dựng không gian, ta cần một số nguyên dương $r \ge n$ nguyên tố cùng nhau với $n$, tức $\gcd(n, r) = 1$.
Trong thực tế, ta luôn chọn $r$ là $2^m$ với số nguyên dương $m$, vì khi đó các phép nhân, chia và lấy modulo $r$ có thể được cài đặt hiệu quả bằng phép dịch và các phép toán bit khác.
Trong hầu hết ứng dụng, $n$ là số lẻ, vì việc phân tích một số chẵn thành thừa số không khó.
Do đó mọi lũy thừa của $2$ đều nguyên tố cùng nhau với $n$.

Đại diện $\bar{x}$ của số $x$ trong không gian Montgomery được định nghĩa là:

$$\bar{x} := x \cdot r \bmod n$$

Phép chuyển đổi này thực chất cũng là một phép nhân kiểu mà ta muốn tối ưu.
Vì vậy đây vẫn là một phép toán tốn kém.
Tuy nhiên, mỗi số chỉ cần chuyển vào không gian một lần.
Khi đã ở trong không gian Montgomery, ta có thể thực hiện hiệu quả bao nhiêu phép toán tùy ý.
Cuối cùng ta chuyển kết quả trở lại.
Vì vậy chi phí này không đáng ngại khi thực hiện nhiều phép toán modulo $n$.

Trong không gian Montgomery, phần lớn các phép toán vẫn thực hiện như bình thường.
Ta có thể cộng hai phần tử ($x \cdot r + y \cdot r \equiv (x + y) \cdot r \bmod n$), trừ, kiểm tra bằng nhau và thậm chí tính ước chung lớn nhất của một số với $n$ (vì $\gcd(n, r) = 1$).
Tất cả đều dùng thuật toán thông thường.

Tuy nhiên phép nhân không như vậy.

Ta mong muốn kết quả là:

$$\bar{x} * \bar{y} = \overline{x \cdot y} = (x \cdot y) \cdot r \bmod n.$$

Nhưng phép nhân thông thường sẽ cho:

$$\bar{x} \cdot \bar{y} = (x \cdot y) \cdot r \cdot r \bmod n.$$

Do đó phép nhân trong không gian Montgomery được định nghĩa là:

$$\bar{x} * \bar{y} := \bar{x} \cdot \bar{y} \cdot r^{-1} \bmod n.$$

## Phép rút gọn Montgomery

Nhân hai số trong không gian Montgomery đòi hỏi tính hiệu quả $x \cdot r^{-1} \bmod n$.
Phép toán này gọi là **phép rút gọn Montgomery**, còn được biết đến là thuật toán **REDC**.

Vì $\gcd(n, r) = 1$, tồn tại hai số $r^{-1}$ và $n^{\prime}$ thỏa mãn $0 < r^{-1}, n^{\prime} < n$ sao cho

$$r \cdot r^{-1} + n \cdot n^{\prime} = 1.$$

**Ghi chú bản dịch:** Điều kiện cả hai hệ số trong đẳng thức trên đều dương là sai. Ví dụ với n bằng 3 và r bằng 8, các hệ số Bézout có thể chọn là 2 và âm 5. Đại diện của âm 5 theo modulo 8 là 3, chính là nghịch đảo dương dùng trong phép rút gọn.

Có thể tính cả $r^{-1}$ lẫn $n^{\prime}$ bằng [thuật toán Euclid mở rộng](extended-euclid-algorithm.md).

Dùng đẳng thức này, ta viết $x \cdot r^{-1}$ thành:

$$\begin{aligned}
x \cdot r^{-1} &= x \cdot r \cdot r^{-1} / r = x \cdot (-n \cdot n^{\prime} + 1) / r \\
&= (-x \cdot n \cdot n^{\prime} + x) / r \equiv (-x \cdot n \cdot n^{\prime} + l \cdot r \cdot n + x) / r \bmod n\\
&\equiv ((-x \cdot n^{\prime} + l \cdot r) \cdot n + x) / r \bmod n
\end{aligned}$$

Các đẳng thức đồng dư đúng với mọi số nguyên $l$.
Điều đó có nghĩa là ta có thể cộng hoặc trừ một bội tùy ý của $r$ vào $x \cdot n^{\prime}$; nói cách khác, ta có thể tính $q := x \cdot n^{\prime}$ theo modulo $r$.

Ta thu được thuật toán sau để tính $x \cdot r^{-1} \bmod n$:

```text
function reduce(x):
    q = (x mod r) * n' mod r
    a = (x - q * n) / r
    if a < 0:
        a += n
    return a
```

Vì $x < n \cdot n < r \cdot n$ (ngay cả khi $x$ là kết quả của một phép nhân) và $q \cdot n < r \cdot n$, ta biết $-n < (x - q \cdot n) / r < n$.
Do đó phép lấy modulo cuối cùng được thực hiện bằng một lần kiểm tra và một phép cộng.

Như vậy, ta có thể thực hiện phép rút gọn Montgomery mà không cần phép lấy modulo tốn kém.
Nếu chọn $r$ là lũy thừa của $2$, các phép lấy modulo và phép chia trong thuật toán có thể tính bằng mặt nạ bit và phép dịch.

Một ứng dụng khác của phép rút gọn Montgomery là chuyển một số từ không gian Montgomery trở về không gian thông thường.

## Mẹo tính nghịch đảo nhanh

Để tính hiệu quả nghịch đảo $n^{\prime} := n^{-1} \bmod r$, ta có thể dùng mẹo sau, lấy ý tưởng từ phương pháp Newton:

$$a \cdot x \equiv 1 \bmod 2^k \Longrightarrow a \cdot x \cdot (2 - a \cdot x) \equiv 1 \bmod 2^{2k}$$

Có thể chứng minh điều này dễ dàng.
Nếu $a \cdot x = 1 + m \cdot 2^k$, ta có:

$$\begin{aligned}
a \cdot x \cdot (2 - a \cdot x) &= 2 \cdot a \cdot x - (a \cdot x)^2 \\
&= 2 \cdot (1 + m \cdot 2^k) - (1 + m \cdot 2^k)^2 \\
&= 2 + 2 \cdot m \cdot 2^k - 1 - 2 \cdot m \cdot 2^k - m^2 \cdot 2^{2k} \\
&= 1 - m^2 \cdot 2^{2k} \\
&\equiv 1 \bmod 2^{2k}.
\end{aligned}$$

Điều này có nghĩa là ta có thể bắt đầu với $x = 1$ là nghịch đảo của $a$ theo modulo $2^1$, áp dụng mẹo vài lần; mỗi vòng lặp làm tăng gấp đôi số bit đúng của $x$.

## Cài đặt

Với trình biên dịch GCC, ta vẫn có thể tính hiệu quả $x \cdot y \bmod n$ khi cả ba số là số nguyên 64 bit, vì trình biên dịch hỗ trợ số nguyên 128 bit qua các kiểu `__int128` và `__uint128`.

```cpp
long long result = (__int128)x * y % n;
```

Tuy nhiên không có kiểu số nguyên 256 bit.
Vì vậy, dưới đây ta trình bày một cài đặt phép nhân 128 bit.

```cpp
using u64 = uint64_t;
using u128 = __uint128_t;
using i128 = __int128_t;

struct u256 {
    u128 high, low;

    static u256 mult(u128 x, u128 y) {
        u64 a = x >> 64, b = x;
        u64 c = y >> 64, d = y;
        // (a*2^64 + b) * (c*2^64 + d) =
        // (a*c) * 2^128 + (a*d + b*c)*2^64 + (b*d)
        u128 ac = (u128)a * c;
        u128 ad = (u128)a * d;
        u128 bc = (u128)b * c;
        u128 bd = (u128)b * d;
        u128 carry = (u128)(u64)ad + (u128)(u64)bc + (bd >> 64u);
        u128 high = ac + (ad >> 64u) + (bc >> 64u) + (carry >> 64u);
        u128 low = (ad << 64u) + (bc << 64u) + bd;
        return {high, low};
    }
};

struct Montgomery {
    Montgomery(u128 n) : mod(n), inv(1) {
        for (int i = 0; i < 7; i++)
            inv *= 2 - n * inv;
    }

    u128 init(u128 x) {
        x %= mod;
        for (int i = 0; i < 128; i++) {
            x <<= 1;
            if (x >= mod)
                x -= mod;
        }
        return x;
    }

    u128 reduce(u256 x) {
        u128 q = x.low * inv;
        i128 a = x.high - u256::mult(q, mod).high;
        if (a < 0)
            a += mod;
        return a;
    }

    u128 mult(u128 a, u128 b) {
        return reduce(u256::mult(a, b));
    }

    u128 mod, inv;
};
```

**Ghi chú bản dịch:** Cài đặt khởi tạo ở trên có thể tràn khi dịch trái trước khi so sánh với modulo. Chẳng hạn, với modulo bằng lũy thừa thứ 127 của 2 cộng 1 và đầu vào bằng lũy thừa thứ 127 của 2, bước dịch đầu tiên tràn về 0 trong kiểu 128 bit, trong khi kết quả đúng sau rút gọn là lũy thừa thứ 127 của 2 trừ 1. Mã cần xử lý bit tràn để áp dụng cho miền này.

## Chuyển đổi nhanh

Phương pháp hiện tại để chuyển một số vào không gian Montgomery khá chậm.
Có những cách nhanh hơn.

Ta có thể nhận thấy hệ thức sau:

$$\bar{x} := x \cdot r \bmod n = x \cdot r^2 / r = x * r^2$$

Chuyển một số vào không gian chỉ là nhân số đó với $r^2$ bên trong không gian.
Vì vậy, ta có thể tính trước $r^2 \bmod n$ và chỉ thực hiện một phép nhân thay vì dịch số 128 lần.

Trong mã dưới đây, ta khởi tạo `r2` bằng `-n % n`, tương đương $r - n \equiv r \bmod n$, rồi dịch trái 4 lần để nhận $r \cdot 2^4 \bmod n$.
Số này có thể được hiểu là $2^4$ trong không gian Montgomery.
Nếu bình phương nó $5$ lần, ta được $(2^4)^{2^5} = (2^4)^{32} = 2^{128} = r$ trong không gian Montgomery, chính là $r^2 \bmod n$.

```
struct Montgomery {
    Montgomery(u128 n) : mod(n), inv(1), r2(-n % n) {
        for (int i = 0; i < 7; i++)
            inv *= 2 - n * inv;

        for (int i = 0; i < 4; i++) {
            r2 <<= 1;
            if (r2 >= mod)
                r2 -= mod;
        }
        for (int i = 0; i < 5; i++)
            r2 = mul(r2, r2);
    }

    u128 init(u128 x) {
        return mult(x, r2);
    }

    u128 mod, inv, r2;
};
```

**Ghi chú bản dịch:** Đoạn mã chuyển đổi nhanh là phác thảo chưa đầy đủ: nó gọi hàm có tên khác với hàm nhân đã định nghĩa ở trên và không đưa lại toàn bộ các định nghĩa cần thiết.
