---
tags:
  - Translated
e_maxx_link: sqrt_decomposition
translation:
  source: data_structures/sqrt_decomposition.md
  source_commit: 5b74cb0dd4f684050ad2388086c9a47333c36419
  status: draft
  last_synced: 2026-08-07
---

# Chia căn

Chia căn (Sqrt Decomposition) là một phương pháp (hoặc một cấu trúc dữ liệu) cho phép thực hiện một số thao tác phổ biến như tìm tổng các phần tử của mảng con, tìm phần tử nhỏ nhất/lớn nhất, v.v. trong $O(\sqrt n)$ thao tác, nhanh hơn đáng kể so với $O(n)$ của thuật toán ngây thơ.

Trước tiên, ta mô tả cấu trúc dữ liệu cho một trong những ứng dụng đơn giản nhất của ý tưởng này, sau đó chỉ ra cách tổng quát hóa để giải một số bài toán khác, và cuối cùng xét một cách dùng hơi khác của cùng ý tưởng: chia các truy vấn đầu vào thành các khối cỡ căn bậc hai.

## Cấu trúc dữ liệu dựa trên chia căn

Cho mảng $a[0 \dots n-1]$, hãy cài đặt một cấu trúc dữ liệu cho phép tìm tổng các phần tử $a[l \dots r]$ với mọi $l$ và $r$ trong $O(\sqrt n)$ thao tác.

### Mô tả

Ý tưởng cơ bản của chia căn là tiền xử lý. Ta chia mảng $a$ thành các khối có độ dài xấp xỉ $\sqrt n$, rồi với mỗi khối $i$ tính trước tổng các phần tử trong đó là $b[i]$.

Ta có thể giả sử cả kích thước khối và số khối đều bằng $\sqrt n$ làm tròn lên:

$$ s = \lceil \sqrt n \rceil $$

Khi đó mảng $a$ được chia thành các khối như sau:

$$ \underbrace{a[0], a[1], \dots, a[s-1]}_{\text{b[0]}}, \underbrace{a[s], \dots, a[2s-1]}_{\text{b[1]}}, \dots, \underbrace{a[(s-1) \cdot s], \dots, a[n-1]}_{\text{b[s-1]}} $$

Khối cuối có thể chứa ít phần tử hơn các khối khác (nếu $n$ không chia hết cho $s$), nhưng điều này không quan trọng vì có thể xử lý dễ dàng.
Như vậy, với mỗi khối $k$, ta biết tổng các phần tử trong khối là $b[k]$:

$$ b[k] = \sum\limits_{i=k\cdot s}^{\min {(n-1,(k+1)\cdot s - 1})} a[i] $$

Ta đã tính xong các giá trị $b[k]$ với $O(n)$ thao tác. Chúng giúp trả lời mỗi truy vấn $[l, r]$ như thế nào?
Nhận xét rằng nếu đoạn $[l, r]$ đủ dài, nó sẽ chứa một số khối hoàn chỉnh; với mỗi khối như vậy ta lấy tổng các phần tử chỉ bằng một thao tác. Vì thế, đoạn $[l, r]$ chỉ còn hai phần thuộc các khối ở hai đầu mà ta phải cộng trực tiếp từng phần tử.

Do đó, để tính tổng trên đoạn $[l, r]$, ta chỉ cần cộng các phần tử ở hai "đuôi":
$[l\dots (k + 1)\cdot s-1]$ và $[p\cdot s\dots r]$, rồi cộng các giá trị $b[i]$ của mọi khối từ $k + 1$ đến $p-1$:

$$ \sum\limits_{i=l}^r a[i] = \sum\limits_{i=l}^{(k+1) \cdot s-1} a[i] + \sum\limits_{i=k+1}^{p-1} b[i] + \sum\limits_{i=p\cdot s}^r a[i] $$

_Lưu ý: Khi $k = p$, tức $l$ và $r$ thuộc cùng một khối, công thức trên không áp dụng được và ta nên tính tổng trực tiếp._

Cách làm này giảm đáng kể số thao tác. Thật vậy, kích thước mỗi "đuôi" không vượt quá độ dài khối $s$, và số khối cần cộng cũng không vượt quá $s$. Vì đã chọn $s \approx \sqrt n$, tổng số thao tác để tìm tổng trên đoạn $[l, r]$ là $O(\sqrt n)$.

### Cài đặt

Bắt đầu với cài đặt đơn giản nhất:

```cpp
// input data
int n;
vector<int> a (n);

// preprocessing
int len = (int) sqrt (n + .0) + 1; // size of the block and the number of blocks
vector<int> b (len);
for (int i=0; i<n; ++i)
    b[i / len] += a[i];

// answering the queries
for (;;) {
    int l, r;
  // read input data for the next query
    int sum = 0;
    for (int i=l; i<=r; )
        if (i % len == 0 && i + len - 1 <= r) {
            // if the whole block starting at i belongs to [l, r]
            sum += b[i / len];
            i += len;
        }
        else {
            sum += a[i];
            ++i;
        }
}
```

Cài đặt này thực hiện quá nhiều phép chia không cần thiết (mà phép chia chậm hơn đáng kể so với các phép toán số học khác). Thay vào đó, ta có thể tính trước chỉ số hai khối $c_l$ và $c_r$ chứa các chỉ số $l$ và $r$, rồi duyệt các khối $c_l+1 \dots c_r-1$ riêng, đồng thời xử lý hai "đuôi" trong các khối $c_l$ và $c_r$. Cách làm này đúng với công thức cuối ở phần mô tả và coi trường hợp $c_l = c_r$ là một trường hợp riêng.

```cpp
int sum = 0;
int c_l = l / len,   c_r = r / len;
if (c_l == c_r)
    for (int i=l; i<=r; ++i)
        sum += a[i];
else {
    for (int i=l, end=(c_l+1)*len-1; i<=end; ++i)
        sum += a[i];
    for (int i=c_l+1; i<=c_r-1; ++i)
        sum += b[i];
    for (int i=c_r*len; i<=r; ++i)
        sum += a[i];
}
```

## Các bài toán khác

Cho đến giờ ta mới xét bài toán tìm tổng các phần tử của một mảng con liên tiếp. Có thể mở rộng bài toán để cho phép **cập nhật từng phần tử của mảng**. Nếu phần tử $a[i]$ thay đổi, ta chỉ cần cập nhật giá trị $b[k]$ của khối chứa phần tử đó ($k = i / s$) bằng một thao tác:

$$ b[k] += a_{new}[i] - a_{old}[i] $$

Mặt khác, bài toán tìm tổng có thể được thay bằng bài toán tìm phần tử nhỏ nhất/lớn nhất của một mảng con. Nếu bài toán đồng thời cho phép cập nhật từng phần tử, ta vẫn có thể cập nhật $b[k]$, nhưng phải duyệt mọi giá trị trong khối $k$ với $O(s) = O(\sqrt{n})$ thao tác.

Chia căn có thể được áp dụng tương tự cho cả một lớp bài toán khác: đếm số phần tử bằng 0, tìm phần tử khác 0 đầu tiên, đếm các phần tử thỏa một tính chất nào đó, v.v.

Một lớp bài toán khác xuất hiện khi ta cần **cập nhật các phần tử trên một đoạn**: tăng các giá trị hiện tại hoặc gán chúng thành một giá trị cho trước.

Ví dụ, giả sử ta có hai loại thao tác trên mảng: cộng một giá trị $\delta$ vào mọi phần tử trên đoạn $[l, r]$, hoặc truy vấn giá trị của phần tử $a[i]$. Ta lưu trong $b[k]$ giá trị cần cộng vào mọi phần tử của khối $k$ (ban đầu mọi $b[k] = 0$). Với mỗi thao tác "cộng", ta cộng $\delta$ vào $b[k]$ cho mọi khối nằm trọn trong đoạn $[l, r]$, đồng thời cộng $\delta$ trực tiếp vào $a[i]$ cho các phần tử thuộc hai "đuôi" của đoạn. Đáp án của truy vấn $i$ đơn giản là $a[i] + b[i/s]$. Như vậy thao tác "cộng" có độ phức tạp $O(\sqrt{n})$, còn trả lời một truy vấn mất $O(1)$.

Cuối cùng, hai lớp bài toán trên có thể kết hợp nếu đề yêu cầu **vừa** cập nhật phần tử trên đoạn **vừa** truy vấn trên đoạn. Cả hai thao tác đều có thể thực hiện trong $O(\sqrt{n})$. Ta cần hai mảng khối $b$ và $c$: một mảng theo dõi các cập nhật phần tử và một mảng theo dõi đáp án truy vấn.

Còn nhiều bài toán khác có thể giải bằng chia căn. Ví dụ, với bài toán duy trì một tập số hỗ trợ thêm/xóa số, kiểm tra một số có thuộc tập hay không và tìm số lớn thứ $k$, ta có thể lưu các số theo thứ tự tăng dần rồi chia thành nhiều khối, mỗi khối chứa khoảng $\sqrt{n}$ số. Mỗi khi thêm hoặc xóa một số, các khối phải được cân bằng lại bằng cách chuyển phần tử giữa đầu và cuối của các khối kề nhau.

## Thuật toán Mo

Một ý tưởng tương tự dựa trên chia căn có thể được dùng để trả lời các truy vấn đoạn ($Q$) theo kiểu offline trong $O((N+Q)\sqrt{N})$.
Thoạt nhìn điều này có vẻ tệ hơn nhiều so với các phương pháp ở phần trước, vì độ phức tạp hơi kém hơn và không thể cập nhật giá trị giữa hai truy vấn.
Nhưng trong nhiều tình huống, phương pháp này có những ưu điểm riêng.
Với chia căn thông thường, ta phải tính trước đáp án cho từng khối rồi ghép chúng khi trả lời truy vấn.
Trong một số bài, bước ghép này lại rất khó.
Chẳng hạn, mỗi truy vấn yêu cầu tìm **mode** của đoạn (giá trị xuất hiện nhiều nhất).
Khi đó mỗi khối phải lưu số lần xuất hiện của từng giá trị trong một cấu trúc dữ liệu nào đó, và ta không còn ghép các khối đủ nhanh được nữa.
**Thuật toán Mo** dùng một cách tiếp cận hoàn toàn khác. Nó có thể trả lời loại truy vấn này nhanh vì chỉ duy trì một cấu trúc dữ liệu duy nhất, với các thao tác trên cấu trúc đó đều đơn giản và nhanh.

Ý tưởng là trả lời các truy vấn theo một thứ tự đặc biệt dựa trên chỉ số.
Trước tiên ta trả lời mọi truy vấn có chỉ số trái thuộc khối 0, sau đó mọi truy vấn có chỉ số trái thuộc khối 1, và cứ tiếp tục như vậy.
Trong mỗi khối, ta cũng trả lời truy vấn theo một thứ tự đặc biệt: sắp xếp theo chỉ số phải của truy vấn.

Như đã nói, ta chỉ dùng một cấu trúc dữ liệu.
Cấu trúc này lưu thông tin về đoạn hiện tại.
Ban đầu đoạn này rỗng.
Khi muốn trả lời truy vấn tiếp theo theo thứ tự đặc biệt, ta chỉ cần mở rộng hoặc thu hẹp đoạn hiện tại bằng cách thêm/xóa các phần tử ở hai đầu cho đến khi biến nó thành đoạn của truy vấn.
Nhờ vậy, mỗi bước ta chỉ thêm hoặc xóa một phần tử, vốn thường là các thao tác khá dễ trên cấu trúc dữ liệu.

Vì thay đổi thứ tự trả lời truy vấn, cách làm này chỉ dùng được khi ta được phép trả lời các truy vấn theo chế độ offline.

### Cài đặt

Trong thuật toán Mo, ta dùng hai hàm để thêm một chỉ số vào và xóa một chỉ số khỏi đoạn đang duy trì.

```cpp
void remove(idx);  // TODO: remove value at idx from data structure
void add(idx);     // TODO: add value at idx from data structure
int get_answer();  // TODO: extract the current answer of the data structure

int block_size;

struct Query {
    int l, r, idx;
    bool operator<(Query other) const
    {
        return make_pair(l / block_size, r) <
               make_pair(other.l / block_size, other.r);
    }
};

vector<int> mo_s_algorithm(vector<Query> queries) {
    vector<int> answers(queries.size());
    sort(queries.begin(), queries.end());

    // TODO: initialize data structure

    int cur_l = 0;
    int cur_r = -1;
    // invariant: data structure will always reflect the range [cur_l, cur_r]
    for (Query q : queries) {
        while (cur_l > q.l) {
            cur_l--;
            add(cur_l);
        }
        while (cur_r < q.r) {
            cur_r++;
            add(cur_r);
        }
        while (cur_l < q.l) {
            remove(cur_l);
            cur_l++;
        }
        while (cur_r > q.r) {
            remove(cur_r);
            cur_r--;
        }
        answers[q.idx] = get_answer();
    }
    return answers;
}
```

Tùy bài toán, ta có thể dùng một cấu trúc dữ liệu khác và sửa các hàm `add`/`remove`/`get_answer` tương ứng.
Ví dụ, nếu đề yêu cầu truy vấn tổng trên đoạn thì cấu trúc dữ liệu chỉ cần là một số nguyên đơn giản, ban đầu bằng $0$.
Hàm `add` chỉ cần cộng giá trị ở vị trí tương ứng và cập nhật biến đáp án.
Ngược lại, hàm `remove` trừ giá trị ở vị trí đó rồi cập nhật biến đáp án.
Còn `get_answer` chỉ trả về số nguyên này.

Để trả lời truy vấn mode, ta có thể dùng một cây tìm kiếm nhị phân (ví dụ `map<int, int>`) để lưu số lần xuất hiện của mỗi số trong đoạn hiện tại, và một cây tìm kiếm nhị phân thứ hai (ví dụ `set<pair<int, int>>`) để duy trì số lần xuất hiện của các giá trị theo thứ tự (chẳng hạn dưới dạng cặp số-lần xuất hiện).
Phương thức `add` xóa số hiện tại khỏi cây thứ hai, tăng số đếm trong cây thứ nhất rồi chèn số trở lại cây thứ hai.
`remove` làm tương tự nhưng giảm số đếm.
Còn `get_answer` chỉ nhìn vào cây thứ hai và trả về giá trị tốt nhất trong $O(1)$.

### Độ phức tạp

Sắp xếp mọi truy vấn mất $O(Q \log Q)$.

Còn các thao tác khác thì sao?
Các hàm `add` và `remove` sẽ được gọi bao nhiêu lần?

Gọi kích thước khối là $S$.

Nếu chỉ xét mọi truy vấn có chỉ số trái thuộc cùng một khối, các truy vấn được sắp theo chỉ số phải.
Vì vậy ta chỉ gọi `add(cur_r)` và `remove(cur_r)` tổng cộng $O(N)$ lần cho tất cả truy vấn này.
Suy ra có $O(\frac{N}{S} N)$ lần gọi trên mọi khối.

Giá trị `cur_l` thay đổi nhiều nhất $O(S)$ giữa hai truy vấn.
Vì vậy ta có thêm $O(S Q)$ lần gọi `add(cur_l)` và `remove(cur_l)`.

Với $S \approx \sqrt{N}$, tổng cộng có $O((N + Q) \sqrt{N})$ thao tác.
Do đó độ phức tạp là $O((N+Q)F\sqrt{N})$, trong đó $O(F)$ là độ phức tạp của hàm `add` và `remove`.

### Mẹo cải thiện thời gian chạy

* Kích thước khối chính xác bằng $\sqrt{N}$ không phải lúc nào cũng cho thời gian chạy tốt nhất. Ví dụ, nếu $\sqrt{N}=750$ thì kích thước khối $700$ hoặc $800$ đôi khi có thể chạy nhanh hơn.
Quan trọng hơn, đừng tính kích thước khối lúc chạy chương trình — hãy đặt nó thành `const`. Phép chia cho hằng số được compiler tối ưu rất tốt.
* Ở các khối lẻ, sắp xếp chỉ số phải theo thứ tự tăng dần; ở các khối chẵn, sắp xếp theo thứ tự giảm dần. Cách này giảm chuyển động của con trỏ phải, vì cách sắp xếp thông thường khiến con trỏ phải phải quay từ cuối về đầu khi bắt đầu mỗi khối. Với cách cải tiến, không còn cần bước đặt lại này.

```cpp
bool cmp(pair<int, int> p, pair<int, int> q) {
    if (p.first / BLOCK_SIZE != q.first / BLOCK_SIZE)
        return p < q;
    return (p.first / BLOCK_SIZE & 1) ? (p.second < q.second) : (p.second > q.second);
}
```

Bạn có thể đọc về một cách sắp xếp còn nhanh hơn [tại đây](https://codeforces.com/blog/entry/61203).

## Bài tập luyện tập

* [Codeforces - Kuriyama Mirai's Stones](https://codeforces.com/problemset/problem/433/B)
* [Codeforces - Another Problem about Beautiful Pairs](https://codeforces.com/contest/2197/problem/D)
* [UVA - 12003 - Array Transformer](https://uva.onlinejudge.org/index.php?option=com_onlinejudge&Itemid=8&page=show_problem&problem=3154)
* [UVA - 11990 Dynamic Inversion](https://uva.onlinejudge.org/index.php?option=com_onlinejudge&Itemid=8&page=show_problem&problem=3141)
* [SPOJ - Give Away](http://www.spoj.com/problems/GIVEAWAY/)
* [Codeforces - Till I Collapse](http://codeforces.com/contest/786/problem/C)
* [Codeforces - Destiny](http://codeforces.com/contest/840/problem/D)
* [Codeforces - Holes](http://codeforces.com/contest/13/problem/E)
* [Codeforces - XOR and Favorite Number](https://codeforces.com/problemset/problem/617/E)
* [Codeforces - Powerful array](http://codeforces.com/problemset/problem/86/D)
* [SPOJ - DQUERY](https://www.spoj.com/problems/DQUERY)
* [Codeforces - Robin Hood Archery](https://codeforces.com/contest/2014/problem/H)