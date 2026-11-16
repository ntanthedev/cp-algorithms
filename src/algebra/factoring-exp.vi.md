---
tags:
  - Original
translation:
  source: algebra/factoring-exp.md
  source_commit: 179d657e6d73dcd93ff04c31b973d22fcb2e031d
  status: draft
  last_synced: 2026-11-16
---

# Lũy thừa nhị phân bằng phân tích thừa số

Xét bài toán tính $ax^y \pmod{2^d}$ với các số nguyên $a$, $x$, $y$ và $d \geq 3$, trong đó $x$ là số lẻ.

Thuật toán dưới đây giải bài toán bằng $O(d)$ phép cộng và phép toán nhị phân cùng một phép nhân với $y$.

Do cấu trúc của nhóm nhân modulo $2^d$, mọi số $x$ thỏa mãn $x \equiv 1 \pmod 4$ đều có thể biểu diễn dưới dạng

$$
x \equiv b^{L(x)} \pmod{2^d},
$$

trong đó $b \equiv 5 \pmod 8$. Không mất tính tổng quát, giả sử $x \equiv 1 \pmod 4$, vì có thể đưa trường hợp $x \equiv 3 \pmod 4$ về $x \equiv 1 \pmod 4$ bằng cách thay $x \mapsto -x$ và $a \mapsto (-1)^{y} a$. Khi đó, $ax^y$ được biểu diễn thành

$$
a x^y \equiv a b^{yL(x)} \pmod{2^d}.
$$

Ý tưởng chính là đơn giản hóa phép tính $L(x)$ và $b^{y L(x)}$ nhờ làm việc theo modulo $2^d$. Vì lý do sẽ thấy sau, ta dùng $4L(x)$ thay cho $L(x)$, và lấy modulo $2^d$ thay vì $2^{d-2}$.

Trong bài này ta xét cài đặt cho số nguyên $32$ bit. Gọi

* `mbin_log_32(r, x)` là hàm tính $r+4L(x) \pmod{2^d}$;
* `mbin_exp_32(r, x)` là hàm tính $r b^{\frac{x}{4}} \pmod{2^d}$;
* `mbin_power_odd_32(a, x, y)` là hàm tính $ax^y \pmod{2^d}$.

Khi đó `mbin_power_odd_32` được cài đặt như sau:

```cpp
uint32_t mbin_power_odd_32(uint32_t rem, uint32_t base, uint32_t exp) {
    if (base & 2) {
        /* divider is considered negative */
        base = -base;
        /* check if result should be negative */
        if (exp & 1) {
            rem = -rem;
        }
    }
    return (mbin_exp_32(rem, mbin_log_32(0, base) * exp));
}
```

## Tính 4L(x) từ x

Cho số lẻ $x$ thỏa mãn $x \equiv 1 \pmod 4$. Ta có thể biểu diễn số này dưới dạng

$$
x \equiv (2^{a_1}+1)\dots(2^{a_k}+1) \pmod{2^d},
$$

trong đó $1 < a_1 < \dots < a_k < d$. Hàm $L(\cdot)$ được xác định với mỗi thừa số, vì chúng đều bằng $1$ theo modulo $4$. Do đó,

$$
4L(x) \equiv 4L(2^{a_1}+1)+\dots+4L(2^{a_k}+1) \pmod{2^{d}}.
$$

Vì vậy, nếu tính trước $t_k = 4L(2^n+1)$ với mọi $1 < k < d$, ta có thể tính $4L(x)$ cho mọi số $x$.

Với số nguyên 32 bit, ta có thể dùng bảng sau:

```cpp
const uint32_t mbin_log_32_table[32] = {
    0x00000000, 0x00000000, 0xd3cfd984, 0x9ee62e18,
    0xe83d9070, 0xb59e81e0, 0xa17407c0, 0xce601f80,
    0xf4807f00, 0xe701fe00, 0xbe07fc00, 0xfc1ff800,
    0xf87ff000, 0xf1ffe000, 0xe7ffc000, 0xdfff8000,
    0xffff0000, 0xfffe0000, 0xfffc0000, 0xfff80000,
    0xfff00000, 0xffe00000, 0xffc00000, 0xff800000,
    0xff000000, 0xfe000000, 0xfc000000, 0xf8000000,
    0xf0000000, 0xe0000000, 0xc0000000, 0x80000000,
};
```

Trong thực tế, cách làm hơi khác mô tả trên. Thay vì tìm cách phân tích $x$, ta lần lượt nhân $x$ với $2^n+1$ cho đến khi nó trở thành $1$ theo modulo $2^d$. Bằng cách này, ta tìm được biểu diễn của $x^{-1}$, tức là

$$
x (2^{a_1}+1)\dots(2^{a_k}+1) \equiv 1 \pmod {2^d}.
$$

Để làm vậy, ta duyệt các $n$ thỏa mãn $1 < n < d$. Nếu bit thứ $n$ của $x$ hiện tại bằng 1, ta nhân $x$ với $2^n+1$; trong C++ có thể viết gọn là `x = x + (x << n)`. Việc này không đổi các bit thấp hơn $n$, nhưng đưa bit thứ $n$ về 0 vì $x$ là số lẻ.

Từ đó, hàm `mbin_log_32(r, x)` được cài đặt như sau:

```cpp
uint32_t mbin_log_32(uint32_t r, uint32_t x) {
    uint8_t n;

    for (n = 2; n < 32; n++) {
        if (x & (1 << n)) {
            x = x + (x << n);
            r -= mbin_log_32_table[n];
        }
    }

    return r;
}
```

Lưu ý $4L(x) = -4L(x^{-1})$, nên thay vì cộng $4L(2^n+1)$, ta trừ giá trị đó khỏi $r$, ban đầu bằng $0$.

## Tính x từ 4L(x)

Với $k \geq 1$, ta có

$$
(a 2^{k}+1)^2 = a^2 2^{2k} +a 2^{k+1}+1 = b2^{k+1}+1,
$$

từ đó, bằng cách liên tiếp bình phương, suy ra

$$
(2^a+1)^{2^b} \equiv 1 \pmod{2^{a+b}}.
$$

Áp dụng kết quả này với $a=2^n+1$ và $b=d-k$, ta suy ra cấp nhân của $2^n+1$ là một ước của $2^{d-n}$.

Điều này có nghĩa là $L(2^n+1)$ phải chia hết cho $2^{n}$, vì cấp của $b$ là $2^{d-2}$ và cấp của $b^y$ là $2^{d-2-v}$, trong đó $2^v$ là lũy thừa lớn nhất của $2$ là ước của $y$, nên ta cần

$$
2^{d-k} \equiv 0 \pmod{2^{d-2-v}},
$$

vì vậy $v$ phải lớn hơn hoặc bằng $k-2$. Biểu thức này hơi bất tiện; để khắc phục, từ đầu ta đã nhân $L(x)$ với $4$. Khi biết $4L(x)$, ta có thể phân tích duy nhất nó thành tổng các $4L(2^n+1)$ bằng cách lần lượt xét các bit của $4L(x)$. Nếu bit thứ $n$ bằng $1$, ta nhân kết quả với $2^n+1$ và trừ $4L(2^n+1)$ khỏi giá trị $4L(x)$ hiện tại.

Do đó, `mbin_exp_32` được cài đặt như sau:

```cpp
uint32_t mbin_exp_32(uint32_t r, uint32_t x) {
    uint8_t n;

    for (n = 2; n < 32; n++) {
        if (x & (1 << n)) {
            r = r + (r << n);
            x -= mbin_log_32_table[n];
        }
    }

    return r;
}
```

## Tối ưu thêm

Có thể giảm một nửa số vòng lặp nếu nhận thấy $4L(2^{d-1}+1)=2^{d-1}$ và với $2k \geq d$ ta có

$$
(2^n+1)^2 \equiv 2^{2n} + 2^{n+1}+1 \equiv 2^{n+1}+1 \pmod{2^d},
$$

từ đó suy ra $4L(2^n+1)=2^n$ khi $2n \geq d$. Do đó, có thể đơn giản hóa thuật toán bằng cách chỉ duyệt đến $\frac{d}{2}$ rồi dùng tính chất trên để tính phần còn lại bằng các phép toán bit:

```cpp
uint32_t mbin_log_32(uint32_t r, uint32_t x) {
    uint8_t n;

    for (n = 2; n != 16; n++) {
        if (x & (1 << n)) {
            x = x + (x << n);
            r -= mbin_log_32_table[n];
        }
    }

    r -= (x & 0xFFFF0000);

    return r;
}

uint32_t mbin_exp_32(uint32_t r, uint32_t x) {
    uint8_t n;

    for (n = 2; n != 16; n++) {
        if (x & (1 << n)) {
            r = r + (r << n);
            x -= mbin_log_32_table[n];
        }
    }

    r *= 1 - (x & 0xFFFF0000);

    return r;
}
```

## Tính bảng logarit

Để tính bảng logarit, có thể điều chỉnh thuật toán [Pohlig–Hellman algorithm](https://en.wikipedia.org/wiki/Pohlig–Hellman_algorithm) cho trường hợp modulo là lũy thừa của $2$.

Nhiệm vụ chính là tính $x$ sao cho $g^x \equiv y \pmod{2^d}$, với $g=5$ và $y$ có dạng $2^n+1$.

Bình phương hai vế $k$ lần, ta được

$$
g^{2^k x} \equiv y^{2^k} \pmod{2^d}.
$$

Lưu ý cấp của $g$ không lớn hơn $2^{d}$ (thực ra không lớn hơn $2^{d-2}$, nhưng ta dùng $2^d$ cho thuận tiện), do đó với $k=d-1$, vế trái sẽ là $g^1$ hoặc $g^0$. Điều này cho phép xác định bit thấp nhất của $x$ bằng cách so sánh $y^{2^k}$ với $g$. Giờ giả sử $x=x_0 + 2^k x_1$, trong đó $x_0$ là phần đã biết và $x_1$ chưa biết. Khi đó

$$
g^{x_0+2^k x_1} \equiv y \pmod{2^d}.
$$

Nhân hai vế với $g^{-x_0}$, ta được

$$
g^{2^k x_1} \equiv (g^{-x_0} y) \pmod{2^d}.
$$

Bây giờ, bình phương hai vế $d-k-1$ lần để tìm bit tiếp theo của $x$, cuối cùng khôi phục được toàn bộ các bit.

**Ghi chú bản dịch:** Bài gốc có một số điểm cần thận trọng. Với cơ số b bằng 5 và n bằng 2, logarit của 5 bằng 1, nên phát biểu rằng logarit đó chia hết cho 4 là sai; lập luận ngay sau đó chỉ dẫn tới bậc chia hết yếu hơn. Các chỉ số n và k cũng không nhất quán trong định nghĩa bảng và phép thế vào công thức. Trong mục tính bảng logarit, nếu cấp của 5 là lũy thừa thứ d trừ hai của 2 thì nâng 5 lên lũy thừa thứ d trừ một của 2 luôn cho 1, nên lập luận được nêu không phân biệt được bit. Mã dùng số nguyên không dấu 32 bit và phép tràn tự nhiên theo modulo lũy thừa thứ 32 của 2; không mặc nhiên tổng quát sang mọi d.

## Tài liệu tham khảo

* [M30, Hans Petter Selasky, 2009](https://ia601602.us.archive.org/29/items/B-001-001-251/B-001-001-251.pdf#page=640)
