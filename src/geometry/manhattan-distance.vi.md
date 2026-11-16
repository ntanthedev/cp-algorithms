---
tags:
  - Original
translation:
  source: geometry/manhattan-distance.md
  source_commit: 9d0086536a38e388797dcd1043562aed61d5d867
  status: draft
  last_synced: 2026-11-16
---

# Khoảng cách Manhattan
	
## Định nghĩa
Với hai điểm $p$ và $q$ trên mặt phẳng, ta có thể định nghĩa khoảng cách giữa chúng là tổng độ chênh lệch giữa các tọa độ $x$ và $y$: 

$$d(p,q) = |x_p - x_q| + |y_p - y_q|$$

Khoảng cách này tương ứng với [hình học Manhattan (taxicab)](https://en.wikipedia.org/wiki/Taxicab_geometry), trong đó các điểm được coi là những giao lộ của một thành phố có quy hoạch như Manhattan, nơi ta chỉ có thể di chuyển theo đường ngang hoặc dọc như hình dưới:

<div style="text-align: center;">
  <img src="https://upload.wikimedia.org/wikipedia/commons/0/08/Manhattan_distance.svg" alt="Khoảng cách Manhattan">
</div>

Hình minh họa một số đường đi ngắn nhất giữa hai điểm màu đen, tất cả đều có độ dài $12$.

Có một số mẹo và thuật toán thú vị với khoảng cách này; dưới đây ta sẽ tìm hiểu một vài cách.

## Cặp điểm xa nhau nhất theo khoảng cách Manhattan

Cho $n$ điểm $P$, ta muốn tìm cặp điểm $p,q$ xa nhau nhất, tức là cực đại hóa $|x_p - x_q| + |y_p - y_q|$.

Trước hết xét một chiều, tức là $y=0$. Nhận xét chính là ta có thể thử cả hai khả năng $|x_p - x_q|$ bằng $x_p - x_q$ hoặc $-x_p + x_q$: nếu chọn sai dấu của giá trị tuyệt đối thì ta chỉ thu được giá trị nhỏ hơn, nên không ảnh hưởng tới đáp án. Cụ thể:

$$|x_p - x_q| = \max(x_p - x_q, -x_p + x_q)$$

Chẳng hạn, ta có thể thử để $x_p$ mang dấu cộng, khi đó $q$ phải mang dấu trừ. Như vậy ta cần tìm:

$$\max\limits_{p, q \in P}(x_p + (-x_q)) = \max\limits_{p \in P}(x_p) + \max\limits_{q \in P}( - x_q ).$$

Ta có thể mở rộng ý tưởng này cho 2 chiều hoặc nhiều hơn. Với $d$ chiều, ta cần thử tất cả $2^d$ cách chọn dấu. Chẳng hạn, ở $2$ chiều, nếu thử trường hợp $p$ mang cả hai dấu cộng thì ta cần tìm: 

$$\max\limits_{p, q \in P} [(x_p + (-x_q)) + (y_p + (-y_q))] = \max\limits_{p \in P}(x_p + y_p) + \max\limits_{q \in P}(-x_q - y_q).$$

Vì đã làm cho $p$ và $q$ độc lập, giờ đây ta dễ dàng tìm được $p$ và $q$ cực đại hóa biểu thức.

Đoạn code dưới đây tổng quát hóa cách làm cho $d$ chiều và chạy trong $O(n \cdot 2^d \cdot d)$.

```cpp
long long ans = 0;
for (int msk = 0; msk < (1 << d); msk++) {
    long long mx = LLONG_MIN, mn = LLONG_MAX;
    for (int i = 0; i < n; i++) {
        long long cur = 0;
        for (int j = 0; j < d; j++) {
            if (msk & (1 << j)) cur += p[i][j];
            else cur -= p[i][j];
        }
        mx = max(mx, cur);
        mn = min(mn, cur);
    }
    ans = max(ans, mx - mn);
}
```

## Phép quay các điểm và khoảng cách Chebyshev

Ta biết rằng với mọi $m, n \in \mathbb{R}$,

$$|m| + |n| = \text{max}(|m + n|, |m - n|).$$

Để chứng minh, chỉ cần xét dấu của $m$ và $n$. Phần chứng minh được dành làm bài tập.

Áp dụng đẳng thức này vào công thức khoảng cách Manhattan, ta được

$$d((x_1, y_1), (x_2, y_2)) = |x_1 - x_2| + |y_1 - y_2| = \text{max}(|(x_1 + y_1) - (x_2 + y_2)|, |(y_1 - x_1) - (y_2 - x_2)|).$$

Biểu thức cuối trong đẳng thức trên là [khoảng cách Chebyshev](https://en.wikipedia.org/wiki/Chebyshev_distance) giữa hai điểm $(x_1 + y_1, y_1 - x_1)$ và $(x_2 + y_2, y_2 - x_2)$. Nghĩa là sau khi áp dụng phép biến đổi

$$\alpha : (x, y) \to (x + y, y - x),$$

khoảng cách Manhattan giữa $p$ và $q$ trở thành khoảng cách Chebyshev giữa $\alpha(p)$ và $\alpha(q)$.

Ta cũng nhận thấy $\alpha$ là một [phép đồng dạng xoắn](https://en.wikipedia.org/wiki/Spiral_similarity) (phép quay mặt phẳng rồi vị tự theo tâm $O$), với tâm $(0, 0)$, góc quay $45^{\circ}$ theo chiều kim đồng hồ và tỉ số vị tự $\sqrt{2}$.

Hình dưới giúp trực quan hóa phép biến đổi:

<div style="text-align: center;">
  <img src="chebyshev-transformation.png" alt="Phép biến đổi Chebyshev">
</div>

## Cây khung nhỏ nhất Manhattan

Bài toán cây khung nhỏ nhất Manhattan yêu cầu tìm các cạnh nối tất cả các điểm cho trước trên mặt phẳng sao cho tổng trọng số nhỏ nhất. Trọng số cạnh nối hai điểm là khoảng cách Manhattan giữa chúng. Để đơn giản, giả sử các điểm đều có vị trí khác nhau.
Dưới đây là cách tìm cây khung nhỏ nhất trong $O(n \log{n})$ bằng cách tìm với mỗi điểm láng giềng gần nhất của nó trong từng bát phân, như hình dưới. Ta thu được $O(n)$ cạnh ứng viên; như sẽ trình bày bên dưới, chúng được đảm bảo chứa cây khung nhỏ nhất. Bước cuối là dùng một thuật toán cây khung nhỏ nhất thông thường, chẳng hạn [thuật toán Kruskal dùng cấu trúc hợp nhất tập rời nhau](https://cp-algorithms.com/graph/mst_kruskal_with_dsu.html).

<div style="text-align: center;">
  <img src="manhattan-mst-octants.png" alt="Hình tám bát phân">
  *Tám bát phân đối với điểm S*
</div>

Thuật toán này được trình bày lần đầu trong bài báo của [H. Zhou, N. Shenoy và W. Nichollos (2002)](https://ieeexplore.ieee.org/document/913303). Một thuật toán khác của [J. Stolfi](https://www.academia.edu/15667173/On_computing_all_north_east_nearest_neighbors_in_the_L1_metric) dùng chia để trị cũng rất thú vị và chỉ khác ở cách tìm láng giềng gần nhất trong từng bát phân. Cả hai có cùng độ phức tạp, nhưng thuật toán ở đây dễ cài đặt hơn và có hằng số nhỏ hơn.

Trước hết, hãy xem vì sao chỉ cần xét láng giềng gần nhất trong mỗi bát phân. Ý tưởng là chứng minh rằng với điểm $s$ và hai điểm khác $p$ và $q$ trong cùng bát phân, ta có $d(p, q) < \max(d(s, p), d(s, q))$. Điều này quan trọng vì nếu có cây khung nhỏ nhất mà $s$ nối với cả $p$ và $q$, ta có thể xóa một trong hai cạnh và thêm cạnh $(p,q)$, làm giảm tổng chi phí. Để chứng minh, không mất tính tổng quát, giả sử $p$ và $q$ thuộc bát phân $R_1$ được xác định bởi $x_s \leq x$ và $x_s - y_s > x -  y$, rồi xét từng trường hợp. Hình dưới cho trực giác về kết quả này.

<div style="text-align: center;">
  <img src="manhattan-mst-uniqueness.png" alt="láng giềng gần nhất duy nhất">
  *Trực giác: giới hạn của bát phân khiến $p$ và $q$ không thể đồng thời gần $s$ hơn là gần nhau*
</div>


Vậy câu hỏi chính là làm sao tìm láng giềng gần nhất trong từng bát phân cho mỗi một trong $n$ điểm.

## Láng giềng gần nhất trong mỗi bát phân trong O(n log n)

Để đơn giản, ta tập trung vào bát phân bắc–đông bắc ($R_1$ trong hình trên). Có thể tìm các hướng còn lại bằng cùng thuật toán sau khi quay đầu vào.

Ta dùng phương pháp đường quét. Ta xử lý các điểm từ tây nam sang đông bắc, tức theo thứ tự $x + y$ không giảm. Ta cũng duy trì tập các điểm chưa tìm được láng giềng gần nhất, gọi là "tập hoạt động". Các hình sau giúp trực quan hóa thuật toán.

<div style="text-align: center;">
  <img src="manhattan-mst-sweep-line-1.png" alt="đường quét cho cây khung Manhattan">
  *Mũi tên đen cho biết hướng quét. Các điểm dưới đường thẳng thuộc tập hoạt động, còn các điểm phía trên chưa được xử lý. Màu xanh chỉ các điểm thuộc bát phân của điểm đang xử lý; màu đỏ chỉ các điểm không thuộc bát phân cần tìm.*
</div>

<div style="text-align: center;">
  <img src="manhattan-mst-sweep-line-2.png" alt="đường quét cho cây khung Manhattan">
  *Hình này cho thấy tập hoạt động sau khi xử lý điểm $p$.  $2$ điểm xanh ở hình trước có $p$ trong bát phân bắc–đông bắc và không còn thuộc tập hoạt động vì đã tìm được láng giềng gần nhất.*
</div>

Khi thêm điểm mới $p$, với mọi điểm $s$ có $p$ trong bát phân đang xét, ta có thể gán $p$ làm láng giềng gần nhất. Thật vậy, khoảng cách giữa chúng là $d(p,s) = |x_p - x_s| + |y_p - y_s| = (x_p + y_p) - (x_s + y_s)$ vì $p$ nằm trong bát phân bắc–đông bắc. Do đã sắp xếp, các điểm sau không có giá trị $x + y$ nhỏ hơn, nên $p$ được đảm bảo có khoảng cách nhỏ hơn. Ta xóa các điểm đó khỏi tập hoạt động, rồi thêm $p$ vào tập.

Câu hỏi tiếp theo là tìm hiệu quả các điểm $s$ có $p$ trong bát phân bắc–đông bắc, tức là những điểm $s$ thỏa mãn:

- $x_s \leq x_p$
- $x_p - y_p < x_s - y_s$

Vì không điểm nào trong tập hoạt động nằm trong vùng $R_1$ của điểm khác, với hai điểm $q_1$ và $q_2$ trong tập này ta có $x_{q_1} \neq x_{q_2}$ và thứ tự của chúng thỏa mãn $x_{q_1} < x_{q_2} \implies x_{q_1} - y_{q_1} \leq x_{q_2} - y_{q_2}$.

Có thể hình dung điều này qua các hình trên bằng cách xem thứ tự $x - y$ như một "đường quét" đi từ tây bắc xuống đông nam, vuông góc với đường được vẽ.

Điều này có nghĩa là nếu giữ tập hoạt động theo thứ tự $x$, các ứng viên $s$ nằm liên tiếp. Ta có thể tìm $x_s \leq x_p$ lớn nhất rồi xử lý các điểm theo thứ tự $x$ giảm dần cho đến khi điều kiện thứ hai $x_p - y_p < x_s - y_s$ không còn đúng (thực ra ta có thể cho phép $x_p - y_p = x_s - y_s$ để xử lý trường hợp các điểm có tọa độ bằng nhau). Vì xóa điểm khỏi tập ngay sau khi xử lý, độ phức tạp khấu hao là $O(n \log(n))$.
	Sau khi có điểm gần nhất ở hướng đông bắc, ta quay các điểm và lặp lại. Có thể chứng minh rằng cách này đồng thời tìm được điểm gần nhất ở hướng tây nam, nên chỉ cần lặp 4 lần thay vì 8.

Tóm lại:

- Sắp xếp các điểm theo $x + y$ không giảm;
- Với mỗi điểm, duyệt tập hoạt động từ điểm có $x$ lớn nhất thỏa mãn $x \leq x_p$ và dừng nếu $x_p - y_p \geq x_s - y_s$. Với mỗi điểm $s$ hợp lệ, thêm cạnh $(s,p, d(s,p))$ vào danh sách;
- Thêm điểm $p$ vào tập hoạt động;
- Quay các điểm và lặp lại cho đến khi duyệt tất cả các bát phân.
- Áp dụng thuật toán Kruskal trên danh sách cạnh để tìm cây khung nhỏ nhất. 

Dưới đây là một bản cài đặt dựa trên [KACTL](https://github.com/kth-competitive-programming/kactl/blob/main/content/geometry/ManhattanMST.h).

```{.cpp file=manhattan_mst}
struct point {
    long long x, y;
};

// Returns a list of edges in the format (weight, u, v). 
// Passing this list to Kruskal algorithm will give the Manhattan MST.
vector<tuple<long long, int, int>> manhattan_mst_edges(vector<point> ps) {
    vector<int> ids(ps.size());
    iota(ids.begin(), ids.end(), 0);
    vector<tuple<long long, int, int>> edges;
    for (int rot = 0; rot < 4; rot++) { // for every rotation
        sort(ids.begin(), ids.end(), [&](int i, int j){
            return (ps[i].x + ps[i].y) < (ps[j].x + ps[j].y);
        });
        map<int, int, greater<int>> active; // (xs, id)
        for (auto i : ids) {
            for (auto it = active.lower_bound(ps[i].x); it != active.end();
            active.erase(it++)) {
                int j = it->second;
                if (ps[i].x - ps[i].y > ps[j].x - ps[j].y) break;
                assert(ps[i].x >= ps[j].x && ps[i].y >= ps[j].y);
                edges.push_back({(ps[i].x - ps[j].x) + (ps[i].y - ps[j].y), i, j});
            }
            active[ps[i].x] = i;
        }
        for (auto &p : ps) { // rotate
            if (rot & 1) p.x *= -1;
            else swap(p.x, p.y);
        }
    }
    return edges;
}
```

## Bài tập
 * [AtCoder Beginner Contest 178E - Dist Max](https://atcoder.jp/contests/abc178/tasks/abc178_e)
 * [CodeForces 1093G - Multidimensional Queries](https://codeforces.com/contest/1093/problem/G)
 * [CodeForces 944F - Game with Tokens](https://codeforces.com/contest/944/problem/F)
 * [AtCoder Code Festival 2017D - Four Coloring](https://atcoder.jp/contests/code-festival-2017-quala/tasks/code_festival_2017_quala_d)
 * [The 2023 ICPC Asia EC Regionals Online Contest (I) - J. Minimum Manhattan Distance](https://codeforces.com/gym/104639/problem/J)
 * [Petrozavodsk Winter Training Camp 2016 Contest 4 - B. Airports](https://codeforces.com/group/eqgxxTNwgd/contest/100959/attachments)
