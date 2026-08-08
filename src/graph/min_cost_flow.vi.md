---
tags:
  - Translated
e_maxx_link: min_cost_flow
translation:
  source: graph/min_cost_flow.md
  source_commit: b13716d40db706b1c30cc5c457ca953612b237e8
  status: draft
  last_synced: 2026-08-07
---

# Luồng với chi phí cực tiểu - Thuật toán đường đi ngắn nhất liên tiếp

Cho một mạng $G$ gồm $n$ đỉnh và $m$ cạnh.
Với mỗi cạnh (nói chung là cạnh có hướng, nhưng xem thêm bên dưới), ta biết dung lượng (một số nguyên không âm) và chi phí cho mỗi đơn vị luồng đi qua cạnh đó (một số nguyên bất kỳ).
Ngoài ra, nguồn $s$ và đích $t$ cũng được đánh dấu.

Với một giá trị $K$ cho trước, ta cần tìm một luồng có lượng đúng bằng giá trị này và, trong tất cả các luồng như vậy, chọn luồng có tổng chi phí nhỏ nhất.
Bài toán này được gọi là **bài toán luồng với chi phí cực tiểu** (minimum-cost flow).

Đôi khi bài toán được phát biểu hơi khác:
ta muốn tìm luồng cực đại và, trong tất cả các luồng cực đại, tìm luồng có chi phí nhỏ nhất.
Bài toán này được gọi là **bài toán luồng cực đại với chi phí cực tiểu** (minimum-cost maximum-flow).

Cả hai bài toán đều có thể được giải hiệu quả bằng thuật toán đường đi ngắn nhất liên tiếp (successive shortest paths).

## Thuật toán

Thuật toán này rất giống [Edmonds-Karp](edmonds_karp.md) dùng để tính luồng cực đại.

### Trường hợp đơn giản nhất

Trước hết, ta chỉ xét trường hợp đơn giản nhất: đồ thị có hướng và giữa mỗi cặp đỉnh có nhiều nhất một cạnh (ví dụ, nếu $(i, j)$ là một cạnh của đồ thị thì $(j, i)$ không thể đồng thời thuộc đồ thị).

Gọi $U_{i j}$ là dung lượng của cạnh $(i, j)$ nếu cạnh này tồn tại.
Gọi $C_{i j}$ là chi phí cho mỗi đơn vị luồng đi qua cạnh $(i, j)$.
Cuối cùng, gọi $F_{i, j}$ là luồng trên cạnh $(i, j)$.
Ban đầu, mọi giá trị luồng đều bằng 0.

Ta **biến đổi** mạng như sau:
với mỗi cạnh $(i, j)$, thêm **cạnh ngược** $(j, i)$ vào mạng với dung lượng $U_{j i} = 0$ và chi phí $C_{j i} = -C_{i j}$.
Theo giả thiết ở trên, cạnh $(j, i)$ chưa có trong mạng trước đó, nên mạng sau khi biến đổi vẫn không phải đa đồ thị (đồ thị có nhiều cạnh giữa cùng một cặp đỉnh).
Ngoài ra, trong suốt thuật toán ta luôn duy trì điều kiện $F_{j i} = -F_{i j}$.

Ta định nghĩa **mạng thặng dư** ứng với một luồng cố định $F$ như sau (tương tự thuật toán Ford-Fulkerson):
mạng thặng dư chỉ chứa các cạnh chưa bão hòa (tức các cạnh thỏa mãn $F_{i j} < U_{i j}$), và dung lượng thặng dư của mỗi cạnh như vậy là $R_{i j} = U_{i j} - F_{i j}$.

Bây giờ ta có thể mô tả **thuật toán** tính luồng với chi phí cực tiểu.
Ở mỗi lần lặp, ta tìm đường đi ngắn nhất trong đồ thị thặng dư từ $s$ tới $t$.
Khác với Edmonds-Karp, ở đây độ dài đường đi được tính theo chi phí của đường thay vì số cạnh.
Nếu không còn đường đi nào, thuật toán kết thúc; nguồn tiếng Anh gọi luồng $F$ hiện tại là luồng mong muốn.
Nếu tìm được một đường, ta tăng luồng trên đường đó nhiều nhất có thể (tức tìm dung lượng thặng dư nhỏ nhất $R$ trên đường, tăng luồng thêm lượng đó và giảm luồng trên các cạnh ngược cùng một lượng).
Nếu tại một thời điểm luồng đạt giá trị $K$, ta dừng thuật toán (lưu ý rằng ở lần lặp cuối, chỉ được tăng một lượng vừa đủ để giá trị luồng cuối cùng không vượt quá $K$).

**Ghi chú bản dịch:** Phát biểu “luồng hiện tại là luồng mong muốn” khi không còn đường đi chỉ đúng nếu lượng luồng yêu cầu đã đạt được. Với phiên bản yêu cầu một lượng K cố định, nếu hết đường trước khi đạt K thì không tồn tại luồng khả thi có lượng K; implementation phía dưới cũng xử lý trường hợp này bằng cách trả về -1. Lỗi wording này được tách riêng để đề xuất sửa upstream.

Không khó để thấy rằng nếu đặt $K$ bằng vô hạn thì thuật toán sẽ tìm luồng cực đại với chi phí cực tiểu.
Vì vậy, cả hai biến thể của bài toán đều có thể giải bằng cùng một thuật toán.

### Đồ thị vô hướng / đa đồ thị

Trường hợp đồ thị vô hướng hoặc đa đồ thị không khác về mặt ý tưởng so với thuật toán trên.
Thuật toán vẫn hoạt động trên các đồ thị này.
Tuy nhiên, việc cài đặt trở nên phức tạp hơn một chút.

Một **cạnh vô hướng** $(i, j)$ thực chất tương đương với hai cạnh có hướng $(i, j)$ và $(j, i)$ có cùng dung lượng và chi phí.

**Ghi chú bản dịch:** Nguồn tiếng Anh viết “same capacity and values”. Trong ngữ cảnh này, thuộc tính thứ hai đã được định nghĩa là chi phí trên mỗi đơn vị luồng; bản dịch dùng “chi phí” để tránh mơ hồ và correction tương ứng được bổ sung vào PR upstream riêng.

Vì thuật toán luồng với chi phí cực tiểu ở trên sinh một cạnh ngược cho mỗi cạnh có hướng, nên một cạnh vô hướng được tách thành $4$ cạnh có hướng và ta thực sự thu được một **đa đồ thị**.

Ta xử lý **nhiều cạnh** như thế nào?
Thứ nhất, luồng trên từng cạnh trong số các cạnh song song phải được lưu riêng.
Thứ hai, khi tìm đường đi ngắn nhất, ta cần biết chính xác cạnh nào trong số các cạnh song song được dùng trên đường.
Vì vậy, thay vì chỉ lưu mảng đỉnh trước thông thường, ta còn phải lưu số hiệu cạnh đã dùng để đi tới cùng với đỉnh trước.
Thứ ba, khi luồng trên một cạnh cụ thể tăng lên, ta phải giảm luồng trên cạnh ngược tương ứng.
Do có nhiều cạnh, với mỗi cạnh ta cần lưu số hiệu của cạnh ngược của nó.

Ngoài các điểm trên, không có trở ngại nào khác đối với đồ thị vô hướng hoặc đa đồ thị.

### Độ phức tạp

Thuật toán được trình bày ở đây nói chung có độ phức tạp hàm mũ theo kích thước đầu vào. Cụ thể hơn, trong trường hợp xấu nhất mỗi lần lặp có thể chỉ đẩy được $1$ đơn vị luồng, cần $O(F)$ lần lặp để tìm luồng với chi phí cực tiểu có lượng $F$, nên tổng thời gian là $O(F \cdot T)$, trong đó $T$ là thời gian cần để tìm đường đi ngắn nhất từ nguồn tới đích.

Nếu dùng thuật toán [Bellman-Ford](bellman_ford.md), thời gian chạy là $O(F mn)$. Cũng có thể sửa đổi [thuật toán Dijkstra](dijkstra.md) để cần $O(nm)$ tiền xử lý ban đầu rồi chạy trong $O(m \log n)$ cho mỗi lần lặp, cho tổng thời gian $O(mn + F m \log n)$. [Tại đây](http://web.archive.org/web/20211009144446/https://min-25.hatenablog.com/entry/2018/03/19/235802) có một bộ sinh đồ thị mà trên đó thuật toán như vậy cần $O(2^{n/2} n^2 \log n)$ thời gian.

Dijkstra đã sửa đổi sử dụng các **thế** (potentials) từ [thuật toán Johnson](https://en.wikipedia.org/wiki/Johnson%27s_algorithm). Có thể kết hợp ý tưởng của thuật toán này với Dinic để giảm số lần lặp từ $F$ xuống $\min(F, nC)$, trong đó $C$ là chi phí lớn nhất trong các cạnh. Có thể đọc thêm về thế và cách kết hợp với Dinic [tại đây](https://codeforces.com/blog/entry/105658).

## Cài đặt

Dưới đây là một cài đặt sử dụng [thuật toán SPFA](bellman_ford.md) cho trường hợp đơn giản nhất.

```{.cpp file=min_cost_flow_successive_shortest_path}
struct Edge
{
    int from, to, capacity, cost;
};

vector<vector<int>> adj, cost, capacity;

const int INF = 1e9;

void shortest_paths(int n, int v0, vector<int>& d, vector<int>& p) {
    d.assign(n, INF);
    d[v0] = 0;
    vector<bool> inq(n, false);
    queue<int> q;
    q.push(v0);
    p.assign(n, -1);

    while (!q.empty()) {
        int u = q.front();
        q.pop();
        inq[u] = false;
        for (int v : adj[u]) {
            if (capacity[u][v] > 0 && d[v] > d[u] + cost[u][v]) {
                d[v] = d[u] + cost[u][v];
                p[v] = u;
                if (!inq[v]) {
                    inq[v] = true;
                    q.push(v);
                }
            }
        }
    }
}

int min_cost_flow(int N, vector<Edge> edges, int K, int s, int t) {
    adj.assign(N, vector<int>());
    cost.assign(N, vector<int>(N, 0));
    capacity.assign(N, vector<int>(N, 0));
    for (Edge e : edges) {
        adj[e.from].push_back(e.to);
        adj[e.to].push_back(e.from);
        cost[e.from][e.to] = e.cost;
        cost[e.to][e.from] = -e.cost;
        capacity[e.from][e.to] = e.capacity;
    }

    int flow = 0;
    int cost = 0;
    vector<int> d, p;
    while (flow < K) {
        shortest_paths(N, s, d, p);
        if (d[t] == INF)
            break;
        
        // find max flow on that path
        int f = K - flow;
        int cur = t;
        while (cur != s) {
            f = min(f, capacity[p[cur]][cur]);
            cur = p[cur];
        }

        // apply flow
        flow += f;
        cost += f * d[t];
        cur = t;
        while (cur != s) {
            capacity[p[cur]][cur] -= f;
            capacity[cur][p[cur]] += f;
            cur = p[cur];
        }
    }

    if (flow < K)
        return -1;
    else
        return cost;
}
```

## Bài tập luyện tập

* [CSES - Task Assignment](https://cses.fi/problemset/task/2129)
* [CSES - Grid Puzzle II](https://cses.fi/problemset/task/2131)
* [AtCoder - Dream Team](https://atcoder.jp/contests/abc247/tasks/abc247_g)