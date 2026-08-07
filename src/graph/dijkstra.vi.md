---
tags:
  - Translated
e_maxx_link: dijkstra
translation:
  source: graph/dijkstra.md
  source_commit: 6aaec093f6db5e07f22dfef978dc3af674505931
  status: draft
  last_synced: 2026-08-07
---

# Thuật toán Dijkstra

Cho một đồ thị có hướng hoặc vô hướng có trọng số, gồm $n$ đỉnh và $m$ cạnh. Trọng số của mọi cạnh đều không âm. Ta cũng được cho một đỉnh bắt đầu $s$. Bài viết này trình bày cách tìm độ dài đường đi ngắn nhất từ đỉnh bắt đầu $s$ đến mọi đỉnh khác, đồng thời khôi phục chính các đường đi ngắn nhất đó.

Bài toán này còn được gọi là **bài toán đường đi ngắn nhất từ một nguồn** (single-source shortest paths problem).

## Thuật toán

Thuật toán dưới đây được nhà khoa học máy tính người Hà Lan Edsger W. Dijkstra mô tả vào năm 1959.

Ta tạo mảng $d[]$, trong đó với mỗi đỉnh $v$, giá trị $d[v]$ lưu độ dài hiện tại của đường đi ngắn nhất từ $s$ đến $v$.
Ban đầu $d[s] = 0$, còn với mọi đỉnh khác, độ dài này bằng vô cực.
Trong cài đặt, ta dùng một số đủ lớn (được bảo đảm lớn hơn mọi độ dài đường đi có thể xuất hiện) để biểu diễn vô cực.

$$d[v] = \infty,~ v \ne s$$

Ngoài ra, ta duy trì một mảng Boolean $u[]$ cho biết mỗi đỉnh $v$ đã được đánh dấu hay chưa. Ban đầu mọi đỉnh đều chưa được đánh dấu:

$$u[v] = {\rm false}$$

Thuật toán Dijkstra chạy trong $n$ vòng lặp. Ở mỗi vòng, ta chọn một đỉnh chưa được đánh dấu $v$ có giá trị $d[v]$ nhỏ nhất.

Rõ ràng, ở vòng đầu tiên đỉnh bắt đầu $s$ sẽ được chọn.

Đỉnh $v$ được chọn sẽ được đánh dấu. Tiếp theo, từ đỉnh $v$ ta thực hiện các **phép nới lỏng** (relaxations): xét mọi cạnh dạng $(v,\text{to})$ và với mỗi đỉnh $\text{to}$, thuật toán cố gắng cải thiện giá trị $d[\text{to}]$. Nếu trọng số của cạnh hiện tại bằng $len$, phép nới lỏng được viết như sau:

$$d[\text{to}] = \min (d[\text{to}], d[v] + len)$$

Sau khi xét xong tất cả các cạnh như vậy, vòng lặp hiện tại kết thúc. Cuối cùng, sau $n$ vòng lặp, mọi đỉnh đều đã được đánh dấu và thuật toán dừng. Ta sẽ chứng minh rằng các giá trị $d[v]$ thu được chính là độ dài đường đi ngắn nhất từ $s$ đến mọi đỉnh $v$.

Nếu một số đỉnh không thể đi tới từ đỉnh bắt đầu $s$, giá trị $d[v]$ của chúng sẽ vẫn là vô cực. Khi đó, một vài vòng cuối của thuật toán sẽ chọn các đỉnh này nhưng không thực hiện được công việc hữu ích nào. Vì vậy, ta có thể dừng thuật toán ngay khi đỉnh được chọn có khoảng cách bằng vô cực.

### Khôi phục đường đi ngắn nhất

Thông thường ta không chỉ cần biết độ dài đường đi ngắn nhất mà còn cần chính đường đi đó. Ta sẽ lưu thêm đủ thông tin để khôi phục đường đi ngắn nhất từ $s$ đến một đỉnh bất kỳ. Duy trì một mảng đỉnh trước $p[]$, trong đó với mỗi đỉnh $v \ne s$, $p[v]$ là đỉnh đứng ngay trước $v$ trên đường đi ngắn nhất từ $s$ đến $v$. Ta dùng tính chất sau: nếu lấy đường đi ngắn nhất đến một đỉnh $v$ rồi bỏ $v$ khỏi đường đi, ta nhận được một đường đi kết thúc tại $p[v]$, và đường đi này cũng là ngắn nhất đối với đỉnh $p[v]$. Nhờ mảng đỉnh trước, ta có thể khôi phục đường đi đến bất kỳ đỉnh nào: bắt đầu từ $v$, liên tục chuyển sang đỉnh trước của đỉnh hiện tại cho đến khi tới đỉnh bắt đầu $s$. Khi đó ta thu được đường đi theo thứ tự ngược. Vì vậy, đường đi ngắn nhất $P$ đến đỉnh $v$ có dạng:

$$P = (s, \ldots, p[p[p[v]]], p[p[v]], p[v], v)$$

Việc xây dựng mảng đỉnh trước rất đơn giản: với mỗi phép nới lỏng thành công, tức là khi từ một đỉnh được chọn $v$ ta cải thiện được khoảng cách đến đỉnh $\text{to}$, ta cập nhật đỉnh trước của $\text{to}$ thành $v$:

$$p[\text{to}] = v$$

## Chứng minh

Khẳng định chính làm cơ sở cho tính đúng đắn của thuật toán Dijkstra là:

**Sau khi một đỉnh $v$ được đánh dấu, khoảng cách hiện tại đến nó $d[v]$ là khoảng cách ngắn nhất và sẽ không bao giờ thay đổi nữa.**

Ta chứng minh bằng quy nạp. Ở vòng lặp đầu tiên, khẳng định là hiển nhiên: đỉnh duy nhất được đánh dấu là $s$, và $d[s] = 0$ đúng là độ dài đường đi ngắn nhất đến $s$. Giả sử khẳng định đúng với mọi vòng trước, tức là đúng với tất cả các đỉnh đã được đánh dấu; ta cần chứng minh nó vẫn đúng sau vòng hiện tại. Gọi $v$ là đỉnh được chọn ở vòng hiện tại, tức là đỉnh sắp được đánh dấu. Ta cần chứng minh rằng $d[v]$ thực sự bằng độ dài đường đi ngắn nhất đến nó, ký hiệu là $l[v]$.

Xét đường đi ngắn nhất $P$ đến đỉnh $v$. Ta chia đường đi này thành hai phần: $P_1$ chỉ gồm các đỉnh đã được đánh dấu (ít nhất đỉnh bắt đầu $s$ thuộc $P_1$), và phần còn lại $P_2$ (phần này có thể chứa một đỉnh đã được đánh dấu, nhưng luôn bắt đầu bằng một đỉnh chưa được đánh dấu). Gọi đỉnh đầu tiên của $P_2$ là $p$, và đỉnh cuối cùng của $P_1$ là $q$.

Trước hết, ta chứng minh khẳng định với đỉnh $p$, tức là $d[p] = l[p]$.
Điều này gần như hiển nhiên: ở một vòng trước, ta đã chọn đỉnh $q$ và thực hiện phép nới lỏng từ nó.
Do cách chọn đỉnh $p$, đường đi ngắn nhất đến $p$ chính là đường đi ngắn nhất đến $q$ cộng với cạnh $(p,q)$, nên phép nới lỏng từ $q$ đã đặt $d[p]$ bằng độ dài đường đi ngắn nhất $l[p]$.

Vì trọng số các cạnh không âm, độ dài đường đi ngắn nhất $l[p]$ (mà ta vừa chứng minh bằng $d[p]$) không vượt quá độ dài $l[v]$ của đường đi ngắn nhất đến đỉnh $v$. Đồng thời $l[v] \le d[v]$ (vì Dijkstra không thể tìm được một đường đi ngắn hơn chính đường đi ngắn nhất), nên ta có:

$$d[p] = l[p] \le l[v] \le d[v]$$

Mặt khác, vì cả $p$ và $v$ đều chưa được đánh dấu, và vòng hiện tại chọn $v$ chứ không phải $p$, ta có bất đẳng thức:

$$d[p] \ge d[v]$$

Từ hai bất đẳng thức trên suy ra $d[p] = d[v]$, và kết hợp với các đẳng thức đã có, ta được:

$$d[v] = l[v]$$

Q.E.D.

## Cài đặt

Thuật toán Dijkstra thực hiện $n$ vòng lặp. Ở mỗi vòng, nó chọn một đỉnh chưa được đánh dấu $v$ có giá trị $d[v]$ nhỏ nhất, đánh dấu đỉnh này rồi xét mọi cạnh $(v, \text{to})$ để cố gắng cải thiện $d[\text{to}]$.

Thời gian chạy của thuật toán gồm:

* $n$ lần tìm đỉnh có giá trị $d[v]$ nhỏ nhất trong số $O(n)$ đỉnh chưa được đánh dấu
* $m$ lần thử nới lỏng

Trong cài đặt đơn giản nhất, mỗi lần tìm đỉnh cần $O(n)$ phép toán, còn mỗi phép nới lỏng thực hiện được trong $O(1)$. Vì vậy độ phức tạp tổng thể là:

$$O(n^2+m)$$ 

Độ phức tạp này tối ưu cho đồ thị dày, tức là khi $m \approx n^2$.
Tuy nhiên, với đồ thị thưa, khi $m$ nhỏ hơn nhiều so với số cạnh tối đa $n^2$, bài toán có thể được giải trong $O(n \log n + m)$. Thuật toán và cài đặt được trình bày trong bài [Dijkstra trên đồ thị thưa](dijkstra_sparse.md).


```{.cpp file=dijkstra_dense}
const int INF = 1000000000;
vector<vector<pair<int, int>>> adj;

void dijkstra(int s, vector<int> & d, vector<int> & p) {
    int n = adj.size();
    d.assign(n, INF);
    p.assign(n, -1);
    vector<bool> u(n, false);

    d[s] = 0;
    for (int i = 0; i < n; i++) {
        int v = -1;
        for (int j = 0; j < n; j++) {
            if (!u[j] && (v == -1 || d[j] < d[v]))
                v = j;
        }
        
        if (d[v] == INF)
            break;
        
        u[v] = true;
        for (auto edge : adj[v]) {
            int to = edge.first;
            int len = edge.second;
            
            if (d[v] + len < d[to]) {
                d[to] = d[v] + len;
                p[to] = v;
            }
        }
    }
}
```

Ở đây đồ thị $\text{adj}$ được lưu dưới dạng danh sách kề: với mỗi đỉnh $v$, $\text{adj}[v]$ chứa danh sách các cạnh đi ra từ đỉnh này, tức là danh sách các `pair<int,int>` mà phần tử thứ nhất là đỉnh ở đầu còn lại của cạnh, còn phần tử thứ hai là trọng số cạnh.

Hàm nhận đỉnh bắt đầu $s$ và hai vector dùng làm giá trị trả về.

Trước tiên, code khởi tạo các mảng: khoảng cách $d[]$, trạng thái đánh dấu $u[]$ và đỉnh trước $p[]$. Sau đó nó thực hiện $n$ vòng lặp. Ở mỗi vòng, chọn đỉnh $v$ có khoảng cách $d[v]$ nhỏ nhất trong số các đỉnh chưa được đánh dấu. Nếu khoảng cách đến đỉnh $v$ bằng vô cực, thuật toán dừng. Nếu không, đỉnh được đánh dấu và mọi cạnh đi ra từ nó được xét. Nếu có thể nới lỏng theo một cạnh (tức là cải thiện được $d[\text{to}]$), ta cập nhật khoảng cách $d[\text{to}]$ và đỉnh trước $p[\text{to}]$.

Sau khi hoàn tất các vòng lặp, mảng $d[]$ lưu độ dài đường đi ngắn nhất đến mọi đỉnh, còn mảng $p[]$ lưu đỉnh trước của mọi đỉnh (trừ đỉnh bắt đầu $s$). Đường đi đến một đỉnh bất kỳ $t$ có thể được khôi phục như sau:

```{.cpp file=dijkstra_restore_path}
vector<int> restore_path(int s, int t, vector<int> const& p) {
    vector<int> path;

    for (int v = t; v != s; v = p[v])
        path.push_back(v);
    path.push_back(s);

    reverse(path.begin(), path.end());
    return path;
}
```

## Tài liệu tham khảo

* Edsger Dijkstra. A note on two problems in connexion with graphs [1959]
* Thomas Cormen, Charles Leiserson, Ronald Rivest, Clifford Stein. Introduction to Algorithms [2005]

## Bài tập luyện tập
* [Timus - Ivan's Car](http://acm.timus.ru/problem.aspx?space=1&num=1930) [Difficulty:Medium]
* [Timus - Sightseeing Trip](http://acm.timus.ru/problem.aspx?space=1&num=1004)
* [SPOJ - SHPATH](http://www.spoj.com/problems/SHPATH/) [Difficulty:Easy]
* [Codeforces - Dijkstra?](http://codeforces.com/problemset/problem/20/C) [Difficulty:Easy]
* [Codeforces - Shortest Path](http://codeforces.com/problemset/problem/59/E)
* [Codeforces - Jzzhu and Cities](http://codeforces.com/problemset/problem/449/B)
* [Codeforces - The Classic Problem](http://codeforces.com/problemset/problem/464/E)
* [Codeforces - President and Roads](http://codeforces.com/problemset/problem/567/E)
* [Codeforces - Complete The Graph](http://codeforces.com/problemset/problem/715/B)
* [TopCoder - SkiResorts](https://community.topcoder.com/stat?c=problem_statement&pm=12468)
* [TopCoder - MaliciousPath](https://community.topcoder.com/stat?c=problem_statement&pm=13596)
* [SPOJ - Ada and Trip](http://www.spoj.com/problems/ADATRIP/)
* [LA - 3850 - Here We Go(relians) Again](https://vjudge.net/problem/UVALive-3850)
* [GYM - Destination Unknown (D)](http://codeforces.com/gym/100625)
* [UVA 12950 - Even Obsession](https://uva.onlinejudge.org/index.php?option=onlinejudge&page=show_problem&problem=4829)
* [GYM - Journey to Grece (A)](http://codeforces.com/gym/100753)
* [UVA 13030 - Brain Fry](https://uva.onlinejudge.org/index.php?option=com_onlinejudge&Itemid=8&category=866&page=show_problem&problem=4918)
* [UVA 1027 - Toll](https://uva.onlinejudge.org/index.php?option=onlinejudge&page=show_problem&problem=3468)
* [UVA 11377 - Airport Setup](https://uva.onlinejudge.org/index.php?option=onlinejudge&page=show_problem&problem=2372)
* [Codeforces - Dynamic Shortest Path](http://codeforces.com/problemset/problem/843/D)
* [UVA 11813 - Shopping](https://uva.onlinejudge.org/index.php?option=com_onlinejudge&Itemid=8&page=show_problem&problem=2913)
* [UVA 11833 - Route Change](https://uva.onlinejudge.org/index.php?option=com_onlinejudge&Itemid=8&category=226&page=show_problem&problem=2933)
* [SPOJ - Easy Dijkstra Problem](http://www.spoj.com/problems/EZDIJKST/en/)
* [LA - 2819 - Cave Raider](https://vjudge.net/problem/UVALive-2819)
* [UVA 12144 - Almost Shortest Path](https://uva.onlinejudge.org/index.php?option=onlinejudge&page=show_problem&problem=3296)
* [UVA 12047 - Highest Paid Toll](https://uva.onlinejudge.org/index.php?option=com_onlinejudge&Itemid=8&page=show_problem&problem=3198)
* [UVA 11514 - Batman](https://uva.onlinejudge.org/index.php?option=onlinejudge&page=show_problem&problem=2509)
* [Codeforces - Team Rocket Rises Again](http://codeforces.com/contest/757/problem/F)
* [UVA - 11338 - Minefield](https://uva.onlinejudge.org/index.php?option=com_onlinejudge&Itemid=8&page=show_problem&problem=2313)
* [UVA 11374 - Airport Express](https://uva.onlinejudge.org/index.php?option=com_onlinejudge&Itemid=8&page=show_problem&problem=2369)
* [UVA 11097 - Poor My Problem](https://uva.onlinejudge.org/index.php?option=com_onlinejudge&Itemid=8&page=show_problem&problem=2038)
* [UVA 13172 - The music teacher](https://uva.onlinejudge.org/index.php?option=onlinejudge&Itemid=8&page=show_problem&problem=5083)
* [Codeforces - Dirty Arkady's Kitchen](http://codeforces.com/contest/827/problem/F)
* [SPOJ - Delivery Route](http://www.spoj.com/problems/DELIVER/)
* [SPOJ - Costly Chess](http://www.spoj.com/problems/CCHESS/)
* [CSES - Shortest Routes 1](https://cses.fi/problemset/task/1671)
* [CSES - Flight Discount](https://cses.fi/problemset/task/1195)
* [CSES - Flight Routes](https://cses.fi/problemset/task/1196)
