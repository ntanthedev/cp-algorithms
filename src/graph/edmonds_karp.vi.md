---
tags:
  - Translated
e_maxx_link: edmonds_karp
translation:
  source: graph/edmonds_karp.md
  source_commit: 2436fd3f5b0f5c9f995fef848be78d2b56ba9127
  status: draft
  last_synced: 2026-08-07
---

# Luồng cực đại - Ford-Fulkerson và Edmonds-Karp

Thuật toán Edmonds-Karp là một cách cài đặt phương pháp Ford-Fulkerson để tính luồng cực đại trong một mạng luồng.

## Mạng luồng

Trước hết, ta định nghĩa **mạng luồng** (flow network), **luồng** (flow) và **luồng cực đại** (maximum flow).

Một **mạng** là đồ thị có hướng $G$ với tập đỉnh $V$, tập cạnh $E$ và một hàm $c$ gán cho mỗi cạnh $e \in E$ một số nguyên không âm, gọi là **dung lượng** của $e$.
Một mạng như vậy được gọi là **mạng luồng** nếu ta đánh dấu thêm hai đỉnh: một đỉnh là **nguồn** (source) và một đỉnh là **đích** (sink).

Một **luồng** trong mạng luồng là một hàm $f$, cũng gán cho mỗi cạnh $e$ một số nguyên không âm, chính là lượng luồng trên cạnh đó.
Hàm này phải thỏa mãn hai điều kiện sau:

Luồng trên một cạnh không được vượt quá dung lượng của cạnh đó.

$$f(e) \le c(e)$$

Với mỗi đỉnh $u$ ngoại trừ nguồn và đích, tổng luồng đi vào phải bằng tổng luồng đi ra.

$$\sum_{(v, u) \in E} f((v, u)) = \sum_{(u, v) \in E} f((u, v))$$

Đỉnh nguồn $s$ chỉ có luồng đi ra, còn đỉnh đích $t$ chỉ có luồng đi vào.

Dễ thấy đẳng thức sau luôn đúng:

$$\sum_{(s, u) \in E} f((s, u)) = \sum_{(u, t) \in E} f((u, t))$$

Một cách hình dung trực quan về mạng luồng là hệ thống ống nước:
coi các cạnh là các ống nước, dung lượng của một cạnh là lượng nước lớn nhất có thể chảy qua ống trong một giây, còn luồng trên cạnh là lượng nước hiện đang chảy qua ống trong một giây.
Cách hình dung này giải thích điều kiện thứ nhất: lượng nước chảy qua một ống không thể vượt quá dung lượng của nó.
Các đỉnh đóng vai trò như các nút nối, nơi nước đi vào từ một số ống rồi được phân phối sang các ống khác.
Điều này cũng giải thích điều kiện thứ hai.
Toàn bộ lượng nước đi vào một nút phải được phân phối sang các ống khác.
Nước không thể tự nhiên biến mất hoặc xuất hiện.
Nguồn $s$ là nơi sinh ra toàn bộ nước, và nước chỉ có thể thoát ra tại đích $t$.

Hình dưới đây minh họa một mạng luồng.
Giá trị thứ nhất trên mỗi cạnh là luồng, ban đầu bằng 0; giá trị thứ hai là dung lượng.
<div style="text-align: center;">
  <img src="Flow1.png" alt="Flow network">
</div>

Giá trị của luồng trong một mạng là tổng luồng được tạo ra tại nguồn $s$, hay tương đương là tổng luồng được nhận tại đích $t$.
Một **luồng cực đại** là luồng có giá trị lớn nhất có thể.
Bài toán ta muốn giải là tìm luồng cực đại của một mạng luồng.

**Ghi chú bản dịch:** Nguồn tiếng Anh dùng cụm “maximal flow” ở một số vị trí dù bài toán và tiêu đề đều nói về “maximum flow”. Hai khái niệm này có thể khác nhau trong thuật ngữ toán học; bản dịch dùng nhất quán **luồng cực đại** theo đúng bài toán maximum flow và ghi nhận lỗi nguồn để sửa ở PR upstream riêng.

Trong mô hình ống nước, bài toán có thể phát biểu như sau:
ta có thể đẩy tối đa bao nhiêu nước qua hệ thống ống từ nguồn tới đích?

Hình dưới đây minh họa luồng cực đại trong mạng luồng.
<div style="text-align: center;">
  <img src="Flow9.png" alt="Maximal flow">
</div>

## Phương pháp Ford-Fulkerson

Ta cần định nghĩa thêm một khái niệm.
**Dung lượng thặng dư** (residual capacity) của một cạnh có hướng là dung lượng của cạnh trừ đi luồng hiện tại trên cạnh đó.
Cần lưu ý rằng nếu có một luồng trên cạnh có hướng $(u, v)$, thì cạnh ngược có dung lượng 0 và ta có thể định nghĩa luồng trên đó là $f((v, u)) = -f((u, v))$.
Điều này cũng xác định dung lượng thặng dư cho mọi cạnh ngược.
Từ các cạnh này, ta có thể xây dựng **mạng thặng dư** (residual network): vẫn giữ nguyên các đỉnh và cạnh, nhưng dùng dung lượng thặng dư làm dung lượng.

Phương pháp Ford-Fulkerson hoạt động như sau.
Đầu tiên, đặt luồng trên mọi cạnh bằng 0.
Sau đó, ta tìm một **đường tăng luồng** (augmenting path) từ $s$ tới $t$.
Đường tăng luồng là một đường đi đơn trong đồ thị thặng dư mà mọi cạnh trên đường đều có dung lượng thặng dư dương.
Nếu tìm được một đường như vậy, ta có thể tăng luồng dọc theo các cạnh của đường đó.
Ta tiếp tục tìm các đường tăng luồng và tăng luồng.
Khi không còn đường tăng luồng nào nữa, luồng hiện tại là cực đại.

Ta mô tả cụ thể hơn việc tăng luồng dọc theo một đường tăng luồng.
Gọi $C$ là dung lượng thặng dư nhỏ nhất trong số các cạnh trên đường.
Khi đó, với mỗi cạnh $(u, v)$ trên đường, ta cập nhật $f((u, v)) ~\text{+=}~ C$ và $f((v, u)) ~\text{-=}~ C$.

Dưới đây là một ví dụ minh họa phương pháp.
Ta dùng lại mạng luồng ở trên.
Ban đầu, luồng bằng 0.
<div style="text-align: center;">
  <img src="Flow1.png" alt="Flow network">
</div>

Ta có thể tìm đường $s - A - B - t$ với các dung lượng thặng dư lần lượt là 7, 5 và 8.
Giá trị nhỏ nhất là 5, vì vậy ta có thể tăng luồng trên đường này thêm 5.
Khi đó giá trị luồng của mạng là 5.
<div style="text-align: center;">
  <img src="Flow2.png" alt="First path">
  <img src="Flow3.png" alt="Network after first path">
</div>

Ta lại tìm một đường tăng luồng, lần này là $s - D - A - C - t$ với các dung lượng thặng dư 4, 3, 3 và 5.
Do đó ta tăng luồng thêm 3 và thu được luồng có giá trị 8.
<div style="text-align: center;">
  <img src="Flow4.png" alt="Second path">
  <img src="Flow5.png" alt="Network after second path">
</div>

Lần này ta tìm được đường $s - D - C - B - t$ với các dung lượng thặng dư 1, 2, 3 và 3, vì vậy ta tăng luồng thêm 1.
<div style="text-align: center;">
  <img src="Flow6.png" alt="Third path">
  <img src="Flow7.png" alt="Network after third path">
</div>

Tiếp theo ta tìm được đường tăng luồng $s - A - D - C - t$ với các dung lượng thặng dư 2, 3, 1 và 2.
Ta có thể tăng luồng thêm 1.
Điểm thú vị là đường này chứa cạnh ngược $(A, D)$.
Trong mạng luồng ban đầu, ta không được phép gửi luồng từ $A$ tới $D$.
Nhưng vì hiện đã có luồng bằng 3 từ $D$ tới $A$, việc đi theo cạnh ngược này là hợp lệ.
Trực giác như sau:
thay vì gửi luồng bằng 3 từ $D$ tới $A$, ta chỉ gửi 2, rồi bù lại bằng cách gửi thêm 1 đơn vị luồng từ $s$ tới $A$; nhờ đó ta có thể gửi thêm 1 đơn vị luồng theo đường $D - C - t$.
<div style="text-align: center;">
  <img src="Flow8.png" alt="Fourth path">
  <img src="Flow9.png" alt="Network after fourth path">
</div>

Bây giờ không thể tìm thêm đường tăng luồng nào từ $s$ tới $t$, nên luồng có giá trị $10$ là lớn nhất có thể.
Ta đã tìm được luồng cực đại.

Cần lưu ý rằng phương pháp Ford-Fulkerson không quy định cụ thể cách tìm đường tăng luồng.
Có thể dùng [DFS](depth-first-search.md) hoặc [BFS](breadth-first-search.md), cả hai đều chạy trong $O(E)$.
Nếu mọi dung lượng trong mạng đều là số nguyên, thì mỗi đường tăng luồng làm giá trị luồng của mạng tăng ít nhất 1 (xem thêm [định lý luồng nguyên](#integral-theorem)).
Vì vậy độ phức tạp của Ford-Fulkerson là $O(E F)$, với $F$ là giá trị luồng cực đại của mạng.
Với dung lượng hữu tỉ, thuật toán vẫn dừng nhưng không có cận độ phức tạp như trên.
Với dung lượng vô tỉ, thuật toán có thể không bao giờ dừng, thậm chí có thể không hội tụ tới luồng cực đại.

## Thuật toán Edmonds-Karp

Edmonds-Karp đơn giản là một cách cài đặt phương pháp Ford-Fulkerson, dùng [BFS](breadth-first-search.md) để tìm đường tăng luồng.
Thuật toán được Yefim Dinitz công bố lần đầu vào năm 1970, sau đó Jack Edmonds và Richard Karp công bố độc lập vào năm 1972.

Ta có thể đưa ra độ phức tạp không phụ thuộc vào giá trị luồng cực đại.
Thuật toán chạy trong thời gian $O(V E^2)$, kể cả khi dung lượng là số vô tỉ.
Trực giác là mỗi khi tìm được một đường tăng luồng, một trong các cạnh sẽ bị bão hòa; nếu cạnh đó xuất hiện lại trong một đường tăng luồng về sau thì khoảng cách từ cạnh tới $s$ sẽ lớn hơn.
Độ dài của một đường đi đơn bị chặn bởi $V$.

### Cài đặt

Ma trận `capacity` lưu dung lượng cho mọi cặp đỉnh.
`adj` là danh sách kề của **đồ thị vô hướng**, vì khi tìm đường tăng luồng ta cũng cần sử dụng các cạnh ngược của những cạnh có hướng.

Hàm `maxflow` trả về giá trị của luồng cực đại.
Trong quá trình chạy thuật toán, ma trận `capacity` thực chất lưu dung lượng thặng dư của mạng.
Giá trị luồng trên từng cạnh không được lưu trực tiếp, nhưng có thể dễ dàng mở rộng cài đặt bằng một ma trận bổ sung để lưu luồng và trả về nó.

```{.cpp file=edmondskarp}
int n;
vector<vector<int>> capacity;
vector<vector<int>> adj;

int bfs(int s, int t, vector<int>& parent) {
    fill(parent.begin(), parent.end(), -1);
    parent[s] = -2;
    queue<pair<int, int>> q;
    q.push({s, INF});

    while (!q.empty()) {
        int cur = q.front().first;
        int flow = q.front().second;
        q.pop();

        for (int next : adj[cur]) {
            if (parent[next] == -1 && capacity[cur][next]) {
                parent[next] = cur;
                int new_flow = min(flow, capacity[cur][next]);
                if (next == t)
                    return new_flow;
                q.push({next, new_flow});
            }
        }
    }

    return 0;
}

int maxflow(int s, int t) {
    int flow = 0;
    vector<int> parent(n);
    int new_flow;

    while (new_flow = bfs(s, t, parent)) {
        flow += new_flow;
        int cur = t;
        while (cur != s) {
            int prev = parent[cur];
            capacity[prev][cur] -= new_flow;
            capacity[cur][prev] += new_flow;
            cur = prev;
        }
    }

    return flow;
}
```

## Định lý luồng nguyên ## { #integral-theorem}

Định lý phát biểu rằng nếu mọi dung lượng trong mạng đều là số nguyên, thì giá trị của luồng cực đại là một số nguyên, đồng thời tồn tại một luồng cực đại mà luồng trên mỗi cạnh cũng là số nguyên. Cụ thể, phương pháp Ford-Fulkerson sẽ tìm được một luồng như vậy.

## Định lý luồng cực đại - lát cắt cực tiểu

Một **$s$-$t$-cut** là một cách chia các đỉnh của mạng luồng thành hai tập, sao cho một tập chứa nguồn $s$ và tập còn lại chứa đích $t$.
Dung lượng của một $s$-$t$-cut được định nghĩa là tổng dung lượng của các cạnh đi từ phía chứa nguồn sang phía chứa đích.

Rõ ràng ta không thể gửi từ $s$ tới $t$ lượng luồng lớn hơn dung lượng của bất kỳ $s$-$t$-cut nào.
Vì vậy, luồng cực đại bị chặn trên bởi dung lượng của lát cắt cực tiểu.

Định lý luồng cực đại - lát cắt cực tiểu còn khẳng định mạnh hơn.
Nó nói rằng giá trị của luồng cực đại bằng đúng dung lượng của lát cắt cực tiểu.

Trong hình dưới đây là lát cắt cực tiểu của mạng luồng đã dùng ở trên.
Dung lượng của lát cắt $\{s, A, D\}$ và $\{B, C, t\}$ là $5 + 3 + 2 = 10$, đúng bằng giá trị luồng cực đại ta đã tìm được.
Các lát cắt khác có dung lượng lớn hơn, chẳng hạn lát cắt giữa $\{s, A\}$ và $\{B, C, D, t\}$ có dung lượng $4 + 3 + 5 = 12$.
<div style="text-align: center;">
  <img src="Cut.png" alt="Minimum cut">
</div>

Sau khi tính luồng cực đại bằng phương pháp Ford-Fulkerson, ta có thể tìm một lát cắt cực tiểu.
Một lát cắt cực tiểu có thể được tạo như sau:
một tập gồm tất cả các đỉnh có thể đi tới từ $s$ trong đồ thị thặng dư bằng các cạnh có dung lượng thặng dư dương, và tập còn lại gồm mọi đỉnh khác.
Phân hoạch này có thể tìm dễ dàng bằng [DFS](depth-first-search.md) bắt đầu từ $s$.

## Bài tập luyện tập
- [Codeforces - Array and Operations](https://codeforces.com/contest/498/problem/c)
- [Codeforces - Red-Blue Graph](https://codeforces.com/contest/1288/problem/f)
- [CSES - Download Speed](https://cses.fi/problemset/task/1694)
- [CSES - Police Chase](https://cses.fi/problemset/task/1695)
- [CSES - School Dance](https://cses.fi/problemset/task/1696)
- [CSES - Distinct Routes](https://cses.fi/problemset/task/1711)
