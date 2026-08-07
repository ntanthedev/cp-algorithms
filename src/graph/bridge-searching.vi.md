---
title: Finding bridges in a graph in O(N+M)
tags:
  - Translated
e_maxx_link: bridge_searching
translation:
  source: graph/bridge-searching.md
  source_commit: c2d8f0ce6ec86a5f646add2cfed996c7effa4013
  status: draft
  last_synced: 2026-08-07
---
# Tìm cạnh cầu trong đồ thị trong $O(N+M)$

Cho một đồ thị vô hướng. **Cạnh cầu** (bridge) là một cạnh mà khi xóa đi sẽ làm đồ thị mất liên thông (chính xác hơn là làm tăng số thành phần liên thông của đồ thị). Bài toán yêu cầu tìm tất cả các cạnh cầu trong đồ thị đã cho.

Có thể hình dung bài toán như sau: cho một bản đồ các thành phố được nối với nhau bằng đường, hãy tìm tất cả các con đường "quan trọng", tức là những con đường mà nếu bị xóa thì sẽ không còn đường đi giữa một cặp thành phố nào đó.

Thuật toán được trình bày ở đây dựa trên [tìm kiếm theo chiều sâu](depth-first-search.md) và có độ phức tạp $O(N+M)$, trong đó $N$ là số đỉnh và $M$ là số cạnh của đồ thị.

Ngoài ra còn có bài [Finding Bridges Online](bridge-searching-online.md). Khác với thuật toán offline được trình bày ở đây, thuật toán online có thể duy trì danh sách tất cả các cạnh cầu trong một đồ thị thay đổi theo thời gian (với giả thiết thay đổi duy nhất là thêm cạnh mới).

## Thuật toán

Chọn một đỉnh bất kỳ $root$ của đồ thị và chạy [tìm kiếm theo chiều sâu](depth-first-search.md) từ đó. Ta có nhận xét sau (khá dễ chứng minh):

- Giả sử trong DFS ta đang xét các cạnh đi ra từ đỉnh $v$. Cạnh hiện tại $(v, to)$ là một cạnh cầu khi và chỉ khi không có đỉnh nào trong số $to$ và các hậu duệ của nó trên cây duyệt DFS có cạnh ngược nối tới $v$ hoặc một tổ tiên của nó. Thật vậy, điều kiện này có nghĩa là không tồn tại cách nào khác để đi từ $v$ tới $to$ ngoài cạnh $(v, to)$.

Bây giờ ta cần kiểm tra nhận xét này một cách hiệu quả với mọi đỉnh. Ta sẽ sử dụng "thời điểm vào đỉnh" được tính trong quá trình tìm kiếm theo chiều sâu.

Gọi $\mathtt{tin}[v]$ là thời điểm vào đỉnh $v$. Ta xây dựng mảng $\mathtt{low}$ để lưu thời điểm vào sớm nhất của một đỉnh mà $v$ có thể đi tới bằng một cạnh xuất phát từ chính đỉnh đó hoặc từ một hậu duệ của nó trong cây DFS. Cụ thể, $\mathtt{low}[v]$ là giá trị nhỏ nhất trong $\mathtt{tin}[v]$, các thời điểm vào $\mathtt{tin}[p]$ với mỗi đỉnh $p$ được nối với $v$ bởi một cạnh ngược $(v, p)$, và các giá trị $\mathtt{low}[to]$ với mỗi đỉnh $to$ là hậu duệ trực tiếp của $v$ trong cây DFS:

$$\mathtt{low}[v] = \min \left\{ 
    \begin{array}{l}
    \mathtt{tin}[v] \\ 
    \mathtt{tin}[p]  &\text{ for all }p\text{ for which }(v, p)\text{ is a back edge} \\ 
    \mathtt{low}[to] &\text{ for all }to\text{ for which }(v, to)\text{ is a tree edge}
    \end{array}
\right\}$$

Khi đó, tồn tại một cạnh ngược từ đỉnh $v$ hoặc một hậu duệ của nó tới một tổ tiên của nó khi và chỉ khi $v$ có một đỉnh con $to$ sao cho $\mathtt{low}[to] \leq \mathtt{tin}[v]$. Nếu $\mathtt{low}[to] = \mathtt{tin}[v]$ thì cạnh ngược đi thẳng về $v$; nếu không, cạnh ngược đi tới một tổ tiên của $v$.

Do đó, cạnh hiện tại $(v, to)$ trên cây DFS là một cạnh cầu khi và chỉ khi $\mathtt{low}[to] > \mathtt{tin}[v]$.

## Cài đặt

Cài đặt cần phân biệt ba trường hợp: khi ta đi xuống theo một cạnh của cây DFS, khi gặp một cạnh ngược tới tổ tiên của đỉnh hiện tại, và khi quay về đỉnh cha. Ba trường hợp là:

- $\mathtt{visited}[to] = false$ - cạnh thuộc cây DFS;
- $\mathtt{visited}[to] = true$ && $to \neq parent$ - cạnh là cạnh ngược tới một tổ tiên;
- $to = parent$ - cạnh dẫn ngược về đỉnh cha trên cây DFS.

Để cài đặt, ta cần một hàm tìm kiếm theo chiều sâu nhận thêm đỉnh cha của đỉnh hiện tại.

Với trường hợp có nhiều cạnh song song, cần cẩn thận khi bỏ qua cạnh dẫn tới đỉnh cha. Ta có thể dùng cờ `parent_skipped` để bảo đảm chỉ bỏ qua đỉnh cha đúng một lần.

```{.cpp file=bridge_searching_offline}
void IS_BRIDGE(int v,int to); // some function to process the found bridge
int n; // number of nodes
vector<vector<int>> adj; // adjacency list of graph

vector<bool> visited;
vector<int> tin, low;
int timer;
 
void dfs(int v, int p = -1) {
    visited[v] = true;
    tin[v] = low[v] = timer++;
    bool parent_skipped = false;
    for (int to : adj[v]) {
        if (to == p && !parent_skipped) {
            parent_skipped = true;
            continue;
        }
        if (visited[to]) {
            low[v] = min(low[v], tin[to]);
        } else {
            dfs(to, v);
            low[v] = min(low[v], low[to]);
            if (low[to] > tin[v])
                IS_BRIDGE(v, to);
        }
    }
}
 
void find_bridges() {
    timer = 0;
    visited.assign(n, false);
    tin.assign(n, -1);
    low.assign(n, -1);
    for (int i = 0; i < n; ++i) {
        if (!visited[i])
            dfs(i);
    }
}
```

Hàm chính là `find_bridges`; hàm này thực hiện các bước khởi tạo cần thiết rồi bắt đầu tìm kiếm theo chiều sâu trong từng thành phần liên thông của đồ thị.

Hàm `IS_BRIDGE(a, b)` là một hàm dùng để xử lý việc cạnh $(a, b)$ là cạnh cầu, chẳng hạn như in cạnh đó ra.

Lưu ý rằng theo phần mô tả của nguồn, cài đặt này hoạt động sai nếu đồ thị có nhiều cạnh song song vì bỏ qua chúng. Tất nhiên, các cạnh song song sẽ không bao giờ thuộc đáp án, vì vậy `IS_BRIDGE` có thể kiểm tra thêm rằng cạnh cầu được báo không phải là một cạnh song song. Một cách khác là truyền vào `dfs` chỉ số của cạnh dùng để đi vào đỉnh thay vì truyền đỉnh cha (và lưu chỉ số của tất cả các đỉnh).

**Ghi chú bản dịch:** Đoạn trên của nguồn tiếng Anh có hai điểm không còn khớp với cài đặt hiện tại. Thứ nhất, code đã chỉ bỏ qua đúng một cạnh dẫn về cha nên cạnh song song còn lại vẫn được xét. Thứ hai, câu cuối nguồn viết “store the indices of all vertices”, trong khi phương án truyền chỉ số cạnh cần lưu chỉ số của các cạnh. Bản dịch giữ nội dung nguồn trong đoạn chính và nêu rõ hai điểm này ở đây; chúng đã được tách thành PR sửa upstream riêng.

## Bài tập luyện tập

- [UVA #796 "Critical Links"](http://uva.onlinejudge.org/index.php?option=com_onlinejudge&Itemid=8&page=show_problem&problem=737) [difficulty: low]
- [UVA #610 "Street Directions"](http://uva.onlinejudge.org/index.php?option=onlinejudge&page=show_problem&problem=551) [difficulty: medium]
- [Case of the Computer Network (Codeforces Round #310 Div. 1 E)](http://codeforces.com/problemset/problem/555/E) [difficulty: hard]
* [UVA 12363 - Hedge Mazes](https://uva.onlinejudge.org/index.php?option=onlinejudge&page=show_problem&problem=3785)
* [UVA 315 - Network](https://uva.onlinejudge.org/index.php?option=com_onlinejudge&Itemid=8&page=show_problem&problem=251)
* [GYM - Computer Network (J)](http://codeforces.com/gym/100114)
* [SPOJ - King Graffs Defense](http://www.spoj.com/problems/GRAFFDEF/)
* [SPOJ - Critical Edges](http://www.spoj.com/problems/EC_P/)
* [Codeforces - Break Up](http://codeforces.com/contest/700/problem/C)
* [Codeforces - Tourist Reform](http://codeforces.com/contest/732/problem/F)
* [Codeforces - Non-academic problem](https://codeforces.com/contest/1986/problem/F)