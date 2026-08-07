---
tags:
  - Translated
e_maxx_link: 2_sat
translation:
  source: graph/2SAT.md
  source_commit: 0dcf8e07ac9e8b0c6c4cbf35d543ae054f26d6b5
  status: draft
  last_synced: 2026-08-07
---

# 2-SAT 

SAT (Boolean satisfiability problem - bài toán thỏa mãn Boolean) là bài toán gán giá trị Boolean cho các biến sao cho một công thức Boolean cho trước được thỏa mãn.
Công thức Boolean thường được cho ở dạng CNF (conjunctive normal form - dạng chuẩn hội), tức là phép hội của nhiều mệnh đề (clause), trong đó mỗi mệnh đề là phép tuyển của các literal (một biến hoặc phủ định của một biến).
2-SAT (2-satisfiability) là một trường hợp giới hạn của SAT; trong 2-SAT, mỗi mệnh đề có đúng hai literal.
Sau đây là một ví dụ về bài toán 2-SAT.
Hãy tìm cách gán $a, b, c$ sao cho công thức sau đúng:

$$(a \lor \lnot b) \land (\lnot a \lor b) \land (\lnot a \lor \lnot b) \land (a \lor \lnot c)$$

SAT là bài toán NP-complete và hiện chưa có thuật toán hiệu quả đã biết để giải trường hợp tổng quát.
Tuy nhiên, 2SAT có thể được giải hiệu quả trong $O(n + m)$, với $n$ là số biến và $m$ là số mệnh đề.

## Thuật toán:

Trước hết, ta cần chuyển bài toán sang một dạng khác gọi là dạng chuẩn kéo theo (implicative normal form).
Lưu ý rằng biểu thức $a \lor b$ tương đương với $\lnot a \Rightarrow b \land \lnot b \Rightarrow a$ (nếu một trong hai biến sai thì biến còn lại bắt buộc phải đúng).

Bây giờ ta xây dựng một đồ thị có hướng biểu diễn các phép kéo theo này:
với mỗi biến $x$ sẽ có hai đỉnh $v_x$ và $v_{\lnot x}$.
Các cạnh tương ứng với các phép kéo theo.

Xét lại ví dụ dưới dạng 2-CNF:

$$(a \lor \lnot b) \land (\lnot a \lor b) \land (\lnot a \lor \lnot b) \land (a \lor \lnot c)$$

Đồ thị có hướng sẽ chứa các đỉnh và cạnh sau:

$$\begin{array}{cccc}
\lnot a \Rightarrow \lnot b & a \Rightarrow b & a \Rightarrow \lnot b & \lnot a \Rightarrow \lnot c\\
b \Rightarrow a & \lnot b \Rightarrow \lnot a & b \Rightarrow \lnot a & c \Rightarrow a
\end{array}$$

Ta có thể thấy đồ thị kéo theo (implication graph) trong hình sau:

<div style="text-align: center;">
  <img src="2SAT.png" alt=""Implication Graph of 2-SAT example"">
</div>

Một tính chất đáng chú ý của đồ thị kéo theo là:
nếu có cạnh $a \Rightarrow b$ thì cũng có cạnh $\lnot b \Rightarrow \lnot a$. 

Ngoài ra, nếu đi tới được $x$ từ $\lnot x$, đồng thời đi tới được $\lnot x$ từ $x$, thì bài toán không có lời giải.
Dù ta chọn giá trị nào cho biến $x$ thì cũng dẫn đến mâu thuẫn: nếu gán $x$ bằng $\text{true}$, phép kéo theo buộc $\lnot x$ cũng phải bằng $\text{true}$, và ngược lại.
Hóa ra điều kiện này không chỉ cần mà còn đủ.
Ta sẽ chứng minh điều đó trong vài đoạn tiếp theo.
Nhắc lại rằng nếu đi tới được một đỉnh từ đỉnh thứ hai và cũng đi tới được đỉnh thứ hai từ đỉnh thứ nhất, thì hai đỉnh này nằm trong cùng một thành phần liên thông mạnh.
Do đó, có thể phát biểu tiêu chuẩn tồn tại lời giải như sau:

Bài toán 2-SAT có lời giải khi và chỉ khi với mọi biến $x$, hai đỉnh $x$ và $\lnot x$ nằm trong hai thành phần liên thông mạnh khác nhau của đồ thị kéo theo.

**Ghi chú bản dịch:** Câu tương ứng trong nguồn tiếng Anh có cụm từ thừa “of the strong connection”, nhưng tiêu chuẩn ngay trước và sau đó đều xác định rõ rằng ta đang xét các thành phần liên thông mạnh của đồ thị kéo theo. Bản dịch giữ đúng ý kỹ thuật này; lỗi diễn đạt của nguồn được tách riêng để đề xuất sửa ở upstream.

Tiêu chuẩn này có thể được kiểm tra trong $O(n + m)$ bằng cách tìm tất cả các thành phần liên thông mạnh.

Hình sau biểu diễn tất cả các thành phần liên thông mạnh của ví dụ.
Dễ kiểm tra rằng không thành phần nào trong bốn thành phần chứa đồng thời một đỉnh $x$ và phủ định $\lnot x$ của nó, vì vậy ví dụ có lời giải.
Trong các đoạn tiếp theo, ta sẽ học cách tính một phép gán hợp lệ; trước mắt, để minh họa, một lời giải là $a = \text{false}$, $b = \text{false}$, $c = \text{false}$.

<div style="text-align: center;">
  <img src="2SAT_SCC.png" alt=""Strongly Connected Components of the 2-SAT example"">
</div>

**Ghi chú bản dịch:** Hai thẻ ảnh trong nguồn hiện có thuộc tính alt sai cú pháp do dấu ngoặc kép bị lặp. Bản dịch giữ nguyên cấu trúc HTML của nguồn để đồng bộ; lỗi markup này được xử lý riêng ở upstream.

Bây giờ ta xây dựng thuật toán tìm lời giải của bài toán 2-SAT với giả thiết rằng lời giải tồn tại.

Lưu ý rằng dù lời giải tồn tại, vẫn có thể xảy ra trường hợp đi tới được $\lnot x$ từ $x$ trong đồ thị kéo theo, hoặc (nhưng không thể đồng thời) đi tới được $x$ từ $\lnot x$.
Trong trường hợp đó, một trong hai lựa chọn $\text{true}$ hoặc $\text{false}$ cho $x$ sẽ dẫn tới mâu thuẫn, còn lựa chọn kia thì không.
Ta cần biết cách chọn giá trị sao cho không tạo ra mâu thuẫn.

Hãy sắp xếp các thành phần liên thông mạnh theo thứ tự tô-pô (tức là $\text{comp}[v] \le \text{comp}[u]$ nếu có đường đi từ $v$ tới $u$), và gọi $\text{comp}[v]$ là chỉ số của thành phần liên thông mạnh chứa đỉnh $v$.
Khi đó, nếu $\text{comp}[x] < \text{comp}[\lnot x]$ thì ta gán $x$ bằng $\text{false}$, ngược lại gán bằng $\text{true}$.

Ta chứng minh rằng phép gán này không dẫn tới mâu thuẫn.
Giả sử $x$ được gán $\text{true}$.
Trường hợp còn lại được chứng minh tương tự.

Trước hết, ta chứng minh rằng đỉnh $x$ không thể đi tới đỉnh $\lnot x$.
Vì ta gán $\text{true}$ nên chỉ số thành phần liên thông mạnh của $x$ phải lớn hơn chỉ số thành phần của $\lnot x$.
Điều đó có nghĩa là $\lnot x$ nằm bên trái thành phần chứa $x$, và đỉnh nằm sau không thể đi tới đỉnh nằm trước.

Tiếp theo, ta chứng minh không tồn tại biến $y$ sao cho cả hai đỉnh $y$ và $\lnot y$ đều đi tới được từ $x$ trong đồ thị kéo theo.
Điều này sẽ gây mâu thuẫn vì $x = \text{true}$ kéo theo $y = \text{true}$ và $\lnot y = \text{true}$.
Ta chứng minh bằng phản chứng.
Giả sử cả $y$ và $\lnot y$ đều đi tới được từ $x$. Theo tính chất của đồ thị kéo theo, từ cả $y$ và $\lnot y$ đều đi tới được $\lnot x$.
Theo tính bắc cầu, từ $x$ đi tới được $\lnot x$, mâu thuẫn với giả thiết.

Như vậy, với giả thiết rằng với mọi biến $x$, hai đỉnh $x$ và $\lnot x$ nằm trong các thành phần liên thông mạnh khác nhau, ta đã xây dựng được thuật toán tìm các giá trị cần gán cho biến.
Phần trên cũng đã chứng minh tính đúng đắn của thuật toán.
Do đó, đồng thời ta cũng chứng minh được tiêu chuẩn tồn tại lời giải đã nêu ở trên.

## Cài đặt:

Bây giờ ta có thể cài đặt toàn bộ thuật toán.
Trước hết, ta xây dựng đồ thị kéo theo và tìm tất cả các thành phần liên thông mạnh.
Việc này có thể được thực hiện bằng thuật toán Kosaraju trong $O(n + m)$.
Ở lượt duyệt thứ hai, thuật toán Kosaraju thăm các thành phần liên thông mạnh theo thứ tự tô-pô, vì vậy ta dễ dàng tính được $\text{comp}[v]$ cho mỗi đỉnh $v$.

Sau đó, ta chọn giá trị gán cho $x$ bằng cách so sánh $\text{comp}[x]$ và $\text{comp}[\lnot x]$. 
Nếu $\text{comp}[x] = \text{comp}[\lnot x]$, ta trả về $\text{false}$ để báo rằng không tồn tại phép gán hợp lệ thỏa mãn bài toán 2-SAT.

Dưới đây là cài đặt lời giải 2-SAT khi đồ thị kéo theo `adj` và đồ thị chuyển vị $adj^{\intercal}$ (trong đó chiều của mọi cạnh được đảo ngược) đã được xây dựng.
Trong đồ thị, các đỉnh có chỉ số $2k$ và $2k+1$ là hai đỉnh tương ứng với biến $k$, trong đó $2k+1$ tương ứng với biến bị phủ định.

```{.cpp file=2sat}
struct TwoSatSolver {
    int n_vars;
    int n_vertices;
    vector<vector<int>> adj, adj_t;
    vector<bool> used;
    vector<int> order, comp;
    vector<bool> assignment;

    TwoSatSolver(int _n_vars) : n_vars(_n_vars), n_vertices(2 * n_vars), adj(n_vertices), adj_t(n_vertices), used(n_vertices), order(), comp(n_vertices, -1), assignment(n_vars) {
        order.reserve(n_vertices);
    }
    void dfs1(int v) {
        used[v] = true;
        for (int u : adj[v]) {
            if (!used[u])
                dfs1(u);
        }
        order.push_back(v);
    }

    void dfs2(int v, int cl) {
        comp[v] = cl;
        for (int u : adj_t[v]) {
            if (comp[u] == -1)
                dfs2(u, cl);
        }
    }

    bool solve_2SAT() {
        order.clear();
        used.assign(n_vertices, false);
        for (int i = 0; i < n_vertices; ++i) {
            if (!used[i])
                dfs1(i);
        }

        comp.assign(n_vertices, -1);
        for (int i = 0, j = 0; i < n_vertices; ++i) {
            int v = order[n_vertices - i - 1];
            if (comp[v] == -1)
                dfs2(v, j++);
        }

        assignment.assign(n_vars, false);
        for (int i = 0; i < n_vertices; i += 2) {
            if (comp[i] == comp[i + 1])
                return false;
            assignment[i / 2] = comp[i] > comp[i + 1];
        }
        return true;
    }

    void add_disjunction(int a, bool na, int b, bool nb) {
        // na and nb signify whether a and b are to be negated 
        a = 2 * a ^ na;
        b = 2 * b ^ nb;
        int neg_a = a ^ 1;
        int neg_b = b ^ 1;
        adj[neg_a].push_back(b);
        adj[neg_b].push_back(a);
        adj_t[b].push_back(neg_a);
        adj_t[a].push_back(neg_b);
    }

    static void example_usage() {
        TwoSatSolver solver(3); // a, b, c
        solver.add_disjunction(0, false, 1, true);  //     a  v  not b
        solver.add_disjunction(0, true, 1, true);   // not a  v  not b
        solver.add_disjunction(1, false, 2, false); //     b  v      c
        solver.add_disjunction(0, false, 0, false); //     a  v      a
        assert(solver.solve_2SAT() == true);
        auto expected = vector<bool>{{true, false, true}};
        assert(solver.assignment == expected);
    }
};
```

## Bài tập luyện tập
 * [Codeforces: The Door Problem](http://codeforces.com/contest/776/problem/D)
 * [Kattis: Illumination](https://open.kattis.com/problems/illumination)
 * [UVA: Rectangles](https://uva.onlinejudge.org/index.php?option=com_onlinejudge&Itemid=8&page=show_problem&problem=3081)
 * [Codeforces : Radio Stations](https://codeforces.com/problemset/problem/1215/F)
 * [CSES : Giant Pizza](https://cses.fi/problemset/task/1684)
 * [Codeforces: +-1](https://codeforces.com/contest/1971/problem/H)
 * [Gym: (C) Colorful Village](https://codeforces.com/gym/104772/problem/C)
 * [POI: Renovation](https://szkopul.edu.pl/problemset/problem/xNjwUvwdHQoQTFBrmyG8vD1O/site/?key=statement)