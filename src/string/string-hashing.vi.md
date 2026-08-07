---
tags:
  - Translated
e_maxx_link: string_hashes
translation:
  source: string/string-hashing.md
  source_commit: f354b5e1d3bde22b261f2bdf27766de3f86bd530
  status: draft
  last_synced: 2026-08-07
---

# Băm chuỗi

Các thuật toán băm (hashing) rất hữu ích trong nhiều bài toán.

Ta muốn giải quyết bài toán so sánh các chuỗi một cách hiệu quả.
Cách vét cạn đơn giản là so sánh trực tiếp các ký tự của hai chuỗi, có độ phức tạp thời gian $O(\min(n_1, n_2))$ nếu $n_1$ và $n_2$ là độ dài của hai chuỗi.
Ta muốn làm tốt hơn.
Ý tưởng của băm chuỗi là ánh xạ mỗi chuỗi thành một số nguyên rồi so sánh các số đó thay vì so sánh trực tiếp chuỗi.
Nhờ vậy, thời gian so sánh chuỗi có thể giảm xuống $O(1)$.

Để thực hiện phép chuyển đổi này, ta cần một **hàm băm** (hash function).
Mục tiêu của hàm băm là chuyển một chuỗi thành một số nguyên, gọi là **giá trị băm** (hash) của chuỗi.
Điều kiện sau phải được bảo đảm: nếu hai chuỗi $s$ và $t$ bằng nhau ($s = t$), thì giá trị băm của chúng cũng phải bằng nhau ($\text{hash}(s) = \text{hash}(t)$).
Nếu không, ta sẽ không thể dùng giá trị băm để so sánh chuỗi.

Lưu ý rằng chiều ngược lại không nhất thiết đúng.
Nếu hai giá trị băm bằng nhau ($\text{hash}(s) = \text{hash}(t)$), hai chuỗi chưa chắc bằng nhau.
Ví dụ, một hàm băm hợp lệ có thể đơn giản là $\text{hash}(s) = 0$ với mọi $s$.
Đây rõ ràng là một ví dụ vô dụng trong thực tế, nhưng về mặt định nghĩa nó vẫn là một hàm băm hợp lệ.
Lý do chiều ngược lại không bắt buộc đúng là số lượng chuỗi tăng theo cấp số mũ.
Nếu chỉ muốn hàm băm phân biệt mọi chuỗi gồm chữ cái thường có độ dài nhỏ hơn 15, giá trị băm đã không còn vừa trong một số nguyên 64 bit (chẳng hạn `unsigned long long`) vì số chuỗi quá lớn.
Và dĩ nhiên ta cũng không muốn so sánh các số nguyên dài tùy ý, vì việc đó lại có độ phức tạp $O(n)$.

Do đó, thông thường ta muốn hàm băm ánh xạ các chuỗi vào một miền số cố định $[0, m)$; khi ấy so sánh chuỗi chỉ còn là so sánh hai số nguyên có độ dài cố định.
Đồng thời, nếu $s \neq t$, ta muốn xác suất $\text{hash}(s) \neq \text{hash}(t)$ là rất cao.

Đây là điểm quan trọng cần ghi nhớ.
Sử dụng băm không bảo đảm đúng 100% theo nghĩa xác định, bởi hai chuỗi hoàn toàn khác nhau vẫn có thể nhận cùng một giá trị băm; hiện tượng này gọi là **va chạm băm**.
Tuy nhiên, trong phần lớn bài toán, ta có thể bỏ qua rủi ro này vì xác suất hai chuỗi khác nhau bị va chạm vẫn rất nhỏ.
Bài viết cũng sẽ trình bày một số kỹ thuật để giữ xác suất va chạm ở mức rất thấp.

## Tính giá trị băm của một chuỗi

Một cách tốt và được dùng rộng rãi để định nghĩa giá trị băm của chuỗi $s$ có độ dài $n$ là

$$\begin{align}
\text{hash}(s) &= s[0] + s[1] \cdot p + s[2] \cdot p^2 + ... + s[n-1] \cdot p^{n-1} \mod m \\
&= \sum_{i=0}^{n-1} s[i] \cdot p^i \mod m,
\end{align}$$

trong đó $p$ và $m$ là hai số dương được chọn trước.
Cách này được gọi là **hàm băm đa thức** (polynomial rolling hash function).

Ta nên chọn $p$ là một số nguyên tố xấp xỉ số lượng ký tự trong bảng chữ cái đầu vào.
Ví dụ, nếu đầu vào chỉ gồm chữ cái thường trong bảng chữ cái tiếng Anh, $p = 31$ là một lựa chọn tốt.
Nếu đầu vào có thể chứa cả chữ hoa và chữ thường, $p = 53$ là một lựa chọn khả thi.
Code trong bài viết này sẽ dùng $p = 31$.

Hiển nhiên $m$ nên là một số lớn, vì xác suất hai chuỗi ngẫu nhiên va chạm xấp xỉ $\approx \frac{1}{m}$.
Đôi khi người ta chọn $m = 2^{64}$, vì khi đó hiện tượng tràn số của số nguyên 64 bit hoạt động đúng như phép lấy mô-đun.
Tuy nhiên, tồn tại một phương pháp tạo ra các chuỗi bị va chạm mà không phụ thuộc vào cách chọn $p$.
Vì vậy trong thực tế, $m = 2^{64}$ không được khuyến nghị.
Một lựa chọn tốt cho $m$ là một số nguyên tố lớn.
Code trong bài chỉ dùng $m = 10^9+9$.
Đây là một số lớn nhưng vẫn đủ nhỏ để phép nhân hai giá trị có thể thực hiện bằng số nguyên 64 bit.

Dưới đây là ví dụ tính giá trị băm của chuỗi $s$ chỉ gồm chữ cái thường.
Ta chuyển mỗi ký tự của $s$ thành một số nguyên.
Ở đây dùng ánh xạ $a \rightarrow 1$, $b \rightarrow 2$, $\dots$, $z \rightarrow 26$.
Không nên dùng ánh xạ $a \rightarrow 0$, vì khi đó các chuỗi $a$, $aa$, $aaa$, $\dots$ đều có giá trị băm bằng $0$.

```{.cpp file=hashing_function}
long long compute_hash(string const& s) {
    const int p = 31;
    const int m = 1e9 + 9;
    long long hash_value = 0;
    long long p_pow = 1;
    for (char c : s) {
        hash_value = (hash_value + (c - 'a' + 1) * p_pow) % m;
        p_pow = (p_pow * p) % m;
    }
    return hash_value;
}
```

Tính trước các lũy thừa của $p$ có thể giúp cải thiện hiệu năng.

## Các bài toán ví dụ

### Tìm các chuỗi trùng nhau trong một mảng chuỗi

Bài toán: Cho danh sách gồm $n$ chuỗi $s_i$, mỗi chuỗi có độ dài không quá $m$, hãy tìm mọi chuỗi trùng nhau và chia chúng thành các nhóm.

Với thuật toán hiển nhiên là sắp xếp trực tiếp các chuỗi, ta có độ phức tạp $O(n m \log n)$: việc sắp xếp cần $O(n \log n)$ phép so sánh và mỗi phép so sánh mất $O(m)$ thời gian.
Tuy nhiên, bằng cách dùng giá trị băm, thời gian mỗi phép so sánh giảm xuống $O(1)$, cho thuật toán có độ phức tạp $O(n m + n \log n)$.

Ta tính giá trị băm của mỗi chuỗi, sắp xếp các giá trị băm cùng chỉ số tương ứng, rồi gom những chỉ số có cùng giá trị băm vào một nhóm.

```{.cpp file=hashing_group_identical_strings}
vector<vector<int>> group_identical_strings(vector<string> const& s) {
    int n = s.size();
    vector<pair<long long, int>> hashes(n);
    for (int i = 0; i < n; i++)
        hashes[i] = {compute_hash(s[i]), i};

    sort(hashes.begin(), hashes.end());

    vector<vector<int>> groups;
    for (int i = 0; i < n; i++) {
        if (i == 0 || hashes[i].first != hashes[i-1].first)
            groups.emplace_back();
        groups.back().push_back(hashes[i].second);
    }
    return groups;
}
```

### Tính nhanh giá trị băm của chuỗi con trong một chuỗi cho trước

Bài toán: Cho chuỗi $s$ và hai chỉ số $i$, $j$, hãy tìm giá trị băm của chuỗi con $s [i \dots j]$.

Theo định nghĩa, ta có:

$$\text{hash}(s[i \dots j]) = \sum_{k = i}^j s[k] \cdot p^{k-i} \mod m$$

Nhân hai vế với $p^i$ ta được:

$$\begin{align}
\text{hash}(s[i \dots j]) \cdot p^i &= \sum_{k = i}^j s[k] \cdot p^k \mod m \\
&= \text{hash}(s[0 \dots j]) - \text{hash}(s[0 \dots i-1]) \mod m
\end{align}$$

Vì vậy, nếu biết giá trị băm của mọi tiền tố của chuỗi $s$, ta có thể tính trực tiếp giá trị băm của bất kỳ chuỗi con nào bằng công thức trên.
Vấn đề duy nhất là phải chia $\text{hash}(s[0 \dots j]) - \text{hash}(s[0 \dots i-1])$ cho $p^i$.
Do đó ta cần tìm [nghịch đảo nhân mô-đun](../algebra/module-inverse.md) của $p^i$ rồi nhân với nghịch đảo này.
Có thể tính trước nghịch đảo của mọi $p^i$, nhờ đó giá trị băm của bất kỳ chuỗi con nào trong $s$ được tính trong $O(1)$ thời gian.

Tuy nhiên còn có một cách đơn giản hơn.
Trong phần lớn trường hợp, thay vì tính chính xác giá trị băm của chuỗi con, chỉ cần tính giá trị băm nhân với một lũy thừa nào đó của $p$.
Giả sử ta có hai giá trị băm của hai chuỗi con, một giá trị đã nhân với $p^i$ và giá trị kia đã nhân với $p^j$.
Nếu $i < j$, ta nhân giá trị băm thứ nhất với $p^{j-i}$; ngược lại, nhân giá trị thứ hai với $p^{i-j}$.
Khi đó cả hai giá trị băm đều được nhân với cùng một lũy thừa của $p$ (là giá trị lớn hơn giữa $i$ và $j$), nên có thể so sánh chúng dễ dàng mà không cần phép chia nào.

## Ứng dụng của băm

Dưới đây là một số ứng dụng điển hình của băm:

* [Thuật toán Rabin-Karp](rabin-karp.md) để tìm mẫu trong chuỗi trong $O(n)$ thời gian
* Tính số chuỗi con khác nhau của một chuỗi trong $O(n^2)$ (xem bên dưới)
* Tính số chuỗi con đối xứng trong một chuỗi.

### Xác định số chuỗi con khác nhau trong một chuỗi

Bài toán: Cho chuỗi $s$ có độ dài $n$, chỉ gồm chữ cái thường tiếng Anh, hãy tìm số chuỗi con khác nhau của chuỗi này.

Để giải bài toán, ta duyệt mọi độ dài chuỗi con $l = 1 \dots n$.
Với mỗi độ dài $l$, ta tạo một mảng gồm giá trị băm của mọi chuỗi con có độ dài $l$, sau khi tất cả chúng được nhân với cùng một lũy thừa của $p$.
Số phần tử khác nhau trong mảng chính là số chuỗi con phân biệt có độ dài $l$.
Cộng số này vào đáp án cuối cùng.

Để thuận tiện, ta dùng $h[i]$ làm giá trị băm của tiền tố có $i$ ký tự và định nghĩa $h[0] = 0$.

```{.cpp file=hashing_count_unique_substrings}
int count_unique_substrings(string const& s) {
    int n = s.size();
    
    const int p = 31;
    const int m = 1e9 + 9;
    vector<long long> p_pow(n);
    p_pow[0] = 1;
    for (int i = 1; i < n; i++)
        p_pow[i] = (p_pow[i-1] * p) % m;

    vector<long long> h(n + 1, 0);
    for (int i = 0; i < n; i++)
        h[i+1] = (h[i] + (s[i] - 'a' + 1) * p_pow[i]) % m;

    int cnt = 0;
    for (int l = 1; l <= n; l++) {
        unordered_set<long long> hs;
        for (int i = 0; i <= n - l; i++) {
            long long cur_h = (h[i + l] + m - h[i]) % m;
            cur_h = (cur_h * p_pow[n-i-1]) % m;
            hs.insert(cur_h);
        }
        cnt += hs.size();
    }
    return cnt;
}
```

Lưu ý rằng $O(n^2)$ chưa phải độ phức tạp thời gian tốt nhất cho bài toán này.
Một lời giải $O(n \log n)$ được mô tả trong bài [Suffix Arrays](suffix-array.md), và thậm chí có thể tính trong $O(n)$ bằng [Suffix Tree](./suffix-tree-ukkonen.md) hoặc [Suffix Automaton](./suffix-automaton.md).

## Giảm xác suất va chạm

Thông thường hàm băm đa thức nêu trên đã đủ tốt và không xảy ra va chạm trong bộ test.
Nhớ rằng xác suất xảy ra va chạm chỉ xấp xỉ $\approx \frac{1}{m}$.
Với $m = 10^9 + 9$, xác suất là $\approx 10^{-9}$, khá nhỏ.
Nhưng lưu ý rằng ở đây ta mới chỉ thực hiện một phép so sánh.
Điều gì xảy ra nếu so sánh một chuỗi $s$ với $10^6$ chuỗi khác nhau?
Xác suất có ít nhất một lần va chạm lúc này xấp xỉ $\approx 10^{-3}$.
Nếu muốn so sánh $10^6$ chuỗi khác nhau với nhau (chẳng hạn để đếm số chuỗi phân biệt), xác suất xuất hiện ít nhất một va chạm đã xấp xỉ $\approx 1$.
Khi đó gần như chắc chắn bài toán sẽ gặp va chạm và trả về kết quả sai.

Có một mẹo rất đơn giản để cải thiện xác suất.
Ta có thể tính hai giá trị băm khác nhau cho mỗi chuỗi (bằng cách dùng hai giá trị $p$ khác nhau và/hoặc hai giá trị $m$ khác nhau), rồi so sánh các cặp giá trị này.
Nếu $m$ của mỗi hàm băm đều cỡ $10^9$, cách này gần tương đương với dùng một hàm băm có $m \approx 10^{18}$.
Khi so sánh $10^6$ chuỗi với nhau, xác suất có ít nhất một va chạm lúc này giảm xuống xấp xỉ $\approx 10^{-6}$.

## Bài tập luyện tập
* [Good Substrings - Codeforces](https://codeforces.com/contest/271/problem/D)
* [A Needle in the Haystack - SPOJ](http://www.spoj.com/problems/NHAY/)
* [String Hashing - Kattis](https://open.kattis.com/problems/hashing)
* [Double Profiles - Codeforces](http://codeforces.com/problemset/problem/154/C)
* [Password - Codeforces](http://codeforces.com/problemset/problem/126/B)
* [SUB_PROB - SPOJ](http://www.spoj.com/problems/SUB_PROB/)
* [INSQ15_A](https://www.codechef.com/problems/INSQ15_A)
* [SPOJ - Ada and Spring Cleaning](http://www.spoj.com/problems/ADACLEAN/)
* [GYM - Text Editor](http://codeforces.com/gym/101466/problem/E)
* [12012 - Detection of Extraterrestrial](https://uva.onlinejudge.org/index.php?option=onlinejudge&page=show_problem&problem=3163)
* [Codeforces - Games on a CD](http://codeforces.com/contest/727/problem/E)
* [UVA 11855 - Buzzwords](https://uva.onlinejudge.org/index.php?option=com_onlinejudge&Itemid=8&page=show_problem&problem=2955)
* [Codeforces - Santa Claus and a Palindrome](http://codeforces.com/contest/752/problem/D)
* [Codeforces - String Compression](http://codeforces.com/contest/825/problem/F)
* [Codeforces - Palindromic Characteristics](http://codeforces.com/contest/835/problem/D)
* [SPOJ - Test](http://www.spoj.com/problems/CF25E/)
* [Codeforces - Palindrome Degree](http://codeforces.com/contest/7/problem/D)
* [Codeforces - Deletion of Repeats](http://codeforces.com/contest/19/problem/C)
* [HackerRank - Gift Boxes](https://www.hackerrank.com/contests/womens-codesprint-5/challenges/gift-boxes)

