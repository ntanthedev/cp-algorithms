---
tags:
  - Translated
e_maxx_link: intersecting_segments
translation:
  source: geometry/intersecting_segments.md
  source_commit: ce61cd887a9d0d8e50da79aa00990d258af80736
  status: draft
  last_synced: 2026-11-16
---

# Tìm một cặp đoạn thẳng giao nhau

Cho $n$ đoạn thẳng trên mặt phẳng. Hãy kiểm tra xem có ít nhất hai đoạn giao nhau hay không.
Nếu có, in ra một cặp đoạn thẳng giao nhau; nếu có nhiều đáp án, chỉ cần chọn một cặp bất kỳ.

Cách làm đơn giản là duyệt mọi cặp đoạn thẳng trong $O(n^2)$ và kiểm tra từng cặp có giao nhau hay không. Bài viết này mô tả thuật toán có thời gian chạy $O(n \log n)$ dựa trên **thuật toán đường quét**.

## Thuật toán

Hãy tưởng tượng một đường thẳng đứng $x = -\infty$ và bắt đầu di chuyển đường thẳng này sang phải.
Trong quá trình di chuyển, đường thẳng sẽ gặp các đoạn thẳng; mỗi khi một đoạn giao với đường quét, chúng giao nhau tại đúng một điểm (ta giả sử không có đoạn thẳng đứng).

<div style="text-align: center;">
  <img src="sweep_line_1.png" alt="Giao điểm của đường quét và đoạn thẳng">
</div>

Vậy với mỗi đoạn, tại một thời điểm, giao điểm của nó xuất hiện trên đường quét; giao điểm di chuyển theo đường quét, rồi cuối cùng đoạn biến mất khỏi đường quét.

Ta quan tâm đến **thứ tự tương đối của các đoạn thẳng** theo chiều dọc.
Cụ thể, ta lưu danh sách các đoạn cắt đường quét tại một thời điểm, sắp xếp theo tọa độ $y$ của giao điểm trên đường quét.

<div style="text-align: center;">
  <img src="sweep_line_2.png" alt="Thứ tự tương đối của các đoạn trên đường quét">
</div>

Thứ tự này hữu ích vì hai đoạn giao nhau sẽ có cùng tọa độ $y$ tại ít nhất một thời điểm:

<div style="text-align: center;">
  <img src="sweep_line_3.png" alt="Giao điểm có cùng tọa độ y">
</div>

Ta phát biểu các nhận xét chính:

  - Để tìm một cặp giao nhau, chỉ cần xét **các đoạn kề nhau** tại mỗi vị trí cố định của đường quét.
  - Không cần xét đường quét tại mọi vị trí thực $(-\infty \ldots +\infty)$ mà **chỉ cần xét các vị trí tại đó có đoạn mới xuất hiện hoặc đoạn cũ biến mất**. Nói cách khác, chỉ cần xét các vị trí bằng hoành độ đầu mút của các đoạn.
  - Khi một đoạn mới xuất hiện, chỉ cần **chèn** nó vào vị trí phù hợp trong danh sách từ vị trí đường quét trước đó. Ta chỉ cần kiểm tra giao nhau giữa **đoạn mới thêm và hai đoạn kề ngay phía trên và phía dưới nó trong danh sách**.
  - Khi một đoạn biến mất, chỉ cần **xóa** nó khỏi danh sách hiện tại. Sau đó cần **kiểm tra giao nhau giữa hai đoạn láng giềng phía trên và phía dưới trong danh sách**.
  - Ngoài các thay đổi đã mô tả, không có thay đổi nào khác trong thứ tự các đoạn của danh sách. Không cần kiểm tra giao nhau thêm.

Để hiểu vì sao những phát biểu này đúng, chỉ cần các nhận xét sau:

  - Hai đoạn không giao nhau không bao giờ đổi **thứ tự tương đối**.<br>
    Thật vậy, nếu một đoạn ban đầu ở trên đoạn kia rồi sau đó xuống dưới, thì giữa hai thời điểm đó chúng đã giao nhau.
  - Hai đoạn không giao nhau cũng không thể có cùng tọa độ $y$.
  - Suy ra khi một đoạn xuất hiện, ta có thể tìm vị trí của nó trong hàng đợi và không cần sắp xếp lại đoạn này nữa: **thứ tự của nó so với các đoạn khác trong hàng đợi sẽ không đổi**.
  - Hai đoạn giao nhau sẽ kề nhau trong hàng đợi tại thời điểm đường quét đi qua giao điểm của chúng.
  - Do đó, để tìm cặp đoạn thẳng giao nhau, chỉ cần kiểm tra giao nhau cho đúng các cặp đã từng kề nhau ít nhất một lần trong quá trình đường quét di chuyển. <br>
    Dễ thấy chỉ cần kiểm tra đoạn mới thêm với hai láng giềng phía trên và phía dưới của nó; khi xóa một đoạn, kiểm tra hai láng giềng phía trên và phía dưới của đoạn đó (sẽ trở thành kề nhau sau khi xóa).<br>
  - Chú ý rằng tại một vị trí cố định của đường quét, trước tiên phải **thêm tất cả các đoạn** bắt đầu tại hoành độ này, rồi mới **xóa tất cả các đoạn** kết thúc tại đây.<br>
    Nhờ vậy, ta không bỏ sót giao điểm tại đầu mút, tức trường hợp hai đoạn có chung một đầu mút.
  - Lưu ý rằng **các đoạn thẳng đứng** thực ra không ảnh hưởng đến tính đúng đắn của thuật toán.<br>
    Các đoạn này có đặc điểm là xuất hiện và biến mất cùng lúc. Tuy nhiên, theo nhận xét trước, mọi đoạn đều được thêm vào hàng đợi trước rồi mới bị xóa. Do đó nếu đoạn thẳng đứng giao với một đoạn khác đang mở tại thời điểm ấy (kể cả đoạn thẳng đứng), giao điểm sẽ được phát hiện.<br>
    **Đặt đoạn thẳng đứng ở vị trí nào trong hàng đợi?** Một đoạn thẳng đứng không có một tọa độ $y$ cụ thể mà trải dài trên cả một đoạn theo tọa độ $y$. Tuy nhiên, dễ thấy có thể lấy bất kỳ tọa độ nào trên đoạn đó làm tọa độ $y$.

Như vậy, toàn bộ thuật toán thực hiện không quá $2n$ phép kiểm tra giao nhau giữa các cặp đoạn và thực hiện $O(n)$ thao tác trên hàng đợi các đoạn ($O(1)$ thao tác khi mỗi đoạn xuất hiện và biến mất).

Vì vậy **độ phức tạp tiệm cận của thuật toán** là $O(n \log n)$.

## Cài đặt

Dưới đây là bản cài đặt đầy đủ của thuật toán:

```cpp
const double EPS = 1E-9;

struct pt {
    double x, y;
};

struct seg {
    pt p, q;
    int id;

    double get_y(double x) const {
        if (abs(p.x - q.x) < EPS)
            return p.y;
        return p.y + (q.y - p.y) * (x - p.x) / (q.x - p.x);
    }
};

bool intersect1d(double l1, double r1, double l2, double r2) {
    if (l1 > r1)
        swap(l1, r1);
    if (l2 > r2)
        swap(l2, r2);
    return max(l1, l2) <= min(r1, r2) + EPS;
}

int vec(const pt& a, const pt& b, const pt& c) {
    double s = (b.x - a.x) * (c.y - a.y) - (b.y - a.y) * (c.x - a.x);
    return abs(s) < EPS ? 0 : s > 0 ? +1 : -1;
}

bool intersect(const seg& a, const seg& b)
{
    return intersect1d(a.p.x, a.q.x, b.p.x, b.q.x) &&
           intersect1d(a.p.y, a.q.y, b.p.y, b.q.y) &&
           vec(a.p, a.q, b.p) * vec(a.p, a.q, b.q) <= 0 &&
           vec(b.p, b.q, a.p) * vec(b.p, b.q, a.q) <= 0;
}

bool operator<(const seg& a, const seg& b)
{
    double x = max(min(a.p.x, a.q.x), min(b.p.x, b.q.x));
    return a.get_y(x) < b.get_y(x) - EPS;
}

struct event {
    double x;
    int tp, id;

    event() {}
    event(double x, int tp, int id) : x(x), tp(tp), id(id) {}

    bool operator<(const event& e) const {
        if (abs(x - e.x) > EPS)
            return x < e.x;
        return tp > e.tp;
    }
};

set<seg> s;
vector<set<seg>::iterator> where;

set<seg>::iterator prev(set<seg>::iterator it) {
    return it == s.begin() ? s.end() : --it;
}

set<seg>::iterator next(set<seg>::iterator it) {
    return ++it;
}

pair<int, int> solve(const vector<seg>& a) {
    int n = (int)a.size();
    vector<event> e;
    for (int i = 0; i < n; ++i) {
        e.push_back(event(min(a[i].p.x, a[i].q.x), +1, i));
        e.push_back(event(max(a[i].p.x, a[i].q.x), -1, i));
    }
    sort(e.begin(), e.end());

    s.clear();
    where.resize(a.size());
    for (size_t i = 0; i < e.size(); ++i) {
        int id = e[i].id;
        if (e[i].tp == +1) {
            set<seg>::iterator nxt = s.lower_bound(a[id]), prv = prev(nxt);
            if (nxt != s.end() && intersect(*nxt, a[id]))
                return make_pair(nxt->id, id);
            if (prv != s.end() && intersect(*prv, a[id]))
                return make_pair(prv->id, id);
            where[id] = s.insert(nxt, a[id]);
        } else {
            set<seg>::iterator nxt = next(where[id]), prv = prev(where[id]);
            if (nxt != s.end() && prv != s.end() && intersect(*nxt, *prv))
                return make_pair(prv->id, nxt->id);
            s.erase(where[id]);
        }
    }

    return make_pair(-1, -1);
}
```

Hàm chính là `solve()`, trả về hai đoạn giao nhau nếu tồn tại, hoặc $(-1, -1)$ nếu không có giao điểm.

Hàm `intersect ()` kiểm tra hai đoạn có giao nhau hay không bằng **thuật toán dựa trên diện tích có hướng của tam giác**.

Hàng đợi các đoạn là biến toàn cục `s`, một `set<event>`. Các iterator xác định vị trí của mỗi đoạn trong hàng đợi (để thuận tiện khi xóa) được lưu trong mảng toàn cục `where`.

**Ghi chú của người dịch:** Kiểu hàng đợi được mô tả ở trên không khớp với code: phần tử của nó là đoạn thẳng, không phải sự kiện.

Hai hàm phụ `prev()` và `next()` trả về iterator tới phần tử trước và sau (hoặc `end()` nếu không tồn tại).

Hằng số `EPS` biểu thị sai số khi so sánh hai số thực (chủ yếu được dùng khi kiểm tra giao nhau giữa hai đoạn).

## Bài tập
 * [TIMUS 1469 No Smoking!](https://acm.timus.ru/problem.aspx?space=1&num=1469)
