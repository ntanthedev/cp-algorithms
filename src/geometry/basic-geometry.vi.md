---
tags:
  - Original
translation:
  source: geometry/basic-geometry.md
  source_commit: 1e0ed561dc22f3e5ce3b8befc9af655be4873ffd
  status: draft
  last_synced: 2026-09-30
---

# Hình học cơ bản

Trong bài viết này, ta sẽ xét các phép toán cơ bản trên điểm trong không gian Euclid, vốn là nền tảng của toàn bộ hình học giải tích.
Với mỗi điểm $\mathbf r$, ta xét vector $\vec{\mathbf r}$ có hướng từ $\mathbf 0$ tới $\mathbf r$.
Về sau, ta sẽ không phân biệt $\mathbf r$ với $\vec{\mathbf r}$ và dùng thuật ngữ **điểm** như một từ đồng nghĩa với **vector**.

## Các phép toán tuyến tính

Các điểm 2D và 3D đều tạo thành một không gian tuyến tính, nghĩa là ta có thể cộng các điểm với nhau và nhân một điểm với một số. Dưới đây là các cài đặt cơ bản cho trường hợp 2D:

```{.cpp file=point2d}
struct point2d {
    ftype x, y;
    point2d() {}
    point2d(ftype x, ftype y): x(x), y(y) {}
    point2d& operator+=(const point2d &t) {
        x += t.x;
        y += t.y;
        return *this;
    }
    point2d& operator-=(const point2d &t) {
        x -= t.x;
        y -= t.y;
        return *this;
    }
    point2d& operator*=(ftype t) {
        x *= t;
        y *= t;
        return *this;
    }
    point2d& operator/=(ftype t) {
        x /= t;
        y /= t;
        return *this;
    }
    point2d operator+(const point2d &t) const {
        return point2d(*this) += t;
    }
    point2d operator-(const point2d &t) const {
        return point2d(*this) -= t;
    }
    point2d operator*(ftype t) const {
        return point2d(*this) *= t;
    }
    point2d operator/(ftype t) const {
        return point2d(*this) /= t;
    }
};
point2d operator*(ftype a, point2d b) {
    return b * a;
}
```
Và với các điểm 3D:
```{.cpp file=point3d}
struct point3d {
    ftype x, y, z;
    point3d() {}
    point3d(ftype x, ftype y, ftype z): x(x), y(y), z(z) {}
    point3d& operator+=(const point3d &t) {
        x += t.x;
        y += t.y;
        z += t.z;
        return *this;
    }
    point3d& operator-=(const point3d &t) {
        x -= t.x;
        y -= t.y;
        z -= t.z;
        return *this;
    }
    point3d& operator*=(ftype t) {
        x *= t;
        y *= t;
        z *= t;
        return *this;
    }
    point3d& operator/=(ftype t) {
        x /= t;
        y /= t;
        z /= t;
        return *this;
    }
    point3d operator+(const point3d &t) const {
        return point3d(*this) += t;
    }
    point3d operator-(const point3d &t) const {
        return point3d(*this) -= t;
    }
    point3d operator*(ftype t) const {
        return point3d(*this) *= t;
    }
    point3d operator/(ftype t) const {
        return point3d(*this) /= t;
    }
};
point3d operator*(ftype a, point3d b) {
    return b * a;
}
```

Ở đây, `ftype` là một kiểu dữ liệu dùng cho tọa độ, thường là `int`, `double` hoặc `long long`.

## Tích vô hướng

### Định nghĩa
Tích vô hướng (dot product, còn gọi là scalar product) $\mathbf a \cdot \mathbf b$ của hai vector $\mathbf a$ và $\mathbf b$ có thể được định nghĩa theo hai cách tương đương.
Về mặt hình học, đó là tích giữa độ dài của vector thứ nhất và độ dài hình chiếu của vector thứ hai lên vector thứ nhất.
Như có thể thấy trong hình dưới đây, hình chiếu này chính là $|\mathbf a| \cos \theta$, với $\theta$ là góc giữa $\mathbf a$ và $\mathbf b$. Do đó $\mathbf a\cdot  \mathbf b = |\mathbf a| \cos \theta \cdot |\mathbf b|$.

<div style="text-align: center;">
  <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/3/3e/Dot_Product.svg/300px-Dot_Product.svg.png" alt="">
</div>

Tích vô hướng có một số tính chất đáng chú ý:

1. $\mathbf a \cdot \mathbf b = \mathbf b \cdot \mathbf a$
2. $(\alpha \cdot \mathbf a)\cdot \mathbf b = \alpha \cdot (\mathbf a \cdot \mathbf b)$
3. $(\mathbf a + \mathbf b)\cdot \mathbf c = \mathbf a \cdot \mathbf c + \mathbf b \cdot \mathbf c$

Nói cách khác, đây là một phép toán giao hoán và tuyến tính theo cả hai đối số.
Ký hiệu các vector đơn vị là

$$\mathbf e_x = \begin{pmatrix} 1 \\ 0 \\ 0 \end{pmatrix}, \mathbf e_y = \begin{pmatrix} 0 \\ 1 \\ 0 \end{pmatrix}, \mathbf e_z = \begin{pmatrix} 0 \\ 0 \\ 1 \end{pmatrix}.$$

Với ký hiệu này, ta có thể viết vector $\mathbf r = (x;y;z)$ dưới dạng $r = x \cdot \mathbf e_x + y \cdot \mathbf e_y + z \cdot \mathbf e_z$.
Và vì với các vector đơn vị

$$\mathbf e_x\cdot \mathbf e_x = \mathbf e_y\cdot \mathbf e_y = \mathbf e_z\cdot \mathbf e_z = 1,\\
\mathbf e_x\cdot \mathbf e_y = \mathbf e_y\cdot \mathbf e_z = \mathbf e_z\cdot \mathbf e_x = 0$$

ta thấy rằng, theo tọa độ, với $\mathbf a = (x_1;y_1;z_1)$ và $\mathbf b = (x_2;y_2;z_2)$ ta có

$$\mathbf a\cdot \mathbf b = (x_1 \cdot \mathbf e_x + y_1 \cdot\mathbf e_y + z_1 \cdot\mathbf e_z)\cdot( x_2 \cdot\mathbf e_x + y_2 \cdot\mathbf e_y + z_2 \cdot\mathbf e_z) = x_1 x_2 + y_1 y_2 + z_1 z_2$$

Đây cũng chính là định nghĩa đại số của tích vô hướng.
Từ đó, ta có thể viết các hàm để tính tích vô hướng.

```{.cpp file=dotproduct}
ftype dot(point2d a, point2d b) {
    return a.x * b.x + a.y * b.y;
}
ftype dot(point3d a, point3d b) {
    return a.x * b.x + a.y * b.y + a.z * b.z;
}
```

Khi giải bài, ta nên dùng định nghĩa đại số để tính tích vô hướng, nhưng vẫn cần ghi nhớ định nghĩa hình học và các tính chất để khai thác chúng.

### Tính chất

Ta có thể biểu diễn nhiều đại lượng hình học thông qua tích vô hướng.
Ví dụ:

1. Chuẩn của $\mathbf a$ (bình phương độ dài): $|\mathbf a|^2 = \mathbf a\cdot \mathbf a$
2. Độ dài của $\mathbf a$: $|\mathbf a| = \sqrt{\mathbf a\cdot \mathbf a}$
3. Hình chiếu của $\mathbf a$ lên $\mathbf b$: $\dfrac{\mathbf a\cdot\mathbf b}{|\mathbf b|}$
4. Góc giữa hai vector: $\arccos \left(\dfrac{\mathbf a\cdot \mathbf b}{|\mathbf a| \cdot |\mathbf b|}\right)$
5. Từ ý trước, ta thấy tích vô hướng dương nếu góc giữa hai vector là góc nhọn, âm nếu là góc tù và bằng không nếu chúng trực giao, tức tạo thành một góc vuông.

Lưu ý rằng tất cả các hàm này không phụ thuộc vào số chiều, vì vậy chúng giống nhau cho trường hợp 2D và 3D:

```{.cpp file=dotproperties}
ftype norm(point2d a) {
    return dot(a, a);
}
double abs(point2d a) {
    return sqrt(norm(a));
}
double proj(point2d a, point2d b) {
    return dot(a, b) / abs(b);
}
double angle(point2d a, point2d b) {
    return acos(dot(a, b) / abs(a) / abs(b));
}
```

Để thấy một tính chất quan trọng tiếp theo, hãy xét tập các điểm $\mathbf r$ thỏa mãn $\mathbf r\cdot \mathbf a = C$ với một hằng số cố định $C$.
Ta có thể thấy đây chính xác là tập các điểm có hình chiếu lên $\mathbf a$ tại điểm $C \cdot \dfrac{\mathbf a}{|\mathbf a| ^ 2}$, và chúng tạo thành một siêu phẳng trực giao với $\mathbf a$.
Trong hình dưới đây ở trường hợp 2D, ta có thể thấy vector $\mathbf a$ cùng một số vector khác có cùng tích vô hướng với nó:

<div style="text-align: center;">
  <img src="https://i.imgur.com/eyO7St4.png" alt="Vectors having same dot product with a">
</div>

Trong 2D, các vector này tạo thành một đường thẳng; trong 3D, chúng tạo thành một mặt phẳng.
Kết quả này cho phép ta định nghĩa một đường thẳng trong 2D dưới dạng $\mathbf r\cdot \mathbf n=C$ hoặc $(\mathbf r - \mathbf r_0)\cdot \mathbf n=0$, trong đó $\mathbf n$ là vector trực giao với đường thẳng, $\mathbf r_0$ là bất kỳ vector nào đã nằm trên đường thẳng và $C = \mathbf r_0\cdot \mathbf n$.
Tương tự, ta có thể định nghĩa một mặt phẳng trong 3D.

## Tích có hướng

### Định nghĩa

Giả sử ta có ba vector $\mathbf a$, $\mathbf b$ và $\mathbf c$ trong không gian 3D, ghép thành một hình hộp song song như trong hình dưới đây:
<div style="text-align: center;">
  <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/3/3e/Parallelepiped_volume.svg/250px-Parallelepiped_volume.svg.png" alt="Three vectors">
</div>

Ta sẽ tính thể tích của nó như thế nào?
Từ kiến thức phổ thông, ta biết cần nhân diện tích đáy với chiều cao, tức hình chiếu của $\mathbf a$ lên phương vuông góc với đáy.
Điều đó có nghĩa là nếu ta định nghĩa $\mathbf b \times \mathbf c$ là vector vuông góc với cả $\mathbf b$ và $\mathbf c$, có độ dài bằng diện tích hình bình hành tạo bởi $\mathbf b$ và $\mathbf c$, thì $|\mathbf a\cdot (\mathbf b\times\mathbf c)|$ sẽ bằng thể tích của hình hộp song song.
Để quy ước nhất quán, ta chọn hướng của $\mathbf b\times \mathbf c$ sao cho phép quay từ vector $\mathbf b$ sang vector $\mathbf c$, khi nhìn từ phía đầu mút của $\mathbf b\times \mathbf c$, luôn ngược chiều kim đồng hồ (xem hình dưới đây).

<div style="text-align: center;">
  <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/b/b0/Cross_product_vector.svg/250px-Cross_product_vector.svg.png" alt="cross product">
</div>

Điều này định nghĩa tích có hướng (cross product, hay vector product) $\mathbf b\times \mathbf c$ của hai vector $\mathbf b$ và $\mathbf c$, cũng như tích hỗn tạp (triple product) $\mathbf a\cdot(\mathbf b\times \mathbf c)$ của ba vector $\mathbf a$, $\mathbf b$ và $\mathbf c$.

Một số tính chất đáng chú ý của tích có hướng và tích hỗn tạp:

1.  $\mathbf a\times \mathbf b = -\mathbf b\times \mathbf a$
2.  $(\alpha \cdot \mathbf a)\times \mathbf b = \alpha \cdot (\mathbf a\times \mathbf b)$
3.  Với mọi $\mathbf b$ và $\mathbf c$, tồn tại duy nhất một vector $\mathbf r$ sao cho $\mathbf a\cdot (\mathbf b\times \mathbf c) = \mathbf a\cdot\mathbf r$ với mọi vector $\mathbf a$. <br>Thật vậy, nếu tồn tại hai vector như vậy là $\mathbf r_1$ và $\mathbf r_2$, thì $\mathbf a\cdot (\mathbf r_1 - \mathbf r_2)=0$ với mọi vector $\mathbf a$, điều này chỉ có thể xảy ra khi $\mathbf r_1 = \mathbf r_2$.
4.  $\mathbf a\cdot (\mathbf b\times \mathbf c) = \mathbf b\cdot (\mathbf c\times \mathbf a) = -\mathbf a\cdot( \mathbf c\times \mathbf b)$
5.  $(\mathbf a + \mathbf b)\times \mathbf c = \mathbf a\times \mathbf c + \mathbf b\times \mathbf c$.
    Thật vậy, với mọi vector $\mathbf r$, ta có chuỗi đẳng thức:

    \[\mathbf r\cdot( (\mathbf a + \mathbf b)\times \mathbf c) = (\mathbf a + \mathbf b) \cdot (\mathbf c\times \mathbf r) =  \mathbf a \cdot(\mathbf c\times \mathbf r) + \mathbf b\cdot(\mathbf c\times \mathbf r) = \mathbf r\cdot (\mathbf a\times \mathbf c) + \mathbf r\cdot(\mathbf b\times \mathbf c) = \mathbf r\cdot(\mathbf a\times \mathbf c + \mathbf b\times \mathbf c)\]

    Theo ý 3, điều này chứng minh $(\mathbf a + \mathbf b)\times \mathbf c = \mathbf a\times \mathbf c + \mathbf b\times \mathbf c$.

6.  $|\mathbf a\times \mathbf b|=|\mathbf a| \cdot |\mathbf b| \sin \theta$ với $\theta$ là góc giữa $\mathbf a$ và $\mathbf b$, vì $|\mathbf a\times \mathbf b|$ bằng diện tích hình bình hành tạo bởi $\mathbf a$ và $\mathbf b$.

Từ các tính chất trên và đẳng thức sau với các vector đơn vị

$$\mathbf e_x\times \mathbf e_x = \mathbf e_y\times \mathbf e_y = \mathbf e_z\times \mathbf e_z = \mathbf 0,\\
\mathbf e_x\times \mathbf e_y = \mathbf e_z,~\mathbf e_y\times \mathbf e_z = \mathbf e_x,~\mathbf e_z\times \mathbf e_x = \mathbf e_y$$

ta có thể tính tích có hướng của $\mathbf a = (x_1;y_1;z_1)$ và $\mathbf b = (x_2;y_2;z_2)$ theo tọa độ:

$$\mathbf a\times \mathbf b = (x_1 \cdot \mathbf e_x + y_1 \cdot \mathbf e_y + z_1 \cdot \mathbf e_z)\times (x_2 \cdot \mathbf e_x + y_2 \cdot \mathbf e_y + z_2 \cdot \mathbf e_z) =$$

$$(y_1 z_2 - z_1 y_2)\mathbf e_x  + (z_1 x_2 - x_1 z_2)\mathbf e_y + (x_1 y_2 - y_1 x_2)\mathbf e_z$$

Cũng có thể viết gọn hơn dưới dạng:

$$\mathbf a\times \mathbf b = \begin{vmatrix}\mathbf e_x & \mathbf e_y & \mathbf e_z \\ x_1 & y_1 & z_1 \\ x_2 & y_2 & z_2 \end{vmatrix},~a\cdot(b\times c) = \begin{vmatrix} x_1 & y_1 & z_1 \\ x_2 & y_2 & z_2 \\ x_3 & y_3 & z_3 \end{vmatrix}$$

Ở đây $| \cdot |$ biểu thị định thức của một ma trận.

Một dạng tích có hướng (cụ thể là tích giả vô hướng, pseudo-scalar product) cũng có thể được cài đặt trong trường hợp 2D.
Nếu muốn tính diện tích hình bình hành tạo bởi các vector $\mathbf a$ và $\mathbf b$, ta có thể tính $|\mathbf e_z\cdot(\mathbf a\times \mathbf b)| = |x_1 y_2 - y_1 x_2|$.
Một cách khác để thu được kết quả tương tự là nhân $|\mathbf a|$ (đáy của hình bình hành) với chiều cao, tức hình chiếu của vector $\mathbf b$ lên vector $\mathbf a$ sau khi quay $90^\circ$, vector này là $\widehat{\mathbf a}=(-y_1;x_1)$.
Nói cách khác, ta tính $|\widehat{\mathbf a}\cdot\mathbf b|=|x_1y_2 - y_1 x_2|$.

Nếu xét cả dấu, diện tích sẽ dương khi phép quay từ $\mathbf a$ sang $\mathbf b$ (tức khi nhìn từ phía đầu mút của $\mathbf e_z$) diễn ra ngược chiều kim đồng hồ và âm trong trường hợp ngược lại.
Điều này định nghĩa tích giả vô hướng.
Lưu ý rằng giá trị này cũng bằng $|\mathbf a| \cdot |\mathbf b| \sin \theta$, trong đó $\theta$ là góc từ $\mathbf a$ đến $\mathbf b$ đo theo chiều ngược kim đồng hồ (và mang giá trị âm nếu phép quay theo chiều kim đồng hồ).

Hãy cài đặt tất cả những nội dung trên!

```{.cpp file=crossproduct}
point3d cross(point3d a, point3d b) {
    return point3d(a.y * b.z - a.z * b.y,
                   a.z * b.x - a.x * b.z,
                   a.x * b.y - a.y * b.x);
}
ftype triple(point3d a, point3d b, point3d c) {
    return dot(a, cross(b, c));
}
ftype cross(point2d a, point2d b) {
    return a.x * b.y - a.y * b.x;
}
```

### Tính chất

Với tích có hướng, nó bằng vector không khi và chỉ khi hai vector $\mathbf a$ và $\mathbf b$ thẳng hàng (chúng nằm trên cùng một đường thẳng, tức song song).
Tương tự với tích hỗn tạp: nó bằng không khi và chỉ khi các vector $\mathbf a$, $\mathbf b$ và $\mathbf c$ đồng phẳng (chúng nằm trên cùng một mặt phẳng).

Từ đó, ta có thể thu được các phương trình tổng quát để xác định đường thẳng và mặt phẳng.
Một đường thẳng có thể được xác định bằng vector chỉ phương $\mathbf d$ và một điểm ban đầu $\mathbf r_0$, hoặc bằng hai điểm $\mathbf a$ và $\mathbf b$.
Nó được xác định bởi $(\mathbf r - \mathbf r_0)\times\mathbf d=0$ hoặc $(\mathbf r - \mathbf a)\times (\mathbf b - \mathbf a) = 0$.
Với mặt phẳng, ta có thể xác định nó bằng ba điểm $\mathbf a$, $\mathbf b$ và $\mathbf c$ theo phương trình $(\mathbf r - \mathbf a)\cdot((\mathbf b - \mathbf a)\times (\mathbf c - \mathbf a))=0$, hoặc bằng một điểm ban đầu $\mathbf r_0$ và hai vector chỉ phương nằm trên mặt phẳng $\mathbf d_1$ và $\mathbf d_2$: $(\mathbf r - \mathbf r_0)\cdot(\mathbf d_1\times \mathbf d_2)=0$.

Trong 2D, tích giả vô hướng cũng có thể được dùng để kiểm tra hướng giữa hai vector vì nó dương nếu phép quay từ vector thứ nhất sang vector thứ hai là ngược chiều kim đồng hồ và âm trong trường hợp ngược lại.
Và tất nhiên, nó có thể được dùng để tính diện tích đa giác, nội dung này được trình bày trong một bài viết khác.
Trong không gian 3D, tích hỗn tạp có thể được dùng cho cùng mục đích.

## Bài tập

### Giao điểm hai đường thẳng

Có nhiều cách để biểu diễn một đường thẳng trong 2D và ta không nên ngần ngại kết hợp chúng.
Ví dụ, giả sử ta có hai đường thẳng và muốn tìm giao điểm của chúng.
Ta có thể nói mọi điểm trên đường thẳng thứ nhất đều có thể được tham số hóa dưới dạng $\mathbf r = \mathbf a_1 + t \cdot \mathbf d_1$, trong đó $\mathbf a_1$ là điểm ban đầu, $\mathbf d_1$ là vector chỉ phương và $t$ là một tham số thực.
Với đường thẳng thứ hai, mọi điểm trên nó phải thỏa mãn $(\mathbf r - \mathbf a_2)\times \mathbf d_2=0$. Từ đó, ta có thể dễ dàng tìm tham số $t$:

$$(\mathbf a_1 + t \cdot \mathbf d_1 - \mathbf a_2)\times \mathbf d_2=0 \quad\Rightarrow\quad t = \dfrac{(\mathbf a_2 - \mathbf a_1)\times\mathbf d_2}{\mathbf d_1\times \mathbf d_2}$$

Hãy cài đặt hàm tìm giao điểm của hai đường thẳng.

```{.cpp file=basic_line_intersection}
point2d intersect(point2d a1, point2d d1, point2d a2, point2d d2) {
    return a1 + cross(a2 - a1, d2) / cross(d1, d2) * d1;
}
```

### Giao của các mặt phẳng

Tuy nhiên, đôi khi việc dựa vào trực giác hình học có thể khá khó.
Ví dụ, giả sử ta có ba mặt phẳng được xác định bởi các điểm ban đầu $\mathbf a_i$ và các hướng $\mathbf d_i$, và muốn tìm giao điểm của chúng.
Ta có thể nhận thấy rằng chỉ cần giải hệ phương trình:

$$\begin{cases}\mathbf r\cdot \mathbf n_1 = \mathbf a_1\cdot \mathbf n_1, \\ \mathbf r\cdot \mathbf n_2 = \mathbf a_2\cdot \mathbf n_2, \\ \mathbf r\cdot \mathbf n_3 = \mathbf a_3\cdot \mathbf n_3\end{cases}$$

Thay vì tiếp tục tìm một cách giải hình học, ta có thể chuyển ngay sang cách giải đại số.
Chẳng hạn, nếu đã cài đặt lớp điểm, ta có thể dễ dàng giải hệ này bằng quy tắc Cramer vì tích hỗn tạp chính là định thức của ma trận có các vector làm cột:

```{.cpp file=plane_intersection}
point3d intersect(point3d a1, point3d n1, point3d a2, point3d n2, point3d a3, point3d n3) {
    point3d x(n1.x, n2.x, n3.x);
    point3d y(n1.y, n2.y, n3.y);
    point3d z(n1.z, n2.z, n3.z); 
    point3d d(dot(a1, n1), dot(a2, n2), dot(a3, n3));
    return point3d(triple(d, y, z),
                   triple(x, d, z),
                   triple(x, y, d)) / triple(n1, n2, n3);
}
```

Bây giờ, bạn có thể tự thử tìm cách giải cho các phép toán hình học thường gặp để làm quen với những kỹ thuật này.