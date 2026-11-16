---
tags:
  - Translated
e_maxx_link: assignment_mincostflow
translation:
  source: graph/Assignment-problem-min-flow.md
  source_commit: 57768bfc3e8d6cce85229a66cdb076fb67711281
  status: draft
  last_synced: 2026-11-15
---

# Giải bài toán phân công bằng luồng chi phí nhỏ nhất

**Bài toán phân công** có hai cách phát biểu tương đương:

   - Cho ma trận vuông $A[1..N, 1..N]$, cần chọn $N$ phần tử sao cho mỗi hàng và mỗi cột có đúng một phần tử được chọn, và tổng giá trị các phần tử đó nhỏ nhất.
   - Có $N$ đơn hàng và $N$ máy. Với mỗi đơn hàng, đã biết chi phí sản xuất trên từng máy. Mỗi máy chỉ có thể thực hiện một đơn hàng. Cần phân tất cả đơn hàng cho các máy sao cho tổng chi phí nhỏ nhất.

Ở đây ta xét lời giải dựa trên thuật toán tìm [luồng chi phí nhỏ nhất (min-cost-flow)](min_cost_flow.md), giải bài toán phân công trong $\mathcal{O}(N^3)$.

## Mô tả

Ta dựng một mạng hai phía: có nguồn $S$, đích $T$, phía thứ nhất có $N$ đỉnh (tương ứng các hàng của ma trận hoặc các đơn hàng), phía thứ hai cũng có $N$ đỉnh (tương ứng các cột của ma trận hoặc các máy). Giữa mỗi đỉnh $i$ của tập thứ nhất và mỗi đỉnh $j$ của tập thứ hai, vẽ một cạnh có khả năng thông qua 1 và chi phí $A_{ij}$. Từ nguồn $S$, vẽ cạnh đến mọi đỉnh $i$ của tập thứ nhất với khả năng thông qua 1 và chi phí 0. Từ mỗi đỉnh $j$ của tập thứ hai, vẽ cạnh đến đích $T$ với khả năng thông qua 1 và chi phí 0.

Ta tìm luồng cực đại có chi phí nhỏ nhất trong mạng thu được. Giá trị luồng sẽ là $N$. Hơn nữa, với mỗi đỉnh $i$ ở phía thứ nhất có đúng một đỉnh $j$ ở phía thứ hai sao cho luồng $F_{ij}$ = 1. Đây là một tương ứng một-một giữa các đỉnh của hai phía và là lời giải bài toán (vì luồng tìm được có chi phí nhỏ nhất, tổng chi phí các cạnh được chọn là nhỏ nhất có thể, đúng với tiêu chí tối ưu).

Độ phức tạp của lời giải phụ thuộc vào thuật toán tìm luồng cực đại có chi phí nhỏ nhất. Độ phức tạp là $\mathcal{O}(N^3)$ khi dùng [Dijkstra](dijkstra.md), hoặc $\mathcal{O}(N^4)$ khi dùng [Bellman-Ford](bellman_ford.md). Lý do là luồng có giá trị $O(N)$ và mỗi lần chạy Dijkstra có thể thực hiện trong $O(N^2)$, trong khi Bellman-Ford mất $O(N^3)$.

**Ghi chú bản dịch:** Cận dùng Dijkstra cần xử lý các cạnh chi phí âm trong mạng dư, chẳng hạn bằng thế đỉnh và chi phí đã điều chỉnh không âm. Đoạn mã bên dưới dùng SPFA, nên không thể suy ra cận Dijkstra từ chính đoạn mã đó.

## Cài đặt

Cách cài đặt dưới đây khá dài và có lẽ có thể rút gọn đáng kể.
Nó sử dụng [thuật toán SPFA](bellman_ford.md) để tìm đường đi ngắn nhất.

```cpp
const int INF = 1000 * 1000 * 1000;

vector<int> assignment(vector<vector<int>> a) {
    int n = a.size();
    int m = n * 2 + 2;
    vector<vector<int>> f(m, vector<int>(m));
    int s = m - 2, t = m - 1;
    int cost = 0;
    while (true) {
        vector<int> dist(m, INF);
        vector<int> p(m);
        vector<bool> inq(m, false);
        queue<int> q;
        dist[s] = 0;
        p[s] = -1;
        q.push(s);
        while (!q.empty()) {
            int v = q.front();
            q.pop();
            inq[v] = false;
            if (v == s) {
                for (int i = 0; i < n; ++i) {
                    if (f[s][i] == 0) {
                        dist[i] = 0;
                        p[i] = s;
                        inq[i] = true;
                        q.push(i);
                    }
                }
            } else {
                if (v < n) {
                    for (int j = n; j < n + n; ++j) {
                        if (f[v][j] < 1 && dist[j] > dist[v] + a[v][j - n]) {
                            dist[j] = dist[v] + a[v][j - n];
                            p[j] = v;
                            if (!inq[j]) {
                                q.push(j);
                                inq[j] = true;
                            }
                        }
                    }
                } else {
                    for (int j = 0; j < n; ++j) {
                        if (f[v][j] < 0 && dist[j] > dist[v] - a[j][v - n]) {
                            dist[j] = dist[v] - a[j][v - n];
                            p[j] = v;
                            if (!inq[j]) {
                                q.push(j);
                                inq[j] = true;
                            }
                        }
                    }
                }
            }
        }

        int curcost = INF;
        for (int i = n; i < n + n; ++i) {
            if (f[i][t] == 0 && dist[i] < curcost) {
                curcost = dist[i];
                p[t] = i;
            }
        }
        if (curcost == INF)
            break;
        cost += curcost;
        for (int cur = t; cur != -1; cur = p[cur]) {
            int prev = p[cur];
            if (prev != -1)
                f[cur][prev] = -(f[prev][cur] = 1);
        }
    }

    vector<int> answer(n);
    for (int i = 0; i < n; ++i) {
        for (int j = 0; j < n; ++j) {
            if (f[i][j + n] == 1)
                answer[i] = j;
        }
    }
    return answer;
}
```

**Ghi chú bản dịch:** Mã dùng INF = 1000000000 và kiểu int cho khoảng cách, chi phí; cần chọn giá trị vô cực và kiểu số phù hợp với dữ liệu, kể cả các phép cộng và trừ, để tránh không relax được cạnh hoặc tràn số. Ví dụ ma trận $2 \times 2$ có mọi chi phí bằng INF khiến mã dừng mà trả về [0, 0], không phải phân công hợp lệ. Cần kiểm tra tính hợp lệ của kết quả khi dùng mã.
