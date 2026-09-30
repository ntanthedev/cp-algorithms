---
tags:
  - Translated
e_maxx_link: bracket_sequences
translation:
  source: combinatorics/bracket_sequences.md
  source_commit: e24a18cb0736f244f1d7455d0f58a50e72c65acf
  status: draft
  last_synced: 2026-09-30
---

# Dãy ngoặc đúng

Một **dãy ngoặc đúng (balanced bracket sequence)** là một xâu chỉ gồm các dấu ngoặc sao cho khi chèn thêm một số số và phép toán thích hợp vào dãy này, ta thu được một biểu thức toán học hợp lệ.
Có thể định nghĩa hình thức dãy ngoặc đúng như sau:

- $e$ (xâu rỗng) là một dãy ngoặc đúng.
- nếu $s$ là một dãy ngoặc đúng thì $(s)$ cũng là một dãy ngoặc đúng.
- nếu $s$ và $t$ là các dãy ngoặc đúng thì $s t$ cũng là một dãy ngoặc đúng.

Chẳng hạn, $(())()$ là một dãy ngoặc đúng, còn $())($ thì không.

Tương tự, ta cũng có thể định nghĩa các dãy ngoặc dùng nhiều loại ngoặc.

Trong bài viết này, ta xét một số bài toán kinh điển liên quan đến dãy ngoặc đúng (để đơn giản, từ đây ta chỉ gọi là dãy): kiểm tra tính đúng, đếm số dãy, tìm dãy kế tiếp theo thứ tự từ điển, sinh tất cả dãy có kích thước nhất định, tìm chỉ số của một dãy và sinh dãy thứ $k$.
Ta cũng sẽ xét hai biến thể của các bài toán: trường hợp đơn giản chỉ cho phép một loại ngoặc và trường hợp khó hơn có nhiều loại ngoặc.

## Kiểm tra tính đúng

Ta cần kiểm tra một xâu đã cho có phải là dãy ngoặc đúng hay không.

Trước tiên, giả sử chỉ có một loại ngoặc.
Trong trường hợp này có một thuật toán rất đơn giản.
Gọi $\text{depth}$ là số ngoặc mở hiện tại chưa được đóng.
Ban đầu $\text{depth} = 0$.
Ta duyệt tất cả ký tự của xâu; nếu ký tự ngoặc hiện tại là ngoặc mở thì tăng $\text{depth}$, ngược lại thì giảm nó.
Nếu tại bất kỳ thời điểm nào biến $\text{depth}$ trở thành số âm, hoặc khi kết thúc nó khác $0$, thì xâu không phải là một dãy ngoặc đúng.
Ngược lại, xâu là dãy ngoặc đúng.

Nếu có nhiều loại ngoặc thì cần thay đổi thuật toán.
Thay vì một bộ đếm $\text{depth}$, ta tạo một stack để lưu tất cả các ngoặc mở đã gặp.
Nếu ký tự ngoặc hiện tại là ngoặc mở, ta đẩy nó vào stack.
Nếu đó là ngoặc đóng, ta kiểm tra stack có khác rỗng hay không và phần tử trên đỉnh stack có cùng loại với ngoặc đóng hiện tại hay không.
Nếu cả hai điều kiện đều được thỏa mãn, ta lấy ngoặc mở đó ra khỏi stack.
Nếu tại bất kỳ thời điểm nào một trong hai điều kiện không được thỏa mãn, hoặc khi kết thúc stack vẫn không rỗng, thì xâu không phải là dãy ngoặc đúng.
Ngược lại, xâu là dãy ngoặc đúng.

## Số lượng dãy ngoặc đúng

### Công thức

Số dãy ngoặc đúng chỉ dùng một loại ngoặc có thể được tính bằng [số Catalan](catalan-numbers.md).
Số dãy ngoặc đúng có độ dài $2n$ ($n$ cặp ngoặc) là:

$$\frac{1}{n+1} \binom{2n}{n}$$

Nếu cho phép $k$ loại ngoặc, thì mỗi cặp có thể thuộc bất kỳ một trong $k$ loại (độc lập với các cặp khác), do đó số dãy ngoặc đúng là:

$$\frac{1}{n+1} \binom{2n}{n} k^n$$

### Quy hoạch động

Mặt khác, các số này cũng có thể được tính bằng **quy hoạch động**.
Gọi $d[n]$ là số dãy ngoặc đúng có $n$ cặp ngoặc.
Lưu ý rằng vị trí đầu tiên luôn là một ngoặc mở.
Ở một vị trí nào đó phía sau sẽ là ngoặc đóng tương ứng với nó.
Rõ ràng bên trong cặp ngoặc này là một dãy ngoặc đúng, và tương tự, phần nằm sau cặp ngoặc này cũng là một dãy ngoặc đúng.
Vì vậy, để tính $d[n]$, ta xét có bao nhiêu dãy ngoặc đúng gồm $i$ cặp nằm bên trong cặp ngoặc đầu tiên và có bao nhiêu dãy ngoặc đúng gồm $n-1-i$ cặp nằm phía sau cặp đó.
Do đó, ta có công thức:

$$d[n] = \sum_{i=0}^{n-1} d[i] \cdot d[n-1-i]$$

Giá trị khởi tạo cho truy hồi này là $d[0] = 1$.

## Tìm dãy ngoặc đúng kế tiếp theo thứ tự từ điển

Ở đây ta chỉ xét trường hợp có một loại ngoặc hợp lệ.

Cho một dãy ngoặc đúng, ta cần tìm dãy ngoặc đúng kế tiếp theo thứ tự từ điển.

Ta cần tìm ngoặc mở ngoài cùng bên phải có thể thay bằng ngoặc đóng mà vẫn duy trì điều kiện để dãy còn có thể hoàn thành thành một dãy ngoặc đúng.
Sau khi thay vị trí này, ta có thể điền phần còn lại của xâu bằng hậu tố nhỏ nhất theo thứ tự từ điển: trước hết đặt nhiều ngoặc mở nhất có thể, sau đó điền các vị trí còn lại bằng ngoặc đóng.
Nói cách khác, ta cố giữ nguyên một tiền tố dài nhất có thể và thay hậu tố bằng hậu tố nhỏ nhất theo thứ tự từ điển.

Để tìm vị trí này, ta có thể duyệt các ký tự từ phải sang trái và duy trì độ cân bằng $\text{depth}$ giữa ngoặc mở và ngoặc đóng.
Khi gặp một ngoặc mở, ta giảm $\text{depth}$; khi gặp một ngoặc đóng, ta tăng nó.
Nếu tại một vị trí ta gặp ngoặc mở và độ cân bằng sau khi xử lý ký tự này là dương, thì ta đã tìm được vị trí ngoài cùng bên phải có thể thay đổi.
Ta thay ký tự đó, tính số ngoặc mở và ngoặc đóng cần thêm vào phía bên phải, rồi sắp chúng theo cách nhỏ nhất theo thứ tự từ điển.

Nếu không tìm thấy vị trí phù hợp thì dãy hiện tại đã là dãy lớn nhất có thể và không có đáp án.

```{.cpp file=next_balanced_brackets_sequence}
bool next_balanced_sequence(string & s) {
    int n = s.size();
    int depth = 0;
    for (int i = n - 1; i >= 0; i--) {
        if (s[i] == '(')
            depth--;
        else
            depth++;

        if (s[i] == '(' && depth > 0) {
            depth--;
            int open = (n - i - 1 - depth) / 2;
            int close = n - i - 1 - open;
            string next = s.substr(0, i) + ')' + string(open, '(') + string(close, ')');
            s.swap(next);
            return true;
        }
    }
    return false;
}
```

Hàm này tính dãy ngoặc đúng kế tiếp trong thời gian $O(n)$ và trả về false nếu không có dãy kế tiếp.

## Tìm tất cả dãy ngoặc đúng

Đôi khi ta cần tìm và in ra tất cả các dãy ngoặc đúng có độ dài cho trước $n$.

Để sinh chúng, ta có thể bắt đầu với dãy nhỏ nhất theo thứ tự từ điển $((\dots(())\dots))$, sau đó liên tục tìm dãy kế tiếp theo thứ tự từ điển bằng thuật toán ở mục trước.

Tuy nhiên, nếu độ dài của dãy không quá lớn (chẳng hạn $n$ nhỏ hơn $12$), ta cũng có thể thuận tiện sinh mọi hoán vị bằng hàm `next_permutation` của C++ STL rồi kiểm tra từng dãy có đúng hay không.

Ngoài ra, ta có thể sinh các dãy bằng những ý tưởng đã dùng để đếm tất cả các dãy bằng quy hoạch động.
Ta sẽ trình bày các ý tưởng này trong hai mục tiếp theo.

## Chỉ số của dãy

Cho một dãy ngoặc đúng có $n$ cặp ngoặc.
Ta cần tìm chỉ số của nó trong danh sách tất cả các dãy ngoặc đúng có $n$ cặp ngoặc được sắp theo thứ tự từ điển.

Ta định nghĩa một mảng phụ $d[i][j]$, trong đó $i$ là độ dài của dãy ngoặc (bán cân bằng: mỗi ngoặc đóng đều có một ngoặc mở tương ứng, nhưng không phải mọi ngoặc mở đều nhất thiết đã có ngoặc đóng tương ứng), và $j$ là độ cân bằng hiện tại (hiệu giữa số ngoặc mở và ngoặc đóng).
$d[i][j]$ là số dãy như vậy thỏa các tham số trên.
Ta sẽ tính các giá trị này với chỉ một loại ngoặc.

Với giá trị khởi đầu $i = 0$, đáp án là hiển nhiên: $d[0][0] = 1$, và $d[0][j] = 0$ với $j > 0$.
Bây giờ xét $i > 0$ và ký tự cuối cùng của dãy.
Nếu ký tự cuối là ngoặc mở $($, thì trạng thái trước đó là $(i-1, j-1)$; nếu là ngoặc đóng $)$, thì trạng thái trước đó là $(i-1, j+1)$.
Do đó, ta nhận được công thức truy hồi:

$$d[i][j] = d[i-1][j-1] + d[i-1][j+1]$$

Hiển nhiên $d[i][j] = 0$ với $j$ âm.
Vì vậy, ta có thể tính mảng này trong $O(n^2)$.

Bây giờ ta sẽ tính chỉ số của một dãy đã cho.

Trước hết, giả sử chỉ có một loại ngoặc.
Ta dùng bộ đếm $\text{depth}$ cho biết độ sâu lồng nhau hiện tại và duyệt các ký tự của dãy.
Nếu ký tự hiện tại $s[i]$ bằng $($, ta tăng $\text{depth}$.
Nếu ký tự hiện tại $s[i]$ bằng $)$, ta cần cộng $d[2n-i-1][\text{depth}+1]$ vào đáp án, tức là tính tất cả các hậu tố có thể bắt đầu bằng $($ (những dãy này nhỏ hơn theo thứ tự từ điển), rồi giảm $\text{depth}$.

Bây giờ giả sử có $k$ loại ngoặc khác nhau.

Khi xét ký tự hiện tại $s[i]$ trước khi cập nhật lại $\text{depth}$, ta phải duyệt qua tất cả các loại ngoặc nhỏ hơn ký tự hiện tại và thử đặt ngoặc đó vào vị trí hiện tại (thu được độ cân bằng mới $\text{ndepth} = \text{depth} \pm 1$), rồi cộng số cách hoàn thành phần còn lại của dãy (độ dài $2n-i-1$, độ cân bằng $ndepth$) vào đáp án:

$$d[2n - i - 1][\text{ndepth}] \cdot k^{\frac{2n - i - 1 - ndepth}{2}}$$

Công thức này có thể được suy ra như sau:
Trước hết, ta tạm "quên" rằng có nhiều loại ngoặc và lấy đáp án $d[2n - i - 1][\text{ndepth}]$.
Bây giờ xét đáp án thay đổi thế nào khi có $k$ loại ngoặc.
Ta có $2n - i - 1$ vị trí chưa xác định, trong đó $\text{ndepth}$ vị trí đã được xác định bởi các ngoặc mở.
Tất cả các ngoặc còn lại ($(2n - i - 1 - \text{ndepth})/2$ cặp) có thể thuộc bất kỳ loại nào, vì vậy ta nhân số cách với lũy thừa tương ứng của $k$.

## Tìm dãy thứ $k$ {data-toc-label="Finding the k-th sequence"}

Gọi $n$ là số cặp ngoặc trong dãy.
Ta cần tìm dãy ngoặc đúng thứ $k$ trong danh sách tất cả các dãy ngoặc đúng được sắp theo thứ tự từ điển với một $k$ cho trước.

Tương tự mục trước, ta tính mảng phụ $d[i][j]$, là số dãy ngoặc bán cân bằng có độ dài $i$ và độ cân bằng $j$.

Trước hết, ta xét trường hợp chỉ có một loại ngoặc.

Ta sẽ duyệt qua các ký tự của xâu cần sinh.
Như trong bài toán trước, ta lưu bộ đếm $\text{depth}$ là độ sâu lồng nhau hiện tại.
Ở mỗi vị trí, ta cần quyết định đặt ngoặc mở hay ngoặc đóng. Để đặt ngoặc mở, điều kiện $d[2n - i - 1][\text{depth}+1] \ge k$ phải đúng.
Nếu đúng, ta tăng bộ đếm $\text{depth}$ rồi chuyển sang ký tự tiếp theo.
Nếu không, ta giảm $k$ đi $d[2n - i - 1][\text{depth}+1]$, đặt một ngoặc đóng rồi tiếp tục.

```{.cpp file=kth_balances_bracket}
string kth_balanced(int n, int k) {
    vector<vector<int>> d(2*n+1, vector<int>(n+1, 0));
    d[0][0] = 1;
    for (int i = 1; i <= 2*n; i++) {
        d[i][0] = d[i-1][1];
        for (int j = 1; j < n; j++)
            d[i][j] = d[i-1][j-1] + d[i-1][j+1];
        d[i][n] = d[i-1][n-1];
    }

    string ans;
    int depth = 0;
    for (int i = 0; i < 2*n; i++) {
        if (depth + 1 <= n && d[2*n-i-1][depth+1] >= k) {
            ans += '(';
            depth++;
        } else {
            ans += ')';
            if (depth + 1 <= n)
                k -= d[2*n-i-1][depth+1];
            depth--;
        }
    }
    return ans;
}
```

Bây giờ giả sử có $k$ loại ngoặc.
Lời giải chỉ khác một chút: ta cần nhân giá trị $d[2n-i-1][\text{ndepth}]$ với $k^{(2n-i-1-\text{ndepth})/2}$ và xét đến việc ký tự tiếp theo có thể thuộc nhiều loại ngoặc khác nhau.

Dưới đây là cài đặt dùng hai loại ngoặc: ngoặc tròn và ngoặc vuông:

```{.cpp file=kth_balances_bracket_multiple}
string kth_balanced2(int n, int k) {
    vector<vector<int>> d(2*n+1, vector<int>(n+1, 0));
    d[0][0] = 1;
    for (int i = 1; i <= 2*n; i++) {
        d[i][0] = d[i-1][1];
        for (int j = 1; j < n; j++)
            d[i][j] = d[i-1][j-1] + d[i-1][j+1];
        d[i][n] = d[i-1][n-1];
    }

    string ans;
    int shift, depth = 0;

    stack<char> st;
    for (int i = 0; i < 2*n; i++) {

        // '('
        shift = ((2*n-i-1-depth-1) / 2);
        if (shift >= 0 && depth + 1 <= n) {
            int cnt = d[2*n-i-1][depth+1] << shift;
            if (cnt >= k) {
                ans += '(';
                st.push('(');
                depth++;
                continue;
            }
            k -= cnt;
        }

        // ')'
        shift = ((2*n-i-1-depth+1) / 2);
        if (shift >= 0 && depth && st.top() == '(') {
            int cnt = d[2*n-i-1][depth-1] << shift;
            if (cnt >= k) {
                ans += ')';
                st.pop();
                depth--;
                continue;
            }
            k -= cnt;
        }
            
        // '['
        shift = ((2*n-i-1-depth-1) / 2);
        if (shift >= 0 && depth + 1 <= n) {
            int cnt = d[2*n-i-1][depth+1] << shift;
            if (cnt >= k) {
                ans += '[';
                st.push('[');
                depth++;
                continue;
            }
            k -= cnt;
        }

        // ']'
        ans += ']';
        st.pop();
        depth--;
    }
    return ans;
}
```
