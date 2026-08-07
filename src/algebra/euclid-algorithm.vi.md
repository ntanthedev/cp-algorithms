---
tags:
  - Translated
e_maxx_link: euclid_algorithm
translation:
  source: algebra/euclid-algorithm.md
  source_commit: 2de9318719fc24bf21956eaad3b6067b86a78f4c
  status: draft
  last_synced: 2026-08-06
---

# Thuật toán Euclid để tính ước chung lớn nhất

Cho hai số nguyên không âm $a$ và $b$, ta cần tìm **UCLN** (ước chung lớn nhất, hay greatest common divisor — GCD) của chúng, tức số lớn nhất đồng thời là ước của cả $a$ và $b$.
Đại lượng này thường được ký hiệu là $\gcd(a, b)$. Về mặt toán học, nó được định nghĩa như sau:

$$\gcd(a, b) = \max \{k > 0 : (k \mid a) \text{ and } (k \mid b) \}$$

(trong đó ký hiệu "$\mid$" biểu thị quan hệ chia hết; chẳng hạn "$k \mid a$" nghĩa là "$k$ chia hết $a$")

Khi một trong hai số bằng không và số còn lại khác không, theo định nghĩa, ước chung lớn nhất của chúng chính là số còn lại. Khi cả hai số đều bằng không, ước chung lớn nhất không được xác định (vì có thể chọn một số lớn tùy ý), nhưng trong lập trình ta thường quy ước giá trị đó bằng không để bảo toàn tính kết hợp của phép $\gcd$. Vì vậy, ta có quy tắc đơn giản: nếu một số bằng không thì ước chung lớn nhất là số còn lại.

Thuật toán Euclid được trình bày dưới đây cho phép tìm ước chung lớn nhất của hai số $a$ và $b$ trong $O(\log \min(a, b))$. Do phép toán này có **tính kết hợp**, để tìm UCLN của **nhiều hơn hai số**, ta có thể tính $\gcd(a, b, c) = \gcd(a, \gcd(b, c))$ và tiếp tục tương tự.

Thuật toán lần đầu được mô tả trong tác phẩm "Elements" của Euclid (khoảng năm 300 trước Công nguyên), dù có thể nó đã xuất hiện từ trước đó.

## Thuật toán

Ban đầu, thuật toán Euclid được phát biểu như sau: liên tục lấy số lớn hơn trừ đi số nhỏ hơn cho đến khi một trong hai số bằng không. Thật vậy, nếu $g$ chia hết cả $a$ và $b$ thì $g$ cũng chia hết $a-b$. Ngược lại, nếu $g$ chia hết $a-b$ và $b$, thì $g$ cũng chia hết $a = b + (a-b)$. Do đó, tập các ước chung của $\{a, b\}$ và $\{b,a-b\}$ là như nhau.

Lưu ý rằng $a$ vẫn là số lớn hơn cho đến khi ta trừ $b$ khỏi nó ít nhất $\left\lfloor\frac{a}{b}\right\rfloor$ lần. Vì vậy, để tăng tốc, ta thay $a-b$ bằng $a-\left\lfloor\frac{a}{b}\right\rfloor b = a \bmod b$. Khi đó thuật toán có thể được viết rất gọn:

$$\gcd(a, b) = \begin{cases}a,&\text{if }b = 0 \\ \gcd(b, a \bmod b),&\text{otherwise.}\end{cases}$$

## Cài đặt

```cpp
int gcd (int a, int b) {
    if (b == 0)
        return a;
    else
        return gcd (b, a % b);
}
```

Dùng toán tử ba ngôi trong C++, ta có thể viết hàm trên trong một dòng.

```cpp
int gcd (int a, int b) {
    return b ? gcd (b, a % b) : a;
}
```

Cuối cùng, dưới đây là cách cài đặt không dùng đệ quy:

```cpp
int gcd (int a, int b) {
    while (b) {
        a %= b;
        swap(a, b);
    }
    return a;
}
```

Lưu ý rằng kể từ C++17, `gcd` đã được cung cấp dưới dạng một [hàm chuẩn](https://en.cppreference.com/w/cpp/numeric/gcd) của C++.

## Độ phức tạp thời gian

Thời gian chạy của thuật toán được đánh giá bằng định lý Lamé, qua đó cho thấy một mối liên hệ đáng chú ý giữa thuật toán Euclid và dãy Fibonacci:

Nếu $a > b \geq 1$ và $b < F_n$ với một giá trị $n$ nào đó, thuật toán Euclid thực hiện nhiều nhất $n-2$ lời gọi đệ quy.

Hơn nữa, có thể chứng minh rằng cận trên này là tối ưu. Khi $a = F_n$ và $b = F_{n-1}$, hàm $gcd(a, b)$ thực hiện đúng $n-2$ lời gọi đệ quy. Nói cách khác, hai số Fibonacci liên tiếp là trường hợp xấu nhất của thuật toán Euclid.

Vì các số Fibonacci tăng theo cấp số nhân, ta suy ra thuật toán Euclid chạy trong $O(\log \min(a, b))$.

Một cách đánh giá khác là nhận thấy rằng trong trường hợp $a \geq b$, giá trị $a \bmod b$ nhỏ hơn $a$ ít nhất hai lần, nên số lớn hơn giảm ít nhất một nửa sau mỗi vòng lặp của thuật toán. Áp dụng lập luận này khi tính UCLN của tập số $a_1,\dots,a_n \leq C$, ta còn có thể đánh giá tổng thời gian là $O(n + \log C)$ thay vì $O(n \log C)$, bởi mỗi vòng lặp không tầm thường đều làm ứng viên UCLN hiện tại giảm ít nhất hai lần.

## Bội chung nhỏ nhất

Việc tính bội chung nhỏ nhất (thường ký hiệu là **BCNN**, hay least common multiple — LCM) có thể quy về tính UCLN bằng công thức đơn giản sau:

$$\text{lcm}(a, b) = \frac{a \cdot b}{\gcd(a, b)}$$

Vì vậy, BCNN có thể được tính bằng thuật toán Euclid với cùng độ phức tạp thời gian.

Một cách cài đặt giúp hạn chế tràn số nguyên bằng cách chia $a$ cho UCLN trước khi nhân được viết như sau:

```cpp
int lcm (int a, int b) {
    return a / gcd(a, b) * b;
}
```

## UCLN nhị phân

Thuật toán UCLN nhị phân (Binary GCD) là một phiên bản tối ưu của thuật toán Euclid thông thường.

Phần chậm của thuật toán thông thường là các phép chia lấy dư. Dù thường coi phép modulo có độ phức tạp $O(1)$, trên thực tế nó chậm hơn đáng kể so với các phép toán đơn giản như cộng, trừ hoặc thao tác bit.
Vì vậy, nếu có thể thì ta nên tránh phép modulo.

Ta có thể xây dựng một thuật toán tính UCLN nhanh mà không sử dụng phép lấy dư. Thuật toán dựa trên các tính chất sau:

  - Nếu cả hai số đều chẵn, ta có thể tách một thừa số hai khỏi mỗi số rồi tính UCLN của phần còn lại: $\gcd(2a, 2b) = 2 \gcd(a, b)$.
  - Nếu một số chẵn và số kia lẻ, ta có thể bỏ thừa số 2 khỏi số chẵn: $\gcd(2a, b) = \gcd(a, b)$ nếu $b$ lẻ.
  - Nếu cả hai số đều lẻ, lấy một số trừ số kia không làm thay đổi UCLN: $\gcd(a, b) = \gcd(b, a-b)$

Chỉ dùng các tính chất trên cùng một số hàm thao tác bit nhanh của GCC, ta có thể cài đặt phiên bản sau:

```cpp
int gcd(int a, int b) {
    if (!a || !b)
        return a | b;
    unsigned shift = __builtin_ctz(a | b);
    a >>= __builtin_ctz(a);
    do {
        b >>= __builtin_ctz(b);
        if (a > b)
            swap(a, b);
        b -= a;
    } while (b);
    return a << shift;
}
```

Thông thường, kiểu tối ưu này không cần thiết vì phần lớn ngôn ngữ lập trình đã có hàm tính UCLN trong thư viện chuẩn.
Chẳng hạn, từ C++17 ta có thể dùng hàm `std::gcd` trong header `numeric`.

## Bài tập luyện tập

- [CSAcademy - Greatest Common Divisor](https://csacademy.com/contest/archive/task/gcd/)
- [Codeforces 1916B - Two Divisors](https://codeforces.com/contest/1916/problem/B)