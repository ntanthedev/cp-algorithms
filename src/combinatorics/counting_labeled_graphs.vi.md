---
tags:
  - Translated
e_maxx_link: counting_connected_graphs
translation:
  source: combinatorics/counting_labeled_graphs.md
  source_commit: 6060b38ac1137c98ff535c9efcfc66bda662aa36
  status: draft
  last_synced: 2026-11-15
---

# Đếm đồ thị có nhãn

## Đồ thị có nhãn

Cho một đồ thị có $n$ đỉnh.
Ta cần tính số lượng $G_n$ đồ thị có nhãn với $n$ đỉnh (có nhãn nghĩa là các đỉnh được đánh số từ $1$ đến $n$).
Các cạnh được coi là vô hướng; không cho phép khuyên và đa cạnh.

Xét tập hợp tất cả các cạnh có thể có của đồ thị.
Với mỗi cạnh $(i, j)$, ta có thể giả sử $i < j$ (vì đồ thị vô hướng và không có khuyên).
Do đó tập hợp tất cả các cạnh có lực lượng $\binom{n}{2}$, tức $\frac{n(n-1)}{2}$.

Vì mỗi đồ thị có nhãn được xác định duy nhất bởi các cạnh của nó, số đồ thị có nhãn với $n$ đỉnh bằng:

$$G_n = 2^{\frac{n(n-1)}{2}}$$

## Đồ thị liên thông có nhãn

Ở đây, ta thêm điều kiện đồ thị phải liên thông.

Gọi số đồ thị liên thông cần tìm với $n$ đỉnh là $C_n$.

Trước hết, ta xét có bao nhiêu đồ thị **không liên thông**.
Khi đó số đồ thị liên thông bằng $G_n$ trừ đi số đồ thị không liên thông.
Cụ thể hơn, ta sẽ đếm số **đồ thị không liên thông có gốc**. Đồ thị có gốc là đồ thị trong đó một đỉnh được chọn làm gốc.
Rõ ràng có $n$ cách chọn gốc cho đồ thị có $n$ đỉnh được gán nhãn; vì vậy cuối cùng ta cần chia số đồ thị không liên thông có gốc cho $n$ để được số đồ thị không liên thông.

Đỉnh gốc nằm trong một thành phần liên thông có kích thước thuộc $1, \dots n-1$.
Có $k \binom{n}{k} C_k G_{n-k}$ đồ thị mà đỉnh gốc nằm trong thành phần liên thông có $k$ đỉnh (có $\binom{n}{k}$ cách chọn $k$ đỉnh cho thành phần, nối chúng thành đồ thị liên thông theo một trong $C_k$ cách, chọn bất kỳ một trong $k$ đỉnh làm gốc, và nối hoặc không nối $n-k$ đỉnh còn lại tùy ý, tạo ra thừa số $G_{n-k}$).
Do đó số đồ thị không liên thông với $n$ đỉnh là:

$$\frac{1}{n} \sum_{k=1}^{n-1} k \binom{n}{k} C_k G_{n-k}$$

Cuối cùng, số đồ thị liên thông là:

$$C_n = G_n - \frac{1}{n} \sum_{k=1}^{n-1} k \binom{n}{k} C_k G_{n-k}$$

## Đồ thị có nhãn với $k$ thành phần liên thông {data-toc-label="Labeled graphs with k connected components"}

Dựa trên công thức ở phần trước, ta sẽ tìm cách đếm số đồ thị có nhãn với $n$ đỉnh và $k$ thành phần liên thông.

Có thể tính số này bằng quy hoạch động.
Ta tính $D[i][j]$ — số đồ thị có nhãn với $i$ đỉnh và $j$ thành phần — với mỗi $i \le n$ và $j \le k$.

Xét cách tính phần tử tiếp theo $D[n][k]$ khi đã biết các giá trị trước đó.
Ta dùng một cách tiếp cận phổ biến: lấy đỉnh cuối cùng (có chỉ số $n$).
Đỉnh này thuộc một thành phần nào đó.
Nếu kích thước thành phần là $s$, có $\binom{n-1}{s-1}$ cách chọn tập đỉnh như vậy và $C_s$ cách nối chúng thành đồ thị liên thông. Sau khi loại thành phần này khỏi đồ thị, còn lại $n-s$ đỉnh với $k-1$ thành phần liên thông.
Vì vậy ta được công thức truy hồi sau:

$$D[n][k] = \sum_{s=1}^{n} \binom{n-1}{s-1} C_s D[n-s][k-1]$$
