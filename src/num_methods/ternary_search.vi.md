---
tags:
  - Translated
e_maxx_link: ternary_search
translation:
  source: num_methods/ternary_search.md
  source_commit: 7e73c7771f78b2f94ccd68068136437d6e5e0685
  status: draft
  last_synced: 2026-08-09
---

# Tìm kiếm tam phân

Cho một hàm $f(x)$ có tính unimodal trên đoạn $[l, r]$. Ở đây, hàm unimodal có một trong hai dạng sau:

1. Hàm tăng chặt trước, đạt giá trị lớn nhất (tại một điểm hoặc trên một đoạn), rồi giảm chặt.

2. Hàm giảm chặt trước, đạt giá trị nhỏ nhất, rồi tăng chặt.

Trong bài này, ta xét trường hợp thứ nhất.
Trường hợp thứ hai hoàn toàn đối xứng với trường hợp thứ nhất.

Bài toán là tìm giá trị lớn nhất của hàm $f(x)$ trên đoạn $[l, r]$.

## Thuật toán

Xét hai điểm bất kỳ $m_1$ và $m_2$ trong đoạn sao cho $l < m_1 < m_2 < r$. Ta tính giá trị hàm tại $m_1$ và $m_2$, tức là $f(m_1)$ và $f(m_2)$. Khi đó có ba trường hợp:

-   $f(m_1) < f(m_2)$

    Giá trị lớn nhất cần tìm không thể nằm ở phía trái $m_1$, tức trên đoạn $[l, m_1]$, vì hoặc cả $m_1$ và $m_2$, hoặc chỉ $m_1$, nằm trong vùng hàm đang tăng. Trong cả hai trường hợp, ta phải tiếp tục tìm giá trị lớn nhất trên đoạn $[m_1, r]$.

-   $f(m_1) > f(m_2)$

    Trường hợp này đối xứng với trường hợp trước: giá trị lớn nhất không thể nằm ở phía phải $m_2$, tức trên đoạn $[m_2, r]$, nên không gian tìm kiếm được thu hẹp còn đoạn $[l, m_2]$.

-   $f(m_1) = f(m_2)$

    Có thể thấy rằng hoặc cả hai điểm đều nằm trong vùng mà hàm đạt giá trị lớn nhất, hoặc $m_1$ nằm trong vùng hàm tăng còn $m_2$ nằm trong vùng hàm giảm (ở đây ta dùng tính tăng/giảm chặt của hàm). Vì vậy, không gian tìm kiếm được thu hẹp còn $[m_1, m_2]$. Để đơn giản hóa code, trường hợp này có thể được gộp với một trong hai trường hợp trước.

Như vậy, dựa trên việc so sánh giá trị hàm tại hai điểm bên trong, ta có thể thay đoạn hiện tại $[l, r]$ bằng một đoạn mới ngắn hơn $[l^\prime, r^\prime]$. Lặp lại quy trình này, ta có thể làm đoạn tìm kiếm ngắn tùy ý. Cuối cùng, độ dài đoạn sẽ nhỏ hơn một hằng số độ chính xác được chọn trước và ta có thể dừng. Đây là một phương pháp số, nên sau đó ta có thể coi hàm đạt giá trị lớn nhất tại mọi điểm của đoạn cuối cùng $[l, r]$. Không mất tính tổng quát, ta có thể lấy $f(l)$ làm giá trị trả về.

Ta chưa đặt bất kỳ ràng buộc nào lên cách chọn $m_1$ và $m_2$. Cách chọn này quyết định tốc độ hội tụ và độ chính xác của cài đặt. Cách phổ biến nhất là chọn hai điểm sao cho chúng chia đoạn $[l, r]$ thành ba phần bằng nhau. Khi đó:

$$m_1 = l + \frac{(r - l)}{3}$$

$$m_2 = r - \frac{(r - l)}{3}$$ 

Nếu chọn $m_1$ và $m_2$ gần nhau hơn, tốc độ hội tụ sẽ tăng nhẹ.

### Phân tích thời gian chạy

$$T(n) = T({2n}/{3}) + O(1) = \Theta(\log n)$$

Có thể hình dung như sau: sau mỗi lần tính giá trị hàm tại $m_1$ và $m_2$, ta thực chất loại bỏ khoảng một phần ba đoạn, ở bên trái hoặc bên phải. Vì vậy kích thước không gian tìm kiếm còn ${2n}/{3}$ so với ban đầu.

Áp dụng [Định lý Master](https://en.wikipedia.org/wiki/Master_theorem_(analysis_of_algorithms)), ta thu được ước lượng độ phức tạp trên.

### Trường hợp đối số nguyên

Nếu $f(x)$ nhận đối số nguyên, đoạn $[l, r]$ trở thành rời rạc. Vì ta không đặt ràng buộc nào lên cách chọn $m_1$ và $m_2$, tính đúng đắn của thuật toán không thay đổi. Ta vẫn có thể chọn $m_1$ và $m_2$ để chia $[l, r]$ thành ba phần xấp xỉ bằng nhau.

Điểm khác biệt nằm ở điều kiện dừng. Tìm kiếm tam phân phải dừng khi $(r - l) < 3$, vì lúc đó ta không còn bảo đảm chọn được $m_1$ và $m_2$ khác nhau, đồng thời khác $l$ và $r$; nếu tiếp tục có thể dẫn tới vòng lặp vô hạn. Khi $(r - l) < 3$, cần kiểm tra trực tiếp các điểm ứng viên còn lại $(l, l + 1, \ldots, r)$ để tìm điểm cho giá trị $f(x)$ lớn nhất.

### Tìm kiếm theo tỉ lệ vàng

Trong một số bài toán, việc tính $f(x)$ có thể khá chậm, trong khi không thể giảm số vòng lặp vì yêu cầu độ chính xác. May mắn là ta có thể chỉ cần tính $f(x)$ một lần ở mỗi vòng lặp (trừ vòng đầu tiên).

Để thấy cách làm, xét lại cách chọn $m_1$ và $m_2$. Giả sử ta chọn $m_1$ và $m_2$ trên $[l, r]$ sao cho $\frac{r - l}{r - m_1} = \frac{r - l}{m_2 - l} = \varphi$, trong đó $\varphi$ là một hằng số. Để giảm số lần tính hàm, ta muốn chọn $\varphi$ sao cho ở vòng lặp tiếp theo, một trong hai điểm đánh giá mới $m_1'$, $m_2'$ trùng với $m_1$ hoặc $m_2$, nhờ đó có thể tái sử dụng giá trị hàm đã tính.

Giả sử sau vòng lặp hiện tại ta đặt $l = m_1$. Khi đó điểm $m_1'$ thỏa $\frac{r - m_1}{r - m_1'} = \varphi$. Ta muốn điểm này trùng với $m_2$, tức là $\frac{r - m_1}{r - m_2} = \varphi$.

Nhân hai vế của $\frac{r - m_1}{r - m_2} = \varphi$ với $\frac{r - m_2}{r - l}$, ta được $\frac{r - m_1}{r - l} = \varphi\frac{r - m_2}{r - l}$. Chú ý rằng $\frac{r - m_1}{r - l} = \frac{1}{\varphi}$ và $\frac{r - m_2}{r - l} = \frac{r - l + l - m_2}{r - l} = 1 - \frac{1}{\varphi}$. Thay vào và nhân với $\varphi$, ta thu được phương trình:

$\varphi^2 - \varphi - 1 = 0$

Đây là phương trình tỉ lệ vàng quen thuộc. Giải phương trình cho $\frac{1 \pm \sqrt{5}}{2}$. Vì $\varphi$ phải dương, ta có $\varphi = \frac{1 + \sqrt{5}}{2}$. Áp dụng lập luận tương tự cho trường hợp đặt $r = m_2$ và muốn $m_2'$ trùng với $m_1$, ta cũng thu được cùng giá trị $\varphi$. Vì vậy, nếu chọn $m_1 = l + \frac{r - l}{1 + \varphi}$ và $m_2 = r - \frac{r - l}{1 + \varphi}$, ở mỗi vòng lặp ta có thể tái sử dụng một trong các giá trị $f(x)$ đã tính ở vòng trước.

## Cài đặt

```cpp
double ternary_search(double l, double r) {
	double eps = 1e-9;				//set the error limit here
	while (r - l > eps) {
		double m1 = l + (r - l) / 3;
		double m2 = r - (r - l) / 3;
		double f1 = f(m1);		//evaluates the function at m1
		double f2 = f(m2);		//evaluates the function at m2
		if (f1 < f2)
			l = m1;
		else
			r = m2;
	}
	return f(l);					//return the maximum of f(x) in [l, r]
}
```

Ở đây `eps` thực chất là sai số tuyệt đối (chưa tính đến sai số do việc tính giá trị hàm không chính xác).

Thay vì dùng điều kiện `r - l > eps`, ta có thể chọn một số vòng lặp cố định làm điều kiện dừng. Số vòng lặp cần đủ lớn để bảo đảm độ chính xác yêu cầu. Thông thường, trong các bài lập trình có giới hạn sai số ${10}^{-6}$, khoảng 200 - 300 vòng lặp là đủ. Ngoài ra, số vòng lặp không phụ thuộc trực tiếp vào giá trị của $l$ và $r$, nên theo cách diễn đạt của nguồn, số vòng lặp tương ứng với sai số tương đối cần đạt.

**Ghi chú bản dịch:** Cách nói “sai số tương đối” ở câu trên dễ gây hiểu nhầm. Số vòng lặp cố định quyết định tỉ lệ co của độ dài đoạn tìm kiếm so với đoạn ban đầu; sai số tuyệt đối cuối cùng vẫn phụ thuộc vào độ dài đoạn ban đầu, và điều đó không tự động đồng nghĩa với sai số tương đối của nghiệm.

## Bài tập luyện tập

- [Codeforces - New Bakery](https://codeforces.com/problemset/problem/1978/B)
- [Codechef - Race time](https://www.codechef.com/problems/AMCS03)
- [Hackerearth - Rescuer](https://www.hackerearth.com/problem/algorithm/rescuer-2d2495cb/)
- [Spoj - Building Construction](http://www.spoj.com/problems/KOPC12A/)
- [Codeforces - Weakness and Poorness](http://codeforces.com/problemset/problem/578/C)
* [LOJ - Closest Distance](http://lightoj.com/volume_showproblem.php?problem=1146)
* [GYM - Dome of Circus (D)](http://codeforces.com/gym/101309)
* [UVA - Galactic Taxes](https://uva.onlinejudge.org/index.php?option=com_onlinejudge&Itemid=8&page=show_problem&problem=4898)
* [GYM - Chasing the Cheetahs (A)](http://codeforces.com/gym/100829)
* [UVA - 12197 - Trick or Treat](https://uva.onlinejudge.org/index.php?option=com_onlinejudge&Itemid=8&page=show_problem&problem=3349)
* [SPOJ - Building Construction](http://www.spoj.com/problems/KOPC12A/)
* [Codeforces - Devu and his Brother](https://codeforces.com/problemset/problem/439/D)
* [Codechef - Is This JEE ](https://www.codechef.com/problems/ICM2003)
* [Codeforces - Restorer Distance](https://codeforces.com/contest/1355/problem/E)
* [TIMUS 1058 Chocolate](https://acm.timus.ru/problem.aspx?space=1&num=1058)
* [TIMUS 1436 Billboard](https://acm.timus.ru/problem.aspx?space=1&num=1436)
* [TIMUS 1451 Beerhouse Tale](https://acm.timus.ru/problem.aspx?space=1&num=1451)
* [TIMUS 1719 Kill the Shaitan-Boss](https://acm.timus.ru/problem.aspx?space=1&num=1719)
* [TIMUS 1913 Titan Ruins: Alignment of Forces](https://acm.timus.ru/problem.aspx?space=1&num=1913)
