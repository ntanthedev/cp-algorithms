---
tags:
  - Translated
e_maxx_link: burnside_polya
translation:
  source: combinatorics/burnside.md
  source_commit: 6df2bd19f28ca46f3f99ec3532db6992bd206b71
  status: draft
  last_synced: 2026-11-16
---

# Bổ đề Burnside / Định lý đếm Pólya

## Bổ đề Burnside

**Bổ đề Burnside** được **Burnside** phát biểu và chứng minh năm 1897, nhưng trước đó đã được **Frobenius** phát hiện năm 1887 và thậm chí sớm hơn bởi **Cauchy** năm 1845.
Vì vậy, đôi khi bổ đề còn được gọi là **bổ đề Cauchy-Frobenius**.

Bổ đề Burnside cho phép đếm số lớp tương đương trong các tập hợp dựa trên tính đối xứng nội tại.

### Đối tượng và biểu diễn

Ta cần phân biệt rõ số đối tượng và số biểu diễn.

Các biểu diễn khác nhau có thể tương ứng với cùng một đối tượng, nhưng mỗi biểu diễn chỉ tương ứng với đúng một đối tượng.
Do đó tập mọi biểu diễn được chia thành các lớp tương đương.
Nhiệm vụ là tính số đối tượng, hay tương đương là số lớp tương đương.
Ví dụ sau làm rõ sự khác biệt giữa đối tượng và biểu diễn.

### Ví dụ: tô màu cây nhị phân

Giả sử ta có bài toán sau.
Cần đếm số cách tô hai màu cho cây nhị phân có gốc gồm $n$ đỉnh, trong đó tại mỗi đỉnh ta không phân biệt con trái và con phải.

Ở đây tập đối tượng là tập các cách tô màu cây khác nhau.

Bây giờ ta định nghĩa tập biểu diễn.
Một biểu diễn của cách tô màu là hàm $f(v)$ gán cho mỗi đỉnh một màu (ở đây dùng các màu $0$ và $1$).
Tập biểu diễn gồm mọi hàm có thể có thuộc loại này và hiển nhiên có kích thước bằng $2^n$.

Đồng thời ta phân hoạch tập này thành các lớp tương đương.

Chẳng hạn, giả sử $n = 3$, cây gồm gốc $1$ và hai con $2$ và $3$.
Khi đó các hàm $f_1$ và $f_2$ sau được coi là tương đương.

$$\begin{array}{ll}
f_1(1) = 0 & f_2(1) = 0\\
f_1(2) = 1 & f_2(2) = 0\\
f_1(3) = 0 & f_2(3) = 1
\end{array}$$

### Các hoán vị bất biến

Vì sao hai hàm $f_1$ và $f_2$ này thuộc cùng một lớp tương đương?
Trực quan, ta có thể đổi chỗ các con $2$ và $3$ của đỉnh $1$; sau phép biến đổi đó, hàm $f_1$ trùng với $f_2$.

Một cách hình thức, điều đó có nghĩa là tồn tại **hoán vị bất biến** $\pi$ (tức hoán vị không làm thay đổi bản thân đối tượng mà chỉ thay đổi biểu diễn), sao cho:

$$f_2 \pi \equiv f_1$$

Vì vậy, từ định nghĩa đối tượng, ta có thể tìm mọi hoán vị bất biến, tức các hoán vị không làm đổi đối tượng khi áp dụng vào biểu diễn.
Sau đó có thể kiểm tra hai hàm $f_1$ và $f_2$ có tương đương hay không (tức có cùng ứng với một đối tượng hay không) bằng cách kiểm tra điều kiện $f_2 \pi \equiv f_1$ với từng hoán vị bất biến (hoặc tương đương là $f_1 \pi \equiv f_2$).
Nếu có ít nhất một hoán vị thỏa mãn điều kiện, $f_1$ và $f_2$ tương đương; nếu không, chúng không tương đương.

Tìm tất cả các hoán vị bất biến theo định nghĩa đối tượng là bước then chốt khi áp dụng cả bổ đề Burnside lẫn định lý đếm Pólya.
Rõ ràng các hoán vị này phụ thuộc vào bài toán cụ thể và việc tìm chúng hoàn toàn mang tính heuristic dựa trên trực giác.
Tuy nhiên, trong phần lớn trường hợp chỉ cần tìm thủ công vài hoán vị "cơ bản" có thể sinh ra mọi hoán vị còn lại (phần việc này có thể giao cho máy tính).

Không khó để thấy các hoán vị bất biến tạo thành một **nhóm**, vì tích (hợp thành) của các hoán vị bất biến vẫn là một hoán vị bất biến.
Ta ký hiệu **nhóm các hoán vị bất biến** là $G$.

### Phát biểu bổ đề

Để phát biểu bổ đề, ta cần thêm một định nghĩa đại số.
Một **điểm bất động** $f$ của hoán vị $\pi$ là phần tử không đổi dưới hoán vị đó: $f \equiv f \pi$.
Chẳng hạn, trong ví dụ này, các điểm bất động là các hàm $f$ tương ứng với cách tô màu không thay đổi khi áp dụng hoán vị $\pi$ (tức không thay đổi theo nghĩa hình thức của đẳng thức giữa các hàm).
Gọi $I(\pi)$ là **số điểm bất động** của hoán vị $\pi$.

Khi đó **bổ đề Burnside** phát biểu:
Số lớp tương đương bằng tổng số điểm bất động tương ứng với mọi hoán vị trong nhóm $G$, chia cho kích thước của nhóm:

$$|\text{Classes}| = \frac{1}{|G|} \sum_{\pi \in G} I(\pi)$$

Dù bản thân bổ đề Burnside không thật thuận tiện để dùng trong thực tế (chưa rõ cách nhanh chóng tìm giá trị $I(\pi)$), nó thể hiện rõ nhất bản chất toán học làm nền tảng cho ý tưởng đếm các lớp tương đương.

### Chứng minh bổ đề Burnside

Chứng minh bổ đề Burnside dưới đây không quan trọng đối với ứng dụng thực tế, nên có thể bỏ qua khi đọc lần đầu.

Đây là chứng minh đơn giản nhất đã biết và không dùng lý thuyết nhóm.
Chứng minh được Kenneth P. Bogart công bố năm 1991.

Ta cần chứng minh đẳng thức sau:

$$|\text{Classes}| \cdot |G| = \sum_{\pi \in G} I(\pi)$$

Vế phải chính là số "cặp bất biến" $(f, \pi)$, tức các cặp thỏa mãn $f \pi \equiv f$.
Rõ ràng ta có thể đổi thứ tự tính tổng.
Cho tổng chạy qua mọi phần tử $f$ và cộng các giá trị $J(f)$ — số hoán vị nhận $f$ làm điểm bất động.

$$|\text{Classes}| \cdot |G| = \sum_{f} J(f)$$

Để chứng minh công thức này, ta lập một bảng có các cột gắn nhãn bằng mọi hàm $f_i$ và các hàng gắn nhãn bằng mọi hoán vị $\pi_j$.
Điền vào các ô giá trị $f_i \pi_j$.
Nếu xem các cột là tập hợp, một số cột sẽ trùng nhau; khi đó các hàm $f$ tương ứng với chúng cũng tương đương.
Vì vậy, số cột khác nhau (xét như tập hợp) bằng số lớp.
Theo lý thuyết nhóm, cột gắn nhãn $f_i$ là quỹ đạo của phần tử này.
Các phần tử tương đương có cùng quỹ đạo, và số quỹ đạo chính là số lớp.

Như vậy các cột của bảng được chia thành các lớp tương đương.
Xét một lớp và các cột thuộc lớp đó.
Trước hết, các cột này chỉ có thể chứa các phần tử $f_i$ của lớp tương đương đó (nếu không, một hoán vị $\pi_j$ đã chuyển một hàm sang lớp khác, điều không thể vì ta chỉ xét hoán vị bất biến).
Thứ hai, mỗi phần tử $f_i$ xuất hiện cùng số lần trong mỗi cột (điều này cũng suy ra từ việc các cột tương ứng với những phần tử tương đương).
Từ đó suy ra mọi cột trong cùng một lớp tương đương trùng nhau khi xét như đa tập.

Bây giờ cố định một phần tử tùy ý $f$.
Một mặt, theo định nghĩa, nó xuất hiện đúng $J(f)$ lần trong cột của mình.
Mặt khác, mọi cột trong cùng lớp tương đương đều giống nhau khi xét là đa tập.
Vì vậy, trong mỗi cột của một lớp tương đương, mọi phần tử $g$ đều xuất hiện đúng $J(g)$ lần.

Do đó, nếu chọn tùy ý một cột từ mỗi lớp tương đương rồi cộng số phần tử trong các cột đó, một mặt ta được $|\text{Classes}| \cdot |G|$ (bằng cách nhân số cột với số hàng), mặt khác được tổng các giá trị $J(f)$ cho mọi $f$ (theo các lập luận trên):

$$|\text{Classes}| \cdot |G| = \sum_{f} J(f)$$

## Định lý đếm Pólya

Định lý đếm Pólya tổng quát hóa bổ đề Burnside, đồng thời cung cấp công cụ thuận tiện hơn để tìm số lớp tương đương.
Định lý này đã được Redfield phát hiện trước Pólya vào năm 1927, nhưng công trình của ông không được các nhà toán học chú ý.
Pólya độc lập tìm ra cùng kết quả năm 1937 và công trình của ông được đón nhận hơn.

Ở đây ta chỉ xét một trường hợp riêng của định lý đếm Pólya rất hữu ích trong thực tế.
Ta không bàn về công thức tổng quát của định lý.

Gọi $C(\pi)$ là số chu trình trong hoán vị $\pi$.
Khi đó có công thức sau (một **trường hợp riêng của định lý đếm Pólya**):

$$|\text{Classes}| = \frac{1}{|G|} \sum_{\pi \in G} k^{C(\pi)}$$

$k$ là số giá trị mà mỗi phần tử trong biểu diễn có thể nhận; với bài toán tô màu cây nhị phân, giá trị này là $k = 2$.

### Chứng minh

Công thức này là hệ quả trực tiếp của bổ đề Burnside.
Ta chỉ cần tìm biểu thức tường minh cho $I(\pi)$ xuất hiện trong bổ đề.
Nhắc lại rằng $I(\pi)$ là số điểm bất động của hoán vị $\pi$.

Xét một hoán vị $\pi$ và một phần tử $f$.
Khi áp dụng $\pi$, các thành phần trong $f$ dịch chuyển theo các chu trình của hoán vị.
Để kết quả thỏa mãn $f \equiv f \pi$, các thành phần thuộc cùng một chu trình phải bằng nhau.
Đồng thời, các chu trình khác nhau độc lập với nhau.
Vì vậy, với mỗi chu trình của hoán vị $\pi$, ta có thể chọn một giá trị (trong $k$ giá trị có thể), từ đó có số điểm bất động:

$$I(\pi) = k^{C(\pi)}$$

## Ứng dụng: Tô màu vòng cổ

Bài toán "Necklace" là một bài toán tổ hợp kinh điển.
Yêu cầu là đếm số vòng cổ khác nhau gồm $n$ hạt, mỗi hạt được tô một trong $k$ màu.
Khi so sánh hai vòng cổ, được phép xoay nhưng không được lật ngược (tức là cho phép dịch vòng).

Trong bài toán này ta có thể tìm ngay nhóm các hoán vị bất biến:

$$\begin{align}
\pi_0 &= 1 2 3 \dots n\\
\pi_1 &= 2 3 \dots n 1\\
\pi_2 &= 3 \dots n 12\\
&\dots\\
\pi_{n-1} &= n 1 2 3\dots\end{align}$$

Ta tìm công thức tường minh tính $C(\pi_i)$.
Trước hết, hoán vị $\pi_i$ có giá trị $i + j$ ở vị trí thứ $j$ (lấy theo modulo $n$).
Xét cấu trúc chu trình của $\pi_i$.
Ta thấy $1$ chuyển thành $1 + i$, $1 + i$ chuyển thành $1 + 2i$, rồi thành $1 + 3i$, v.v. cho đến khi gặp số dạng $1 + k n$.
Các phần tử còn lại cũng tương tự.
Vì vậy mọi chu trình có cùng độ dài, cụ thể là $\frac{\text{lcm}(i, n)}{i} = \frac{n}{\gcd(i, n)}$.
Do đó số chu trình trong $\pi_i$ bằng $\gcd(i, n)$.

Thay các giá trị này vào định lý đếm Pólya, ta được lời giải:

$$\frac{1}{n} \sum_{i=1}^n k^{\gcd(i, n)}$$

Có thể giữ nguyên công thức này hoặc rút gọn thêm.
Hãy đổi cách tính tổng để duyệt mọi ước của $n$.
Trong tổng ban đầu có nhiều số hạng tương đương: nếu $i$ không là ước của $n$, ta tìm được một ước như vậy sau khi tính $\gcd(i, n)$.
Do đó, với mỗi ước $d ~|~ n$, số hạng $k^{\gcd(d, n)} = k^d$ xuất hiện trong tổng nhiều lần; ta có thể viết lại đáp án là

$$\frac{1}{n} \sum_{d ~|~ n} C_d k^d,$$

trong đó $C_d$ là số giá trị $i$ thỏa mãn $\gcd(i, n) = d$.
Ta có thể tìm biểu thức tường minh cho giá trị này.
Mỗi số $i$ như vậy có dạng $i = d j$ với $\gcd(j, n / d) = 1$ (nếu không thì $\gcd(i, n) > d$).
Vì vậy ta có thể đếm số $j$ có tính chất này.
[Hàm phi Euler](../algebra/phi-function.md) cho kết quả $C_d = \phi(n / d)$, do đó ta được đáp án:

$$\frac{1}{n} \sum_{d ~|~ n} \phi\left(\frac{n}{d}\right) k^d$$

## Ứng dụng: Tô màu mặt xuyến

Nhiều khi ta không thể tìm được công thức tường minh cho số lớp tương đương.
Trong nhiều bài toán, số hoán vị của một nhóm có thể quá lớn để tính bằng tay và không thể tính giải tích số chu trình của chúng.

Khi đó, ta nên tìm thủ công vài hoán vị "cơ bản" có thể sinh toàn bộ nhóm $G$.
Sau đó viết chương trình sinh mọi hoán vị trong nhóm $G$, đếm số chu trình và tính đáp án bằng công thức.

Xét ví dụ bài toán tô màu mặt xuyến.
Cho một tờ giấy kẻ ô $n \times m$ ($n < m$), trong đó một số ô màu đen.
Dán hai cạnh dài $m$ với nhau để thu được hình trụ.
Sau đó dán hai đường tròn trên và dưới của hình trụ với nhau mà không xoắn để tạo thành mặt xuyến.
Yêu cầu tính số mặt xuyến tô màu khác nhau, giả sử không nhìn thấy các đường dán và có thể xoay mặt xuyến.

Ta lại bắt đầu với tờ giấy $n \times m$.
Dễ thấy các phép biến đổi sau bảo toàn lớp tương đương:
dịch vòng các hàng, dịch vòng các cột và xoay tờ giấy 180 độ.
Các phép biến đổi này cũng có thể sinh toàn bộ nhóm phép biến đổi bất biến.
Nếu đánh số các ô giấy theo cách nào đó, ta có thể viết ba hoán vị $p_1$, $p_2$, $p_3$ tương ứng với các loại biến đổi này.

Tiếp theo chỉ cần sinh mọi hoán vị thu được dưới dạng tích.
Mọi hoán vị đó đều có dạng $p_1^{i_1} p_2^{i_2} p_3^{i_3}$ với $i_1 = 0 \dots m-1$, $i_2 = 0 \dots n-1$, $i_3 = 0 \dots 1$.

Từ đó ta có thể cài đặt lời giải cho bài toán.

```{.cpp file=burnside_tori}
using Permutation = vector<int>;

void operator*=(Permutation& p, Permutation const& q) {
    Permutation copy = p;
    for (int i = 0; i < p.size(); i++)
        p[i] = copy[q[i]];
}

int count_cycles(Permutation p) {
    int cnt = 0;
    for (int i = 0; i < p.size(); i++) {
        if (p[i] != -1) {
            cnt++;
            for (int j = i; p[j] != -1;) {
                int next = p[j];
                p[j] = -1;
                j = next;
            }
        }
    }
    return cnt;
}

int solve(int n, int m) {
    Permutation p(n*m), p1(n*m), p2(n*m), p3(n*m);
    for (int i = 0; i < n*m; i++) {
        p[i] = i;
        p1[i] = (i % n + 1) % n + i / n * n;
        p2[i] = (i / n + 1) % m * n + i % n;
        p3[i] = (m - 1 - i / n) * n + (n - 1 - i % n);
    }

    set<Permutation> s;
    for (int i1 = 0; i1 < n; i1++) {
        for (int i2 = 0; i2 < m; i2++) {
            for (int i3 = 0; i3 < 2; i3++) {
                s.insert(p);
                p *= p3;
            }
            p *= p2;
        }
        p *= p1;
    }

    int sum = 0;
    for (Permutation const& p : s) {
        sum += 1 << count_cycles(p);
    }
    return sum / s.size();
}
```

**Ghi chú bản dịch:** Công thức độ dài chu trình có phép chia cho chỉ số phép xoay nên không xác định với phép xoay không dịch; trường hợp này có n chu trình, mỗi chu trình dài 1. Ở ví dụ mặt xuyến, phạm vi số mũ của hai phép dịch trong bài gốc bị đổi chỗ so với mã: phép dịch thứ nhất có chu kỳ n, phép thứ hai có chu kỳ m. Ngoài ra, phép dịch bit và biến tổng kiểu số nguyên trong mã có thể tràn khi số ô lớn; chẳng hạn hoán vị đồng nhất trên lưới 4 nhân 8 có 32 chu trình.

## Bài tập luyện tập
* [CSES - Counting Necklaces](https://cses.fi/problemset/task/2209)
* [CSES - Counting Grids](https://cses.fi/problemset/task/2210)
* [Codeforces - Buildings](https://codeforces.com/gym/101873/problem/B)
* [CS Academy - Cube Coloring](https://csacademy.com/contest/beta-round-8/task/cube-coloring/)
* [Codeforces - Side Transmutations](https://codeforces.com/contest/1065/problem/E)
* [LightOJ - Necklace](https://vjudge.net/problem/LightOJ-1419)
* [POJ - Necklace of Beads](http://poj.org/problem?id=1286)
* [CodeChef - Lucy and Flowers](https://www.codechef.com/problems/DECORATE)
* [HackerRank - Count the Necklaces](https://www.hackerrank.com/contests/infinitum12/challenges/count-the-necklaces)
* [POJ - Magic Bracelet](http://poj.org/problem?id=2888)
* [SPOJ - Sorting Machine](https://www.spoj.com/problems/SRTMACH/)
* [Project Euler - Pizza Toppings](https://projecteuler.net/problem=281)
* [ICPC 2011 SERCP - Alphabet Soup](https://basecamp.eolymp.com/tr/problems/3064)
* [GCPC 2017 - Buildings](https://basecamp.eolymp.com/en/problems/11615)
