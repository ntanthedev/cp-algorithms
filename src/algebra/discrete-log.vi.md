---
tags:
  - Translated
e_maxx_link: discrete_log
translation:
  source: algebra/discrete-log.md
  source_commit: de93bdea70577bde70207f9fd5806866436d9543
  status: draft
  last_synced: 2026-08-07
---

# Logarit rời rạc

Logarit rời rạc là một số nguyên $x$ thỏa mãn phương trình

$$a^x \equiv b \pmod m$$

với các số nguyên $a$, $b$ và $m$ cho trước.

Logarit rời rạc không phải lúc nào cũng tồn tại; chẳng hạn phương trình $2^x \equiv 3 \pmod 7$ không có nghiệm. Không có một điều kiện đơn giản để xác định logarit rời rạc có tồn tại hay không.

Trong bài này, ta trình bày thuật toán **Baby-step giant-step** do Shanks đề xuất năm 1971 để tính logarit rời rạc, với độ phức tạp thời gian $O(\sqrt{m})$. Đây là một thuật toán **chia đôi tập (meet-in-the-middle)** vì nó dùng kỹ thuật tách bài toán thành hai nửa.

## Thuật toán

Xét phương trình:

$$a^x \equiv b \pmod m,$$

trong đó $a$ và $m$ nguyên tố cùng nhau.

Đặt $x = np - q$, trong đó $n$ là một hằng số được chọn trước (ta sẽ nói cách chọn $n$ sau). $p$ được gọi là **giant step**, vì khi tăng nó thêm một đơn vị thì $x$ tăng thêm $n$. Tương tự, $q$ được gọi là **baby step**.

Hiển nhiên, mọi số $x$ trong đoạn $[0; m)$ đều có thể biểu diễn dưới dạng này, với $p \in [1; \lceil \frac{m}{n} \rceil ]$ và $q \in [0; n]$.

Khi đó phương trình trở thành:

$$a^{np - q} \equiv b \pmod m.$$

Dùng việc $a$ và $m$ nguyên tố cùng nhau, ta thu được:

$$a^{np} \equiv ba^q \pmod m$$

Ta có thể viết phương trình mới này dưới dạng đơn giản hơn:

$$f_1(p) = f_2(q).$$

Bài toán có thể được giải bằng phương pháp chia đôi tập như sau:

* Tính $f_1$ cho mọi đối số $p$ có thể. Sắp xếp mảng các cặp giá trị-đối số.
* Với mọi đối số $q$ có thể, tính $f_2$ rồi tìm $p$ tương ứng trong mảng đã sắp xếp bằng tìm kiếm nhị phân.

## Độ phức tạp

Ta có thể tính $f_1(p)$ trong $O(\log m)$ bằng [thuật toán lũy thừa nhị phân](binary-exp.md). Tương tự với $f_2(q)$.

Ở bước đầu tiên của thuật toán, ta cần tính $f_1$ cho mọi đối số $p$ có thể rồi sắp xếp các giá trị. Vì vậy bước này có độ phức tạp:

$$O\left(\left\lceil \frac{m}{n} \right\rceil \left(\log m + \log \left\lceil \frac{m}{n} \right\rceil \right)\right) = O\left( \left\lceil \frac {m}{n} \right\rceil \log m\right)$$

Ở bước thứ hai, ta cần tính $f_2(q)$ cho mọi đối số $q$ có thể rồi tìm kiếm nhị phân trên mảng các giá trị của $f_1$, nên bước này có độ phức tạp:

$$O\left(n \left(\log m + \log \frac{m}{n} \right) \right) = O\left(n \log m\right).$$

Cộng hai độ phức tạp lại, ta được $\log m$ nhân với tổng của $n$ và $m/n$. Tổng này nhỏ nhất khi $n = m/n$, nghĩa là để đạt hiệu năng tối ưu, nên chọn $n$ sao cho:

$$n = \sqrt{m}.$$

Khi đó, độ phức tạp của thuật toán là:

$$O(\sqrt {m} \log m).$$

## Cài đặt

### Cài đặt đơn giản nhất

Trong đoạn code sau, hàm `powmod` tính $a^b \pmod m$ và hàm `solve` trả về một nghiệm hợp lệ của bài toán.
Hàm trả về $-1$ nếu không có nghiệm và trả về một trong các nghiệm có thể nếu tồn tại.

```cpp
int powmod(int a, int b, int m) {
    int res = 1;
    while (b > 0) {
        if (b & 1) {
            res = (res * 1ll * a) % m;
        }
        a = (a * 1ll * a) % m;
        b >>= 1;
    }
    return res;
}

int solve(int a, int b, int m) {
    a %= m, b %= m;
    int n = sqrt(m) + 1;
    map<int, int> vals;
    for (int p = 1; p <= n; ++p)
        vals[powmod(a, p * n, m)] = p;
    for (int q = 0; q <= n; ++q) {
        int cur = (powmod(a, q, m) * 1ll * b) % m;
        if (vals.count(cur)) {
            int ans = vals[cur] * n - q;
            return ans;
        }
    }
    return -1;
}
```

Trong đoạn code này, ta dùng `map` của thư viện chuẩn C++ để lưu các giá trị của $f_1$.
Bên trong, `map` dùng cây đỏ-đen để lưu dữ liệu.
Vì vậy code này chậm hơn một chút so với cách dùng mảng rồi tìm kiếm nhị phân, nhưng dễ viết hơn nhiều.

Lưu ý rằng code giả sử $0^0 = 1$, tức nó sẽ tính $0$ là nghiệm của phương trình $0^x \equiv 1 \pmod m$ và cũng là nghiệm của $0^x \equiv 0 \pmod 1$.
Đây là một quy ước thường gặp trong đại số, nhưng không được chấp nhận thống nhất trong mọi lĩnh vực.
Đôi khi $0^0$ đơn giản được xem là không xác định.
Nếu không muốn dùng quy ước này, ta cần xử lý riêng trường hợp $a=0$:

```cpp
    if (a == 0)
        return b == 0 ? 1 : -1;
```

Một điểm khác cần lưu ý: nếu có nhiều đối số $p$ cùng ánh xạ tới một giá trị của $f_1$, ta chỉ lưu một đối số trong số đó.
Điều này vẫn đúng ở đây vì ta chỉ muốn trả về một nghiệm có thể.
Nếu cần trả về mọi nghiệm, ta phải đổi `map<int, int>` thành, chẳng hạn, `map<int, vector<int>>`.
Ta cũng cần sửa bước thứ hai tương ứng.

## Cài đặt cải tiến

Một cải tiến có thể thực hiện là bỏ lũy thừa nhị phân.
Ta làm được điều này bằng cách duy trì một biến được nhân với $a$ mỗi lần tăng $q$, và một biến được nhân với $a^n$ mỗi lần tăng $p$.
Sau thay đổi này, độ phức tạp của thuật toán vẫn như cũ, nhưng thừa số $\log$ giờ chỉ đến từ `map`.
Thay cho `map`, ta cũng có thể dùng bảng băm (`unordered_map` trong C++), có độ phức tạp trung bình $O(1)$ cho thao tác chèn và tìm kiếm.

Các bài toán thường yêu cầu tìm $x$ nhỏ nhất thỏa phương trình.
Ta có thể tìm mọi đáp án rồi lấy nhỏ nhất, hoặc giảm nghiệm đầu tiên tìm được bằng [định lý Euler](phi-function.md#application), nhưng có thể khéo léo chọn thứ tự tính các giá trị để bảo đảm nghiệm đầu tiên tìm được chính là nghiệm nhỏ nhất.

```{.cpp file=discrete_log}
// Returns minimum x for which a ^ x % m = b % m, a and m are coprime.
int solve(int a, int b, int m) {
    a %= m, b %= m;
    int n = sqrt(m) + 1;

    int an = 1;
    for (int i = 0; i < n; ++i)
        an = (an * 1ll * a) % m;

    unordered_map<int, int> vals;
    for (int q = 0, cur = b; q <= n; ++q) {
        vals[cur] = q;
        cur = (cur * 1ll * a) % m;
    }

    for (int p = 1, cur = 1; p <= n; ++p) {
        cur = (cur * 1ll * an) % m;
        if (vals.count(cur)) {
            int ans = n * p - vals[cur];
            return ans;
        }
    }
    return -1;
}
```

Độ phức tạp là $O(\sqrt{m})$ khi dùng `unordered_map`.

## Khi $a$ và $m$ không nguyên tố cùng nhau { data-toc-label='When a and m are not coprime' }
Giả sử $g = \gcd(a, m)$ và $g > 1$. Rõ ràng $a^x \bmod m$ với mọi $x \ge 1$ đều chia hết cho $g$.

Nếu $g \nmid b$, phương trình không có nghiệm $x$.

Nếu $g \mid b$, đặt $a = g \alpha, b = g \beta, m = g \nu$.

$$
\begin{aligned}
a^x & \equiv b \mod m \\\
(g \alpha) a^{x - 1} & \equiv g \beta \mod g \nu \\\
\alpha a^{x-1} & \equiv \beta \mod \nu
\end{aligned}
$$

Có thể dễ dàng mở rộng thuật toán Baby-step giant-step để giải $ka^{x} \equiv b \pmod m$ theo $x$.

```{.cpp file=discrete_log_extended}
// Returns minimum x for which a ^ x % m = b % m.
int solve(int a, int b, int m) {
    a %= m, b %= m;
    int k = 1, add = 0, g;
    while ((g = gcd(a, m)) > 1) {
        if (b == k)
            return add;
        if (b % g)
            return -1;
        b /= g, m /= g, ++add;
        k = (k * 1ll * a / g) % m;
    }

    int n = sqrt(m) + 1;
    int an = 1;
    for (int i = 0; i < n; ++i)
        an = (an * 1ll * a) % m;

    unordered_map<int, int> vals;
    for (int q = 0, cur = b; q <= n; ++q) {
        vals[cur] = q;
        cur = (cur * 1ll * a) % m;
    }

    for (int p = 1, cur = k; p <= n; ++p) {
        cur = (cur * 1ll * an) % m;
        if (vals.count(cur)) {
            int ans = n * p - vals[cur] + add;
            return ans;
        }
    }
    return -1;
}
```

Độ phức tạp thời gian vẫn là $O(\sqrt{m})$ như trước, vì bước rút gọn ban đầu để $a$ và $m$ trở thành nguyên tố cùng nhau được thực hiện trong $O(\log^2 m)$.

## Bài tập luyện tập
* [Spoj - Power Modulo Inverted](http://www.spoj.com/problems/MOD/)
* [Topcoder - SplittingFoxes3](https://community.topcoder.com/stat?c=problem_statement&pm=14386&rd=16801)
* [CodeChef - Inverse of a Function](https://www.codechef.com/problems/INVXOR/)
* [Hard Equation](https://codeforces.com/gym/101853/problem/G) (giả sử $0^0$ không xác định)
* [CodeChef - Chef and Modular Sequence](https://www.codechef.com/problems/CHEFMOD)

## Tài liệu tham khảo
* [Wikipedia - Baby-step giant-step](https://en.wikipedia.org/wiki/Baby-step_giant-step)
* [Answer by Zander on Mathematics StackExchange](https://math.stackexchange.com/a/133054)
