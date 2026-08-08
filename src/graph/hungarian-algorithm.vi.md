---
tags:
  - Translated
e_maxx_link: assignment_hungary
translation:
  source: graph/hungarian-algorithm.md
  source_commit: 1bc57c1f68debfd40b24194c7cfd59ef66be3ac3
  status: draft
  last_synced: 2026-08-08
---

# Thuật toán Hungary cho bài toán phân công

## Phát biểu bài toán phân công

Bài toán phân công có nhiều cách phát biểu chuẩn (về bản chất đều tương đương). Dưới đây là một số cách:

- Có $n$ công việc và $n$ người lao động. Mỗi người đưa ra mức tiền họ yêu cầu cho từng công việc. Mỗi người chỉ được giao một công việc. Mục tiêu là phân công công việc sao cho tổng chi phí nhỏ nhất.

- Cho ma trận $n \times n$ là $A$, cần chọn một số từ mỗi hàng sao cho mỗi cột cũng có đúng một số được chọn, đồng thời tổng các số được chọn là nhỏ nhất.

- Cho ma trận $n \times n$ là $A$, cần tìm một hoán vị $p$ độ dài $n$ sao cho giá trị $\sum A[i]\left[p[i]\right]$ là nhỏ nhất.

- Xét một đồ thị hai phía đầy đủ có $n$ đỉnh ở mỗi phần, mỗi cạnh có một trọng số. Mục tiêu là tìm một cặp ghép hoàn hảo có tổng trọng số nhỏ nhất.

Cần lưu ý rằng tất cả các cách phát biểu trên đều là bài toán "**vuông**", tức hai chiều luôn bằng $n$. Trong thực tế, ta thường gặp dạng "**chữ nhật**", với $n$ khác $m$ và cần chọn $\min(n,m)$ phần tử. Tuy nhiên, một bài toán "chữ nhật" luôn có thể chuyển thành bài toán "vuông" bằng cách thêm các hàng hoặc cột có giá trị lần lượt bằng không hoặc vô hạn.

Tương tự bài toán tìm nghiệm **nhỏ nhất**, ta cũng có thể đặt bài toán tìm nghiệm **lớn nhất**. Hai bài toán này tương đương: chỉ cần nhân mọi trọng số với $-1$.

## Thuật toán Hungary

### Lịch sử

Thuật toán được Harold **Kuhn** phát triển và công bố vào năm 1955. Chính Kuhn đặt tên "Hungarian" vì thuật toán dựa trên các công trình trước đó của hai nhà toán học Hungary Dénes Kőnig và Jenő Egerváry.<br>
Năm 1957, James **Munkres** chỉ ra rằng thuật toán chạy trong thời gian đa thức (theo nghĩa chặt), không phụ thuộc vào độ lớn của chi phí.<br>
Vì vậy, trong tài liệu, thuật toán không chỉ được gọi là "Hungarian" mà còn là "Kuhn-Munkres algorithm" hoặc "Munkres algorithm".<br>
Tuy nhiên, vào năm 2006 người ta phát hiện rằng cùng thuật toán này đã được nhà toán học Đức Carl Gustav **Jacobi** tìm ra **sớm hơn Kuhn một thế kỷ**. Công trình _About the research of the order of a system of arbitrary ordinary differential equations_, được xuất bản sau khi ông qua đời vào năm 1890, có chứa một thuật toán đa thức cho bài toán phân công. Do công trình được viết bằng tiếng Latin, kết quả này đã không được cộng đồng toán học chú ý trong thời gian dài.

**Ghi chú bản dịch:** Nguồn tiếng Anh viết sai tên Munkres thành “Mankres” ở hai vị trí. Bản dịch dùng đúng tên **Munkres**; typo này được tách để đề xuất sửa upstream.

Cũng cần lưu ý rằng thuật toán ban đầu của Kuhn có độ phức tạp tiệm cận $\mathcal{O}(n^4)$; về sau Jack **Edmonds** và Richard **Karp** (độc lập với **Tomizawa**) chỉ ra cách cải tiến xuống $\mathcal{O}(n^3)$.

### Thuật toán $\mathcal{O}(n^4)$

Để tránh mơ hồ, trước hết ta chủ yếu xét bài toán phân công ở dạng ma trận (tức cho ma trận $A$, cần chọn $n$ ô nằm ở các hàng và cột đôi một khác nhau). Ta đánh số mảng từ $1$, chẳng hạn ma trận $A$ có chỉ số $A[1 \dots n][1 \dots n]$.

Ta cũng giả sử mọi số trong ma trận A đều **không âm** (nếu không, luôn có thể cộng cùng một hằng số vào mọi phần tử để ma trận trở thành không âm).

Ta gọi hai mảng số bất kỳ $u[1 \ldots n]$ và $v[1 \ldots n]$ là một **thế** (potential) nếu thỏa điều kiện:

$$u[i]+v[j]\leq A[i][j],\quad i=1\dots n,\ j=1\dots n$$

(Có thể thấy $u[i]$ ứng với hàng thứ $i$, còn $v[j]$ ứng với cột thứ $j$ của ma trận).

Ta gọi **giá trị $f$ của thế** là tổng các phần tử của hai mảng:

$$f=\sum_{i=1}^{n} u[i] + \sum_{j=1}^{n} v[j].$$

Một mặt, dễ thấy chi phí của nghiệm cần tìm $sol$ **không nhỏ hơn** giá trị của bất kỳ thế nào.

!!! info ""

    **Bổ đề.** $sol\geq f.$

??? info "Chứng minh"

    Nghiệm cần tìm gồm $n$ ô của ma trận $A$, nên với mỗi ô được chọn ta có $u[i]+v[j]\leq A[i][j]$. Vì các phần tử trong $sol$ nằm ở các hàng và cột khác nhau, cộng các bất đẳng thức này trên mọi $A[i][j]$ được chọn sẽ cho $f$ ở vế trái và $sol$ ở vế phải.

Mặt khác, hóa ra luôn tồn tại một nghiệm và một thế khiến bất đẳng thức này trở thành **đẳng thức**. Thuật toán Hungary dưới đây chính là một chứng minh mang tính xây dựng cho điều đó. Tạm thời, chỉ cần chú ý rằng nếu chi phí của một nghiệm bằng giá trị của một thế nào đó, nghiệm này là **tối ưu**.

Với một thế cố định, gọi cạnh $(i,j)$ là **cạnh chặt** (rigid edge) nếu $u[i]+v[j]=A[i][j].$

Nhắc lại cách phát biểu bài toán phân công bằng đồ thị hai phía. Ký hiệu $H$ là đồ thị hai phía chỉ gồm các cạnh chặt. Với thế hiện tại, thuật toán Hungary sẽ duy trì **cặp ghép có số cạnh lớn nhất** $M$ của đồ thị $H$. Ngay khi $M$ có $n$ cạnh, nghiệm của bài toán chính là $M$ (vì đây là một nghiệm có chi phí trùng với giá trị của một thế).

Ta đi thẳng vào **mô tả thuật toán**.

**Bước 1.** Ban đầu, thế được đặt bằng không ($u[i]=v[i]=0$ với mọi $i$), còn cặp ghép $M$ là rỗng.

**Bước 2.** Ở mỗi bước, ta cố tăng số cạnh của cặp ghép hiện tại $M$ thêm một mà không thay đổi thế (nhớ rằng ta đang tìm cặp ghép trong đồ thị cạnh chặt $H$). Để làm vậy, ta dùng [thuật toán Kuhn tìm cặp ghép cực đại trên đồ thị hai phía](kuhn_maximum_bipartite_matching.md). Nhắc lại thuật toán ở đây.
Mọi cạnh thuộc cặp ghép $M$ được định hướng từ phần bên phải sang phần bên trái, còn mọi cạnh khác của đồ thị $H$ được định hướng theo chiều ngược lại.

Theo thuật ngữ của bài toán cặp ghép, một đỉnh được gọi là bão hòa nếu có một cạnh của cặp ghép hiện tại kề với nó. Một đỉnh không kề với cạnh nào của cặp ghép hiện tại được gọi là chưa bão hòa. Một đường đi độ dài lẻ, có cạnh đầu tiên không thuộc cặp ghép và các cạnh sau đó luân phiên thuộc/không thuộc cặp ghép, được gọi là đường tăng.
Ta bắt đầu [duyệt theo chiều sâu](depth-first-search.md) hoặc [duyệt theo chiều rộng](breadth-first-search.md) từ mọi đỉnh chưa bão hòa thuộc phần bên trái. Nếu quá trình duyệt đi tới được một đỉnh chưa bão hòa thuộc phần bên phải, ta đã tìm được một đường tăng từ trái sang phải. Nếu thêm các cạnh lẻ trên đường vào cặp ghép và bỏ các cạnh chẵn (tức thêm cạnh thứ nhất, bỏ cạnh thứ hai, thêm cạnh thứ ba, v.v.), số cạnh của cặp ghép tăng thêm một.

Nếu không tồn tại đường tăng, cặp ghép hiện tại $M$ là tối đại trong đồ thị $H$.

**Ghi chú bản dịch:** Theo bổ đề Berge được chính bài Kuhn sử dụng, không tồn tại đường tăng thực ra suy ra cặp ghép hiện tại là **cực đại** (maximum), mạnh hơn “tối đại” (maximal). Nguồn tiếng Anh dùng từ “maximal” ở câu trên; bản dịch giữ sát wording nguồn và ghi rõ điểm này để đề xuất sửa upstream.

**Bước 3.** Nếu ở bước hiện tại không thể tăng số cạnh của cặp ghép, ta tính lại thế sao cho ở các bước tiếp theo có thêm cơ hội tăng cặp ghép.

Ký hiệu $Z_1$ là tập các đỉnh thuộc phần bên trái đã được thăm trong lần duyệt cuối của thuật toán Kuhn, và $Z_2$ là tập các đỉnh thuộc phần bên phải đã được thăm.

Tính $\Delta$:

$$\Delta = \min_{i\in Z_1,\ j\notin Z_2} A[i][j]-u[i]-v[j].$$

!!! info ""

     **Bổ đề.** $\Delta > 0.$

??? info "Chứng minh"

    Giả sử $\Delta=0$. Khi đó tồn tại một cạnh chặt $(i,j)$ với $i\in Z_1$ và $j\notin Z_2$. Suy ra cạnh $(i,j)$ phải được định hướng từ phần bên phải sang phần bên trái, tức $(i,j)$ thuộc cặp ghép $M$. Nhưng điều này không thể xảy ra, vì ta không thể đi tới đỉnh bão hòa $i$ nếu không đi theo cạnh từ j tới i. Do đó $\Delta > 0$.

Bây giờ ta **tính lại thế** như sau:

- với mọi đỉnh $i\in Z_1$, thực hiện $u[i] \gets u[i]+\Delta$,

- với mọi đỉnh $j\in Z_2$, thực hiện $v[j] \gets v[j]-\Delta$.

!!! info ""

    **Bổ đề.** Thế thu được vẫn là một thế hợp lệ.

??? info "Chứng minh"

    Ta chứng minh rằng sau khi tính lại, $u[i]+v[j]\leq A[i][j]$ với mọi $i,j$. Với mọi phần tử của $A$ có $i\in Z_1$ và $j\in Z_2$, tổng $u[i]+v[j]$ không đổi nên bất đẳng thức vẫn đúng. Với mọi phần tử có $i\notin Z_1$ và $j\in Z_2$, tổng $u[i]+v[j]$ giảm đi $\Delta$, nên bất đẳng thức vẫn đúng. Với các phần tử còn lại có $i\in Z_1$ và $j\notin Z_2$, tổng tăng lên, nhưng bất đẳng thức vẫn được bảo toàn vì theo định nghĩa, $\Delta$ là mức tăng lớn nhất không làm vi phạm bất đẳng thức.

!!! info ""

    **Bổ đề.** Cặp ghép cũ $M$ gồm các cạnh chặt vẫn hợp lệ, tức mọi cạnh của cặp ghép vẫn là cạnh chặt.

??? info "Chứng minh"

    Để một cạnh chặt $(i,j)$ không còn chặt sau khi đổi thế, đẳng thức $u[i] + v[j] = A[i][j]$ phải trở thành bất đẳng thức $u[i] + v[j] < A[i][j]$. Điều này chỉ có thể xảy ra khi $i \notin Z_1$ và $j \in Z_2$. Nhưng $i \notin Z_1$ suy ra cạnh $(i,j)$ không thể là cạnh của cặp ghép.

!!! info ""

    **Bổ đề.** Sau mỗi lần tính lại thế, số đỉnh có thể đi tới trong phép duyệt, tức $|Z_1|+|Z_2|$, tăng nghiêm ngặt.

??? info "Chứng minh"

    Trước hết, mọi đỉnh đi tới được trước khi tính lại vẫn đi tới được sau đó. Thật vậy, nếu một đỉnh đi tới được thì tồn tại một đường đi từ một đỉnh chưa bão hòa thuộc phần bên trái tới nó; vì với các cạnh dạng $(i,j),\ i\in Z_1,\ j\in Z_2$, tổng $u[i]+v[j]$ không đổi, toàn bộ đường đi này vẫn tồn tại sau khi thay đổi thế.
    Tiếp theo, sau mỗi lần tính lại sẽ có ít nhất một đỉnh mới đi tới được. Điều này suy ra từ định nghĩa $\Delta$: cạnh $(i,j)$ tương ứng với giá trị $\Delta$ sẽ trở thành cạnh chặt, nên đỉnh $j$ sẽ đi tới được từ đỉnh $i$.

Từ bổ đề cuối, trước khi tìm được một đường tăng và tăng số cạnh của $M$, có thể xảy ra **không quá $n$ lần tính lại thế**.
Vì vậy, sớm hay muộn ta sẽ tìm được một thế tương ứng với cặp ghép hoàn hảo $M^*$, và $M^*$ chính là đáp án của bài toán.
Về độ phức tạp, thuật toán chạy trong $\mathcal{O}(n^4)$: tổng cộng có không quá $n$ lần tăng cặp ghép; trước mỗi lần như vậy có không quá $n$ lần tính lại thế, mỗi lần tốn $\mathcal{O}(n^2)$.

Ta không trình bày cài đặt của thuật toán $\mathcal{O}(n^4)$ vì nó không ngắn hơn cài đặt $\mathcal{O}(n^3)$ dưới đây.

### Thuật toán $\mathcal{O}(n^3)$

Bây giờ ta tìm cách cài đặt cùng thuật toán trong $\mathcal{O}(n^3)$ (với bài toán chữ nhật $n \times m$, là $\mathcal{O}(n^2m)$).

Ý tưởng then chốt là **xét từng hàng của ma trận một**, thay vì xét tất cả cùng lúc. Khi đó thuật toán ở trên có dạng:

1.  Xét hàng tiếp theo của ma trận $A$.

2.  Chừng nào chưa có đường tăng bắt đầu từ hàng này, tính lại thế.

3.  Ngay khi tìm được một đường tăng, cập nhật cặp ghép dọc theo đường đó (nhờ đó đưa cạnh cuối vào cặp ghép), rồi quay lại bước 1 để xét hàng tiếp theo.

Để đạt độ phức tạp yêu cầu, cần cài đặt các bước 2-3, được thực hiện cho mỗi hàng, trong $\mathcal{O}(n^2)$ (với bài toán chữ nhật là $\mathcal{O}(nm)$).

Nhắc lại hai kết quả đã chứng minh ở trên:

- Khi thế thay đổi, các đỉnh đã đi tới được trong phép duyệt của Kuhn vẫn đi tới được.

- Tổng cộng chỉ có thể có $\mathcal{O}(n)$ lần tính lại thế trước khi tìm được một đường tăng.

Từ đó có các **ý tưởng then chốt** để đạt độ phức tạp yêu cầu:

- Để kiểm tra có đường tăng hay không, không cần khởi động lại phép duyệt Kuhn sau mỗi lần tính lại thế. Thay vào đó, có thể thực hiện phép duyệt Kuhn ở **dạng lặp**: sau mỗi lần tính lại thế, xét các cạnh chặt mới được thêm; nếu đầu trái của chúng đi tới được thì đánh dấu đầu phải cũng đi tới được rồi tiếp tục duyệt từ đó.

- Phát triển ý tưởng trên, có thể mô tả thuật toán như sau: ở mỗi bước của vòng lặp, ta tính lại thế. Sau đó xác định một cột vừa trở thành đi tới được (cột như vậy luôn tồn tại vì sau mỗi lần tính lại thế đều có đỉnh mới đi tới được). Nếu cột chưa bão hòa, ta tìm được một đường tăng. Ngược lại, nếu cột đã bão hòa thì hàng được ghép với nó cũng trở thành đi tới được.

- Để tính lại thế nhanh hơn cách ngây thơ $\mathcal{O}(n^2)$, ta duy trì giá trị nhỏ nhất phụ trợ cho từng cột:

    <br><div style="text-align:center">$minv[j]=\min_{i\in Z_1} A[i][j]-u[i]-v[j].$</div><br>

    Dễ thấy giá trị $\Delta$ cần tìm được biểu diễn qua chúng như sau:

    <br><div style="text-align:center">$\Delta=\min_{j\notin Z_2} minv[j].$</div><br>

    Nhờ đó, có thể tìm $\Delta$ trong $\mathcal{O}(n)$.

    Cần cập nhật mảng $minv$ khi có hàng mới được thăm. Việc này tốn $\mathcal{O}(n)$ cho hàng vừa thêm (cộng trên mọi hàng là $\mathcal{O}(n^2)$). Mảng $minv$ cũng phải được cập nhật khi tính lại thế; thao tác này cũng tốn $\mathcal{O}(n)$ ($minv$ chỉ thay đổi với các cột chưa đi tới được, cụ thể là giảm đi $\Delta$).

Như vậy, thuật toán có dạng sau: vòng lặp ngoài xét lần lượt các hàng của ma trận. Mỗi hàng được xử lý trong $\mathcal{O}(n^2)$ vì chỉ có $\mathcal{O}(n)$ lần tính lại thế (mỗi lần tốn $\mathcal{O}(n)$), mảng $minv$ được duy trì trong $\mathcal{O}(n^2)$, và phép duyệt Kuhn chạy trong $\mathcal{O}(n^2)$ (vì được biểu diễn thành $\mathcal{O}(n)$ lần lặp, mỗi lần thăm một cột mới).

Do đó, độ phức tạp tổng là $\mathcal{O}(n^3)$; với bài toán chữ nhật là $\mathcal{O}(n^2m)$.

## Cài đặt thuật toán Hungary

Cài đặt dưới đây do **Andrey Lopatin** phát triển vài năm trước. Điểm nổi bật là cực kỳ ngắn gọn: toàn bộ thuật toán chỉ gồm **30 dòng mã**.

Cài đặt tìm nghiệm cho ma trận chữ nhật $A[1\dots n][1\dots m]$, với $n\leq m$. Ma trận được đánh số từ 1 để thuận tiện và rút gọn mã: cài đặt thêm một hàng 0 và cột 0 giả, nhờ đó nhiều vòng lặp có thể viết thống nhất mà không cần kiểm tra phụ.

Hai mảng $u[0 \ldots n]$ và $v[0 \ldots m]$ lưu thế. Ban đầu chúng được đặt bằng không, phù hợp với ma trận có hàng 0 (Lưu ý rằng với cài đặt này, ma trận $A$ có chứa số âm hay không cũng không quan trọng).

Mảng $p[0 \ldots m]$ lưu cặp ghép: với mỗi cột $j = 1 \ldots m$, nó lưu số hiệu hàng được chọn $p[j]$ (hoặc $0$ nếu chưa chọn hàng nào). Để cài đặt thuận tiện, giả sử $p[0]$ bằng số hiệu của hàng hiện tại.

Mảng $minv[1 \ldots m]$ lưu cho mỗi cột $j$ giá trị nhỏ nhất phụ trợ cần thiết để tính lại thế nhanh như mô tả ở trên.

Mảng $way[1 \ldots m]$ lưu thông tin về vị trí đạt các giá trị nhỏ nhất đó để sau này truy vết đường tăng. Để truy vết đường, chỉ cần lưu số hiệu cột vì số hiệu hàng có thể lấy từ cặp ghép (tức từ mảng $p$). Vì vậy, với mỗi cột $j$, $way[j]$ lưu số hiệu cột trước đó trên đường (hoặc $0$ nếu không có).

Thuật toán gồm một **vòng lặp qua các hàng của ma trận**; bên trong, hàng thứ $i$ được xét. Vòng lặp _do-while_ thứ nhất chạy cho đến khi tìm được một cột tự do $j0$. Mỗi lần lặp đánh dấu một cột mới $j0$ là đã thăm (được tính ở lần lặp trước, ban đầu bằng không — tức bắt đầu từ cột giả), đồng thời xác định một hàng mới $i0$ kề với nó trong cặp ghép (tức $p[j0]$; khi $j0=0$ ban đầu thì lấy hàng thứ $i$). Do xuất hiện hàng đã thăm mới $i0$, ta cần cập nhật mảng $minv$ và $\Delta$. Nếu $\Delta$ được cập nhật thì cột $j1$ là vị trí đạt giá trị nhỏ nhất (với cách cài đặt này, $\Delta$ có thể bằng không, tức ở bước hiện tại không cần đổi thế vì đã có một cột mới đi tới được). Sau đó, ta tính lại thế và mảng $minv$. Khi vòng lặp "do-while" kết thúc, ta đã tìm được một đường tăng kết thúc tại cột $j0$ và có thể "mở ngược" đường này bằng mảng đỉnh trước $way$.

Hằng số <tt>INF</tt> là "vô hạn", tức một số hiển nhiên lớn hơn mọi số có thể xuất hiện trong ma trận đầu vào $A$.

```{.cpp file=hungarian}
vector<int> u (n+1), v (m+1), p (m+1), way (m+1);
for (int i=1; i<=n; ++i) {
    p[0] = i;
    int j0 = 0;
    vector<int> minv (m+1, INF);
    vector<bool> used (m+1, false);
    do {
        used[j0] = true;
        int i0 = p[j0],  delta = INF,  j1;
        for (int j=1; j<=m; ++j)
            if (!used[j]) {
                int cur = A[i0][j]-u[i0]-v[j];
                if (cur < minv[j])
                    minv[j] = cur,  way[j] = j0;
                if (minv[j] < delta)
                    delta = minv[j],  j1 = j;
            }
        for (int j=0; j<=m; ++j)
            if (used[j])
                u[p[j]] += delta,  v[j] -= delta;
            else
                minv[j] -= delta;
        j0 = j1;
    } while (p[j0] != 0);
    do {
        int j1 = way[j0];
        p[j0] = p[j1];
        j0 = j1;
    } while (j0);
}
```

Có thể khôi phục đáp án ở dạng quen thuộc hơn — với mỗi hàng $i = 1 \ldots n$, tìm số hiệu cột được chọn $ans[i]$ — như sau:

```cpp
vector<int> ans (n+1);
for (int j=1; j<=m; ++j)
    ans[p[j]] = j;
```

Chi phí của cặp ghép có thể lấy trực tiếp từ thế của cột 0 (đổi dấu). Thật vậy, từ mã nguồn có thể thấy $-v[0]$ chứa tổng mọi giá trị $\Delta$, tức tổng thay đổi của thế. Mặc dù nhiều giá trị $u[i]$ và $v[j]$ có thể thay đổi cùng lúc, tổng thay đổi của thế vẫn đúng bằng $\Delta$, vì trước khi có đường tăng, số hàng đi tới được luôn nhiều hơn số cột đi tới được đúng một (chỉ hàng hiện tại $i$ chưa có một "cặp" là cột đã thăm):

```cpp
int cost = -v[0];
```

## Liên hệ với thuật toán đường đi ngắn nhất liên tiếp

Có thể xem thuật toán Hungary là [thuật toán đường đi ngắn nhất liên tiếp](min_cost_flow.md) được điều chỉnh riêng cho bài toán phân công. Không đi sâu vào chi tiết, ta nêu trực giác về mối liên hệ giữa hai thuật toán.

Thuật toán đường đi ngắn nhất liên tiếp sử dụng một phiên bản sửa đổi của thuật toán Johnson để đổi trọng số. Quá trình này gồm bốn bước:

- Dùng thuật toán [Bellman-Ford](bellman_ford.md), bắt đầu từ nguồn $s$ và với mỗi đỉnh tìm trọng số nhỏ nhất $h(v)$ của một đường đi từ $s$ tới $v$.

**Ghi chú bản dịch:** Nguồn tiếng Anh gọi $s$ là “sink” ở câu trên, nhưng ký hiệu và đường đi đều bắt đầu từ $s$; trong ngữ cảnh này phải là **source**. Bản dịch dùng “nguồn” và tách lỗi này để đề xuất sửa upstream.

Với mỗi bước của thuật toán chính:

- Đổi trọng số các cạnh của đồ thị ban đầu như sau: $w(u,v) \gets w(u,v)+h(u)-h(v)$.
- Dùng thuật toán [Dijkstra](dijkstra.md) để tìm đồ thị con các đường đi ngắn nhất của mạng ban đầu.
- Cập nhật các thế cho lần lặp tiếp theo.

Từ mô tả này có thể thấy sự tương đồng mạnh giữa $h(v)$ và các thế: có thể kiểm tra rằng chúng bằng nhau sai khác một hằng số. Ngoài ra, sau khi đổi trọng số, tập mọi cạnh trọng số bằng không chính là đồ thị con đường đi ngắn nhất mà thuật toán chính cố tăng luồng trên đó. Điều tương tự xảy ra trong thuật toán Hungary: ta tạo đồ thị con gồm các cạnh chặt (những cạnh có $A[i][j]-u[i]-v[j]$ bằng không) rồi cố tăng kích thước cặp ghép.

Ở bước 4, mọi $h(v)$ được cập nhật: mỗi khi sửa mạng luồng, ta phải bảo đảm khoảng cách từ nguồn vẫn đúng (nếu không, ở lần lặp sau thuật toán Dijkstra có thể sai). Điều này giống phép cập nhật các thế, nhưng trong trường hợp này chúng không được tăng đều như nhau.

Để hiểu sâu hơn về thế, xem [bài viết này](https://codeforces.com/blog/entry/105658).

## Ví dụ bài toán

Dưới đây là một số ví dụ liên quan đến bài toán phân công, từ rất trực tiếp đến ít hiển nhiên hơn:

- Cho một đồ thị hai phía, cần tìm **cặp ghép cực đại có trọng số nhỏ nhất** (trước hết tối đa hóa số cạnh của cặp ghép, sau đó tối thiểu hóa chi phí).<br>
  Ta xây dựng bài toán phân công bằng cách đặt trọng số "vô hạn" cho các cạnh không tồn tại. Sau khi giải bằng thuật toán Hungary, bỏ khỏi đáp án các cạnh có trọng số vô hạn (các cạnh này có thể xuất hiện nếu bài toán không có nghiệm là một cặp ghép hoàn hảo).

- Cho một đồ thị hai phía, cần tìm **cặp ghép cực đại có trọng số lớn nhất**.<br>
  Cách giải cũng trực tiếp: nhân mọi trọng số với âm một.

- Bài toán **phát hiện vật thể chuyển động trong ảnh**: hai ảnh được chụp tại hai thời điểm, thu được hai tập tọa độ. Cần ghép các vật thể ở ảnh thứ nhất với ảnh thứ hai, tức xác định mỗi điểm ở ảnh thứ hai tương ứng với điểm nào ở ảnh thứ nhất. Ta muốn tối thiểu hóa tổng khoảng cách giữa các cặp điểm (tức tổng quãng đường mà các vật thể đã di chuyển là nhỏ nhất).<br>
  Chỉ cần xây dựng và giải bài toán phân công, với trọng số cạnh là khoảng cách Euclid giữa hai điểm.

- Bài toán **phát hiện vật thể chuyển động bằng thiết bị định hướng**: có hai thiết bị không xác định được vị trí vật thể trong không gian mà chỉ xác định được hướng của chúng. Hai thiết bị (đặt tại hai vị trí khác nhau) đều nhận được $n$ hướng. Cần xác định vị trí các vật thể, tức ghép cặp các hướng của hai thiết bị sao cho tổng khoảng cách từ các vị trí vật thể dự đoán tới các tia chỉ hướng là nhỏ nhất.<br>
  Ta lại xây dựng và giải bài toán phân công: các đỉnh phần bên trái là $n$ hướng của thiết bị thứ nhất, các đỉnh phần bên phải là $n$ hướng của thiết bị thứ hai, còn trọng số cạnh là khoảng cách giữa hai tia tương ứng.

- Phủ một **đồ thị có hướng không chu trình bằng các đường đi**: cho một DAG, cần tìm số đường đi ít nhất (nếu bằng nhau thì tổng trọng số nhỏ nhất) sao cho mỗi đỉnh của đồ thị nằm trên đúng một đường đi.<br>
  Ta xây dựng đồ thị hai phía tương ứng từ đồ thị ban đầu rồi tìm cặp ghép cực đại có trọng số nhỏ nhất. Xem bài viết riêng để biết thêm chi tiết.

- **Tô màu cây**. Cho một cây mà mỗi đỉnh, trừ lá, có đúng $k-1$ con. Cần chọn cho mỗi đỉnh một trong $k$ màu sao cho hai đỉnh kề nhau không cùng màu. Ngoài ra, biết chi phí tô mỗi đỉnh bằng mỗi màu và cần tối thiểu hóa tổng chi phí.<br>
  Ta dùng quy hoạch động. Cụ thể, tính $d[v][c]$, trong đó $v$ là số hiệu đỉnh, $c$ là màu, và $d[v][c]$ là chi phí nhỏ nhất để tô toàn bộ cây con gốc $v$ khi chính đỉnh $v$ có màu $c$. Để tính $d[v][c]$, cần phân phối $k-1$ màu còn lại cho các con của $v$; đây chính là một bài toán phân công (phần bên trái là màu, phần bên phải là các đỉnh con, trọng số cạnh là các giá trị $d$ tương ứng).<br>
  Vì vậy, mỗi giá trị $d[v][c]$ được tính bằng cách giải một bài toán phân công, cho độ phức tạp cuối cùng là $\mathcal{O}(nk^4)$.

- Nếu trong bài toán phân công, trọng số không nằm trên cạnh mà nằm trên đỉnh, và chỉ **trên các đỉnh của cùng một phần**, thì không cần dùng thuật toán Hungary: chỉ cần sắp xếp các đỉnh theo trọng số rồi chạy [thuật toán Kuhn](kuhn_maximum_bipartite_matching.md) thông thường (xem [bài viết riêng](http://e-maxx.ru/algo/vertex_weighted_matching) để biết chi tiết).

- Xét **trường hợp đặc biệt** sau. Mỗi đỉnh của phần bên trái được gán một số $\alpha[i]$, mỗi đỉnh của phần bên phải được gán một số $\beta[j]$. Trọng số của cạnh $(i,j)$ bằng $\alpha[i]\cdot \beta[j]$ (các số $\alpha[i]$ và $\beta[j]$ đã biết). Hãy giải bài toán phân công.<br>
  Để giải mà không dùng thuật toán Hungary, trước hết xét trường hợp mỗi phần có hai đỉnh. Khi đó dễ thấy cách tốt hơn là nối theo thứ tự ngược: đỉnh có $\alpha[i]$ nhỏ hơn nối với đỉnh có $\beta[j]$ lớn hơn. Quy tắc này mở rộng được cho số đỉnh bất kỳ: sắp các đỉnh phần thứ nhất theo $\alpha[i]$ tăng dần, phần thứ hai theo $\beta[j]$ giảm dần, rồi ghép các đỉnh theo cặp theo thứ tự đó. Ta thu được lời giải $\mathcal{O}(n\log n)$.

- **Bài toán về thế**. Cho ma trận $A[1 \ldots n][1 \ldots m]$, cần tìm hai mảng $u[1 \ldots n]$ và $v[1 \ldots m]$ sao cho với mọi $i$ và $j$, $u[i] + v[j] \leq a[i][j]$ và tổng các phần tử của hai mảng $u$ và $v$ là lớn nhất.<br>
  Nếu biết thuật toán Hungary, bài toán này không khó: thuật toán Hungary chính là tìm một thế $u, v$ thỏa yêu cầu. Ngược lại, nếu chưa biết thuật toán Hungary thì bài toán này có vẻ gần như không thể giải trực tiếp.

    !!! info "Ghi chú"

        Bài toán này còn được gọi là **bài toán đối ngẫu** (dual problem) của bài toán phân công: tối thiểu hóa tổng chi phí phân công tương đương với tối đa hóa tổng các thế.

## Tài liệu tham khảo

- [Ravindra Ahuja, Thomas Magnanti, James Orlin. Network Flows [1993]](https://books.google.it/books/about/Network_Flows.html?id=rFuLngEACAAJ&redir_esc=y)

- [Harold Kuhn. The Hungarian Method for the Assignment Problem [1955]](https://link.springer.com/chapter/10.1007/978-3-540-68279-0_2)

- [James Munkres. Algorithms for Assignment and Transportation Problems [1957]](https://www.jstor.org/stable/2098689)

## Bài tập luyện tập

- [UVA - Crime Wave - The Sequel](http://uva.onlinejudge.org/index.php?option=com_onlinejudge&Itemid=8&page=show_problem&problem=1687)

- [UVA - Warehouse](http://uva.onlinejudge.org/index.php?option=com_onlinejudge&Itemid=8&page=show_problem&problem=1829)

- [SGU - Beloved Sons](http://acm.sgu.ru/problem.php?contest=0&problem=210)

- [UVA - The Great Wall Game](http://livearchive.onlinejudge.org/index.php?option=com_onlinejudge&Itemid=8&page=show_problem&problem=1277)

- [UVA - Jogging Trails](http://uva.onlinejudge.org/index.php?option=com_onlinejudge&Itemid=8&page=show_problem&problem=1237)