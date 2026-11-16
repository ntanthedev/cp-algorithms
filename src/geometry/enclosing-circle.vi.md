---
tags:
  - Original
translation:
  source: geometry/enclosing-circle.md
  source_commit: 9ae052a5b2d873c7859fef39b1eccc7841c20a24
  status: draft
  last_synced: 2026-11-16
---

# Đường tròn bao nhỏ nhất

Xét bài toán sau:

!!! example "[Library Checker - Minimum Enclosing Circle](https://judge.yosupo.jp/problem/minimum_enclosing_circle)"

    Cho $n \leq 10^5$ điểm $p_i=(x_i, y_i)$.

    Với mỗi $p_i$, hãy xác định điểm đó có nằm trên đường biên của đường tròn bao nhỏ nhất của $\{p_1,\dots,p_n\}$ hay không.

Ở đây, đường tròn bao nhỏ nhất (MEC) là đường tròn có bán kính nhỏ nhất có thể, chứa tất cả $n$ điểm ở bên trong hoặc trên đường biên. Bài toán có lời giải ngẫu nhiên đơn giản thoạt nhìn có vẻ chạy trong $O(n^3)$, nhưng thực tế có thời gian kỳ vọng $O(n)$.

Để hiểu rõ hơn lập luận bên dưới, trước hết cần nhận xét rằng lời giải của bài toán là duy nhất:

??? question "Vì sao MEC là duy nhất?"

    Xét cách dựng sau: Gọi $r$ là bán kính của MEC. Ta vẽ một đường tròn bán kính $r$ quanh mỗi điểm $p_1,\dots,p_n$. Về mặt hình học, tâm của các đường tròn bán kính $r$ bao phủ tất cả các điểm $p_1,\dots,p_n$ tạo thành giao của cả $n$ hình tròn.

    Nếu giao chỉ gồm một điểm thì điều đó đã chứng minh tính duy nhất. Ngược lại, giao là một hình có diện tích khác không, nên ta có thể giảm $r$ một lượng rất nhỏ mà giao vẫn khác rỗng. Điều này mâu thuẫn với giả thiết rằng $r$ là bán kính nhỏ nhất có thể của đường tròn bao.

    Bằng lập luận tương tự, ta cũng có thể chứng minh tính duy nhất của MEC khi yêu cầu thêm rằng nó đi qua một điểm cho trước $p_i$ hoặc hai điểm $p_i$ và $p_j$ (nó vẫn duy nhất vì bán kính xác định duy nhất đường tròn).

    Một cách khác là giả sử có hai MEC, rồi nhận thấy giao của chúng (đã chứa các điểm $p_1,\dots,p_n$) phải có đường kính nhỏ hơn các đường tròn ban đầu, nên có thể được bao bởi một đường tròn nhỏ hơn.

## Thuật toán Welzl

Để ngắn gọn, ký hiệu $\operatorname{mec}(p_1,\dots,p_n)$ là MEC của $\{p_1,\dots,p_n\}$ và đặt $P_i = \{p_1,\dots,p_i\}$.

Thuật toán được Welzl [đề xuất](https://doi.org/10.1007/BFb0038202) lần đầu năm 1991 như sau:

1. Hoán vị ngẫu nhiên dãy điểm đầu vào.
2. Duy trì ứng viên MEC hiện tại $C$, bắt đầu với $C = \operatorname{mec}(p_1, p_2)$.
3. Duyệt $i=3..n$ và kiểm tra $p_i \in C$.
    1. Nếu $p_i \in C$ thì $C$ là MEC của $P_i$.
    2. Nếu không, gán $C = \operatorname{mec}(p_i, p_1)$ rồi duyệt $j=2..i$ và kiểm tra $p_j \in C$.
        1. Nếu $p_j \in C$ thì $C$ là MEC của $P_j$ trong số các đường tròn đi qua $p_i$.
        2. Nếu không, gán $C=\operatorname{mec}(p_i, p_j)$ rồi duyệt $k=1..j$ và kiểm tra $p_k \in C$.
            1. Nếu $p_k \in C$ thì $C$ là MEC của $P_k$ trong số các đường tròn đi qua $p_i$ và $p_j$.
            2. Nếu không, $C=\operatorname{mec}(p_i,p_j,p_k)$ là MEC của $P_k$ trong số các đường tròn đi qua $p_i$ và $p_j$.

Mỗi cấp lồng nhau đều duy trì một bất biến: $C$ là MEC trong số các đường tròn đồng thời đi qua $0$, $1$ hoặc $2$ điểm được cho thêm. Mỗi khi vòng lặp bên trong kết thúc, bất biến của nó trở thành tương đương với bất biến của lượt lặp hiện tại ở vòng ngoài. Nhờ đó, toàn bộ thuật toán được đảm bảo _đúng đắn_.

Tạm bỏ qua một số chi tiết kỹ thuật, có thể cài đặt toàn bộ thuật toán bằng C++ như sau:

```cpp
struct point {...};

// Is represented by 2 or 3 points on its circumference
struct mec {...};

bool inside(mec const& C, point p) {
    return ...;
}

// Choose some good generator of randomness for the shuffle
mt19937_64 gen(...);
mec enclosing_circle(vector<point> &p) {
    int n = p.size();
    ranges::shuffle(p, gen);
    auto C = mec{p[0], p[1]};
    for(int i = 0; i < n; i++) {
        if(!inside(C, p[i])) {
            C = mec{p[i], p[0]};
            for(int j = 0; j < i; j++) {
                if(!inside(C, p[j])) {
                    C = mec{p[i], p[j]};
                    for(int k = 0; k < j; k++) {
                        if(!inside(C, p[k])) {
                            C = mec{p[i], p[j], p[k]};
                        }
                    }
                }
            }
        }
    }
    return C;
}
```

Ta kỳ vọng việc kiểm tra một điểm $p_i$ nằm trong MEC của $2$ hoặc $3$ điểm có thể thực hiện trong $O(1)$ (sẽ bàn sau). Dù vậy, các vòng lặp lồng nhau khiến thuật toán trên có vẻ tốn $O(n^3)$ trong trường hợp xấu nhất. Vậy tại sao ta khẳng định thời gian kỳ vọng là tuyến tính? Hãy cùng tìm hiểu!

### Phân tích độ phức tạp

Vòng lặp trong cùng (theo $k$) rõ ràng có thời gian kỳ vọng $O(j)$ thao tác. Vậy còn vòng lặp theo $j$?

Vòng này chỉ kích hoạt vòng tiếp theo nếu $p_j$ nằm trên biên của MEC của $P_j$ đồng thời đi qua điểm $i$, _và việc bỏ $p_j$ làm đường tròn nhỏ đi_. Trong tất cả các điểm của $P_j$ chỉ có nhiều nhất $2$ điểm có tính chất đó, vì nếu có hơn $2$ điểm của $P_j$ trên biên thì sau khi bỏ bất kỳ điểm nào vẫn còn ít nhất $3$ điểm trên biên, đủ để xác định duy nhất đường tròn.

Nói cách khác, sau phép xáo trộn ngẫu nhiên ban đầu, xác suất để $p_j$ là một trong nhiều nhất hai điểm không may đó không vượt quá $\frac{2}{j}$. Cộng trên mọi $j$ từ $1$ đến $i$, ta có thời gian kỳ vọng

$$
\sum\limits_{j=1}^i \frac{2}{j} \cdot O(j) = O(i).
$$

Hoàn toàn tương tự, ta cũng có thể chứng minh vòng lặp ngoài cùng có thời gian kỳ vọng $O(n)$.

### Kiểm tra một điểm thuộc MEC của 2 hoặc 3 điểm

Bây giờ hãy xét chi tiết cài đặt `point` và `mec`. Trong bài toán này, dùng [std::complex](https://codeforces.com/blog/entry/22175) làm lớp biểu diễn điểm đặc biệt hữu ích:

```cpp
using ftype = int64_t;
using point = complex<ftype>;
```

Nhắc lại, số phức có dạng $x+yi$, với $i^2=-1$ và $x, y \in \mathbb R$. Trong C++, số phức như vậy được biểu diễn bằng điểm hai chiều $(x, y)$. Số phức đã hỗ trợ các phép tuyến tính cơ bản theo từng thành phần (cộng, nhân với số thực); phép nhân và chia số phức còn mang ý nghĩa hình học nhất định.

Không đi quá sâu vào chi tiết, ta nêu tính chất quan trọng nhất cho bài toán này: nhân hai số phức cộng các góc cực của chúng (đo từ $Ox$ ngược chiều kim đồng hồ), còn lấy liên hợp (tức đổi $z=x+yi$ thành $\overline{z} = x-yi$) nhân góc cực với $-1$. Nhờ đó, ta có thể xây dựng những tiêu chí rất đơn giản để kiểm tra một điểm $z$ có nằm trong MEC của $2$ hoặc $3$ điểm cụ thể hay không.

#### MEC của 2 điểm

Với $2$ điểm $a$ và $b$, MEC của chúng đơn giản là đường tròn tâm $\frac{a+b}{2}$ và bán kính $\frac{|a-b|}{2}$, hay đường tròn có đường kính $ab$. Để kiểm tra $z$ nằm trong đường tròn này, chỉ cần kiểm tra góc giữa $za$ và $zb$ không phải góc nhọn.

<center>
<img src="https://upload.wikimedia.org/wikipedia/commons/8/8e/Diameter_angles.svg">
<br>
<i>Góc bên trong là góc tù, góc bên ngoài là góc nhọn và góc trên đường tròn là góc vuông</i>
</center>

Tương đương, ta cần kiểm tra

$$
I_0=(b-z)\overline{(a-z)}
$$

không có phần thực dương (ứng với các điểm có góc cực giữa $-90^\circ$ và $90^\circ$).

#### MEC của 3 điểm

Thêm $z$ vào tam giác $abc$ sẽ tạo thành một tứ giác. Xét biểu thức:

$$
\angle azb + \angle bca
$$

Trong một [tứ giác nội tiếp](https://en.wikipedia.org/wiki/Cyclic_quadrilateral), nếu $c$ và $z$ nằm cùng phía của $ab$, hai góc bằng nhau và tổng có dấu của chúng bằng $0^\circ$ (dương nếu ngược chiều kim đồng hồ và âm nếu theo chiều kim đồng hồ). Tương ứng, nếu $c$ và $z$ nằm khác phía thì tổng hai góc bằng $180^\circ$.

<center>
<img src="https://upload.wikimedia.org/wikipedia/commons/3/30/Opposing_inscribed_angles.svg">
<br>
<i>Các góc nội tiếp kề nhau bằng nhau, các góc đối bù nhau đến 180 độ</i>
</center>

Dưới góc nhìn số phức, $\angle azb$ là góc cực của $(b-z)\overline{(a-z)}$ còn $\angle bca$ là góc cực của $(a-c)\overline{(b-c)}$. Vậy $\angle azb + \angle bca$ là góc cực của

$$
I_1 = (b-z) \overline{(a-z)} (a-c) \overline{(b-c)}
$$

Nếu góc bằng $0^\circ$ hoặc $180^\circ$ thì phần ảo của $I_1$ bằng $0$; nếu không, ta có thể suy ra $z$ ở trong hay ngoài đường tròn bao của $abc$ bằng cách kiểm tra dấu phần ảo của $I_1$. Phần ảo dương tương ứng với góc dương, còn phần ảo âm tương ứng với góc âm.

Nhưng dấu nào cho biết $z$ nằm trong hay ngoài đường tròn? Như đã nhận thấy, khi $z$ ở trong đường tròn thì độ lớn của $\angle azb$ thường tăng, còn khi ở ngoài thì giảm. Do đó có 4 trường hợp:

1. $\angle bca > 0^\circ$, $c$ cùng phía $ab$ với $z$. Khi đó $\angle azb < 0^\circ$ và $\angle azb + \angle bca < 0^\circ$ với các điểm trong đường tròn.
3. $\angle bca < 0^\circ$, $c$ cùng phía $ab$ với $z$. Khi đó $\angle azb > 0^\circ$ và $\angle azb + \angle bca > 0^\circ$ với các điểm trong đường tròn.
2. $\angle bca > 0^\circ$, $c$ khác phía $ab$ với $z$. Khi đó $\angle azb > 0^\circ$ và $\angle azb + \angle bca > 180^\circ$ với các điểm trong đường tròn.
4. $\angle bca < 0^\circ$, $c$ khác phía $ab$ với $z$. Khi đó $\angle azb < 0^\circ$ và $\angle azb + \angle bca < 180^\circ$ với các điểm trong đường tròn.

Nói cách khác, nếu $\angle bca$ dương thì các điểm trong đường tròn có $\angle azb + \angle bca < 0^\circ$, nếu không chúng có $\angle azb + \angle bca > 0^\circ$, giả sử ta chuẩn hóa các góc giữa $-180^\circ$ và $180^\circ$. Điều này có thể được kiểm tra qua dấu phần ảo của $I_2=(a-c)\overline{(b-c)}$ và $I_1 = I_0 I_2$.

**Lưu ý**: Vì ta nhân bốn số phức để được $I_1$, các hệ số trung gian có thể lớn tới $O(A^4)$, với $A$ là trị tuyệt đối lớn nhất của tọa độ đầu vào. Mặt khác, nếu đầu vào là số nguyên thì cả hai phép kiểm tra trên đều có thể thực hiện hoàn toàn bằng số nguyên.

#### Cài đặt

Để cài đặt phép kiểm tra, trước tiên ta cần quyết định cách biểu diễn MEC. Vì các tiêu chí làm việc trực tiếp với điểm, một cách tự nhiên và hiệu quả là biểu diễn MEC bằng một cặp hoặc bộ ba điểm xác định nó:

```cpp
using mec = variant<
    array<point, 2>,
    array<point, 3>
>;
```

Bây giờ có thể dùng `std::visit` để xử lý hiệu quả cả hai trường hợp theo các tiêu chí trên:

```cpp
/* I < 0 if z inside C,
   I > 0 if z outside C,
   I = 0 if z on the circumference of C */
ftype indicator(mec const& C, point z) {
    return visit([&](auto &&C) {
        point a = C[0], b = C[1];
        point I0 = (b - z) * conj(a - z);
        if constexpr (size(C) == 2) {
            return real(I0);
        } else {
            point c = C[2];
            point I2 = (a - c) * conj(b - c);
            point I1 = I0 * I2;
            return imag(I2) < 0 ? -imag(I1) : imag(I1);
        }
    }, C);
}

bool inside(mec const& C, point p) {
    return indicator(C, p) <= 0;
}

```

Cuối cùng, ta có thể kiểm tra mọi thứ hoạt động bằng cách nộp bài lên Library Checker: [#308668](https://judge.yosupo.jp/submission/308668).

## Bài tập

- [Library Checker - Minimum Enclosing Circle](https://judge.yosupo.jp/problem/minimum_enclosing_circle)
- [BOI 2002 - Aliens](https://www.spoj.com/problems/ALIENS)
