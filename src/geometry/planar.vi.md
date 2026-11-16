---
title: Finding faces of a planar graph
tags:
  - Translated
e_maxx_link: facets
translation:
  source: geometry/planar.md
  source_commit: 2cfc81282d3da37b99198e1794db88ea8934462b
  status: draft
  last_synced: 2026-11-16
---
# Tìm các mặt của đồ thị phẳng

Xét một đồ thị $G$ có $n$ đỉnh và $m$ cạnh, có thể vẽ trên mặt phẳng sao cho hai cạnh chỉ giao nhau tại một đỉnh chung (nếu có).
Những đồ thị như vậy được gọi là **đồ thị phẳng**. Giả sử ta được cho một đồ thị phẳng cùng một cách nhúng bằng đoạn thẳng: mỗi đỉnh $v$ ứng với một điểm $(x, y)$ và tất cả các cạnh được vẽ thành những đoạn thẳng nối các điểm này mà không giao nhau (luôn tồn tại cách nhúng như vậy). Các đoạn thẳng chia mặt phẳng thành nhiều miền, gọi là các mặt. Có đúng một mặt không bị chặn, gọi là **mặt ngoài**; các mặt còn lại gọi là **mặt trong**.

Trong bài này, ta tìm cả mặt trong lẫn mặt ngoài của đồ thị phẳng. Ta giả sử đồ thị liên thông.

## Một số tính chất của đồ thị phẳng

Phần này trình bày một số tính chất của đồ thị phẳng mà không chứng minh. Bạn đọc quan tâm đến chứng minh có thể tham khảo [Graph Theory by R. Diestel](https://www.math.uni-hamburg.de/home/diestel/books/graph.theory/preview/Ch4.pdf) (xem thêm [video lectures on planarity](https://www.youtube.com/@DiestelGraphTheory) dựa trên sách này) hoặc các sách khác.

### Định lý Euler
Theo định lý Euler, mọi cách nhúng hợp lệ của đồ thị phẳng liên thông có $n$ đỉnh, $m$ cạnh và $f$ mặt đều thỏa mãn:

$$n - m + f = 2$$

Tổng quát hơn, mọi đồ thị phẳng có $k$ thành phần liên thông đều thỏa mãn:

$$n - m + f = 1 + k$$

### Số cạnh của đồ thị phẳng
Nếu $n \ge 3$ thì số cạnh tối đa của đồ thị phẳng có $n$ đỉnh là $3n - 6$. Mọi đồ thị phẳng liên thông mà mỗi mặt được giới hạn bởi một tam giác đều đạt số cạnh này. Về độ phức tạp, điều này có nghĩa là $m = O(n)$ đối với mọi đồ thị phẳng.

**Ghi chú của người dịch:** Các cận số cạnh và số mặt trong phần này giả sử đồ thị đơn; nếu cho phép nhiều cạnh song song thì cận trên không còn đúng nói chung.

### Số mặt của đồ thị phẳng
Từ tính chất trên suy ra ngay rằng nếu $n \ge 3$ thì số mặt tối đa của đồ thị phẳng có $n$ đỉnh là $2n - 4$.

### Bậc đỉnh nhỏ nhất trong đồ thị phẳng
Mọi đồ thị phẳng đều có một đỉnh bậc không lớn hơn 5.

**Ghi chú của người dịch:** Khẳng định về bậc đỉnh giả sử đồ thị đơn và có ít nhất một đỉnh.

## Thuật toán

Trước tiên, sắp xếp các cạnh kề của mỗi đỉnh theo góc cực.
Sau đó duyệt đồ thị như sau. Giả sử ta đi vào đỉnh $u$ qua cạnh $(v, u)$ và $(u, w)$ là cạnh tiếp theo sau $(v, u)$ trong danh sách kề đã sắp xếp của $u$. Khi đó đỉnh tiếp theo sẽ là $w$. Nếu bắt đầu phép duyệt này tại một cạnh $(v, u)$, ta sẽ đi quanh đúng một trong các mặt kề với $(v, u)$; mặt cụ thể phụ thuộc vào việc bước đầu đi từ $u$ đến $v$ hay từ $v$ đến $u$.

Thuật toán bây giờ khá rõ ràng: duyệt qua tất cả các cạnh và bắt đầu phép duyệt từ mỗi cạnh chưa được thăm trong những lượt trước. Nhờ đó ta tìm được mỗi mặt đúng một lần, và mỗi cạnh được đi qua hai lần (mỗi chiều một lần).

### Tìm cạnh tiếp theo
Trong khi duyệt, ta phải tìm cạnh tiếp theo theo thứ tự ngược chiều kim đồng hồ. Cách hiển nhiên nhất là tìm kiếm nhị phân theo góc. Tuy nhiên, khi đã biết thứ tự ngược chiều kim đồng hồ của các cạnh kề mỗi đỉnh, ta có thể tính trước cạnh tiếp theo và lưu trong bảng băm. Nếu các cạnh đã được sắp xếp theo góc thì độ phức tạp tìm tất cả các mặt khi đó trở thành tuyến tính.

### Tìm mặt ngoài
Không khó để thấy thuật toán duyệt mỗi mặt trong theo chiều kim đồng hồ và mặt ngoài theo chiều ngược lại; do đó có thể tìm mặt ngoài bằng cách kiểm tra chiều duyệt của từng mặt.

### Độ phức tạp
Do bước sắp xếp, độ phức tạp của thuật toán là $O(m \log m)$; vì $m = O(n)$ nên cũng là $O(n \log n)$. Như đã nói ở trên, nếu không cần sắp xếp thì độ phức tạp là $O(n)$.

## Nếu đồ thị không liên thông thì sao?

Thoạt nhìn, việc tìm các mặt của đồ thị không liên thông có vẻ không khó hơn nhiều vì có thể chạy cùng thuật toán trên từng thành phần liên thông. Tuy nhiên, các thành phần có thể được vẽ lồng nhau, tạo thành các **lỗ** (xem hình dưới). Khi đó mặt trong của một thành phần trở thành mặt ngoài của một số thành phần khác và có biên không liên thông phức tạp. Xử lý trường hợp này khá khó; một cách tiếp cận là xác định các thành phần lồng nhau bằng thuật toán [định vị điểm](point-location.md).

<div style="text-align: center;">
  <img src="planar_hole.png" alt="Đồ thị phẳng có lỗ">
</div>

## Cài đặt
Đoạn cài đặt sau trả về một vector các đỉnh cho mỗi mặt, với mặt ngoài đứng đầu.
Các mặt trong được trả về theo chiều ngược chiều kim đồng hồ, còn mặt ngoài theo chiều kim đồng hồ.

**Ghi chú của người dịch:** Với đồ thị liên thông chỉ gồm một đỉnh và không có cạnh, code trả về danh sách rỗng dù đồ thị vẫn có một mặt ngoài.

Để đơn giản, ta tìm cạnh tiếp theo bằng tìm kiếm nhị phân theo góc.
```{.cpp file=planar}
struct Point {
    int64_t x, y;

    Point(int64_t x_, int64_t y_): x(x_), y(y_) {}

    Point operator - (const Point & p) const {
        return Point(x - p.x, y - p.y);
    }

    int64_t cross (const Point & p) const {
        return x * p.y - y * p.x;
    }

    int64_t cross (const Point & p, const Point & q) const {
        return (p - *this).cross(q - *this);
    }

    int half () const {
        return int(y < 0 || (y == 0 && x < 0));
    }
};

std::vector<std::vector<size_t>> find_faces(std::vector<Point> vertices, std::vector<std::vector<size_t>> adj) {
    size_t n = vertices.size();
    std::vector<std::vector<char>> used(n);
    for (size_t i = 0; i < n; i++) {
        used[i].resize(adj[i].size());
        used[i].assign(adj[i].size(), 0);
        auto compare = [&](size_t l, size_t r) {
            Point pl = vertices[l] - vertices[i];
            Point pr = vertices[r] - vertices[i];
            if (pl.half() != pr.half())
                return pl.half() < pr.half();
            return pl.cross(pr) > 0;
        };
        std::sort(adj[i].begin(), adj[i].end(), compare);
    }
    std::vector<std::vector<size_t>> faces;
    for (size_t i = 0; i < n; i++) {
        for (size_t edge_id = 0; edge_id < adj[i].size(); edge_id++) {
            if (used[i][edge_id]) {
                continue;
            }
            std::vector<size_t> face;
            size_t v = i;
            size_t e = edge_id;
            while (!used[v][e]) {
                used[v][e] = true;
                face.push_back(v);
                size_t u = adj[v][e];
                size_t e1 = std::lower_bound(adj[u].begin(), adj[u].end(), v, [&](size_t l, size_t r) {
                    Point pl = vertices[l] - vertices[u];
                    Point pr = vertices[r] - vertices[u];
                    if (pl.half() != pr.half())
                        return pl.half() < pr.half();
                    return pl.cross(pr) > 0;
                }) - adj[u].begin() + 1;
                if (e1 == adj[u].size()) {
                    e1 = 0;
                }
                v = u;
                e = e1;
            }
            std::reverse(face.begin(), face.end());
            Point p1 = vertices[face[0]];
            __int128 sum = 0;
            for (int j = 0; j < face.size(); ++j) {
                Point p2 = vertices[face[j]];
                Point p3 = vertices[face[(j + 1) % face.size()]];
                sum += (p2 - p1).cross(p3 - p2);
            }
            if (sum <= 0) {
                faces.insert(faces.begin(), face);
            } else {
                faces.emplace_back(face);
            }
        }
    }
    return faces;
}
```

**Ghi chú của người dịch:** Kiểu tích lũy tổng rộng hơn không ngăn được tràn số nguyên trong các phép trừ và tích có hướng được tính trước đó. Cần giới hạn tọa độ để các phép tính trung gian này nằm trong phạm vi của kiểu tương ứng.

## Dựng đồ thị phẳng từ các đoạn thẳng

Đôi khi đầu vào không cho đồ thị tường minh mà là một tập đoạn thẳng trên mặt phẳng; đồ thị thực tế được tạo bởi các giao điểm của chúng như hình dưới. Khi đó ta phải tự dựng đồ thị. Cách đơn giản nhất là cố định một đoạn rồi tìm giao điểm của nó với tất cả các đoạn còn lại. Sắp xếp các giao điểm cùng hai đầu mút của đoạn theo thứ tự từ điển và thêm chúng làm các đỉnh của đồ thị. Đồng thời nối mỗi cặp đỉnh liên tiếp trong thứ tự đó bằng một cạnh. Lặp lại với mọi đoạn sẽ thu được đồ thị. Dĩ nhiên, cần bảo đảm hai giao điểm bằng nhau luôn ứng với cùng một đỉnh. Cách đơn giản nhất là lưu các điểm trong một map theo tọa độ, coi những điểm có tọa độ sai khác rất nhỏ (chẳng hạn nhỏ hơn $10^{-9}$) là bằng nhau. Thuật toán này chạy trong $O(n^2 \log n)$.

<div style="text-align: center;">
  <img src="planar_implicit.png" alt="Đồ thị được xác định ngầm">
</div>

## Cài đặt
```{.cpp file=planar_implicit}
using dbl = long double;

const dbl eps = 1e-9;

struct Point {
    dbl x, y;

    Point(){}
    Point(dbl x_, dbl y_): x(x_), y(y_) {}

    Point operator * (dbl d) const {
        return Point(x * d, y * d);
    }

    Point operator + (const Point & p) const {
        return Point(x + p.x, y + p.y);
    }

    Point operator - (const Point & p) const {
        return Point(x - p.x, y - p.y);
    }

    dbl cross (const Point & p) const {
        return x * p.y - y * p.x;
    }

    dbl cross (const Point & p, const Point & q) const {
        return (p - *this).cross(q - *this);
    }

    dbl dot (const Point & p) const {
        return x * p.x + y * p.y;
    }

    dbl dot (const Point & p, const Point & q) const {
        return (p - *this).dot(q - *this);
    }

    bool operator < (const Point & p) const {
        if (fabs(x - p.x) < eps) {
            if (fabs(y - p.y) < eps) {
                return false;
            } else {
                return y < p.y;
            }
        } else {
            return x < p.x;
        }
    }

    bool operator == (const Point & p) const {
        return fabs(x - p.x) < eps && fabs(y - p.y) < eps;
    }

    bool operator >= (const Point & p) const {
        return !(*this < p);
    }
};

struct Line{
	Point p[2];

	Line(Point l, Point r){p[0] = l; p[1] = r;}
	Point& operator [](const int & i){return p[i];}
	const Point& operator[](const int & i)const{return p[i];}
	Line(const Line & l){
		p[0] = l.p[0]; p[1] = l.p[1];
	}
	Point getOrth()const{
		return Point(p[1].y - p[0].y, p[0].x - p[1].x);
	}
	bool hasPointLine(const Point & t)const{
		return std::fabs(p[0].cross(p[1], t)) < eps;
	}
	bool hasPointSeg(const Point & t)const{
		return hasPointLine(t) && t.dot(p[0], p[1]) < eps;
	}
};

std::vector<Point> interLineLine(Line l1, Line l2){
	if(std::fabs(l1.getOrth().cross(l2.getOrth())) < eps){
		if(l1.hasPointLine(l2[0]))return {l1[0], l1[1]};
		else return {};
	}
	Point u = l2[1] - l2[0];
	Point v = l1[1] - l1[0];
	dbl s = u.cross(l2[0] - l1[0])/u.cross(v);
	return {Point(l1[0] + v * s)};
}

std::vector<Point> interSegSeg(Line l1, Line l2){
	if (l1[0] == l1[1]) {
		if (l2[0] == l2[1]) {
			if (l1[0] == l2[0])
                return {l1[0]};
			else 
                return {};
		} else {
			if (l2.hasPointSeg(l1[0]))
                return {l1[0]};
			else
                return {};
		}
	}
	if (l2[0] == l2[1]) {
		if (l1.hasPointSeg(l2[0]))
            return {l2[0]};
		else 
            return {};
	}
	auto li = interLineLine(l1, l2);
	if (li.empty())
        return li;
	if (li.size() == 2) {
		if (l1[0] >= l1[1])
            std::swap(l1[0], l1[1]);
		if (l2[0] >= l2[1])
            std::swap(l2[0], l2[1]);
        std::vector<Point> res(2);
		if (l1[0] < l2[0])
            res[0] = l2[0];
        else
            res[0] = l1[0];
		if (l1[1] < l2[1])
            res[1] = l1[1];
        else
            res[1] = l2[1];
		if (res[0] == res[1])
            res.pop_back();
		if (res.size() == 2u && res[1] < res[0])
            return {};
		else 
            return res;
	}
	Point cand = li[0];
	if (l1.hasPointSeg(cand) && l2.hasPointSeg(cand))
        return {cand};
	else 
        return {};
}

std::pair<std::vector<Point>, std::vector<std::vector<size_t>>> build_graph(std::vector<Line> segments) {
    std::vector<Point> p;
    std::vector<std::vector<size_t>> adj;
    std::map<std::pair<int64_t, int64_t>, size_t> point_id;
    auto get_point_id = [&](Point pt) {
        auto repr = std::make_pair(
            int64_t(std::round(pt.x * 1000000000) + 1e-6),
            int64_t(std::round(pt.y * 1000000000) + 1e-6)
        );
        if (!point_id.count(repr)) {
            adj.emplace_back();
            size_t id = point_id.size();
            point_id[repr] = id;
            p.push_back(pt);
            return id;
        } else {
            return point_id[repr];
        }
    };
    for (size_t i = 0; i < segments.size(); i++) {
        std::vector<size_t> curr = {
            get_point_id(segments[i][0]),
            get_point_id(segments[i][1])
        };
        for (size_t j = 0; j < segments.size(); j++) {
            if (i == j)
                continue;
            auto inter = interSegSeg(segments[i], segments[j]);
            for (auto pt: inter) {
                curr.push_back(get_point_id(pt));
            }
        }
        std::sort(curr.begin(), curr.end(), [&](size_t l, size_t r) { return p[l] < p[r]; });
        curr.erase(std::unique(curr.begin(), curr.end()), curr.end());
        for (size_t j = 0; j + 1 < curr.size(); j++) {
            adj[curr[j]].push_back(curr[j + 1]);
            adj[curr[j + 1]].push_back(curr[j]);
        }
    }
    for (size_t i = 0; i < adj.size(); i++) {
        std::sort(adj[i].begin(), adj[i].end());
        // removing edges that were added multiple times
        adj[i].erase(std::unique(adj[i].begin(), adj[i].end()), adj[i].end());
    }
    return {p, adj};
}
```

**Ghi chú của người dịch:** Hàm so sánh điểm dựa trên ngưỡng sai số ở code trên không bảo đảm thứ tự yếu nghiêm ngặt mà thuật toán sắp xếp yêu cầu: tính tương đương do hàm này tạo ra có thể không bắc cầu. Cần chọn cách biểu diễn và so sánh tọa độ phù hợp khi dùng cài đặt này.

## Bài tập
 * [TIMUS 1664 Pipeline Transportation](https://acm.timus.ru/problem.aspx?space=1&num=1664)
 * [TIMUS 1681 Brother Bear's Garden](https://acm.timus.ru/problem.aspx?space=1&num=1681)
