---
tags:
  - Translated
e_maxx_link: discrete_root
translation:
  source: algebra/discrete-root.md
  source_commit: 6b635c1acead7c91df1a119c4169b997cf424a7d
  status: draft
  last_synced: 2026-08-07
---

# Căn rời rạc

Bài toán tìm căn rời rạc (discrete root) được định nghĩa như sau. Cho một số nguyên tố $n$ và hai số nguyên $a$, $k$, hãy tìm mọi $x$ sao cho:

$x^k \equiv a \pmod n$

## Thuật toán

Ta sẽ giải bài toán này bằng cách đưa nó về [bài toán logarit rời rạc](discrete-log.md).

Ta sử dụng khái niệm [căn nguyên thủy](primitive-root.md) modulo $n$. Gọi $g$ là một căn nguyên thủy modulo $n$. Vì $n$ là số nguyên tố nên căn nguyên thủy chắc chắn tồn tại, và có thể tìm được trong $O(Ans \cdot \log \phi (n) \cdot \log n) = O(Ans \cdot \log^2 n)$ cộng với thời gian phân tích $\phi (n)$ thành thừa số nguyên tố.

Ta có thể xử lý ngay trường hợp $a = 0$. Khi đó hiển nhiên chỉ có một đáp án: $x = 0$.

Vì $n$ là số nguyên tố và mọi số từ 1 đến $n-1$ đều có thể biểu diễn thành một lũy thừa của căn nguyên thủy, ta có thể viết bài toán căn rời rạc dưới dạng:

$(g^y)^k \equiv a \pmod n$

trong đó

$x \equiv g^y \pmod n$

Từ đó ta viết lại thành

$(g^k)^y \equiv a \pmod n$

Giờ chỉ còn một ẩn $y$, và đây chính là một bài toán logarit rời rạc. Ta có thể tìm nghiệm bằng thuật toán Baby-step giant-step của Shanks trong $O(\sqrt {n} \log n)$ (hoặc xác nhận rằng không tồn tại nghiệm).

Sau khi tìm được một nghiệm $y_0$, một nghiệm của bài toán căn rời rạc là $x_0 = g^{y_0} \pmod n$.

## Tìm mọi nghiệm từ một nghiệm đã biết

Để giải đầy đủ bài toán, ta cần tìm mọi nghiệm khi đã biết một nghiệm $x_0 = g^{y_0} \pmod n$.

Nhắc lại rằng căn nguyên thủy luôn có bậc bằng $\phi (n)$, tức lũy thừa dương nhỏ nhất của $g$ cho kết quả 1 là $\phi (n)$. Vì vậy, nếu cộng thêm $\phi (n)$ vào số mũ, ta vẫn thu được cùng giá trị:

$x^k \equiv g^{ y_0 \cdot k + l \cdot \phi (n)} \equiv a \pmod n \forall l \in Z$

Do đó, mọi nghiệm đều có dạng:

$x = g^{y_0 + \frac {l \cdot \phi (n)}{k}} \pmod n \forall l \in Z$.

trong đó $l$ được chọn sao cho phân số là một số nguyên. Để điều này đúng, tử số phải chia hết cho bội chung nhỏ nhất của $\phi (n)$ và $k$. Nhớ rằng bội chung nhỏ nhất của hai số $lcm(a, b) = \frac{a \cdot b}{gcd(a, b)}$; ta thu được

$x = g^{y_0 + i \frac {\phi (n)}{gcd(k, \phi (n))}} \pmod n \forall i \in Z$.

Đây là công thức cuối cùng cho mọi nghiệm của bài toán căn rời rạc.

## Cài đặt

Dưới đây là một cài đặt đầy đủ, gồm các thủ tục tìm căn nguyên thủy, logarit rời rạc, cũng như tìm và in mọi nghiệm.

```cpp
int gcd(int a, int b) {
	return a ? gcd(b % a, a) : b;
}
 
int powmod(int a, int b, int p) {
	int res = 1;
	while (b > 0) {
		if (b & 1) {
			res = res * a % p;
		}
		a = a * a % p;
		b >>= 1;
	}
	return res;
}
 
// Finds the primitive root modulo p
int generator(int p) {
	vector<int> fact;
	int phi = p-1, n = phi;
	for (int i = 2; i * i <= n; ++i) {
		if (n % i == 0) {
			fact.push_back(i);
			while (n % i == 0)
				n /= i;
		}
	}
	if (n > 1)
		fact.push_back(n);
 
	for (int res = 2; res <= p; ++res) {
		bool ok = true;
		for (int factor : fact) {
			if (powmod(res, phi / factor, p) == 1) {
				ok = false;
				break;
			}
		}
		if (ok) return res;
	}
	return -1;
}
 
// This program finds all numbers x such that x^k = a (mod n)
int main() {
	int n, k, a;
	scanf("%d %d %d", &n, &k, &a);
	if (a == 0) {
		puts("1\n0");
		return 0;
	}
 
	int g = generator(n);
 
	// Baby-step giant-step discrete logarithm algorithm
	int sq = (int) sqrt (n + .0) + 1;
	vector<pair<int, int>> dec(sq);
	for (int i = 1; i <= sq; ++i)
		dec[i-1] = {powmod(g, i * sq * k % (n - 1), n), i};
	sort(dec.begin(), dec.end());
	int any_ans = -1;
	for (int i = 0; i < sq; ++i) {
		int my = powmod(g, i * k % (n - 1), n) * a % n;
		auto it = lower_bound(dec.begin(), dec.end(), make_pair(my, 0));
		if (it != dec.end() && it->first == my) {
			any_ans = it->second * sq - i;
			break;
		}
	}
	if (any_ans == -1) {
		puts("0");
		return 0;
	}
 
	// Print all possible answers
	int delta = (n-1) / gcd(k, n-1);
	vector<int> ans;
	for (int cur = any_ans % delta; cur < n-1; cur += delta)
		ans.push_back(powmod(g, cur, n));
	sort(ans.begin(), ans.end());
	printf("%d\n", ans.size());
	for (int answer : ans)
		printf("%d ", answer);
}
```

## Bài tập luyện tập

* [Codeforces - Lunar New Year and a Recursive Sequence](https://codeforces.com/contest/1106/problem/F)
