---
tags:
  - Original
translation:
  source: graph/centroid_decomposition.md
  source_commit: 7ed8844f64656c95b8ff2f49f1bdadfb83e275cb
  status: draft
  last_synced: 2026-11-16
---

# Phân rã trọng tâm

Kiến thức cần có: [Tìm kiếm theo chiều sâu (DFS)](./depth-first-search.md), [Chia để trị](https://en.wikipedia.org/wiki/Divide-and-conquer_algorithm), [Cây](<https://en.wikipedia.org/wiki/Tree_(graph_theory)>).

## Giới thiệu

**Phân rã trọng tâm** (Centroid Decomposition) là một kỹ thuật chia để trị trên cây. Kỹ thuật này được dùng để giải nhiều bài toán liên quan đến đường đi trên cây, chẳng hạn đếm đường đi có tính chất nhất định, tìm khoảng cách hoặc trả lời truy vấn trên đường đi.

Ý tưởng chính là phân rã cây đệ quy bằng cách tìm **trọng tâm** của nó. Khi xóa đỉnh đặc biệt này, cây tách thành các thành phần mà mỗi thành phần chứa không quá một nửa số đỉnh của cây ban đầu. Điều này đảm bảo độ sâu đệ quy là logarit, từ đó cho phép xây dựng các thuật toán hiệu quả.

## Định nghĩa và tính chất của trọng tâm

Trước tiên ta tìm hiểu trọng tâm là gì. **Trọng tâm** của cây là một đỉnh mà khi xóa đi, không cây con nào còn lại có quá $\frac{N}{2}$ đỉnh, với $N$ là tổng số đỉnh của cây.

<div align="center">
    <img src="./centroid-definition.png" alt="Cây và trọng tâm" />
</div>

Với bất kỳ cây nào có $N$ đỉnh, tồn tại một hoặc hai trọng tâm. Nếu có hai trọng tâm thì chúng phải kề nhau.

### Sự tồn tại và tính duy nhất

**Định lý**: Mỗi cây có ít nhất một và nhiều nhất hai trọng tâm. Nếu có hai trọng tâm thì chúng phải kề nhau.

??? note "Chứng minh"

    _Sự tồn tại_: Bắt đầu từ một đỉnh bất kỳ và liên tục đi đến con có cây con lớn nhất. Dừng lại khi không có con nào có quá $\frac{N}{2}$ đỉnh trong cây con. Khi đó, đỉnh hiện tại $v$ là một trọng tâm vì (1) không cây con nào của nó có quá $\frac{N}{2}$ đỉnh (theo điều kiện dừng), (2) "phía cha" (mọi đỉnh không thuộc cây con gốc $v$ khi $v$ còn là con) có không quá $\frac{N}{2}$ đỉnh (nếu không, ta đã không đi từ cha đến $v$).

    Dễ thấy quá trình này luôn kết thúc, chứng minh tồn tại ít nhất một trọng tâm.

    _Tính duy nhất_: Giả sử có hai trọng tâm $u$ và $v$. Xét đường đi giữa chúng. Khi xóa $u$, đỉnh $v$ phải thuộc một thành phần có không quá $\frac{N}{2}$ đỉnh. Tương tự, khi xóa $v$, đỉnh $u$ phải thuộc một thành phần có không quá $\frac{N}{2}$ đỉnh. Điều này chỉ có thể xảy ra nếu $u$ và $v$ kề nhau; nếu không, khi xóa một trong hai đỉnh, đỉnh còn lại sẽ thuộc một thành phần có quá $\frac{N}{2}$ đỉnh. Điều này mâu thuẫn với giả thiết ban đầu rằng cả hai trọng tâm đều nằm trong thành phần có không quá $\frac{N}{2}$ đỉnh. Hơn nữa, nếu tồn tại hai trọng tâm thì chúng phải chia cây thành hai thành phần, mỗi thành phần có đúng $\frac{N}{2}$ đỉnh; điều này chỉ có thể xảy ra khi $N$ chẵn.

## Định nghĩa và tính chất của phân rã trọng tâm

"Phân rã" cây về cơ bản là tìm trọng tâm một cách đệ quy và chia cây thành các cây con dựa trên các thành phần sau khi xóa trọng tâm. Việc phân rã đệ quy thành các thành phần này tạo ra những tính chất đặc biệt sau:

1. **Độ sâu phân rã**: Độ sâu là $O(\log N)$ vì mỗi mức giảm kích thước thành phần ít nhất một nửa.
2. **Bao phủ đường đi**: Mỗi đường đi trên cây đi qua trọng tâm của một thành phần nào đó trong quá trình phân rã.

### Độ sâu phân rã

**Định lý**: Độ sâu, hay số bước, khi phân rã trọng tâm một cây bất kỳ là $O(\log N)$.

??? note "Chứng minh"

    Xét một đỉnh $v$ bất kỳ trong cây ban đầu. Ta theo dõi số lần $v$ có thể thuộc một thành phần trong quá trình phân rã.

    Ở mức đầu tiên, $v$ thuộc thành phần có kích thước $N$. Khi xóa trọng tâm của thành phần này, $v$ nằm trong một thành phần có kích thước không quá $\frac{N}{2}$ (theo tính chất cân bằng).

    Ở mức thứ hai, $v$ thuộc thành phần có kích thước không quá $\frac{N}{2}$. Xóa trọng tâm của thành phần đó sẽ đưa $v$ vào một thành phần có kích thước không quá $\frac{N}{4}$.

    Tiếp tục như vậy, ở mức thứ $k$, $v$ thuộc thành phần có kích thước không quá $\frac{N}{2^{k-1}}$.

    Việc phân rã dừng khi kích thước các thành phần đạt 1. Điều này xảy ra khi $\frac{N}{2^{k-1}} \leq 1$, suy ra $k \leq \log_2 N + 1$.

    Do đó, độ sâu lớn nhất của cây phân rã trọng tâm là $O(\log N)$.

**Ghi chú bản dịch:** Chiều suy luận trong câu áp chót của chứng minh nguồn không đúng. Để có cận trên, xét một thành phần còn tồn tại ở mức k: kích thước nguyên dương của nó ít nhất là 1 và không quá N/2^(k-1). Do đó 1 ≤ N/2^(k-1), suy ra k ≤ log₂N + 1.

**Hệ quả**: Vì mỗi đỉnh tham gia vào nhiều nhất $O(\log N)$ mức phân rã và ta xử lý mỗi đỉnh một lần ở mỗi mức, các thuật toán dùng phân rã trọng tâm thường có một thừa số độ phức tạp thời gian $O(\log N)$ nhân với lượng công việc trên mỗi đỉnh ở mỗi mức.

### Bao phủ đường đi

**Định lý**: Mỗi đường đi trong cây ban đầu đi qua trọng tâm của một thành phần nào đó trong quá trình phân rã.

??? note "Chứng minh"

    Xét đường đi $P$ bất kỳ từ đỉnh $u$ đến đỉnh $v$ trong cây ban đầu. Ta cần chứng minh đường đi này qua ít nhất một trọng tâm được chọn trong quá trình phân rã.

    Ta chứng minh bằng quy nạp theo quá trình phân rã.

    _Cơ sở_: Ở mức phân rã đầu tiên, ta chọn trọng tâm $c_1$ của toàn bộ cây. Nếu đường đi $P$ qua $c_1$ thì chứng minh hoàn tất.

    _Bước quy nạp_: Giả sử đường đi $P$ không qua $c_1$. Khi xóa $c_1$, cây tách thành nhiều thành phần. Vì $P$ là một đường đi liên thông, cả $u$ và $v$ phải nằm trong cùng một thành phần $C$ sau khi xóa $c_1$ (nếu không, $P$ phải đi qua $c_1$ để nối chúng, mâu thuẫn với giả thiết).

    Ta phân rã đệ quy thành phần $C$. Theo giả thiết quy nạp áp dụng cho $C$, đường đi $P$ (nằm hoàn toàn trong $C$) phải qua trọng tâm của một thành phần trong phép phân rã $C$.

    Quá trình tiếp tục cho đến khi tìm được một trọng tâm mà $P$ đi qua. Quá trình phải kết thúc vì tại mỗi mức, thành phần chứa $P$ nhỏ đi thực sự (theo tính chất cân bằng), và cuối cùng giảm còn một cạnh hoặc một đỉnh.

**Hệ quả**: Tính chất này là cơ sở cho tính đúng đắn của các thuật toán phân rã trọng tâm. Nó đảm bảo rằng khi xử lý mọi đường đi qua từng trọng tâm, ta bao phủ mọi đường đi trên cây đúng một lần ở một mức phân rã nào đó. Đây là lý do phân rã trọng tâm có thể giải hiệu quả các bài toán về đường đi: mỗi đường đi được xét đúng một lần, ở mức mà nó gặp trọng tâm đầu tiên.

## Tìm trọng tâm

Để tìm trọng tâm của cây một cách hiệu quả:

1. Tính kích thước cây con của mọi đỉnh bằng tìm kiếm theo chiều sâu (DFS)
2. Bắt đầu từ một đỉnh bất kỳ
3. Tìm một con $v$ có cây con chứa quá $\frac{N}{2}$ đỉnh
4. Đi đến $v$ và lặp lại bước 3
5. Nếu không có con nào như vậy, đỉnh hiện tại là trọng tâm

Độ phức tạp thời gian: $O(N)$.

Độ phức tạp bộ nhớ: $O(N)$.

## Mô tả thuật toán

Khi dùng phân rã trọng tâm, quy trình tổng quát như sau:

1. **Tìm trọng tâm** của cây hoặc thành phần hiện tại
2. **Xử lý** mọi đường đi qua trọng tâm này và thực hiện các phép tính mong muốn
3. **Xóa** trọng tâm (đánh dấu đã dùng)
4. **Phân rã đệ quy** từng cây con thu được

Quá trình này tạo ra một **cây trọng tâm**. Mỗi nút trong cây này biểu diễn một trọng tâm ở một giai đoạn phân rã. Nghĩa là cha của một trọng tâm (một nút bất kỳ) là trọng tâm được tìm thấy trong thành phần lớn hơn chứa nó. Chiều cao của cây này là $O(\log N)$ như đã chứng minh ở trên.

<div align="center">
    <img src="./CentroidTree.png" alt="Cây trọng tâm" />
</div>

Ví dụ, hình trên biểu diễn một cây trọng tâm. Mỗi nút ở mỗi mức của cây là trọng tâm của thành phần tương ứng (chẳng hạn gốc là trọng tâm của toàn cây, con ngoài cùng bên trái của gốc là trọng tâm của cây con ngoài cùng bên trái của gốc, v.v.).

## Cài đặt

Sau đây là một cách cài đặt phân rã trọng tâm để giải bài toán cụ thể: **đếm mọi đường đi trên cây có độ dài đúng bằng $K$**.

Trong bài toán này, ta được cho một cây có $N$ đỉnh và cần đếm số đường đi có đúng $K$ cạnh. Một đường đi được xác định bởi hai đỉnh phân biệt.

```{.cpp file=centroid_decomposition}
const int MAXN = 1e5;
vector<int> adj[MAXN];
bool removed[MAXN];
int subtree_size[MAXN];
int K;  // Target path length
long long answer = 0;  // Count of paths with length K

int get_subtree_size(int v, int p = -1) {
    subtree_size[v] = 1;
    for (int u : adj[v]) {
        if (u == p || removed[u]) continue;
        subtree_size[v] += get_subtree_size(u, v);
    }
    return subtree_size[v];
}

int get_centroid(int v, int tree_size, int p = -1) {
    for (int u : adj[v]) {
        if (u == p || removed[u]) continue;
        if (subtree_size[u] * 2 > tree_size)
            return get_centroid(u, tree_size, v);
    }
    return v;
}

void get_distances(int v, int p, int dist, vector<int>& distances) {
    if (dist > K) return;
    distances.push_back(dist);
    for (int u : adj[v]) {
        if (u == p || removed[u]) continue;
        get_distances(u, v, dist + 1, distances);
    }
}

void process_centroid(int centroid) {
    unordered_map<int, int> all_distances;
    all_distances[0] = 1;

    for (int u : adj[centroid]) {
        if (removed[u])
            continue;

        vector<int> current_distances;
        get_distances(u, centroid, 1, current_distances);

        for (int d : current_distances) {
            if (K - d >= 0) {
                answer += (all_distances[K - d] ? all_distances[K - d] : 0);
            }
        }

        for (int d : current_distances) {
            if (all_distances.find(d) == all_distances.end())
                all_distances[d] = 0;
            all_distances[d]++;
        }
    }
}

void decompose(int v) {
    int tree_size = get_subtree_size(v);
    int centroid = get_centroid(v, tree_size);

    process_centroid(centroid);

    removed[centroid] = true;

    for (int u : adj[centroid]) {
        if (!removed[u]) {
            decompose(u);
        }
    }
}
```

Mẫu này có thể được điều chỉnh để giải những bài toán khác bằng phân rã trọng tâm. Trong trường hợp cụ thể này, nó giải bài toán đếm mọi đường đi có độ dài $K$. Chiến lược là: với mỗi trọng tâm, đếm các đường đi qua nó bằng cách tìm những cặp đỉnh ở các cây con khác nhau có khoảng cách $d_1$ và $d_2$ với tổng bằng $K$ (tức là một đường đi qua trọng tâm gồm một đỉnh ở cây con này cách trọng tâm $d_1$ và một đỉnh ở cây con khác cách trọng tâm $d_2$, với $d_1 + d_2 = K$). Với mỗi khoảng cách $d$ trong cây con hiện tại, đoạn mã đếm số đỉnh cách trọng tâm $K - d$ trong các cây con đã xét. Phép tối ưu bỏ qua các khoảng cách lớn hơn $K$ để tránh đệ quy không cần thiết.

**Ghi chú bản dịch:** Đoạn mã còn đếm các đường đi có một đầu mút là chính trọng tâm: cnt[0] = 1 biểu diễn trọng tâm ở khoảng cách 0.

### Xây dựng cây trọng tâm

Nếu cần xây dựng cấu trúc cây trọng tâm tường minh (có ích khi trả lời truy vấn):



```cpp
int centroid_parent[MAXN];

int decompose(int v, int p = -1) {
    int tree_size = get_subtree_size(v);
    int centroid = get_centroid(v, tree_size);

    centroid_parent[centroid] = p;
    removed[centroid] = true;

    for (int u : adj[centroid]) {
        if (!removed[u]) {
            decompose(u, centroid);
        }
    }

    return centroid;
}
```

## Bài tập

- [CSES - Finding a Centroid](https://cses.fi/problemset/task/2079) [độ khó: dễ]
- [CSES - Fixed-Length Paths II](https://cses.fi/problemset/task/2081) [độ khó: dễ]
- [Codeforces - Xenia and Tree](http://codeforces.com/problemset/problem/342/E) [độ khó: trung bình]
- [Codeforces - Digit Tree](http://codeforces.com/contest/716/problem/E) [độ khó: trung bình]
- [OJ - Race](https://oj.uz/problem/view/IOI11_race) [độ khó: trung bình]
- [SPOJ - QTREE5](http://www.spoj.com/problems/QTREE5/) [độ khó: khó]
