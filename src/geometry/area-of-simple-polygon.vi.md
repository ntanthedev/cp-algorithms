---
title: Finding area of simple polygon in O(N)
tags:
  - Translated
e_maxx_link: polygon_area
translation:
  source: geometry/area-of-simple-polygon.md
  source_commit: d07d3ce1cadd849c467d8bda23afb5ac09ad6b6c
  status: draft
  last_synced: 2026-08-09
---
# Tính diện tích đa giác đơn trong $O(N)$

Cho một đa giác đơn (tức không tự cắt, không nhất thiết lồi). Ta cần tính diện tích của đa giác từ các đỉnh đã cho.

## Phương pháp 1

Ta có thể duyệt qua tất cả các cạnh và cộng diện tích các hình thang được giới hạn bởi từng cạnh và trục x. Diện tích cần được tính kèm dấu để phần diện tích thừa được triệt tiêu. Do đó, ta có công thức:

$$A = \sum_{(p,q)\in \text{edges}} \frac{(p_x - q_x) \cdot (p_y + q_y)}{2}$$

Cài đặt:

```cpp
double area(const vector<point>& fig) {
    double res = 0;
    for (unsigned i = 0; i < fig.size(); i++) {
        point p = i ? fig[i - 1] : fig.back();
        point q = fig[i];
        res += (p.x - q.x) * (p.y + q.y);
    }
    return fabs(res) / 2;
}
```

## Phương pháp 2
Ta có thể chọn tùy ý một điểm $O$, sau đó duyệt qua tất cả các cạnh và cộng diện tích có hướng của tam giác tạo bởi cạnh đó với điểm $O$. Một lần nữa, nhờ dấu của diện tích, phần diện tích thừa sẽ được triệt tiêu.

Phương pháp này tốt hơn vì có thể khái quát cho những trường hợp phức tạp hơn (chẳng hạn khi một số cạnh là cung tròn thay vì đoạn thẳng).
