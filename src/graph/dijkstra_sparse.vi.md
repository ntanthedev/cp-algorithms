---
tags:
  - Translated
e_maxx_link: dijkstra_sparse
translation:
  source: graph/dijkstra_sparse.md
  source_commit: 258498f0e767b9edbc276e5287fb10dc3580ec0f
  status: draft
  last_synced: 2026-08-07
---

# Dijkstra trên đồ thị thưa

Phát biểu bài toán, thuật toán, phần cài đặt cơ bản và chứng minh có thể xem trong bài [Thuật toán Dijkstra](dijkstra.md).

## Thuật toán

Nhắc lại rằng khi phân tích độ phức tạp của thuật toán Dijkstra, ta xét hai thành phần:
thời gian tìm đỉnh chưa được đánh dấu có khoảng cách $d[v]$ nhỏ nhất, và thời gian thực hiện phép nới lỏng, tức là thời gian thay đổi giá trị $d[\text{to}]$.

Trong cài đặt đơn giản nhất, hai thao tác này lần lượt cần $O(n)$ và $O(1)$ thời gian.
Do thao tác thứ nhất được thực hiện $O(n)$ lần còn thao tác thứ hai được thực hiện $O(m)$ lần, ta thu được độ phức tạp $O(n^2 + m)$.

Rõ ràng độ phức tạp này tối ưu cho đồ thị dày, tức là khi $m \approx n^2$.
Tuy nhiên với đồ thị thưa, khi $m$ nhỏ hơn nhiều so với số cạnh tối đa $n^2$, thành phần đầu tiên khiến độ phức tạp trở nên kém tối ưu.
Vì vậy, ta cần giảm thời gian của thao tác tìm đỉnh nhỏ nhất, nhưng không được làm tăng đáng kể chi phí của phép nới lỏng.

Để làm điều đó, có thể dùng nhiều cấu trúc dữ liệu phụ khác nhau.
Về lý thuyết, hiệu quả nhất là **heap Fibonacci** (Fibonacci heap): thao tác lấy phần tử nhỏ nhất chạy trong $O(\log n)$, còn cập nhật một phần tử chạy trong $O(1)$.
Khi đó thuật toán Dijkstra đạt độ phức tạp $O(n \log n + m)$, cũng là cận tối ưu lý thuyết cho bài toán tìm đường đi ngắn nhất trong mô hình này.
Do đó, heap Fibonacci là một cấu trúc dữ liệu tối ưu cho cách tiếp cận này.
Không tồn tại cấu trúc dữ liệu có thể thực hiện đồng thời cả hai thao tác trên trong $O(1)$, vì nếu có thì ta cũng có thể sắp xếp một dãy số tùy ý trong thời gian tuyến tính, điều này là không thể.
Điều thú vị là có một thuật toán của Thorup tìm đường đi ngắn nhất trong $O(m)$, nhưng thuật toán đó chỉ áp dụng cho trọng số nguyên và sử dụng một ý tưởng hoàn toàn khác.
Vì vậy không có mâu thuẫn nào ở đây.
Heap Fibonacci đạt độ phức tạp tối ưu cho nhiệm vụ này, nhưng khá phức tạp để cài đặt và có hằng số ẩn tương đối lớn.

Một phương án thực tế hơn là dùng cấu trúc dữ liệu mà cả thao tác lấy phần tử nhỏ nhất và cập nhật một phần tử đều chạy trong $O(\log n)$.
Khi đó độ phức tạp của Dijkstra là $O(n \log n + m \log n) = O(m \log n)$.

C++ cung cấp hai cấu trúc phù hợp là `set` và `priority_queue`.
`set` thường được cài bằng cây đỏ-đen, còn `priority_queue` dựa trên heap.
Vì vậy `priority_queue` có hằng số ẩn nhỏ hơn, nhưng cũng có một nhược điểm:
nó không hỗ trợ thao tác xóa một phần tử tùy ý.
Do đó ta cần dùng một cách xử lý thay thế, dẫn đến hệ số $\log m$ hơi kém hơn $\log n$ (mặc dù xét theo độ phức tạp tiệm cận thì chúng tương đương).

## Cài đặt

### set

Trước hết xét container `set`.
Vì cần lưu các đỉnh theo thứ tự của giá trị $d[]$, cách thuận tiện là lưu các cặp gồm khoảng cách và chỉ số đỉnh.
Khi đó các cặp trong `set` tự động được sắp theo khoảng cách.

```{.cpp file=dijkstra_sparse_set}
const int INF = 1000000000;
vector<vector<pair<int, int>>> adj;

void dijkstra(int s, vector<int> & d, vector<int> & p) {
    int n = adj.size();
    d.assign(n, INF);
    p.assign(n, -1);

    d[s] = 0;
    set<pair<int, int>> q;
    q.insert({0, s});
    while (!q.empty()) {
        int v = q.begin()->second;
        q.erase(q.begin());

        for (auto edge : adj[v]) {
            int to = edge.first;
            int len = edge.second;
            
            if (d[v] + len < d[to]) {
                q.erase({d[to], to});
                d[to] = d[v] + len;
                p[to] = v;
                q.insert({d[to], to});
            }
        }
    }
}
```

Ta không còn cần mảng $u[]$ như trong cài đặt Dijkstra thông thường.
`set` vừa lưu thông tin cần thiết thay cho mảng đó, vừa giúp tìm đỉnh có khoảng cách nhỏ nhất.
Có thể xem nó hoạt động gần giống một hàng đợi ưu tiên.
Vòng lặp chính chạy cho đến khi tập/hàng đợi không còn đỉnh nào.
Mỗi lần ta lấy ra đỉnh có khoảng cách nhỏ nhất; với mỗi phép nới lỏng thành công, trước tiên xóa cặp cũ, sau đó nới lỏng rồi chèn cặp mới trở lại cấu trúc dữ liệu.

### priority_queue

Khác biệt chính so với cài đặt bằng `set` là trong nhiều ngôn ngữ, bao gồm C++, ta không thể xóa một phần tử tùy ý khỏi `priority_queue` (dù về lý thuyết heap có thể hỗ trợ thao tác đó).
Vì vậy ta dùng một cách xử lý khác:
không xóa cặp cũ khỏi hàng đợi.
Kết quả là cùng một đỉnh có thể xuất hiện nhiều lần trong hàng đợi với các khoảng cách khác nhau.
Trong số các cặp đó, ta chỉ quan tâm tới cặp mà phần tử thứ nhất bằng giá trị hiện tại tương ứng trong $d[]$; các cặp còn lại đã lỗi thời.
Do đó cần một thay đổi nhỏ:
ở đầu mỗi vòng lặp, sau khi lấy cặp tiếp theo ra, ta kiểm tra cặp đó còn hợp lệ hay đã là dữ liệu cũ được xử lý trước đó.
Kiểm tra này rất quan trọng; nếu bỏ qua, độ phức tạp có thể tăng tới $O(n m)$.

Mặc định, `priority_queue` sắp xếp các phần tử theo thứ tự giảm dần.
Để sắp tăng dần, ta có thể lưu khoảng cách với dấu âm hoặc truyền vào một hàm so sánh khác.
Ở đây ta dùng cách thứ hai.

```{.cpp file=dijkstra_sparse_pq}
const int INF = 1000000000;
vector<vector<pair<int, int>>> adj;

void dijkstra(int s, vector<int> & d, vector<int> & p) {
    int n = adj.size();
    d.assign(n, INF);
    p.assign(n, -1);

    d[s] = 0;
    using pii = pair<int, int>;
    priority_queue<pii, vector<pii>, greater<pii>> q;
    q.push({0, s});
    while (!q.empty()) {
        int v = q.top().second;
        int d_v = q.top().first;
        q.pop();
        if (d_v != d[v])
            continue;

        for (auto edge : adj[v]) {
            int to = edge.first;
            int len = edge.second;
            
            if (d[v] + len < d[to]) {
                d[to] = d[v] + len;
                p[to] = v;
                q.push({d[to], to});
            }
        }
    }
}
```

Trong thực tế, phiên bản `priority_queue` thường nhanh hơn một chút so với phiên bản dùng `set`.

Đáng chú ý, một [báo cáo kỹ thuật năm 2007](https://www3.cs.stonybrook.edu/~rezaul/papers/TR-07-54.pdf) kết luận rằng biến thể không dùng thao tác decrease-key chạy nhanh hơn biến thể có decrease-key, và khoảng cách hiệu năng càng rõ trên đồ thị thưa.

### Loại bỏ các cặp

Có thể cải thiện hiệu năng thêm một chút nếu không lưu các cặp trong container mà chỉ lưu chỉ số đỉnh.
Khi đó ta phải nạp chồng toán tử so sánh:
nó cần so sánh hai đỉnh dựa trên khoảng cách lưu trong $d[]$.

Sau một phép nới lỏng, khoảng cách của một số đỉnh sẽ thay đổi.
Tuy nhiên cấu trúc dữ liệu không tự động sắp xếp lại theo các giá trị mới.
Thực tế, thay đổi khoảng cách của một đỉnh khi nó vẫn còn trong hàng đợi có thể phá vỡ tính đúng đắn của cấu trúc dữ liệu.
Như trước, ta cần xóa đỉnh trước khi nới lỏng rồi chèn lại sau đó.

Vì chỉ `set` hỗ trợ xóa theo cách cần thiết, tối ưu này chỉ áp dụng được cho phương án dùng `set`, không áp dụng được cho cài đặt `priority_queue`.
Trong thực tế, cách này có thể cải thiện hiệu năng đáng kể, đặc biệt khi khoảng cách dùng kiểu dữ liệu lớn hơn như `long long` hoặc `double`.
