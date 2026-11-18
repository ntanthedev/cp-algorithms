---
tags:
  - Translated
e_maxx_link: preflow_push
translation:
  source: graph/push-relabel.md
  source_commit: 569a1198a96eee70b1a0f41516259491c06ac819
  status: draft
  last_synced: 2026-11-16
---

# Luồng cực đại - Thuật toán đẩy và gán lại nhãn

Thuật toán đẩy và gán lại nhãn (còn gọi là thuật toán đẩy tiền luồng) dùng để tính luồng cực đại của một mạng luồng. Định nghĩa chính xác của bài toán nằm trong bài [Luồng cực đại - Ford-Fulkerson và Edmonds-Karp](edmonds_karp.md).

Trong bài này ta xét cách giải bằng cách đẩy một tiền luồng qua mạng, với thời gian $O(V^4)$, hay chính xác hơn là $O(V^2 E)$. Thuật toán do Andrew Goldberg và Robert Tarjan thiết kế năm 1985.

## Định nghĩa

Trong thuật toán, ta cần xử lý một **tiền luồng**, tức là một hàm $f$ tương tự hàm luồng nhưng không nhất thiết thỏa mãn ràng buộc bảo toàn luồng. Nó chỉ cần thỏa mãn các ràng buộc

$$0 \le f(e) \le c(e)$$

và

$$\sum_{(v, u) \in E} f((v, u)) \ge \sum_{(u, v) \in E} f((u, v))$$

**Ghi chú bản dịch:** Bất đẳng thức trên nói tổng luồng đi vào không nhỏ hơn tổng luồng đi ra, phù hợp với định nghĩa lượng dư ngay dưới đây. Điều kiện này áp dụng cho các đỉnh khác nguồn; tại nguồn không cần thỏa điều kiện đó.

Do đó một đỉnh có thể nhận nhiều luồng hơn lượng nó phân phối đi. Ta nói đỉnh đó có luồng dư và định nghĩa lượng dư bằng hàm **lượng dư** $x(u) =\sum_{(v, u) \in E} f((v, u)) - \sum_{(u, v) \in E} f((u, v))$.

Tương tự với hàm luồng, từ hàm tiền luồng ta có thể định nghĩa dung lượng thặng dư và mạng thặng dư.

Thuật toán bắt đầu với một tiền luồng ban đầu (một số đỉnh có lượng dư), rồi xử lý và thay đổi tiền luồng trong quá trình chạy. Nói trước một phần chi tiết, thuật toán chọn một đỉnh có lượng dư và đẩy lượng dư đó sang các đỉnh kề. Quá trình lặp lại cho đến khi mọi đỉnh, ngoại trừ nguồn và đích, đều không còn lượng dư. Dễ thấy một tiền luồng không có lượng dư là một luồng hợp lệ. Nhờ vậy thuật toán kết thúc với một luồng thực sự.

Vẫn còn hai vấn đề cần giải quyết. Thứ nhất, làm sao bảo đảm quá trình thực sự kết thúc? Thứ hai, làm sao bảo đảm kết quả là luồng cực đại chứ không phải một luồng bất kỳ?

Để giải quyết, ta dùng một hàm khác là hàm **gán nhãn** $h$, thường còn gọi là hàm **độ cao**, gán cho mỗi đỉnh một số nguyên. Một cách gán nhãn được gọi là hợp lệ nếu $h(s) = |V|$, $h(t) = 0$, và $h(u) \le h(v) + 1$ nếu có cạnh $(u, v)$ trong mạng thặng dư, tức là cạnh $(u, v)$ có dung lượng dương trong mạng thặng dư. Nói cách khác, nếu có thể tăng luồng từ $u$ đến $v$, độ cao của $v$ có thể nhỏ hơn độ cao của $u$ nhiều nhất một đơn vị, nhưng cũng có thể bằng hoặc lớn hơn.

Nếu tồn tại một hàm gán nhãn hợp lệ thì không tồn tại đường tăng luồng từ $s$ đến $t$ trong mạng thặng dư. Thật vậy, một đường như thế có nhiều nhất $|V| - 1$ cạnh và qua mỗi cạnh độ cao giảm nhiều nhất một đơn vị. Điều này là không thể khi độ cao đầu là $h(s) = |V|$ và độ cao cuối là $h(t) = 0$.

Dùng hàm gán nhãn này, ta có thể nêu chiến lược của thuật toán đẩy và gán lại nhãn. Ta bắt đầu với một tiền luồng và một hàm gán nhãn hợp lệ. Ở mỗi bước, ta đẩy một phần lượng dư giữa các đỉnh và cập nhật nhãn các đỉnh. Ta phải bảo đảm tiền luồng và nhãn vẫn hợp lệ sau mỗi bước. Khi thuật toán kết thúc, tiền luồng là một luồng hợp lệ. Vì nhãn cũng hợp lệ, không có đường đi từ $s$ đến $t$ trong mạng thặng dư, do đó luồng thu được là luồng cực đại.

Nếu so sánh Ford-Fulkerson với thuật toán đẩy và gán lại nhãn, ta thấy chúng có vẻ đối ngẫu với nhau. Ford-Fulkerson luôn giữ một luồng hợp lệ và cải thiện nó cho đến khi không còn đường tăng luồng; còn thuật toán đẩy và gán lại nhãn luôn không có đường tăng luồng và cải thiện tiền luồng cho đến khi nó là một luồng hợp lệ.

## Thuật toán

Trước tiên, ta khởi tạo đồ thị với tiền luồng và cách gán nhãn hợp lệ.

Không thể dùng tiền luồng rỗng như trong Ford-Fulkerson, vì khi đó sẽ có đường tăng luồng, kéo theo không tồn tại cách gán nhãn hợp lệ. Vì vậy, ta khởi tạo mỗi cạnh đi ra từ $s$ với dung lượng cực đại của nó: $f((s, u)) = c((s, u))$. Mọi cạnh khác có luồng bằng không. Khi đó có cách gán nhãn hợp lệ: $h(s) = |V|$ cho đỉnh nguồn và $h(u) = 0$ cho các đỉnh còn lại.

Giờ ta mô tả chi tiết hai phép toán.

Với phép `push`, ta cố gắng đẩy càng nhiều luồng dư càng tốt từ một đỉnh $u$ đến một đỉnh kề $v$. Có một quy tắc: chỉ được đẩy luồng từ $u$ đến $v$ nếu $h(u) = h(v) + 1$. Nói dễ hiểu, luồng dư phải chảy xuống nhưng không quá dốc. Dĩ nhiên, ta chỉ có thể đẩy lượng luồng $\min(x(u), c((u, v)) - f((u, v)))$.

Nếu một đỉnh có lượng dư nhưng không thể đẩy lượng dư sang bất kỳ đỉnh kề nào, ta cần tăng độ cao của nó. Ta gọi phép này là `relabel`. Ta tăng độ cao nhiều nhất có thể trong khi vẫn giữ cách gán nhãn hợp lệ.

Tóm lại, thuật toán gồm các bước: khởi tạo một tiền luồng và một cách gán nhãn hợp lệ. Khi còn có thể thực hiện phép đẩy hoặc gán lại nhãn, ta thực hiện chúng. Sau đó tiền luồng thực sự là một luồng và ta trả về nó.

## Độ phức tạp

Dễ chứng minh nhãn lớn nhất của một đỉnh là $2|V| - 1$. Khi đó mọi lượng dư còn lại có thể và sẽ được đẩy trở lại nguồn. Suy ra có nhiều nhất $O(V^2)$ phép gán lại nhãn.

Cũng có thể chứng minh có nhiều nhất $O(V E)$ lần đẩy bão hòa (lần đẩy dùng hết dung lượng cạnh) và nhiều nhất $O(V^2 E)$ lần đẩy không bão hòa (lần đẩy không dùng hết dung lượng cạnh). Nếu chọn một cấu trúc dữ liệu cho phép tìm đỉnh có lượng dư tiếp theo trong $O(1)$ thời gian, tổng độ phức tạp của thuật toán là $O(V^2 E)$.

## Cài đặt

**Ghi chú bản dịch:** Mã nguồn khởi tạo lượng dư tại nguồn bằng giá trị $10^9$, nên giới hạn này có thể làm kết quả nhỏ hơn luồng cực đại. Ví dụ, với mạng chỉ gồm một cạnh từ nguồn đến đích có dung lượng $1.5 \cdot 10^9$, mã chỉ trả về $10^9$.

```{.cpp file=push_relabel}
const int inf = 1000000000;

int n;
vector<vector<int>> capacity, flow;
vector<int> height, excess, seen;
queue<int> excess_vertices;

void push(int u, int v) {
    int d = min(excess[u], capacity[u][v] - flow[u][v]);
    flow[u][v] += d;
    flow[v][u] -= d;
    excess[u] -= d;
    excess[v] += d;
    if (d && excess[v] == d)
        excess_vertices.push(v);
}

void relabel(int u) {
    int d = inf;
    for (int i = 0; i < n; i++) {
        if (capacity[u][i] - flow[u][i] > 0)
            d = min(d, height[i]);
    }
    if (d < inf)
        height[u] = d + 1;
}

void discharge(int u) {
    while (excess[u] > 0) {
        if (seen[u] < n) {
            int v = seen[u];
            if (capacity[u][v] - flow[u][v] > 0 && height[u] > height[v])
                push(u, v);
            else 
                seen[u]++;
        } else {
            relabel(u);
            seen[u] = 0;
        }
    }
}

int max_flow(int s, int t) {
    height.assign(n, 0);
    height[s] = n;
    flow.assign(n, vector<int>(n, 0));
    excess.assign(n, 0);
    excess[s] = inf;
    for (int i = 0; i < n; i++) {
    	if (i != s)
	        push(s, i);
    }
    seen.assign(n, 0);

    while (!excess_vertices.empty()) {
        int u = excess_vertices.front();
        excess_vertices.pop();
        if (u != s && u != t)
            discharge(u);
    }

    int max_flow = 0;
    for (int i = 0; i < n; i++)
        max_flow += flow[i][t];
    return max_flow;
}
```

Ở đây ta dùng hàng đợi `excess_vertices` để lưu mọi đỉnh hiện có lượng dư. Nhờ đó ta có thể chọn đỉnh tiếp theo để thực hiện phép đẩy hoặc gán lại nhãn trong thời gian hằng số.

Để tránh mất quá nhiều thời gian tìm đỉnh kề mà ta có thể đẩy luồng tới, ta dùng một cấu trúc dữ liệu gọi là **cung hiện tại**. Về cơ bản, ta duyệt các cạnh theo thứ tự vòng tròn và luôn lưu cạnh cuối cùng đã dùng. Bằng cách này, với một giá trị nhãn cố định, ta chỉ đổi cạnh hiện tại $O(n)$ lần. Vì việc gán lại nhãn vốn mất $O(n)$ thời gian, độ phức tạp không tăng lên.
