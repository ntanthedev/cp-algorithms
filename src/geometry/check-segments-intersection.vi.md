---
tags:
  - Translated
e_maxx_link: segments_intersection_checking
translation:
  source: geometry/check-segments-intersection.md
  source_commit: 3ff7fc56816a509359ae7537f5357c24fb41f25a
  status: draft
  last_synced: 2026-08-08
---

# Kiểm tra hai đoạn thẳng có giao nhau hay không

Cho hai đoạn thẳng $(a, b)$ và $(c, d)$.
Ta cần kiểm tra xem chúng có giao nhau hay không.
Dĩ nhiên, có thể tìm giao của hai đoạn rồi kiểm tra xem giao có rỗng hay không, nhưng với các đoạn có tọa độ nguyên thì cách đó không thể hoàn toàn thực hiện bằng số nguyên.
Cách tiếp cận được trình bày ở đây có thể làm việc hoàn toàn với số nguyên.

## Thuật toán

Trước hết, xét trường hợp hai đoạn thẳng cùng nằm trên một đường thẳng.
Khi đó chỉ cần kiểm tra xem hình chiếu của chúng lên $Ox$ và $Oy$ có giao nhau hay không.
Trong trường hợp còn lại, $a$ và $b$ không được nằm cùng một phía của đường thẳng $(c, d)$, đồng thời $c$ và $d$ cũng không được nằm cùng một phía của đường thẳng $(a, b)$.
Ta có thể kiểm tra điều này bằng một vài phép tính tích có hướng.

## Cài đặt

Thuật toán dưới đây được cài đặt cho các điểm có tọa độ nguyên. Dĩ nhiên, ta có thể dễ dàng sửa nó để làm việc với số thực `double`.

```{.cpp file=check-segments-inter}
struct pt {
    long long x, y;
    pt() {}
    pt(long long _x, long long _y) : x(_x), y(_y) {}
    pt operator-(const pt& p) const { return pt(x - p.x, y - p.y); }
    long long cross(const pt& p) const { return x * p.y - y * p.x; }
    long long cross(const pt& a, const pt& b) const { return (a - *this).cross(b - *this); }
};

int sgn(const long long& x) { return x >= 0 ? x ? 1 : 0 : -1; }

bool inter1(long long a, long long b, long long c, long long d) {
    if (a > b)
        swap(a, b);
    if (c > d)
        swap(c, d);
    return max(a, c) <= min(b, d);
}

bool check_inter(const pt& a, const pt& b, const pt& c, const pt& d) {
    if (c.cross(a, d) == 0 && c.cross(b, d) == 0)
        return inter1(a.x, b.x, c.x, d.x) && inter1(a.y, b.y, c.y, d.y);
    return sgn(a.cross(b, c)) != sgn(a.cross(b, d)) &&
           sgn(c.cross(d, a)) != sgn(c.cross(d, b));
}
```
