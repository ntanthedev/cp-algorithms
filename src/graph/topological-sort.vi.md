---
tags:
  - Translated
e_maxx_link: topological_sort
translation:
  source: graph/topological-sort.md
  source_commit: c522039bc0fe119fea700c2add2966008415c7f1
  status: draft
  last_synced: 2026-08-07
---

# Sắp xếp tô-pô

Cho một đồ thị có hướng gồm $n$ đỉnh và $m$ cạnh.
Ta cần tìm một **thứ tự của các đỉnh** sao cho mỗi cạnh đều đi từ đỉnh có chỉ số nhỏ hơn đến đỉnh có chỉ số lớn hơn.

Nói cách khác, ta cần tìm một hoán vị của các đỉnh, gọi là **thứ tự tô-pô** (topological order), phù hợp với quan hệ thứ tự do mọi cạnh của đồ thị xác định.

Dưới đây là một đồ thị cùng một thứ tự tô-pô của nó:

<div style="text-align: center;">
  <img src="topological_1.png" alt="ví dụ về đồ thị có hướng">
  <img src="topological_2.png" alt="một thứ tự tô-pô">
</div>

Thứ tự tô-pô có thể **không duy nhất**. Chẳng hạn, giả sử có ba đỉnh $a$, $b$, $c$ sao cho tồn tại đường đi từ $a$ đến $b$ và từ $a$ đến $c$, nhưng không có đường đi từ $b$ đến $c$ hoặc từ $c$ đến $b$.
Đồ thị trong ví dụ cũng có nhiều thứ tự tô-pô; một thứ tự khác được minh họa dưới đây:
<div style="text-align: center;">
  <img src="topological_3.png" alt="thứ tự tô-pô thứ hai">
</div>

Thứ tự tô-pô cũng có thể **không tồn tại**.
Nó chỉ tồn tại khi đồ thị có hướng không chứa chu trình.
Nếu có chu trình chứa hai đỉnh $a$ và $b$, ta gặp mâu thuẫn: $a$ phải có chỉ số nhỏ hơn $b$ vì có thể đi từ $a$ đến $b$, nhưng đồng thời $a$ cũng phải có chỉ số lớn hơn $b$ vì có thể đi từ $b$ đến $a$.
Bằng cách xây dựng, thuật toán trong bài này cũng chứng minh rằng mọi đồ thị có hướng không chu trình đều có ít nhất một thứ tự tô-pô.

Một bài toán phổ biến sử dụng sắp xếp tô-pô có dạng sau. Có $n$ biến chưa biết giá trị. Với một số cặp biến, ta biết biến này nhỏ hơn biến kia. Ta cần kiểm tra các ràng buộc có mâu thuẫn hay không; nếu không, hãy xuất các biến theo thứ tự tăng dần, và có thể xuất bất kỳ đáp án nào nếu tồn tại nhiều đáp án. Dễ thấy đây chính là bài toán tìm thứ tự tô-pô của một đồ thị gồm $n$ đỉnh.

## Thuật toán

Để giải bài toán, ta sử dụng [tìm kiếm theo chiều sâu](depth-first-search.md).

Giả sử đồ thị không có chu trình. Khi đó, tìm kiếm theo chiều sâu hoạt động như thế nào?

Khi bắt đầu từ một đỉnh $v$, DFS cố gắng duyệt theo mọi cạnh đi ra từ $v$.
Thuật toán dừng tại những cạnh có đỉnh cuối đã được thăm trước đó, còn với các cạnh khác, nó đi theo cạnh và tiếp tục đệ quy tại đỉnh cuối.

Vì vậy, khi lời gọi hàm $\text{dfs}(v)$ kết thúc, DFS đã thăm mọi đỉnh có thể đi tới từ $v$, trực tiếp qua một cạnh hoặc gián tiếp qua nhiều cạnh.

Ta thêm đỉnh $v$ vào một danh sách khi hoàn tất $\text{dfs}(v)$. Vì mọi đỉnh có thể đi tới từ $v$ đều đã được thăm, chúng đã nằm trong danh sách trước khi ta thêm $v$.
Thực hiện điều này với mọi đỉnh của đồ thị bằng một hoặc nhiều lần chạy DFS.
Với mỗi cạnh có hướng $v \rightarrow u$, đỉnh $u$ sẽ xuất hiện trong danh sách trước $v$, vì có thể đi từ $v$ đến $u$.
Do đó, nếu gán nhãn cho các đỉnh trong danh sách lần lượt là $n-1, n-2, \dots, 1, 0$, ta thu được một thứ tự tô-pô.
Nói cách khác, danh sách này biểu diễn thứ tự tô-pô theo chiều ngược lại.

Ta cũng có thể diễn giải lập luận trên bằng thời điểm ra của DFS.
Thời điểm ra của đỉnh $v$ là thời điểm lời gọi $\text{dfs}(v)$ kết thúc; các thời điểm có thể được đánh số từ $0$ đến $n-1$.
Thời điểm ra của một đỉnh $v$ luôn lớn hơn thời điểm ra của mọi đỉnh có thể đi tới từ nó, vì các đỉnh đó đã được thăm trước hoặc trong khi thực hiện $\text{dfs}(v)$. Do đó, thứ tự tô-pô cần tìm là thứ tự các đỉnh theo thời điểm ra giảm dần.

## Cài đặt

Cách cài đặt dưới đây giả sử đồ thị không có chu trình, tức thứ tự tô-pô cần tìm tồn tại. Khi cần, ta có thể dễ dàng kiểm tra đồ thị có chu trình hay không theo phương pháp trong bài [tìm kiếm theo chiều sâu](depth-first-search.md).

```cpp
int n; // number of vertices
vector<vector<int>> adj; // adjacency list of graph
vector<bool> visited;
vector<int> ans;

void dfs(int v) {
    visited[v] = true;
    for (int u : adj[v]) {
        if (!visited[u]) {
            dfs(u);
        }
    }
    ans.push_back(v);
}

void topological_sort() {
    visited.assign(n, false);
    ans.clear();
    for (int i = 0; i < n; ++i) {
        if (!visited[i]) {
            dfs(i);
        }
    }
    reverse(ans.begin(), ans.end());
}
```

Hàm chính của lời giải là `topological_sort`. Hàm này khởi tạo các biến của DFS, chạy DFS và lưu đáp án trong vector `ans`. Đáng chú ý, nếu đồ thị có chu trình, kết quả của `topological_sort` vẫn có một tính chất hữu ích: nếu có thể đi từ đỉnh $v$ đến đỉnh $u$ nhưng không thể đi ngược lại, thì $v$ luôn đứng trước $u$ trong mảng kết quả. Tính chất này được sử dụng trong [thuật toán Kosaraju](./strongly-connected-components.md) để tìm các thành phần liên thông mạnh và thứ tự tô-pô của chúng trong một đồ thị có hướng chứa chu trình.

## Bài tập luyện tập

- [SPOJ TOPOSORT - Topological Sorting [difficulty: easy]](http://www.spoj.com/problems/TOPOSORT/)
- [UVA 10305 - Ordering Tasks [difficulty: easy]](https://onlinejudge.org/index.php?option=com_onlinejudge&Itemid=8&page=show_problem&problem=1246)
- [UVA 124 - Following Orders [difficulty: easy]](https://onlinejudge.org/index.php?option=onlinejudge&page=show_problem&problem=60)
- [UVA 200 - Rare Order [difficulty: easy]](https://onlinejudge.org/index.php?option=onlinejudge&page=show_problem&problem=136)
- [Codeforces 510C - Fox and Names [difficulty: easy]](http://codeforces.com/problemset/problem/510/C)
- [SPOJ RPLA - Answer the boss!](https://www.spoj.com/problems/RPLA/)
- [CSES - Course Schedule](https://cses.fi/problemset/task/1679)
- [CSES - Longest Flight Route](https://cses.fi/problemset/task/1680)
- [CSES - Game Routes](https://cses.fi/problemset/task/1681)
