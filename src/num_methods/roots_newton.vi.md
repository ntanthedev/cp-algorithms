---
tags:
  - Translated
e_maxx_link: roots_newton
translation:
  source: num_methods/roots_newton.md
  source_commit: 225d2555f2d5f9a5c54cdf08f4d9efd0f4e56ec1
  status: draft
  last_synced: 2026-08-09
---

# Phương pháp Newton để tìm nghiệm

Đây là một phương pháp lặp do Isaac Newton phát minh vào khoảng năm 1664. Tuy nhiên, phương pháp này đôi khi cũng được gọi là phương pháp Raphson, vì Raphson tìm ra cùng thuật toán vài năm sau Newton nhưng bài viết của ông lại được công bố sớm hơn nhiều.

Bài toán như sau. Cho phương trình:

$$f(x) = 0$$

Ta muốn giải phương trình này. Cụ thể hơn, ta muốn tìm một trong các nghiệm của nó (giả sử nghiệm tồn tại). Giả sử $f(x)$ liên tục và khả vi trên một đoạn $[a, b]$.

## Thuật toán

Đầu vào của thuật toán không chỉ gồm hàm $f(x)$ mà còn có một xấp xỉ ban đầu $x_0$, là điểm mà thuật toán bắt đầu.

<p align="center">
	<img src="./roots_newton.png" alt="plot_f(x)">
</p>

Giả sử ta đã tính được $x_i$. Ta tính $x_{i+1}$ như sau: kẻ tiếp tuyến với đồ thị hàm $f(x)$ tại điểm $x = x_i$, rồi tìm giao điểm của tiếp tuyến này với trục $x$. Đặt $x_{i+1}$ bằng hoành độ của giao điểm vừa tìm được, sau đó lặp lại toàn bộ quá trình.

Không khó để thu được công thức:

$$ x_{i+1} = x_i - \frac{f(x_i)}{f^\prime(x_i)} $$

Trước hết, ta tính hệ số góc $f'(x)$, tức đạo hàm của $f(x)$, rồi xác định phương trình tiếp tuyến:

$$ y - f(x_i) = f'(x_i)(x - x_i) $$ 

Tiếp tuyến cắt trục x tại tọa độ $y = 0$ và $x = x_{i+1}$:

$$ - f(x_i) = f'(x_i)(x_{i+1} - x_i) $$ 

Giải phương trình này, ta thu được giá trị của $x_{i+1}$.

Về trực giác, nếu hàm $f(x)$ đủ "tốt" (trơn) và $x_i$ đủ gần nghiệm thì $x_{i+1}$ sẽ còn gần nghiệm cần tìm hơn.

Tốc độ hội tụ là bậc hai; nói một cách gần đúng, số chữ số chính xác trong giá trị xấp xỉ $x_i$ sẽ tăng gấp đôi sau mỗi vòng lặp.

## Ứng dụng để tính căn bậc hai

Ta dùng bài toán tính căn bậc hai làm ví dụ cho phương pháp Newton.

Nếu thay $f(x) = x^2 - n$, sau khi rút gọn ta được:

$$ x_{i+1} = \frac{x_i + \frac{n}{x_i}}{2} $$

Biến thể thường gặp đầu tiên là cho một số hữu tỉ $n$ và cần tính căn của nó với độ chính xác `eps`:

```cpp
double sqrt_newton(double n) {
	const double eps = 1E-15;
	double x = 1;
	for (;;) {
		double nx = (x + n / x) / 2;
		if (abs(x - nx) < eps)
			break;
		x = nx;
	}
	return x;
}
```

Một biến thể phổ biến khác là cần tính căn nguyên: với $n$ cho trước, tìm $x$ lớn nhất sao cho $x^2 \le n$. Ở đây cần thay đổi nhẹ điều kiện dừng vì có thể xảy ra trường hợp $x$ bắt đầu "nhảy" quanh đáp án. Vì vậy, ta thêm điều kiện: nếu ở bước trước giá trị $x$ đã giảm, còn ở bước hiện tại nó lại có xu hướng tăng, thì thuật toán phải dừng.

```cpp
int isqrt_newton(int n) {
	int x = 1;
	bool decreased = false;
	for (;;) {
		int nx = (x + n / x) >> 1;
		if (x == nx || nx > x && decreased)
			break;
		decreased = nx < x;
		x = nx;
	}
	return x;
}
```

Cuối cùng là biến thể thứ ba dành cho số nguyên lớn. Vì $n$ có thể rất lớn, ta nên chú ý đến xấp xỉ ban đầu. Hiển nhiên, xấp xỉ càng gần căn thật thì càng nhanh thu được kết quả. Một lựa chọn đơn giản và hiệu quả là lấy xấp xỉ ban đầu bằng $2^{\textrm{bits}/2}$, trong đó $\textrm{bits}$ là số bit của $n$. Đoạn code Java sau minh họa biến thể này:

```java
public static BigInteger isqrtNewton(BigInteger n) {
	BigInteger a = BigInteger.ONE.shiftLeft(n.bitLength() / 2);
	boolean p_dec = false;
	for (;;) {
		BigInteger b = n.divide(a).add(a).shiftRight(1);
		if (a.compareTo(b) == 0 || a.compareTo(b) < 0 && p_dec)
			break;
		p_dec = a.compareTo(b) > 0;
		a = b;
	}
	return a;
}
```

**Ghi chú bản dịch:** Hai cài đặt căn bậc hai nguyên ở trên không xử lý riêng trường hợp đầu vào bằng 0. Với trường hợp đó, biến lặp có thể trở thành 0 rồi phép chia ở vòng lặp kế tiếp không còn hợp lệ. Bản dịch giữ nguyên code nguồn; correction được tách sang PR upstream.

Ví dụ, đoạn code này chạy trong $60$ mili giây với $n = 10^{1000}$; nếu bỏ cách chọn xấp xỉ ban đầu cải tiến và chỉ bắt đầu từ $1$, thời gian chạy sẽ vào khoảng $120$ mili giây.

## Bài tập luyện tập
- [UVa 10428 - The Roots](https://uva.onlinejudge.org/index.php?option=com_onlinejudge&Itemid=8&category=16&page=show_problem&problem=1369)
