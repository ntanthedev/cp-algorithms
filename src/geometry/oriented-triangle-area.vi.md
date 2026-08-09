---
tags:
  - Translated
e_maxx_link: oriented_area
translation:
  source: geometry/oriented-triangle-area.md
  source_commit: 191d241d5b9d4758f9f17647d6c0349c05346718
  status: draft
  last_synced: 2026-08-09
---

# Diện tích có hướng của tam giác

Cho ba điểm $p_1$, $p_2$ và $p_3$, hãy tính diện tích có hướng (có dấu) của tam giác tạo bởi chúng. Dấu của diện tích được xác định như sau: hãy tưởng tượng bạn đang đứng trên mặt phẳng tại điểm $p_1$ và nhìn về phía $p_2$. Bạn đi tới $p_2$; nếu $p_3$ nằm bên phải bạn (khi đó ta nói ba điểm tạo thành một lượt rẽ "theo chiều kim đồng hồ"), diện tích mang dấu âm, ngược lại diện tích mang dấu dương. Nếu ba điểm thẳng hàng, diện tích bằng không.

Từ diện tích có dấu này, ta vừa có thể lấy diện tích thông thường không âm (bằng giá trị tuyệt đối của diện tích có dấu), vừa xác định thứ tự các điểm đã cho là theo chiều kim đồng hồ hay ngược chiều kim đồng hồ (điều này hữu ích, chẳng hạn, trong các thuật toán bao lồi).


## Tính toán
Ta dùng tính chất rằng định thức của ma trận $2\times 2$ bằng diện tích có dấu của hình bình hành sinh bởi các vector cột (hoặc hàng) của ma trận.
Điều này tương tự định nghĩa tích có hướng trong 2D (xem [Hình học cơ bản](basic-geometry.md)).
Chia diện tích này cho hai, ta thu được diện tích tam giác cần tìm.
Ta sẽ dùng $\vec{p_1p_2}$ và $\vec{p_2p_3}$ làm các vector cột và tính định thức $2\times 2$:

$$2S=\left|\begin{matrix}x_2-x_1 & x_3-x_2\\y_2-y_1 & y_3-y_2\end{matrix}\right|=(x_2-x_1)(y_3-y_2)-(x_3-x_2)(y_2-y_1)$$

## Cài đặt

```cpp
int signed_area_parallelogram(point2d p1, point2d p2, point2d p3) {
    return cross(p2 - p1, p3 - p2);
}

double triangle_area(point2d p1, point2d p2, point2d p3) {
    return abs(signed_area_parallelogram(p1, p2, p3)) / 2.0;
}

bool clockwise(point2d p1, point2d p2, point2d p3) {
    return signed_area_parallelogram(p1, p2, p3) < 0;
}

bool counter_clockwise(point2d p1, point2d p2, point2d p3) {
    return signed_area_parallelogram(p1, p2, p3) > 0;
}
```

## Bài tập luyện tập
* [Codechef - Chef and Polygons](https://www.codechef.com/problems/CHEFPOLY)
