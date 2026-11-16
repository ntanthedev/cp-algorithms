---
tags:
  - Translated
e_maxx_link: fixed_length_paths
translation:
  source: graph/fixed_length_paths.md
  source_commit: fd3810f9a6ae7d6afc0e1c8993dfd20225b0ea5a
  status: draft
  last_synced: 2026-11-15
---

# Số đường đi có độ dài cố định / Đường đi ngắn nhất có độ dài cố định

Bài viết này trình bày lời giải cho hai bài toán dựa trên cùng một ý tưởng: quy bài toán về việc dựng ma trận, rồi tính kết quả bằng phép nhân ma trận thông thường hoặc một phép nhân đã được biến đổi.

## Số đường đi có độ dài cố định

Cho đồ thị có hướng, không trọng số $G$ với $n$ đỉnh và một số nguyên $k$.
Với mỗi cặp đỉnh $(i, j)$, ta cần tìm số đường đi độ dài $k$ giữa chúng.
Đường đi không cần đơn: trong một đường đi, ta có thể đi qua một đỉnh hoặc một cạnh tùy ý số lần.

Ta biểu diễn đồ thị bằng ma trận kề $G[][]$ kích thước $n \times n$; mỗi phần tử $G[i][j]$ bằng $1$ nếu có cạnh nối đỉnh $i$ với đỉnh $j$, và bằng $0$ nếu không có cạnh.
Thuật toán cũng áp dụng được khi đồ thị có nhiều cạnh song song: nếu một cặp đỉnh $(i, j)$ được nối bằng $m$ cạnh, ta đặt $G[i][j] = m$.
Thuật toán cũng áp dụng được khi đồ thị có cạnh nối một đỉnh với chính nó.

Ma trận kề đã dựng chính là đáp án khi $k = 1$: nó chứa số đường đi có độ dài $1$ giữa mọi cặp đỉnh.

Ta xây dựng lời giải theo từng bước.
Giả sử đã biết đáp án ứng với $k$; sau đây ta tính đáp án ứng với $k + 1$.
Gọi $C_k$ là ma trận ứng với $k$, còn $C_{k+1}$ là ma trận cần dựng.
Công thức sau tính từng phần tử của $C_{k+1}$:

$$C_{k+1}[i][j] = \sum_{p = 1}^{n} C_k[i][p] \cdot G[p][j]$$

Ta thấy công thức này chính là tích hai ma trận $C_k$ và $G$:

$$C_{k+1} = C_k \cdot G$$

Vì vậy, có thể biểu diễn lời giải như sau:

$$C_k = \underbrace{G \cdot G \cdots G}_{k \text{ times}} = G^k$$

Có thể tính lũy thừa ma trận hiệu quả bằng [lũy thừa nhị phân](../algebra/binary-exp.md).
Độ phức tạp của lời giải là $O(n^3 \log k)$.

## Đường đi ngắn nhất có độ dài cố định

Cho đồ thị có hướng, có trọng số $G$ với $n$ đỉnh và một số nguyên $k$.
Với mỗi cặp đỉnh $(i, j)$, ta cần tìm độ dài đường đi ngắn nhất từ $i$ đến $j$ gồm đúng $k$ cạnh.

Ta biểu diễn đồ thị bằng ma trận kề $G[][]$ kích thước $n \times n$, trong đó mỗi phần tử $G[i][j]$ lưu độ dài các cạnh đi từ đỉnh $i$ đến đỉnh $j$.
Nếu không có cạnh nối hai đỉnh, phần tử tương ứng trong ma trận được gán bằng vô cực $\infty$.

Ma trận kề ở dạng này là đáp án khi $k = 1$.
Nó chứa độ dài đường đi ngắn nhất gồm một cạnh giữa mọi cặp đỉnh, hoặc $\infty$ nếu không có đường đi gồm một cạnh.

Ta tiếp tục xây dựng lời giải theo từng bước.
Giả sử đã biết đáp án ứng với $k$; ta sẽ tính đáp án ứng với $k+1$.
Gọi $L_k$ là ma trận ứng với $k$, còn $L_{k+1}$ là ma trận cần dựng.
Công thức sau tính từng phần tử của $L_{k+1}$:

$$L_{k+1}[i][j] = \min_{p = 1 \ldots n} \left(L_k[i][p] + G[p][j]\right)$$

Quan sát công thức, ta thấy đây là phép nhân ma trận $L_k$ với ma trận $G$, nhưng dùng phép lấy giá trị nhỏ nhất thay cho phép cộng, và dùng phép cộng thay cho phép nhân các phần tử.

$$L_{k+1} = L_k \odot G,$$

trong đó phép toán $\odot$ được định nghĩa như sau:

$$A \odot B = C~~\Longleftrightarrow~~C_{i j} = \min_{p = 1 \ldots n}\left(A_{i p} + B_{p j}\right)$$

Do đó, có thể biểu diễn bài toán bằng phép nhân đã biến đổi:

$$L_k = \underbrace{G \odot \ldots \odot G}_{k~\text{times}} = G^{\odot k}$$

Phép nhân biến đổi này có tính kết hợp, nên ta cũng có thể tính lũy thừa hiệu quả bằng [lũy thừa nhị phân](../algebra/binary-exp.md).
Lời giải này cũng có độ phức tạp $O(n^3 \log k)$.

## Tổng quát hóa hai bài toán cho đường đi có độ dài không quá $k$ {data-toc-label="Generalization of the problems for paths with length up to k"}

Các lời giải trên áp dụng cho đường đi có độ dài cố định $k$.
Ta có thể điều chỉnh chúng để giải các bài toán cho phép đường đi có không quá $k$ cạnh.

Để làm vậy, ta chỉnh sửa nhẹ đồ thị đầu vào.

Ta nhân đôi mỗi đỉnh: với mỗi đỉnh $v$, tạo thêm một đỉnh $v'$ rồi thêm cạnh $(v, v')$ và cạnh nối đỉnh này với chính nó $(v', v')$.
Số đường đi từ $i$ đến $j$ có không quá $k$ cạnh bằng số đường đi từ $i$ đến $j'$ có đúng $k + 1$ cạnh, vì có song ánh biến mỗi đường đi $[p_0 = i,~p_1,~\ldots,~p_{m-1},~p_m = j]$ độ dài $m \le k$ thành đường đi $[p_0 = i,~p_1,~\ldots,~p_{m-1},~p_m = j, j', \ldots, j']$ độ dài $k + 1$.

Ta cũng có thể dùng mẹo tương tự để tính đường đi ngắn nhất có không quá $k$ cạnh.
Ta lại nhân đôi mỗi đỉnh và thêm hai cạnh vừa nêu với trọng số $0$.
