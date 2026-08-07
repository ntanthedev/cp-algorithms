---
tags:
  - Translated
e_maxx_link: suffix_array
translation:
  source: string/suffix-array.md
  source_commit: 035f4625a03563c7b2b262b8dc25b1ca5d7146e0
  status: draft
  last_synced: 2026-08-07
---

# Mảng hậu tố (Suffix Array)

## Định nghĩa

Cho $s$ là một xâu có độ dài $n$. Hậu tố thứ $i$ của $s$ là xâu con $s[i \ldots n - 1]$.

Một **mảng hậu tố** chứa các số nguyên biểu diễn **chỉ số bắt đầu** của tất cả hậu tố của một xâu, sau khi các hậu tố đó được sắp xếp.

Ví dụ, xét xâu $s = abaab$.
Tất cả các hậu tố là

$$\begin{array}{ll}
0. & abaab \\
1. & baab \\
2. & aab \\
3. & ab \\
4. & b
\end{array}$$

Sau khi sắp xếp các xâu này:

$$\begin{array}{ll}
2. & aab \\
3. & ab \\
0. & abaab \\
4. & b \\
1. & baab
\end{array}$$

Vì vậy, mảng hậu tố của $s$ là $(2,~ 3,~ 0,~ 4,~ 1)$.

Với vai trò một cấu trúc dữ liệu, mảng hậu tố được sử dụng rộng rãi trong các lĩnh vực như nén dữ liệu, tin sinh học và nói chung là mọi lĩnh vực liên quan đến xâu và các bài toán so khớp chuỗi.

## Xây dựng

### Cách $O(n^2 \log n)$ {data-toc-label="O(n^2 log n) approach"}

Đây là cách ngây thơ nhất.
Ta lấy tất cả hậu tố rồi sắp xếp chúng bằng quicksort hoặc mergesort, đồng thời giữ lại chỉ số ban đầu của từng hậu tố.
Việc sắp xếp cần $O(n \log n)$ phép so sánh, và vì mỗi lần so sánh hai xâu còn tốn thêm $O(n)$ thời gian, độ phức tạp cuối cùng là $O(n^2 \log n)$.

### Cách $O(n \log n)$ {data-toc-label="O(n log n) approach"}

Nói chính xác thì thuật toán sau không sắp xếp các hậu tố, mà sắp xếp các phép dịch vòng của một xâu.
Tuy nhiên, ta có thể rất dễ suy ra thuật toán sắp xếp hậu tố từ đó:
chỉ cần thêm vào cuối xâu một ký tự tùy ý nhỏ hơn mọi ký tự có trong xâu.
Thông thường ta dùng ký hiệu \$.
Khi đó thứ tự của các phép dịch vòng đã sắp xếp tương đương với thứ tự của các hậu tố đã sắp xếp, như ví dụ sau với xâu $dabbb$.

$$\begin{array}{lll}
1. & abbb\$d & abbb \\
4. & b\$dabb & b \\
3. & bb\$dab & bb \\
2. & bbb\$da & bbb \\
0. & dabbb\$ & dabbb
\end{array}$$

Vì ta sẽ sắp xếp các phép dịch vòng, ta xét các **xâu con vòng**.
Ta vẫn dùng ký hiệu $s[i \dots j]$ cho xâu con của $s$ ngay cả khi $i > j$.
Trong trường hợp này, ta thực sự muốn nói tới xâu $s[i \dots n-1] + s[0 \dots j]$.
Ngoài ra, mọi chỉ số đều được lấy theo modulo độ dài của $s$, và để đơn giản ta sẽ lược bỏ phép modulo trong phần trình bày.

Thuật toán sẽ thực hiện $\lceil \log n \rceil + 1$ vòng lặp.
Ở vòng thứ $k$ ($k = 0 \dots \lceil \log n \rceil$), ta sắp xếp $n$ xâu con vòng của $s$ có độ dài $2^k$.
Sau vòng thứ $\lceil \log n \rceil$, các xâu con có độ dài $2^{\lceil \log n \rceil} \ge n$ đã được sắp xếp, nên điều này tương đương với việc sắp xếp toàn bộ các phép dịch vòng.

Trong mỗi vòng lặp, ngoài hoán vị $p[0 \dots n-1]$, trong đó $p[i]$ là chỉ số bắt đầu của xâu con đứng thứ $i$ trong thứ tự đã sắp xếp (xâu con có độ dài $2^k$), ta còn duy trì mảng $c[0 \dots n-1]$, trong đó $c[i]$ biểu diễn **lớp tương đương** của xâu con bắt đầu tại $i$.
Ta cần điều này vì một số xâu con có thể giống nhau và thuật toán phải xử lý chúng như nhau.
Để thuận tiện, các lớp được đánh số từ 0.
Ngoài ra, các giá trị $c[i]$ được gán sao cho vẫn bảo toàn thông tin về thứ tự:
nếu một xâu con nhỏ hơn xâu con khác thì nhãn lớp của nó cũng phải nhỏ hơn.
Số lớp tương đương được lưu trong biến $\text{classes}$.

Xét ví dụ sau.
Cho xâu $s = aaba$.
Các xâu con vòng cùng các mảng $p[]$ và $c[]$ tương ứng ở từng vòng là:

$$\begin{array}{cccc}
0: & (a,~ a,~ b,~ a) & p = (0,~ 1,~ 3,~ 2) & c = (0,~ 0,~ 1,~ 0)\\
1: & (aa,~ ab,~ ba,~ aa) & p = (0,~ 3,~ 1,~ 2) & c = (0,~ 1,~ 2,~ 0)\\
2: & (aaba,~ abaa,~ baaa,~ aaab) & p = (3,~ 0,~ 1,~ 2) & c = (1,~ 2,~ 3,~ 0)\\
\end{array}$$

Cần lưu ý rằng các giá trị của $p[]$ có thể khác nhau.
Ví dụ, ở vòng thứ $0$, mảng cũng có thể là $p = (3,~ 1,~ 0,~ 2)$ hoặc $p = (3,~ 0,~ 1,~ 2)$.
Mọi phương án này đều đưa các xâu con vào thứ tự đã sắp xếp, nên đều hợp lệ.
Trong khi đó, mảng $c[]$ là cố định và không có sự mơ hồ nào.

Bây giờ ta tập trung vào phần cài đặt.
Ta sẽ viết một hàm nhận xâu $s$ và trả về hoán vị của các phép dịch vòng đã sắp xếp.

```{.cpp file=suffix_array_sort_cyclic1}
vector<int> sort_cyclic_shifts(string const& s) {
    int n = s.size();
    const int alphabet = 256;
```

Ban đầu, ở **vòng thứ $0$**, ta phải sắp xếp các xâu con vòng có độ dài $1$, tức là sắp xếp toàn bộ ký tự của xâu và chia chúng thành các lớp tương đương (các ký tự giống nhau được gán cùng một lớp).
Ta có thể làm việc này trực tiếp, chẳng hạn bằng **sắp xếp đếm (counting sort)**.
Với mỗi ký tự, ta đếm số lần nó xuất hiện trong xâu rồi dùng thông tin đó để xây dựng mảng $p[]$.
Sau đó ta duyệt mảng $p[]$ và xây dựng $c[]$ bằng cách so sánh các ký tự kề nhau.

```{.cpp file=suffix_array_sort_cyclic2}
    vector<int> p(n), c(n), cnt(max(alphabet, n), 0);
    for (int i = 0; i < n; i++)
        cnt[s[i]]++;
    for (int i = 1; i < alphabet; i++)
        cnt[i] += cnt[i-1];
    for (int i = 0; i < n; i++)
        p[--cnt[s[i]]] = i;
    c[p[0]] = 0;
    int classes = 1;
    for (int i = 1; i < n; i++) {
        if (s[p[i]] != s[p[i-1]])
            classes++;
        c[p[i]] = classes - 1;
    }
```

Tiếp theo là bước chuyển giữa các vòng.
Giả sử ta đã hoàn thành bước thứ $k-1$ và tính được các mảng $p[]$ và $c[]$ tương ứng.
Ta muốn tính các giá trị cho bước thứ $k$ trong $O(n)$ thời gian.
Vì bước này được thực hiện $O(\log n)$ lần, toàn bộ thuật toán sẽ có độ phức tạp thời gian $O(n \log n)$.

Để làm vậy, nhận thấy một xâu con vòng có độ dài $2^k$ gồm hai xâu con độ dài $2^{k-1}$, và ta có thể so sánh hai nửa này trong $O(1)$ nhờ thông tin từ pha trước — các lớp tương đương $c[]$.
Do đó, với hai xâu con độ dài $2^k$ bắt đầu tại $i$ và $j$, toàn bộ thông tin cần thiết để so sánh chúng nằm trong hai cặp $(c[i],~ c[i + 2^{k-1}])$ và $(c[j],~ c[j + 2^{k-1}])$.

$$\dots
\overbrace{
\underbrace{s_i \dots s_{i+2^{k-1}-1}}_{\text{length} = 2^{k-1},~ \text{class} = c[i]}
\quad
\underbrace{s_{i+2^{k-1}} \dots s_{i+2^k-1}}_{\text{length} = 2^{k-1},~ \text{class} = c[i + 2^{k-1}]}
}^{\text{length} = 2^k}
\dots
\overbrace{
\underbrace{s_j \dots s_{j+2^{k-1}-1}}_{\text{length} = 2^{k-1},~ \text{class} = c[j]}
\quad
\underbrace{s_{j+2^{k-1}} \dots s_{j+2^k-1}}_{\text{length} = 2^{k-1},~ \text{class} = c[j + 2^{k-1}]}
}^{\text{length} = 2^k}
\dots
$$

Điều này cho ta một lời giải rất đơn giản:
**sắp xếp** các xâu con độ dài $2^k$ **theo các cặp số này**.
Kết quả chính là thứ tự $p[]$ cần tìm.
Tuy nhiên, một phép sắp xếp thông thường chạy trong $O(n \log n)$, điều mà ta chưa thỏa mãn.
Cách này chỉ cho thuật toán xây dựng mảng hậu tố trong $O(n \log^2 n)$ thời gian.

Làm thế nào để sắp xếp nhanh các cặp này?
Vì mỗi phần tử trong cặp không vượt quá $n$, ta có thể tiếp tục dùng sắp xếp đếm.
Tuy nhiên, sắp xếp trực tiếp các cặp bằng counting sort không phải cách hiệu quả nhất.
Để có hằng số ẩn tốt hơn, ta dùng một mẹo khác.

Ta dùng kỹ thuật nền tảng của **sắp xếp cơ số (radix sort)**: trước tiên sắp các cặp theo phần tử thứ hai, sau đó theo phần tử thứ nhất bằng một phép sắp xếp ổn định, tức không phá vỡ thứ tự tương đối của các phần tử bằng nhau.
Nhưng các phần tử thứ hai thực ra đã được sắp xếp ở vòng trước.
Vì vậy, để sắp các cặp theo phần tử thứ hai, ta chỉ cần trừ $2^{k-1}$ khỏi các chỉ số trong $p[]$ (ví dụ, nếu xâu con nhỏ nhất có độ dài $2^{k-1}$ bắt đầu tại $i$, thì xâu con độ dài $2^k$ có nửa sau nhỏ nhất bắt đầu tại $i - 2^{k-1}$).

Như vậy, chỉ bằng các phép trừ đơn giản ta đã sắp được các phần tử thứ hai của các cặp trong $p[]$.
Giờ chỉ còn thực hiện phép sắp xếp ổn định theo phần tử thứ nhất.
Như đã nói, việc này có thể làm bằng sắp xếp đếm.

Cuối cùng chỉ cần tính lại các lớp tương đương $c[]$; tương tự trước đó, ta chỉ việc duyệt hoán vị đã sắp xếp $p[]$ và so sánh các cặp kề nhau.

Đây là phần cài đặt còn lại.
Ta dùng các mảng tạm $pn[]$ và $cn[]$ để lưu hoán vị theo phần tử thứ hai và các chỉ số lớp tương đương mới.

```{.cpp file=suffix_array_sort_cyclic3}
    vector<int> pn(n), cn(n);
    for (int h = 0; (1 << h) < n; ++h) {
        for (int i = 0; i < n; i++) {
            pn[i] = p[i] - (1 << h);
            if (pn[i] < 0)
                pn[i] += n;
        }
        fill(cnt.begin(), cnt.begin() + classes, 0);
        for (int i = 0; i < n; i++)
            cnt[c[pn[i]]]++;
        for (int i = 1; i < classes; i++)
            cnt[i] += cnt[i-1];
        for (int i = n-1; i >= 0; i--)
            p[--cnt[c[pn[i]]]] = pn[i];
        cn[p[0]] = 0;
        classes = 1;
        for (int i = 1; i < n; i++) {
            pair<int, int> cur = {c[p[i]], c[(p[i] + (1 << h)) % n]};
            pair<int, int> prev = {c[p[i-1]], c[(p[i-1] + (1 << h)) % n]};
            if (cur != prev)
                ++classes;
            cn[p[i]] = classes - 1;
        }
        c.swap(cn);
    }
    return p;
}
```
Thuật toán cần $O(n \log n)$ thời gian và $O(n)$ bộ nhớ. Để đơn giản, ta dùng toàn bộ miền ASCII làm bảng chữ cái.

Nếu biết xâu chỉ chứa một tập con ký tự, chẳng hạn chỉ có chữ cái thường, ta có thể tối ưu cài đặt. Tuy nhiên hệ số cải thiện thường không đáng kể vì kích thước bảng chữ cái chỉ ảnh hưởng ở vòng đầu tiên. Các vòng sau phụ thuộc vào số lớp tương đương, mà số này có thể nhanh chóng đạt $O(n)$ ngay cả khi ban đầu xâu chỉ dùng bảng chữ cái kích thước $2$.

Cũng cần lưu ý rằng thuật toán này chỉ sắp xếp các phép dịch vòng.
Như đã nói ở đầu mục, ta có thể tạo thứ tự hậu tố đã sắp xếp bằng cách thêm một ký tự nhỏ hơn mọi ký tự khác trong xâu, rồi sắp xếp các phép dịch vòng của xâu mới, chẳng hạn với $s + \$$.
Điều này hiển nhiên cho mảng hậu tố của $s$, nhưng có thêm $|s|$ ở đầu.

```{.cpp file=suffix_array_construction}
vector<int> suffix_array_construction(string s) {
    s += "$";
    vector<int> sorted_shifts = sort_cyclic_shifts(s);
    sorted_shifts.erase(sorted_shifts.begin());
    return sorted_shifts;
}
```

## Ứng dụng

### Tìm phép dịch vòng nhỏ nhất

Thuật toán trên sắp xếp toàn bộ các phép dịch vòng mà không cần thêm ký tự vào xâu, vì vậy $p[0]$ cho ta vị trí bắt đầu của phép dịch vòng nhỏ nhất. 

### Tìm một xâu con trong xâu

Bài toán yêu cầu tìm xâu $s$ trong một văn bản $t$ theo kiểu online — ta biết trước văn bản $t$, nhưng chưa biết xâu truy vấn $s$.
Ta có thể xây dựng mảng hậu tố cho văn bản $t$ trong $O(|t| \log |t|)$ thời gian.
Sau đó ta tìm xâu con $s$ như sau.
Mỗi lần xuất hiện của $s$ phải là tiền tố của một hậu tố nào đó của $t$.
Vì các hậu tố đã được sắp xếp, ta có thể tìm kiếm nhị phân $s$ trên $p$.
Mỗi lần so sánh hậu tố hiện tại với xâu $s$ trong quá trình tìm kiếm nhị phân tốn $O(|s|)$ thời gian, nên tổng độ phức tạp để tìm xâu là $O(|s| \log |t|)$.
Ngoài ra, nếu xâu con xuất hiện nhiều lần trong $t$, mọi lần xuất hiện sẽ nằm cạnh nhau trong $p$.
Do đó, ta có thể tìm số lần xuất hiện bằng một lần tìm kiếm nhị phân thứ hai, và cũng dễ dàng in ra mọi vị trí xuất hiện.

### So sánh hai xâu con của một xâu

Ta muốn so sánh hai xâu con có cùng độ dài của một xâu $s$ trong $O(1)$ thời gian, tức kiểm tra xem xâu con thứ nhất có nhỏ hơn xâu con thứ hai hay không.

Ta xây dựng mảng hậu tố trong $O(|s| \log |s|)$ thời gian và lưu lại toàn bộ kết quả trung gian của các lớp tương đương $c[]$.

Nhờ thông tin này, ta có thể so sánh hai xâu con bất kỳ có độ dài là lũy thừa của hai trong O(1):
chỉ cần so sánh lớp tương đương của hai xâu con.
Bây giờ ta tổng quát hóa phương pháp cho xâu con có độ dài bất kỳ.

Hãy so sánh hai xâu con độ dài $l$ bắt đầu tại $i$ và $j$.
Ta tìm độ dài khối lớn nhất nằm trong một xâu con có độ dài này: số $k$ lớn nhất sao cho $2^k \le l$.
Sau đó, việc so sánh hai xâu con có thể thay bằng so sánh hai khối chồng lấn độ dài $2^k$:
đầu tiên so sánh hai khối bắt đầu tại $i$ và $j$; nếu chúng bằng nhau thì so sánh hai khối kết thúc tại các vị trí $i + l - 1$ và $j + l - 1$:

$$\dots
\overbrace{\underbrace{s_i \dots s_{i+l-2^k} \dots s_{i+2^k-1}}_{2^k} \dots s_{i+l-1}}^{\text{first}}
\dots
\overbrace{\underbrace{s_j \dots s_{j+l-2^k} \dots s_{j+2^k-1}}_{2^k} \dots s_{j+l-1}}^{\text{second}}
\dots$$

$$\dots
\overbrace{s_i \dots \underbrace{s_{i+l-2^k} \dots s_{i+2^k-1} \dots s_{i+l-1}}_{2^k}}^{\text{first}}
\dots
\overbrace{s_j \dots \underbrace{s_{j+l-2^k} \dots s_{j+2^k-1} \dots s_{j+l-1}}_{2^k}}^{\text{second}}
\dots$$

Đây là cài đặt cho phép so sánh.
Lưu ý hàm này giả sử $k$ đã được tính trước.
$k$ có thể được tính bằng $\lfloor \log l \rfloor$, nhưng hiệu quả hơn nếu tính trước mọi giá trị $k$ cho từng $l$.
Xem chẳng hạn bài [Sparse Table](../data_structures/sparse-table.md), nơi dùng ý tưởng tương tự và tính trước toàn bộ giá trị $\log$.

```cpp
int compare(int i, int j, int l, int k) {
    pair<int, int> a = {c[k][i], c[k][(i+l-(1 << k))%n]};
    pair<int, int> b = {c[k][j], c[k][(j+l-(1 << k))%n]};
    return a == b ? 0 : a < b ? -1 : 1;
}
```

### Tiền tố chung dài nhất của hai xâu con với bộ nhớ bổ sung

Với một xâu $s$, ta muốn tính tiền tố chung dài nhất (**LCP**) của hai hậu tố bất kỳ bắt đầu tại $i$ và $j$.

Phương pháp được mô tả ở đây dùng thêm $O(|s| \log |s|)$ bộ nhớ.
Một cách hoàn toàn khác chỉ dùng bộ nhớ tuyến tính sẽ được trình bày ở mục tiếp theo.

Ta xây dựng mảng hậu tố trong $O(|s| \log |s|)$ thời gian và lưu lại kết quả trung gian của các mảng $c[]$ ở mỗi vòng.

Hãy tính LCP cho hai hậu tố bắt đầu tại $i$ và $j$.
Ta có thể so sánh hai xâu con có độ dài là lũy thừa của hai trong $O(1)$.
Ta sẽ so sánh theo các lũy thừa của hai từ lớn xuống nhỏ; nếu hai xâu con có độ dài hiện tại bằng nhau, ta cộng độ dài đó vào đáp án rồi tiếp tục kiểm tra LCP ở phần bên phải của đoạn đã bằng nhau, tức tăng $i$ và $j$ thêm đúng lũy thừa của hai hiện tại.

```cpp
int lcp(int i, int j) {
    int ans = 0;
    for (int k = log_n; k >= 0; k--) {
        if (c[k][i % n] == c[k][j % n]) {
            ans += 1 << k;
            i += 1 << k;
            j += 1 << k;
        }
    }
    return ans;
}
```

Ở đây `log_n` là một hằng số bằng logarithm cơ số $2$ của $n$, làm tròn xuống.

### Tiền tố chung dài nhất của hai xâu con không cần bộ nhớ bổ sung

Ta xét lại bài toán ở mục trước.
Ta cần tính tiền tố chung dài nhất (**LCP**) của hai hậu tố của xâu $s$.

Khác với phương pháp trước, cách này chỉ dùng $O(|s|)$ bộ nhớ.
Kết quả tiền xử lý là một mảng — bản thân nó cũng chứa nhiều thông tin quan trọng về xâu và vì vậy có thể dùng để giải các bài toán khác.
Các truy vấn LCP có thể được trả lời bằng truy vấn RMQ (range minimum query) trên mảng này, nên tùy cách cài đặt ta có thể đạt thời gian truy vấn logarithm hoặc thậm chí hằng số. 

Ý tưởng nền tảng của thuật toán là:
ta sẽ tính tiền tố chung dài nhất cho từng **cặp hậu tố kề nhau trong thứ tự đã sắp xếp**.
Nói cách khác, ta xây dựng mảng $\text{lcp}[0 \dots n-2]$, trong đó $\text{lcp}[i]$ bằng độ dài tiền tố chung dài nhất của hai hậu tố bắt đầu tại $p[i]$ và $p[i+1]$.
Mảng này cho ta đáp án với mọi cặp hậu tố kề nhau.
Sau đó, đáp án cho hai hậu tố bất kỳ không nhất thiết kề nhau cũng có thể suy ra từ mảng này.
Cụ thể, giả sử cần tính LCP của các hậu tố $p[i]$ và $p[j]$.
Khi đó đáp án là $\min(lcp[i],~ lcp[i+1],~ \dots,~ lcp[j-1])$.

Vì vậy, nếu đã có mảng $\text{lcp}$, bài toán được đưa về [RMQ](../sequences/rmq.md), vốn có nhiều lời giải với các độ phức tạp khác nhau.

Nhiệm vụ chính còn lại là **xây dựng** mảng $\text{lcp}$ này.
Ta dùng **thuật toán Kasai**, có thể tính mảng trong $O(n)$ thời gian.

Xét hai hậu tố kề nhau trong thứ tự đã sắp xếp, tức thứ tự của mảng hậu tố.
Gọi vị trí bắt đầu của chúng là $i$ và $j$, và $\text{lcp}$ của chúng bằng $k > 0$.
Nếu bỏ ký tự đầu của cả hai hậu tố — tức xét hậu tố $i+1$ và $j+1$ — thì hiển nhiên $\text{lcp}$ của chúng là $k - 1$.
Tuy nhiên, ta không thể dùng ngay giá trị này để ghi vào mảng $\text{lcp}$, vì hai hậu tố mới có thể không còn đứng cạnh nhau trong thứ tự đã sắp xếp.
Hậu tố $i+1$ chắc chắn nhỏ hơn hậu tố $j+1$, nhưng có thể có các hậu tố khác nằm giữa chúng.
Dù vậy, vì LCP giữa hai hậu tố bằng giá trị nhỏ nhất trên các bước chuyển giữa chúng, ta biết LCP của mọi cặp kề nhau trong khoảng này ít nhất là $k-1$, đặc biệt là giữa $i+1$ và hậu tố kế tiếp.
Và giá trị này có thể còn lớn hơn.

Giờ ta có thể cài đặt thuật toán.
Ta duyệt các hậu tố theo thứ tự độ dài. Nhờ vậy có thể tái sử dụng giá trị $k$ trước đó, vì chuyển từ hậu tố $i$ sang hậu tố $i+1$ chính là bỏ đi ký tự đầu tiên.
Ta cần thêm mảng $\text{rank}$, cho biết vị trí của một hậu tố trong danh sách hậu tố đã sắp xếp.

```{.cpp file=suffix_array_lcp_construction}
vector<int> lcp_construction(string const& s, vector<int> const& p) {
    int n = s.size();
    vector<int> rank(n, 0);
    for (int i = 0; i < n; i++)
        rank[p[i]] = i;

    int k = 0;
    vector<int> lcp(n-1, 0);
    for (int i = 0; i < n; i++) {
        if (rank[i] == n - 1) {
            k = 0;
            continue;
        }
        int j = p[rank[i] + 1];
        while (i + k < n && j + k < n && s[i+k] == s[j+k])
            k++;
        lcp[rank[i]] = k;
        if (k)
            k--;
    }
    return lcp;
}
```

Dễ thấy ta giảm $k$ nhiều nhất $O(n)$ lần (mỗi vòng lặp nhiều nhất một lần, trừ trường hợp $\text{rank}[i] == n-1$, khi đó đặt thẳng về $0$), và LCP của hai xâu không vượt quá $n-1$, nên ta cũng chỉ tăng $k$ tổng cộng $O(n)$ lần.
Do đó thuật toán chạy trong $O(n)$ thời gian.

### Số xâu con phân biệt

Ta tiền xử lý xâu $s$ bằng cách tính mảng hậu tố và mảng LCP.
Từ thông tin này, ta có thể tính số xâu con phân biệt của xâu.

Ta xét xem những xâu con **mới** nào bắt đầu tại $p[0]$, rồi tại $p[1]$, v.v.
Thực chất ta duyệt các hậu tố theo thứ tự đã sắp xếp và xem những tiền tố nào tạo ra xâu con mới.
Nhờ vậy không xâu con nào bị bỏ sót.

Vì các hậu tố đã được sắp xếp, rõ ràng hậu tố hiện tại $p[i]$ tạo ra xâu con mới với mọi tiền tố của nó, ngoại trừ các tiền tố trùng với hậu tố $p[i-1]$.
Do đó, mọi tiền tố ngoại trừ $\text{lcp}[i-1]$ tiền tố đầu tiên đều là mới.
Vì độ dài hậu tố hiện tại là $n - p[i]$, có $n - p[i] - \text{lcp}[i-1]$ tiền tố mới bắt đầu tại $p[i]$.
Cộng trên toàn bộ hậu tố, ta thu được đáp án:

$$\sum_{i=0}^{n-1} (n - p[i]) - \sum_{i=0}^{n-2} \text{lcp}[i] = \frac{n^2 + n}{2} - \sum_{i=0}^{n-2} \text{lcp}[i]$$

## Bài tập

* [Uva 760 - DNA Sequencing](http://uva.onlinejudge.org/index.php?option=com_onlinejudge&Itemid=8&category=24&page=show_problem&problem=701)
* [Uva 1223 - Editor](http://uva.onlinejudge.org/index.php?option=com_onlinejudge&Itemid=8&category=24&page=show_problem&problem=3664)
* [Codechef - Tandem](https://www.codechef.com/problems/TANDEM)
* [Codechef - Substrings and Repetitions](https://www.codechef.com/problems/ANUSAR)
* [Codechef - Entangled Strings](https://www.codechef.com/problems/TANGLED)
* [Codeforces - Martian Strings](http://codeforces.com/problemset/problem/149/E)
* [Codeforces - Little Elephant and Strings](http://codeforces.com/problemset/problem/204/E)
* [SPOJ - Ada and Terramorphing](http://www.spoj.com/problems/ADAPHOTO/)
* [SPOJ - Ada and Substring](http://www.spoj.com/problems/ADASTRNG/)
* [UVA - 1227 - The longest constant gene](https://uva.onlinejudge.org/index.php?option=onlinejudge&page=show_problem&problem=3668)
* [SPOJ - Longest Common Substring](http://www.spoj.com/problems/LCS/en/)
* [UVA 11512 - GATTACA](https://uva.onlinejudge.org/index.php?option=com_onlinejudge&Itemid=8&page=show_problem&problem=2507)
* [LA 7502 - Suffixes and Palindromes](https://vjudge.net/problem/UVALive-7502)
* [GYM - Por Costel and the Censorship Committee](http://codeforces.com/gym/100923/problem/D)
* [UVA 1254 - Top 10](https://uva.onlinejudge.org/index.php?option=com_onlinejudge&Itemid=8&page=show_problem&problem=3695)
* [UVA 12191 - File Recover](https://uva.onlinejudge.org/index.php?option=com_onlinejudge&Itemid=8&page=show_problem&problem=3343)
* [UVA 12206 - Stammering Aliens](https://uva.onlinejudge.org/index.php?option=onlinejudge&page=show_problem&problem=3358)
* [Codechef - Jarvis and LCP](https://www.codechef.com/problems/INSQ16F)
* [LA 3943 - Liking's Letter](https://vjudge.net/problem/UVALive-3943)
* [UVA 11107 - Life Forms](https://uva.onlinejudge.org/index.php?option=com_onlinejudge&Itemid=8&page=show_problem&problem=2048)
* [UVA 12974 - Exquisite Strings](https://uva.onlinejudge.org/index.php?option=com_onlinejudge&Itemid=8&category=862&page=show_problem&problem=4853)
* [UVA 10526 - Intellectual Property](https://uva.onlinejudge.org/index.php?option=com_onlinejudge&Itemid=8&page=show_problem&problem=1467)
* [UVA 12338 - Anti-Rhyme Pairs](https://uva.onlinejudge.org/index.php?option=onlinejudge&page=show_problem&problem=3760)
* [UVA 12191 - File Recover](https://uva.onlinejudge.org/index.php?option=com_onlinejudge&Itemid=8&page=show_problem&problem=3343)
* [SPOJ - Suffix Array](http://www.spoj.com/problems/SARRAY/)
* [LA 4513 - Stammering Aliens](https://vjudge.net/problem/UVALive-4513)
* [SPOJ - LCS2](http://www.spoj.com/problems/LCS2/)
* [Codeforces - Fake News (hard)](http://codeforces.com/contest/802/problem/I)
* [SPOJ - Longest Commong Substring](http://www.spoj.com/problems/LONGCS/)
* [SPOJ - Lexicographical Substring Search](http://www.spoj.com/problems/SUBLEX/)
* [Codeforces - Forbidden Indices](http://codeforces.com/contest/873/problem/F)
* [Codeforces - Tricky and Clever Password](http://codeforces.com/contest/30/problem/E)
* [LA 6856 - Circle of digits](https://vjudge.net/problem/UVALive-6856)