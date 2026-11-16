---
tags:
  - Translated
e_maxx_link:
  - rib_connectivity
  - vertex_connectivity
translation:
  source: graph/edge_vertex_connectivity.md
  source_commit: 6f74f9e0a6dbd31d2e635615e8561e7496d917af
  status: draft
  last_synced: 2026-11-15
---

# Độ liên thông cạnh / độ liên thông đỉnh

## Định nghĩa

Cho đồ thị vô hướng $G$ có $n$ đỉnh và $m$ cạnh.
Độ liên thông cạnh và độ liên thông đỉnh đều là những đặc trưng mô tả đồ thị.

### Độ liên thông cạnh

**Độ liên thông cạnh** $\lambda$ của đồ thị $G$ là số cạnh ít nhất cần xóa để đồ thị $G$ trở nên không liên thông.

Ví dụ, đồ thị vốn không liên thông có độ liên thông cạnh bằng $0$, đồ thị liên thông có ít nhất một cầu có độ liên thông cạnh bằng $1$, còn đồ thị liên thông không có cầu có độ liên thông cạnh ít nhất là $2$.

Ta nói tập cạnh $S$ **tách** hai đỉnh $s$ và $t$ nếu sau khi xóa tất cả các cạnh trong $S$ khỏi đồ thị $G$, hai đỉnh $s$ và $t$ nằm trong các thành phần liên thông khác nhau.

Rõ ràng độ liên thông cạnh của đồ thị bằng kích thước nhỏ nhất của một tập như vậy tách hai đỉnh $s$ và $t$, lấy trên mọi cặp $(s, t)$ có thể.

### Độ liên thông đỉnh

**Độ liên thông đỉnh** $\kappa$ của đồ thị $G$ là số đỉnh ít nhất cần xóa để đồ thị $G$ trở nên không liên thông.

Ví dụ, đồ thị vốn không liên thông có độ liên thông đỉnh bằng $0$, còn đồ thị liên thông có đỉnh khớp có độ liên thông đỉnh bằng $1$.
Ta định nghĩa độ liên thông đỉnh của đồ thị đầy đủ là $n-1$.
Với mọi đồ thị khác, độ liên thông đỉnh không vượt quá $n-2$, vì ta có thể tìm được một cặp đỉnh không nối với nhau bằng cạnh và xóa tất cả $n-2$ đỉnh còn lại.

Ta nói tập đỉnh $T$ **tách** hai đỉnh $s$ và $t$ nếu sau khi xóa tất cả các đỉnh trong $T$ khỏi đồ thị $G$, hai đỉnh đó nằm trong các thành phần liên thông khác nhau.

Rõ ràng độ liên thông đỉnh của đồ thị bằng kích thước nhỏ nhất của một tập như vậy tách hai đỉnh $s$ và $t$, lấy trên mọi cặp $(s, t)$ có thể.

Ghi chú bản dịch: Với hai đỉnh kề nhau, không thể tách chúng bằng cách xóa các đỉnh khác; riêng đồ thị đầy đủ cần dùng quy ước nêu trên thay vì lấy cực tiểu trên các tập tách đỉnh thông thường.

## Tính chất

### Các bất đẳng thức Whitney

**Các bất đẳng thức Whitney** (1932) cho biết mối liên hệ giữa độ liên thông cạnh $\lambda$, độ liên thông đỉnh $\kappa$ và bậc nhỏ nhất của các đỉnh trong đồ thị $\delta$:

$$\kappa \le \lambda \le \delta$$

Theo trực giác, nếu có một tập $\lambda$ cạnh mà khi xóa chúng đồ thị không còn liên thông, ta có thể chọn một đầu mút của mỗi cạnh để tạo thành một tập đỉnh cũng làm đồ thị mất liên thông.
Tập này có kích thước $\le \lambda$.

Nếu chọn đỉnh có bậc nhỏ nhất $\delta$ và xóa mọi cạnh kề với nó, ta cũng thu được một đồ thị không liên thông.
Do đó có bất đẳng thức thứ hai $\lambda \le \delta$.

Ghi chú bản dịch: Lập luận chọn đầu mút trên đây chưa bao quát đầy đủ các trường hợp biên, chẳng hạn khi tập đỉnh được chọn chỉ để lại một đỉnh. Định nghĩa độ liên thông đỉnh của đồ thị đầy đủ cần quy ước riêng như đã nêu.

Điều thú vị là không thể cải thiện các bất đẳng thức Whitney:
tức là với bất kỳ bộ ba số nào thỏa mãn bất đẳng thức này, tồn tại ít nhất một đồ thị tương ứng.
Có thể xây dựng một đồ thị như vậy như sau:
Đồ thị gồm $2(\delta + 1)$ đỉnh; $\delta + 1$ đỉnh đầu tiên tạo thành một clique (mọi cặp đỉnh đều được nối bằng cạnh), và $\delta + 1$ đỉnh còn lại tạo thành một clique thứ hai.
Ngoài ra, ta nối hai clique bằng $\lambda$ cạnh sao cho các cạnh này dùng $\lambda$ đỉnh khác nhau ở clique thứ nhất và chỉ $\kappa$ đỉnh ở clique thứ hai.
Đồ thị thu được sẽ có ba đặc trưng trên.

Ghi chú bản dịch: Khi κ = 0 và λ > 0, cách dựng và phát biểu về mọi bộ ba trong nguồn không áp dụng như đã nêu; đồ thị không liên thông có cả độ liên thông cạnh và đỉnh bằng 0.

### Định lý Ford-Fulkerson

**Định lý Ford-Fulkerson** suy ra rằng số đường đi đôi một không chung cạnh lớn nhất nối hai đỉnh bằng số cạnh ít nhất cần xóa để tách hai đỉnh đó.

## Tính các giá trị

### Độ liên thông cạnh bằng luồng cực đại

Phương pháp này dựa trên định lý Ford-Fulkerson.

Ta duyệt mọi cặp đỉnh $(s, t)$ và với mỗi cặp, tìm số đường đi không chung cạnh lớn nhất giữa chúng.
Có thể tìm giá trị này bằng thuật toán luồng cực đại:
dùng $s$ làm nguồn, $t$ làm đích và gán dung lượng $1$ cho mỗi cạnh.
Khi đó luồng cực đại là số đường đi không chung cạnh.

Độ phức tạp của thuật toán dùng [Edmonds-Karp](../graph/edmonds_karp.md) là $O(V^2 V E^2) = O(V^3 E^2)$.
Tuy nhiên cần lưu ý rằng cận này chứa một hệ số ẩn, vì trên thực tế gần như không thể tạo ra một đồ thị khiến thuật toán luồng cực đại chạy chậm với mọi cặp nguồn và đích.
Đặc biệt, thuật toán sẽ chạy khá nhanh trên đồ thị ngẫu nhiên.

### Thuật toán chuyên biệt cho độ liên thông cạnh

Bài toán tìm độ liên thông cạnh tương đương với bài toán tìm **lát cắt cực tiểu toàn cục**.

Có những thuật toán chuyên biệt cho bài toán này.
Một trong số đó là [thuật toán Stoer-Wagner](stoer_wagner_mincut.md), chạy trong thời gian $O(V^3)$ hoặc $O(V E + V^2 \log V)$.

### Độ liên thông đỉnh

Ta lại duyệt mọi cặp đỉnh $s$ và $t$, rồi với mỗi cặp tìm số đỉnh ít nhất cần xóa để tách $s$ và $t$.

Để làm việc này, ta có thể áp dụng cùng cách tiếp cận bằng luồng cực đại như các mục trước.

Ta tách mỗi đỉnh $x$ thỏa mãn $x \neq s$ và $x \neq t$ thành hai đỉnh $x_1$ và $x_2$.
Nối hai đỉnh này bằng cạnh có hướng $(x_1, x_2)$ với dung lượng $1$, và thay mỗi cạnh $(u, v)$ bằng hai cạnh có hướng $(u_2, v_1)$ và $(v_2, u_1)$, cả hai đều có dung lượng 1.
Theo cách xây dựng, giá trị luồng cực đại sẽ bằng số đỉnh ít nhất cần xóa để tách $s$ và $t$.

Cách tiếp cận này có cùng độ phức tạp với cách dùng luồng để tìm độ liên thông cạnh.

Ghi chú bản dịch: Nguồn không định nghĩa các bản sao của hai đỉnh đầu mút dù dùng chúng trong ký hiệu cạnh. Hơn nữa, với cặp đỉnh kề nhau, cạnh trực tiếp không thể bị cắt bằng cách xóa các đỉnh khác nên phát biểu trên cần xử lý riêng. Đối với đồ thị đầy đủ cũng phải áp dụng quy ước đã nêu.
