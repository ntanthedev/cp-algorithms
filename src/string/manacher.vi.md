---
title: Manacher's Algorithm - Finding all sub-palindromes in O(N)
tags:
  - Translated
e_maxx_link: palindromes_count
translation:
  source: string/manacher.md
  source_commit: 1594a352a5b3f52c7d0e47b5a19ffceff8d9047a
  status: draft
  last_synced: 2026-08-07
---
# Thuật toán Manacher - Tìm mọi xâu con đối xứng trong $O(N)$

## Phát biểu

Cho chuỗi $s$ có độ dài $n$. Hãy tìm mọi cặp $(i, j)$ sao cho chuỗi con $s[i\dots j]$ là một xâu đối xứng. Chuỗi $t$ là xâu đối xứng khi $t = t_{rev}$ ($t_{rev}$ là chuỗi đảo ngược của $t$).

## Phát biểu chính xác hơn

Trong trường hợp xấu nhất, một chuỗi có thể có tới $O(n^2)$ xâu con đối xứng, nên thoạt nhìn có vẻ không thể tồn tại thuật toán tuyến tính cho bài toán này.

Tuy nhiên, thông tin về các xâu đối xứng có thể được lưu **một cách cô đọng**: với mỗi vị trí $i$, ta sẽ tìm số xâu đối xứng không rỗng có tâm tại vị trí đó.

Các xâu đối xứng có cùng tâm tạo thành một dãy liên tiếp: nếu có một xâu đối xứng độ dài $l$ với tâm tại $i$, thì cũng có các xâu đối xứng độ dài $l-2$, $l-4$ và cứ thế, cũng có tâm tại $i$. Vì vậy, ta sẽ lưu thông tin về mọi xâu con đối xứng theo cách này.

Các xâu đối xứng có độ dài lẻ và chẵn được xét riêng bằng $d_{odd}[i]$ và $d_{even}[i]$. Với xâu đối xứng có độ dài chẵn, ta coi tâm của nó nằm tại vị trí $i$ nếu hai ký tự ở giữa là $s[i]$ và $s[i-1]$.

Ví dụ, chuỗi $s = abababc$ có ba xâu đối xứng độ dài lẻ với tâm tại vị trí $s[3] = b$, tức $d_{odd}[3] = 3$:

$$a\ \overbrace{b\ a\ \underbrace{b}_{s_3}\ a\ b}^{d_{odd}[3]=3} c$$

Còn chuỗi $s = cbaabd$ có hai xâu đối xứng độ dài chẵn với tâm tại vị trí $s[3] = a$, tức $d_{even}[3] = 2$:

$$c\ \overbrace{b\ a\ \underbrace{a}_{s_3}\ b}^{d_{even}[3]=2} d$$

Một điều khá bất ngờ là có một thuật toán đủ đơn giản để tính các "mảng đối xứng" $d_{odd}[]$ và $d_{even}[]$ trong thời gian tuyến tính. Thuật toán đó được trình bày trong bài này.

## Lời giải

Nhìn chung, bài toán này có nhiều cách giải: dùng [Băm chuỗi](string-hashing.md) có thể giải trong $O(n\cdot \log n)$, còn với [Cây hậu tố](suffix-tree-ukkonen.md) và LCA nhanh thì có thể giải trong $O(n)$.

Tuy nhiên, phương pháp được trình bày ở đây **đơn giản hơn đáng kể** và có hằng số ẩn nhỏ hơn cả về thời gian lẫn bộ nhớ. Thuật toán này được **Glenn K. Manacher** phát hiện vào năm 1975.

Một cách hiện đại khác để giải bài toán này và xử lý xâu đối xứng nói chung là dùng cây đối xứng, hay eertree.

## Thuật toán ngây thơ

Để tránh nhập nhằng trong phần mô tả sau, trước hết ta xác định rõ "thuật toán ngây thơ" là gì.

Thuật toán hoạt động như sau. Với mỗi vị trí tâm $i$, nó cố tăng đáp án thêm một đơn vị khi còn có thể, mỗi lần so sánh một cặp ký tự tương ứng.

Thuật toán này chậm và chỉ có thể tính đáp án trong $O(n^2)$.

Cài đặt của thuật toán ngây thơ như sau:

```cpp
vector<int> manacher_odd_trivial(string s) {
    int n = s.size();
    s = "$" + s + "^";
    vector<int> p(n + 2);
    for(int i = 1; i <= n; i++) {
        while(s[i - p[i]] == s[i + p[i]]) {
            p[i]++;
        }
    }
    return vector<int>(begin(p) + 1, end(p) - 1);
}
```

Hai ký tự chặn `$` và `^` được dùng để không phải xử lý riêng hai đầu chuỗi.

## Thuật toán Manacher

Ta mô tả thuật toán tìm mọi xâu con đối xứng có độ dài lẻ, tức tính $d_{odd}[]$.

Để tính nhanh, ta duy trì **hai biên loại trừ $(l, r)$** của xâu con đối xứng nằm xa nhất về bên phải đã tìm thấy (tức xâu con đối xứng ngoài cùng bên phải hiện tại là $s[l+1] s[l+2] \dots s[r-1]$). Ban đầu đặt $l = 0, r = 1$, tương ứng với chuỗi rỗng.

Giả sử ta muốn tính $d_{odd}[i]$ cho vị trí $i$ tiếp theo, và mọi giá trị trước đó trong $d_{odd}[]$ đã được tính. Ta làm như sau:

* Nếu $i$ nằm ngoài xâu con đối xứng hiện tại, tức $i \geq r$, ta chỉ cần chạy thuật toán ngây thơ.
    
    Ta tăng dần $d_{odd}[i]$ và mỗi lần kiểm tra xem chuỗi con hiện tại ngoài cùng bên phải $[i - d_{odd}[i]\dots i + d_{odd}[i]]$ có phải xâu đối xứng hay không. Khi gặp cặp ký tự đầu tiên không khớp hoặc chạm biên của $s$, ta dừng lại. Khi đó $d_{odd}[i]$ đã được tính xong. Sau đó, đừng quên cập nhật $(l, r)$. $r$ cần được cập nhật sao cho nó biểu diễn chỉ số cuối của xâu con đối xứng ngoài cùng bên phải hiện tại.

* Bây giờ xét trường hợp $i \le r$. Ta sẽ cố tận dụng các giá trị đã tính trong $d_{odd}[]$. Hãy tìm vị trí "đối xứng" của $i$ trong xâu con đối xứng $(l, r)$, tức vị trí $j = l + (r - i)$, rồi xét giá trị $d_{odd}[j]$. Vì $j$ đối xứng với $i$ qua $(l+r)/2$, ta **gần như luôn có thể** gán $d_{odd}[i] = d_{odd}[j]$. Hình dưới minh họa điều này (xâu đối xứng quanh $j$ thực chất được "sao chép" sang xâu đối xứng quanh $i$):
    
    $$
    \ldots\ 
    \overbrace{
        s_{l+1}\ \ldots\ 
        \underbrace{
            s_{j-d_{odd}[j]+1}\ \ldots\ s_j\ \ldots\ s_{j+d_{odd}[j]-1}\ 
        }_\text{palindrome}\ 
        \ldots\ 
        \underbrace{
            s_{i-d_{odd}[j]+1}\ \ldots\ s_i\ \ldots\ s_{i+d_{odd}[j]-1}\ 
        }_\text{palindrome}\ 
        \ldots\ s_{r-1}\ 
    }^\text{palindrome}\ 
    \ldots
    $$
    
    Tuy nhiên có một **trường hợp khó** cần xử lý chính xác: khi xâu đối xứng "bên trong" chạm biên của xâu đối xứng "bên ngoài", tức $j - d_{odd}[j] \le l$ (hay tương đương $i + d_{odd}[j] \ge r$). Vì không có gì bảo đảm tính đối xứng ở ngoài xâu đối xứng "bên ngoài", việc gán thẳng $d_{odd}[i] = d_{odd}[j]$ sẽ sai: ta không có đủ dữ liệu để khẳng định xâu đối xứng tại vị trí $i$ có cùng độ dài.
    
    Trước mắt, ta cần giới hạn độ dài của xâu đối xứng, tức gán $d_{odd}[i] = r - i$, để xử lý đúng tình huống này. Sau đó ta chạy thuật toán ngây thơ để tiếp tục tăng $d_{odd}[i]$ khi còn có thể.
    
    Hình dưới minh họa trường hợp này (xâu đối xứng có tâm $j$ bị giới hạn để nằm gọn trong xâu đối xứng "bên ngoài"):
    
    $$
    \ldots\ 
    \overbrace{
        \underbrace{
            s_{l+1}\ \ldots\ s_j\ \ldots\ s_{j+(j-l)-1}\ 
        }_\text{palindrome}\ 
        \ldots\ 
        \underbrace{
            s_{i-(r-i)+1}\ \ldots\ s_i\ \ldots\ s_{r-1}
        }_\text{palindrome}\ 
    }^\text{palindrome}\ 
    \underbrace{
        \ldots \ldots \ldots \ldots \ldots
    }_\text{try moving here}
    $$
    
    Hình cho thấy xâu đối xứng có tâm $j$ có thể dài hơn và vượt ra ngoài xâu đối xứng "bên ngoài", nhưng khi lấy $i$ làm tâm, ta chỉ có thể tận dụng phần nằm hoàn toàn trong xâu đối xứng "bên ngoài". Tuy nhiên đáp án tại vị trí $i$ ($d_{odd}[i]$) có thể lớn hơn nhiều so với phần này, vì vậy tiếp theo ta chạy thuật toán ngây thơ để thử mở rộng ra ngoài xâu đối xứng "bên ngoài", tức sang vùng "try moving here".

Một lần nữa, đừng quên cập nhật các giá trị $(l, r)$ sau khi tính mỗi $d_{odd}[i]$.

## Độ phức tạp của thuật toán Manacher

Thoạt nhìn không dễ thấy thuật toán có độ phức tạp thời gian tuyến tính, vì ta thường xuyên chạy thuật toán ngây thơ khi tìm đáp án cho một vị trí cụ thể.

Tuy nhiên, phân tích kỹ hơn cho thấy thuật toán là tuyến tính. Thực tế, [thuật toán xây dựng hàm Z](z-function.md), vốn khá giống thuật toán này, cũng chạy trong thời gian tuyến tính.

Ta nhận thấy mỗi vòng lặp của thuật toán ngây thơ làm $r$ tăng thêm một. Đồng thời $r$ không bao giờ giảm trong suốt thuật toán. Vì vậy tổng số vòng lặp của thuật toán ngây thơ là $O(n)$.

Các phần còn lại của thuật toán Manacher hiển nhiên chạy trong thời gian tuyến tính. Do đó, ta thu được độ phức tạp thời gian $O(n)$.

## Cài đặt thuật toán Manacher

Để tính $d_{odd}[]$, ta có đoạn code sau. Một số điểm cần lưu ý:

 - $i$ là chỉ số của ký tự làm tâm xâu đối xứng hiện tại.
 - Nếu $i$ vượt quá $r$, $d_{odd}[i]$ được khởi tạo bằng 0.
 - Nếu $i$ không vượt quá $r$, $d_{odd}[i]$ hoặc được khởi tạo bằng $d_{odd}[j]$, trong đó $j$ là vị trí đối xứng của $i$ trong $(l,r)$, hoặc bị giới hạn theo kích thước của xâu đối xứng "bên ngoài".
 - Vòng while biểu diễn thuật toán ngây thơ. Ta chạy nó bất kể giá trị của $k$.
 - Nếu kích thước của xâu đối xứng có tâm tại $i$ là $x$, thì $d_{odd}[i]$ lưu $\frac{x+1}{2}$.

```{.cpp file=manacher_odd}
vector<int> manacher_odd(string s) {
    int n = s.size();
    s = "$" + s + "^";
    vector<int> p(n + 2);
    int l = 0, r = 1;
    for(int i = 1; i <= n; i++) {
        if(i <= r) {
            p[i] = min(r - i, p[l + (r - i)]);
        }
        while(s[i - p[i]] == s[i + p[i]]) {
            p[i]++;
        }
        if(i + p[i] > r) {
            l = i - p[i], r = i + p[i];
        }
    }
    return vector<int>(begin(p) + 1, end(p) - 1);
}
```

## Xử lý tính chẵn lẻ

Dù có thể cài đặt thuật toán Manacher riêng cho độ dài lẻ và chẵn, phiên bản cho độ dài chẵn thường bị xem là khó cài đặt hơn vì kém tự nhiên và dễ dẫn đến lỗi lệch một đơn vị.

Để tránh điều đó, ta có thể quy toàn bộ bài toán về trường hợp chỉ xử lý xâu đối xứng có độ dài lẻ. Cách làm là chèn thêm ký tự `#` giữa mỗi cặp ký tự của chuỗi, đồng thời chèn ở đầu và cuối chuỗi:

$$abcbcba \to \#a\#b\#c\#b\#c\#b\#a\#,$$

$$d = [1,2,1,2,1,4,1,8,1,4,1,2,1,2,1].$$

Như có thể thấy, $d[2i]=2 d_{even}[i]+1$ và $d[2i+1]=2 d_{odd}[i]$ trong đó $d$ là mảng Manacher cho các xâu đối xứng độ dài lẻ trên chuỗi đã được nối bằng `#`, còn $d_{odd}$ và $d_{even}$ là các mảng đã định nghĩa ở trên cho chuỗi ban đầu.

Thật vậy, các ký tự `#` không ảnh hưởng đến các xâu đối xứng độ dài lẻ, vốn vẫn có tâm tại các ký tự của chuỗi ban đầu; còn các xâu đối xứng độ dài chẵn của chuỗi ban đầu giờ trở thành các xâu đối xứng độ dài lẻ của chuỗi mới, có tâm tại các ký tự `#`.

Lưu ý rằng $d[2i]$ và $d[2i+1]$ về bản chất lần lượt bằng độ dài lớn nhất của xâu đối xứng lẻ và chẵn có tâm tại $i$, cộng thêm $1$.

Phép biến đổi được cài đặt như sau:

```cpp
vector<int> manacher(string s) {
    string t;
    for(auto c: s) {
        t += string("#") + c;
    }
    auto res = manacher_odd(t + "#");
    return vector<int>(begin(res) + 1, end(res) - 1);
}
```

Để đơn giản, bài viết không trình bày việc tách mảng thành $d_{odd}$ và $d_{even}$ cũng như cách tính tường minh hai mảng này.

## Bài tập

- [Library Checker - Enumerate Palindromes](https://judge.yosupo.jp/problem/enumerate_palindromes)
- [Longest Palindrome](https://cses.fi/problemset/task/1111)
- [UVA 11475 - Extend to Palindrome](https://onlinejudge.org/index.php?option=com_onlinejudge&Itemid=8&category=26&page=show_problem&problem=2470)
- [GYM - (Q) QueryreuQ](https://codeforces.com/gym/101806/problem/Q)
- [CF - Prefix-Suffix Palindrome](https://codeforces.com/contest/1326/problem/D2)
- [SPOJ - Number of Palindromes](https://www.spoj.com/problems/NUMOFPAL/)
- [Kattis - Palindromes](https://open.kattis.com/problems/palindromes)
