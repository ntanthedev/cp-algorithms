---
tags:
  - Translated
e_maxx_link: primitive_root
translation:
  source: algebra/primitive-root.md
  source_commit: 503ff65edae04aad07dd42188ea091aa5790d627
  status: draft
  last_synced: 2026-08-07
---

# Căn nguyên thủy

## Định nghĩa

Trong số học mô-đun, một số $g$ được gọi là `primitive root modulo n` nếu mọi số nguyên tố cùng nhau với $n$ đều đồng dư với một lũy thừa nào đó của $g$ theo mô-đun $n$. Về mặt toán học, $g$ là một `primitive root modulo n` khi và chỉ khi với mọi số nguyên $a$ thỏa $\gcd(a, n) = 1$, tồn tại một số nguyên $k$ sao cho:

$g^k \equiv a \pmod n$.

Khi đó $k$ được gọi là `index` hoặc `discrete logarithm` của $a$ theo cơ số $g$ modulo $n$. $g$ cũng được gọi là `generator` của nhóm nhân các số nguyên modulo $n$.

Đặc biệt, khi $n$ là số nguyên tố, các lũy thừa của một căn nguyên thủy sẽ lần lượt sinh ra mọi số từ $1$ đến $n-1$.

## Sự tồn tại

Căn nguyên thủy modulo $n$ tồn tại khi và chỉ khi:

* $n$ bằng 1, 2, 4, hoặc
* $n$ là lũy thừa của một số nguyên tố lẻ $(n = p^k)$, hoặc
* $n$ bằng hai lần lũy thừa của một số nguyên tố lẻ $(n = 2 \cdot p^k)$.

Định lý này được Gauss chứng minh vào năm 1801.

## Quan hệ với phi hàm Euler

Giả sử $g$ là một căn nguyên thủy modulo $n$. Khi đó ta có thể chứng minh số nhỏ nhất $k$ sao cho $g^k \equiv 1 \pmod n$ bằng $\phi (n)$. Chiều ngược lại cũng đúng, và đây chính là tính chất được dùng trong bài để tìm căn nguyên thủy.

Hơn nữa, nếu tồn tại căn nguyên thủy modulo $n$, số lượng căn nguyên thủy bằng $\phi (\phi (n) )$.

## Thuật toán tìm căn nguyên thủy

Một thuật toán ngây thơ là xét mọi số trong đoạn $[1, n-1]$, rồi với mỗi số kiểm tra xem nó có phải căn nguyên thủy hay không bằng cách tính tất cả các lũy thừa và xem chúng có đôi một khác nhau hay không. Thuật toán này có độ phức tạp $O(g \cdot n)$ và quá chậm. Trong phần này, ta xây dựng một thuật toán nhanh hơn dựa trên một số định lý quen thuộc.

Từ phần trước, ta biết rằng nếu số nhỏ nhất $k$ sao cho $g^k \equiv 1 \pmod n$ bằng $\phi (n)$ thì $g$ là căn nguyên thủy. Với mọi số $a$ nguyên tố cùng nhau với $n$, định lý Euler cho $a ^ { \phi (n) } \equiv 1 \pmod n$. Vì vậy, để kiểm tra $g$ là căn nguyên thủy, chỉ cần bảo đảm rằng với mọi $d$ nhỏ hơn $\phi (n)$, $g^d \not \equiv 1 \pmod n$. Tuy nhiên, cách này vẫn quá chậm.

Theo định lý Lagrange, index của 1 đối với bất kỳ số nào modulo $n$ phải là một ước của $\phi (n)$. Vì vậy, chỉ cần kiểm tra với mọi ước thực sự $d \mid \phi (n)$ rằng $g^d \not \equiv 1 \pmod n$. Đây đã là một thuật toán nhanh hơn nhiều, nhưng ta vẫn có thể làm tốt hơn.

Phân tích $\phi (n) = p_1 ^ {a_1} \cdots p_s ^ {a_s}$. Ta chứng minh rằng trong thuật toán trên, chỉ cần xét các giá trị $d$ có dạng $\frac { \phi (n) } {p_j}$. Thật vậy, giả sử $d$ là một ước thực sự bất kỳ của $\phi (n)$. Khi đó hiển nhiên tồn tại một $j$ sao cho $d \mid \frac { \phi (n) } {p_j}$, tức $d \cdot k = \frac { \phi (n) } {p_j}$. Nhưng nếu $g^d \equiv 1 \pmod n$, ta sẽ có:

$g ^ { \frac { \phi (n)} {p_j} } \equiv g ^ {d \cdot k} \equiv (g^d) ^k \equiv 1^k \equiv 1 \pmod n$.

Nói cách khác, trong các số có dạng $\frac {\phi (n)} {p_i}$ sẽ có ít nhất một số không thỏa điều kiện.

Ta đã có thuật toán đầy đủ để tìm căn nguyên thủy:

* Trước hết, tính $\phi (n)$ và phân tích nó thành thừa số nguyên tố.
* Sau đó duyệt mọi số $g \in [1, n]$; với mỗi số, để kiểm tra nó có phải căn nguyên thủy hay không, ta làm như sau:

    * Tính tất cả $g ^ { \frac {\phi (n)} {p_i}} \pmod n$.
    * Nếu mọi giá trị tính được đều khác $1$, thì $g$ là một căn nguyên thủy.

    Thời gian chạy của thuật toán là $O(Ans \cdot \log \phi (n) \cdot \log n)$ (giả sử $\phi (n)$ có $\log \phi (n)$ ước).

Shoup (1990, 1992) chứng minh rằng, nếu giả thuyết [Riemann tổng quát](http://en.wikipedia.org/wiki/Generalized_Riemann_hypothesis) đúng, thì $g$ là $O(\log^6 p)$.

## Cài đặt

Đoạn code dưới đây giả sử modulo `p` là một số nguyên tố. Để dùng được với mọi giá trị của `p`, ta phải bổ sung việc tính $\phi (p)$. 

```cpp
int powmod (int a, int b, int p) {
	int res = 1;
	while (b)
		if (b & 1)
			res = int (res * 1ll * a % p),  --b;
		else
			a = int (a * 1ll * a % p),  b >>= 1;
	return res;
}
 
int generator (int p) {
	vector<int> fact;
	int phi = p-1,  n = phi;
	for (int i=2; i*i<=n; ++i)
		if (n % i == 0) {
			fact.push_back (i);
			while (n % i == 0)
				n /= i;
		}
	if (n > 1)
		fact.push_back (n);
 
	for (int res=2; res<=p; ++res) {
		bool ok = true;
		for (size_t i=0; i<fact.size() && ok; ++i)
			ok &= powmod (res, phi / fact[i], p) != 1;
		if (ok)  return res;
	}
	return -1;
}
```
