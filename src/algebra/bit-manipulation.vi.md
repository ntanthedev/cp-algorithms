---
tags:
  - Original
translation:
  source: algebra/bit-manipulation.md
  source_commit: f298103232f0d6efa47db18c11ffce8b04d3e282
  status: draft
  last_synced: 2026-08-09
---
# Phép toán bit

## Số nhị phân

**Số nhị phân** là một số được biểu diễn trong hệ cơ số 2, hay hệ nhị phân. Hệ này chỉ dùng hai ký hiệu, thường là "0" và "1".

Ta nói một bit được **bật** nếu nó bằng một, và được **tắt** nếu nó bằng không.

Số nhị phân $(a_k a_{k-1} \dots a_1 a_0)_2$ biểu diễn số:

$$(a_k a_{k-1} \dots a_1 a_0)_2 = a_k \cdot 2^k + a_{k-1} \cdot 2^{k-1} + \dots + a_1 \cdot 2^1 + a_0 \cdot 2^0.$$

Chẳng hạn, số nhị phân $1101_2$ biểu diễn số $13$:

$$\begin{align}
1101_2 &= 1 \cdot 2^3 + 1 \cdot 2^2 + 0 \cdot 2^1 + 1 \cdot 2^0 \\
       &= 1\cdot 8 + 1 \cdot 4 + 0 \cdot 2 + 1 \cdot 1 = 13
\end{align}$$

Máy tính biểu diễn số nguyên dưới dạng số nhị phân.
Các số nguyên dương, dù thuộc kiểu có dấu hay không dấu, được biểu diễn trực tiếp bằng các chữ số nhị phân; còn số nguyên âm có dấu thường được biểu diễn bằng [bù hai](https://en.wikipedia.org/wiki/Two%27s_complement).

```cpp
unsigned int unsigned_number = 13;
assert(unsigned_number == 0b1101);

int positive_signed_number = 13;
assert(positive_signed_number == 0b1101);

int negative_signed_number = -13;
assert(negative_signed_number == 0b1111'1111'1111'1111'1111'1111'1111'0011);
```

CPU có thể thao tác các bit rất nhanh bằng những phép toán chuyên dụng.
Trong một số bài toán, ta có thể tận dụng biểu diễn nhị phân để tăng tốc chương trình.
Trong một số bài khác, thường gặp ở tổ hợp hoặc quy hoạch động, ta cần theo dõi những đối tượng nào đã được chọn từ một tập. Khi đó có thể dùng một số nguyên đủ lớn, mỗi bit đại diện cho một đối tượng; tùy đối tượng được chọn hay bỏ, ta bật hoặc tắt bit tương ứng.

## Các toán tử bit

Với số nguyên có độ dài cố định, các toán tử dưới đây được CPU thực hiện rất nhanh, ở mức tương đương một phép cộng.

### Các toán tử theo bit

-   $\&$ : Toán tử AND theo bit so sánh từng bit của toán hạng thứ nhất với bit tương ứng của toán hạng thứ hai. 
    Nếu cả hai bit đều bằng 1, bit kết quả tương ứng được đặt thành 1. Ngược lại, bit kết quả bằng 0.
 	
-   $|$ : Toán tử OR bao hàm theo bit so sánh từng bit của toán hạng thứ nhất với bit tương ứng của toán hạng thứ hai.
    Nếu ít nhất một trong hai bit bằng 1, bit kết quả tương ứng được đặt thành 1. Ngược lại, bit kết quả bằng 0.

-   $\wedge$ : Toán tử OR loại trừ theo bit (XOR) so sánh từng bit của toán hạng thứ nhất với bit tương ứng của toán hạng thứ hai.
    Nếu một bit bằng 0 còn bit kia bằng 1, bit kết quả tương ứng được đặt thành 1. Ngược lại, bit kết quả bằng 0.

-   $\sim$ : Toán tử bù theo bit (NOT) đảo mọi bit của một số: bit đang bật sẽ bị tắt, còn bit đang tắt sẽ được bật.

**Ghi chú bản dịch:** Nguồn dùng ký hiệu ∧ trong phần mô tả và các công thức cho XOR, trong khi các ví dụ code C++ dùng ký hiệu ^. Trong C++, toán tử XOR theo bit là ^; ký hiệu ∧ ở đây là một điểm trình bày dễ gây nhầm lẫn của nguồn và được giữ nguyên để bảo toàn LaTeX.

Ví dụ:

```
n         = 01011000
n-1       = 01010111
--------------------
n & (n-1) = 01010000
```

```
n         = 01011000
n-1       = 01010111
--------------------
n | (n-1) = 01011111
```

```
n         = 01011000
n-1       = 01010111
--------------------
n ^ (n-1) = 00001111
```

```
n         = 01011000
--------------------
~n        = 10100111
```

### Toán tử dịch bit

Có hai toán tử dùng để dịch các bit.

-   $\gg$ Dịch một số sang phải bằng cách bỏ đi một số chữ số nhị phân ở cuối.
    Mỗi lần dịch một vị trí tương ứng với phép chia nguyên cho 2, nên dịch phải $k$ vị trí tương ứng với phép chia nguyên cho $2^k$.

    Chẳng hạn $5 \gg 2 = 101_2 \gg 2 = 1_2 = 1$, giống với $\frac{5}{2^2} = \frac{5}{4} = 1$.
    Trên máy tính, dịch bit thường nhanh hơn đáng kể so với thực hiện phép chia.

-   $\ll$ Dịch một số sang trái bằng cách thêm các chữ số 0 ở cuối.
    Tương tự dịch phải, dịch trái $k$ vị trí tương ứng với phép nhân với $2^k$.

    Chẳng hạn $5 \ll 3 = 101_2 \ll 3 = 101000_2 = 40$, giống với $5 \cdot 2^3 = 5 \cdot 8 = 40$.

    Tuy nhiên, với số nguyên có độ dài cố định, điều này có nghĩa các chữ số ngoài cùng bên trái có thể bị loại bỏ; nếu dịch quá nhiều, theo mô tả của nguồn ta sẽ nhận được số $0$.


## Các mẹo hữu ích

### Bật/đảo/tắt một bit

Dùng phép dịch bit và một số phép toán bit cơ bản, ta có thể dễ dàng bật, đảo hoặc tắt một bit.
$1 \ll x$ là một số chỉ có bit thứ $x$ được bật, còn $\sim(1 \ll x)$ là một số có mọi bit được bật trừ bit thứ $x$.

- $n ~|~ (1 \ll x)$ bật bit thứ $x$ trong số $n$
- $n ~\wedge~ (1 \ll x)$ đảo bit thứ $x$ trong số $n$
- $n ~\&~ \sim(1 \ll x)$ tắt bit thứ $x$ trong số $n$

### Kiểm tra một bit có được bật hay không

Có thể kiểm tra giá trị của bit thứ $x$ bằng cách dịch số sang phải $x$ vị trí để bit thứ $x$ về hàng đơn vị, sau đó lấy bit đó bằng phép AND theo bit với 1.

``` cpp
bool is_set(unsigned int number, int x) {
    return (number >> x) & 1;
}
```

### Kiểm tra một số có chia hết cho lũy thừa của 2 hay không

Dùng phép AND, ta có thể kiểm tra một số $n$ là chẵn vì $n ~\&~ 1 = 0$ nếu $n$ chẵn, và $n ~\&~ 1 = 1$ nếu $n$ lẻ.
Tổng quát hơn, $n$ chia hết cho $2^{k}$ khi và chỉ khi $n ~\&~ (2^{k} − 1) = 0$.

``` cpp
bool isDivisibleByPowerOf2(int n, int k) {
    int powerOf2 = 1 << k;
    return (n & (powerOf2 - 1)) == 0;
}
```

Ta có thể tính $2^{k}$ bằng cách dịch số 1 sang trái $k$ vị trí.
Mẹo này đúng vì $2^k - 1$ là một số có đúng $k$ bit 1.
Một số chia hết cho $2^k$ phải có các bit ở những vị trí đó bằng 0.

### Kiểm tra một số nguyên có phải lũy thừa của 2 hay không

Một lũy thừa của hai là số chỉ có đúng một bit 1 (chẳng hạn $32 = 0010~0000_2$), còn số liền trước nó có bit đó bằng 0 và mọi bit phía sau đều bằng 1 ($31 = 0001~1111_2$).
Vì vậy, phép AND theo bit giữa một số và số liền trước nó luôn bằng 0, vì chúng không có bit 1 chung.
Dễ kiểm tra rằng điều này chỉ xảy ra với các lũy thừa của hai và với số $0$, vốn không có bit nào được bật.

``` cpp
bool isPowerOfTwo(unsigned int n) {
    return n && !(n & (n - 1));
}
```

### Tắt bit 1 ngoài cùng bên phải

Biểu thức $n ~\&~ (n-1)$ có thể dùng để tắt bit 1 ngoài cùng bên phải của số $n$.
Điều này đúng vì biểu thức $n-1$ đảo tất cả các bit kể từ bit 1 ngoài cùng bên phải của $n$ trở về bên phải, bao gồm cả chính bit 1 đó.
Vì các bit này đều khác so với số ban đầu, phép AND theo bit sẽ đưa tất cả chúng về 0, tạo ra số $n$ ban đầu nhưng với bit 1 ngoài cùng bên phải đã bị tắt.

Chẳng hạn, xét số $52 = 0011~0100_2$:

```
n         = 00110100
n-1       = 00110011
--------------------
n & (n-1) = 00110000
```

### Thuật toán Brian Kernighan

Ta có thể dùng biểu thức trên để đếm số bit 1.

Ý tưởng là chỉ xét các bit đang bật của một số nguyên bằng cách tắt bit 1 ngoài cùng bên phải sau khi đếm nó; vì vậy vòng lặp tiếp theo sẽ xét bit 1 kế tiếp về bên trái.

``` cpp
int countSetBits(int n)
{
    int count = 0;
    while (n)
    {
        n = n & (n - 1);
        count++;
    }
    return count;
}
```

### Đếm tổng số bit 1 đến $n$
Để đếm tổng số bit 1 trong mọi số từ 0 đến $n$ (kể cả $n$), ta có thể chạy thuật toán Brian Kernighan cho từng số đến $n$. Tuy nhiên, cách này có thể dẫn đến "Time Limit Exceeded" khi nộp bài. 

Ta dùng tính chất sau với $2^x$: trong các số từ $1$ đến $2^x - 1$, có tổng cộng $x \cdot 2^{x-1}$ bit 1. Có thể hình dung như sau.
```
0 ->   0 0 0 0
1 ->   0 0 0 1
2 ->   0 0 1 0
3 ->   0 0 1 1
4 ->   0 1 0 0
5 ->   0 1 0 1
6 ->   0 1 1 0
7 ->   0 1 1 1
8 ->   1 0 0 0
```

Ta thấy mọi cột trừ cột ngoài cùng bên trái đều có $4$ bit 1 (tức $2^2$); nói cách khác, đến số $2^3 - 1$, tổng số bit 1 là $3 \cdot 2^{3-1}$.

**Ghi chú bản dịch:** Phần mô tả nguồn gọi x là “lũy thừa lớn nhất của 2”, nhưng các công thức và code thực tế dùng x như số mũ. Ngoài ra, với đầu vào n bằng 1, code cho x bằng 0 rồi thực hiện phép dịch với số vị trí âm; đây là lỗi ca biên của cài đặt nguồn. Bản dịch giữ nguyên code theo quy tắc parity và lỗi này được tách sang PR sửa nguồn riêng.

Từ nhận xét trên, ta có thuật toán sau:

- Tìm lũy thừa lớn nhất của $2$ không vượt quá số đã cho. Gọi số này là $x$.
- Tính tổng số bit 1 từ $1$ đến $2^x - 1$ bằng công thức $x \cdot 2^{x-1}$.
- Đếm số bit 1 ở vị trí cao nhất trong các số từ $2^x$ đến $n$ rồi cộng vào kết quả.
- Trừ $2^x$ khỏi $n$ và lặp lại các bước trên với $n$ mới.

```cpp
int countSetBits(int n) {
        int count = 0;
        while (n > 0) {
            int x = std::bit_width(n) - 1;
            count += x << (x - 1);
            n -= 1 << x;
            count += n + 1;
        }
        return count;
}
```

### Các mẹo bổ sung

- $n ~\&~ (n + 1)$ tắt mọi bit 1 ở cuối: $0011~0111_2 \rightarrow 0011~0000_2$.
- $n ~|~ (n + 1)$ bật bit 0 ngoài cùng bên phải: $0011~0101_2 \rightarrow 0011~0111_2$.
- $n ~\&~ -n$ tách lấy bit 1 ngoài cùng bên phải: $0011~0100_2 \rightarrow 0000~0100_2$.

Có thể tìm thêm nhiều mẹo khác trong cuốn [Hacker's Delight](https://en.wikipedia.org/wiki/Hacker%27s_Delight).

### Hỗ trợ của ngôn ngữ và trình biên dịch

C++ hỗ trợ một số thao tác trên từ C++20 thông qua thư viện chuẩn [bit](https://en.cppreference.com/w/cpp/header/bit):

- `has_single_bit`: kiểm tra số có phải lũy thừa của hai hay không
- `bit_ceil` / `bit_floor`: làm tròn lên/xuống tới lũy thừa của 2 gần nhất theo hướng tương ứng
- `rotl` / `rotr`: xoay các bit của số
- `countl_zero` / `countr_zero` / `countl_one` / `countr_one`: đếm số bit 0/1 liên tiếp ở đầu/cuối
- `popcount`: đếm số bit 1

Ngoài ra, một số trình biên dịch còn cung cấp sẵn các hàm hỗ trợ thao tác bit.
Chẳng hạn GCC định nghĩa một danh sách tại [Built-in Functions Provided by GCC](https://gcc.gnu.org/onlinedocs/gcc/Other-Builtins.html), và các hàm này cũng dùng được với các phiên bản C++ cũ hơn:

- `__builtin_popcount(unsigned int)` trả về số bit 1 (`__builtin_popcount(0b0001'0010'1100) == 4`)
- `__builtin_ffs(int)` trả về vị trí (đánh số từ 1) của bit 1 ngoài cùng bên phải (`__builtin_ffs(0b0001'0010'1100) == 3`)
- `__builtin_clz(unsigned int)` trả về số bit 0 ở đầu (`__builtin_clz(0b0001'0010'1100) == 23`)
- `__builtin_ctz(unsigned int)` trả về số bit 0 ở cuối (`__builtin_ctz(0b0001'0010'1100) == 2`)
- ` __builtin_parity(x)` trả về tính chẵn lẻ của số bit 1 trong biểu diễn bit

_Lưu ý rằng một số thao tác (cả các hàm C++20 lẫn các hàm dựng sẵn của trình biên dịch) có thể khá chậm trong GCC nếu không bật target cụ thể bằng `#pragma GCC target("popcnt")`._

## Bài tập luyện tập

* [Codeforces - Raising Bacteria](https://codeforces.com/problemset/problem/579/A)
* [Codeforces - Fedor and New Game](https://codeforces.com/problemset/problem/467/B)
* [Codeforces - And Then There Were K](https://codeforces.com/problemset/problem/1527/A)
