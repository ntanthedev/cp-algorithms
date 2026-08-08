---
tags:
  - Translated
e_maxx_link: kuhn_matching
translation:
  source: graph/kuhn_maximum_bipartite_matching.md
  source_commit: 25b835ca13720898fd8e69ab100459081dedead0
  status: draft
  last_synced: 2026-08-08
---

# Thuật toán Kuhn cho cặp ghép cực đại trên đồ thị hai phía

## Bài toán
Cho một đồ thị hai phía $G$ gồm $n$ đỉnh và $m$ cạnh. Hãy tìm cặp ghép cực đại, tức chọn được nhiều cạnh nhất có thể sao cho không có hai cạnh được chọn cùng kề với một đỉnh.

## Mô tả thuật toán

### Các định nghĩa cần thiết

* Một **cặp ghép** (matching) $M$ là một tập các cạnh đôi một không kề nhau của đồ thị (nói cách khác, mỗi đỉnh của đồ thị kề với không quá một cạnh trong tập $M$).
**Số cạnh** của một cặp ghép là số cạnh thuộc cặp ghép đó.
Những đỉnh kề với một cạnh thuộc cặp ghép (tức có bậc đúng bằng một trong đồ thị con tạo bởi $M$) được gọi là các đỉnh **bão hòa** bởi cặp ghép này.

* Một **cặp ghép tối đại** (maximal matching) là một cặp ghép $M$ của đồ thị $G$ không phải là tập con của bất kỳ cặp ghép nào khác.

* Một **cặp ghép cực đại** (maximum matching, còn gọi là maximum-cardinality matching) là cặp ghép chứa số cạnh lớn nhất có thể. Mọi cặp ghép cực đại đều là cặp ghép tối đại.

* Một **đường đi** có độ dài $k$ trong bài này được hiểu là một đường đi *đơn* (tức không lặp đỉnh hay cạnh) gồm $k$ cạnh, trừ khi có ghi chú khác.

* Một **đường luân phiên** (alternating path, trên đồ thị hai phía và đối với một cặp ghép cho trước) là đường đi mà các cạnh lần lượt thuộc / không thuộc cặp ghép.

* Một **đường tăng** (augmenting path, trên đồ thị hai phía và đối với một cặp ghép cho trước) là một đường luân phiên có cả đỉnh đầu và đỉnh cuối đều chưa bão hòa, tức không được ghép trong cặp ghép.

* **Hiệu đối xứng** (symmetric difference, còn gọi là **disjunctive union**) của hai tập $A$ và $B$, ký hiệu $A \oplus B$, là tập gồm các phần tử thuộc đúng một trong hai tập $A$ hoặc $B$, nhưng không thuộc cả hai.
Tức là $A \oplus B = (A - B) \cup (B - A) = (A \cup B) - (A \cap B)$.

### Bổ đề Berge

Bổ đề này được nhà toán học người Pháp **Claude Berge** chứng minh vào năm 1957, dù trước đó nhà toán học Đan Mạch **Julius Petersen** đã quan sát thấy kết quả này vào năm 1891 và nhà toán học Hungary **Denés Kőnig** vào năm 1931.

#### Phát biểu
Một cặp ghép $M$ là cực đại $\Leftrightarrow$ không tồn tại đường tăng đối với cặp ghép $M$.

#### Chứng minh

Ta chứng minh cả hai chiều của tương đương bằng phản chứng.

1.  Cặp ghép $M$ là cực đại $\Rightarrow$ không tồn tại đường tăng đối với cặp ghép $M$.
  
    Giả sử tồn tại một đường tăng $P$ đối với cặp ghép cực đại $M$. Đường tăng $P$ nhất thiết có độ dài lẻ và có nhiều hơn đúng một cạnh không thuộc $M$ so với số cạnh vừa thuộc $P$ vừa thuộc $M$.
    Ta tạo một cặp ghép mới $M'$ bằng cách giữ mọi cạnh của cặp ghép ban đầu $M$ trừ những cạnh đồng thời nằm trên $P$, rồi thêm các cạnh thuộc $P$ nhưng không thuộc $M$.
    Đây vẫn là một cặp ghép hợp lệ vì hai đầu mút của $P$ chưa bão hòa bởi $M$, còn các đỉnh khác trên $P$ chỉ bão hòa bởi các cạnh thuộc $P \cap M$.
    Cặp ghép mới $M'$ có nhiều hơn $M$ đúng một cạnh, mâu thuẫn với giả thiết $M$ là cực đại.
    
    Viết hình thức hơn, với một đường tăng $P$ đối với cặp ghép cực đại $M$, cặp ghép $M' = P \oplus M$ thỏa $|M'| = |M| + 1$, mâu thuẫn.
  
2.  Cặp ghép $M$ là cực đại $\Leftarrow$ không tồn tại đường tăng đối với cặp ghép $M$.

    Giả sử tồn tại một cặp ghép $M'$ có nhiều cạnh hơn $M$. Xét hiệu đối xứng $Q = M \oplus M'$. Đồ thị con $Q$ không nhất thiết còn là một cặp ghép.
    Mọi đỉnh trong $Q$ có bậc không quá $2$, vì vậy mỗi thành phần liên thông của nó thuộc một trong ba dạng:

      * một đỉnh cô lập
      * một đường đi (đơn) có các cạnh luân phiên thuộc $M$ và $M'$
      * một chu trình độ dài chẵn có các cạnh luân phiên thuộc $M$ và $M'$
 
    Vì $M'$ có nhiều cạnh hơn $M$, $Q$ chứa nhiều cạnh từ $M'$ hơn từ $M$. Theo nguyên lý Dirichlet, ít nhất một thành phần liên thông phải là một đường đi có nhiều cạnh từ $M'$ hơn từ $M$. Do đường này luân phiên, đỉnh đầu và đỉnh cuối của nó đều chưa bão hòa bởi $M$, nên đây là một đường tăng đối với $M$, trái với giả thiết. &ensp; $\blacksquare$
  
### Thuật toán Kuhn
  
Thuật toán Kuhn là một ứng dụng trực tiếp của bổ đề Berge. Ý tưởng cơ bản như sau:

Ban đầu, ta lấy cặp ghép rỗng. Sau đó, chừng nào còn tìm được một đường tăng, ta đảo trạng thái thuộc cặp ghép của các cạnh trên đường đó rồi tiếp tục tìm đường tăng mới. Khi không còn đường tăng nào, ta dừng lại — cặp ghép hiện tại là cực đại.

Còn lại là cách tìm đường tăng. Thuật toán Kuhn đơn giản tìm một đường tăng bất kỳ bằng phép duyệt [theo chiều sâu](depth-first-search.md) hoặc [theo chiều rộng](breadth-first-search.md). Thuật toán lần lượt xét các đỉnh của đồ thị, bắt đầu một lượt duyệt từ mỗi đỉnh và cố tìm một đường tăng xuất phát từ đỉnh đó.

Sẽ thuận tiện hơn khi mô tả thuật toán nếu giả sử đồ thị đầu vào đã được chia sẵn thành hai phần (dù trên thực tế có thể cài đặt thuật toán mà không cần cung cấp tường minh cách chia này).

Thuật toán xét mọi đỉnh $v$ thuộc phần thứ nhất: $v = 1 \ldots n_1$. Nếu đỉnh hiện tại $v$ đã bão hòa trong cặp ghép hiện tại (tức đã có một cạnh kề với nó được chọn), ta bỏ qua đỉnh này. Ngược lại, thuật toán cố bão hòa $v$ bằng cách bắt đầu tìm một đường tăng từ $v$.

Việc tìm đường tăng được thực hiện bằng một phép duyệt theo chiều sâu hoặc theo chiều rộng đặc biệt (thường dùng duyệt theo chiều sâu vì dễ cài đặt hơn).
Ban đầu, DFS đứng tại đỉnh chưa bão hòa $v$ thuộc phần thứ nhất. Ta xét tất cả các cạnh đi từ đỉnh này. Gọi cạnh hiện tại là $(v, to)$. Nếu đỉnh $to$ chưa bão hòa trong cặp ghép, ta đã tìm được một đường tăng chỉ gồm cạnh $(v, to)$; khi đó chỉ cần thêm cạnh này vào cặp ghép và dừng việc tìm đường tăng từ $v$. Ngược lại, nếu $to$ đã bão hòa bởi một cạnh $(to, p)$, ta đi tiếp theo cạnh đó: tức cố tìm một đường tăng đi qua $(v, to),(to, p), \ldots$.
Để làm vậy, ta chuyển phép duyệt sang đỉnh $p$ và tiếp tục cố tìm một đường tăng từ đỉnh này.

Như vậy, lượt duyệt bắt đầu từ $v$ hoặc tìm được một đường tăng và nhờ đó bão hòa $v$, hoặc không tìm được đường tăng nào (và vì thế không thể bão hòa đỉnh $v$ ở trạng thái cặp ghép hiện tại).

Sau khi đã xét hết các đỉnh $v = 1 \ldots n_1$, cặp ghép hiện tại sẽ là cực đại.
  
### Thời gian chạy

Có thể xem thuật toán Kuhn là một chuỗi gồm $n$ lượt duyệt theo chiều sâu/theo chiều rộng trên toàn bộ đồ thị. Vì vậy, toàn bộ thuật toán chạy trong $O(nm)$, và trong trường hợp xấu nhất là $O(n^3)$.

Tuy nhiên, có thể cải thiện nhẹ đánh giá này. Với thuật toán Kuhn, việc chọn phần nào làm phần thứ nhất và phần nào làm phần thứ hai là quan trọng.
Trong cài đặt mô tả ở trên, DFS/BFS chỉ bắt đầu từ các đỉnh thuộc phần thứ nhất, nên toàn bộ thuật toán chạy trong $O(n_1m)$, với $n_1$ là số đỉnh của phần thứ nhất. Trong trường hợp xấu nhất, độ phức tạp là $O(n_1 ^ 2 n_2)$ (với $n_2$ là số đỉnh của phần thứ hai).
Điều này cho thấy sẽ có lợi hơn nếu phần thứ nhất có ít đỉnh hơn phần thứ hai. Với các đồ thị rất mất cân bằng (khi $n_1$ và $n_2$ chênh lệch nhiều), cách chọn hai phần có thể tạo ra khác biệt đáng kể về thời gian chạy.

## Cài đặt

### Cài đặt chuẩn
Sau đây là một cài đặt của thuật toán dựa trên DFS và nhận đầu vào là một đồ thị hai phía đã được chia tường minh thành hai phần.
Cài đặt này rất ngắn gọn và đáng để ghi nhớ ở dạng này.

Ở đây $n$ là số đỉnh của phần thứ nhất, $k$ là số đỉnh của phần thứ hai, còn $g[v]$ là danh sách các cạnh đi từ đỉnh $v$ thuộc phần thứ nhất (tức danh sách số hiệu các đỉnh mà các cạnh từ $v$ đi tới). Các đỉnh trong hai phần được đánh số độc lập: phần thứ nhất từ $1 \ldots n$, phần thứ hai từ $1 \ldots k$.

Tiếp theo có hai mảng phụ trợ: $\rm mt$ và $\rm used$. Mảng thứ nhất, $\rm mt$, lưu thông tin về cặp ghép hiện tại. Để thuận tiện khi lập trình, ta chỉ lưu thông tin này cho các đỉnh thuộc phần thứ hai: $\textrm{mt[} i \rm]$ là số hiệu đỉnh thuộc phần thứ nhất được ghép với đỉnh $i$ thuộc phần thứ hai (hoặc $-1$ nếu không có cạnh ghép nào kề với nó). Mảng thứ hai là $\rm used$: mảng đánh dấu "đã thăm" thông thường trong DFS (để DFS không đi vào cùng một đỉnh hai lần).

Hàm $\textrm{try_kuhn}$ là một DFS. Hàm trả về $\rm true$ nếu tìm được một đường tăng từ đỉnh $v$, và ta xem như hàm cũng đã thực hiện việc đảo cặp ghép dọc theo đường tìm được.

Bên trong hàm, ta xét mọi cạnh đi ra từ đỉnh $v$ của phần thứ nhất. Nếu cạnh hiện tại dẫn tới một đỉnh chưa bão hòa $to$, hoặc nếu $to$ đã bão hòa nhưng có thể tìm được một đường tăng bằng cách gọi đệ quy từ $\textrm{mt[}to \rm ]$, thì ta đã tìm được một đường tăng. Trước khi trả về $\rm true$, ta đảo cạnh hiện tại bằng cách đổi đỉnh thuộc phần thứ nhất được ghép với $to$ thành $v$.

**Ghi chú bản dịch:** Nguồn tiếng Anh dùng cụm “increasing chain” ở đoạn cài đặt này, nhưng ngữ cảnh và chính thuật toán đang nói về augmenting path; bản dịch dùng nhất quán “đường tăng”. Lỗi wording này được tách để đề xuất sửa upstream.

Chương trình chính trước hết đặt cặp ghép hiện tại là rỗng (mảng $\rm mt$ được điền bằng các giá trị $-1$). Sau đó, với mỗi đỉnh $v$ thuộc phần thứ nhất, ta gọi $\textrm{try_kuhn}$ sau khi đặt lại mảng $\rm used$ về chưa thăm.

Kích thước cặp ghép có thể lấy bằng số lần gọi $\textrm{try_kuhn}$ trong chương trình chính trả về $\rm true$. Cặp ghép cực đại cần tìm nằm trong mảng $\rm mt$.

```cpp
int n, k;
vector<vector<int>> g;
vector<int> mt;
vector<bool> used;

bool try_kuhn(int v) {
    if (used[v])
        return false;
    used[v] = true;
    for (int to : g[v]) {
        if (mt[to] == -1 || try_kuhn(mt[to])) {
            mt[to] = v;
            return true;
        }
    }
    return false;
}

int main() {
    //... reading the graph ...

    mt.assign(k, -1);
    for (int v = 0; v < n; ++v) {
        used.assign(n, false);
        try_kuhn(v);
    }

    for (int i = 0; i < k; ++i)
        if (mt[i] != -1)
            printf("%d %d\n", mt[i] + 1, i + 1);
}
```
    
Nhắc lại rằng thuật toán Kuhn có thể dễ dàng được cài đặt cho một đồ thị đã biết là hai phía nhưng chưa cung cấp tường minh cách chia thành hai phần. Khi đó, ta không còn dùng cách chia tiện lợi ở trên mà lưu thông tin cho mọi đỉnh của đồ thị. Mảng danh sách $g$ lúc này được khai báo cho mọi đỉnh, không chỉ các đỉnh thuộc phần thứ nhất (và các đỉnh của hai phần dùng chung một cách đánh số từ $1$ đến $n$). Hai mảng $\rm mt$ và $\rm used$ cũng được khai báo cho mọi đỉnh và phải được duy trì tương ứng.

### Cài đặt cải tiến

Ta sửa thuật toán như sau. Trước vòng lặp chính, hãy tìm một **cặp ghép bất kỳ** bằng một thuật toán đơn giản (một **heuristic** đơn giản), rồi mới chạy vòng lặp gọi hàm $\textrm{try_kuhn}()$ để cải thiện cặp ghép này. Trên các đồ thị ngẫu nhiên, cách làm thường nhanh hơn đáng kể: với đa số đồ thị, có thể nhanh chóng tìm một cặp ghép khá lớn bằng heuristic, sau đó cải thiện nó thành cặp ghép cực đại bằng thuật toán Kuhn thông thường. Nhờ đó, ta không cần khởi chạy DFS từ những đỉnh đã được đưa vào cặp ghép bởi heuristic.

Ví dụ, có thể duyệt mọi đỉnh thuộc phần thứ nhất, với mỗi đỉnh chọn một cạnh bất kỳ có thể thêm vào cặp ghép rồi thêm cạnh đó. Ngay cả heuristic đơn giản này cũng có thể tăng tốc thuật toán Kuhn nhiều lần.

Lưu ý rằng vòng lặp chính phải thay đổi một chút. Khi gọi hàm $\textrm{try_kuhn}$ trong vòng lặp chính, ta giả sử đỉnh hiện tại chưa thuộc cặp ghép, vì vậy cần thêm phép kiểm tra tương ứng.

Trong cài đặt, chỉ phần mã trong hàm $\textrm{main}()$ thay đổi:

```cpp
int main() {
    // ... reading the graph ...

    mt.assign(k, -1);
    vector<bool> used1(n, false);
    for (int v = 0; v < n; ++v) {
        for (int to : g[v]) {
            if (mt[to] == -1) {
                mt[to] = v;
                used1[v] = true;
                break;
            }
        }
    }
    for (int v = 0; v < n; ++v) {
        if (used1[v])
            continue;
        used.assign(n, false);
        try_kuhn(v);
    }

    for (int i = 0; i < k; ++i)
        if (mt[i] != -1)
            printf("%d %d\n", mt[i] + 1, i + 1);
}
```

**Một heuristic tốt khác** như sau. Ở mỗi bước, tìm đỉnh có bậc nhỏ nhất nhưng không cô lập, chọn một cạnh bất kỳ kề với nó và thêm cạnh đó vào cặp ghép, rồi xóa cả hai đầu mút cùng mọi cạnh kề với chúng khỏi đồ thị. Cách tham lam này hoạt động rất tốt trên các đồ thị ngẫu nhiên; trong nhiều trường hợp nó thậm chí tạo ra cặp ghép cực đại (dù vẫn tồn tại phản ví dụ mà trên đó cặp ghép tìm được nhỏ hơn rất nhiều so với cực đại).

## Ghi chú

* Thuật toán Kuhn là một chương trình con trong **thuật toán Hungary**, còn được gọi là **thuật toán Kuhn-Munkres**.
* Thuật toán Kuhn chạy trong $O(nm)$. Thuật toán nhìn chung dễ cài đặt, nhưng có những thuật toán hiệu quả hơn cho bài toán cặp ghép cực đại trên đồ thị hai phía, chẳng hạn **thuật toán Hopcroft-Karp-Karzanov**, chạy trong $O(\sqrt{n}m)$.
* [Bài toán phủ đỉnh nhỏ nhất](https://en.wikipedia.org/wiki/Vertex_cover) là NP-hard trên đồ thị tổng quát. Tuy nhiên, [định lý Kőnig](https://en.wikipedia.org/wiki/K%C5%91nig%27s_theorem_(graph_theory)) cho biết trên đồ thị hai phía, số cạnh của cặp ghép cực đại bằng số đỉnh của phủ đỉnh nhỏ nhất. Vì vậy, có thể dùng thuật toán cặp ghép cực đại trên đồ thị hai phía để giải bài toán phủ đỉnh nhỏ nhất trong thời gian đa thức trên đồ thị hai phía.

## Bài tập luyện tập

* [Kattis - Gopher II](https://open.kattis.com/problems/gopher2)
* [Kattis - Borders](https://open.kattis.com/problems/borders)