---
tags:
  - Translated
e_maxx_link: floyd_warshall_algorithm
translation:
  source: graph/all-pair-shortest-path-floyd-warshall.md
  source_commit: d89f2f066b613541628b16e5b611657ceee43330
  status: draft
  last_synced: 2026-08-07
---

# Thuật toán Floyd-Warshall

Cho một đồ thị có hướng hoặc vô hướng, có trọng số $G$ gồm $n$ đỉnh.
Bài toán yêu cầu tìm độ dài đường đi ngắn nhất $d_{ij}$ giữa mọi cặp đỉnh $i$ và $j$.

Đồ thị có thể chứa cạnh có trọng số âm, nhưng không được chứa chu trình âm.

Nếu tồn tại một chu trình âm như vậy, ta có thể đi quanh chu trình đó lặp đi lặp lại và sau mỗi vòng làm tổng trọng số của hành trình nhỏ hơn.
Vì thế một số đường đi có thể có trọng số nhỏ tùy ý, hay nói cách khác, đường đi ngắn nhất không được xác định.
Điều này cũng có nghĩa đồ thị vô hướng không thể có cạnh trọng số âm: chỉ riêng việc đi qua cạnh đó rồi quay lại nhiều lần đã tạo thành một chu trình âm.

Thuật toán này cũng có thể dùng để phát hiện chu trình âm.
Đồ thị có chu trình âm nếu sau khi thuật toán kết thúc, tồn tại một đỉnh $v$ có khoảng cách từ chính nó đến nó là số âm.

Thuật toán được Robert Floyd và Stephen Warshall công bố độc lập trong các bài báo năm 1962.
Tuy nhiên, từ năm 1959 Bernard Roy đã công bố về cơ bản cùng một thuật toán, nhưng công trình khi đó không được chú ý.

## Mô tả thuật toán

Ý tưởng cốt lõi là chia quá trình tìm đường đi ngắn nhất giữa hai đỉnh bất kỳ thành nhiều pha tăng dần.

Đánh số các đỉnh từ 1 đến $n$.
Ma trận khoảng cách được ký hiệu là $d[ ][ ]$.

Trước pha thứ $k$ ($k = 1 \dots n$), với mọi cặp đỉnh $i$, $j$, giá trị $d[i][j]$ lưu độ dài đường đi ngắn nhất từ $i$ đến $j$ mà các đỉnh trung gian chỉ thuộc tập $\{1, 2, ..., k-1\}$.

Nói cách khác, trước pha thứ $k$, $d[i][j]$ bằng độ dài đường đi ngắn nhất từ $i$ đến $j$ nếu đường đi chỉ được phép đi qua các đỉnh có số thứ tự nhỏ hơn $k$ ở vị trí trung gian; đỉnh đầu và đỉnh cuối không bị giới hạn bởi điều kiện này.

Dễ thấy tính chất trên đúng ở pha đầu tiên. Với $k = 0$, ta khởi tạo $d[i][j] = w_{i j}$ nếu tồn tại cạnh nối $i$ đến $j$ có trọng số $w_{i j}$, và $d[i][j] = \infty$ nếu không có cạnh.
Trong cài đặt, $\infty$ được thay bằng một giá trị đủ lớn.
Như sẽ thấy ở phần sau, cách khởi tạo này là điều kiện cần để thuật toán hoạt động đúng.

Giả sử hiện tại ta đang ở pha thứ $k$ và muốn tính lại ma trận $d[ ][ ]$ sao cho nó thỏa điều kiện của pha thứ $(k + 1)$.
Ta cần cập nhật khoảng cách cho một số cặp đỉnh $(i, j)$.
Có hai trường hợp cơ bản:

*   Đường đi ngắn nhất từ $i$ đến $j$ với các đỉnh trung gian thuộc tập $\{1, 2, \dots, k\}$ trùng với đường đi ngắn nhất khi chỉ cho phép các đỉnh trung gian thuộc $\{1, 2, \dots, k-1\}$.

    Trong trường hợp này, $d[i][j]$ không thay đổi.

*   Đường đi ngắn nhất khi cho phép thêm đỉnh trung gian $k$ trở nên ngắn hơn.

    Điều đó có nghĩa đường đi mới đi qua đỉnh $k$.
    Khi ấy ta có thể tách đường đi ngắn nhất từ $i$ đến $j$ thành hai phần:
    đường đi từ $i$ đến $k$, và đường đi từ $k$ đến $j$.
    Cả hai phần này chỉ dùng các đỉnh trung gian trong tập $\{1, 2, \dots, k-1\}$ và đều là ngắn nhất dưới ràng buộc đó.
    Vì độ dài của chúng đã được tính ở pha trước, ta có thể tính độ dài đường đi mới từ $i$ đến $j$ bằng $d[i][k] + d[k][j]$.

Kết hợp hai trường hợp, ở pha thứ $k$ ta cập nhật mọi cặp $(i,j)$ như sau:

$$d_{\text{new}}[i][j] = min(d[i][j], d[i][k] + d[k][j])$$

Do đó, công việc ở mỗi pha chỉ là duyệt qua mọi cặp đỉnh và cập nhật độ dài đường đi ngắn nhất giữa chúng.
Sau pha thứ $n$, $d[i][j]$ trong ma trận khoảng cách chính là độ dài đường đi ngắn nhất từ $i$ đến $j$, hoặc bằng $\infty$ nếu không tồn tại đường đi.

Một lưu ý cuối cùng: ta không cần tạo ma trận riêng $d_{\text{new}}[ ][ ]$ để lưu tạm kết quả của pha thứ $k$; mọi thay đổi có thể được thực hiện trực tiếp trên $d[ ][ ]$.
Thật vậy, ở mỗi pha ta chỉ có thể làm một khoảng cách trong ma trận nhỏ đi, nên việc cập nhật tại chỗ không thể làm hỏng đáp án của các cặp sẽ được xử lý ở pha $(k+1)$ hoặc sau đó.

Độ phức tạp thời gian của thuật toán hiển nhiên là $O(n^3)$.

## Cài đặt

Giả sử $d[][]$ là mảng hai chiều kích thước $n \times n$, được khởi tạo theo pha thứ $0$ như đã mô tả ở trên.
Ta cũng đặt $d[i][i] = 0$ với mọi $i$ ở pha thứ $0$.

Khi đó thuật toán được cài đặt như sau:

```cpp
for (int k = 0; k < n; ++k) {
    for (int i = 0; i < n; ++i) {
        for (int j = 0; j < n; ++j) {
            d[i][j] = min(d[i][j], d[i][k] + d[k][j]); 
        }
    }
}
```

Ta giả sử rằng nếu không có cạnh giữa hai đỉnh $i$ và $j$, thì $d[i][j]$ chứa một số đủ lớn, lớn hơn độ dài của mọi đường đi có thể có trong đồ thị.
Khi đó việc dùng cạnh không tồn tại này sẽ luôn bất lợi, và thuật toán hoạt động đúng.

Tuy nhiên, nếu đồ thị có cạnh trọng số âm thì cần xử lý cẩn thận hơn.
Nếu không, ma trận kết quả có thể xuất hiện các giá trị dạng $\infty - 1$, $\infty - 2$, v.v.; các giá trị đó thực chất vẫn biểu thị rằng không tồn tại đường đi giữa hai đỉnh tương ứng.
Vì vậy, khi có cạnh trọng số âm, nên viết Floyd-Warshall như sau để không thực hiện chuyển trạng thái thông qua những đường đi không tồn tại.

```cpp
for (int k = 0; k < n; ++k) {
    for (int i = 0; i < n; ++i) {
        for (int j = 0; j < n; ++j) {
            if (d[i][k] < INF && d[k][j] < INF)
                d[i][j] = min(d[i][j], d[i][k] + d[k][j]); 
        }
    }
}
```

## Khôi phục dãy đỉnh của đường đi ngắn nhất

Ta có thể dễ dàng lưu thêm thông tin để khôi phục đường đi ngắn nhất giữa hai đỉnh bất kỳ dưới dạng một dãy đỉnh.

Ngoài ma trận khoảng cách $d[ ][ ]$, ta duy trì một ma trận tổ tiên $p[ ][ ]$ lưu số thứ tự của pha gần nhất mà khoảng cách ngắn nhất giữa hai đỉnh được cập nhật.
Số thứ tự của pha đó chính là một đỉnh nằm ở giữa đường đi ngắn nhất cần tìm.
Khi đó ta chỉ cần tiếp tục tìm đường đi ngắn nhất từ $i$ đến $p[i][j]$ và từ $p[i][j]$ đến $j$.
Điều này dẫn đến một thuật toán đệ quy đơn giản để khôi phục đường đi ngắn nhất.

## Trường hợp trọng số thực

Nếu trọng số cạnh không phải số nguyên mà là số thực, cần tính đến sai số số học khi làm việc với kiểu số dấu phẩy động.

Floyd-Warshall có một đặc điểm không thuận lợi là sai số có thể tích lũy rất nhanh.
Nếu ở pha đầu tiên đã có sai số $\delta$, sang pha thứ hai sai số có thể thành $2 \delta$, pha thứ ba thành $4 \delta$, và cứ thế tiếp tục.

Để hạn chế vấn đề này, có thể sửa thuật toán để xét một ngưỡng sai số (EPS = $\delta$) trong phép so sánh:

```cpp
if (d[i][k] + d[k][j] < d[i][j] - EPS)
    d[i][j] = d[i][k] + d[k][j]; 
```

## Trường hợp có chu trình âm

Về mặt hình thức, Floyd-Warshall không áp dụng cho đồ thị có chu trình âm.
Tuy nhiên, với mọi cặp đỉnh $i$, $j$ mà không tồn tại đường đi bắt đầu từ $i$, đi qua một chu trình âm rồi kết thúc ở $j$, thuật toán vẫn cho kết quả đúng.

Với những cặp đỉnh mà đáp án không tồn tại do có thể đi qua chu trình âm, Floyd-Warshall sẽ lưu một giá trị nào đó trong ma trận khoảng cách, có thể rất âm nhưng không nhất thiết phản ánh đúng ý nghĩa toán học.
Ta có thể mở rộng thuật toán để xử lý rõ các cặp này, chẳng hạn gán kết quả là $-\text{INF}$.

Cách làm như sau:
chạy Floyd-Warshall thông thường trên đồ thị.
Sau đó, đường đi ngắn nhất từ $i$ đến $j$ không tồn tại khi và chỉ khi tồn tại một đỉnh $t$ sao cho có thể đi từ $i$ đến $t$, từ $t$ đến $j$, và $d[t][t] < 0$.

Ngoài ra, khi dùng Floyd-Warshall trên đồ thị có chu trình âm, cần nhớ rằng khoảng cách có thể giảm theo cấp số nhân về phía âm.
Vì vậy phải tránh tràn số nguyên bằng cách chặn khoảng cách nhỏ nhất ở một giá trị nào đó, chẳng hạn $-\text{INF}$.

Để tìm hiểu thêm về chu trình âm, xem bài riêng [Tìm chu trình âm trong đồ thị](finding-negative-cycle-in-graph.md).

## Bài tập luyện tập
 - [UVA: Page Hopping](https://uva.onlinejudge.org/index.php?option=onlinejudge&page=show_problem&problem=762)
 - [SPOJ: Possible Friends](http://www.spoj.com/problems/SOCIALNE/)
 - [CODEFORCES: Greg and Graph](http://codeforces.com/problemset/problem/295/B)
 - [SPOJ: CHICAGO - 106 miles to Chicago](http://www.spoj.com/problems/CHICAGO/)
 * [UVA 10724 - Road Construction](https://uva.onlinejudge.org/index.php?option=onlinejudge&page=show_problem&problem=1665)
 * [UVA  117 - The Postal Worker Rings Once](https://uva.onlinejudge.org/index.php?option=onlinejudge&page=show_problem&problem=53)
 * [Codeforces - Traveling Graph](http://codeforces.com/problemset/problem/21/D)
 * [UVA - 1198 - The Geodetic Set Problem](https://uva.onlinejudge.org/index.php?option=onlinejudge&page=show_problem&problem=3639)
 * [UVA - 10048 - Audiophobia](https://uva.onlinejudge.org/index.php?option=com_onlinejudge&Itemid=8&page=show_problem&problem=989)
 * [UVA - 125 - Numbering Paths](https://uva.onlinejudge.org/index.php?option=onlinejudge&page=show_problem&problem=61)
 * [LOJ - Travel Company](http://lightoj.com/volume_showproblem.php?problem=1221)
 * [UVA 423 - MPI Maelstrom](https://uva.onlinejudge.org/index.php?option=com_onlinejudge&Itemid=8&page=show_problem&problem=364)
 * [UVA 1416 - Warfare And Logistics](https://uva.onlinejudge.org/index.php?option=com_onlinejudge&Itemid=8&page=show_problem&problem=4162)
 * [UVA 1233 - USHER](https://uva.onlinejudge.org/index.php?option=com_onlinejudge&Itemid=8&page=show_problem&problem=3674)
 * [UVA 10793 - The Orc Attack](https://uva.onlinejudge.org/index.php?option=com_onlinejudge&Itemid=8&page=show_problem&problem=1734)
 * [UVA 10099 The Tourist Guide](https://uva.onlinejudge.org/index.php?option=com_onlinejudge&Itemid=8&page=show_problem&problem=1040)
 * [UVA 869 - Airline Comparison](https://uva.onlinejudge.org/index.php?option=com_onlinejudge&page=show_problem&problem=810)
 * [UVA 13211 - Geonosis](https://uva.onlinejudge.org/index.php?option=onlinejudge&Itemid=8&page=show_problem&problem=5134)
 * [SPOJ - Defend the Rohan](http://www.spoj.com/problems/ROHAAN/)
 * [Codeforces - Roads in Berland](http://codeforces.com/contest/25/problem/C)
 * [Codeforces - String Problem](http://codeforces.com/contest/33/problem/B)
 * [GYM - Manic Moving (C)](http://codeforces.com/gym/101223)
 * [SPOJ - Arbitrage](http://www.spoj.com/problems/ARBITRAG/)
 * [UVA - 12179 - Randomly-priced Tickets](https://uva.onlinejudge.org/index.php?option=com_onlinejudge&Itemid=8&page=show_problem&problem=3331)
 * [LOJ - 1086 - Jogging Trails](http://lightoj.com/volume_showproblem.php?problem=1086)
 * [SPOJ - Ingredients](http://www.spoj.com/problems/INGRED/)
 * [CSES - Shortest Routes II](https://cses.fi/problemset/task/1672)
