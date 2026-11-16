---
tags:
  - Translated
e_maxx_link: linear_systems_gauss
translation:
  source: linear_algebra/linear-system-gauss.md
  source_commit: cefbc1e3053da8bdf0260c4ef19e5d88df5ea64e
  status: draft
  last_synced: 2026-11-16
---

# Phương pháp Gauss giải hệ phương trình tuyến tính

Cho một hệ gồm $n$ phương trình đại số tuyến tính (SLAE) với $m$ ẩn số. Hãy giải hệ: xác định hệ vô nghiệm, có đúng một nghiệm hay có vô số nghiệm. Nếu hệ có ít nhất một nghiệm, hãy tìm một nghiệm bất kỳ.

Phát biểu hình thức của bài toán là giải hệ:

$$\begin{align}
a_{11} x_1 + a_{12} x_2 + &\dots + a_{1m} x_m = b_1 \\
a_{21} x_1 + a_{22} x_2 + &\dots + a_{2m} x_m = b_2\\
&\vdots \\
a_{n1} x_1 + a_{n2} x_2 + &\dots + a_{nm} x_m = b_n
\end{align}$$

trong đó các hệ số $a_{ij}$ (với $i$ từ 1 đến $n$, $j$ từ 1 đến $m$) và $b_i$ ($i$ từ 1 đến $n$) đã biết, còn các biến $x_i$ ($i$ từ 1 đến $m$) là các ẩn số.

Bài toán này cũng có biểu diễn ma trận đơn giản:

$$Ax = b,$$

trong đó $A$ là ma trận kích thước $n \times m$ gồm các hệ số $a_{ij}$ và $b$ là vector cột có kích thước $n$.

Phương pháp trong bài cũng có thể dùng để giải phương trình theo modulo một số p bất kỳ, tức là:

$$\begin{align}
a_{11} x_1 + a_{12} x_2 + &\dots + a_{1m} x_m \equiv b_1 \pmod p \\
a_{21} x_1 + a_{22} x_2 + &\dots + a_{2m} x_m \equiv b_2 \pmod p \\
&\vdots \\
a_{n1} x_1 + a_{n2} x_2 + &\dots + a_{nm} x_m \equiv b_n \pmod p
\end{align}$$

> **Ghi chú bản dịch:** Khẳng định về modulo bất kỳ trong bài gốc cần thận trọng: với modulo hợp số, một phần tử khác không chưa chắc có nghịch đảo, nên không thể luôn thực hiện phép chia dùng trong thuật toán dưới đây.

## Gauss

Nói chính xác, phương pháp dưới đây nên được gọi là phép khử "Gauss-Jordan", vì đây là một biến thể của phương pháp Gauss được Jordan mô tả năm 1887.

## Tổng quan

Thuật toán `sequential elimination` (loại bỏ tuần tự) các biến trong mỗi phương trình cho đến khi mỗi phương trình chỉ còn một biến. Nếu $n = m$, có thể hình dung việc này là biến đổi ma trận $A$ thành ma trận đơn vị và giải hệ trong trường hợp hiển nhiên đó, khi nghiệm duy nhất bằng hệ số $b_i$.

Phép khử Gauss dựa trên hai phép biến đổi đơn giản:

* Có thể đổi chỗ hai phương trình.
* Có thể thay một phương trình bằng tổ hợp tuyến tính của hàng đó (với hệ số khác không) và một số hàng khác (với hệ số tùy ý).

Ở bước đầu, thuật toán Gauss-Jordan chia hàng đầu tiên cho $a_{11}$. Sau đó thuật toán cộng hàng đầu tiên vào các hàng còn lại sao cho các hệ số ở cột đầu tiên đều bằng không. Để làm điều này, ở hàng thứ i ta phải cộng hàng đầu tiên nhân với $- a_{i1}$. Lưu ý thao tác này cũng phải thực hiện với vector $b$. Theo một nghĩa nào đó, vector $b$ hoạt động như cột thứ $m+1$ của ma trận $A$.

Kết quả là sau bước đầu, cột đầu của ma trận $A$ gồm $1$ ở hàng đầu và $0$ ở các hàng khác.

Tương tự, ta thực hiện bước thứ hai khi xét cột thứ hai của hàng thứ hai. Đầu tiên chia hàng cho $a_{22}$, rồi trừ nó khỏi các hàng khác để toàn bộ cột thứ hai bằng $0$ (trừ hàng thứ hai).

Ta tiếp tục với mọi cột của ma trận $A$. Nếu $n = m$, $A$ sẽ trở thành ma trận đơn vị.

## Tìm phần tử trụ

Mô tả trên bỏ qua nhiều chi tiết. Ở bước thứ $i$, nếu $a_{ii}$ bằng không, ta không thể áp dụng trực tiếp phương pháp đã mô tả. Thay vào đó, trước tiên phải `select a pivoting row` (chọn hàng trụ): tìm một hàng của ma trận có cột thứ $i$ khác không, rồi đổi chỗ hai hàng.

Ở đây ta đổi hàng chứ không đổi cột. Bởi nếu đổi cột, khi tìm được nghiệm ta phải nhớ đổi lại về đúng vị trí. Vì vậy đổi hàng dễ hơn nhiều.

Trong nhiều cài đặt, ngay cả khi $a_{ii} \neq 0$, người ta vẫn đổi hàng thứ $i$ với một hàng trụ theo heuristic nào đó, chẳng hạn chọn hàng trụ có giá trị tuyệt đối của $a_{ji}$ lớn nhất. Heuristic này được dùng để giảm phạm vi giá trị của ma trận trong các bước sau. Không có heuristic này, ngay cả với ma trận cỡ khoảng $20$, sai số sẽ quá lớn và có thể gây tràn kiểu dữ liệu dấu phẩy động trong C++.

## Trường hợp suy biến

Khi $m = n$ và hệ không suy biến (tức định thức khác không và hệ có nghiệm duy nhất), thuật toán trên sẽ biến đổi $A$ thành ma trận đơn vị.

Bây giờ xét `general case` (trường hợp tổng quát), trong đó $n$ và $m$ không nhất thiết bằng nhau và hệ có thể suy biến. Trong các trường hợp này, có thể không tìm thấy phần tử trụ ở bước thứ $i$. Điều đó nghĩa là tại cột thứ $i$, từ hàng hiện tại trở đi, mọi phần tử đều bằng không. Khi đó hoặc không có giá trị nào có thể gán cho biến $x_i$ (nghĩa là SLAE vô nghiệm), hoặc $x_i$ là biến độc lập và có thể nhận giá trị tùy ý. Khi cài đặt Gauss-Jordan, nên tiếp tục xử lý các biến sau và bỏ qua cột thứ $i$ (tương đương loại cột thứ $i$ của ma trận).

Do đó, một số biến có thể được xác định là độc lập trong quá trình xử lý. Khi số biến $m$ lớn hơn số phương trình $n$, ta sẽ tìm thấy ít nhất $m - n$ biến độc lập.

Nói chung, nếu tìm được ít nhất một biến độc lập thì nó có thể nhận giá trị tùy ý, còn các biến khác (phụ thuộc) được biểu diễn theo nó. Điều này nghĩa là khi làm việc trên trường số thực, hệ có khả năng có vô số nghiệm. Nhưng cần nhớ rằng ngay cả khi có biến độc lập, SLAE vẫn có thể vô nghiệm. Điều này xảy ra khi các phương trình chưa xử lý còn lại có ít nhất một số hạng hằng khác không. Có thể kiểm tra bằng cách gán không cho mọi biến độc lập, tính các biến khác rồi thay vào SLAE ban đầu xem chúng có thỏa mãn hệ không.

## Cài đặt

Dưới đây là cài đặt Gauss-Jordan. Hàng trụ được chọn theo heuristic lấy giá trị lớn nhất trong cột hiện tại.

Đầu vào của hàm `gauss` là ma trận hệ $a$. Cột cuối của ma trận này là vector $b$.

Hàm trả về số nghiệm của hệ $(0, 1,\textrm{or } \infty)$. Nếu có ít nhất một nghiệm thì nghiệm được trả về trong vector $ans$.

```{.cpp file=gauss}
const double EPS = 1e-9;
const int INF = 2; // it doesn't actually have to be infinity or a big number

int gauss (vector < vector<double> > a, vector<double> & ans) {
	int n = (int) a.size();
	int m = (int) a[0].size() - 1;

	vector<int> where (m, -1);
	for (int col=0, row=0; col<m && row<n; ++col) {
		int sel = row;
		for (int i=row; i<n; ++i)
			if (abs (a[i][col]) > abs (a[sel][col]))
				sel = i;
		if (abs (a[sel][col]) < EPS)
			continue;
		for (int i=col; i<=m; ++i)
			swap (a[sel][i], a[row][i]);
		where[col] = row;

		for (int i=0; i<n; ++i)
			if (i != row) {
				double c = a[i][col] / a[row][col];
				for (int j=col; j<=m; ++j)
					a[i][j] -= a[row][j] * c;
			}
		++row;
	}

	ans.assign (m, 0);
	for (int i=0; i<m; ++i)
		if (where[i] != -1)
			ans[i] = a[where[i]][m] / a[where[i]][i];
	for (int i=0; i<n; ++i) {
		double sum = 0;
		for (int j=0; j<m; ++j)
			sum += ans[j] * a[i][j];
		if (abs (sum - a[i][m]) > EPS)
			return 0;
	}

	for (int i=0; i<m; ++i)
		if (where[i] == -1)
			return INF;
	return 1;
}
```

Ghi chú cài đặt:

* Hàm dùng hai con trỏ: cột hiện tại $col$ và hàng hiện tại $row$.
* Với mỗi biến $x_i$, giá trị $where(i)$ là hàng mà cột này khác không. Cần vector này vì một số biến có thể độc lập.
* Trong cài đặt này, hàng thứ $i$ hiện tại không được chia cho $a_{ii}$ như mô tả ở trên nên cuối cùng ma trận không phải ma trận đơn vị (dù việc chia hàng thứ $i$ có thể giúp giảm sai số).
* Sau khi tìm một nghiệm, ta thay nó trở lại ma trận để kiểm tra hệ có ít nhất một nghiệm hay không. Nếu nghiệm thử thành công, hàm trả về 1 hoặc $\inf$, tùy theo có ít nhất một biến độc lập hay không.

## Độ phức tạp

Bây giờ ta ước lượng độ phức tạp của thuật toán. Thuật toán gồm $m$ pha, trong mỗi pha:

* Tìm và đổi chỗ hàng trụ. Việc này mất $O(n + m)$ khi dùng heuristic nêu trên.
* Nếu tìm được phần tử trụ ở cột hiện tại, ta phải cộng phương trình này vào mọi phương trình khác, mất thời gian $O(nm)$.

Vậy độ phức tạp cuối cùng là $O(\min (n, m) . nm)$. Khi $n = m$, độ phức tạp đơn giản là $O(n^3)$.

Lưu ý khi SLAE không nằm trên số thực mà theo modulo hai, ta có thể giải hệ nhanh hơn nhiều như mô tả dưới đây.

## Tăng tốc thuật toán

Có thể tăng tốc cài đặt trước lên hai lần bằng cách chia thuật toán thành hai pha: xuôi và ngược:

* Pha xuôi: tương tự cài đặt trước, nhưng chỉ cộng hàng hiện tại vào các hàng sau nó. Kết quả là ta thu được ma trận tam giác thay vì ma trận đường chéo.
* Pha ngược: khi ma trận đã là tam giác, trước tiên tính giá trị của biến cuối. Sau đó thay giá trị này để tìm biến tiếp theo. Rồi thay hai giá trị đó để tìm các biến tiếp theo...

Pha ngược chỉ mất $O(nm)$, nhanh hơn nhiều so với pha xuôi. Ở pha xuôi, ta giảm một nửa số phép tính, do đó giảm thời gian chạy của cài đặt.

## Giải SLAE theo modulo

Để giải SLAE theo một modulo, ta vẫn có thể dùng thuật toán đã mô tả. Tuy nhiên, khi modulo bằng 2, ta có thể thực hiện khử Gauss-Jordan hiệu quả hơn nhiều bằng các phép toán bit và kiểu dữ liệu bitset của C++:

```cpp
int gauss (vector < bitset<N> > a, int n, int m, bitset<N> & ans) {
	vector<int> where (m, -1);
	for (int col=0, row=0; col<m && row<n; ++col) {
		for (int i=row; i<n; ++i)
			if (a[i][col]) {
				swap (a[i], a[row]);
				break;
			}
		if (! a[row][col])
			continue;
		where[col] = row;

		for (int i=0; i<n; ++i)
			if (i != row && a[i][col])
				a[i] ^= a[row];
		++row;
	}
        // The rest of implementation is the same as above
}
```

Nhờ nén bit, cài đặt không chỉ ngắn hơn mà còn nhanh hơn 32 lần.

## Một ghi chú về các heuristic chọn hàng trụ

Không có quy tắc chung về heuristic nên sử dụng.

Heuristic được dùng trong cài đặt trước hoạt động khá tốt trong thực tế. Hóa ra nó cũng cho kết quả gần giống "chọn trụ toàn phần", trong đó hàng trụ được tìm giữa mọi phần tử của ma trận con (tính từ hàng hiện tại và cột hiện tại).

Tuy vậy, cần lưu ý cả hai heuristic đều phụ thuộc vào hệ số co giãn của các phương trình ban đầu. Ví dụ, nếu một phương trình được nhân với $10^6$, gần như chắc chắn phương trình này sẽ được chọn làm trụ ở bước đầu. Điều này có vẻ lạ, do đó có thể hợp lý hơn khi dùng heuristic phức tạp hơn gọi là `implicit pivoting`.

Chọn trụ ngầm so sánh các phần tử như thể cả hai hàng đã được chuẩn hóa để phần tử lớn nhất bằng một. Để cài đặt kỹ thuật này, cần lưu giá trị lớn nhất của mỗi hàng (hoặc duy trì mỗi hàng sao cho giá trị lớn nhất bằng một, nhưng điều này có thể làm tăng sai số tích lũy).

## Cải thiện nghiệm

Dù có nhiều heuristic, thuật toán Gauss-Jordan vẫn có thể dẫn đến sai số lớn đối với các ma trận đặc biệt ngay cả ở kích thước $50 - 100$.

Vì vậy đôi khi cần cải thiện nghiệm Gauss-Jordan thu được bằng một phương pháp số đơn giản, ví dụ phương pháp lặp đơn.

Như vậy lời giải có hai bước: trước tiên áp dụng thuật toán Gauss-Jordan, sau đó áp dụng một phương pháp số lấy nghiệm của bước đầu làm nghiệm khởi tạo.

## Bài tập luyện tập
* [Spoj - Xor Maximization](http://www.spoj.com/problems/XMAX/)
* [Codechef - Knight Moving](https://www.codechef.com/SEP12/problems/KNGHTMOV)
* [Lightoj - Graph Coloring](http://lightoj.com/volume_showproblem.php?problem=1279)
* [UVA 12910 - Snakes and Ladders](https://uva.onlinejudge.org/index.php?option=com_onlinejudge&Itemid=8&page=show_problem&problem=4775)
* [TIMUS1042 Central Heating](http://acm.timus.ru/problem.aspx?space=1&num=1042)
* [TIMUS1766 Humpty Dumpty](http://acm.timus.ru/problem.aspx?space=1&num=1766)
* [TIMUS1266 Kirchhoff's Law](http://acm.timus.ru/problem.aspx?space=1&num=1266)
* [Codeforces - No game no life](https://codeforces.com/problemset/problem/1411/G)
