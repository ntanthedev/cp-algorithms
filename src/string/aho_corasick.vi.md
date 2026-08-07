---
tags:
  - Translated
e_maxx_link: aho_corasick
translation:
  source: string/aho_corasick.md
  source_commit: 36ec40c7d332da0045c85d4187aff9eb3d6419b4
  status: draft
  last_synced: 2026-08-07
---

# Thuật toán Aho-Corasick

Thuật toán Aho-Corasick cho phép ta nhanh chóng tìm nhiều mẫu trong một văn bản.
Tập các chuỗi mẫu còn được gọi là một _từ điển_.
Ta ký hiệu tổng độ dài của các chuỗi trong từ điển là $m$ và kích thước bảng chữ cái là $k$.
Thuật toán xây dựng một automaton trạng thái hữu hạn dựa trên trie trong thời gian $O(m k)$, sau đó dùng automaton này để xử lý văn bản.

Thuật toán được Alfred Aho và Margaret Corasick đề xuất vào năm 1975.

## Xây dựng trie

<center>
<img src="https://upload.wikimedia.org/wikipedia/commons/e/e2/Trie.svg" width="400px">
<br>
<i>Một trie được xây từ các từ "Java", "Rad", "Rand", "Rau", "Raum" và "Rose".</i>
<br>
<i><a href="https://commons.wikimedia.org/wiki/File:Trie.svg">Hình ảnh</a> của [nd](https://de.wikipedia.org/wiki/Benutzer:Nd) được phân phối theo giấy phép <a href="https://creativecommons.org/licenses/by-sa/3.0/deed.en">CC BY-SA 3.0</a>.</i>
</center>

Về hình thức, trie là một cây có gốc, trong đó mỗi cạnh của cây được gắn nhãn bằng một ký tự
và các cạnh đi ra từ cùng một đỉnh có nhãn khác nhau.

Ta đồng nhất mỗi đỉnh trong trie với chuỗi tạo bởi các nhãn trên đường đi từ gốc đến đỉnh đó.

Mỗi đỉnh còn có một cờ $\text{output}$; cờ này được bật
nếu đỉnh tương ứng với một mẫu trong từ điển.

Theo đó, trie của một tập chuỗi là một trie sao cho mỗi đỉnh $\text{output}$ tương ứng với một chuỗi trong tập, và ngược lại, mỗi chuỗi trong tập tương ứng với một đỉnh $\text{output}$.

Bây giờ ta mô tả cách xây dựng trie cho một tập chuỗi trong thời gian tuyến tính theo tổng độ dài của chúng.

Ta định nghĩa cấu trúc cho các đỉnh của cây:
```{.cpp file=aho_corasick_trie_definition}
const int K = 26;

struct Vertex {
    int next[K];
    bool output = false;

    Vertex() {
        fill(begin(next), end(next), -1);
    }
};

vector<Vertex> trie(1);
```

Ở đây, ta lưu trie dưới dạng một mảng các $\text{Vertex}$.
Mỗi $\text{Vertex}$ chứa cờ $\text{output}$ và các cạnh dưới dạng mảng $\text{next}[]$, trong đó $\text{next}[i]$ là chỉ số của đỉnh ta đến được khi đi theo ký tự $i$, hoặc bằng $-1$ nếu không có cạnh như vậy.
Ban đầu trie chỉ có một đỉnh — đỉnh gốc — với chỉ số $0$.

Tiếp theo ta cài đặt một hàm thêm chuỗi $s$ vào trie.
Cách cài đặt khá đơn giản:
ta bắt đầu ở đỉnh gốc và, miễn là tồn tại các cạnh tương ứng với các ký tự của $s$, ta đi theo chúng.
Nếu không có cạnh cho một ký tự nào đó, ta tạo một đỉnh mới và nối nó bằng một cạnh.
Cuối quá trình, ta bật cờ $\text{output}$ ở đỉnh cuối cùng.

```{.cpp file=aho_corasick_trie_add}
void add_string(string const& s) {
    int v = 0;
    for (char ch : s) {
        int c = ch - 'a';
        if (trie[v].next[c] == -1) {
            trie[v].next[c] = trie.size();
            trie.emplace_back();
        }
        v = trie[v].next[c];
    }
    trie[v].output = true;
}
```

Cài đặt này hiển nhiên chạy trong thời gian tuyến tính,
và vì mỗi đỉnh lưu $k$ liên kết nên nó dùng $O(m k)$ bộ nhớ.

Có thể giảm lượng bộ nhớ xuống $O(m)$ bằng cách dùng map thay cho mảng ở mỗi đỉnh.
Tuy nhiên, khi đó độ phức tạp thời gian tăng thành $O(m \log k)$.

## Xây dựng automaton

Giả sử ta đã xây dựng trie cho tập chuỗi đã cho.
Bây giờ hãy nhìn nó theo một góc độ khác.
Nếu xét một đỉnh bất kỳ,
chuỗi tương ứng với đỉnh đó là tiền tố của một hoặc nhiều chuỗi trong tập; do đó mỗi đỉnh của trie có thể được hiểu là một vị trí trong một hoặc nhiều chuỗi của tập.

Thực ra, các đỉnh của trie có thể được xem là các trạng thái của một **automaton hữu hạn tất định**.
Từ bất kỳ trạng thái nào, với một ký tự đầu vào, ta có thể chuyển sang trạng thái khác, tức sang một vị trí khác trong tập chuỗi.
Ví dụ, nếu từ điển chỉ có chuỗi $abc$ và ta đang đứng ở đỉnh $ab$, thì với ký tự $c$ ta có thể chuyển tới đỉnh $abc$.

Như vậy, ta có thể hiểu các cạnh của trie là các phép chuyển trạng thái trong automaton theo ký tự tương ứng.
Tuy nhiên, trong automaton ta cần có phép chuyển cho mọi cặp trạng thái và ký tự.
Nếu ta thử chuyển bằng một ký tự nhưng trie không có cạnh tương ứng, ta vẫn phải chuyển tới một trạng thái nào đó.

Cụ thể hơn, giả sử ta đang ở trạng thái tương ứng với chuỗi $t$ và muốn chuyển sang trạng thái khác bằng ký tự $c$.
Nếu tồn tại cạnh có nhãn $c$, ta chỉ cần đi qua cạnh đó và nhận được đỉnh tương ứng với $t + c$.
Nếu không có cạnh như vậy, để giữ bất biến rằng trạng thái hiện tại là phần khớp dài nhất trong phần chuỗi đã xử lý, ta phải tìm chuỗi dài nhất trong trie là một hậu tố thực sự của $t$, rồi thử thực hiện phép chuyển từ đó.

Ví dụ, giả sử trie được xây từ hai chuỗi $ab$ và $bc$, và hiện ta đang ở đỉnh tương ứng với $ab$, cũng là một đỉnh $\text{output}$.
Để chuyển với ký tự $c$, ta buộc phải đi tới trạng thái tương ứng với chuỗi $b$, rồi từ đó đi theo cạnh mang ký tự $c$.

<center>
<img src="https://upload.wikimedia.org/wikipedia/commons/9/90/A_diagram_of_the_Aho-Corasick_string_search_algorithm.svg" width="300px">
<br>
<i>Một automaton Aho-Corasick được xây từ các từ "a", "ab", "bc", "bca", "c" và "caa".</i>
<br>
<i>Mũi tên xanh dương là các liên kết hậu tố, mũi tên xanh lá là các liên kết terminal.</i>
</center>

Một **liên kết hậu tố** (suffix link) của đỉnh $p$ là một cạnh trỏ tới hậu tố thực sự dài nhất của chuỗi tương ứng với đỉnh $p$.
Trường hợp đặc biệt duy nhất là đỉnh gốc của trie; liên kết hậu tố của nó trỏ về chính nó.
Giờ ta có thể phát biểu lại quy tắc chuyển trạng thái trong automaton như sau:
khi chưa có phép chuyển từ đỉnh hiện tại của trie bằng ký tự hiện tại (hoặc cho đến khi ta chạm đỉnh gốc), ta đi theo liên kết hậu tố.

Như vậy, ta đã quy bài toán xây dựng automaton về bài toán tìm liên kết hậu tố cho mọi đỉnh của trie.
Tuy nhiên, hơi bất ngờ là chính các phép chuyển đã xây trong automaton lại được dùng để xây các liên kết hậu tố này.

Liên kết hậu tố của đỉnh gốc và mọi đỉnh con trực tiếp của nó đều trỏ về đỉnh gốc.
Với một đỉnh $v$ nằm sâu hơn trong cây, ta có thể tính liên kết hậu tố như sau:
nếu $p$ là tổ tiên của $v$ và $c$ là ký tự gắn trên cạnh từ $p$ đến $v$,
ta đi tới $p$,
sau đó đi theo liên kết hậu tố của nó và thực hiện phép chuyển bằng ký tự $c$ từ đó.

Như vậy, bài toán tìm phép chuyển được quy về bài toán tìm liên kết hậu tố, còn bài toán tìm liên kết hậu tố lại được quy về bài toán tìm một liên kết hậu tố và một phép chuyển, ngoại trừ các đỉnh gần gốc.
Ta thu được một quan hệ phụ thuộc đệ quy có thể giải trong thời gian tuyến tính.

Chuyển sang phần cài đặt.
Lưu ý rằng giờ với mỗi đỉnh $v$, ta sẽ lưu tổ tiên $p$ và ký tự $pch$ trên cạnh từ $p$ đến $v$.
Ngoài ra, tại mỗi đỉnh ta lưu liên kết hậu tố $\text{link}$ (hoặc $-1$ nếu chưa được tính), và trong mảng $\text{go}[k]$ ta lưu các phép chuyển của máy theo từng ký hiệu (cũng bằng $-1$ nếu chưa được tính).

```{.cpp file=aho_corasick_automaton}
const int K = 26;

struct Vertex {
    int next[K];
    bool output = false;
    int p = -1;
    char pch;
    int link = -1;
    int go[K];

    Vertex(int p=-1, char ch='$') : p(p), pch(ch) {
        fill(begin(next), end(next), -1);
        fill(begin(go), end(go), -1);
    }
};

vector<Vertex> t(1);

void add_string(string const& s) {
    int v = 0;
    for (char ch : s) {
        int c = ch - 'a';
        if (t[v].next[c] == -1) {
            t[v].next[c] = t.size();
            t.emplace_back(v, ch);
        }
        v = t[v].next[c];
    }
    t[v].output = true;
}

int go(int v, char ch);

int get_link(int v) {
    if (t[v].link == -1) {
        if (v == 0 || t[v].p == 0)
            t[v].link = 0;
        else
            t[v].link = go(get_link(t[v].p), t[v].pch);
    }
    return t[v].link;
}

int go(int v, char ch) {
    int c = ch - 'a';
    if (t[v].go[c] == -1) {
        if (t[v].next[c] != -1)
            t[v].go[c] = t[v].next[c];
        else
            t[v].go[c] = v == 0 ? 0 : go(get_link(v), ch);
    }
    return t[v].go[c];
} 
```

Dễ thấy rằng nhờ ghi nhớ các liên kết hậu tố và phép chuyển,
tổng thời gian để tìm toàn bộ liên kết hậu tố và phép chuyển là tuyến tính.

Để xem minh họa cho ý tưởng này, tham khảo slide 103 trong [slide của Stanford](http://web.stanford.edu/class/archive/cs/cs166/cs166.1166/lectures/02/Slides02.pdf).

### Xây dựng bằng BFS

Thay vì tính phép chuyển và liên kết hậu tố bằng các lời gọi đệ quy tới `go` và `get_link`, ta có thể tính chúng từ dưới lên bắt đầu từ đỉnh gốc.
(Thực tế, khi từ điển chỉ gồm một chuỗi, ta thu được thuật toán Knuth-Morris-Pratt quen thuộc.)

Cách này có một số ưu điểm so với cách trên: thay vì phụ thuộc vào tổng độ dài $m$, thời gian chạy chỉ phụ thuộc vào số đỉnh $n$ của trie. Hơn nữa, có thể điều chỉnh cho bảng chữ cái lớn bằng cấu trúc dữ liệu mảng persistent, nhờ đó thời gian xây dựng là $O(n \log k)$ thay vì $O(mk)$; đây là cải thiện đáng kể vì $m$ có thể lên tới $n^2$.

Ta có thể lập luận quy nạp dựa trên việc BFS từ gốc duyệt các đỉnh theo thứ tự độ dài tăng dần.
Có thể giả sử rằng khi đang ở đỉnh $v$, liên kết hậu tố $u = link[v]$ của nó đã được tính, và mọi phép chuyển từ các đỉnh có độ dài ngắn hơn cũng đã được tính đầy đủ.

Giả sử hiện tại ta đứng ở đỉnh $v$ và xét ký tự $c$. Về cơ bản có hai trường hợp:

1. $go[v][c] = -1$. Khi đó, ta có thể gán $go[v][c] = go[u][c]$, vốn đã biết theo giả thiết quy nạp;
2. $go[v][c] = w \neq -1$. Khi đó, ta có thể gán $link[w] = go[u][c]$.

Theo cách này, ta tốn $O(1)$ thời gian cho mỗi cặp gồm một đỉnh và một ký tự, nên thời gian chạy là $O(nk)$. Chi phí lớn nhất ở đây là ta sao chép rất nhiều phép chuyển từ $u$ trong trường hợp đầu, trong khi các phép chuyển của trường hợp thứ hai tạo thành trie và tổng cộng chỉ có $n$ trên toàn bộ các đỉnh. Để tránh sao chép $go[u][c]$, ta có thể dùng cấu trúc mảng persistent: ban đầu sao chép $go[u]$ sang $go[v]$, rồi chỉ cập nhật các ký tự mà phép chuyển khác đi. Cách này dẫn tới thuật toán $O(n \log k)$.

## Ứng dụng

### Tìm mọi chuỗi trong một tập cho trước xuất hiện trong văn bản

Cho một tập chuỗi và một văn bản.
Ta cần in ra mọi lần xuất hiện của mọi chuỗi trong tập trong văn bản với độ phức tạp $O(\text{len} + \text{ans})$, trong đó $\text{len}$ là độ dài văn bản và $\text{ans}$ là kích thước đáp án.

Ta xây dựng automaton cho tập chuỗi này.
Sau đó xử lý văn bản từng ký tự bằng automaton,
bắt đầu tại đỉnh gốc của trie.
Nếu tại một thời điểm ta đang ở trạng thái $v$ và ký tự tiếp theo là $c$, ta chuyển sang trạng thái kế tiếp bằng $\text{go}(v, c)$, qua đó hoặc tăng độ dài của chuỗi con đang khớp thêm $1$, hoặc giảm nó bằng cách đi theo một liên kết hậu tố.

Làm thế nào để biết tại trạng thái $v$ có chuỗi nào trong tập khớp hay không?
Trước hết, rõ ràng nếu ta đang đứng tại một đỉnh $\text{output}$ thì chuỗi tương ứng với đỉnh đó kết thúc tại vị trí hiện tại trong văn bản.
Tuy nhiên, đó không phải trường hợp duy nhất tạo ra một kết quả khớp:
nếu ta có thể đi theo các liên kết hậu tố để tới một hay nhiều đỉnh $\text{output}$, thì mỗi đỉnh $\text{output}$ tìm được cũng tương ứng với một kết quả khớp.
Một ví dụ đơn giản cho tình huống này là tập chuỗi $\{dabce, abc, bc\}$ và văn bản $dabc$.

Do đó, nếu tại mỗi đỉnh $\text{output}$ ta lưu chỉ số của chuỗi tương ứng (hoặc danh sách chỉ số nếu tập có các chuỗi trùng nhau), thì trong $O(n)$ thời gian ta có thể tìm chỉ số của mọi chuỗi khớp với trạng thái hiện tại bằng cách đi theo các liên kết hậu tố từ đỉnh hiện tại về gốc.
Đây chưa phải cách hiệu quả nhất, vì tổng độ phức tạp sẽ là $O(n ~ \text{len})$.
Ta có thể tối ưu bằng cách tính và lưu đỉnh $\text{output}$ gần nhất có thể tới được theo các liên kết hậu tố (đôi khi gọi là **exit link**).
Giá trị này có thể được tính lười trong thời gian tuyến tính.
Nhờ đó, từ mỗi đỉnh ta có thể đi trong $O(1)$ tới đỉnh được đánh dấu tiếp theo trên đường liên kết hậu tố, tức tới kết quả khớp tiếp theo.
Vì vậy mỗi kết quả khớp chỉ tốn $O(1)$ thời gian và tổng độ phức tạp đạt $O(\text{len} + \text{ans})$.

Nếu chỉ muốn đếm số lần xuất hiện thay vì tìm các chỉ số cụ thể, ta có thể tính với mỗi đỉnh $v$ số đỉnh được đánh dấu trên đường liên kết hậu tố của nó.
Tổng thời gian để tính các giá trị này là $O(n)$.
Do đó, ta có thể cộng tổng số kết quả khớp trong $O(\text{len})$.

### Tìm chuỗi nhỏ nhất theo thứ tự từ điển có độ dài cho trước và không khớp với bất kỳ chuỗi nào đã cho

Cho một tập chuỗi và một độ dài $L$.
Ta cần tìm một chuỗi độ dài $L$ không chứa bất kỳ chuỗi nào trong tập và chọn chuỗi nhỏ nhất theo thứ tự từ điển trong số đó.

Ta có thể xây dựng automaton cho tập chuỗi.
Nhắc lại rằng các đỉnh $\text{output}$ là những trạng thái tại đó ta khớp với một chuỗi trong tập.
Vì bài này yêu cầu tránh mọi kết quả khớp, ta không được phép đi vào các trạng thái đó.
Mặt khác, mọi đỉnh còn lại đều có thể đi vào.
Vì vậy, ta xóa mọi đỉnh "xấu" khỏi máy và trên đồ thị automaton còn lại tìm đường đi có độ dài $L$ nhỏ nhất theo thứ tự từ điển.
Bài toán này có thể giải trong $O(L)$, chẳng hạn bằng [tìm kiếm theo chiều sâu](../graph/depth-first-search.md).

### Tìm chuỗi ngắn nhất chứa mọi chuỗi đã cho

Ở đây ta dùng các ý tưởng tương tự.
Với mỗi đỉnh, ta lưu một mask cho biết những chuỗi nào khớp tại trạng thái đó.
Khi đó bài toán có thể được phát biểu lại như sau:
bắt đầu tại trạng thái $(v = \text{root},~ \text{mask} = 0)$, ta muốn đi tới trạng thái $(v,~ \text{mask} = 2^n - 1)$, trong đó $n$ là số chuỗi trong tập.
Khi chuyển từ trạng thái này sang trạng thái khác bằng một ký tự, ta cập nhật mask tương ứng.
Bằng cách chạy [tìm kiếm theo chiều rộng](../graph/breadth-first-search.md), ta có thể tìm đường đi ngắn nhất tới trạng thái $(v,~ \text{mask} = 2^n - 1)$.

### Tìm chuỗi nhỏ nhất theo thứ tự từ điển có độ dài $L$ và chứa $k$ chuỗi {data-toc-label="Finding the lexicographically smallest string of length L containing k strings"}

Tương tự bài toán trước, với mỗi đỉnh ta tính số kết quả khớp tương ứng với nó (tức số đỉnh được đánh dấu có thể tới được bằng các liên kết hậu tố).
Ta phát biểu lại bài toán: trạng thái hiện tại được xác định bởi bộ ba $(v,~ \text{len},~ \text{cnt})$, và ta muốn đi từ trạng thái $(\text{root},~ 0,~ 0)$ tới trạng thái $(v,~ L,~ k)$, trong đó $v$ có thể là bất kỳ đỉnh nào.
Do đó, ta có thể tìm một đường đi như vậy bằng tìm kiếm theo chiều sâu (và nếu phép tìm kiếm xét các cạnh theo thứ tự tự nhiên của chúng, đường đi tìm được sẽ tự động là nhỏ nhất theo thứ tự từ điển).

## Bài tập

- [UVA #11590 - Prefix Lookup](https://uva.onlinejudge.org/index.php?option=com_onlinejudge&Itemid=8&page=show_problem&problem=2637)
- [UVA #11171 - SMS](https://uva.onlinejudge.org/index.php?option=com_onlinejudge&Itemid=8&page=show_problem&problem=2112)
- [UVA #10679 - I Love Strings!!](https://uva.onlinejudge.org/index.php?option=onlinejudge&page=show_problem&problem=1620)
- [Codeforces - x-prime Substrings](https://codeforces.com/problemset/problem/1400/F)
- [Codeforces - Frequency of String](http://codeforces.com/problemset/problem/963/D)
- [CodeChef - TWOSTRS](https://www.codechef.com/MAY20A/problems/TWOSTRS)

## Tài liệu tham khảo
- [Stanford's CS166 - Aho-Corasick Automata](http://web.stanford.edu/class/archive/cs/cs166/cs166.1166/lectures/02/Slides02.pdf) ([Condensed](http://web.stanford.edu/class/archive/cs/cs166/cs166.1166/lectures/02/Small02.pdf))
