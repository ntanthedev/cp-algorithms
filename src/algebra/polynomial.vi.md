---
tags:
  - Original
translation:
  source: algebra/polynomial.md
  source_commit: b9baa985852a741f71026ee1e10c563f6e41111b
  status: draft
  last_synced: 2026-11-17
---

# Các phép toán trên đa thức và chuỗi

Các bài toán lập trình thi đấu, đặc biệt là những bài liên quan đến đếm, thường được giải bằng cách quy về việc tính toán trên đa thức và chuỗi lũy thừa hình thức.

Các khái niệm liên quan bao gồm phép nhân, nội suy đa thức và những phép toán phức tạp hơn như lôgarit và hàm mũ của đa thức. Bài viết này giới thiệu ngắn gọn các phép toán đó cùng những cách tiếp cận thường dùng.

## Khái niệm và tính chất cơ bản

Trong phần này, ta tập trung vào định nghĩa và các tính chất "trực quan" của một số phép toán trên đa thức. Chi tiết kỹ thuật về cài đặt và độ phức tạp sẽ được trình bày ở các phần sau.

### Phép nhân đa thức

!!! info "Định nghĩa"
	**Đa thức một biến** là biểu thức có dạng $A(x) = a_0 + a_1 x + \dots + a_n x^n$.

Các giá trị $a_0, \dots, a_n$ là hệ số của đa thức, thường được lấy từ một tập số hoặc cấu trúc tương tự số. Trong bài này, ta giả sử các hệ số thuộc một [trường](https://en.wikipedia.org/wiki/Field_(mathematics)), nghĩa là các phép cộng, trừ, nhân và chia trên chúng đều được xác định (trừ phép chia cho $0$) và nhìn chung hoạt động tương tự như với số thực.

Một ví dụ điển hình là trường các phần dư modulo số nguyên tố $p$.

Để đơn giản, ta bỏ từ _một biến_ vì đây là loại đa thức duy nhất được xét trong bài. Ta cũng viết $A$ thay cho $A(x)$ khi có thể và dựa vào ngữ cảnh để hiểu. Ta giả sử $a_n \neq 0$ hoặc $A(x)=0$.

!!! info "Định nghĩa"
	**Tích** của hai đa thức được định nghĩa bằng cách khai triển như một biểu thức số học:

	$$
	A(x) B(x) = \left(\sum\limits_{i=0}^n a_i x^i \right)\left(\sum\limits_{j=0}^m b_j x^j\right) = \sum\limits_{i,j} a_i b_j x^{i+j} = \sum\limits_{k=0}^{n+m} c_k x^k = C(x).
	$$

	Dãy hệ số $c_0, c_1, \dots, c_{n+m}$ của $C(x)$ được gọi là **tích chập** (convolution) của $a_0, \dots, a_n$ và $b_0, \dots, b_m$.

!!! info "Định nghĩa"
	**Bậc** của đa thức $A$ với $a_n \neq 0$ được định nghĩa là $\deg A = n$.

	Để thống nhất, bậc của $A(x) = 0$ được định nghĩa là $\deg A = -\infty$.

Theo quy ước này, $\deg AB = \deg A + \deg B$ với mọi đa thức $A$ và $B$.

Tích chập là cơ sở để giải nhiều bài toán đếm.

!!! Example
	Bạn có $n$ đối tượng loại thứ nhất và $m$ đối tượng loại thứ hai.

	Các đối tượng loại thứ nhất có giá trị $a_1, \dots, a_n$, còn các đối tượng loại thứ hai có giá trị $b_1, \dots, b_m$.

	Bạn chọn một đối tượng loại thứ nhất và một đối tượng loại thứ hai. Có bao nhiêu cách để tổng giá trị bằng $k$?

??? hint "Lời giải"
	Xét tích $(x^{a_1} + \dots + x^{a_n})(x^{b_1} + \dots + x^{b_m})$. Khi khai triển, mỗi đơn thức tương ứng với cặp $(a_i, b_j)$ và đóng góp vào hệ số của $x^{a_i+b_j}$. Nói cách khác, đáp án là hệ số của $x^k$ trong tích.

!!! Example
	Bạn gieo một con xúc xắc $6$ mặt $n$ lần và cộng kết quả của tất cả các lần gieo. Xác suất nhận được tổng bằng $k$ là bao nhiêu?

??? hint "Lời giải"
	Đáp án là số kết quả có tổng bằng $k$ chia cho tổng số kết quả, tức $6^n$.

	Có bao nhiêu kết quả có tổng bằng $k$? Với $n=1$, ta có thể biểu diễn bằng đa thức $A(x) = x^1+x^2+\dots+x^6$.

	Với $n=2$, áp dụng cách tương tự ví dụ trên, ta thấy số kết quả được biểu diễn bởi đa thức $(x^1+x^2+\dots+x^6)^2$.

	Do đó, đáp án của bài toán là hệ số thứ $k$ của $(x^1+x^2+\dots+x^6)^n$, chia cho $6^n$.

Hệ số của $x^k$ trong đa thức $A(x)$ được ký hiệu ngắn gọn là $[x^k]A$.

### Chuỗi lũy thừa hình thức

!!! info "Định nghĩa"
	**Chuỗi lũy thừa hình thức** là một tổng vô hạn $A(x) = a_0 + a_1 x + a_2 x^2 + \dots$, được xét mà không quan tâm đến tính hội tụ của nó.

Nói cách khác, chẳng hạn khi xét tổng $1+\frac{1}{2}+\frac{1}{4}+\frac{1}{8}+\dots=2$, ta ngầm hiểu rằng nó _hội tụ_ về $2$ khi số số hạng tiến tới vô hạn. Tuy nhiên, chuỗi hình thức chỉ được xét theo các dãy tạo nên chúng.

!!! info "Định nghĩa"
	**Tích** của hai chuỗi lũy thừa hình thức $A(x)$ và $B(x)$ cũng được định nghĩa bằng cách khai triển như một biểu thức số học:


	$$
	A(x) B(x) = \left(\sum\limits_{i=0}^\infty a_i x^i \right)\left(\sum\limits_{j=0}^\infty b_j x^j\right) = \sum\limits_{i,j} a_i b_j x^{i+j} = \sum\limits_{k=0}^{\infty} c_k x^k = C(x),
	$$

	trong đó các hệ số $c_0, c_1, \dots$ được định nghĩa bằng các tổng hữu hạn

	$$
	c_k = \sum\limits_{i=0}^k a_i b_{k-i}.
	$$

	Dãy $c_0, c_1, \dots$ cũng được gọi là **tích chập** của $a_0, a_1, \dots$ và $b_0, b_1, \dots$, qua đó mở rộng khái niệm này cho các dãy vô hạn.

Vì vậy, đa thức có thể được xem là chuỗi lũy thừa hình thức có số hệ số hữu hạn.

Chuỗi lũy thừa hình thức đóng vai trò quan trọng trong tổ hợp liệt kê, nơi chúng được nghiên cứu như [hàm sinh](https://en.wikipedia.org/wiki/Generating_function) của các dãy khác nhau. Giải thích chi tiết về hàm sinh và trực giác đằng sau chúng nằm ngoài phạm vi bài viết này; bạn đọc có thể tham khảo [tại đây](https://codeforces.com/blog/entry/103979) để tìm hiểu ý nghĩa tổ hợp của chúng.

Tuy nhiên, ta sẽ đề cập rất ngắn gọn rằng nếu $A(x)$ và $B(x)$ là hàm sinh của các dãy đếm đối tượng theo số "nguyên tử" trong chúng (ví dụ đếm cây theo số đỉnh), thì tích $A(x) B(x)$ đếm các đối tượng có thể mô tả thành cặp gồm một đối tượng loại $A$ và một đối tượng loại $B$, theo tổng số "nguyên tử" của cặp.

!!! Example
	Cho $A(x) = \sum\limits_{i=0}^\infty 2^i x^i$ đếm các gói đá, mỗi viên có một trong $2$ màu (vì vậy có $2^i$ gói kích thước $i$), và $B(x) = \sum\limits_{j=0}^{\infty} 3^j x^j$ đếm các gói đá, mỗi viên có một trong $3$ màu. Khi đó $C(x) = A(x) B(x) = \sum\limits_{k=0}^\infty c_k x^k$ đếm các đối tượng được mô tả là "hai gói đá, gói thứ nhất chỉ chứa đá loại $A$, gói thứ hai chỉ chứa đá loại $B$, tổng số viên là $k$" bằng hệ số $c_k$.

Tương tự, một số hàm khác trên chuỗi lũy thừa hình thức cũng có ý nghĩa trực quan.

### Phép chia đa thức

Tương tự số nguyên, ta có thể định nghĩa phép chia dài trên đa thức.

!!! info "Định nghĩa"

	Với hai đa thức bất kỳ $A$ và $B \neq 0$, ta có thể biểu diễn $A$ dưới dạng

	$$
	A = D \cdot B + R,~ \deg R < \deg B,
	$$

	trong đó $R$ được gọi là **phần dư** của $A$ modulo $B$ và $D$ được gọi là **thương**.

Đặt $\deg A = n$ và $\deg B = m$, cách làm trực tiếp là chia dài: nhân $B$ với đơn thức $\frac{a_n}{b_m} x^{n - m}$ rồi trừ khỏi $A$, lặp lại cho đến khi bậc của $A$ nhỏ hơn bậc của $B$. Phần còn lại của $A$ cuối cùng là phần dư, còn tổng các đa thức đã dùng để nhân $B$ trong quá trình đó tạo thành thương.

!!! info "Định nghĩa"
	Nếu $A$ và $B$ có cùng phần dư modulo $C$, ta nói chúng **đồng dư** modulo $C$, ký hiệu là

	$$
	A \equiv B \pmod{C}.
	$$

Phép chia đa thức hữu ích nhờ nhiều tính chất quan trọng:

- $A$ là bội của $B$ khi và chỉ khi $A \equiv 0 \pmod B$.

- Suy ra $A \equiv B \pmod C$ khi và chỉ khi $A-B$ là bội của $C$.

- Đặc biệt, $A \equiv B \pmod{C \cdot D}$ suy ra $A \equiv B \pmod{C}$.

- Với mọi đa thức bậc nhất $x-r$, ta có $A(x) \equiv A(r) \pmod{x-r}$.

- Suy ra $A$ là bội của $x-r$ khi và chỉ khi $A(r)=0$.

- Với modulo là $x^k$, ta có $A \equiv a_0 + a_1 x + \dots + a_{k-1} x^{k-1} \pmod{x^k}$.

Lưu ý rằng phép chia dài không thể được định nghĩa một cách phù hợp cho chuỗi lũy thừa hình thức. Thay vào đó, với mọi $A(x)$ có $a_0 \neq 0$, ta có thể định nghĩa chuỗi lũy thừa hình thức nghịch đảo $A^{-1}(x)$ sao cho $A(x) A^{-1}(x) = 1$. Kết quả này có thể được dùng để tính kết quả phép chia đa thức.

## Cài đặt cơ bản
Bạn có thể tìm cài đặt cơ bản cho đại số đa thức [tại đây](https://cp-algorithms.github.io/cp-algorithms-aux/cp-algo/math/poly.hpp).

Cài đặt hỗ trợ mọi phép toán đơn giản và một số phương thức hữu ích khác. Lớp chính là `poly<T>` dành cho các đa thức có hệ số kiểu `T`.

Các phép toán số học `+`, `-`, `*`, `%` và `/` đều được hỗ trợ, trong đó `%` và `/` tương ứng với phần dư và thương trong phép chia Euclid.

Ngoài ra còn có lớp `modular<m>` để thực hiện các phép toán số học trên phần dư modulo số nguyên tố `m`.

Các hàm hữu ích khác:

- `deriv()`: tính đạo hàm $P'(x)$ của $P(x)$.
- `integr()`: tính nguyên hàm $Q(x) = \int P(x)$ của $P(x)$ sao cho $Q(0)=0$.
- `inv(size_t n)`: tính $n$ hệ số đầu tiên của $P^{-1}(x)$ trong $O(n \log n)$.
- `log(size_t n)`: tính $n$ hệ số đầu tiên của $\ln P(x)$ trong $O(n \log n)$.
- `exp(size_t n)`: tính $n$ hệ số đầu tiên của $\exp P(x)$ trong $O(n \log n)$.
- `pow(size_t k, size_t n)`: tính $n$ hệ số đầu tiên của $P^{k}(x)$ trong $O(n \log nk)$.
- `deg()`: trả về bậc của $P(x)$.
- `lead()`: trả về hệ số của $x^{\deg P(x)}$.
- `resultant(poly<T> a, poly<T> b)`: tính kết thức của $a$ và $b$ trong $O(|a| \cdot |b|)$.
- `bpow(T x, size_t n)`: tính $x^n$.
- `bpow(T x, size_t n, T m)`: tính $x^n \pmod{m}$.
- `chirpz(T z, size_t n)`: tính $P(1), P(z), P(z^2), \dots, P(z^{n-1})$ trong $O(n \log n)$.
- `vector<T> eval(vector<T> x)`: tính $P(x_1), \dots, P(x_n)$ trong $O(n \log^2 n)$.
- `poly<T> inter(vector<T> x, vector<T> y)`: nội suy đa thức từ tập các cặp $P(x_i) = y_i$ trong $O(n \log^2 n)$.
- Còn một số hàm khác, bạn có thể tự khám phá mã nguồn!

## Các phép toán số học

### Phép nhân

Phép toán cốt lõi là phép nhân hai đa thức. Cụ thể, cho hai đa thức $A$ và $B$:

$$A = a_0 + a_1 x + \dots + a_n x^n$$

$$B = b_0 + b_1 x + \dots + b_m x^m$$

Ta cần tính đa thức $C = A \cdot B$, được định nghĩa là

$$\boxed{C = \sum\limits_{i=0}^n \sum\limits_{j=0}^m a_i b_j x^{i+j}}  = c_0 + c_1 x + \dots + c_{n+m} x^{n+m}.$$

Có thể tính tích này trong $O(n \log n)$ bằng [biến đổi Fourier nhanh](fft.md) và hầu hết các phương pháp ở đây sẽ dùng nó như một bước con.

### Chuỗi nghịch đảo

Nếu $A(0) \neq 0$, luôn tồn tại một chuỗi lũy thừa hình thức vô hạn $A^{-1}(x) = q_0+q_1 x + q_2 x^2 + \dots$ sao cho $A^{-1} A = 1$. Việc tính $k$ hệ số đầu tiên của $A^{-1}$ (tức là tính modulo $x^k$) thường hữu ích. Có hai cách chính để làm điều đó.

#### Chia để trị

Thuật toán này được đề cập trong [bài viết của Schönhage](http://algo.inria.fr/seminars/sem00-01/schoenhage.pdf) và lấy cảm hứng từ [phương pháp Graeffe](https://en.wikipedia.org/wiki/Graeffe's_method). Ta biết rằng với $B(x)=A(x)A(-x)$ thì $B(x)=B(-x)$, tức $B(x)$ là đa thức chẵn. Điều đó nghĩa là chỉ các hệ số có chỉ số chẵn mới có thể khác không và ta có thể viết $B(x)=T(x^2)$. Do đó, ta có phép biến đổi:

$$A^{-1}(x) \equiv \frac{1}{A(x)} \equiv \frac{A(-x)}{A(x)A(-x)} \equiv \frac{A(-x)}{T(x^2)} \pmod{x^k}$$

Lưu ý rằng có thể tính $T(x)$ bằng một phép nhân, sau đó ta chỉ quan tâm đến nửa đầu các hệ số của chuỗi nghịch đảo của nó. Điều này quy bài toán tính $A^{-1} \pmod{x^k}$ ban đầu về tính $T^{-1} \pmod{x^{\lceil k / 2 \rceil}}$.

Độ phức tạp của phương pháp này được ước lượng là

$$T(n) = T(n/2) + O(n \log n) = O(n \log n).$$

#### Thuật toán Sieveking–Kung

Quá trình tổng quát được mô tả ở đây gọi là nâng Hensel, vì nó xuất phát từ bổ đề Hensel. Ta sẽ trình bày chi tiết hơn ở dưới; trước mắt hãy tập trung vào lời giải cụ thể. "Nâng" ở đây có nghĩa là ta bắt đầu với xấp xỉ $B_0=q_0=a_0^{-1}$, tức $A^{-1} \pmod x$, rồi lặp lại việc nâng từ $\bmod x^a$ lên $\bmod x^{2a}$.

Cho $B_k \equiv A^{-1} \pmod{x^a}$. Xấp xỉ tiếp theo cần thỏa mãn $A B_{k+1} \equiv 1 \pmod{x^{2a}}$ và có thể được biểu diễn là $B_{k+1} = B_k + x^a C$. Từ đó suy ra phương trình

$$A(B_k + x^{a}C) \equiv 1 \pmod{x^{2a}}.$$

Đặt $A B_k \equiv 1 + x^a D \pmod{x^{2a}}$, khi đó phương trình trên suy ra

$$x^a(D+AC) \equiv 0 \pmod{x^{2a}} \implies D \equiv -AC \pmod{x^a} \implies C \equiv -B_k D \pmod{x^a}.$$

Từ đây ta thu được công thức cuối cùng:

$$x^a C \equiv -B_k x^a D  \equiv B_k(1-AB_k) \pmod{x^{2a}} \implies \boxed{B_{k+1} \equiv B_k(2-AB_k) \pmod{x^{2a}}}$$

Vậy bắt đầu từ $B_0 \equiv a_0^{-1} \pmod x$, ta sẽ tính dãy $B_k$ sao cho $AB_k \equiv 1 \pmod{x^{2^k}}$ với độ phức tạp

$$T(n) = T(n/2) + O(n \log n) = O(n \log n).$$

Thuật toán này có thể trông phức tạp hơn thuật toán đầu tiên một chút, nhưng có cơ sở lập luận vững chắc, thiết thực và có thể tổng quát hóa mạnh mẽ khi nhìn từ một góc độ khác; điều này sẽ được giải thích ở dưới.

### Phép chia Euclid

Xét hai đa thức $A(x)$ và $B(x)$ có bậc lần lượt là $n$ và $m$. Như đã nói ở trên, ta có thể viết lại $A(x)$ thành

$$A(x) = B(x) D(x) + R(x), \deg R < \deg B.$$

Cho $n \geq m$, suy ra $\deg D = n - m$ và $n-m+1$ hệ số bậc cao nhất của $A$ không ảnh hưởng đến $R$. Điều này có nghĩa là ta có thể khôi phục $D(x)$ từ $n-m+1$ hệ số bậc cao nhất của $A(x)$ và $B(x)$ nếu xem đây là một hệ phương trình.

Hệ phương trình tuyến tính này có thể được viết dưới dạng:

$$\begin{bmatrix} a_n \\ \vdots \\ a_{m+1} \\ a_{m} \end{bmatrix} = \begin{bmatrix}
b_m & \dots & 0 & 0 \\
\vdots & \ddots & \vdots & \vdots \\
\dots & \dots & b_m & 0 \\
\dots & \dots & b_{m-1} & b_m
\end{bmatrix} \begin{bmatrix}d_{n-m} \\ \vdots \\ d_1 \\ d_0\end{bmatrix}$$

Từ đó, nếu đưa vào các đa thức đảo ngược

$$A^R(x) = x^nA(x^{-1})= a_n + a_{n-1} x + \dots + a_0 x^n$$

$$B^R(x) = x^m B(x^{-1}) = b_m + b_{m-1} x + \dots + b_0 x^m$$

$$D^R(x) = x^{n-m}D(x^{-1}) = d_{n-m} + d_{n-m-1} x + \dots + d_0 x^{n-m}$$

thì hệ có thể được viết lại thành

$$A^R(x) \equiv B^R(x) D^R(x) \pmod{x^{n-m+1}}.$$

Từ đây ta có thể khôi phục duy nhất mọi hệ số của $D(x)$:

$$\boxed{D^R(x) \equiv A^R(x) (B^R(x))^{-1} \pmod{x^{n-m+1}}}$$

Sau đó, ta có thể khôi phục $R(x)$ bằng $R(x) = A(x) - B(x)D(x)$.

Lưu ý rằng ma trận trên là một [ma trận Toeplitz](https://en.wikipedia.org/wiki/Toeplitz_matrix) tam giác. Như thấy ở đây, giải hệ phương trình tuyến tính với ma trận Toeplitz bất kỳ thực chất tương đương với tính nghịch đảo đa thức. Hơn nữa, ma trận nghịch đảo của nó cũng là ma trận Toeplitz tam giác và các phần tử của nó, theo ký hiệu trên, là các hệ số của $(B^R(x))^{-1} \pmod{x^{n-m+1}}$.

## Tính các hàm của đa thức

### Phương pháp Newton

Hãy tổng quát hóa thuật toán Sieveking–Kung. Xét phương trình $F(P) = 0$, trong đó $P(x)$ là đa thức cần tìm và $F(x)$ là một hàm nhận giá trị đa thức được định nghĩa bởi

$$F(x) = \sum\limits_{i=0}^\infty \alpha_i (x-\beta)^i,$$

trong đó $\beta$ là một hằng số. Có thể chứng minh rằng nếu đưa vào một biến hình thức mới $y$, ta có thể biểu diễn $F(x)$ dưới dạng

$$F(x) = F(y) + (x-y)F'(y) + (x-y)^2 G(x,y),$$

trong đó $F'(x)$ là chuỗi lũy thừa hình thức đạo hàm, được định nghĩa bởi

$$F'(x) = \sum\limits_{i=0}^\infty (i+1)\alpha_{i+1}(x-\beta)^i,$$

và $G(x, y)$ là một chuỗi lũy thừa hình thức theo $x$ và $y$. Dùng kết quả này, ta có thể tìm nghiệm bằng phép lặp.

Cho $F(Q_k) \equiv 0 \pmod{x^{a}}$. Ta cần tìm $Q_{k+1} \equiv Q_k + x^a C \pmod{x^{2a}}$ sao cho $F(Q_{k+1}) \equiv 0 \pmod{x^{2a}}$.

Thay $x = Q_{k+1}$ và $y=Q_k$ vào công thức trên, ta được

$$F(Q_{k+1}) \equiv F(Q_k) + (Q_{k+1} - Q_k) F'(Q_k) + (Q_{k+1} - Q_k)^2 G(x, y) \pmod x^{2a}.$$

Vì $Q_{k+1} - Q_k \equiv 0 \pmod{x^a}$ nên $(Q_{k+1} - Q_k)^2 \equiv 0 \pmod{x^{2a}}$, do đó

$$0 \equiv F(Q_{k+1}) \equiv F(Q_k) + (Q_{k+1} - Q_k) F'(Q_k) \pmod{x^{2a}}.$$

Công thức cuối cho ta giá trị của $Q_{k+1}$:

$$\boxed{Q_{k+1} = Q_k - \dfrac{F(Q_k)}{F'(Q_k)} \pmod{x^{2a}}}$$

Vậy, khi biết cách tính nghịch đảo đa thức và tính $F(Q_k)$, ta có thể tìm $n$ hệ số của $P$ với độ phức tạp

$$T(n) = T(n/2) + f(n),$$

trong đó $f(n)$ là thời gian cần để tính $F(Q_k)$ và $F'(Q_k)^{-1}$, thường là $O(n \log n)$.

Quy tắc lặp trên được biết đến trong giải tích số dưới tên [phương pháp Newton](https://en.wikipedia.org/wiki/Newton%27s_method).

#### Bổ đề Hensel

Như đã nói, về mặt hình thức và tổng quát, kết quả này được gọi là [bổ đề Hensel](https://en.wikipedia.org/wiki/Hensel%27s_lemma) và có thể được dùng theo nghĩa rộng hơn khi làm việc với một dãy các vành lồng nhau. Trong trường hợp cụ thể này, ta làm việc với dãy phần dư đa thức modulo $x$, $x^2$, $x^3$, v.v.

Một ví dụ khác mà phép nâng Hensel có thể hữu ích là [số p-adic](https://en.wikipedia.org/wiki/P-adic_number), trong đó ta thực sự làm việc với dãy phần dư số nguyên modulo $p$, $p^2$, $p^3$, v.v. Chẳng hạn, phương pháp Newton có thể tìm mọi [số tự đồng cấu](https://en.wikipedia.org/wiki/Automorphic_number) (số mà bình phương của nó có các chữ số cuối chính là số đó) trong một cơ số cho trước. Bài toán này được để lại làm bài tập cho bạn đọc. Bạn có thể thử [bài này](https://acm.timus.ru/problem.aspx?space=1&num=1698) để kiểm tra lời giải với cơ số $10$.


### Lôgarit

Với hàm $\ln P(x)$, ta biết rằng:

$$
\boxed{(\ln P(x))' = \dfrac{P'(x)}{P(x)}}
$$

Do đó ta có thể tính $n$ hệ số của $\ln P(x)$ trong $O(n \log n)$.


### Chuỗi nghịch đảo

Ta có thể tìm công thức cho $A^{-1}$ bằng phương pháp Newton.
Để làm vậy, ta lấy phương trình $A=Q^{-1}$, do đó:

$$F(Q) = Q^{-1} - A$$

$$F'(Q) = -Q^{-2}$$

$$\boxed{Q_{k+1} \equiv Q_k(2-AQ_k) \pmod{x^{2^{k+1}}}}$$

### Hàm mũ

Hãy xét cách tính $e^{P(x)}=Q(x)$. Ta cần có $\ln Q = P$, do đó:

$$F(Q) = \ln Q - P$$

$$F'(Q) = Q^{-1}$$

$$\boxed{Q_{k+1} \equiv Q_k(1 + P - \ln Q_k) \pmod{x^{2^{k+1}}}}$$

### Lũy thừa bậc $k$ { data-toc-label="k-th power" }

Giờ ta cần tính $P^k(x)=Q$. Có thể thực hiện bằng công thức sau:

$$Q = \exp\left[k \ln P(x)\right]$$

Tuy nhiên, lưu ý rằng chỉ có thể tính đúng lôgarit và hàm mũ nếu tìm được một giá trị $Q_0$ ban đầu.

Để tìm giá trị này, cần tính lôgarit hoặc hàm mũ của hệ số tự do của đa thức.

Nhưng cách hợp lý duy nhất để làm điều đó là có $P(0)=1$ với $Q = \ln P$ để $Q(0)=0$, và $P(0)=0$ với $Q = e^P$ để $Q(0)=1$.

Do đó chỉ có thể dùng công thức trên nếu $P(0) = 1$. Trong trường hợp khác, nếu $P(x) = \alpha x^t T(x)$ với $T(0)=1$, ta có thể viết:

$$\boxed{P^k(x) = \alpha^kx^{kt} \exp[k \ln T(x)]}$$

Lưu ý rằng ta cũng có thể tính một căn bậc $k$ của đa thức nếu tính được $\sqrt[k]{\alpha}$, chẳng hạn khi $\alpha=1$.

## Tính giá trị và nội suy

### Biến đổi chirp-z

Trong trường hợp cần tính giá trị đa thức tại các điểm $x_r = z^{2r}$, ta có thể làm như sau:

$$A(z^{2r}) = \sum\limits_{k=0}^n a_k z^{2kr}$$

Thay $2kr = r^2+k^2-(r-k)^2$. Khi đó tổng được viết lại thành:

$$\boxed{A(z^{2r}) = z^{r^2}\sum\limits_{k=0}^n (a_k z^{k^2}) z^{-(r-k)^2}}$$

Ngoại trừ thừa số $z^{r^2}$, biểu thức này bằng tích chập của các dãy $u_k = a_k z^{k^2}$ và $v_k = z^{-k^2}$.

Lưu ý ở đây $u_k$ có chỉ số từ $0$ đến $n$, còn $v_k$ có chỉ số từ $-n$ đến $m$, trong đó $m$ là số mũ lớn nhất của $z$ mà ta cần.

Nếu cần tính giá trị đa thức tại các điểm $x_r = z^{2r+1}$, ta có thể quy về bài toán trước bằng phép biến đổi $a_k \to a_k z^k$.

Điều này cho ta thuật toán $O(n \log n)$ để tính giá trị tại các lũy thừa của $z$, nhờ đó có thể tính DFT cho kích thước không phải lũy thừa của hai.

Một nhận xét khác là $kr = \binom{k+r}{2} - \binom{k}{2} - \binom{r}{2}$. Khi đó ta có

$$\boxed{A(z^r) = z^{-\binom{r}{2}}\sum\limits_{k=0}^n \left(a_k z^{-\binom{k}{2}}\right)z^{\binom{k+r}{2}}}$$

Hệ số của $x^{n+r}$ trong tích của các đa thức $A_0(x) = \sum\limits_{k=0}^n a_{n-k}z^{-\binom{n-k}{2}}x^k$ và $A_1(x) = \sum\limits_{k\geq 0}z^{\binom{k}{2}}x^k$ bằng $z^{\binom{r}{2}}A(z^r)$. Ta có thể dùng công thức $z^{\binom{k+1}{2}}=z^{\binom{k}{2}+k}$ để tính các hệ số của $A_0(x)$ và $A_1(x)$.

### Tính giá trị tại nhiều điểm
Giả sử cần tính $A(x_1), \dots, A(x_n)$. Như đã nói, $A(x) \equiv A(x_i) \pmod{x-x_i}$. Do đó ta có thể làm như sau:

1. Tính một cây phân đoạn (Segment Tree) sao cho đoạn $[l,r)$ chứa tích $P_{l, r}(x) = (x-x_l)(x-x_{l+1})\dots(x-x_{r-1})$.
2. Bắt đầu với $l=1$ và $r=n+1$ ở nút gốc. Đặt $m=\lfloor(l+r)/2\rfloor$. Đi xuống $[l,m)$ với đa thức $A(x) \pmod{P_{l,m}(x)}$.
3. Bước này tính đệ quy $A(x_l), \dots, A(x_{m-1})$; làm tương tự cho $[m,r)$ với $A(x) \pmod{P_{m,r}(x)}$.
4. Nối kết quả của hai lời gọi đệ quy và trả về.

Toàn bộ quá trình chạy trong $O(n \log^2 n)$.

### Nội suy

Có một công thức trực tiếp của Lagrange để nội suy đa thức khi biết tập các cặp $(x_i, y_i)$:

$$\boxed{A(x) = \sum\limits_{i=1}^n y_i \prod\limits_{j \neq i}\dfrac{x-x_j}{x_i - x_j}}$$

Tính trực tiếp công thức này rất khó, nhưng ta có thể tính trong $O(n \log^2 n)$ bằng cách chia để trị:

Xét $P(x) = (x-x_1)\dots(x-x_n)$. Để biết các hệ số ở mẫu trong $A(x)$, ta cần tính các tích như:

$$
P_i = \prod\limits_{j \neq i} (x_i-x_j)
$$

Nhưng khi xét đạo hàm $P'(x)$, ta thấy $P'(x_i) = P_i$. Vì vậy có thể tính các $P_i$ bằng cách tính giá trị đa thức trong $O(n \log^2 n)$.

Giờ xét thuật toán đệ quy trên cùng cây phân đoạn như trong phép tính giá trị tại nhiều điểm. Thuật toán bắt đầu từ các lá, với giá trị $\dfrac{y_i}{P_i}$ ở mỗi lá.

Khi trở về từ đệ quy, ta gộp kết quả từ nút trái và nút phải theo $A_{l,r} = A_{l,m}P_{m,r} + P_{l,m} A_{m,r}$.

Bằng cách này, khi trở về gốc ta sẽ có chính xác $A(x)$ tại đó.
Toàn bộ quá trình cũng chạy trong $O(n \log^2 n)$.

## Ước chung lớn nhất và kết thức

Giả sử cho các đa thức $A(x) = a_0 + a_1 x + \dots + a_n x^n$ và $B(x) = b_0 + b_1 x + \dots + b_m x^m$.

Gọi $\lambda_0, \dots, \lambda_n$ là các nghiệm của $A(x)$ và $\mu_0, \dots, \mu_m$ là các nghiệm của $B(x)$, có tính đến bội của chúng.

Ta muốn biết $A(x)$ và $B(x)$ có nghiệm chung nào không. Có hai cách liên quan với nhau để làm điều đó.

### Thuật toán Euclid

Ta đã có một [bài viết](euclid-algorithm.md) về thuật toán này. Với một miền bất kỳ, có thể viết thuật toán Euclid đơn giản như sau:

```cpp
template<typename T>
T gcd(const T &a, const T &b) {
	return b == T(0) ? a : gcd(b, a % b);
}
```

Có thể chứng minh rằng với các đa thức $A(x)$ và $B(x)$, thuật toán chạy trong $O(nm)$.


### Kết thức

Hãy tính tích $A(\mu_0)\cdots A(\mu_m)$. Tích này bằng không khi và chỉ khi có $\mu_i$ là nghiệm của $A(x)$.

Để có tính đối xứng, ta cũng có thể nhân tích với $b_m^n$ và viết lại toàn bộ dưới dạng:

$$\boxed{\mathcal{R}(A, B) = b_m^n\prod\limits_{j=0}^m A(\mu_j) = b_m^n a_m^n \prod\limits_{i=0}^n \prod\limits_{j=0}^m (\mu_j - \lambda_i)= (-1)^{mn}a_n^m \prod\limits_{i=0}^n B(\lambda_i)}$$

Giá trị được định nghĩa ở trên gọi là kết thức (resultant) của hai đa thức $A(x)$ và $B(x)$. Từ định nghĩa, ta có các tính chất:

1. $\mathcal R(A, B) = (-1)^{nm} \mathcal R(B, A)$.
2. $\mathcal R(A, B)= a_n^m b_m^n$ khi $n=0$ hoặc $m=0$.
3. Nếu $b_m=1$ thì $\mathcal R(A - CB, B) = \mathcal R(A, B)$ với đa thức $C(x)$ bất kỳ và $n,m \geq 1$.
4. Từ đó suy ra $\mathcal R(A, B) = b_m^{\deg(A) - \deg(A-CB)}\mathcal R(A - CB, B)$ với $A(x)$, $B(x)$, $C(x)$ bất kỳ.

Điều đáng chú ý là kết thức của hai đa thức thực ra luôn thuộc cùng vành với các hệ số của chúng!

Các tính chất này cũng cho phép tính kết thức cùng với thuật toán Euclid, chạy trong $O(nm)$.


```cpp
template<typename T>
T resultant(poly<T> a, poly<T> b) {
	if(b.is_zero()) {
		return 0;
	} else if(b.deg() == 0) {
		return bpow(b.lead(), a.deg());
	} else {
		int pw = a.deg();
		a %= b;
		pw -= a.deg();
		base mul = bpow(b.lead(), pw) * base((b.deg() & a.deg() & 1) ? -1 : 1);
		base ans = resultant(b, a);
		return ans * mul;
	}
}
```

### Thuật toán half-GCD

Có một cách để tính ước chung lớn nhất và kết thức trong $O(n \log^2 n)$.

Thủ tục này thực hiện một phép biến đổi tuyến tính $2 \times 2$ ánh xạ cặp đa thức $a(x)$, $b(x)$ thành cặp khác $c(x), d(x)$ sao cho $\deg d(x) \leq \frac{\deg a(x)}{2}$. Nếu thực hiện cẩn thận, ta có thể tính half-GCD của bất kỳ cặp đa thức nào bằng nhiều nhất $2$ lời gọi đệ quy trên các đa thức nhỏ hơn ít nhất $2$ lần.

Chi tiết cụ thể của thuật toán khá dài dòng, nhưng bạn có thể tìm cài đặt trong thư viện, ở hàm `half_gcd`.

Sau khi cài đặt half-GCD, ta có thể áp dụng lặp lại cho các đa thức cho đến khi thu được cặp $\gcd(a, b)$ và $0$.

## Bài tập

- [CodeChef - RNG](https://www.codechef.com/problems/RNG)
- [CodeForces - Basis Change](https://codeforces.com/gym/102129/problem/D)
- [CodeForces - Permutant](https://codeforces.com/gym/102129/problem/G)
- [CodeForces - Medium Hadron Collider](https://codeforces.com/gym/102129/problem/C)
