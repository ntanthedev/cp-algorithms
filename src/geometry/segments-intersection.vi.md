---
tags:
  - Translated
e_maxx_link: segments_intersection
translation:
  source: geometry/segments-intersection.md
  source_commit: 7d39ffe004a1b4bffd5388771001b6bc5ca87fea
  status: draft
  last_synced: 2026-08-08
---

# Tìm giao của hai đoạn thẳng

Cho hai đoạn thẳng AB và CD, mỗi đoạn được mô tả bởi một cặp đầu mút. Một đoạn thẳng có thể chỉ là một điểm nếu hai đầu mút trùng nhau. 
Ta cần tìm giao của hai đoạn thẳng này; kết quả có thể rỗng (nếu hai đoạn không giao nhau), là một điểm duy nhất, hoặc là một đoạn thẳng (nếu hai đoạn chồng lên nhau).

## Lời giải

Ta có thể tìm giao của hai đoạn thẳng tương tự như khi tìm [giao của hai đường thẳng](lines-intersection.md): 
dựng phương trình đường thẳng từ các đầu mút của mỗi đoạn rồi kiểm tra xem hai đường thẳng có song song hay không. 

Nếu hai đường thẳng không song song, ta tìm giao điểm của chúng rồi kiểm tra xem điểm đó có thuộc cả hai đoạn hay không
(chỉ cần kiểm tra giao điểm có nằm trong hình chiếu của mỗi đoạn lên hai trục X và Y). 
Trong trường hợp này, đáp án hoặc là "không có giao", hoặc là chính giao điểm duy nhất của hai đường thẳng.

Trường hợp hai đường thẳng song song phức tạp hơn một chút (trường hợp một hoặc cả hai đoạn chỉ là một điểm cũng thuộc trường hợp này).
Khi đó, ta cần kiểm tra xem hai đoạn có cùng nằm trên một đường thẳng hay không.
Nếu không, đáp án là "không có giao".
Nếu có, đáp án là phần giao của hai đoạn cùng nằm trên đường thẳng đó. Ta tìm phần giao bằng cách 
sắp xếp các đầu mút của hai đoạn theo thứ tự tăng dần của một tọa độ thích hợp, rồi lấy đầu mút trái nằm bên phải hơn và đầu mút phải nằm bên trái hơn.

Nếu cả hai đoạn đều chỉ là các điểm đơn, hai điểm đó phải trùng nhau; hợp lý nhất là kiểm tra riêng trường hợp này.

Ở đầu thuật toán, ta thêm một phép kiểm tra hộp bao (bounding box). Phép kiểm tra này là cần thiết khi hai đoạn cùng nằm trên một đường thẳng,
và vì rất nhẹ nên cũng giúp thuật toán chạy nhanh hơn trung bình trên các bộ test ngẫu nhiên.


## Cài đặt

Dưới đây là phần cài đặt, bao gồm mọi hàm hỗ trợ cần thiết để xử lý đường thẳng và đoạn thẳng.

Hàm chính `intersect` trả về true nếu hai đoạn có giao khác rỗng,
và lưu hai đầu mút của đoạn giao vào các tham số `left` và `right`. 
Nếu đáp án chỉ là một điểm, hai giá trị được ghi vào `left` và `right` sẽ giống nhau.

```{.cpp file=segment_intersection}
const double EPS = 1E-9;

struct pt {
    double x, y;

    bool operator<(const pt& p) const
    {
        return x < p.x - EPS || (abs(x - p.x) < EPS && y < p.y - EPS);
    }
};

struct line {
    double a, b, c;

    line() {}
    line(pt p, pt q)
    {
        a = p.y - q.y;
        b = q.x - p.x;
        c = -a * p.x - b * p.y;
        norm();
    }

    void norm()
    {
        double z = sqrt(a * a + b * b);
        if (abs(z) > EPS)
            a /= z, b /= z, c /= z;
    }

    double dist(pt p) const { return a * p.x + b * p.y + c; }
};

double det(double a, double b, double c, double d)
{
    return a * d - b * c;
}

inline bool betw(double l, double r, double x)
{
    return min(l, r) <= x + EPS && x <= max(l, r) + EPS;
}

inline bool intersect_1d(double a, double b, double c, double d)
{
    if (a > b)
        swap(a, b);
    if (c > d)
        swap(c, d);
    return max(a, c) <= min(b, d) + EPS;
}

bool intersect(pt a, pt b, pt c, pt d, pt& left, pt& right)
{
    if (!intersect_1d(a.x, b.x, c.x, d.x) || !intersect_1d(a.y, b.y, c.y, d.y))
        return false;
    line m(a, b);
    line n(c, d);
    double zn = det(m.a, m.b, n.a, n.b);
    if (abs(zn) < EPS) {
        if (abs(m.dist(c)) > EPS || abs(n.dist(a)) > EPS)
            return false;
        if (b < a)
            swap(a, b);
        if (d < c)
            swap(c, d);
        left = max(a, c);
        right = min(b, d);
        return true;
    } else {
        left.x = right.x = -det(m.c, m.b, n.c, n.b) / zn;
        left.y = right.y = -det(m.a, m.c, n.a, n.c) / zn;
        return betw(a.x, b.x, left.x) && betw(a.y, b.y, left.y) &&
               betw(c.x, d.x, left.x) && betw(c.y, d.y, left.y);
    }
}
```
