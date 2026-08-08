---
tags:
  - Translated
e_maxx_link: segment_to_line
translation:
  source: geometry/segment-to-line.md
  source_commit: b9e0917b7d479f6dbbdef83f280c30d51db86d57
  status: draft
  last_synced: 2026-08-08
---

# Tìm phương trình đường thẳng đi qua một đoạn thẳng

Bài toán đặt ra như sau: cho tọa độ hai đầu mút của một đoạn thẳng, hãy dựng một đường thẳng đi qua đoạn đó.

Ta giả sử đoạn thẳng không suy biến, tức là có độ dài lớn hơn không (nếu không thì hiển nhiên có vô số đường thẳng khác nhau đi qua điểm đó).

### Trường hợp hai chiều

Cho đoạn thẳng $PQ$, tức là ta biết tọa độ hai đầu mút $P_x , P_y , Q_x , Q_y$ .

Ta cần dựng **phương trình đường thẳng trên mặt phẳng** đi qua đoạn thẳng này, tức là tìm các hệ số $A , B , C$ trong phương trình:

$$A x + B y + C = 0.$$

Lưu ý rằng với bộ ba $(A, B, C)$ cần tìm có **vô số** nghiệm cùng mô tả một đường thẳng:
ta có thể nhân cả ba hệ số với một số khác không bất kỳ mà vẫn thu được cùng đường thẳng.
Vì vậy, nhiệm vụ của ta là tìm một trong các bộ ba đó.

Có thể dễ dàng kiểm tra (bằng cách thay các biểu thức và tọa độ của $P$, $Q$ vào phương trình đường thẳng) rằng bộ hệ số sau là phù hợp:

$$\begin{align}
A &= P_y - Q_y, \\
B &= Q_x - P_x, \\
C &= - A P_x - B P_y.
\end{align}$$

### Trường hợp tọa độ nguyên

Một ưu điểm quan trọng của cách dựng đường thẳng này là nếu tọa độ hai đầu mút là số nguyên thì các hệ số thu được cũng là **số nguyên** . Trong một số trường hợp, điều này cho phép thực hiện các phép toán hình học mà hoàn toàn không cần dùng số thực.

Tuy nhiên có một nhược điểm nhỏ: cùng một đường thẳng có thể thu được nhiều bộ ba hệ số khác nhau.
Để tránh điều này mà vẫn giữ các hệ số nguyên, ta có thể dùng kỹ thuật **chuẩn hóa** sau. Tìm [ước chung lớn nhất](../algebra/euclid-algorithm.md) của các số $| A | , | B | , | C |$ , chia cả ba hệ số cho giá trị đó, rồi chuẩn hóa dấu: nếu $A <0$ hoặc $A = 0, B <0$ thì nhân cả ba hệ số với $-1$ .
Kết quả là các đường thẳng giống nhau sẽ cho cùng một bộ ba hệ số, nhờ đó việc kiểm tra hai đường thẳng có bằng nhau hay không trở nên đơn giản.

### Trường hợp số thực

Khi làm việc với số thực, ta luôn phải lưu ý đến sai số.

Các hệ số $A$ và $B$ có cùng bậc độ lớn với tọa độ ban đầu, còn hệ số $C$ có bậc độ lớn bằng bình phương của chúng. Các giá trị này có thể đã khá lớn; chẳng hạn khi ta [tìm giao điểm hai đường thẳng](lines-intersection.md), chúng còn lớn hơn nữa, dẫn đến sai số làm tròn đáng kể ngay cả khi tọa độ các đầu mút chỉ có bậc $10^3$.

Vì vậy, khi làm việc với số thực, nên thực hiện **chuẩn hóa** để các hệ số thỏa $A ^ 2 + B ^ 2 = 1$ . Ta tính giá trị $Z$ :

$$Z = \sqrt{A ^ 2 + B ^ 2},$$

rồi chia cả ba hệ số $A , B , C$ cho nó.

Khi đó, bậc độ lớn của $A$ và $B$ không còn phụ thuộc vào bậc độ lớn của tọa độ đầu vào, còn $C$ sẽ có cùng bậc độ lớn với tọa độ đầu vào. Trong thực tế, điều này cải thiện đáng kể độ chính xác của phép tính.

Cuối cùng, xét việc **so sánh** các đường thẳng: sau khi chuẩn hóa như trên, cùng một đường thẳng chỉ còn có thể cho hai bộ ba hệ số, khác nhau bởi phép nhân với $-1$.
Do đó, nếu ta chuẩn hóa thêm về dấu (nếu $A < -\varepsilon$  hoặc $| A | < \varepsilon$, $B <- \varepsilon$ thì nhân với $-1$ ), các hệ số thu được sẽ là duy nhất.

### Trường hợp ba chiều và nhiều chiều

Ngay trong trường hợp ba chiều đã **không có một phương trình đơn giản** để mô tả đường thẳng (có thể biểu diễn nó là giao của hai mặt phẳng, tức một hệ hai phương trình, nhưng cách này không thuận tiện).

Vì vậy, trong không gian ba chiều và nhiều chiều, ta phải dùng **dạng tham số của đường thẳng**, tức biểu diễn bằng một điểm $p$ và một vectơ $v$ :

$$p + v t, ~~~ t \in \mathbb{R}.$$

Nói cách khác, đường thẳng gồm mọi điểm có thể thu được bằng cách xuất phát từ $p$ rồi cộng thêm vectơ $v$ nhân với một hệ số tùy ý.

Việc **dựng** đường thẳng ở dạng tham số từ tọa độ hai đầu mút của một đoạn thẳng rất đơn giản: lấy một đầu mút làm điểm $p$, và lấy vectơ từ đầu mút thứ nhất đến đầu mút thứ hai làm vectơ $v$.
