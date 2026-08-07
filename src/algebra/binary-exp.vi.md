---
tags:
  - Translated
e_maxx_link: binary_pow
translation:
  source: algebra/binary-exp.md
  source_commit: 789e889fdf35777ef20030db2a398b300c65e302
  status: draft
  last_synced: 2026-08-07
---

# Lũy thừa nhị phân

Lũy thừa nhị phân (còn gọi là **lũy thừa bằng bình phương**, exponentiation by squaring) là một kỹ thuật cho phép tính $a^n$, với $n$ là số nguyên không âm, chỉ bằng $O(\log n)$ phép nhân thay vì $O(n)$ phép nhân như cách trực tiếp.

Kỹ thuật này còn có nhiều ứng dụng quan trọng không chỉ trong số học, vì nó có thể dùng với bất kỳ phép toán nào có tính **kết hợp**:

$$(X \cdot Y) \cdot Z = X \cdot (Y \cdot Z)$$

Ví dụ rõ nhất là phép nhân mô-đun, phép nhân ma trận và một số bài toán khác sẽ được trình bày bên dưới.

## Thuật toán

Theo cách trực tiếp, để nâng $a$ lên lũy thừa $n$ ta nhân $a$ với chính nó $n - 1$ lần:
$a^{n} = a \cdot a \cdot \ldots \cdot a$. Tuy nhiên cách này không thực tế khi $a$ hoặc $n$ lớn.

$a^{b+c} = a^b \cdot a^c$ và $a^{2b} = a^b \cdot a^b = (a^b)^2$.

Ý tưởng của lũy thừa nhị phân là chia nhỏ công việc dựa trên biểu diễn nhị phân của số mũ.

Ví dụ, viết $n$ trong cơ số 2:

$$3^{13} = 3^{1101_2} = 3^8 \cdot 3^4 \cdot 3^1$$

Vì số $n$ có đúng $\lfloor \log_2 n \rfloor + 1$ chữ số trong cơ số 2, ta chỉ cần thực hiện $O(\log n)$ phép nhân nếu biết các lũy thừa $a^1, a^2, a^4, a^8, \dots, a^{2^{\lfloor \log_2 n \rfloor}}$.

Vì vậy ta chỉ cần một cách nhanh để tính các giá trị đó.
Điều này rất đơn giản, vì mỗi phần tử trong dãy chỉ là bình phương của phần tử trước.

$$\begin{align}
3^1 &= 3 \\
3^2 &= \left(3^1\right)^2 = 3^2 = 9 \\
3^4 &= \left(3^2\right)^2 = 9^2 = 81 \\
3^8 &= \left(3^4\right)^2 = 81^2 = 6561
\end{align}$$

Để thu được $3^{13}$, ta chỉ cần nhân ba giá trị tương ứng với các bit được bật của $n$ và bỏ qua $3^2$:
$3^{13} = 6561 \cdot 81 \cdot 3 = 1594323$

Độ phức tạp cuối cùng là $O(\log n)$: ta cần tính $\log n$ lũy thừa của $a$, sau đó thực hiện nhiều nhất $\log n$ phép nhân để ghép chúng thành đáp án.

Cách đệ quy sau biểu diễn đúng ý tưởng đó:

$$a^n = \begin{cases}
1 &\text{if } n == 0 \\
\left(a^{\frac{n}{2}}\right)^2 &\text{if } n > 0 \text{ and } n \text{ even}\\
\left(a^{\frac{n - 1}{2}}\right)^2 \cdot a &\text{if } n > 0 \text{ and } n \text{ odd}\\
\end{cases}$$

## Cài đặt

Trước hết là cách đệ quy, dịch trực tiếp từ công thức truy hồi:

```cpp
long long binpow(long long a, long long b) {
    if (b == 0)
        return 1;
    long long res = binpow(a, b / 2);
    if (b % 2)
        return res * res * a;
    else
        return res * res;
}
```

Cách thứ hai thực hiện cùng nhiệm vụ mà không dùng đệ quy.
Nó tính các lũy thừa trong một vòng lặp và nhân những giá trị có bit tương ứng được bật trong $n$.
Mặc dù hai cách có cùng độ phức tạp, phiên bản lặp thường nhanh hơn trong thực tế vì không có chi phí của các lời gọi đệ quy.

```cpp
long long binpow(long long a, long long b) {
    long long res = 1;
    while (b > 0) {
        if (b & 1)
            res = res * a;
        a = a * a;
        b >>= 1;
    }
    return res;
}
```

## Ứng dụng

### Tính hiệu quả lũy thừa lớn theo mô-đun

**Bài toán:**
Tính $x^n \bmod m$.
Đây là một phép toán rất phổ biến, chẳng hạn được dùng khi tính [nghịch đảo nhân mô-đun](module-inverse.md).

**Lời giải:**
Vì phép lấy mô-đun tương thích với phép nhân ($a \cdot b \equiv (a \bmod m) \cdot (b \bmod m) \pmod m$), ta có thể dùng trực tiếp thuật toán trên và thay mỗi phép nhân bằng phép nhân mô-đun:

```cpp
long long binpow(long long a, long long b, long long m) {
    a %= m;
    long long res = 1;
    while (b > 0) {
        if (b & 1)
            res = res * a % m;
        a = a * a % m;
        b >>= 1;
    }
    return res;
}
```

**Lưu ý:**
Có thể tăng tốc thuật toán khi $b >> m$.
Nếu $m$ dương và $\gcd(x, m) = 1$, thì với $m$ nguyên tố ta có $x^n \equiv x^{n \bmod (m-1)} \pmod{m}$, còn với $m$ hợp số ta có $x^n \equiv x^{n \bmod{\phi(m)}} \pmod{m}$.
Điều này suy ra trực tiếp từ định lý nhỏ Fermat và định lý Euler; xem bài [Nghịch đảo mô-đun](module-inverse.md#fermat-euler) để biết thêm chi tiết.

### Tính hiệu quả số Fibonacci

**Bài toán:** Tính số Fibonacci thứ $n$, $F_n$.

**Lời giải:** Xem thêm bài [Fibonacci Number](fibonacci-numbers.md).
Ở đây ta chỉ trình bày tổng quan thuật toán.
Để tính số Fibonacci tiếp theo, ta chỉ cần hai số trước đó vì $F_n = F_{n-1} + F_{n-2}$.
Ta có thể xây dựng một ma trận $2 \times 2$ mô tả phép biến đổi này:
chuyển từ $F_i$ và $F_{i+1}$ sang $F_{i+1}$ và $F_{i+2}$.
Chẳng hạn, áp dụng phép biến đổi này lên cặp $F_0$ và $F_1$ sẽ cho $F_1$ và $F_2$.
Do đó ta có thể nâng ma trận biến đổi lên lũy thừa $n$ để tìm $F_n$ trong thời gian $O(\log n)$.

### Áp dụng một hoán vị $k$ lần { data-toc-label='Applying a permutation <script type="math/tex">k</script> times' }

**Bài toán:** Cho một dãy độ dài $n$. Áp dụng một hoán vị đã cho lên dãy đó $k$ lần.

**Lời giải:** Chỉ cần nâng hoán vị lên lũy thừa $k$ bằng lũy thừa nhị phân, sau đó áp dụng nó lên dãy. Độ phức tạp là $O(n \log k)$.

```cpp
vector<int> applyPermutation(vector<int> sequence, vector<int> permutation) {
    vector<int> newSequence(sequence.size());
    for(int i = 0; i < sequence.size(); i++) {
        newSequence[i] = sequence[permutation[i]];
    }
    return newSequence;
}

vector<int> permute(vector<int> sequence, vector<int> permutation, long long k) {
    while (k > 0) {
        if (k & 1) {
            sequence = applyPermutation(sequence, permutation);
        }
        permutation = applyPermutation(permutation, permutation);
        k >>= 1;
    }
    return sequence;
}
```

**Lưu ý:** Bài toán này có thể giải hiệu quả hơn trong thời gian tuyến tính bằng cách xây dựng đồ thị hoán vị và xét từng chu trình độc lập. Khi đó ta tính $k$ theo mô-đun kích thước chu trình rồi xác định vị trí cuối cùng của mỗi số thuộc chu trình đó.

### Áp dụng nhanh một tập phép biến đổi hình học lên một tập điểm

**Bài toán:** Cho $n$ điểm $p_i$, áp dụng $m$ phép biến đổi lên mỗi điểm. Mỗi phép biến đổi có thể là tịnh tiến, co giãn hoặc quay quanh một trục cho trước theo một góc cho trước. Ngoài ra còn có phép toán "loop" áp dụng một danh sách phép biến đổi $k$ lần; các "loop" có thể lồng nhau. Hãy áp dụng toàn bộ phép biến đổi nhanh hơn $O(n \cdot length)$, trong đó $length$ là tổng số phép biến đổi sau khi khai triển mọi "loop".

**Lời giải:** Xét tác động của từng loại phép biến đổi lên tọa độ:

* Phép tịnh tiến: cộng một hằng số khác nhau vào mỗi tọa độ.
* Phép co giãn: nhân mỗi tọa độ với một hằng số khác nhau.
* Phép quay: phép biến đổi phức tạp hơn (không đi vào chi tiết ở đây), nhưng mỗi tọa độ mới vẫn có thể biểu diễn dưới dạng tổ hợp tuyến tính của các tọa độ cũ.

Như vậy, mỗi phép biến đổi có thể được biểu diễn bằng một phép biến đổi tuyến tính trên các tọa độ. Do đó một phép biến đổi có thể viết thành ma trận $4 \times 4$ dạng:

$$\begin{pmatrix}
a_{11} & a_ {12} & a_ {13} & a_ {14} \\
a_{21} & a_ {22} & a_ {23} & a_ {24} \\
a_{31} & a_ {32} & a_ {33} & a_ {34} \\
a_{41} & a_ {42} & a_ {43} & a_ {44}
\end{pmatrix}$$

Khi nhân ma trận đó với một vector chứa các tọa độ cũ và một tọa độ bổ sung bằng $1$, ta nhận được vector chứa các tọa độ mới với tọa độ bổ sung đó vẫn bằng $1$:

$$\begin{pmatrix} x & y & z & 1 \end{pmatrix} \cdot
\begin{pmatrix}
a_{11} & a_ {12} & a_ {13} & a_ {14} \\
a_{21} & a_ {22} & a_ {23} & a_ {24} \\
a_{31} & a_ {32} & a_ {33} & a_ {34} \\
a_{41} & a_ {42} & a_ {43} & a_ {44}
\end{pmatrix}
 = \begin{pmatrix} x' & y' & z' & 1 \end{pmatrix}$$

(Tại sao lại thêm một tọa độ thứ tư giả? Đây chính là ưu điểm của [tọa độ thuần nhất](https://en.wikipedia.org/wiki/Homogeneous_coordinates), một công cụ rất hữu ích trong đồ họa máy tính. Nếu không có tọa độ này, các phép biến đổi affine như tịnh tiến không thể biểu diễn bằng một phép nhân ma trận duy nhất vì ta phải _cộng_ một hằng số vào tọa độ. Trong không gian nhiều chiều hơn, phép biến đổi affine trở thành phép biến đổi tuyến tính.)

Một số ví dụ về biểu diễn ma trận của các phép biến đổi:

* Phép tịnh tiến: dịch tọa độ $x$ thêm $5$, tọa độ $y$ thêm $7$ và tọa độ $z$ thêm $9$.

$$\begin{pmatrix}
1 & 0 & 0 & 0 \\
0 & 1 & 0 & 0 \\
0 & 0 & 1 & 0 \\
5 & 7 & 9 & 1
\end{pmatrix}$$

* Phép co giãn: nhân tọa độ $x$ với $10$ và hai tọa độ còn lại với $5$.

$$\begin{pmatrix}
10 & 0 & 0 & 0 \\
0 & 5 & 0 & 0 \\
0 & 0 & 5 & 0 \\
0 & 0 & 0 & 1
\end{pmatrix}$$

* Phép quay: quay $\theta$ độ quanh trục $x$ theo quy tắc bàn tay phải (ngược chiều kim đồng hồ).

$$\begin{pmatrix}
1 & 0 & 0 & 0 \\
0 & \cos \theta & -\sin \theta & 0 \\
0 & \sin \theta & \cos \theta & 0 \\
0 & 0 & 0 & 1
\end{pmatrix}$$

Khi mọi phép biến đổi đã được biểu diễn dưới dạng ma trận, cả chuỗi phép biến đổi có thể biểu diễn bằng tích các ma trận đó, còn một "loop" lặp $k$ lần có thể biểu diễn bằng cách nâng ma trận lên lũy thừa $k$, tính bằng lũy thừa nhị phân trong $O(\log{k})$. Ta có thể tính trước ma trận đại diện cho toàn bộ phép biến đổi trong $O(m \log{k})$, sau đó áp dụng nó lên mỗi điểm trong số $n$ điểm trong $O(n)$, cho tổng độ phức tạp $O(n + m \log{k})$.


### Số đường đi độ dài $k$ trong đồ thị { data-toc-label='Number of paths of length <script type="math/tex">k</script> in a graph' }

**Bài toán:** Cho một đồ thị có hướng không trọng số gồm $n$ đỉnh, tìm số đường đi độ dài $k$ từ một đỉnh $u$ bất kỳ tới một đỉnh $v$ bất kỳ.

**Lời giải:** Bài toán này được trình bày chi tiết hơn trong [một bài riêng](../graph/fixed_length_paths.md). Thuật toán nâng ma trận kề $M$ của đồ thị lên lũy thừa $k$; $m_{ij} = 1$ nếu có cạnh từ $i$ tới $j$, và bằng $0$ nếu không. Sau khi nâng lũy thừa, $m_{ij}$ là số đường đi độ dài $k$ từ $i$ tới $j$. Độ phức tạp là $O(n^3 \log k)$.

**Lưu ý:** Bài riêng đó cũng xét một biến thể: cạnh có trọng số và cần tìm đường đi trọng số nhỏ nhất chứa đúng $k$ cạnh. Bài toán này cũng được giải bằng cách nâng lũy thừa ma trận kề. Khi đó phần tử ma trận là trọng số cạnh từ $i$ tới $j$, hoặc $\infty$ nếu không có cạnh.
Thay vì phép nhân ma trận thông thường, ta dùng một phép toán biến đổi:
thay phép nhân hai giá trị bằng phép cộng, và thay phép cộng tổng bằng phép lấy nhỏ nhất.
Cụ thể: $result_{ij} = \min\limits_{1\ \leq\ k\ \leq\ n}(a_{ik} + b_{kj})$.

### Biến thể của lũy thừa nhị phân: nhân hai số theo mô-đun $m$ { data-toc-label='Variation of binary exponentiation: multiplying two numbers modulo <script type="math/tex">m</script>' }

**Bài toán:** Nhân hai số $a$ và $b$ theo mô-đun $m$. $a$ và $b$ vừa với các kiểu dữ liệu có sẵn, nhưng tích của chúng quá lớn để chứa trong số nguyên 64 bit. Mục tiêu là tính $a \cdot b \pmod m$ mà không dùng số nguyên độ chính xác tùy ý.

**Lời giải:** Ta áp dụng cùng cách xây dựng nhị phân như trên nhưng dùng phép cộng thay cho phép nhân. Nói cách khác, ta "khai triển" phép nhân hai số thành $O (\log m)$ phép cộng và nhân đôi, mà bản chất cũng là một phép cộng.

$$a \cdot b = \begin{cases}
0 &\text{if }a = 0 \\
2 \cdot \frac{a}{2} \cdot b &\text{if }a > 0 \text{ and }a \text{ even} \\
2 \cdot \frac{a-1}{2} \cdot b + b &\text{if }a > 0 \text{ and }a \text{ odd}
\end{cases}$$

**Lưu ý:** Có thể giải bài này theo cách khác bằng số thực dấu phẩy động. Trước hết tính biểu thức $\frac{a \cdot b}{m}$ bằng số thực rồi ép về số nguyên không dấu $q$. Sau đó lấy $a \cdot b$ trừ $q \cdot m$ bằng số học số nguyên không dấu và lấy mô-đun $m$ để thu được đáp án. Cách này có vẻ không đáng tin cậy, nhưng rất nhanh và dễ cài đặt. Xem thêm [tại đây](https://cs.stackexchange.com/questions/77016/modular-multiplication).

## Bài tập luyện tập

* [UVa 1230 - MODEX](http://uva.onlinejudge.org/index.php?option=com_onlinejudge&Itemid=8&category=24&page=show_problem&problem=3671)
* [UVa 374 - Big Mod](http://uva.onlinejudge.org/index.php?option=com_onlinejudge&Itemid=8&category=24&page=show_problem&problem=310)
* [UVa 11029 - Leading and Trailing](https://uva.onlinejudge.org/index.php?option=onlinejudge&page=show_problem&problem=1970)
* [Codeforces - Parking Lot](http://codeforces.com/problemset/problem/630/I)
* [leetcode - Count good numbers](https://leetcode.com/problems/count-good-numbers/)
* [Codechef - Chef and Riffles](https://www.codechef.com/JAN221B/problems/RIFFLES)
* [Codeforces - Decoding Genome](https://codeforces.com/contest/222/problem/E)
* [Codeforces - Neural Network Country](https://codeforces.com/contest/852/problem/B)
* [Codeforces - Magic Gems](https://codeforces.com/problemset/problem/1117/D)
* [SPOJ - The last digit](http://www.spoj.com/problems/LASTDIG/)
* [SPOJ - Locker](http://www.spoj.com/problems/LOCKER/)
* [LA - 3722 Jewel-eating Monsters](https://vjudge.net/problem/UVALive-3722)
* [SPOJ - Just add it](http://www.spoj.com/problems/ZSUM/)
* [Codeforces - Stairs and Lines](https://codeforces.com/contest/498/problem/E)
