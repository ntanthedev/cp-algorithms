---
tags:
  - Translated
e_maxx_link: lca_linear
translation:
  source: graph/lca_farachcoltonbender.md
  source_commit: 5065093597d0659ea259223bdf29145017354c6e
  status: draft
  last_synced: 2026-08-07
---

# Tổ tiên chung gần nhất - Thuật toán Farach-Colton và Bender

Cho $G$ là một cây.
Với mỗi truy vấn dạng $(u, v)$, ta muốn tìm tổ tiên chung gần nhất của hai đỉnh $u$ và $v$. Cụ thể, ta cần tìm một đỉnh $w$ vừa nằm trên đường đi từ $u$ tới đỉnh gốc, vừa nằm trên đường đi từ $v$ tới đỉnh gốc; nếu có nhiều đỉnh như vậy, ta chọn đỉnh xa gốc nhất.
Nói cách khác, đỉnh cần tìm $w$ là tổ tiên thấp nhất của $u$ và $v$.
Đặc biệt, nếu $u$ là tổ tiên của $v$ thì $u$ chính là tổ tiên chung gần nhất của chúng.

Thuật toán được trình bày trong bài này do Farach-Colton và Bender phát triển.
Về mặt tiệm cận, đây là một thuật toán tối ưu.

## Thuật toán

Ta sử dụng phép quy bài toán LCA về bài toán RMQ kinh điển.
Ta duyệt toàn bộ các đỉnh của cây bằng [DFS](depth-first-search.md), đồng thời lưu một mảng chứa thứ tự các đỉnh được thăm và độ cao của chúng.
LCA của hai đỉnh $u$ và $v$ chính là đỉnh có độ cao nhỏ nhất nằm giữa hai lần xuất hiện tương ứng của $u$ và $v$ trong Euler tour.

Hình dưới đây minh họa một Euler tour có thể có của một cây; danh sách phía dưới cho biết các đỉnh được thăm và độ cao của chúng.

**Ghi chú bản dịch:** Nguồn tiếng Anh ở câu trên dùng “a graph”, nhưng toàn bộ ngữ cảnh của bài LCA và phép duyệt đang xét một cây. Vì vậy hình minh họa phải được hiểu là Euler tour của cây; lỗi diễn đạt này đã được đề xuất sửa trong upstream PR #1679.

<div style="text-align: center;">
  <img src="LCA_Euler.png" alt="LCA_Euler_Tour">
</div>

$$\begin{array}{|l|c|c|c|c|c|c|c|c|c|c|c|c|c|}
\hline
\text{Nodes:}   & 1 & 2 & 5 & 2 & 6 & 2 & 1 & 3 & 1 & 4 & 7 & 4 & 1 \\ \hline
\text{Heights:} & 1 & 2 & 3 & 2 & 3 & 2 & 1 & 2 & 1 & 2 & 3 & 2 & 1 \\ \hline
\end{array}$$

Bạn có thể đọc thêm về phép quy này trong bài [Lowest Common Ancestor](lca.md).
Trong bài đó, giá trị nhỏ nhất trên một đoạn được tìm bằng chia căn trong $O(\sqrt{N})$ hoặc bằng Segment Tree trong $O(\log N)$.
Trong bài này, ta sẽ tìm cách trả lời truy vấn giá trị nhỏ nhất trên đoạn trong $O(1)$, trong khi thời gian tiền xử lý vẫn chỉ là $O(N)$.

Lưu ý rằng bài toán RMQ sau khi quy đổi có một tính chất rất đặc biệt:
hai phần tử kề nhau bất kỳ trong mảng luôn chênh lệch đúng một đơn vị (vì các phần tử của mảng chỉ là độ cao của các đỉnh theo thứ tự duyệt; ta hoặc đi xuống một hậu duệ, khi đó phần tử kế tiếp tăng một, hoặc quay về tổ tiên, khi đó phần tử kế tiếp giảm một).
Thuật toán Farach-Colton và Bender đưa ra lời giải dành riêng cho dạng RMQ đặc biệt này.

Ký hiệu $A$ là mảng mà ta muốn thực hiện các truy vấn giá trị nhỏ nhất trên đoạn.
Và $N$ là kích thước của $A$.

Có một cấu trúc dữ liệu đơn giản để giải RMQ với tiền xử lý $O(N \log N)$ và thời gian $O(1)$ cho mỗi truy vấn: [Sparse Table](../data_structures/sparse-table.md).
Ta xây dựng bảng $T$, trong đó mỗi phần tử $T[i][j]$ bằng giá trị nhỏ nhất của $A$ trên đoạn $[i, i + 2^j - 1]$.
Hiển nhiên $0 \leq j \leq \lceil \log N \rceil$, vì vậy kích thước của Sparse Table là $O(N \log N)$.
Ta có thể xây dựng bảng trong $O(N \log N)$ bằng nhận xét $T[i][j] = \min(T[i][j-1], T[i+2^{j-1}][j-1])$.

Làm thế nào để trả lời một truy vấn RMQ trong $O(1)$ bằng cấu trúc dữ liệu này?
Giả sử truy vấn nhận được là $[l, r]$, khi đó đáp án là $\min(T[l][\text{sz}], T[r-2^{\text{sz}}+1][\text{sz}])$, với $\text{sz}$ là số mũ lớn nhất sao cho $2^{\text{sz}}$ không vượt quá độ dài đoạn $r-l+1$.
Thật vậy, ta có thể phủ đoạn $[l, r]$ bằng hai đoạn có độ dài $2^{\text{sz}}$: một đoạn bắt đầu tại $l$ và một đoạn kết thúc tại $r$.
Hai đoạn này có thể chồng lên nhau, nhưng điều đó không ảnh hưởng tới phép tính.
Để thực sự đạt độ phức tạp $O(1)$ cho mỗi truy vấn, ta cần biết giá trị $\text{sz}$ ứng với mọi độ dài có thể từ $1$ tới $N$.
Các giá trị này có thể được tiền xử lý dễ dàng.

Bây giờ ta muốn giảm độ phức tạp tiền xử lý xuống $O(N)$.

Ta chia mảng $A$ thành các khối có kích thước $K = 0.5 \log N$, trong đó $\log$ là logarit cơ số 2.
Với mỗi khối, ta tính phần tử nhỏ nhất rồi lưu các giá trị đó vào mảng $B$.
$B$ có kích thước $\frac{N}{K}$.
Ta xây dựng một Sparse Table từ mảng $B$.
Kích thước và độ phức tạp thời gian của cấu trúc này là:

$$\frac{N}{K}\log\left(\frac{N}{K}\right) = \frac{2N}{\log(N)} \log\left(\frac{2N}{\log(N)}\right) =$$

$$= \frac{2N}{\log(N)} \left(1 + \log\left(\frac{N}{\log(N)}\right)\right) \leq \frac{2N}{\log(N)} + 2N = O(N)$$

Bây giờ ta chỉ còn phải tìm cách trả lời nhanh truy vấn giá trị nhỏ nhất nằm hoàn toàn trong một khối.
Thực tế, nếu truy vấn là $[l, r]$ và $l$, $r$ nằm ở hai khối khác nhau thì đáp án là giá trị nhỏ nhất trong ba đại lượng sau:
giá trị nhỏ nhất của hậu tố thuộc khối chứa $l$ bắt đầu tại $l$, giá trị nhỏ nhất của tiền tố thuộc khối chứa $r$ kết thúc tại $r$, và giá trị nhỏ nhất của các khối nằm giữa chúng.
Giá trị nhỏ nhất của các khối ở giữa có thể được trả lời trong $O(1)$ bằng Sparse Table.
Vì vậy, chỉ còn các truy vấn RMQ nằm trong cùng một khối.

Tại đây ta sẽ khai thác tính chất đặc biệt của mảng.
Nhớ rằng các giá trị trong mảng — chính là độ cao của các đỉnh trên cây — luôn chênh lệch nhau một đơn vị.
Nếu bỏ phần tử đầu tiên của một khối và lấy mọi phần tử còn lại trừ đi phần tử đó, mỗi khối có thể được đặc trưng bởi một dãy độ dài $K - 1$ chỉ gồm các số $+1$ và $-1$.
Do các khối rất nhỏ, chỉ có ít dãy khác nhau có thể xuất hiện.
Số dãy có thể có là:

$$2^{K-1} = 2^{0.5 \log(N) - 1} = 0.5 \left(2^{\log(N)}\right)^{0.5} = 0.5 \sqrt{N}$$

Do đó, số loại khối khác nhau là $O(\sqrt{N})$, vì vậy ta có thể tiền xử lý kết quả các truy vấn giá trị nhỏ nhất trong mọi loại khối khác nhau trong $O(\sqrt{N} K^2) = O(\sqrt{N} \log^2(N)) = O(N)$.
Trong phần cài đặt, ta có thể đặc trưng một khối bằng một bitmask độ dài $K-1$ (vừa trong một kiểu int thông thường) và lưu chỉ số của phần tử nhỏ nhất vào mảng $\text{block}[\text{mask}][l][r]$ có kích thước $O(\sqrt{N} \log^2(N))$.

Như vậy, ta đã biết cách tiền xử lý cả các truy vấn giá trị nhỏ nhất bên trong từng khối lẫn truy vấn trên một dãy các khối, tất cả trong $O(N)$.
Với các dữ liệu tiền xử lý này, mỗi truy vấn có thể được trả lời trong $O(1)$ bằng nhiều nhất bốn giá trị đã tính trước: giá trị nhỏ nhất trong khối chứa `l`, giá trị nhỏ nhất trong khối chứa `r`, và hai giá trị nhỏ nhất của hai đoạn chồng lấn thuộc các khối nằm giữa chúng.

## Cài đặt

```cpp
int n;
vector<vector<int>> adj;

int block_size, block_cnt;
vector<int> first_visit;
vector<int> euler_tour;
vector<int> height;
vector<int> log_2;
vector<vector<int>> st;
vector<vector<vector<int>>> blocks;
vector<int> block_mask;

void dfs(int v, int p, int h) {
    first_visit[v] = euler_tour.size();
    euler_tour.push_back(v);
    height[v] = h;
    
    for (int u : adj[v]) {
        if (u == p)
            continue;
        dfs(u, v, h + 1);
        euler_tour.push_back(v);
    }
}

int min_by_h(int i, int j) {
    return height[euler_tour[i]] < height[euler_tour[j]] ? i : j;
}

void precompute_lca(int root) {
    // get euler tour & indices of first occurrences
    first_visit.assign(n, -1);
    height.assign(n, 0);
    euler_tour.reserve(2 * n);
    dfs(root, -1, 0);

    // precompute all log values
    int m = euler_tour.size();
    log_2.reserve(m + 1);
    log_2.push_back(-1);
    for (int i = 1; i <= m; i++)
        log_2.push_back(log_2[i / 2] + 1);

    block_size = max(1, log_2[m] / 2);
    block_cnt = (m + block_size - 1) / block_size;

    // precompute minimum of each block and build sparse table
    st.assign(block_cnt, vector<int>(log_2[block_cnt] + 1));
    for (int i = 0, j = 0, b = 0; i < m; i++, j++) {
        if (j == block_size)
            j = 0, b++;
        if (j == 0 || min_by_h(i, st[b][0]) == i)
            st[b][0] = i;
    }
    for (int l = 1; l <= log_2[block_cnt]; l++) {
        for (int i = 0; i < block_cnt; i++) {
            int ni = i + (1 << (l - 1));
            if (ni >= block_cnt)
                st[i][l] = st[i][l-1];
            else
                st[i][l] = min_by_h(st[i][l-1], st[ni][l-1]);
        }
    }

    // precompute mask for each block
    block_mask.assign(block_cnt, 0);
    for (int i = 0, j = 0, b = 0; i < m; i++, j++) {
        if (j == block_size)
            j = 0, b++;
        if (j > 0 && (i >= m || min_by_h(i - 1, i) == i - 1))
            block_mask[b] += 1 << (j - 1);
    }

    // precompute RMQ for each unique block
    int possibilities = 1 << (block_size - 1);
    blocks.resize(possibilities);
    for (int b = 0; b < block_cnt; b++) {
        int mask = block_mask[b];
        if (!blocks[mask].empty())
            continue;
        blocks[mask].assign(block_size, vector<int>(block_size));
        for (int l = 0; l < block_size; l++) {
            blocks[mask][l][l] = l;
            for (int r = l + 1; r < block_size; r++) {
                blocks[mask][l][r] = blocks[mask][l][r - 1];
                if (b * block_size + r < m)
                    blocks[mask][l][r] = min_by_h(b * block_size + blocks[mask][l][r], 
                            b * block_size + r) - b * block_size;
            }
        }
    }
}

int lca_in_block(int b, int l, int r) {
    return blocks[block_mask[b]][l][r] + b * block_size;
}

int lca(int v, int u) {
    int l = first_visit[v];
    int r = first_visit[u];
    if (l > r)
        swap(l, r);
    int bl = l / block_size;
    int br = r / block_size;
    if (bl == br)
        return euler_tour[lca_in_block(bl, l % block_size, r % block_size)];
    int ans1 = lca_in_block(bl, l % block_size, block_size - 1);
    int ans2 = lca_in_block(br, 0, r % block_size);
    int ans = min_by_h(ans1, ans2);
    if (bl + 1 < br) {
        int l = log_2[br - bl - 1];
        int ans3 = st[bl+1][l];
        int ans4 = st[br - (1 << l)][l];
        ans = min_by_h(ans, min_by_h(ans3, ans4));
    }
    return euler_tour[ans];
}
```