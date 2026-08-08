---
tags:
  - Translated
e_maxx_link: circle_line_intersection
translation:
  source: geometry/circle-line-intersection.md
  source_commit: 58460b2433878ed6238fa4491074f6df453163f7
  status: draft
  last_synced: 2026-08-08
---

# Giao của đường tròn và đường thẳng

Cho tọa độ tâm và bán kính của một đường tròn, cùng phương trình của một đường thẳng. Ta cần tìm các giao điểm của chúng.

## Lời giải

Thay vì giải hệ hai phương trình, ta sẽ tiếp cận bài toán bằng hình học. Cách này cho nghiệm có độ ổn định số tốt hơn.

Không mất tính tổng quát, giả sử đường tròn có tâm tại gốc tọa độ. Nếu không, ta tịnh tiến tâm về gốc rồi điều chỉnh hằng số $C$ trong phương trình đường thẳng. Khi đó ta có đường tròn tâm $(0,0)$ bán kính $r$ và đường thẳng có phương trình $Ax+By+C=0$.

Trước hết, hãy tìm điểm trên đường thẳng gần gốc tọa độ nhất, ký hiệu $(x_0, y_0)$. Thứ nhất, khoảng cách từ điểm đó đến gốc phải là

$$ d_0 = \frac{|C|}{\sqrt{A^2+B^2}} $$

Thứ hai, vì vectơ $(A, B)$ vuông góc với đường thẳng, tọa độ của điểm này phải tỉ lệ với các tọa độ của vectơ đó. Ta đã biết khoảng cách từ điểm tới gốc nên chỉ cần co giãn vectơ $(A, B)$ về đúng độ dài này, thu được:

$$\begin{align}
x_0 &= - \frac{AC}{A^2 + B^2} \\
y_0 &= - \frac{BC}{A^2 + B^2} 
\end{align}$$

Các dấu trừ không quá hiển nhiên, nhưng có thể dễ dàng kiểm tra bằng cách thay $x_0$ và $y_0$ vào phương trình đường thẳng.

Đến đây ta có thể xác định số giao điểm, thậm chí tìm luôn nghiệm khi có một hoặc không có giao điểm. Thật vậy, nếu khoảng cách từ $(x_0, y_0)$ đến gốc tọa độ $d_0$ lớn hơn bán kính $r$, đáp án là **không có giao điểm**. Nếu $d_0=r$, đáp án là **một giao điểm** $(x_0, y_0)$. Nếu $d_0<r$, có hai giao điểm và ta cần tìm tọa độ của chúng.

Ta biết điểm $(x_0, y_0)$ nằm bên trong đường tròn. Hai giao điểm $(a_x, a_y)$ và $(b_x, b_y)$ phải thuộc đường thẳng $Ax+By+C=0$, đồng thời cách $(x_0, y_0)$ cùng một khoảng $d$. Khoảng cách này được tính dễ dàng:

$$ d = \sqrt{r^2 - \frac{C^2}{A^2 + B^2}} $$

Lưu ý rằng vectơ $(-B, A)$ cùng phương với đường thẳng. Vì vậy, ta có thể tìm hai điểm cần thiết bằng cách cộng và trừ vectơ $(-B,A)$ đã được co giãn về độ dài $d$ với điểm $(x_0, y_0)$. 

Cuối cùng, tọa độ hai giao điểm là:

$$\begin{align}
m &= \sqrt{\frac{d^2}{A^2 + B^2}} \\
a_x &= x_0 + B \cdot m, a_y = y_0 - A \cdot m \\
b_x &= x_0 - B \cdot m, b_y = y_0 + A \cdot m
\end{align}$$

Nếu giải hệ phương trình ban đầu bằng phương pháp đại số, ta có thể nhận được một dạng đáp án khác với sai số lớn hơn. Phương pháp hình học ở đây trực quan và chính xác hơn.

## Cài đặt

Như đã nêu từ đầu, ta giả sử đường tròn có tâm tại gốc tọa độ. Vì vậy đầu vào của chương trình là bán kính $r$ của đường tròn cùng các tham số $A$, $B$ và $C$ của phương trình đường thẳng.

```cpp
double r, a, b, c; // given as input
double x0 = -a*c/(a*a+b*b), y0 = -b*c/(a*a+b*b);
if (c*c > r*r*(a*a+b*b)+EPS)
    puts ("no points");
else if (abs (c*c - r*r*(a*a+b*b)) < EPS) {
    puts ("1 point");
    cout << x0 << ' ' << y0 << '\n';
}
else {
    double d = r*r - c*c/(a*a+b*b);
    double mult = sqrt (d / (a*a+b*b));
    double ax, ay, bx, by;
    ax = x0 + b * mult;
    bx = x0 - b * mult;
    ay = y0 - a * mult;
    by = y0 + a * mult;
    puts ("2 points");
    cout << ax << ' ' << ay << '\n' << bx << ' ' << by << '\n';
}
```

## Bài tập luyện tập

- [CODECHEF: ANDOOR](https://www.codechef.com/problems/ANDOOR)
