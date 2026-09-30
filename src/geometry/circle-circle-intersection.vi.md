---
tags:
  - Translated
e_maxx_link: circles_intersection
translation:
  source: geometry/circle-circle-intersection.md
  source_commit: ef7ab4e647558ee220ad400fa0cb78309e721fa4
  status: draft
  last_synced: 2026-09-29
---

# Giao của hai đường tròn

Cho hai đường tròn trên mặt phẳng 2D, mỗi đường tròn được mô tả bởi tọa độ tâm và bán kính. Hãy tìm các giao điểm của chúng (các trường hợp có thể xảy ra: một hoặc hai giao điểm, không có giao điểm, hoặc hai đường tròn trùng nhau).

## Lời giải

Ta sẽ đưa bài toán này về [bài toán giao của đường tròn và đường thẳng](circle-line-intersection.md).

Không mất tính tổng quát, giả sử đường tròn thứ nhất có tâm tại gốc tọa độ (nếu không, ta có thể dời gốc tọa độ tới tâm đường tròn thứ nhất rồi điều chỉnh lại tọa độ các giao điểm khi xuất kết quả). Ta có hệ hai phương trình:

$$x^2+y^2=r_1^2$$

$$(x - x_2)^2 + (y - y_2)^2 = r_2^2$$

Lấy phương trình thứ hai trừ phương trình thứ nhất để loại các số hạng bậc hai:

$$x^2+y^2=r_1^2$$

$$x \cdot (-2x_2) + y \cdot (-2y_2) + (x_2^2+y_2^2+r_1^2-r_2^2) = 0$$

Như vậy, ta đã đưa bài toán ban đầu về bài toán tìm giao của đường tròn thứ nhất với một đường thẳng:

$$Ax + By + C = 0$$

$$\begin{align}
A &= -2x_2 \\
B &= -2y_2 \\
C &= x_2^2+y_2^2+r_1^2-r_2^2
\end{align}$$

Bài toán này có thể được giải như mô tả trong [bài viết tương ứng](circle-line-intersection.md).

Trường hợp suy biến duy nhất cần xét riêng là khi tâm của hai đường tròn trùng nhau. Khi đó $x_2=y_2=0$, nên $A=B=0$ và phương trình còn lại là $C=r_1^2-r_2^2=0$. Phương trình này được thỏa mãn khi và chỉ khi hai bán kính bằng nhau. Nếu chúng bằng nhau, hai đường tròn trùng nhau và có vô số giao điểm; ngược lại, chúng không có giao điểm.

## Bài tập luyện tập

- [RadarFinder](https://community.topcoder.com/stat?c=problem_statement&pm=7766)
- [Runaway to a shadow - Codeforces Round #357](http://codeforces.com/problemset/problem/681/E)
- [ASC 1 Problem F "Get out!"](http://codeforces.com/gym/100199/problem/F)
- [SPOJ: CIRCINT](http://www.spoj.com/problems/CIRCINT/)
- [UVA - 10301 - Rings and Glue](https://uva.onlinejudge.org/index.php?option=onlinejudge&page=show_problem&problem=1242)
- [Codeforces 933C A Colorful Prospect](https://codeforces.com/problemset/problem/933/C)
- [TIMUS 1429 Biscuits](https://acm.timus.ru/problem.aspx?space=1&num=1429)
