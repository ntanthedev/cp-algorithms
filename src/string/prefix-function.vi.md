---
tags:
  - Translated
e_maxx_link: prefix_function
translation:
  source: string/prefix-function.md
  source_commit: 94d3efc3e3f788f47aa1815e77e17c9ecb71fbd5
  status: draft
  last_synced: 2026-08-07
---

# Hàm tiền tố. Thuật toán Knuth–Morris–Pratt

## Định nghĩa hàm tiền tố

Cho một chuỗi $s$ có độ dài $n$.
**Hàm tiền tố** của chuỗi này được định nghĩa là một mảng $\pi$ có độ dài $n$, trong đó $\pi[i]$ là độ dài của tiền tố thực sự dài nhất của chuỗi con $s[0 \dots i]$ đồng thời cũng là hậu tố của chính chuỗi con đó.
Một tiền tố thực sự của một chuỗi là tiền tố không bằng toàn bộ chuỗi.
Theo định nghĩa, $\pi[0] = 0$.

Về mặt toán học, định nghĩa của hàm tiền tố có thể được viết như sau:

$$\pi[i] = \max_ {k = 0 \dots i} \{k : s[0 \dots k-1] = s[i-(k-1) \dots i] \}$$

Ví dụ, hàm tiền tố của chuỗi "abcabcd" là $[0, 0, 0, 1, 2, 3, 0]$, còn hàm tiền tố của chuỗi "aabaaab" là $[0, 1, 0, 1, 2, 2, 3]$.

## Thuật toán ngây thơ

Một thuật toán bám trực tiếp theo định nghĩa của hàm tiền tố như sau:

```{.cpp file=prefix_slow}
vector<int> prefix_function(string s) {
    int n = (int)s.length();
    vector<int> pi(n);
    for (int i = 0; i < n; i++)
        for (int k = 0; k <= i; k++)
            if (s.substr(0, k) == s.substr(i-k+1, k))
                pi[i] = k;
    return pi;
}
```

Dễ thấy độ phức tạp của thuật toán là $O(n^3)$, vì vậy vẫn còn nhiều chỗ để cải thiện.

## Thuật toán hiệu quả

Thuật toán này được Knuth và Pratt đề xuất, đồng thời Morris cũng độc lập đề xuất vào năm 1977.
Nó được dùng làm thành phần chính của một thuật toán tìm kiếm chuỗi con.

### Tối ưu thứ nhất

Nhận xét quan trọng đầu tiên là giá trị của hàm tiền tố chỉ có thể tăng nhiều nhất một đơn vị.

Thật vậy, nếu không phải vậy, giả sử $\pi[i + 1] \gt \pi[i] + 1$, ta có thể lấy hậu tố kết thúc tại vị trí $i + 1$ có độ dài $\pi[i + 1]$ rồi bỏ ký tự cuối cùng của nó.
Khi đó ta thu được một hậu tố kết thúc tại vị trí $i$ có độ dài $\pi[i + 1] - 1$, tốt hơn $\pi[i]$, tạo thành mâu thuẫn.

Hình minh họa sau cho thấy mâu thuẫn này.
Hậu tố thực sự dài nhất tại vị trí $i$ đồng thời là một tiền tố có độ dài $2$, còn tại vị trí $i+1$ độ dài đó là $4$.
Do đó chuỗi $s_0 ~ s_1 ~ s_2 ~ s_3$ bằng chuỗi $s_{i-2} ~ s_{i-1} ~ s_i ~ s_{i+1}$, suy ra các chuỗi $s_0 ~ s_1 ~ s_2$ và $s_{i-2} ~ s_{i-1} ~ s_i$ cũng bằng nhau, vì thế $\pi[i]$ phải bằng $3$.

$$\underbrace{\overbrace{s_0 ~ s_1}^{\pi[i] = 2} ~ s_2 ~ s_3}_{\pi[i+1] = 4} ~ \dots ~ \underbrace{s_{i-2} ~ \overbrace{s_{i-1} ~ s_{i}}^{\pi[i] = 2} ~ s_{i+1}}_{\pi[i+1] = 4}$$

Vì vậy khi chuyển sang vị trí tiếp theo, giá trị hàm tiền tố có thể tăng một, giữ nguyên hoặc giảm đi một lượng nào đó.
Chỉ riêng tính chất này đã cho phép giảm độ phức tạp xuống $O(n^2)$, vì trong một bước hàm tiền tố tăng nhiều nhất một đơn vị.
Tổng cộng hàm chỉ có thể tăng tối đa $n$ bước, nên tổng số bước giảm cũng chỉ tối đa $n$.
Điều đó có nghĩa ta chỉ cần thực hiện $O(n)$ phép so sánh chuỗi và đạt độ phức tạp $O(n^2)$.

### Tối ưu thứ hai

Ta tiếp tục loại bỏ các phép so sánh chuỗi.
Để làm được điều này, ta phải tận dụng toàn bộ thông tin đã tính ở các bước trước.

Giả sử ta đang tính giá trị hàm tiền tố $\pi$ cho $i + 1$.
Nếu $s[i+1] = s[\pi[i]]$, ta có thể khẳng định $\pi[i+1] = \pi[i] + 1$, vì đã biết hậu tố tại vị trí $i$ có độ dài $\pi[i]$ bằng tiền tố có cùng độ dài.
Điều này tiếp tục được minh họa bằng ví dụ sau.

$$\underbrace{\overbrace{s_0 ~ s_1 ~ s_2}^{\pi[i]} ~ \overbrace{s_3}^{s_3 = s_{i+1}}}_{\pi[i+1] = \pi[i] + 1} ~ \dots ~ \underbrace{\overbrace{s_{i-2} ~ s_{i-1} ~ s_{i}}^{\pi[i]} ~ \overbrace{s_{i+1}}^{s_3 = s_{i + 1}}}_{\pi[i+1] = \pi[i] + 1}$$

Nếu không phải vậy, tức $s[i+1] \neq s[\pi[i]]$, ta cần thử một chuỗi ngắn hơn.
Để tăng tốc, ta muốn chuyển ngay tới độ dài lớn nhất $j \lt \pi[i]$ sao cho tính chất tiền tố vẫn đúng tại vị trí $i$, tức $s[0 \dots j-1] = s[i-j+1 \dots i]$:

$$\overbrace{\underbrace{s_0 ~ s_1}_j ~ s_2 ~ s_3}^{\pi[i]} ~ \dots ~ \overbrace{s_{i-3} ~ s_{i-2} ~ \underbrace{s_{i-1} ~ s_{i}}_j}^{\pi[i]} ~ s_{i+1}$$

Nếu tìm được độ dài $j$ như vậy, ta lại chỉ cần so sánh hai ký tự $s[i+1]$ và $s[j]$.
Nếu chúng bằng nhau, ta gán $\pi[i+1] = j + 1$.
Ngược lại, ta cần tìm giá trị lớn nhất nhỏ hơn $j$ mà tính chất tiền tố vẫn đúng, rồi tiếp tục như vậy.
Quá trình có thể đi tới $j = 0$.
Nếu lúc đó $s[i+1] = s[0]$, ta gán $\pi[i+1] = 1$, còn không thì $\pi[i+1] = 0$.

Như vậy ta đã có khung tổng quát của thuật toán.
Câu hỏi còn lại là làm sao tìm hiệu quả các độ dài dành cho $j$.
Nhắc lại rằng:
với độ dài hiện tại $j$ tại vị trí $i$ mà tính chất tiền tố đúng, tức $s[0 \dots j-1] = s[i-j+1 \dots i]$, ta muốn tìm $k \lt j$ lớn nhất mà tính chất tiền tố vẫn đúng.

$$\overbrace{\underbrace{s_0 ~ s_1}_k ~ s_2 ~ s_3}^j ~ \dots ~ \overbrace{s_{i-3} ~ s_{i-2} ~ \underbrace{s_{i-1} ~ s_{i}}_k}^j ~s_{i+1}$$

Hình minh họa cho thấy giá trị này chính là $\pi[j-1]$, vốn đã được tính trước đó.

### Thuật toán hoàn chỉnh

Cuối cùng ta có thể xây dựng một thuật toán không cần so sánh các chuỗi con và chỉ thực hiện $O(n)$ thao tác.

Quy trình đầy đủ như sau:

- Ta tính các giá trị tiền tố $\pi[i]$ trong một vòng lặp từ $i = 1$ đến $i = n-1$ ($\pi[0]$ chỉ được gán bằng $0$).
- Để tính giá trị hiện tại $\pi[i]$, đặt biến $j$ là độ dài hậu tố tốt nhất đối với $i-1$. Ban đầu $j = \pi[i-1]$.
- Kiểm tra xem hậu tố có độ dài $j+1$ có đồng thời là tiền tố hay không bằng cách so sánh $s[j]$ và $s[i]$.
Nếu chúng bằng nhau, gán $\pi[i] = j + 1$; nếu không, giảm $j$ xuống $\pi[j-1]$ rồi lặp lại bước này.
- Nếu đã đạt $j = 0$ mà vẫn không khớp, gán $\pi[i] = 0$ rồi chuyển sang chỉ số tiếp theo $i + 1$.

### Cài đặt

Cài đặt cuối cùng khá ngắn gọn và dễ đọc.

```{.cpp file=prefix_fast}
vector<int> prefix_function(string s) {
    int n = (int)s.length();
    vector<int> pi(n);
    for (int i = 1; i < n; i++) {
        int j = pi[i-1];
        while (j > 0 && s[i] != s[j])
            j = pi[j-1];
        if (s[i] == s[j])
            j++;
        pi[i] = j;
    }
    return pi;
}
```

Đây là một thuật toán **online**, tức nó xử lý dữ liệu ngay khi dữ liệu xuất hiện — chẳng hạn có thể đọc từng ký tự của chuỗi và xử lý ngay, tìm giá trị hàm tiền tố cho mỗi ký tự tiếp theo.
Thuật toán vẫn cần lưu chính chuỗi và các giá trị hàm tiền tố đã tính trước đó, nhưng nếu biết trước giá trị lớn nhất $M$ mà hàm tiền tố có thể đạt trên chuỗi, ta chỉ cần lưu $M+1$ ký tự đầu tiên của chuỗi và cùng số lượng giá trị hàm tiền tố.

## Ứng dụng

### Tìm một chuỗi con trong chuỗi. Thuật toán Knuth–Morris–Pratt

Đây là ứng dụng kinh điển của hàm tiền tố.

Cho một văn bản $t$ và một chuỗi $s$, ta muốn tìm và in ra vị trí của mọi lần chuỗi $s$ xuất hiện trong văn bản $t$.

Để thuận tiện, gọi $n$ là độ dài chuỗi s và $m$ là độ dài văn bản $t$.

Ta tạo chuỗi $s + \# + t$, trong đó $\#$ là ký tự phân cách không xuất hiện trong cả $s$ lẫn $t$.
Hãy tính hàm tiền tố cho chuỗi này.
Bây giờ xét ý nghĩa của các giá trị hàm tiền tố, ngoại trừ $n + 1$ phần tử đầu tiên (thuộc chuỗi $s$ và ký tự phân cách).
Theo định nghĩa, giá trị $\pi[i]$ cho biết độ dài lớn nhất của một chuỗi con kết thúc tại vị trí $i$ và trùng với tiền tố.
Trong trường hợp này, đó chính là khối dài nhất trùng với $s$ và kết thúc tại vị trí $i$.
Độ dài này không thể lớn hơn $n$ do có ký tự phân cách.
Nếu đạt $\pi[i] = n$, điều đó có nghĩa chuỗi $s$ xuất hiện đầy đủ tại đây, tức kết thúc ở vị trí $i$.
Chỉ cần nhớ rằng các vị trí đang được đánh chỉ số trong chuỗi $s + \# + t$.

Vì vậy, nếu tại vị trí $i$ ta có $\pi[i] = n$, thì trong chuỗi $t$, chuỗi $s$ xuất hiện tại vị trí $i - (n + 1) - n + 1 = i - 2n$.

Như đã nói khi mô tả cách tính hàm tiền tố, nếu biết các giá trị tiền tố không bao giờ vượt quá một giá trị nhất định, ta không cần lưu toàn bộ chuỗi và toàn bộ hàm mà chỉ cần lưu phần đầu của chúng.
Trong trường hợp này, ta chỉ cần lưu chuỗi $s + \#$ và các giá trị hàm tiền tố của nó.
Ta có thể đọc từng ký tự của chuỗi $t$ và tính giá trị hàm tiền tố hiện tại.

Như vậy thuật toán Knuth–Morris–Pratt giải bài toán trong $O(n + m)$ thời gian và dùng $O(n)$ bộ nhớ.

### Đếm số lần xuất hiện của mỗi tiền tố

Ở đây ta xét đồng thời hai bài toán.
Cho chuỗi $s$ có độ dài $n$.
Trong biến thể thứ nhất, ta muốn đếm số lần mỗi tiền tố $s[0 \dots i]$ xuất hiện trong chính chuỗi đó.
Trong biến thể thứ hai, ta được cho thêm một chuỗi $t$ và muốn đếm số lần mỗi tiền tố $s[0 \dots i]$ xuất hiện trong $t$.

Trước tiên giải bài toán thứ nhất.
Xét giá trị hàm tiền tố $\pi[i]$ tại vị trí $i$.
Theo định nghĩa, tiền tố có độ dài $\pi[i]$ của chuỗi $s$ xuất hiện và kết thúc tại vị trí $i$, và không có tiền tố dài hơn nào thỏa điều kiện này.
Đồng thời, các tiền tố ngắn hơn cũng có thể kết thúc tại vị trí đó.
Dễ thấy ta gặp lại chính câu hỏi đã giải khi tính hàm tiền tố:
cho một tiền tố có độ dài $j$ đồng thời là hậu tố kết thúc tại vị trí $i$, tiền tố nhỏ hơn tiếp theo $\lt j$ cũng là hậu tố kết thúc tại vị trí $i$ là gì?
Vì vậy tại vị trí $i$ kết thúc tiền tố độ dài $\pi[i]$, tiền tố độ dài $\pi[\pi[i] - 1]$, tiền tố $\pi[\pi[\pi[i] - 1] - 1]$, và cứ tiếp tục như vậy cho tới khi chỉ số trở thành 0.
Ta có thể tính đáp án như sau.

```{.cpp file=prefix_count_each_prefix}
vector<int> ans(n + 1);
for (int i = 0; i < n; i++)
    ans[pi[i]]++;
for (int i = n-1; i > 0; i--)
    ans[pi[i-1]] += ans[i];
for (int i = 0; i <= n; i++)
    ans[i]++;
```

Đầu tiên, với mỗi giá trị của hàm tiền tố ta đếm số lần nó xuất hiện trong mảng $\pi$, sau đó tính đáp án cuối cùng:
nếu biết tiền tố độ dài $i$ xuất hiện đúng $\text{ans}[i]$ lần, số này phải được cộng vào số lần xuất hiện của hậu tố dài nhất của nó đồng thời là tiền tố.
Cuối cùng cần cộng thêm $1$ vào mỗi kết quả, vì bản thân các tiền tố ban đầu cũng phải được tính.

Bây giờ xét bài toán thứ hai.
Ta áp dụng mẹo từ Knuth–Morris–Pratt:
tạo chuỗi $s + \# + t$ và tính hàm tiền tố của nó.
Khác biệt duy nhất so với bài toán thứ nhất là ta chỉ quan tâm các giá trị tiền tố thuộc phần chuỗi $t$, tức $\pi[i]$ với $i \ge n + 1$.
Với các giá trị đó, ta thực hiện đúng các phép tính như ở bài toán thứ nhất.

### Số lượng chuỗi con khác nhau trong một chuỗi

Cho chuỗi $s$ có độ dài $n$.
Ta muốn tính số lượng chuỗi con khác nhau xuất hiện trong đó.

Ta giải bài toán theo cách lặp dần.
Cụ thể, giả sử đã biết số chuỗi con khác nhau hiện tại, ta sẽ tìm cách cập nhật số lượng này khi thêm một ký tự vào cuối.

Gọi $k$ là số chuỗi con khác nhau hiện có trong $s$, rồi thêm ký tự $c$ vào cuối $s$.
Hiển nhiên sẽ xuất hiện một số chuỗi con mới kết thúc bằng $c$.
Ta muốn đếm những chuỗi con mới chưa từng xuất hiện trước đó.

Lấy chuỗi $t = s + c$ rồi đảo ngược nó.
Bài toán trở thành đếm xem có bao nhiêu tiền tố không xuất hiện ở nơi nào khác.
Nếu tính giá trị lớn nhất của hàm tiền tố $\pi_{\text{max}}$ trên chuỗi đảo ngược $t$, thì tiền tố dài nhất xuất hiện trong $s$ có độ dài $\pi_{\text{max}}$.
Rõ ràng mọi tiền tố ngắn hơn cũng xuất hiện trong đó.

Do đó số chuỗi con mới xuất hiện khi thêm ký tự $c$ là $|s| + 1 - \pi_{\text{max}}$.

Với mỗi ký tự được thêm vào, ta có thể tính số chuỗi con mới trong $O(n)$ lần, nên tổng độ phức tạp thời gian là $O(n^2)$.

Cũng cần lưu ý rằng ta có thể tính số chuỗi con khác nhau khi thêm ký tự ở đầu, hoặc khi xóa ký tự ở đầu hay cuối chuỗi.

### Nén chuỗi

Cho chuỗi $s$ có độ dài $n$.
Ta muốn tìm biểu diễn "nén" ngắn nhất của chuỗi, tức tìm chuỗi $t$ có độ dài nhỏ nhất sao cho $s$ có thể được biểu diễn bằng phép nối một hoặc nhiều bản sao của $t$.

Rõ ràng ta chỉ cần tìm độ dài của $t$. Khi biết độ dài, đáp án chính là tiền tố của $s$ có độ dài đó.

Tính hàm tiền tố của $s$.
Dùng giá trị cuối cùng để định nghĩa $k = n - \pi[n - 1]$.
Ta sẽ chứng minh rằng nếu $k$ chia hết $n$ thì $k$ là đáp án; nếu không thì không thể nén hiệu quả và đáp án là $n$.

Giả sử $n$ chia hết cho $k$.
Khi đó chuỗi có thể được chia thành các khối có độ dài $k$.
Theo định nghĩa hàm tiền tố, tiền tố độ dài $n - k$ bằng hậu tố của nó.
Điều này có nghĩa khối cuối cùng bằng khối ngay trước nó.
Khối ngay trước lại phải bằng khối đứng trước nữa.
Và cứ tiếp tục như vậy.
Kết quả là mọi khối đều bằng nhau, vì thế có thể nén chuỗi $s$ xuống độ dài $k$.

Ta vẫn cần chứng minh đây thực sự là tối ưu.
Nếu tồn tại cách nén ngắn hơn $k$, giá trị hàm tiền tố ở cuối sẽ lớn hơn $n - k$.
Do đó $k$ thực sự là đáp án.

Bây giờ giả sử $n$ không chia hết cho $k$.
Ta sẽ chứng minh điều này kéo theo độ dài đáp án là $n$.
Chứng minh bằng phản chứng.
Giả sử tồn tại đáp án và cách nén có độ dài $p$ ($p$ chia hết $n$).
Khi đó giá trị cuối cùng của hàm tiền tố phải lớn hơn $n - p$, tức hậu tố sẽ phủ một phần khối đầu tiên.
Xét khối thứ hai của chuỗi.
Vì tiền tố bằng hậu tố, cả hai cùng phủ khối này và độ dịch tương đối giữa chúng là $k$ không chia hết độ dài khối $p$ (nếu không $k$ sẽ chia hết $n$), nên mọi ký tự của khối phải giống nhau.
Nhưng khi đó chuỗi chỉ gồm một ký tự lặp đi lặp lại, do đó có thể nén xuống chuỗi độ dài $1$, suy ra $k = 1$ và $k$ chia hết $n$.
Mâu thuẫn.

$$\overbrace{s_0 ~ s_1 ~ s_2 ~ s_3}^p ~ \overbrace{s_4 ~ s_5 ~ s_6 ~ s_7}^p$$

$$s_0 ~ s_1 ~ s_2 ~ \underbrace{\overbrace{s_3 ~ s_4 ~ s_5 ~ s_6}^p ~ s_7}_{\pi[7] = 5}$$

$$s_4 = s_3, ~ s_5 = s_4, ~ s_6 = s_5, ~ s_7 = s_6 ~ \Rightarrow ~ s_0 = s_1 = s_2 = s_3$$

### Xây dựng automaton theo hàm tiền tố

Quay lại phép nối hai chuỗi qua một ký tự phân cách: với các chuỗi $s$ và $t$, ta tính hàm tiền tố cho chuỗi $s + \# + t$.
Rõ ràng, vì $\#$ là ký tự phân cách, giá trị hàm tiền tố sẽ không bao giờ vượt quá $|s|$.
Suy ra chỉ cần lưu chuỗi $s + \#$ và các giá trị hàm tiền tố của nó, rồi có thể tính hàm tiền tố cho mọi ký tự tiếp theo ngay khi chúng xuất hiện:

$$\underbrace{s_0 ~ s_1 ~ \dots ~ s_{n-1} ~ \#}_{\text{need to store}} ~ \underbrace{t_0 ~ t_1 ~ \dots ~ t_{m-1}}_{\text{do not need to store}}$$

Thật vậy, trong tình huống này, chỉ cần biết ký tự tiếp theo $c \in t$ và giá trị hàm tiền tố ở vị trí trước là đủ để tính giá trị kế tiếp, không cần dùng bất kỳ ký tự trước đó nào của chuỗi $t$ hay giá trị hàm tiền tố tại chúng.

Nói cách khác, ta có thể xây dựng một **automaton** (máy trạng thái hữu hạn): trạng thái hiện tại chính là giá trị hàm tiền tố, còn phép chuyển từ trạng thái này sang trạng thái khác được quyết định bởi ký tự tiếp theo.

Vì vậy, ngay cả khi chưa có chuỗi $t$, ta vẫn có thể xây dựng bảng chuyển $(\text{old}_\pi, c) \rightarrow \text{new}_\pi$ bằng chính thuật toán tính bảng chuyển:

```{.cpp file=prefix_automaton_slow}
void compute_automaton(string s, vector<vector<int>>& aut) {
    s += '#';
    int n = s.size();
    vector<int> pi = prefix_function(s);
    aut.assign(n, vector<int>(26));
    for (int i = 0; i < n; i++) {
        for (int c = 0; c < 26; c++) {
            int j = i;
            while (j > 0 && 'a' + c != s[j])
                j = pi[j-1];
            if ('a' + c == s[j])
                j++;
            aut[i][c] = j;
        }
    }
}
```

Tuy nhiên ở dạng này, với bảng chữ cái gồm các chữ cái thường, thuật toán chạy trong $O(n^2 26)$ thời gian.
Ta có thể áp dụng quy hoạch động và tận dụng các phần của bảng đã được tính.
Mỗi khi chuyển từ giá trị $j$ sang $\pi[j-1]$, thực chất ta nói rằng phép chuyển $(j, c)$ dẫn đến cùng trạng thái với phép chuyển $(\pi[j-1], c)$, mà đáp án này đã được tính chính xác trước đó.

```{.cpp file=prefix_automaton_fast}
void compute_automaton(string s, vector<vector<int>>& aut) {
    s += '#';
    int n = s.size();
    vector<int> pi = prefix_function(s);
    aut.assign(n, vector<int>(26));
    for (int i = 0; i < n; i++) {
        for (int c = 0; c < 26; c++) {
            if (i > 0 && 'a' + c != s[i])
                aut[i][c] = aut[pi[i-1]][c];
            else
                aut[i][c] = i + ('a' + c == s[i]);
        }
    }
}
```

Kết quả là ta xây dựng automaton trong $O(26 n)$ thời gian.

Khi nào automaton như vậy hữu ích?
Trước hết, nhớ rằng ta dùng hàm tiền tố cho chuỗi $s + \# + t$ và chủ yếu dùng các giá trị của nó cho một mục đích: tìm mọi lần chuỗi $s$ xuất hiện trong chuỗi $t$.

Do đó lợi ích dễ thấy nhất của automaton là **tăng tốc việc tính hàm tiền tố** cho chuỗi $s + \# + t$.
Sau khi xây dựng automaton cho $s + \#$, ta không còn cần lưu chuỗi $s$ hay các giá trị hàm tiền tố của nó.
Mọi phép chuyển đã được tính sẵn trong bảng.

Nhưng còn một ứng dụng thứ hai ít hiển nhiên hơn.
Ta có thể dùng automaton khi chuỗi $t$ là một **chuỗi khổng lồ được xây dựng theo một số quy tắc**.
Ví dụ, đó có thể là các chuỗi Gray hoặc một chuỗi được hình thành bằng cách kết hợp đệ quy một số chuỗi ngắn từ đầu vào.

Để đầy đủ, ta giải một bài toán như sau:
cho số $k \le 10^5$ và chuỗi $s$ có độ dài $\le 10^5$.
Ta cần tính số lần $s$ xuất hiện trong chuỗi Gray thứ $k$.
Nhắc lại rằng các chuỗi Gray được định nghĩa như sau:

$$\begin{align}
g_1 &= \text{"a"}\\
g_2 &= \text{"aba"}\\
g_3 &= \text{"abacaba"}\\
g_4 &= \text{"abacabadabacaba"}
\end{align}$$

Trong những trường hợp như vậy, ngay cả việc tạo chuỗi $t$ cũng là bất khả thi vì độ dài của nó quá lớn.
Chuỗi Gray thứ $k$ có độ dài $2^k-1$ ký tự.
Tuy nhiên, ta có thể tính hiệu quả giá trị hàm tiền tố ở cuối chuỗi chỉ bằng cách biết giá trị hàm tiền tố ở đầu.

Ngoài chính automaton, ta còn tính các giá trị $G[i][j]$ — trạng thái của automaton sau khi xử lý chuỗi $g_i$ bắt đầu từ trạng thái $j$.
Đồng thời tính $K[i][j]$ — số lần $s$ xuất hiện trong $g_i$ khi xử lý $g_i$ bắt đầu từ trạng thái $j$.
Thực chất, $K[i][j]$ là số lần hàm tiền tố đạt giá trị $|s|$ trong quá trình xử lý.
Đáp án của bài toán khi đó là $K[k][0]$.

Làm sao tính các giá trị này?
Trước hết các giá trị cơ sở là $G[0][j] = j$ và $K[0][j] = 0$.
Mọi giá trị tiếp theo có thể được tính từ các giá trị trước đó và automaton.
Để tính cho một $i$ nào đó, nhớ rằng chuỗi $g_i$ gồm $g_{i-1}$, ký tự thứ $i$ của bảng chữ cái và $g_{i-1}$.
Vì vậy automaton sẽ chuyển tới trạng thái:

$$\text{mid} = \text{aut}[G[i-1][j]][i]$$

$$G[i][j] = G[i-1][\text{mid}]$$

Các giá trị $K[i][j]$ cũng có thể được đếm dễ dàng.

$$K[i][j] = K[i-1][j] + (\text{mid} == |s|) + K[i-1][\text{mid}]$$

Nhờ đó ta giải được bài toán với chuỗi Gray, và tương tự là rất nhiều bài toán cùng kiểu khác.
Ví dụ, đúng phương pháp này cũng giải được bài toán sau:
ta được cho chuỗi $s$ và một số mẫu $t_i$, mỗi mẫu được mô tả như sau:
đó là một chuỗi ký tự thông thường, trong đó có thể chứa các phép chèn đệ quy của các chuỗi trước đó dưới dạng $t_k^{\text{cnt}}$, nghĩa là tại vị trí đó phải chèn chuỗi $t_k$ $\text{cnt}$ lần.
Ví dụ về các mẫu như vậy:

$$\begin{align}
t_1 &= \text{"abdeca"}\\
t_2 &= \text{"abc"} + t_1^{30} + \text{"abd"}\\
t_3 &= t_2^{50} + t_1^{100}\\
t_4 &= t_2^{10} + t_3^{100}
\end{align}$$

Các phép thay thế đệ quy làm chuỗi phình rất nhanh, tới mức độ dài có thể đạt cỡ $100^{100}$.

Ta cần tìm số lần chuỗi $s$ xuất hiện trong từng chuỗi.

Bài toán có thể được giải theo cùng cách: xây dựng automaton của hàm tiền tố, rồi tính các phép chuyển cho từng mẫu bằng cách tận dụng kết quả trước đó.

## Bài tập luyện tập

* [UVA # 455 "Periodic Strings"](http://uva.onlinejudge.org/index.php?option=onlinejudge&page=show_problem&problem=396)
* [UVA # 11022 "String Factoring"](http://uva.onlinejudge.org/index.php?option=onlinejudge&page=show_problem&problem=1963)
* [UVA # 11452 "Dancing the Cheeky-Cheeky"](http://uva.onlinejudge.org/index.php?option=onlinejudge&page=show_problem&problem=2447)
* [UVA 12604 - Caesar Cipher](https://uva.onlinejudge.org/index.php?option=com_onlinejudge&Itemid=8&page=show_problem&problem=4282)
* [UVA 12467 - Secret Word](https://uva.onlinejudge.org/index.php?option=com_onlinejudge&Itemid=8&page=show_problem&problem=3911)
* [UVA 11019 - Matrix Matcher](https://uva.onlinejudge.org/index.php?option=onlinejudge&page=show_problem&problem=1960)
* [SPOJ - Pattern Find](http://www.spoj.com/problems/NAJPF/)
* [SPOJ - A Needle in the Haystack](https://www.spoj.com/problems/NHAY/)
* [Codeforces - Anthem of Berland](http://codeforces.com/contest/808/problem/G)
* [Codeforces - MUH and Cube Walls](http://codeforces.com/problemset/problem/471/D)
* [Codeforces - Prefixes and Suffixes](https://codeforces.com/contest/432/problem/D)