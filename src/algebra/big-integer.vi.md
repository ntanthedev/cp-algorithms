---
tags:
  - Translated
e_maxx_link: big_integer
translation:
  source: algebra/big-integer.md
  source_commit: 72d1379836bd402347e0af600cbb7833f571418c
  status: draft
  last_synced: 2026-11-16
---

# Số học với độ chính xác tùy ý

Số học với độ chính xác tùy ý, còn gọi là "bignum" hoặc đơn giản là "số học số lớn", gồm các cấu trúc dữ liệu và thuật toán cho phép xử lý những số lớn hơn nhiều so với phạm vi của các kiểu dữ liệu thông thường. Dưới đây là một số phương pháp.

## Số học số nguyên lớn cổ điển

Ý tưởng chính là lưu số dưới dạng mảng các "chữ số" trong một cơ số nào đó. Các cơ số thường dùng nhất là 10, lũy thừa của 10 ($10^4$ hoặc $10^9$) và 2.

Các phép toán được thực hiện bằng những thuật toán cộng, trừ, nhân và chia đặt tính như ở trường. Ta cũng có thể dùng các thuật toán nhân nhanh: biến đổi Fourier nhanh và thuật toán Karatsuba.

Ở đây ta chỉ xét số nguyên không âm. Để xử lý số âm, cần thêm và duy trì một cờ "số âm" hoặc dùng biểu diễn số nguyên dạng bù hai.

### Cấu trúc dữ liệu

Ta lưu số bằng một `vector<int>`, trong đó mỗi phần tử là một "chữ số" của số đó.

```cpp
typedef vector<int> lnum;
```

Để tăng hiệu năng, ta dùng cơ số $10^9$, nên mỗi "chữ số" của số lớn chứa 9 chữ số thập phân.

```cpp
const int base = 1000*1000*1000;
```

Các chữ số được lưu từ hàng thấp nhất đến hàng cao nhất. Các phép toán được cài đặt sao cho kết quả không có số 0 ở đầu, với điều kiện các toán hạng cũng không có số 0 ở đầu. Sau mỗi phép toán có thể tạo ra số 0 ở đầu, cần chạy đoạn mã loại bỏ chúng. Trong biểu diễn này, có hai cách hợp lệ để biểu diễn số 0: vector rỗng và vector chỉ chứa một chữ số 0.

### Xuất dữ liệu

In số nguyên lớn là phép toán đơn giản nhất. Trước tiên in phần tử cuối của vector (hoặc 0 nếu vector rỗng), sau đó in các phần tử còn lại và thêm số 0 ở đầu nếu cần để mỗi phần có đúng 9 chữ số.

```cpp
printf ("%d", a.empty() ? 0 : a.back());
for (int i=(int)a.size()-2; i>=0; --i)
	printf ("%09d", a[i]);
```

Ta ép `a.size()` sang số nguyên có dấu để tránh tràn xuống của số nguyên không dấu khi vector có ít hơn 2 phần tử.

### Nhập dữ liệu

Để đọc số nguyên lớn, đọc biểu diễn của nó vào một `string` rồi chuyển thành các "chữ số":

```cpp
for (int i=(int)s.length(); i>0; i-=9)
	if (i < 9)
		a.push_back (atoi (s.substr (0, i).c_str()));
	else
		a.push_back (atoi (s.substr (i-9, 9).c_str()));
```

Nếu dùng mảng `char` thay cho `string`, mã còn ngắn hơn:

```cpp
for (int i=(int)strlen(s); i>0; i-=9) {
	s[i] = 0;
	a.push_back (atoi (i>=9 ? s+i-9 : s));
}
```

Nếu đầu vào có thể chứa số 0 ở đầu, ta có thể loại bỏ chúng như sau:

```cpp
while (a.size() > 1 && a.back() == 0)
	a.pop_back();
```

### Phép cộng

Cộng số nguyên lớn $a$ với $b$ và lưu kết quả vào $a$:

```cpp
int carry = 0;
for (size_t i=0; i<max(a.size(),b.size()) || carry; ++i) {
	if (i == a.size())
		a.push_back (0);
	a[i] += carry + (i < b.size() ? b[i] : 0);
	carry = a[i] >= base;
	if (carry)  a[i] -= base;
}
```

### Phép trừ

Lấy số nguyên lớn $a$ trừ $b$ ($a \ge b$) và lưu kết quả vào $a$:

```cpp
int carry = 0;
for (size_t i=0; i<b.size() || carry; ++i) {
	a[i] -= carry + (i < b.size() ? b[i] : 0);
	carry = a[i] < 0;
	if (carry)  a[i] += base;
}
while (a.size() > 1 && a.back() == 0)
	a.pop_back();
```

Sau phép trừ, ta loại bỏ các số 0 ở đầu để duy trì quy ước số nguyên lớn không có số 0 ở đầu.

### Nhân với số nguyên nhỏ

Nhân số nguyên lớn $a$ với số nguyên nhỏ $b$ ($b < base$) và lưu kết quả vào $a$:

```cpp
int carry = 0;
for (size_t i=0; i<a.size() || carry; ++i) {
	if (i == a.size())
		a.push_back (0);
	long long cur = carry + a[i] * 1ll * b;
	a[i] = int (cur % base);
	carry = int (cur / base);
}
while (a.size() > 1 && a.back() == 0)
	a.pop_back();
```

Tối ưu thêm: nếu thời gian chạy đặc biệt quan trọng, có thể thay hai phép chia bằng một phép chia: chỉ tính thương nguyên (biến `carry`), rồi dùng phép nhân để tìm số dư. Cách này thường giúp mã nhanh hơn, dù mức cải thiện không quá lớn.

### Nhân với số nguyên lớn

Nhân hai số nguyên lớn $a$ và $b$, lưu kết quả vào $c$:

```cpp
lnum c (a.size()+b.size());
for (size_t i=0; i<a.size(); ++i)
	for (int j=0, carry=0; j<(int)b.size() || carry; ++j) {
		long long cur = c[i+j] + a[i] * 1ll * (j < (int)b.size() ? b[j] : 0) + carry;
		c[i+j] = int (cur % base);
		carry = int (cur / base);
	}
while (c.size() > 1 && c.back() == 0)
	c.pop_back();
```

### Chia cho số nguyên nhỏ

Chia số nguyên lớn $a$ cho số nguyên nhỏ $b$ ($b < base$), lưu thương nguyên vào $a$ và số dư vào `carry`:

```cpp
int carry = 0;
for (int i=(int)a.size()-1; i>=0; --i) {
	long long cur = a[i] + carry * 1ll * base;
	a[i] = int (cur / b);
	carry = int (cur % b);
}
while (a.size() > 1 && a.back() == 0)
	a.pop_back();
```

## Số học số nguyên lớn bằng biểu diễn phân tích thừa số

Ý tưởng là lưu số nguyên dưới dạng phân tích thừa số, tức các lũy thừa của những số nguyên tố là ước của số đó.

Cách này rất dễ cài đặt và hỗ trợ nhân, chia dễ dàng (nhanh hơn phương pháp cổ điển về độ phức tạp tiệm cận), nhưng không hỗ trợ cộng hoặc trừ. Nó cũng tiết kiệm bộ nhớ hơn nhiều so với cách cổ điển.

Phương pháp này thường được dùng để tính modulo một hợp số M; khi đó, một số được lưu bằng các lũy thừa của những ước của M mà số đó chia hết, cùng với phần dư modulo M.

## Số học số nguyên lớn theo các modulo nguyên tố (thuật toán Garner)

Ý tưởng là chọn một tập số nguyên tố (thường đủ nhỏ để lưu trong kiểu số nguyên thông thường) và lưu số nguyên dưới dạng vector các số dư khi chia nó cho từng số nguyên tố đó.

Định lý phần dư Trung Hoa cho biết biểu diễn này đủ để khôi phục duy nhất mọi số từ 0 đến tích các số nguyên tố đó trừ một. [Thuật toán Garner](garners-algorithm.md) cho phép khôi phục số nguyên dạng thông thường từ biểu diễn này.

Cách này tiết kiệm bộ nhớ so với phương pháp cổ điển (dù không tiết kiệm nhiều như biểu diễn phân tích thừa số). Ngoài ra, nó hỗ trợ cộng, trừ và nhân nhanh với thời gian tỉ lệ với số lượng số nguyên tố dùng làm modulo (xem bài [Định lý phần dư Trung Hoa](chinese-remainder-theorem.md) để biết cách cài đặt).

Đổi lại, việc chuyển số nguyên về dạng thông thường khá mất công và đòi hỏi cài đặt số học độ chính xác tùy ý cổ điển có phép nhân. Ngoài ra, phương pháp này không hỗ trợ phép chia.

## Số học phân số với độ chính xác tùy ý

Trong thi lập trình, phân số xuất hiện ít hơn số nguyên và việc cài đặt số học số lớn cho phân số cũng khó hơn nhiều, vì vậy chỉ một số ít kỹ thuật được sử dụng.

### Số học với phân số tối giản

Một số được biểu diễn bằng phân số tối giản $\frac{a}{b}$, trong đó $a$ và $b$ là số nguyên. Mọi phép toán trên phân số có thể quy về các phép toán trên tử số và mẫu số nguyên. Thông thường cần dùng số học độ chính xác tùy ý cổ điển để lưu tử và mẫu, nhưng đôi khi kiểu số nguyên 64 bit có sẵn là đủ.

### Lưu số mũ dấu phẩy động dưới dạng riêng

Đôi khi bài toán yêu cầu xử lý số rất nhỏ hoặc rất lớn mà không được xảy ra tràn trên hay tràn dưới. Kiểu double có sẵn chiếm 8–10 byte và cho phép số mũ trong khoảng $[-308; 308]$, đôi khi không đủ.

Cách làm rất đơn giản: dùng một biến nguyên riêng để lưu số mũ; sau mỗi phép toán, chuẩn hóa số dấu phẩy động, tức đưa nó về khoảng $[0.1; 1)$ bằng cách điều chỉnh số mũ tương ứng.

Khi nhân hoặc chia hai số như vậy, ta lần lượt cộng hoặc trừ các số mũ của chúng. Khi cộng hoặc trừ hai số, trước tiên cần đưa chúng về cùng số mũ bằng cách nhân một số với 10 lũy thừa bằng hiệu hai số mũ.

Cuối cùng, cơ số của số mũ không nhất thiết phải là 10. Dựa trên biểu diễn nội bộ của số dấu phẩy động, dùng cơ số 2 là hợp lý nhất.

## Bài tập luyện tập


* [UVA - How Many Fibs?](https://uva.onlinejudge.org/index.php?option=onlinejudge&page=show_problem&problem=1124)
* [UVA - Product](https://uva.onlinejudge.org/index.php?option=com_onlinejudge&Itemid=8&page=show_problem&problem=1047)
* [UVA - Maximum Sub-sequence Product](https://uva.onlinejudge.org/index.php?option=onlinejudge&page=show_problem&problem=728)
* [SPOJ - Fast Multiplication](http://www.spoj.com/problems/MUL/en/)
* [SPOJ - GCD2](http://www.spoj.com/problems/GCD2/)
* [UVA - Division](https://uva.onlinejudge.org/index.php?option=onlinejudge&page=show_problem&problem=1024)
* [UVA - Fibonacci Freeze](https://uva.onlinejudge.org/index.php?option=com_onlinejudge&Itemid=8&page=show_problem&problem=436)
* [UVA - Krakovia](https://uva.onlinejudge.org/index.php?option=onlinejudge&page=show_problem&problem=1866)
* [UVA - Simplifying Fractions](https://uva.onlinejudge.org/index.php?option=com_onlinejudge&Itemid=8&page=show_problem&problem=1755)
* [UVA - 500!](https://uva.onlinejudge.org/index.php?option=onlinejudge&page=show_problem&problem=564)
* [Hackerrank - Factorial digit sum](https://www.hackerrank.com/contests/projecteuler/challenges/euler020/problem)
* [UVA - Immortal Rabbits](https://uva.onlinejudge.org/index.php?option=com_onlinejudge&Itemid=8&page=show_problem&problem=4803)
* [SPOJ - 0110SS](http://www.spoj.com/problems/IWGBS/)
* [Codeforces - Notepad](http://codeforces.com/contest/17/problem/D)
