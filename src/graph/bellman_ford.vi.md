---
tags:
  - Translated
e_maxx_link: ford_bellman
translation:
  source: graph/bellman_ford.md
  source_commit: b9f9ab626cc8e7104ee356592084b85993ec9ebb
  status: draft
  last_synced: 2026-08-07
---

# Thuật toán Bellman-Ford

**Đường đi ngắn nhất từ một nguồn với cạnh có trọng số âm**

Giả sử ta được cho một đồ thị có hướng có trọng số $G$ gồm $n$ đỉnh và $m$ cạnh, cùng một đỉnh xác định $v$. Mục tiêu là tìm độ dài đường đi ngắn nhất từ đỉnh $v$ đến mọi đỉnh còn lại.

Khác với thuật toán Dijkstra, Bellman-Ford có thể áp dụng cho đồ thị chứa cạnh có trọng số âm. Tuy nhiên, nếu đồ thị chứa chu trình âm thì đường đi ngắn nhất đến một số đỉnh có thể không tồn tại (vì trọng số đường đi có thể giảm tới âm vô cực). Dù vậy, thuật toán có thể được sửa đổi để phát hiện sự tồn tại của chu trình âm, thậm chí khôi phục chính chu trình đó.

Thuật toán mang tên hai nhà khoa học người Mỹ Richard Bellman và Lester Ford. Ford thực tế đã phát minh thuật toán này vào năm 1956 khi nghiên cứu một bài toán toán học khác, cuối cùng bài toán đó được quy về một bài toán con tìm đường đi ngắn nhất trên đồ thị; Ford đã đưa ra phác thảo thuật toán để giải bài toán. Năm 1958, Bellman công bố một bài báo tập trung riêng vào bài toán đường đi ngắn nhất và trình bày rõ thuật toán theo dạng mà ngày nay chúng ta biết đến.

## Mô tả thuật toán

Trước hết giả sử đồ thị không chứa chu trình âm. Trường hợp có chu trình âm sẽ được xét riêng ở phần sau.

Ta tạo mảng khoảng cách $d[0 \ldots n-1]$, sau khi thuật toán kết thúc mảng này sẽ chứa đáp án. Ban đầu đặt $d[v] = 0$, còn mọi phần tử khác của $d[ ]$ bằng vô cực $\infty$.

Thuật toán gồm nhiều pha. Trong mỗi pha, ta duyệt qua toàn bộ các cạnh của đồ thị và cố gắng thực hiện **phép nới lỏng** trên mỗi cạnh $(a,b)$ có trọng số $c$. Nới lỏng cạnh là thử cải thiện giá trị $d[b]$ bằng $d[a] + c$. Nói cách khác, ta cố gắng cải thiện đáp án cho đỉnh $b$ bằng cách đi tới nó qua cạnh $(a,b)$ từ đáp án hiện tại của đỉnh $a$.

Ta khẳng định rằng $n-1$ pha là đủ để tính đúng độ dài mọi đường đi ngắn nhất trong đồ thị (vẫn với giả thiết không tồn tại chu trình âm). Với các đỉnh không thể đi tới từ nguồn, khoảng cách $d[ ]$ sẽ vẫn bằng vô cực $\infty$.

## Cài đặt

Khác với nhiều thuật toán đồ thị khác, với Bellman-Ford ta thường biểu diễn đồ thị thuận tiện nhất bằng một danh sách duy nhất chứa tất cả các cạnh, thay vì $n$ danh sách cạnh đi ra từ từng đỉnh. Ta bắt đầu cài đặt bằng cấu trúc $\rm edge$ để biểu diễn cạnh. Đầu vào của thuật toán gồm $n$, $m$, danh sách cạnh $e$ và đỉnh bắt đầu $v$. Các đỉnh được đánh số từ $0$ đến $n - 1$.

### Cài đặt đơn giản nhất

Hằng số $\rm INF$ biểu diễn giá trị "vô cực" — cần chọn nó đủ lớn để lớn hơn mọi độ dài đường đi có thể xuất hiện.

```cpp
struct Edge {
    int a, b, cost;
};

int n, m, v;
vector<Edge> edges;
const int INF = 1000000000;

void solve()
{
    vector<int> d(n, INF);
    d[v] = 0;
    for (int i = 0; i < n - 1; ++i)
        for (Edge e : edges)
            if (d[e.a] < INF)
                d[e.b] = min(d[e.b], d[e.a] + e.cost);
    // display d, for example, on the screen
}
```

Điều kiện `if (d[e.a] < INF)` chỉ cần thiết khi đồ thị có cạnh trọng số âm: nếu bỏ kiểm tra này, thuật toán có thể nới lỏng từ những đỉnh mà ta chưa tìm được đường đi tới, làm xuất hiện các khoảng cách sai dạng $\infty - 1$, $\infty - 2$, v.v.

### Cài đặt tốt hơn

Có thể tăng tốc thuật toán trong thực tế: thường đáp án đã ổn định sau một vài pha, còn các pha sau chỉ tiếp tục duyệt toàn bộ cạnh mà không làm được công việc hữu ích. Vì vậy, ta duy trì một cờ cho biết trong pha hiện tại có giá trị nào thay đổi hay không; nếu một pha không có thay đổi, thuật toán có thể dừng. Tối ưu này không cải thiện độ phức tạp tiệm cận — vẫn có những đồ thị cần đủ $n-1$ pha — nhưng thường giúp thuật toán nhanh hơn đáng kể trên dữ liệu trung bình, chẳng hạn các đồ thị ngẫu nhiên.

Với tối ưu này, nhìn chung không cần tự giới hạn số pha ở $n-1$: thuật toán sẽ tự dừng sau khi đạt số pha cần thiết.

```cpp
void solve()
{
    vector<int> d(n, INF);
    d[v] = 0;
    for (;;) {
        bool any = false;

        for (Edge e : edges)
            if (d[e.a] < INF)
                if (d[e.b] > d[e.a] + e.cost) {
                    d[e.b] = d[e.a] + e.cost;
                    any = true;
                }

        if (!any)
            break;
    }
    // display d, for example, on the screen
}
```

### Khôi phục đường đi

Bây giờ ta xem cách sửa thuật toán để không chỉ tìm độ dài đường đi ngắn nhất mà còn khôi phục được chính các đường đi đó.

Ta tạo thêm mảng $p[0 \ldots n-1]$, trong đó với mỗi đỉnh ta lưu "đỉnh trước" của nó, tức đỉnh đứng ngay trước nó trên đường đi ngắn nhất dẫn tới đỉnh đó. Thực chất, đường đi ngắn nhất đến một đỉnh $a$ là đường đi ngắn nhất đến một đỉnh nào đó $p[a]$, rồi nối thêm $a$ ở cuối.

Thuật toán hoạt động theo đúng logic này: giả sử khoảng cách ngắn nhất đến một đỉnh đã được tính, rồi dùng đỉnh đó để cố gắng cải thiện khoảng cách đến các đỉnh khác. Vì vậy, mỗi khi cải thiện thành công, ta chỉ cần ghi lại trong $p[ ]$ đỉnh mà từ đó phép cải thiện xảy ra.

Dưới đây là cài đặt Bellman-Ford có khả năng khôi phục đường đi ngắn nhất tới một đỉnh cho trước $t$:

```cpp
void solve()
{
    vector<int> d(n, INF);
    d[v] = 0;
    vector<int> p(n, -1);

    for (;;) {
        bool any = false;
        for (Edge e : edges)
            if (d[e.a] < INF)
                if (d[e.b] > d[e.a] + e.cost) {
                    d[e.b] = d[e.a] + e.cost;
                    p[e.b] = e.a;
                    any = true;
                }
        if (!any)
            break;
    }

    if (d[t] == INF)
        cout << "No path from " << v << " to " << t << ".";
    else {
        vector<int> path;
        for (int cur = t; cur != -1; cur = p[cur])
            path.push_back(cur);
        reverse(path.begin(), path.end());

        cout << "Path from " << v << " to " << t << ": ";
        for (int u : path)
            cout << u << ' ';
    }
}
```

Bắt đầu từ đỉnh $t$, ta liên tục đi qua các đỉnh trước cho đến khi tới đỉnh bắt đầu, là đỉnh không có đỉnh trước, đồng thời lưu các đỉnh đã đi qua vào danh sách $\rm path$. Danh sách này chính là đường đi ngắn nhất từ $v$ đến $t$ nhưng theo thứ tự ngược, nên ta gọi hàm $\rm reverse()$ trên $\rm path$ rồi mới xuất đường đi.

## Chứng minh thuật toán

Trước hết, với mọi đỉnh $u$ không thể đi tới từ đỉnh bắt đầu $v$, thuật toán vẫn hoạt động đúng: nhãn $d[u]$ giữ nguyên bằng vô cực, vì Bellman-Ford sẽ tìm một đường nào đó tới mọi đỉnh có thể đi tới từ nguồn $v$, còn phép nới lỏng với các đỉnh còn lại sẽ không bao giờ xảy ra.

Ta chứng minh khẳng định sau: sau khi thực hiện pha thứ $i$, Bellman-Ford tìm đúng mọi đường đi ngắn nhất có số cạnh không vượt quá $i$.

Nói cách khác, với một đỉnh bất kỳ $a$, gọi $k$ là số cạnh trên một đường đi ngắn nhất đến nó (nếu có nhiều đường đi ngắn nhất, có thể chọn bất kỳ một đường). Theo khẳng định này, thuật toán bảo đảm sau pha thứ $k$, đường đi ngắn nhất đến $a$ đã được tìm thấy.

**Chứng minh**:
Xét một đỉnh bất kỳ $a$ có thể đi tới từ đỉnh bắt đầu $v$, và xét một đường đi ngắn nhất tới nó $(p_0=v, p_1, \ldots, p_k=a)$. Trước pha đầu tiên, đường đi ngắn nhất tới đỉnh $p_0 = v$ đã được biết chính xác. Trong pha đầu tiên, cạnh $(p_0,p_1)$ được thuật toán xét, nên khoảng cách đến $p_1$ được tính đúng sau pha đầu tiên. Lặp lại lập luận này $k$ lần, ta thấy sau pha thứ $k$, khoảng cách đến đỉnh $p_k = a$ được tính đúng, đúng như cần chứng minh.

Cuối cùng, một đường đi ngắn nhất không thể có nhiều hơn $n - 1$ cạnh. Vì vậy chạy đến pha thứ $(n-1)$ là đủ; sau đó không còn phép nới lỏng nào có thể cải thiện khoảng cách tới một đỉnh.

## Trường hợp có chu trình âm

Ở các phần trên ta giả sử đồ thị không có chu trình âm. Chính xác hơn, điều ta quan tâm là chu trình âm có thể đi tới từ đỉnh bắt đầu $v$; một chu trình âm không thể đi tới từ $v$ không làm thay đổi kết quả đã phân tích ở trên. Khi tồn tại chu trình âm có thể đi tới, phát sinh thêm vấn đề: khoảng cách đến mọi đỉnh trên chu trình, cũng như mọi đỉnh có thể đi tới từ chu trình đó, không được xác định — về mặt ý nghĩa chúng phải bằng âm vô cực $(- \infty)$.

Dễ thấy Bellman-Ford có thể liên tục thực hiện phép nới lỏng giữa các đỉnh của chu trình âm và các đỉnh đi tới được từ chu trình. Vì vậy, nếu không giới hạn số pha ở $n - 1$, thuật toán có thể chạy vô hạn và liên tục giảm khoảng cách của các đỉnh đó.

Từ đây ta có **tiêu chuẩn để phát hiện chu trình âm có thể đi tới từ đỉnh nguồn $v$**: sau pha thứ $(n-1)$, nếu chạy thêm một pha và vẫn thực hiện được ít nhất một phép nới lỏng, thì đồ thị có chu trình âm có thể đi tới từ $v$; nếu không thì không có chu trình như vậy.

Hơn nữa, nếu phát hiện được chu trình như vậy, ta có thể sửa Bellman-Ford để khôi phục chu trình dưới dạng một dãy đỉnh. Chỉ cần nhớ đỉnh cuối cùng $x$ được nới lỏng ở pha thứ $n$. Đỉnh này hoặc nằm trên chu trình âm, hoặc có thể đi tới từ chu trình đó. Để chắc chắn đi vào một đỉnh thuộc chu trình âm, bắt đầu từ $x$ và lần theo đỉnh trước $n$ lần. Khi đó ta tới một đỉnh $y$ được bảo đảm nằm trên chu trình âm. Tiếp tục đi qua các đỉnh trước từ $y$ cho tới khi quay lại chính $y$; điều này chắc chắn xảy ra vì các phép nới lỏng trên chu trình âm diễn ra theo vòng.

### Cài đặt:

```cpp
void solve()
{
    vector<int> d(n, INF);
    d[v] = 0;
    vector<int> p(n, -1);
    int x;
    for (int i = 0; i < n; ++i) {
        x = -1;
        for (Edge e : edges)
            if (d[e.a] < INF)
                if (d[e.b] > d[e.a] + e.cost) {
                    d[e.b] = max(-INF, d[e.a] + e.cost);
                    p[e.b] = e.a;
                    x = e.b;
                }
    }

    if (x == -1)
        cout << "No negative cycle from " << v;
    else {
        int y = x;
        for (int i = 0; i < n; ++i)
            y = p[y];

        vector<int> path;
        for (int cur = y;; cur = p[cur]) {
            path.push_back(cur);
            if (cur == y && path.size() > 1)
                break;
        }
        reverse(path.begin(), path.end());

        cout << "Negative cycle: ";
        for (int u : path)
            cout << u << ' ';
    }
}
```

Do có chu trình âm, trong $n$ vòng lặp khoảng cách có thể giảm rất sâu về phía âm, tới cỡ $-n m W$, trong đó $W$ là trị tuyệt đối lớn nhất của một trọng số cạnh. Vì vậy trong code ta dùng biện pháp bổ sung để tránh tràn số nguyên:

```cpp
d[e.b] = max(-INF, d[e.a] + e.cost);
```

Cài đặt trên tìm một chu trình âm có thể đi tới từ một đỉnh bắt đầu $v$. Tuy nhiên, có thể sửa thuật toán để tìm một chu trình âm bất kỳ trong đồ thị: chỉ cần khởi tạo mọi khoảng cách $d[i]$ bằng 0 thay vì vô cực, như thể ta đang tìm đường đi ngắn nhất đồng thời từ tất cả các đỉnh. Tính đúng đắn của việc phát hiện chu trình âm không bị ảnh hưởng.

Xem thêm bài riêng [Tìm chu trình âm trong đồ thị](finding-negative-cycle-in-graph.md).

## Shortest Path Faster Algorithm (SPFA)

SPFA là một cải tiến của Bellman-Ford dựa trên quan sát rằng không phải mọi lần thử nới lỏng đều thành công.
Ý tưởng chính là duy trì một hàng đợi chỉ chứa các đỉnh vừa được nới lỏng và vẫn có khả năng tiếp tục nới lỏng các đỉnh kề.
Mỗi khi nới lỏng thành công một đỉnh kề, ta đưa đỉnh đó vào hàng đợi. Thuật toán này cũng có thể phát hiện chu trình âm giống Bellman-Ford.

Trong trường hợp xấu nhất, độ phức tạp của SPFA vẫn là $O(n m)$ như Bellman-Ford, nhưng trong thực tế nó thường chạy nhanh hơn và một số [nguồn cho rằng độ phức tạp trung bình có thể đạt $O(m)$](https://en.wikipedia.org/wiki/Shortest_Path_Faster_Algorithm#Average-case_performance). Tuy nhiên cần cẩn thận, vì đây là thuật toán tất định và không khó để xây dựng phản ví dụ khiến nó chạy trong $O(n m)$.

Có một số điểm cần chú ý khi cài đặt, chẳng hạn thuật toán có thể chạy vô hạn nếu tồn tại chu trình âm.
Để tránh điều này, có thể lưu một bộ đếm số lần mỗi đỉnh được nới lỏng và dừng ngay khi một đỉnh nào đó được nới lỏng lần thứ $n$.
Ngoài ra, không cần đưa một đỉnh vào hàng đợi nếu nó đã ở trong hàng đợi.

```{.cpp file=spfa}
const int INF = 1000000000;
vector<vector<pair<int, int>>> adj;

bool spfa(int s, vector<int>& d) {
    int n = adj.size();
    d.assign(n, INF);
    vector<int> cnt(n, 0);
    vector<bool> inqueue(n, false);
    queue<int> q;

    d[s] = 0;
    q.push(s);
    inqueue[s] = true;
    while (!q.empty()) {
        int v = q.front();
        q.pop();
        inqueue[v] = false;

        for (auto edge : adj[v]) {
            int to = edge.first;
            int len = edge.second;

            if (d[v] + len < d[to]) {
                d[to] = d[v] + len;
                if (!inqueue[to]) {
                    q.push(to);
                    inqueue[to] = true;
                    cnt[to]++;
                    if (cnt[to] > n)
                        return false;  // negative cycle
                }
            }
        }
    }
    return true;
}
```


## Các bài liên quan trên hệ thống chấm trực tuyến

Danh sách các bài có thể giải bằng thuật toán Bellman-Ford:

* [E-OLYMP #1453 "Ford-Bellman" [difficulty: low]](https://www.e-olymp.com/en/problems/1453)
* [UVA #423 "MPI Maelstrom" [difficulty: low]](http://uva.onlinejudge.org/index.php?option=com_onlinejudge&Itemid=8&page=show_problem&problem=364)
* [UVA #534 "Frogger" [difficulty: medium]](http://uva.onlinejudge.org/index.php?option=com_onlinejudge&Itemid=8&category=7&page=show_problem&problem=475)
* [UVA #10099 "The Tourist Guide" [difficulty: medium]](http://uva.onlinejudge.org/index.php?option=com_onlinejudge&Itemid=8&category=12&page=show_problem&problem=1040)
* [UVA #515 "King" [difficulty: medium]](http://uva.onlinejudge.org/index.php?option=onlinejudge&page=show_problem&problem=456)
* [UVA 12519 - The Farnsworth Parabox](https://uva.onlinejudge.org/index.php?option=com_onlinejudge&Itemid=8&page=show_problem&problem=3964)

Xem thêm danh sách bài tập trong bài [Tìm chu trình âm trong đồ thị](finding-negative-cycle-in-graph.md).
* [CSES - High Score](https://cses.fi/problemset/task/1673)
* [CSES - Cycle Finding](https://cses.fi/problemset/task/1197)
