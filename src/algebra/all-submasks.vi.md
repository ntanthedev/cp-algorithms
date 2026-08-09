---
tags:
  - Translated
e_maxx_link: all_submasks
translation:
  source: algebra/all-submasks.md
  source_commit: 9169d23d4e5c24c509bfa88d886aedc86c6a063c
  status: draft
  last_synced: 2026-08-09
---

# Liệt kê mask con

## Liệt kê mọi mask con của một mask cho trước

Cho một bitmask $m$, ta muốn duyệt hiệu quả qua tất cả **mask con (submask)** của nó, tức các mask $s$ mà chỉ những bit đã xuất hiện trong mask $m$ mới có thể được bật.

Xét cách cài đặt thuật toán này dựa trên một mẹo thao tác bit:

```cpp
int s = m;
while (s > 0) {
 ... you can use s ...
 s = (s-1) & m;
}
```

hoặc dùng câu lệnh `for` gọn hơn:

```cpp
for (int s=m; s; s=(s-1)&m)
 ... you can use s ...
```

Trong cả hai cách viết trên, mask con bằng không sẽ không được xử lý. Ta có thể xử lý nó bên ngoài vòng lặp, hoặc dùng một cách viết kém gọn hơn, chẳng hạn:

```cpp
for (int s=m; ; s=(s-1)&m) {
 ... you can use s ...
 if (s==0)  break;
}
```

Ta hãy xem vì sao đoạn code trên duyệt qua mọi mask con của $m$, không lặp lại và theo thứ tự giảm dần.

Giả sử mask hiện tại là $s$ và ta muốn chuyển sang mask kế tiếp. Khi trừ mask $s$ đi một đơn vị, bit 1 ngoài cùng bên phải sẽ bị tắt, còn mọi bit ở bên phải nó trở thành 1. Sau đó ta loại bỏ những bit 1 "thừa" không thuộc mask $m$, vì chúng không thể xuất hiện trong một mask con của mask ban đầu. Ta thực hiện bước loại bỏ này bằng phép toán bit `(s-1) & m`. Kết quả là ta "cắt" mask $s-1$ về giá trị lớn nhất mà nó có thể nhận trong khi vẫn là một mask con hợp lệ, tức mask con kế tiếp sau $s$ theo thứ tự giảm dần.

Như vậy, thuật toán sinh tất cả mask con của mask đã cho theo thứ tự giảm dần và chỉ thực hiện hai phép toán ở mỗi vòng lặp.

Một trường hợp đặc biệt là $s = 0$. Sau khi thực hiện $s-1$, ta nhận được một mask có tất cả bit đều bằng 1 (biểu diễn bit của -1); sau `(s-1) & m`, $s$ sẽ trở lại bằng $m$. Vì vậy cần cẩn thận với mask $s = 0$: nếu vòng lặp không dừng tại 0, thuật toán có thể rơi vào vòng lặp vô hạn.

## Duyệt mọi mask cùng các mask con của chúng. Độ phức tạp $O(3^n)$

Trong nhiều bài toán, đặc biệt là các bài dùng quy hoạch động bitmask, ta cần duyệt qua mọi bitmask và với mỗi mask lại duyệt tất cả mask con của nó:

```cpp
for (int m=0; m<(1<<n); ++m)
	for (int s=m; s; s=(s-1)&m)
 ... s and m ...
```

Ta sẽ chứng minh vòng lặp trong cùng thực hiện tổng cộng $O(3^n)$ lượt.

**Chứng minh thứ nhất**: Xét bit thứ $i$. Có đúng ba khả năng:

1. bit đó không thuộc mask $m$ (và do đó cũng không thuộc mask con $s$),
2. bit đó thuộc $m$ nhưng không thuộc $s$, hoặc
3. bit đó thuộc cả $m$ lẫn $s$.

Vì có tổng cộng $n$ bit, ta có $3^n$ tổ hợp khác nhau.

**Chứng minh thứ hai**: Nếu mask $m$ có $k$ bit bằng 1 thì nó có $2^k$ mask con. Có tổng cộng $\binom{n}{k}$ mask có $k$ bit bằng 1 (xem [hệ số nhị thức](../combinatorics/binomial-coefficients.md)), nên tổng số cặp mask và mask con trên mọi mask là:

$$\sum_{k=0}^n \binom{n}{k} \cdot 2^k$$

Để tính tổng này, nhận xét rằng biểu thức trên chính là khai triển của $(1+2)^n$ theo định lý nhị thức. Vì vậy ta thu được $3^n$ tổ hợp, đúng như cần chứng minh.

## Bài tập luyện tập

* [Atcoder - Close Group](https://atcoder.jp/contests/abc187/tasks/abc187_f)
* [Codeforces - Nuclear Fusion](http://codeforces.com/problemset/problem/71/E)
* [Codeforces - Sandy and Nuts](http://codeforces.com/problemset/problem/599/E)
* [Uva 1439 - Exclusive Access 2](https://uva.onlinejudge.org/index.php?option=com_onlinejudge&Itemid=8&page=show_problem&problem=4185)
* [UVa 11825 - Hackers' Crackdown](https://uva.onlinejudge.org/index.php?option=com_onlinejudge&Itemid=8&page=show_problem&problem=2925)
