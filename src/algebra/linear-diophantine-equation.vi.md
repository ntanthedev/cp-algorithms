---
tags:
  - Translated
e_maxx_link: diofant_2_equation
translation:
  source: algebra/linear-diophantine-equation.md
  source_commit: 72a35898bc5ab07b2559cde952383c878b7787ae
  status: draft
  last_synced: 2026-08-07
---

# Phương trình Diophantine tuyến tính

Phương trình Diophantine tuyến tính (hai ẩn) là phương trình có dạng tổng quát:

$$ax + by = c$$

trong đó $a$, $b$, $c$ là các số nguyên đã biết, còn $x$, $y$ là các ẩn nguyên.

Trong bài này, ta xét một số bài toán cổ điển đối với dạng phương trình này:

* tìm một nghiệm
* tìm tất cả các nghiệm
* tìm số lượng nghiệm và chính các nghiệm trong một khoảng cho trước
* tìm một nghiệm có giá trị $x + y$ nhỏ nhất

## Trường hợp suy biến

Một trường hợp suy biến cần xử lý riêng là $a = b = 0$. Dễ thấy khi đó phương trình hoặc không có nghiệm, hoặc có vô số nghiệm, tùy theo $c = 0$ hay không. Trong phần còn lại của bài, ta bỏ qua trường hợp này.

## Lời giải trực tiếp

Khi $a \neq 0$ và $b \neq 0$, phương trình $ax+by=c$ có thể được xét tương đương dưới một trong hai dạng sau:

\begin{align}
ax &\equiv c \pmod b \\
by &\equiv c \pmod a
\end{align}

Không mất tính tổng quát, giả sử $b \neq 0$ và xét phương trình thứ nhất. Khi $a$ và $b$ nguyên tố cùng nhau, nghiệm của nó được cho bởi

$$x \equiv ca^{-1} \pmod b,$$

trong đó $a^{-1}$ là [nghịch đảo mô-đun](module-inverse.md) của $a$ theo mô-đun $b$.

Khi $a$ và $b$ không nguyên tố cùng nhau, mọi giá trị $ax$ theo mô-đun $b$ với $x$ nguyên đều chia hết cho $g=\gcd(a, b)$, vì vậy nghiệm chỉ tồn tại khi $c$ chia hết cho $g$. Trong trường hợp đó, có thể tìm một nghiệm bằng cách chia phương trình cho $g$:

$$(a/g) x \equiv (c/g) \pmod{b/g}.$$

Theo định nghĩa của $g$, hai số $a/g$ và $b/g$ nguyên tố cùng nhau, nên nghiệm được biểu diễn tường minh là

$$\begin{cases}
x \equiv (c/g)(a/g)^{-1}\pmod{b/g},\\
y = \frac{c-ax}{b}.
\end{cases}$$

## Lời giải bằng thuật toán

**Bổ đề Bézout** (cũng gọi là đồng nhất thức Bézout) là một kết quả hữu ích để hiểu lời giải sau.

> Gọi $g = \gcd(a,b)$. Khi đó tồn tại các số nguyên $x,y$ sao cho $ax + by = g$.
> 
> Hơn nữa, $g$ là số nguyên dương nhỏ nhất có thể biểu diễn dưới dạng $ax + by$; mọi số nguyên có dạng $ax + by$ đều là bội của $g$.

Để tìm một nghiệm của phương trình Diophantine hai ẩn, ta có thể dùng [thuật toán Euclid mở rộng](extended-euclid-algorithm.md). Trước hết giả sử $a$ và $b$ không âm. Khi áp dụng thuật toán Euclid mở rộng cho $a$ và $b$, ta tìm được ước chung lớn nhất $g$ cùng hai số $x_g$ và $y_g$ sao cho:

$$a x_g + b y_g = g$$

Nếu $c$ chia hết cho $g = \gcd(a, b)$ thì phương trình Diophantine đã cho có nghiệm; nếu không thì không có nghiệm. Chứng minh rất trực tiếp: một tổ hợp tuyến tính của hai số luôn chia hết cho ước chung của chúng.

Giả sử $c$ chia hết cho $g$, khi đó ta có:

$$a \cdot x_g \cdot \frac{c}{g} + b \cdot y_g \cdot \frac{c}{g} = c$$

Do đó một nghiệm của phương trình Diophantine là:

$$x_0 = x_g \cdot \frac{c}{g},$$

$$y_0 = y_g \cdot \frac{c}{g}.$$

Ý tưởng trên vẫn đúng khi $a$, $b$ hoặc cả hai là số âm. Ta chỉ cần đổi dấu $x_0$ và $y_0$ khi cần thiết.

Cuối cùng, ta có thể cài đặt ý tưởng như sau (lưu ý đoạn code này không xét trường hợp $a = b = 0$):

```{.cpp file=linear_diophantine_any}
int gcd(int a, int b, int& x, int& y) {
    if (b == 0) {
        x = 1;
        y = 0;
        return a;
    }
    int x1, y1;
    int d = gcd(b, a % b, x1, y1);
    x = y1;
    y = x1 - y1 * (a / b);
    return d;
}

bool find_any_solution(int a, int b, int c, int &x0, int &y0, int &g) {
    g = gcd(abs(a), abs(b), x0, y0);
    if (c % g) {
        return false;
    }

    x0 *= c / g;
    y0 *= c / g;
    if (a < 0) x0 = -x0;
    if (b < 0) y0 = -y0;
    return true;
}
```

## Tìm tất cả nghiệm

Từ một nghiệm $(x_0, y_0)$, ta có thể suy ra toàn bộ nghiệm của phương trình đã cho.

Gọi $g = \gcd(a, b)$ và $x_0, y_0$ là các số nguyên thỏa mãn:

$$a \cdot x_0 + b \cdot y_0 = c$$

Ta nhận thấy rằng nếu cộng $b / g$ vào $x_0$ và đồng thời trừ $a / g$ khỏi $y_0$ thì đẳng thức vẫn không thay đổi:

$$a \cdot \left(x_0 + \frac{b}{g}\right) + b \cdot \left(y_0 - \frac{a}{g}\right) = a \cdot x_0 + b \cdot y_0 + a \cdot \frac{b}{g} - b \cdot \frac{a}{g} = c$$

Rõ ràng có thể lặp lại quá trình này, nên mọi cặp số có dạng:

$$x = x_0 + k \cdot \frac{b}{g}$$

$$y = y_0 - k \cdot \frac{a}{g}$$

đều là nghiệm của phương trình đã cho.

Vì phương trình là tuyến tính, mọi nghiệm nằm trên cùng một đường thẳng, và theo định nghĩa của $g$, đây chính là tập tất cả các nghiệm có thể có của phương trình Diophantine đã cho.

## Tìm số lượng nghiệm và các nghiệm trong khoảng cho trước

Từ phần trước, có thể thấy nếu không đặt bất kỳ ràng buộc nào thì sẽ có vô số nghiệm. Vì vậy trong phần này, ta thêm các giới hạn cho khoảng của $x$ và $y$, rồi đếm và liệt kê các nghiệm thỏa mãn.

Cho hai khoảng: $[min_x; max_x]$ và $[min_y; max_y]$, và giả sử ta chỉ muốn tìm các nghiệm nằm trong hai khoảng này.

Lưu ý rằng nếu $a$ hoặc $b$ bằng $0$, nguồn bài viết nói bài toán chỉ có một nghiệm và không xét trường hợp này ở đây.

**Ghi chú bản dịch:** Với các ràng buộc khoảng, câu trên của nguồn không đúng trong mọi trường hợp: nếu một hệ số bằng $0$, một ẩn có thể được cố định trong khi ẩn còn lại vẫn nhận nhiều giá trị trong khoảng. Phần cài đặt bên dưới thực sự giả sử $a \neq 0$ và $b \neq 0$.

Trước hết, ta có thể tìm một nghiệm có giá trị $x$ nhỏ nhất sao cho $x \ge min_x$. Để làm vậy, đầu tiên tìm một nghiệm bất kỳ của phương trình Diophantine. Sau đó dịch chuyển nghiệm này để đạt $x \ge min_x$ bằng mô tả tập nghiệm ở phần trước. Việc này thực hiện được trong $O(1)$.
Ký hiệu giá trị nhỏ nhất này của $x$ là $l_{x1}$.

Tương tự, ta có thể tìm giá trị lớn nhất của $x$ thỏa mãn $x \le max_x$. Ký hiệu giá trị này là $r_{x1}$.

Tương tự, ta tìm giá trị nhỏ nhất của $y$ với $y \ge min_y$ và giá trị lớn nhất của $y$ với $y \le max_y$. Ký hiệu các giá trị $x$ tương ứng là $l_{x2}$ và $r_{x2}$.

Nghiệm cuối cùng là tất cả các nghiệm có $x$ thuộc giao của $[l_{x1}, r_{x1}]$ và $[l_{x2}, r_{x2}]$. Ký hiệu giao này là $[l_x, r_x]$.

Đoạn code sau cài đặt ý tưởng này.
Lưu ý rằng ở đầu ta chia $a$ và $b$ cho $g$.
Vì phương trình $a x + b y = c$ tương đương với phương trình $\frac{a}{g} x + \frac{b}{g} y = \frac{c}{g}$, ta có thể dùng phương trình sau và đạt $\gcd(\frac{a}{g}, \frac{b}{g}) = 1$, nhờ đó các công thức đơn giản hơn.

```{.cpp file=linear_diophantine_all}
void shift_solution(int & x, int & y, int a, int b, int cnt) {
    x += cnt * b;
    y -= cnt * a;
}

int find_all_solutions(int a, int b, int c, int minx, int maxx, int miny, int maxy) {
    int x, y, g;
    if (!find_any_solution(a, b, c, x, y, g))
        return 0;
    a /= g;
    b /= g;

    int sign_a = a > 0 ? +1 : -1;
    int sign_b = b > 0 ? +1 : -1;

    shift_solution(x, y, a, b, (minx - x) / b);
    if (x < minx)
        shift_solution(x, y, a, b, sign_b);
    if (x > maxx)
        return 0;
    int lx1 = x;

    shift_solution(x, y, a, b, (maxx - x) / b);
    if (x > maxx)
        shift_solution(x, y, a, b, -sign_b);
    int rx1 = x;

    shift_solution(x, y, a, b, -(miny - y) / a);
    if (y < miny)
        shift_solution(x, y, a, b, -sign_a);
    if (y > maxy)
        return 0;
    int lx2 = x;

    shift_solution(x, y, a, b, -(maxy - y) / a);
    if (y > maxy)
        shift_solution(x, y, a, b, sign_a);
    int rx2 = x;

    if (lx2 > rx2)
        swap(lx2, rx2);
    int lx = max(lx1, lx2);
    int rx = min(rx1, rx2);

    if (lx > rx)
        return 0;
    return (rx - lx) / abs(b) + 1;
}
```

Khi đã có $l_x$ và $r_x$, việc liệt kê tất cả nghiệm cũng đơn giản. Chỉ cần duyệt $x = l_x + k \cdot \frac{b}{g}$ với mọi $k \ge 0$ cho đến khi $x = r_x$, rồi tìm các giá trị $y$ tương ứng từ phương trình $a x + b y = c$.

## Tìm nghiệm có giá trị $x + y$ nhỏ nhất { data-toc-label='Find the solution with minimum value of <script type="math/tex">x + y</script>' }

Ở đây, $x$ và $y$ cũng cần có một số ràng buộc; nếu không, đáp án có thể tiến tới âm vô cùng.

Ý tưởng tương tự phần trước: ta tìm một nghiệm bất kỳ của phương trình Diophantine, rồi dịch chuyển nghiệm để thỏa mãn các điều kiện cần thiết.

Cuối cùng, dùng mô tả tập tất cả nghiệm để tìm giá trị nhỏ nhất:

$$x' = x + k \cdot \frac{b}{g},$$

$$y' = y - k \cdot \frac{a}{g}.$$

Lưu ý rằng $x + y$ thay đổi như sau:

$$x' + y' = x + y + k \cdot \left(\frac{b}{g} - \frac{a}{g}\right) = x + y + k \cdot \frac{b-a}{g}$$

Nếu $a < b$, ta cần chọn giá trị $k$ nhỏ nhất có thể. Nếu $a > b$, ta cần chọn giá trị $k$ lớn nhất có thể. Nếu $a = b$, mọi nghiệm đều có cùng tổng $x + y$.

## Bài tập luyện tập

* [Spoj - Crucial Equation](http://www.spoj.com/problems/CEQU/)
* [SGU 106](http://codeforces.com/problemsets/acmsguru/problem/99999/106)
* [Codeforces - Ebony and Ivory](http://codeforces.com/contest/633/problem/A)
* [Codechef - Get AC in one go](https://www.codechef.com/problems/COPR16G)
* [LightOj - Solutions to an equation](http://www.lightoj.com/volume_showproblem.php?problem=1306)
* [Atcoder - F - S = 1](https://atcoder.jp/contests/abc340/tasks/abc340_f)
