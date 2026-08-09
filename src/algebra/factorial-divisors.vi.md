---
tags:
  - Translated
e_maxx_link: factorial_divisors
translation:
  source: algebra/factorial-divisors.md
  source_commit: 8071fab1b3bf96db89e6d6cfbc31e63c921b91ec
  status: draft
  last_synced: 2026-08-09
---

# Tìm số mũ lớn nhất của một ước trong giai thừa

Cho hai số $n$ và $k$. Hãy tìm số nguyên lớn nhất $x$ sao cho $k^x$ là ước của $n!$.

## $k$ nguyên tố {data-toc-label="Prime k"}

Trước hết, xét trường hợp $k$ là số nguyên tố. Viết giai thừa dưới dạng tích:

$$n! = 1 \cdot 2 \cdot 3 \ldots (n-1) \cdot n$$

Cứ mỗi phần tử thứ $k$ trong tích lại chia hết cho $k$, tức đóng góp thêm $+1$ vào đáp án; số phần tử như vậy là $\Bigl\lfloor\dfrac{n}{k}\Bigr\rfloor$.

Tiếp theo, cứ mỗi phần tử thứ $k^2$ lại chia hết cho $k^2$, nên đóng góp thêm một $+1$ nữa vào đáp án (thừa số $k$ thứ nhất đã được tính ở đoạn trước). Số phần tử như vậy là $\Bigl\lfloor\dfrac{n}{k^2}\Bigr\rfloor$.

Tương tự, với mỗi $i$, cứ mỗi phần tử thứ $k^i$ lại đóng góp thêm $+1$ vào đáp án, và có $\Bigl\lfloor\dfrac{n}{k^i}\Bigr\rfloor$ phần tử như vậy.

Đáp án cuối cùng là

$$\Bigl\lfloor\dfrac{n}{k}\Bigr\rfloor + \Bigl\lfloor\dfrac{n}{k^2}\Bigr\rfloor + \ldots + \Bigl\lfloor\dfrac{n}{k^i}\Bigr\rfloor + \ldots$$

Kết quả này còn được gọi là [công thức Legendre](https://en.wikipedia.org/wiki/Legendre%27s_formula).
Tổng trên tất nhiên là hữu hạn, vì chỉ xấp xỉ $\log_k n$ số hạng đầu tiên khác 0. Do đó, thời gian chạy của thuật toán là $O(\log_k n)$.

### Cài đặt

```cpp

int fact_pow (int n, int k) {
	int res = 0;
	while (n) {
		n /= k;
		res += n;
	}
	return res;
}

```

## $k$ hợp số {data-toc-label="Composite k"}

Không thể áp dụng trực tiếp ý tưởng trên. Thay vào đó, ta phân tích $k$ thành thừa số nguyên tố, viết $k = k_1^{p_1} \cdot \ldots \cdot k_m^{p_m}$. Với mỗi $k_i$, dùng thuật toán phía trên để tìm số lần thừa số này xuất hiện trong $n!$; gọi giá trị đó là $a_i$. Nguồn viết đáp án cho trường hợp $k$ hợp số là

$$\min_ {i=1 \ldots m} \dfrac{a_i}{p_i}$$

**Ghi chú bản dịch:** Vì bài toán yêu cầu x là số nguyên, biểu thức nguồn phía trên còn thiếu phép lấy phần nguyên. Với mỗi thừa số nguyên tố trong phân tích của k, số bản sao đầy đủ có thể lấy từ n! là phần nguyên của số lần thừa số đó xuất hiện chia cho số mũ tương ứng; đáp án phải lấy giá trị nhỏ nhất trong các số nguyên đó. Vấn đề này được đề xuất sửa riêng ở bản tiếng Anh.
