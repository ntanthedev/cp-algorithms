---
tags:
  - Translated
e_maxx_link: kirchhoff_theorem
translation:
  source: graph/kirchhoff-theorem.md
  source_commit: e336e42b324dca1bf3e13427230cfb7137412e52
  status: draft
  last_synced: 2026-11-15
---

# Định lý Kirchhoff: Đếm số cây khung

Bài toán: Cho một đồ thị vô hướng liên thông (có thể có nhiều cạnh nối cùng một cặp đỉnh) được biểu diễn bằng ma trận kề. Hãy tìm số cây khung khác nhau của đồ thị.

Công thức sau được Kirchhoff chứng minh năm 1847.

## Định lý ma trận cây của Kirchhoff

Gọi $A$ là ma trận kề của đồ thị: $A_{u,v}$ là số cạnh giữa $u$ và $v$.
Gọi $D$ là ma trận bậc của đồ thị: đây là ma trận đường chéo với $D_{u,u}$ là bậc của đỉnh $u$ (tính cả các cạnh song song và khuyên — cạnh nối đỉnh $u$ với chính nó).

Ma trận Laplace của đồ thị được định nghĩa là $L = D - A$.
Theo định lý Kirchhoff, mọi phần bù đại số của ma trận này bằng nhau và bằng số cây khung của đồ thị.
Phần bù đại số $(i,j)$ của một ma trận là tích của $(-1)^{i + j}$ với định thức của ma trận thu được sau khi xóa hàng thứ $i$ và cột thứ $j$.
Vì vậy, chẳng hạn ta có thể xóa hàng cuối và cột cuối của ma trận $L$; trị tuyệt đối của định thức ma trận thu được sẽ cho số cây khung.

Có thể tính định thức của ma trận trong $O(N^3)$ bằng [phương pháp Gauss](../linear_algebra/determinant-gauss.md).

Chứng minh của định lý này khá khó và không được trình bày ở đây; để xem phác thảo chứng minh và các biến thể của định lý cho đồ thị không có cạnh song song và cho đồ thị có hướng, xem [Wikipedia](https://en.wikipedia.org/wiki/Kirchhoff%27s_theorem).

## Liên hệ với các định luật mạch điện Kirchhoff

Định lý ma trận cây và các định luật mạch điện của Kirchhoff có một mối liên hệ đẹp. Có thể chứng minh (dùng định luật Ohm và định luật Kirchhoff thứ nhất) rằng điện trở $R_{ij}$ giữa hai điểm $i$ và $j$ của mạch là

$$R_{ij} = \frac{ \left| L^{(i,j)} \right| }{ | L^j | }.$$

Ở đây, ma trận $L$ được xây dựng từ ma trận nghịch đảo điện trở $A$ ($A_{i,j}$ là nghịch đảo điện trở của dây dẫn giữa hai điểm $i$ và $j$) theo quy trình mô tả trong định lý ma trận cây Kirchhoff.
$T^j$ là ma trận đã xóa hàng và cột $j$, còn $T^{(i,j)}$ là ma trận đã xóa hai hàng và hai cột $i$ và $j$.

Ghi chú bản dịch: Nguồn dùng ký hiệu T trong câu trên nhưng dùng L trong công thức; các ma trận con ở đây cần được hiểu là lấy từ L. Với khuyên, cách tính bậc và đường chéo của ma trận kề cần nhất quán để khuyên không làm thay đổi ma trận Laplace; nguồn chưa nói rõ quy ước này.

Định lý Kirchhoff cho công thức này một ý nghĩa hình học.

## Bài tập
 - [CODECHEF: Roads in Stars](https://www.codechef.com/problems/STARROAD)
 - [SPOJ: Maze](http://www.spoj.com/problems/KPMAZE/)
 - [CODECHEF: Complement Spanning Trees](https://www.codechef.com/problems/CSTREE)
