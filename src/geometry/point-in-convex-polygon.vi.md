---
title: Check if point belongs to the convex polygon in O(log N)
tags:
  - Translated
e_maxx_link: pt_in_polygon
translation:
  source: geometry/point-in-convex-polygon.md
  source_commit: 4b3b4a89883c42237fb667ccdd2ca7543ddfeda7
  status: draft
  last_synced: 2026-08-08
---
# Kiểm tra một điểm có thuộc đa giác lồi trong $O(\log N)$ hay không

Xét bài toán sau: cho một đa giác lồi có các đỉnh là tọa độ nguyên và rất nhiều truy vấn.
Mỗi truy vấn là một điểm; ta cần xác định điểm đó nằm bên trong hoặc trên biên của đa giác hay không.
Giả sử các đỉnh của đa giác được sắp theo thứ tự ngược chiều kim đồng hồ. Mỗi truy vấn được xử lý trực tuyến trong $O(\log n)$.

## Thuật toán
Hãy chọn điểm có tọa độ x nhỏ nhất. Nếu có nhiều điểm như vậy, ta chọn điểm có tọa độ y nhỏ nhất. Ký hiệu điểm này là $p_0$.
Khi đó, tất cả các điểm còn lại $p_1,\dots,p_n$ của đa giác được sắp theo góc cực quanh điểm đã chọn (vì đa giác được sắp ngược chiều kim đồng hồ).

Nếu điểm cần truy vấn thuộc đa giác, nó sẽ thuộc một tam giác nào đó $p_0, p_i, p_{i + 1}$ (có thể thuộc nhiều hơn một tam giác nếu nằm trên biên của các tam giác).
Xét tam giác $p_0, p_i, p_{i + 1}$ chứa $p$ và có $i$ lớn nhất trong tất cả các tam giác như vậy.

Có một trường hợp đặc biệt: $p$ nằm trên đoạn $(p_0, p_n)$. Ta sẽ kiểm tra riêng trường hợp này.
Nếu không, tất cả các điểm $p_j$ với $j \le i$ đều nằm ngược chiều kim đồng hồ so với $p$ khi xét quanh $p_0$, còn các điểm khác thì không.
Điều này cho phép ta tìm kiếm nhị phân điểm $p_i$ sao cho $p_i$ không nằm ngược chiều kim đồng hồ so với $p$ khi xét quanh $p_0$, đồng thời $i$ lớn nhất trong tất cả các điểm thỏa mãn.
Sau đó, ta kiểm tra xem điểm truy vấn có thực sự nằm trong tam giác đã xác định hay không.

Dấu của $(a - c) \times (b - c)$ cho biết điểm $a$ nằm theo hay ngược chiều kim đồng hồ so với điểm $b$ khi xét quanh điểm $c$.
Nếu $(a - c) \times (b - c) > 0$, điểm $a$ nằm bên phải vector đi từ $c$ đến $b$, tức nằm theo chiều kim đồng hồ so với $b$ khi xét quanh $c$.
Nếu $(a - c) \times (b - c) < 0$, điểm nằm bên trái, tức ngược chiều kim đồng hồ.
Còn nếu tích có hướng bằng 0, điểm nằm đúng trên đường thẳng đi qua $b$ và $c$.

Quay lại thuật toán:
Xét một điểm truy vấn $p$.
Trước hết, ta phải kiểm tra điểm có nằm trong miền góc giới hạn bởi hai hướng đến $p_1$ và $p_n$ hay không.
Nếu không, ta đã biết nó không thể thuộc đa giác.
Có thể làm điều này bằng cách kiểm tra tích có hướng $(p_1 - p_0)\times(p - p_0)$ bằng 0 hoặc cùng dấu với $(p_1 - p_0)\times(p_n - p_0)$, đồng thời $(p_n - p_0)\times(p - p_0)$ bằng 0 hoặc cùng dấu với $(p_n - p_0)\times(p_1 - p_0)$.
Sau đó, ta xử lý trường hợp đặc biệt khi $p$ nằm trên đường thẳng $(p_0, p_1)$.
Tiếp theo, ta có thể tìm kiếm nhị phân điểm cuối cùng trong $p_1,\dots p_n$ không nằm ngược chiều kim đồng hồ so với $p$ khi xét quanh $p_0$.
Với một điểm $p_i$, điều kiện này được kiểm tra bằng $(p_i - p_0)\times(p - p_0) \le 0$. Sau khi tìm được điểm $p_i$ như vậy, ta cần kiểm tra $p$ có nằm trong tam giác $p_0, p_i, p_{i + 1}$ hay không.
Để kiểm tra, ta chỉ cần xác nhận $|(p_i - p_0)\times(p_{i + 1} - p_0)| = |(p_0 - p)\times(p_i - p)| + |(p_i - p)\times(p_{i + 1} - p)| + |(p_{i + 1} - p)\times(p_0 - p)|$.
Điều này kiểm tra diện tích của tam giác $p_0, p_i, p_{i+1}$ có đúng bằng tổng diện tích các tam giác $p_0, p_i, p$, $p_0, p, p_{i+1}$ và $p_i, p_{i+1}, p$ hay không.
Nếu $p$ nằm ngoài, tổng diện tích ba tam giác nhỏ sẽ lớn hơn diện tích tam giác ban đầu.
Nếu $p$ nằm trong, hai giá trị sẽ bằng nhau.

Ghi chú bản dịch: Nguồn hiện tại không nhất quán khi mô tả trường hợp đặc biệt: đoạn đầu ghi “(p_0, p_n)”, trong khi phần thuật toán bên dưới và cài đặt xử lý riêng “(p_0, p_1)”. Bản dịch giữ nguyên cả hai mệnh đề để đồng bộ với nguồn; vấn đề này được báo và đề xuất sửa riêng ở bản tiếng Anh.

## Cài đặt

Hàm `prepare` bảo đảm điểm nhỏ nhất theo thứ tự từ điển (tọa độ x nhỏ nhất, nếu hòa thì tọa độ y nhỏ nhất) trở thành $p_0$, đồng thời tính các vector $p_i - p_0$.
Sau đó, hàm `pointInConvexPolygon` tính kết quả của một truy vấn.
Ta cũng lưu lại điểm $p_0$ và tịnh tiến mỗi điểm truy vấn về hệ tọa độ lấy điểm đó làm gốc để tính đúng khoảng cách, vì bản thân vector không có điểm đầu cố định.
Sau khi tịnh tiến các điểm truy vấn, ta có thể giả sử mọi vector đều bắt đầu tại gốc tọa độ $(0, 0)$, nhờ đó đơn giản hóa các phép tính khoảng cách và độ dài.

```{.cpp file=points_in_convex_polygon}
struct pt {
    long long x, y;
    pt() {}
    pt(long long _x, long long _y) : x(_x), y(_y) {}
    pt operator+(const pt &p) const { return pt(x + p.x, y + p.y); }
    pt operator-(const pt &p) const { return pt(x - p.x, y - p.y); }
    long long cross(const pt &p) const { return x * p.y - y * p.x; }
    long long dot(const pt &p) const { return x * p.x + y * p.y; }
    long long cross(const pt &a, const pt &b) const { return (a - *this).cross(b - *this); }
    long long dot(const pt &a, const pt &b) const { return (a - *this).dot(b - *this); }
    long long sqrLen() const { return this->dot(*this); }
};

bool lexComp(const pt &l, const pt &r) {
    return l.x < r.x || (l.x == r.x && l.y < r.y);
}

int sgn(long long val) { return val > 0 ? 1 : (val == 0 ? 0 : -1); }

vector<pt> seq;
pt translation;
int n;

bool pointInTriangle(pt a, pt b, pt c, pt point) {
    long long s1 = abs(a.cross(b, c));
    long long s2 = abs(point.cross(a, b)) + abs(point.cross(b, c)) + abs(point.cross(c, a));
    return s1 == s2;
}

void prepare(vector<pt> &points) {
    n = points.size();
    int pos = 0;
    for (int i = 1; i < n; i++) {
        if (lexComp(points[i], points[pos]))
            pos = i;
    }
    rotate(points.begin(), points.begin() + pos, points.end());

    n--;
    seq.resize(n);
    for (int i = 0; i < n; i++)
        seq[i] = points[i + 1] - points[0];
    translation = points[0];
}

bool pointInConvexPolygon(pt point) {
    point = point - translation;
    if (seq[0].cross(point) != 0 &&
            sgn(seq[0].cross(point)) != sgn(seq[0].cross(seq[n - 1])))
        return false;
    if (seq[n - 1].cross(point) != 0 &&
            sgn(seq[n - 1].cross(point)) != sgn(seq[n - 1].cross(seq[0])))
        return false;

    if (seq[0].cross(point) == 0)
        return seq[0].sqrLen() >= point.sqrLen();

    int l = 0, r = n - 1;
    while (r - l > 1) {
        int mid = (l + r) / 2;
        int pos = mid;
        if (seq[pos].cross(point) >= 0)
            l = mid;
        else
            r = mid;
    }
    int pos = l;
    return pointInTriangle(seq[pos], seq[pos + 1], pt(0, 0), point);
}
```

## Bài tập
* [SGU253 Theodore Roosevelt](https://codeforces.com/problemsets/acmsguru/problem/99999/253)
* [Codeforces 55E Very simple problem](https://codeforces.com/contest/55/problem/E)
* [Codeforces 166B Polygons](https://codeforces.com/problemset/problem/166/B)
