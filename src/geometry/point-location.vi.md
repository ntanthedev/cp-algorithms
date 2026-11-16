---
title: Point location in O(log n)
tags:
  - Original
translation:
  source: geometry/point-location.md
  source_commit: c6d21b7f8a308666ebccb07b1bfbcda15d9f20e7
  status: draft
  last_synced: 2026-11-16
---
# Định vị điểm trong $O(log n)$

Xét bài toán sau: cho một [phân hoạch phẳng](https://en.wikipedia.org/wiki/Planar_straight-line_graph) không có đỉnh bậc một hoặc bậc không, cùng nhiều truy vấn.
Mỗi truy vấn là một điểm, và ta cần xác định mặt của phân hoạch chứa điểm đó.
Ta sẽ trả lời mỗi truy vấn ngoại tuyến trong $O(\log n)$.<br>
Bài toán này có thể xuất hiện khi cần định vị các điểm trong một biểu đồ Voronoi hoặc một đa giác đơn.

## Thuật toán

Trước tiên, với mỗi điểm truy vấn $p\ (x_0, y_0)$, ta muốn tìm một cạnh thỏa mãn: nếu điểm nằm trên một cạnh thì nó nằm trên cạnh tìm được; nếu không, cạnh này phải cắt đường thẳng $x = x_0$ tại đúng một điểm $(x_0, y)$ với $y < y_0$ và $y$ lớn nhất trong số các cạnh như vậy.
Hình sau minh họa cả hai trường hợp.

<div style="text-align: center;">
  <img src="point_location_goal.png" alt="Minh họa mục tiêu cần tìm">
</div>

Ta giải bài toán ngoại tuyến bằng thuật toán đường quét. Duyệt các hoành độ của điểm truy vấn và đầu mút các cạnh theo thứ tự tăng dần, đồng thời duy trì một tập cạnh $s$. Với mỗi hoành độ, ta tạo trước một số sự kiện.

Có bốn loại sự kiện: _add_, _remove_, _vertical_, _get_.
Với mỗi cạnh thẳng đứng (hai đầu mút có cùng hoành độ), thêm một sự kiện _vertical_ tại hoành độ tương ứng.
Với mỗi cạnh còn lại, thêm một sự kiện _add_ tại hoành độ nhỏ hơn của hai đầu mút và một sự kiện _remove_ tại hoành độ lớn hơn.
Cuối cùng, với mỗi điểm truy vấn, thêm một sự kiện _get_ tại hoành độ của điểm đó.

Tại mỗi hoành độ, ta sắp xếp các sự kiện theo loại theo thứ tự (_vertical_, _get_, _remove_, _add_).
Hình sau minh họa tất cả các sự kiện sau khi sắp xếp tại mỗi hoành độ.

<div style="text-align: center;">
  <img src="point_location_events.png" alt="Minh họa các sự kiện">
</div>

Trong quá trình quét, ta duy trì hai tập.
Tập $t$ dành cho tất cả các cạnh không thẳng đứng, còn tập $vert$ dành riêng cho các cạnh thẳng đứng.
Ta xóa các phần tử trong $vert$ khi bắt đầu xử lý mỗi hoành độ.

Xét cách xử lý các sự kiện tại một hoành độ cố định.

 - Khi gặp sự kiện _vertical_, ta chèn tung độ nhỏ hơn của hai đầu mút cạnh tương ứng vào $vert$.
 - Khi gặp sự kiện _remove_ hoặc _add_, ta xóa cạnh tương ứng khỏi $t$ hoặc thêm cạnh đó vào $t$.
 - Cuối cùng, với mỗi sự kiện _get_, ta kiểm tra điểm có nằm trên một cạnh thẳng đứng nào không bằng tìm kiếm nhị phân trong $vert$.
Nếu điểm không nằm trên cạnh thẳng đứng nào, ta phải tìm câu trả lời cho truy vấn trong $t$.
Để làm vậy, ta lại dùng tìm kiếm nhị phân.
Để xử lý một số trường hợp suy biến (chẳng hạn tam giác $(0,~0)$, $(0,~2)$, $(1, 1)$ khi truy vấn điểm $(0,~0)$), ta phải trả lời lại tất cả các sự kiện _get_ sau khi xử lý xong mọi sự kiện tại hoành độ này và chọn câu trả lời tốt hơn trong hai lần.

Tiếp theo, ta chọn hàm so sánh cho tập $t$.
Hàm này cần kiểm tra xem một cạnh có không nằm phía trên cạnh kia tại mọi hoành độ mà cả hai cùng phủ hay không. Giả sử có hai cạnh $(a, b)$ và $(c, d)$. Khi đó hàm so sánh có dạng mã giả:<br>

$val = sgn((b - a)\times(c - a)) + sgn((b - a)\times(d - a))$<br>
<b>if</b> $val \neq 0$<br>
<b>then return</b> $val > 0$<br>
$val = sgn((d - c)\times(a - c)) + sgn((d - c)\times(b - c))$<br>
<b>return</b> $val < 0$<br>

Giờ đây mỗi truy vấn đã có cạnh tương ứng.
Làm thế nào để tìm mặt?
Nếu không tìm được cạnh thì điểm nằm trong mặt ngoài.
Nếu điểm thuộc cạnh tìm được thì mặt chứa điểm không duy nhất.
Trong trường hợp còn lại có hai ứng viên: hai mặt có cạnh này trên biên.
Làm thế nào để biết mặt nào là đáp án? Lưu ý rằng cạnh này không thẳng đứng.
Khi đó đáp án là mặt nằm phía trên cạnh.
Ta tìm mặt như vậy cho mỗi cạnh không thẳng đứng.
Xét một lượt duyệt ngược chiều kim đồng hồ quanh mỗi mặt.
Nếu trong lượt duyệt đó hoành độ tăng khi đi qua cạnh thì mặt này là mặt cần tìm cho cạnh ấy.

## Ghi chú

Thực ra, với cây lưu phiên bản (persistent tree), cách tiếp cận này có thể trả lời truy vấn trực tuyến.

## Cài đặt

Đoạn code sau dùng số nguyên nhưng có thể dễ dàng sửa để dùng số thực kiểu double (bằng cách thay đổi các hàm so sánh và kiểu điểm).
Cài đặt giả sử phân hoạch đã được lưu đúng trong một [DCEL](https://en.wikipedia.org/wiki/Doubly_connected_edge_list) và mặt ngoài được đánh số $-1$.<br>
Với mỗi truy vấn, trả về cặp $(1, i)$ nếu điểm nằm thực sự bên trong mặt số $i$, và cặp $(0, i)$ nếu điểm nằm trên cạnh số $i$.

```{.cpp file=point-location}
typedef long long ll;

bool ge(const ll& a, const ll& b) { return a >= b; }
bool le(const ll& a, const ll& b) { return a <= b; }
bool eq(const ll& a, const ll& b) { return a == b; }
bool gt(const ll& a, const ll& b) { return a > b; }
bool lt(const ll& a, const ll& b) { return a < b; }
int sgn(const ll& x) { return le(x, 0) ? eq(x, 0) ? 0 : -1 : 1; }

struct pt {
    ll x, y;
    pt() {}
    pt(ll _x, ll _y) : x(_x), y(_y) {}
    pt operator-(const pt& a) const { return pt(x - a.x, y - a.y); }
    ll dot(const pt& a) const { return x * a.x + y * a.y; }
    ll dot(const pt& a, const pt& b) const { return (a - *this).dot(b - *this); }
    ll cross(const pt& a) const { return x * a.y - y * a.x; }
    ll cross(const pt& a, const pt& b) const { return (a - *this).cross(b - *this); }
    bool operator==(const pt& a) const { return a.x == x && a.y == y; }
};

struct Edge {
    pt l, r;
};

bool edge_cmp(Edge* edge1, Edge* edge2)
{
    const pt a = edge1->l, b = edge1->r;
    const pt c = edge2->l, d = edge2->r;
    int val = sgn(a.cross(b, c)) + sgn(a.cross(b, d));
    if (val != 0)
        return val > 0;
    val = sgn(c.cross(d, a)) + sgn(c.cross(d, b));
    return val < 0;
}

enum EventType { DEL = 2, ADD = 3, GET = 1, VERT = 0 };

struct Event {
    EventType type;
    int pos;
    bool operator<(const Event& event) const { return type < event.type; }
};

vector<Edge*> sweepline(vector<Edge*> planar, vector<pt> queries)
{
    using pt_type = decltype(pt::x);

    // collect all x-coordinates
    auto s =
        set<pt_type, std::function<bool(const pt_type&, const pt_type&)>>(lt);
    for (pt p : queries)
        s.insert(p.x);
    for (Edge* e : planar) {
        s.insert(e->l.x);
        s.insert(e->r.x);
    }

    // map all x-coordinates to ids
    int cid = 0;
    auto id =
        map<pt_type, int, std::function<bool(const pt_type&, const pt_type&)>>(
            lt);
    for (auto x : s)
        id[x] = cid++;

    // create events
    auto t = set<Edge*, decltype(*edge_cmp)>(edge_cmp);
    auto vert_cmp = [](const pair<pt_type, int>& l,
                       const pair<pt_type, int>& r) {
        if (!eq(l.first, r.first))
            return lt(l.first, r.first);
        return l.second < r.second;
    };
    auto vert = set<pair<pt_type, int>, decltype(vert_cmp)>(vert_cmp);
    vector<vector<Event>> events(cid);
    for (int i = 0; i < (int)queries.size(); i++) {
        int x = id[queries[i].x];
        events[x].push_back(Event{GET, i});
    }
    for (int i = 0; i < (int)planar.size(); i++) {
        int lx = id[planar[i]->l.x], rx = id[planar[i]->r.x];
        if (lx > rx) {
            swap(lx, rx);
            swap(planar[i]->l, planar[i]->r);
        }
        if (lx == rx) {
            events[lx].push_back(Event{VERT, i});
        } else {
            events[lx].push_back(Event{ADD, i});
            events[rx].push_back(Event{DEL, i});
        }
    }

    // perform sweep line algorithm
    vector<Edge*> ans(queries.size(), nullptr);
    for (int x = 0; x < cid; x++) {
        sort(events[x].begin(), events[x].end());
        vert.clear();
        for (Event event : events[x]) {
            if (event.type == DEL) {
                t.erase(planar[event.pos]);
            }
            if (event.type == VERT) {
                vert.insert(make_pair(
                    min(planar[event.pos]->l.y, planar[event.pos]->r.y),
                    event.pos));
            }
            if (event.type == ADD) {
                t.insert(planar[event.pos]);
            }
            if (event.type == GET) {
                auto jt = vert.upper_bound(
                    make_pair(queries[event.pos].y, planar.size()));
                if (jt != vert.begin()) {
                    --jt;
                    int i = jt->second;
                    if (ge(max(planar[i]->l.y, planar[i]->r.y),
                           queries[event.pos].y)) {
                        ans[event.pos] = planar[i];
                        continue;
                    }
                }
                Edge* e = new Edge;
                e->l = e->r = queries[event.pos];
                auto it = t.upper_bound(e);
                if (it != t.begin())
                    ans[event.pos] = *(--it);
                delete e;
            }
        }

        for (Event event : events[x]) {
            if (event.type != GET)
                continue;
            if (ans[event.pos] != nullptr &&
                eq(ans[event.pos]->l.x, ans[event.pos]->r.x))
                continue;

            Edge* e = new Edge;
            e->l = e->r = queries[event.pos];
            auto it = t.upper_bound(e);
            delete e;
            if (it == t.begin())
                e = nullptr;
            else
                e = *(--it);
            if (ans[event.pos] == nullptr) {
                ans[event.pos] = e;
                continue;
            }
            if (e == nullptr)
                continue;
            if (e == ans[event.pos])
                continue;
            if (id[ans[event.pos]->r.x] == x) {
                if (id[e->l.x] == x) {
                    if (gt(e->l.y, ans[event.pos]->r.y))
                        ans[event.pos] = e;
                }
            } else {
                ans[event.pos] = e;
            }
        }
    }
    return ans;
}

struct DCEL {
    struct Edge {
        pt origin;
        Edge* nxt = nullptr;
        Edge* twin = nullptr;
        int face;
    };
    vector<Edge*> body;
};

vector<pair<int, int>> point_location(DCEL planar, vector<pt> queries)
{
    vector<pair<int, int>> ans(queries.size());
    vector<Edge*> planar2;
    map<intptr_t, int> pos;
    map<intptr_t, int> added_on;
    int n = planar.body.size();
    for (int i = 0; i < n; i++) {
        if (planar.body[i]->face > planar.body[i]->twin->face)
            continue;
        Edge* e = new Edge;
        e->l = planar.body[i]->origin;
        e->r = planar.body[i]->twin->origin;
        added_on[(intptr_t)e] = i;
        pos[(intptr_t)e] =
            lt(planar.body[i]->origin.x, planar.body[i]->twin->origin.x)
                ? planar.body[i]->face
                : planar.body[i]->twin->face;
        planar2.push_back(e);
    }
    auto res = sweepline(planar2, queries);
    for (int i = 0; i < (int)queries.size(); i++) {
        if (res[i] == nullptr) {
            ans[i] = make_pair(1, -1);
            continue;
        }
        pt p = queries[i];
        pt l = res[i]->l, r = res[i]->r;
        if (eq(p.cross(l, r), 0) && le(p.dot(l, r), 0)) {
            ans[i] = make_pair(0, added_on[(intptr_t)res[i]]);
            continue;
        }
        ans[i] = make_pair(1, pos[(intptr_t)res[i]]);
    }
    for (auto e : planar2)
        delete e;
    return ans;
}
```

## Bài tập
 * [TIMUS 1848 Fly Hunt](http://acm.timus.ru/problem.aspx?space=1&num=1848&locale=en)
 * [UVA 12310 Point Location](https://onlinejudge.org/index.php?option=com_onlinejudge&Itemid=8&category=297&page=show_problem&problem=3732)
