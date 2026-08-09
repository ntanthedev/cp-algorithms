---
tags:
  - Translated
e_maxx_link: fibonacci_numbers
translation:
  source: algebra/fibonacci-numbers.md
  source_commit: 6d18015f0fe63987e28d70d027914500a35d506d
  status: draft
  last_synced: 2026-08-09
---

# Số Fibonacci

Dãy Fibonacci được định nghĩa như sau:

$$F_0 = 0, F_1 = 1, F_n = F_{n-1} + F_{n-2}$$

Các phần tử đầu tiên của dãy ([OEIS A000045](http://oeis.org/A000045)) là:

$$0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, ...$$

## Tính chất

Các số Fibonacci có rất nhiều tính chất thú vị. Dưới đây là một vài tính chất:

* Đồng nhất thức Cassini:
  
$$F_{n-1} F_{n+1} - F_n^2 = (-1)^n$$

>Có thể chứng minh bằng quy nạp. Knuth có một chứng minh chỉ trong một dòng bằng cách lấy định thức của dạng ma trận 2x2 ở phía dưới.

* Quy tắc "cộng":
  
$$F_{n+k} = F_k F_{n+1} + F_{k-1} F_n$$

* Áp dụng đồng nhất thức trên cho trường hợp $k = n$, ta được:
  
$$F_{2n} = F_n (F_{n+1} + F_{n-1})$$

* Từ đây, bằng quy nạp ta có thể chứng minh rằng với mọi số nguyên dương $k$,  $F_{nk}$ là bội của $F_n$.

* Mệnh đề đảo cũng đúng: nếu $F_m$ là bội của $F_n$, thì $m$ là bội của $n$.

**Ghi chú bản dịch:** Mệnh đề đảo ở trên có ngoại lệ khi chỉ số n bằng 2, vì số Fibonacci thứ 2 bằng 1 nên là ước của mọi số Fibonacci. Chẳng hạn số Fibonacci thứ 3 là bội của số Fibonacci thứ 2 nhưng 3 không phải là bội của 2. Với chỉ số n nguyên dương khác 2, mệnh đề đúng.

* Đồng nhất thức UCLN:
  
$$GCD(F_m, F_n) = F_{GCD(m, n)}$$

* Các số Fibonacci là những đầu vào tạo ra trường hợp xấu nhất cho thuật toán Euclid (xem định lý Lamé trong bài [Thuật toán Euclid](euclid-algorithm.md))

## Mã Fibonacci

Ta có thể dùng dãy Fibonacci để mã hóa các số nguyên dương thành các từ mã nhị phân. Theo định lý Zeckendorf, mọi số tự nhiên $n$ đều có thể được biểu diễn duy nhất thành tổng các số Fibonacci:

$$N = F_{k_1} + F_{k_2} + \ldots + F_{k_r}$$

sao cho $k_1 \ge k_2 + 2,\ k_2 \ge k_3 + 2,\  \ldots,\  k_r \ge 2$ (tức biểu diễn không được dùng hai số Fibonacci liên tiếp).

Từ đó suy ra mọi số đều có thể được mã hóa duy nhất bằng mã Fibonacci.
Ta có thể mô tả biểu diễn này bằng mã nhị phân $d_0 d_1 d_2 \dots d_s 1$, trong đó $d_i$ bằng $1$ nếu $F_{i+2}$ được dùng trong biểu diễn.
Ta nối thêm một $1$ vào cuối mã để đánh dấu kết thúc từ mã.
Đây là vị trí duy nhất xuất hiện hai bit 1 liên tiếp.

$$\begin{eqnarray}
1 &=& 1 &=& F_2 &=& (11)_F \\
2 &=& 2 &=& F_3 &=& (011)_F \\
6 &=& 5 + 1 &=& F_5 + F_2 &=& (10011)_F \\
8 &=& 8 &=& F_6 &=& (000011)_F \\
9 &=& 8 + 1 &=& F_6 + F_2 &=& (100011)_F \\
19 &=& 13 + 5 + 1 &=& F_7 + F_5 + F_2 &=& (1001011)_F
\end{eqnarray}$$

Có thể mã hóa một số nguyên $n$ bằng thuật toán tham lam đơn giản:

1. Duyệt các số Fibonacci từ lớn nhất xuống nhỏ nhất cho đến khi tìm được một số nhỏ hơn hoặc bằng $n$.

2. Giả sử số đó là $F_i$. Trừ $F_i$ khỏi $n$ và đặt $1$ vào vị trí $i-2$ của từ mã (đánh chỉ số từ 0, từ bit trái nhất sang bit phải nhất).

3. Lặp lại cho đến khi phần còn lại bằng không.

4. Thêm một $1$ vào cuối từ mã để đánh dấu kết thúc.

Để giải mã một từ mã, trước hết bỏ số $1$ cuối cùng. Sau đó, nếu bit thứ $i$ được bật (đánh chỉ số từ 0, từ bit trái nhất sang bit phải nhất), cộng $F_{i+2}$ vào số cần tìm.


## Công thức cho số Fibonacci thứ $n^{\text{th}}$ { data-toc-label="Formulas for the <script type='math/tex'>n</script>-th Fibonacci number" }

### Biểu thức dạng đóng

Có một công thức được gọi là "công thức Binet", mặc dù Moivre đã biết công thức này từ trước:

$$F_n = \frac{\left(\frac{1 + \sqrt{5}}{2}\right)^n - \left(\frac{1 - \sqrt{5}}{2}\right)^n}{\sqrt{5}}$$

Công thức này dễ chứng minh bằng quy nạp, nhưng cũng có thể suy ra bằng khái niệm hàm sinh hoặc bằng cách giải một phương trình hàm.

Có thể nhận thấy ngay rằng giá trị tuyệt đối của số hạng thứ hai luôn nhỏ hơn $1$ và giảm rất nhanh theo hàm mũ. Vì vậy, chỉ riêng số hạng thứ nhất đã "gần như" bằng $F_n$. Có thể viết chặt chẽ như sau: 

$$F_n = \left[\frac{\left(\frac{1 + \sqrt{5}}{2}\right)^n}{\sqrt{5}}\right]$$

trong đó dấu ngoặc vuông biểu thị phép làm tròn tới số nguyên gần nhất.

Do hai công thức này đòi hỏi độ chính xác rất cao khi tính toán với số thực, chúng ít hữu ích trong tính toán thực tế.

### Tính Fibonacci trong thời gian tuyến tính

Có thể dễ dàng tìm số Fibonacci thứ $n$ trong $O(n)$ bằng cách lần lượt tính các số cho đến $n$. Tuy nhiên, như ta sẽ thấy, còn có những cách nhanh hơn.

Ta có thể bắt đầu với cách lặp, tận dụng công thức $F_n = F_{n-1} + F_{n-2}$; theo mô tả của nguồn, ta sẽ tiền tính các giá trị này trong một mảng và chú ý hai trường hợp cơ sở $F_0$ và $F_1$.

```{.cpp file=fibonacci_linear}
int fib(int n) {
    int a = 0;
    int b = 1;
    for (int i = 0; i < n; i++) {
        int tmp = a + b;
        a = b;
        b = tmp;
    }
    return a;
}
```

Theo mô tả nguồn, cách này cho lời giải tuyến tính, thời gian $O(n)$, đồng thời lưu mọi giá trị đứng trước $n$ trong dãy.

**Ghi chú bản dịch:** Phần mô tả nguồn nói tiền tính trong một mảng và lưu toàn bộ các giá trị trước đó, nhưng phần cài đặt phía trên thực tế chỉ giữ hai số Fibonacci liên tiếp. Vì vậy, chính cài đặt này dùng bộ nhớ hằng số chứ không lưu toàn bộ dãy.

### Dạng ma trận

Để chuyển từ $(F_n, F_{n-1})$ sang $(F_{n+1}, F_n)$, ta có thể biểu diễn hệ thức truy hồi tuyến tính bằng phép nhân ma trận 2x2:

$$
\begin{pmatrix}
1 & 1 \\
1 & 0
\end{pmatrix}
\begin{pmatrix}
F_n \\
F_{n-1}
\end{pmatrix}
=
\begin{pmatrix}
F_n + F_{n-1}  \\
F_{n}
\end{pmatrix}
=
\begin{pmatrix}
F_{n+1}  \\
F_{n}
\end{pmatrix}
$$

Ta có thể xem việc áp dụng hệ thức truy hồi nhiều lần là phép nhân ma trận lặp; cách biểu diễn này có nhiều tính chất hữu ích. Cụ thể,

$$
\begin{pmatrix}
1 & 1 \\
1 & 0
\end{pmatrix}^n
\begin{pmatrix}
F_1 \\
F_0
\end{pmatrix}
=
\begin{pmatrix}
F_{n+1}  \\
F_{n}
\end{pmatrix}
$$

trong đó $F_1 = 1, F_0 = 0$. 
Thực tế, do 

$$
\begin{pmatrix} 1 & 1 \\ 1 & 0 \end{pmatrix}
= \begin{pmatrix} F_2 & F_1 \\ F_1 & F_0 \end{pmatrix}
$$

ta có thể dùng trực tiếp ma trận:

$$
\begin{pmatrix} 1 & 1 \\ 1 & 0 \end{pmatrix}^n
= \begin{pmatrix} F_{n+1} & F_n \\ F_n & F_{n-1} \end{pmatrix}
$$

Do đó, để tìm $F_n$ trong thời gian $O(\log  n)$, ta cần nâng ma trận lên lũy thừa n. (Xem [Lũy thừa nhị phân](binary-exp.md))

```{.cpp file=fibonacci_matrix}
struct matrix {
    long long mat[2][2];
    matrix friend operator *(const matrix &a, const matrix &b){
        matrix c;
        for (int i = 0; i < 2; i++) {
          for (int j = 0; j < 2; j++) {
              c.mat[i][j] = 0;
              for (int k = 0; k < 2; k++) {
                  c.mat[i][j] += a.mat[i][k] * b.mat[k][j];
              }
          }
        }
        return c;
    }
};

matrix matpow(matrix base, long long n) {
    matrix ans{ {
      {1, 0},
      {0, 1}
    } };
    while (n) {
        if(n&1)
            ans = ans*base;
        base = base*base;
        n >>= 1;
    }
    return ans;
}

long long fib(int n) {
    matrix base{ {
      {1, 1},
      {1, 0}
    } };
    return matpow(base, n).mat[0][1];
}
```

### Phương pháp nhân đôi nhanh

Khai triển biểu thức ma trận ở trên với $n = 2\cdot k$

$$
\begin{pmatrix}
F_{2k+1} & F_{2k}\\
F_{2k} & F_{2k-1}
\end{pmatrix}
=
\begin{pmatrix}
1 & 1\\
1 & 0
\end{pmatrix}^{2k}
=
\begin{pmatrix}
F_{k+1} & F_{k}\\
F_{k} & F_{k-1}
\end{pmatrix}
^2
$$

ta thu được các phương trình đơn giản hơn:

$$ \begin{align}
F_{2k+1} &= F_{k+1}^2 + F_{k}^2 \\
F_{2k} &= F_k(F_{k+1}+F_{k-1}) = F_k (2F_{k+1} - F_{k})\\
\end{align}.$$

Nhờ hai phương trình trên, ta có thể dễ dàng tính các số Fibonacci bằng đoạn mã sau:

```{.cpp file=fibonacci_doubling}
pair<int, int> fib (int n) {
    if (n == 0)
        return {0, 1};

    auto p = fib(n >> 1);
    int c = p.first * (2 * p.second - p.first);
    int d = p.first * p.first + p.second * p.second;
    if (n & 1)
        return {d, c + d};
    else
        return {c, d};
}
```
Đoạn mã trên trả về $F_n$ và $F_{n+1}$ dưới dạng một cặp.

## Tính tuần hoàn modulo p

Xét dãy Fibonacci modulo $p$. Ta sẽ chứng minh dãy này tuần hoàn.

Ta chứng minh bằng phản chứng. Xét $p^2 + 1$ cặp số Fibonacci đầu tiên khi lấy modulo $p$:

$$(F_0,\ F_1),\ (F_1,\ F_2),\ \ldots,\ (F_{p^2},\ F_{p^2 + 1})$$

Chỉ có $p$ số dư khác nhau modulo $p$ và nhiều nhất $p^2$ cặp số dư khác nhau, nên trong các cặp trên phải có ít nhất hai cặp giống nhau. Điều này đủ để chứng minh dãy tuần hoàn, vì một số Fibonacci được xác định bởi hai số đứng trước nó. Do đó, nếu hai cặp số liên tiếp lặp lại thì các số đứng sau chúng cũng sẽ lặp lại theo cùng cách.

Bây giờ chọn hai cặp có cùng số dư và có chỉ số nhỏ nhất trong dãy. Gọi hai cặp đó là $(F_a,\ F_{a + 1})$ và $(F_b,\ F_{b + 1})$. Ta sẽ chứng minh $a = 0$. Nếu điều này sai, sẽ tồn tại hai cặp đứng trước là $(F_{a-1},\ F_a)$ và $(F_{b-1},\ F_b)$, và theo hệ thức Fibonacci, hai cặp đứng trước này cũng cho cùng cặp số dư modulo p. Tuy nhiên, điều đó mâu thuẫn với việc ta đã chọn hai cặp có chỉ số nhỏ nhất, qua đó chứng minh không có tiền chu kỳ (tức dãy tuần hoàn ngay từ $F_0$).

## Bài tập luyện tập

* [SPOJ - Euclid Algorithm Revisited](http://www.spoj.com/problems/MAIN74/)
* [SPOJ - Fibonacci Sum](http://www.spoj.com/problems/FIBOSUM/)
* [HackerRank - Is Fibo](https://www.hackerrank.com/challenges/is-fibo/problem)
* [Project Euler - Even Fibonacci numbers](https://www.hackerrank.com/contests/projecteuler/challenges/euler002/problem)
* [DMOJ - Fibonacci Sequence](https://dmoj.ca/problem/fibonacci)
* [DMOJ - Fibonacci Sequence (Harder)](https://dmoj.ca/problem/fibonacci2)
* [DMOJ UCLV - Numbered sequence of pencils](https://dmoj.uclv.edu.cu/problem/secnum)
* [DMOJ UCLV - Fibonacci 2D](https://dmoj.uclv.edu.cu/problem/fibonacci)
* [DMOJ UCLV - fibonacci calculation](https://dmoj.uclv.edu.cu/problem/fibonaccicalculatio)
* [LightOJ -  Number Sequence](https://lightoj.com/problem/number-sequence)
* [Codeforces - C. Fibonacci](https://codeforces.com/problemset/gymProblem/102644/C)
* [Codeforces - A. Hexadecimal's theorem](https://codeforces.com/problemset/problem/199/A)
* [Codeforces - B. Blackboard Fibonacci](https://codeforces.com/problemset/problem/217/B)
* [Codeforces - E. Fibonacci Number](https://codeforces.com/problemset/problem/193/E)
