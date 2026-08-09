---
tags:
  - Translated
e_maxx_link: gray_code
translation:
  source: algebra/gray-code.md
  source_commit: a7926d30b75ef8481b5068d49cf6b2be628a0312
  status: draft
  last_synced: 2026-08-09
---

# Mã Gray

Mã Gray là một hệ biểu diễn nhị phân trong đó hai giá trị liên tiếp chỉ khác nhau đúng một bit. 

Ký hiệu $G(n)$ là biểu diễn của số $n$ bằng mã Gray. Dãy mã Gray của các số 3 bit là: 000, 001, 011, 010, 110, 111, 101, 100, nên $G(4) = (110)_2 = 6$. 
Chẳng hạn, $G(3) = (010)_2$ và $G(4) = (110)_2$ khác nhau đúng một bit, là bit ngoài cùng bên trái. Tương tự, $G(4) = 110$ và $G(5) = (111)_2$ khác nhau đúng một bit, là bit ngoài cùng bên phải. Tính chất này đúng với mọi cặp số liên tiếp. 

Mã này được Frank Gray phát minh vào năm 1953.

## Tìm mã Gray

Hãy xét các bit của số $n$ và các bit của số $G(n)$. Nhận xét rằng bit thứ $i$ của $G(n)$ bằng 1 khi và chỉ khi bit thứ $i$ của $n$ bằng 1 còn bit thứ $i + 1$ bằng 0, hoặc ngược lại (bit thứ $i$ bằng 0 và bit thứ $i + 1$ bằng 1). Vì vậy, $G(n) = n \oplus (n >> 1)$:  

```cpp
int g (int n) {
    return n ^ (n >> 1);
}
```

## Khôi phục số từ mã Gray

Cho mã Gray $g$, hãy khôi phục số ban đầu $n$.

Ta đi từ các bit cao nhất xuống các bit thấp nhất (bit thấp nhất có chỉ số 1 và bit cao nhất có chỉ số $k$). Quan hệ giữa các bit $n_i$ của số $n$ và các bit $g_i$ của số $g$ là:

$$\begin{align}
  n_k &= g_k, \\
  n_{k-1} &= g_{k-1} \oplus n_k = g_k \oplus g_{k-1}, \\
  n_{k-2} &= g_{k-2} \oplus n_{k-1} = g_k \oplus g_{k-1} \oplus g_{k-2}, \\
  n_{k-3} &= g_{k-3} \oplus n_{k-2} = g_k \oplus g_{k-1} \oplus g_{k-2} \oplus g_{k-3},
  \vdots
\end{align}$$

Cách đơn giản nhất để viết thành code là:

```cpp
int rev_g (int g) {
  int n = 0;
  for (; g; g >>= 1)
    n ^= g;
  return n;
}
```

## Ứng dụng thực tế
Mã Gray có nhiều ứng dụng hữu ích, đôi khi khá bất ngờ:

*   Mã Gray $n$ bit tạo thành một chu trình Hamilton trên siêu lập phương, trong đó mỗi bit tương ứng với một chiều. 

*   Mã Gray được dùng để giảm sai số khi chuyển đổi tín hiệu số sang tín hiệu tương tự (chẳng hạn trong cảm biến). 

*   Mã Gray có thể được dùng để giải bài toán Tháp Hà Nội.
    Gọi $n$ là số đĩa. Bắt đầu với mã Gray độ dài $n$ gồm toàn bit 0 ($G(0)$), rồi lần lượt chuyển giữa các mã Gray liên tiếp (từ $G(i)$ sang $G(i+1)$).
    Bit thứ $i$ của mã Gray hiện tại biểu diễn đĩa thứ $n$ 
    (bit thấp nhất tương ứng với đĩa nhỏ nhất và bit cao nhất tương ứng với đĩa lớn nhất). 
    Vì mỗi bước chỉ có đúng một bit thay đổi, ta có thể xem việc đổi bit thứ $i$ là di chuyển đĩa thứ $i$.
    Nhận xét rằng ở mỗi bước (trừ vị trí bắt đầu và kết thúc), mỗi đĩa (trừ đĩa nhỏ nhất) chỉ có đúng một cách di chuyển hợp lệ.
    Đĩa nhỏ nhất luôn có hai cách di chuyển, nhưng có một chiến lược luôn dẫn đến đáp án:
    nếu $n$ lẻ thì dãy di chuyển của đĩa nhỏ nhất có dạng $f \to t \to r \to f \to t \to r \to ...$
    trong đó $f$ là cọc ban đầu, $t$ là cọc đích và $r$ là cọc còn lại, còn 
    nếu $n$ chẵn: $f \to r \to t \to f \to r \to t \to ...$.

*   Mã Gray cũng được dùng trong lý thuyết thuật toán di truyền.

**Ghi chú bản dịch:** Trong bullet về Tháp Hà Nội, câu nguồn ghi “bit thứ i” biểu diễn “đĩa thứ n”, nhưng câu kế tiếp lại dùng việc đổi bit thứ i như di chuyển đĩa thứ i. Theo ngữ cảnh, “đĩa thứ n” nhiều khả năng là typo và phải là “đĩa thứ i”.

## Bài tập luyện tập
*   <a href="https://cses.fi/problemset/task/2205">Gray Code &nbsp;&nbsp;&nbsp;&nbsp; [Độ khó: dễ]</a>
*   <a href="http://codeforces.com/problemsets/acmsguru/problem/99999/249">SGU #249 <b>"Matrix"</b> &nbsp;&nbsp;&nbsp;&nbsp; [Độ khó: trung bình]</a>
