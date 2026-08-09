---
tags:
  - Translated
e_maxx_link: diofant_1_equation
translation:
  source: algebra/linear_congruence_equation.md
  source_commit: c663f523fc09b4defdc1e3af825b43c3b42f07e2
  status: draft
  last_synced: 2026-08-09
---

# Phương trình đồng dư tuyến tính

Phương trình có dạng:

$$a \cdot x \equiv b \pmod n,$$

trong đó $a$, $b$ và $n$ là các số nguyên đã biết, còn $x$ là số nguyên cần tìm.

Ta cần tìm giá trị $x$ trong đoạn $[0, n-1]$ (rõ ràng, trên toàn bộ tập số nguyên có thể có vô hạn nghiệm; các nghiệm sai khác nhau một bội của mô-đun, cụ thể là $n \cdot k$ , với $k$ là một số nguyên bất kỳ). Nếu nghiệm không duy nhất, ta cũng sẽ xét cách tìm tất cả các nghiệm.

## Giải bằng cách tìm nghịch đảo mô-đun

Trước hết, xét trường hợp đơn giản hơn khi $a$ và $n$ **nguyên tố cùng nhau** ($\gcd(a, n) = 1$).
Khi đó, ta có thể tìm [nghịch đảo mô-đun](module-inverse.md) của $a$. Nhân cả hai vế của phương trình với nghịch đảo này, ta thu được một nghiệm **duy nhất**.

$$x \equiv b \cdot a ^ {- 1} \pmod n$$

Bây giờ xét trường hợp $a$ và $n$ **không nguyên tố cùng nhau** ($\gcd(a, n) \ne 1$).
Khi đó, nghiệm không phải lúc nào cũng tồn tại (chẳng hạn $2 \cdot x \equiv 1 \pmod 4$ không có nghiệm).

Đặt $g = \gcd(a, n)$, tức [ước chung lớn nhất](euclid-algorithm.md) của $a$ và $n$ (trong trường hợp này lớn hơn một).

Nếu $b$ không chia hết cho $g$ thì phương trình vô nghiệm. Thật vậy, với mọi $x$, vế trái $a \cdot x \pmod n$ luôn chia hết cho $g$, trong khi vế phải thì không; do đó không thể có nghiệm.

Nếu $g$ là ước của $b$, ta chia cả hai vế của phương trình cho $g$ (tức chia $a$, $b$ và $n$ cho $g$) và thu được phương trình mới:

$$a^\prime \cdot x \equiv b^\prime \pmod{n^\prime}$$

trong đó $a^\prime$ và $n^\prime$ đã nguyên tố cùng nhau, nên ta có thể giải bằng cách ở trên.
Gọi $x^\prime$ là nghiệm tìm được cho $x$.

Rõ ràng $x^\prime$ cũng là một nghiệm của phương trình ban đầu.
Tuy nhiên, đó **không phải nghiệm duy nhất**.
Có thể chứng minh rằng phương trình ban đầu có đúng $g$ nghiệm, có dạng:

$$x_i \equiv (x^\prime + i\cdot n^\prime) \pmod n \quad \text{for } i = 0 \ldots g-1$$

Tóm lại, **số nghiệm** của phương trình đồng dư tuyến tính hoặc bằng $g = \gcd(a, n)$, hoặc bằng không.

## Giải bằng thuật toán Euclid mở rộng

Ta có thể biến đổi phương trình đồng dư tuyến tính thành phương trình Diophantine sau:

$$a \cdot x + n \cdot k = b,$$

trong đó $x$ và $k$ là các số nguyên chưa biết.

Cách giải phương trình này được trình bày trong bài [Phương trình Diophantine tuyến tính](linear-diophantine-equation.md), dựa trên [thuật toán Euclid mở rộng](extended-euclid-algorithm.md).

Bài đó cũng mô tả cách suy ra toàn bộ nghiệm từ một nghiệm đã biết; nếu xét kỹ, phương pháp này hoàn toàn tương đương với cách ở phần trước.
