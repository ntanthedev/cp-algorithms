---
tags:
  - Translated
e_maxx_link: mst_prim
translation:
  source: graph/mst_prim.md
  source_commit: 8815a26305b5688078ec0423f4fdbcdcd222c168
  status: draft
  last_synced: 2026-08-07
---

# Cây khung nhỏ nhất - thuật toán Prim

Cho một đồ thị vô hướng có trọng số $G$ gồm $n$ đỉnh và $m$ cạnh.
Ta muốn tìm một cây khung nối tất cả các đỉnh và có tổng trọng số cạnh nhỏ nhất.
Cây khung là một tập cạnh sao cho giữa hai đỉnh bất kỳ tồn tại đúng một đường đi đơn.
Cây khung có trọng số nhỏ nhất được gọi là **cây khung nhỏ nhất** (minimum spanning tree, MST).

Trong hình bên trái là một đồ thị vô hướng có trọng số, còn hình bên phải là cây khung nhỏ nhất tương ứng.

<div style="text-align: center;">
  <img src="MST_before.png" alt="Đồ thị ngẫu nhiên">
  <img src="MST_after.png" alt="Cây khung nhỏ nhất của đồ thị">
</div>

Dễ thấy mọi cây khung đều phải chứa đúng $n-1$ cạnh.

Bài toán này xuất hiện rất tự nhiên trong nhiều tình huống.
Ví dụ, giả sử có $n$ thành phố và với mỗi cặp thành phố ta biết chi phí xây một con đường giữa chúng (hoặc biết rằng về mặt vật lý không thể xây đường giữa hai thành phố đó).
Ta cần xây các con đường sao cho có thể đi từ mọi thành phố đến mọi thành phố khác, đồng thời tổng chi phí xây dựng là nhỏ nhất.

## Thuật toán Prim

Thuật toán này ban đầu được nhà toán học người Séc Vojtěch Jarník phát hiện vào năm 1930.
Tuy nhiên, nó thường được biết đến với tên thuật toán Prim, theo tên nhà toán học người Mỹ Robert Clay Prim, người đã độc lập phát hiện lại và công bố thuật toán vào năm 1957.
Edsger Dijkstra cũng công bố thuật toán này vào năm 1959.

### Mô tả thuật toán

Ta bắt đầu với dạng đơn giản nhất của thuật toán.
Cây khung nhỏ nhất được xây dựng dần bằng cách thêm từng cạnh một.
Ban đầu cây chỉ chứa một đỉnh được chọn tùy ý.
Sau đó, chọn cạnh có trọng số nhỏ nhất đi ra từ đỉnh này và thêm nó vào cây khung.
Lúc đó cây khung đã chứa hai đỉnh.
Tiếp theo, chọn và thêm cạnh có trọng số nhỏ nhất sao cho một đầu của cạnh nằm ở một đỉnh đã được chọn (tức đã thuộc cây khung), còn đầu kia nằm ở một đỉnh chưa được chọn.
Ta tiếp tục theo cùng nguyên tắc: mỗi lần chọn cạnh nhẹ nhất nối một đỉnh đã chọn với một đỉnh chưa chọn.
Quá trình lặp lại cho đến khi cây khung chứa tất cả các đỉnh, hay tương đương là đã chọn $n - 1$ cạnh.

Cuối cùng, cây khung thu được sẽ có trọng số nhỏ nhất.
Nếu đồ thị ban đầu không liên thông thì không tồn tại cây khung, vì vậy số cạnh được chọn sẽ nhỏ hơn $n - 1$.

### Chứng minh

Giả sử đồ thị $G$ liên thông, tức đáp án tồn tại.
Ký hiệu $T$ là cây thu được từ thuật toán Prim và $S$ là một cây khung nhỏ nhất.
Hiển nhiên $T$ là một cây khung và là đồ thị con của $G$.
Ta chỉ cần chứng minh tổng trọng số của $S$ và $T$ bằng nhau.

Xét thời điểm đầu tiên thuật toán thêm vào $T$ một cạnh không thuộc $S$.
Gọi cạnh này là $e$, hai đầu của nó là $a$ và $b$, và tập các đỉnh đã được chọn là $V$ ($a \in V$ và $b \notin V$, hoặc ngược lại).

Trong cây khung nhỏ nhất $S$, hai đỉnh $a$ và $b$ được nối bởi một đường đi $P$.
Trên đường đi này tồn tại một cạnh $f$ sao cho một đầu của $f$ nằm trong $V$ còn đầu kia nằm ngoài $V$.
Vì thuật toán chọn $e$ thay vì $f$, trọng số của $f$ phải lớn hơn hoặc bằng trọng số của $e$.

Ta thêm cạnh $e$ vào cây khung nhỏ nhất $S$ rồi bỏ cạnh $f$.
Việc thêm $e$ tạo ra một chu trình, và vì $f$ cũng nằm trên chu trình duy nhất đó, sau khi bỏ $f$ đồ thị lại không có chu trình.
Đồng thời, do ta chỉ bỏ một cạnh khỏi chu trình, đồ thị kết quả vẫn liên thông.

Cây khung mới không thể có tổng trọng số lớn hơn vì trọng số của $e$ không lớn hơn trọng số của $f$; nó cũng không thể có trọng số nhỏ hơn vì $S$ vốn đã là cây khung nhỏ nhất.
Do đó, thay $f$ bằng $e$ tạo ra một cây khung nhỏ nhất khác.
Và $e$ phải có cùng trọng số với $f$.

Vì vậy, các cạnh mà thuật toán Prim chọn có thể thay thế tương ứng các cạnh của một cây khung nhỏ nhất mà không làm thay đổi tổng trọng số, nên thuật toán Prim thực sự tạo ra một cây khung nhỏ nhất.

## Cài đặt

Độ phức tạp của thuật toán phụ thuộc vào cách ta tìm cạnh nhỏ nhất tiếp theo trong số các cạnh phù hợp.
Có nhiều cách tiếp cận dẫn đến các độ phức tạp và cách cài đặt khác nhau.

### Cài đặt trực tiếp: $O(n m)$ và $O(n^2 + m \log n)$

Nếu tìm cạnh bằng cách duyệt qua toàn bộ các cạnh có thể có, ta cần $O(m)$ thời gian để tìm cạnh nhẹ nhất.
Tổng độ phức tạp khi đó là $O(n m)$.
Trong trường hợp xấu nhất, độ phức tạp là $O(n^3)$, rất chậm.

Có thể cải tiến nếu ta chỉ xét một cạnh từ mỗi đỉnh đã được chọn.
Ví dụ, có thể sắp xếp các cạnh đi ra từ mỗi đỉnh theo trọng số tăng dần và lưu con trỏ tới cạnh hợp lệ đầu tiên, tức cạnh đi tới một đỉnh chưa được chọn.
Sau khi tìm và chọn cạnh nhẹ nhất, ta cập nhật các con trỏ.
Phần này có độ phức tạp $O(n^2 + m)$; việc sắp xếp các cạnh cần thêm $O(m \log n)$, dẫn tới độ phức tạp $O(n^2 \log n)$ trong trường hợp xấu nhất.

Dưới đây ta xét hai biến thể khác nhau đôi chút, một cho đồ thị dày và một cho đồ thị thưa, đều có độ phức tạp tốt hơn.

### Đồ thị dày: $O(n^2)$

Ta nhìn bài toán theo một hướng khác:
với mỗi đỉnh chưa được chọn, lưu cạnh có trọng số nhỏ nhất nối nó tới một đỉnh đã được chọn.

Khi đó ở mỗi bước ta chỉ cần xét các cạnh nhỏ nhất này, mất $O(n)$ thời gian.

Sau khi thêm một cạnh, một số cạnh nhỏ nhất đã lưu cần được cập nhật.
Lưu ý rằng các trọng số đang lưu chỉ có thể giảm: cạnh nhỏ nhất của mỗi đỉnh chưa chọn hoặc giữ nguyên, hoặc được thay bằng cạnh nối tới đỉnh vừa mới được chọn.
Vì vậy bước này cũng có thể thực hiện trong $O(n)$.

Ta thu được một phiên bản Prim có độ phức tạp $O(n^2)$.

Cài đặt này đặc biệt thuận tiện cho bài toán cây khung nhỏ nhất Euclid:
ta có $n$ điểm trên mặt phẳng, khoảng cách giữa mọi cặp điểm là khoảng cách Euclid, và muốn tìm cây khung nhỏ nhất của đồ thị đầy đủ này.
Bài toán có thể được giải bằng thuật toán trên trong $O(n^2)$ thời gian và $O(n)$ bộ nhớ, điều mà [thuật toán Kruskal](mst_kruskal.md) không làm được theo cùng cách biểu diễn.

```cpp
int n;
vector<vector<int>> adj; // adjacency matrix of graph
const int INF = 1000000000; // weight INF means there is no edge

struct Edge {
    int w = INF, to = -1;
};

void prim() {
    int total_weight = 0;
    vector<bool> selected(n, false);
    vector<Edge> min_e(n);
    min_e[0].w = 0;

    for (int i=0; i<n; ++i) {
        int v = -1;
        for (int j = 0; j < n; ++j) {
            if (!selected[j] && (v == -1 || min_e[j].w < min_e[v].w))
                v = j;
        }

        if (min_e[v].w == INF) {
            cout << "No MST!" << endl;
            exit(0);
        }

        selected[v] = true;
        total_weight += min_e[v].w;
        if (min_e[v].to != -1)
            cout << v << " " << min_e[v].to << endl;

        for (int to = 0; to < n; ++to) {
            if (adj[v][to] < min_e[to].w)
                min_e[to] = {adj[v][to], v};
        }
    }

    cout << total_weight << endl;
}
```

Ma trận kề `adj[][]` kích thước $n \times n$ lưu trọng số các cạnh và dùng trọng số `INF` nếu không tồn tại cạnh giữa hai đỉnh.
Thuật toán dùng hai mảng: cờ `selected[]` cho biết các đỉnh đã được chọn, và mảng `min_e[]` lưu cạnh nhẹ nhất nối mỗi đỉnh chưa chọn tới một đỉnh đã chọn (gồm trọng số và đỉnh đầu kia).
Thuật toán thực hiện $n$ bước; ở mỗi bước, chọn đỉnh có cạnh nhỏ nhất rồi cập nhật `min_e[]` của tất cả các đỉnh còn lại.

### Đồ thị thưa: $O(m \log n)$

Trong thuật toán vừa mô tả, các thao tác tìm giá trị nhỏ nhất và thay đổi một số giá trị có thể được xem là các thao tác trên tập hợp.
Hai thao tác cổ điển này được nhiều cấu trúc dữ liệu hỗ trợ, ví dụ `set` trong C++ (thường được cài bằng cây đỏ-đen).

Thuật toán chính không thay đổi, nhưng giờ ta có thể tìm cạnh nhỏ nhất trong $O(\log n)$ thời gian.
Mặt khác, nếu cập nhật lại toàn bộ các con trỏ theo cách trực tiếp thì sẽ mất $O(n \log n)$ ở mỗi bước, kém hơn thuật toán trước.

Tuy nhiên, xét trên toàn bộ thuật toán, ta chỉ cần thực hiện tổng cộng $O(m)$ lần cập nhật và $O(n)$ lần tìm cạnh nhỏ nhất, nên tổng độ phức tạp là $O(m \log n)$.
Với đồ thị thưa, cách này tốt hơn biến thể phía trên, nhưng với đồ thị dày thì chậm hơn.

```cpp
const int INF = 1000000000;

struct Edge {
    int w = INF, to = -1;
    bool operator<(Edge const& other) const {
        return make_pair(w, to) < make_pair(other.w, other.to);
    }
};

int n;
vector<vector<Edge>> adj;

void prim() {
    int total_weight = 0;
    vector<Edge> min_e(n);
    min_e[0].w = 0;
    set<Edge> q;
    q.insert({0, 0});
    vector<bool> selected(n, false);
    for (int i = 0; i < n; ++i) {
        if (q.empty()) {
            cout << "No MST!" << endl;
            exit(0);
        }

        int v = q.begin()->to;
        selected[v] = true;
        total_weight += q.begin()->w;
        q.erase(q.begin());

        if (min_e[v].to != -1)
            cout << v << " " << min_e[v].to << endl;

        for (Edge e : adj[v]) {
            if (!selected[e.to] && e.w < min_e[e.to].w) {
                q.erase({min_e[e.to].w, e.to});
                min_e[e.to] = {e.w, v};
                q.insert({e.w, e.to});
            }
        }
    }

    cout << total_weight << endl;
}
```

Ở đây đồ thị được biểu diễn bằng danh sách kề `adj[]`, trong đó `adj[v]` chứa toàn bộ các cạnh của đỉnh $v$ dưới dạng cặp trọng số và đỉnh đích.
`min_e[v]` lưu cạnh có trọng số nhỏ nhất từ đỉnh $v$ tới một đỉnh đã được chọn, cũng dưới dạng cặp trọng số và đỉnh đích.
Ngoài ra, hàng đợi `q` chứa tất cả các đỉnh chưa được chọn theo thứ tự tăng dần của trọng số `min_e`.
Thuật toán thực hiện `n` bước; ở mỗi bước, nó chọn đỉnh `v` có trọng số `min_e` nhỏ nhất bằng cách lấy phần tử đầu hàng đợi, sau đó duyệt mọi cạnh đi ra từ đỉnh này và cập nhật các giá trị trong `min_e` (mỗi lần cập nhật cũng phải xóa cạnh cũ khỏi hàng đợi `q` rồi chèn cạnh mới vào).
