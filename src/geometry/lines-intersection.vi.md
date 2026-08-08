---
tags:
  - Translated
e_maxx_link: lines_intersection
translation:
  source: geometry/lines-intersection.md
  source_commit: bbfc54ba85f265d16abc8aa04377c30f421fd29e
  status: draft
  last_synced: 2026-08-08
---

# Giao điểm của hai đường thẳng

Cho hai đường thẳng được mô tả bởi các phương trình $a_1 x + b_1 y + c_1 = 0$ và  $a_2 x + b_2 y + c_2 = 0$.
Ta cần tìm giao điểm của hai đường thẳng hoặc xác định rằng chúng song song.

## Lời giải

Nếu hai đường thẳng không song song thì chúng cắt nhau.
Để tìm giao điểm, ta cần giải hệ phương trình tuyến tính sau:

$$\begin{cases} a_1 x + b_1 y + c_1 = 0 \\
a_2 x + b_2 y + c_2 = 0
\end{cases}$$

Dùng quy tắc Cramer, ta có thể viết ngay nghiệm của hệ, cũng chính là giao điểm cần tìm của hai đường thẳng:

$$x = - \frac{\begin{vmatrix}c_1 & b_1 \cr c_2 & b_2\end{vmatrix}}{\begin{vmatrix}a_1 & b_1 \cr a_2 & b_2\end{vmatrix} } = - \frac{c_1 b_2 - c_2 b_1}{a_1 b_2 - a_2 b_1},$$

$$y = - \frac{\begin{vmatrix}a_1 & c_1 \cr a_2 & c_2\end{vmatrix}}{\begin{vmatrix}a_1 & b_1 \cr a_2 & b_2\end{vmatrix}} = - \frac{a_1 c_2 - a_2 c_1}{a_1 b_2 - a_2 b_1}.$$

Nếu mẫu số bằng $0$, tức là

$$\begin{vmatrix}a_1 & b_1 \cr a_2 & b_2\end{vmatrix} = a_1 b_2 - a_2 b_1 = 0 $$

thì hệ hoặc vô nghiệm (hai đường thẳng song song và phân biệt), hoặc có vô số nghiệm (hai đường thẳng trùng nhau).
Nếu cần phân biệt hai trường hợp này, ta phải kiểm tra xem các hệ số $c$ có tỉ lệ theo cùng hệ số tỉ lệ với các hệ số $a$ và $b$ hay không.
Để làm vậy, chỉ cần tính hai định thức sau; nếu cả hai đều bằng $0$ thì hai đường thẳng trùng nhau:

$$\begin{vmatrix}a_1 & c_1 \cr a_2 & c_2\end{vmatrix}, \begin{vmatrix}b_1 & c_1 \cr b_2 & c_2\end{vmatrix} $$

Lưu ý rằng một cách khác để tính giao điểm được trình bày trong bài [Hình học cơ bản](basic-geometry.md).

## Cài đặt

```{.cpp file=line_intersection}
struct pt {
    double x, y;
};

struct line {
    double a, b, c;
};

const double EPS = 1e-9;

double det(double a, double b, double c, double d) {
    return a*d - b*c;
}

bool intersect(line m, line n, pt & res) {
    double zn = det(m.a, m.b, n.a, n.b);
    if (abs(zn) < EPS)
        return false;
    res.x = -det(m.c, m.b, n.c, n.b) / zn;
    res.y = -det(m.a, m.c, n.a, n.c) / zn;
    return true;
}

bool parallel(line m, line n) {
    return abs(det(m.a, m.b, n.a, n.b)) < EPS;
}

bool equivalent(line m, line n) {
    return abs(det(m.a, m.b, n.a, n.b)) < EPS
        && abs(det(m.a, m.c, n.a, n.c)) < EPS
        && abs(det(m.b, m.c, n.b, n.c)) < EPS;
}
```
