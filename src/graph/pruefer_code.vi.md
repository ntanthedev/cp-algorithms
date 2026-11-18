---
tags:
  - Translated
e_maxx_link: prufer_code_cayley_formula
translation:
  source: graph/pruefer_code.md
  source_commit: d6cb08863385b0936717ca4708427560b8c43ca8
  status: draft
  last_synced: 2026-11-16
---

# Mã Prüfer

Trong bài này, ta tìm hiểu **mã Prüfer** (hay dãy Prüfer), một cách mã hóa duy nhất cây có gán nhãn thành một dãy số.

Với mã Prüfer, ta sẽ chứng minh **công thức Cayley** (cho biết số cây khung của một đồ thị đầy đủ).
Ta cũng trình bày lời giải bài toán đếm số cách thêm cạnh vào một đồ thị để đồ thị liên thông.

**Lưu ý**, ta không xét cây chỉ gồm một đỉnh — đây là trường hợp đặc biệt mà một số phát biểu mâu thuẫn với nhau.

## Mã Prüfer

Mã Prüfer là cách mã hóa một cây có gán nhãn với $n$ đỉnh bằng một dãy $n - 2$ số nguyên trong đoạn $[0; n-1]$.
Phép mã hóa này cũng là một **song ánh** giữa tất cả các cây khung của đồ thị đầy đủ và các dãy số.

Dù dùng mã Prüfer để lưu trữ và thao tác trên cây không thực tế do đặc điểm của cách biểu diễn, mã Prüfer vẫn thường xuyên được sử dụng, chủ yếu để giải các bài toán tổ hợp.

Người phát minh là Heinz Prüfer đã đề xuất mã này năm 1918 để chứng minh công thức Cayley.

### Xây dựng mã Prüfer cho cây cho trước

Mã Prüfer được xây dựng như sau.
Ta lặp lại quy trình sau $n - 2$ lần:
chọn lá có số hiệu nhỏ nhất, xóa lá đó khỏi cây và ghi lại số hiệu đỉnh nối với nó.
Sau $n - 2$ lần lặp, chỉ còn lại $2$ đỉnh và thuật toán kết thúc.

Vậy mã Prüfer của một cây cho trước là dãy $n - 2$ số; mỗi số là số hiệu của đỉnh được nối với lá bị xóa, tức là số này thuộc đoạn $[0, n-1]$.

Có thể cài đặt thuật toán tính mã Prüfer dễ dàng với độ phức tạp thời gian $O(n \log n)$ bằng cách dùng một cấu trúc dữ liệu lấy phần tử nhỏ nhất (chẳng hạn `set` hoặc `priority_queue` trong C++), chứa danh sách các lá hiện tại.

```{.cpp file=pruefer_code_slow}
vector<vector<int>> adj;

vector<int> pruefer_code() {
    int n = adj.size();
    set<int> leafs;
    vector<int> degree(n);
    vector<bool> killed(n, false);
    for (int i = 0; i < n; i++) {
        degree[i] = adj[i].size();
        if (degree[i] == 1)
            leafs.insert(i);
    }

    vector<int> code(n - 2);
    for (int i = 0; i < n - 2; i++) {
        int leaf = *leafs.begin();
        leafs.erase(leafs.begin());
        killed[leaf] = true;

        int v;
        for (int u : adj[leaf]) {
            if (!killed[u])
                v = u;
        }

        code[i] = v;
        if (--degree[v] == 1)
            leafs.insert(v);
    }

    return code;
}
```

Tuy nhiên, cách xây dựng cũng có thể được cài đặt trong thời gian tuyến tính.
Phương pháp này được mô tả ở mục tiếp theo.

### Xây dựng mã Prüfer cho cây cho trước trong thời gian tuyến tính

Bản chất của thuật toán là dùng một **con trỏ di động**, luôn trỏ đến đỉnh lá hiện tại mà ta muốn xóa.

Thoạt nhìn điều này có vẻ bất khả thi, vì trong quá trình xây dựng mã Prüfer, số hiệu lá có thể tăng và giảm.
Tuy nhiên, quan sát kỹ hơn cho thấy thực ra không phải vậy.
Số lượng lá sẽ không tăng. Nó hoặc giảm đi một (ta xóa một đỉnh lá mà không có lá mới), hoặc giữ nguyên (ta xóa một đỉnh lá và có thêm một lá khác).
Trong trường hợp đầu, không còn cách nào khác ngoài tìm đỉnh lá nhỏ nhất tiếp theo.
Tuy nhiên, trong trường hợp thứ hai, ta có thể quyết định trong thời gian $O(1)$ liệu có thể tiếp tục dùng đỉnh vừa trở thành lá hay phải tìm đỉnh lá nhỏ nhất tiếp theo.
Và khá nhiều lần ta có thể tiếp tục với đỉnh lá mới.

Để làm điều này, ta dùng biến $\text{ptr}$, cho biết trong tập các đỉnh từ $0$ đến $\text{ptr}$ có nhiều nhất một đỉnh lá, chính là đỉnh hiện tại.
Mọi đỉnh khác trong đoạn đó hoặc đã bị xóa khỏi cây, hoặc vẫn còn nhiều hơn một đỉnh kề.
Đồng thời, ta nói rằng chưa có đỉnh lá nào lớn hơn $\text{ptr}$ bị xóa.

Biến này đã rất hữu ích trong trường hợp đầu.
Sau khi xóa đỉnh lá hiện tại, ta biết rằng không thể có đỉnh lá nào từ $0$ đến $\text{ptr}$, do đó có thể bắt đầu tìm đỉnh tiếp theo ngay tại $\text{ptr} + 1$, thay vì phải tìm lại từ đỉnh $0$.
Trong trường hợp thứ hai, ta phân biệt thêm hai trường hợp:
Nếu đỉnh lá mới nhỏ hơn $\text{ptr}$, nó phải là đỉnh lá tiếp theo, vì ta biết không còn đỉnh nào khác nhỏ hơn $\text{ptr}$.
Hoặc đỉnh lá mới lớn hơn.
Khi đó ta cũng biết nó phải lớn hơn $\text{ptr}$ và có thể bắt đầu tìm lại từ $\text{ptr} + 1$.

Dù có thể phải tìm tuyến tính nhiều lần để tìm đỉnh lá tiếp theo, con trỏ $\text{ptr}$ chỉ tăng, nên tổng độ phức tạp thời gian là $O(n)$.

```{.cpp file=pruefer_code_fast}
vector<vector<int>> adj;
vector<int> parent;

void dfs(int v) {
    for (int u : adj[v]) {
        if (u != parent[v]) {
            parent[u] = v;
            dfs(u);
        }
    }
}

vector<int> pruefer_code() {
    int n = adj.size();
    parent.resize(n);
    parent[n-1] = -1;
    dfs(n-1);

    int ptr = -1;
    vector<int> degree(n);
    for (int i = 0; i < n; i++) {
        degree[i] = adj[i].size();
        if (degree[i] == 1 && ptr == -1)
            ptr = i;
    }

    vector<int> code(n - 2);
    int leaf = ptr;
    for (int i = 0; i < n - 2; i++) {
        int next = parent[leaf];
        code[i] = next;
        if (--degree[next] == 1 && next < ptr) {
            leaf = next;
        } else {
            ptr++;
            while (degree[ptr] != 1)
                ptr++;
            leaf = ptr;
        }
    }

    return code;
}
```

Trong mã, trước tiên ta tìm `parent[i]` cho mỗi đỉnh: đó là tổ tiên mà đỉnh này có tại thời điểm bị xóa khỏi cây.
Ta có thể tìm tổ tiên này bằng cách chọn đỉnh $n-1$ làm gốc của cây.
Điều này khả thi vì đỉnh $n-1$ sẽ không bao giờ bị xóa khỏi cây.
Ta cũng tính bậc của mỗi đỉnh.
`ptr` là con trỏ cho biết số hiệu nhỏ nhất của các đỉnh lá còn lại (ngoại trừ đỉnh hiện tại `leaf`).
Ta lấy `next` làm đỉnh lá hiện tại nếu nó cũng là một đỉnh lá và nhỏ hơn `ptr`; nếu không, ta tìm tuyến tính đỉnh lá nhỏ nhất bằng cách tăng con trỏ.

**Ghi chú bản dịch:** Mô tả con trỏ ngay trước đó trong nguồn chưa đúng với mọi trạng thái: ban đầu nó có thể bằng chính lá hiện tại. Bất biến ở phần giải thích phía trên là con trỏ chỉ tăng và trong các đỉnh từ 0 đến vị trí của con trỏ có nhiều nhất một lá, là lá hiện tại.

Dễ thấy đoạn mã này có độ phức tạp $O(n)$.

### Một số tính chất của mã Prüfer

- Sau khi xây dựng mã Prüfer, còn lại hai đỉnh.
  Một trong hai là đỉnh lớn nhất $n-1$, nhưng không thể nói gì thêm về đỉnh còn lại.
- Mỗi đỉnh xuất hiện trong mã Prüfer đúng một số lần cố định, bằng bậc của nó trừ một.
  Có thể dễ dàng kiểm tra điều này vì bậc giảm mỗi lần ta ghi số hiệu đỉnh vào mã, và ta xóa đỉnh khi bậc bằng $1$.
  Với hai đỉnh còn lại, tính chất này cũng đúng.

### Khôi phục cây từ mã Prüfer

Để khôi phục cây, chỉ cần tập trung vào tính chất ở mục trước.
Ta đã biết bậc của tất cả các đỉnh trong cây cần tìm.
Vì vậy ta có thể tìm mọi đỉnh lá và cả lá đầu tiên bị xóa ở bước đầu tiên (nó phải là lá nhỏ nhất).
Đỉnh lá này được nối với đỉnh tương ứng với số trong ô đầu tiên của mã Prüfer.

Như vậy, ta tìm được cạnh đầu tiên đã bị xóa khi tạo mã Prüfer.
Ta có thể thêm cạnh này vào đáp án và giảm bậc của cả hai đầu mút.

Ta lặp lại thao tác đến khi đã dùng mọi số trong mã Prüfer:
tìm đỉnh nhỏ nhất có bậc bằng $1$, nối nó với đỉnh tiếp theo trong mã Prüfer và giảm bậc.

Cuối cùng chỉ còn hai đỉnh có bậc bằng $1$.
Đây là các đỉnh không bị xóa trong quá trình tạo mã Prüfer.
Nối chúng để thu được cạnh cuối cùng của cây.
Một trong hai luôn là đỉnh $n-1$.

Thuật toán này dễ **cài đặt** trong $O(n \log n)$: ta dùng một cấu trúc dữ liệu hỗ trợ lấy phần tử nhỏ nhất (ví dụ `set<>` hoặc `priority_queue<>` trong C++) để lưu mọi đỉnh lá.

Cách cài đặt sau trả về danh sách các cạnh tương ứng với cây.


```{.cpp file=pruefer_decode_slow}
vector<pair<int, int>> pruefer_decode(vector<int> const& code) {
    int n = code.size() + 2;
    vector<int> degree(n, 1);
    for (int i : code)
        degree[i]++;

    set<int> leaves;
    for (int i = 0; i < n; i++) {
        if (degree[i] == 1)
            leaves.insert(i);
    }

    vector<pair<int, int>> edges;
    for (int v : code) {
        int leaf = *leaves.begin();
        leaves.erase(leaves.begin());

        edges.emplace_back(leaf, v);
        if (--degree[v] == 1)
            leaves.insert(v);
    }
    edges.emplace_back(*leaves.begin(), n-1);
    return edges;
}
```

### Khôi phục cây từ mã Prüfer trong thời gian tuyến tính

Để thu được cây trong thời gian tuyến tính, ta có thể áp dụng cùng kỹ thuật đã dùng để xây dựng mã Prüfer trong thời gian tuyến tính.

Ta không cần cấu trúc dữ liệu để lấy phần tử nhỏ nhất.
Thay vào đó, ta nhận thấy sau khi xử lý cạnh hiện tại, chỉ có một đỉnh trở thành lá.
Vì vậy, ta có thể tiếp tục với đỉnh này hoặc tìm một đỉnh nhỏ hơn bằng cách tìm kiếm tuyến tính với con trỏ.

```{.cpp file=pruefer_decode_fast}
vector<pair<int, int>> pruefer_decode(vector<int> const& code) {
    int n = code.size() + 2;
    vector<int> degree(n, 1);
    for (int i : code)
        degree[i]++;

    int ptr = 0;
    while (degree[ptr] != 1)
        ptr++;
    int leaf = ptr;

    vector<pair<int, int>> edges;
    for (int v : code) {
        edges.emplace_back(leaf, v);
        if (--degree[v] == 1 && v < ptr) {
            leaf = v;
        } else {
            ptr++;
            while (degree[ptr] != 1)
                ptr++;
            leaf = ptr;
        }
    }
    edges.emplace_back(leaf, n-1);
    return edges;
}
```

### Song ánh giữa cây và mã Prüfer

Mỗi cây đều có một mã Prüfer tương ứng.
Và từ mỗi mã Prüfer ta có thể khôi phục cây ban đầu.

Suy ra mỗi mã Prüfer (tức dãy $n-2$ số trong đoạn $[0; n - 1]$) cũng tương ứng với một cây.

Do đó, tất cả các cây và tất cả các mã Prüfer lập thành một song ánh (**tương ứng một-một**).

## Công thức Cayley

Công thức Cayley phát biểu rằng **số cây khung của đồ thị đầy đủ có gán nhãn** với $n$ đỉnh bằng:

$$n^{n-2}$$

Có nhiều cách chứng minh công thức này.
Khi dùng khái niệm mã Prüfer, phát biểu này trở nên dễ hiểu.

Thật vậy, bất kỳ mã Prüfer nào gồm $n-2$ số trong đoạn $[0; n-1]$ đều tương ứng với một cây có $n$ đỉnh.
Do đó có $n^{n-2}$ mã Prüfer khác nhau như vậy.
Vì mỗi cây đó là một cây khung của đồ thị đầy đủ có $n$ đỉnh, số cây khung ấy cũng bằng $n^{n-2}$.

## Số cách làm cho đồ thị liên thông

Khái niệm mã Prüfer còn mạnh hơn thế.
Nó cho phép xây dựng các công thức tổng quát hơn nhiều so với công thức Cayley.

Trong bài toán này, ta được cho một đồ thị có $n$ đỉnh và $m$ cạnh.
Đồ thị hiện có $k$ thành phần liên thông.
Ta muốn tính số cách thêm $k-1$ cạnh để đồ thị trở nên liên thông (rõ ràng $k-1$ là số cạnh tối thiểu cần thiết để làm đồ thị liên thông).

Ta hãy suy ra một công thức giải bài toán.

Ký hiệu kích thước các thành phần liên thông trong đồ thị là $s_1, \dots, s_k$.
Ta không thể thêm cạnh bên trong một thành phần liên thông.
Do đó, bài toán này hóa ra rất giống bài toán tìm số cây khung của một đồ thị đầy đủ có $k$ đỉnh.
Khác biệt duy nhất là mỗi đỉnh thực ra có kích thước $s_i$: mỗi cạnh nối với đỉnh $i$ thực chất nhân đáp án với $s_i$.

Vì vậy, để tính số cách có thể, điều quan trọng là đếm số lần mỗi đỉnh trong $k$ đỉnh được dùng trong cây kết nối.
Để thu được công thức cho bài toán, cần lấy tổng đáp án trên mọi bộ bậc có thể.

Gọi $d_1, \dots, d_k$ là bậc của các đỉnh trong cây sau khi nối các đỉnh.
Tổng các bậc bằng hai lần số cạnh:

$$\sum_{i=1}^k d_i = 2k - 2$$

Nếu đỉnh $i$ có bậc $d_i$, nó xuất hiện $d_i - 1$ lần trong mã Prüfer.
Mã Prüfer của một cây có $k$ đỉnh có độ dài $k-2$.
Do đó, số cách chọn một mã gồm $k-2$ số, trong đó số $i$ xuất hiện đúng $d_i - 1$ lần, bằng **hệ số đa thức**

$$\binom{k-2}{d_1-1, d_2-1, \dots, d_k-1} = \frac{(k-2)!}{(d_1-1)! (d_2-1)! \cdots (d_k-1)!}.$$

Vì mỗi cạnh kề với đỉnh $i$ nhân đáp án với $s_i$, khi giả sử bậc các đỉnh là $d_1, \dots, d_k$, ta nhận được đáp án:

$$s_1^{d_1} \cdot s_2^{d_2} \cdots s_k^{d_k} \cdot \binom{k-2}{d_1-1, d_2-1, \dots, d_k-1}$$

Để được đáp án cuối cùng, ta cần lấy tổng biểu thức này trên mọi cách chọn bậc có thể:

$$\sum_{\substack{d_i \ge 1 \\\\ \sum_{i=1}^k d_i = 2k -2}} s_1^{d_1} \cdot s_2^{d_2} \cdots s_k^{d_k} \cdot \binom{k-2}{d_1-1, d_2-1, \dots, d_k-1}$$

Đáp án này hiện trông khá phức tạp, nhưng ta có thể dùng **định lý đa thức**, phát biểu rằng:

$$(x_1 + \dots + x_m)^p = \sum_{\substack{c_i \ge 0 \\\\ \sum_{i=1}^m c_i = p}} x_1^{c_1} \cdot x_2^{c_2} \cdots x_m^{c_m} \cdot \binom{p}{c_1, c_2, \dots c_m}$$

Biểu thức này đã khá giống.
Để áp dụng, ta chỉ cần thay $e_i = d_i - 1$:

$$\sum_{\substack{e_i \ge 0 \\\\ \sum_{i=1}^k e_i = k - 2}} s_1^{e_1+1} \cdot s_2^{e_2+1} \cdots s_k^{e_k+1} \cdot \binom{k-2}{e_1, e_2, \dots, e_k}$$

Sau khi áp dụng định lý đa thức, ta được **đáp án của bài toán**:

$$s_1 \cdot s_2 \cdots s_k \cdot (s_1 + s_2 + \dots + s_k)^{k-2} = s_1 \cdot s_2 \cdots s_k \cdot n^{k-2}$$

Tình cờ công thức này cũng đúng với $k = 1$.

## Bài tập

- [UVA #10843 - Anne's game](https://uva.onlinejudge.org/index.php?option=com_onlinejudge&Itemid=8&category=20&page=show_problem&problem=1784)
- [Timus #1069 - Prufer Code](http://acm.timus.ru/problem.aspx?space=1&num=1069)
- [Codeforces - Clues](http://codeforces.com/contest/156/problem/D)
- [Topcoder - TheCitiesAndRoadsDivTwo](https://community.topcoder.com/stat?c=problem_statement&pm=10774&rd=14146)
