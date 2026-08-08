---
tags:
  - Translated
e_maxx_link: inclusion_exclusion_principle
translation:
  source: combinatorics/inclusion-exclusion.md
  source_commit: ed6767216f0f81af0bdb0e0174ed3a5d147967e8
  status: draft
  last_synced: 2026-08-08
---

# Nguyên lý bao hàm – loại trừ

Nguyên lý bao hàm – loại trừ là một phương pháp tổ hợp quan trọng để tính số phần tử của một tập hợp hoặc xác suất của các biến cố phức tạp. Nó liên hệ kích thước của các tập riêng lẻ với kích thước hợp của chúng.

## Phát biểu

### Công thức bằng lời

Có thể diễn đạt nguyên lý bao hàm – loại trừ như sau:

Để tính số phần tử của hợp nhiều tập hợp, trước hết cộng kích thước của từng tập **riêng lẻ**, sau đó trừ kích thước của mọi giao **từng cặp**, rồi cộng lại kích thước của các giao **từng bộ ba**, trừ kích thước của các giao **từng bộ bốn**, và tiếp tục xen kẽ như vậy cho đến giao của **tất cả** các tập.

### Công thức theo ngôn ngữ tập hợp

Định nghĩa trên có thể viết dưới dạng toán học như sau:

$$\left| \bigcup_{i=1}^n A_i \right| = \sum_{i=1}^n|A_i| - \sum_{1\leq i<j\leq n} |A_i \cap A_j| + \sum _{1\leq i<j<k\leq n}|A_i \cap A_j \cap A_k| - \cdots + (-1)^{n-1} | A_1 \cap \cdots \cap A_n |$$

Và viết gọn hơn:

$$\left|\bigcup_{i=1}^n A_i \right| = \sum_{\emptyset \neq J\subseteq \{1,2,\ldots ,n\}} (-1)^{|J|-1}{\Biggl |}\bigcap_{j\in J}A_{j}{\Biggr |}$$

### Diễn giải bằng biểu đồ Venn

Xét biểu đồ của ba tập $A$, $B$ và $C$:

![Biểu đồ Venn](venn-inclusion-exclusion.png "Biểu đồ Venn")

Diện tích hợp $A \cup B \cup C$ bằng tổng diện tích của $A$, $B$ và $C$, trừ đi các phần bị tính hai lần $A \cap B$, $A \cap C$, $B \cap C$, rồi cộng lại phần bị cả ba tập phủ lên $A \cap B \cap C$:

$$S(A \cup B \cup C) = S(A) + S(B) + S(C) - S(A \cap B) - S(A \cap C) - S(B \cap C) + S(A \cap B \cap C)$$

Lập luận này cũng tổng quát được cho hợp của $n$ tập hợp.

### Công thức trong xác suất

Nếu $A_i$ $(i = 1,2...n)$ là các biến cố và ${\cal P}(A_i)$ là xác suất biến cố $A_i$ xảy ra, thì xác suất của hợp các biến cố (tức xác suất có ít nhất một biến cố xảy ra) bằng:

$$\begin{eqnarray}
{\cal P} \left( \bigcup_{i=1}^n A_i \right) &=& \sum_{i=1}^n{\cal P}(A_i)\ - \sum_{1\leq i<j\leq n} {\cal P}(A_i \cap A_j)\  + \\
&+& \sum _{1\leq i<j<k\leq n}{\cal P}(A_i \cap A_j \cap A_k) - \cdots + (-1)^{n-1} {\cal P}( A_1 \cap \cdots \cap A_n )
\end{eqnarray}$$

Và viết gọn hơn:

$${\cal P} \left(\bigcup_{i=1}^n A_i \right) = \sum_{\emptyset \neq J\subseteq \{1,2,\ldots ,n\}} (-1)^{|J|-1}\ {\cal P}{\Biggl (}\bigcap_{j\in J}A_{j}{\Biggr )}$$

## Chứng minh

Để chứng minh, thuận tiện nhất là dùng công thức toán học theo ngôn ngữ tập hợp:

$$\left|\bigcup_{i=1}^n A_i \right| = \sum_{\emptyset \neq J\subseteq \{1,2,\ldots ,n\}} (-1)^{|J|-1}{\Biggl |}\bigcap_{j\in J}A_{j}{\Biggr |}$$

Ta cần chứng minh rằng mọi phần tử thuộc ít nhất một tập $A_i$ chỉ xuất hiện đúng một lần trong công thức (các phần tử không thuộc bất kỳ tập $A_i$ nào hiển nhiên không bao giờ xuất hiện ở vế phải).

Xét một phần tử $x$ xuất hiện trong $k \geq 1$ tập $A_i$. Ta sẽ chứng minh nó được đếm đúng một lần. Lưu ý rằng:

* trong các hạng tử có $|J| = 1$, phần tử $x$ được tính **$+\ k$** lần;
* trong các hạng tử có $|J| = 2$, phần tử $x$ được tính **$-\ \binom{k}{2}$** lần — vì nó xuất hiện trong những hạng tử chọn hai trong số $k$ tập chứa $x$;
* trong các hạng tử có $|J| = 3$, phần tử $x$ được tính **$+\ \binom{k}{3}$** lần;
* $\cdots$
* trong các hạng tử có $|J| = k$, phần tử $x$ được tính **$(-1)^{k-1}\cdot \binom{k}{k}$** lần;
* trong các hạng tử có $|J| \gt k$, phần tử $x$ được tính **không** lần nào;

Ta thu được tổng [các hệ số nhị thức](binomial-coefficients.md) sau:

$$ T = \binom{k}{1} - \binom{k}{2} + \binom{k}{3} - \cdots + (-1)^{i-1}\cdot \binom{k}{i} + \cdots + (-1)^{k-1}\cdot \binom{k}{k}$$

Biểu thức này rất giống khai triển nhị thức của $(1 - x)^k$:

$$ (1 - x)^k = \binom{k}{0} - \binom{k}{1} \cdot x + \binom{k}{2} \cdot x^2 - \binom{k}{3} \cdot x^3 + \cdots + (-1)^k\cdot \binom{k}{k} \cdot x^k $$

Khi $x = 1$, $(1 - x)^k$ gần như chính là $T$. Tuy nhiên, biểu thức còn có thêm $\binom{k}{0} = 1$, và phần còn lại được nhân với $-1$. Do đó $(1 - 1)^k = 1 - T$. Suy ra $T = 1 - (1 - 1)^k = 1$, đúng như cần chứng minh: phần tử được tính đúng một lần.

## Tổng quát hóa để đếm phần tử nằm trong đúng $r$ tập {data-toc-label="Generalization for calculating number of elements in exactly r sets"}

Nguyên lý bao hàm – loại trừ có thể viết lại để tính số phần tử không nằm trong tập nào:

$$\left|\bigcap_{i=1}^n \overline{A_i}\right|=\sum_{m=0}^n (-1)^m \sum_{|X|=m} \left|\bigcap_{i\in X} A_{i}\right|$$

Xét tổng quát hóa để tính số phần tử nằm trong đúng $r$ tập:

$$\left|\bigcup_{|B|=r}\left[\bigcap_{i \in B} A_i \cap \bigcap_{j \not\in B} \overline{A_j}\right]\right|=\sum_{m=r}^n (-1)^{m-r}\dbinom{m}{r} \sum_{|X|=m} \left|\bigcap_{i \in X} A_{i}\right|$$

Để chứng minh công thức, xét một tập $B$ cụ thể. Từ nguyên lý bao hàm – loại trừ cơ bản, ta có:

$$\left|\bigcap_{i \in B} A_i \cap \bigcap_{j \not \in B} \overline{A_j}\right|=\sum_{m=r}^{n} (-1)^{m-r} \sum_{\substack{|X|=m \newline B \subset X}}\left|\bigcap_{i\in X} A_{i}\right|$$

Các tập ở vế trái không giao nhau với những $B$ khác nhau, nên có thể cộng trực tiếp. Đồng thời, mỗi tập $X$ luôn có hệ số $(-1)^{m-r}$ mỗi khi xuất hiện, và nó xuất hiện với đúng $\dbinom{m}{r}$ tập $B$.

## Ứng dụng khi giải bài

Nguyên lý bao hàm – loại trừ khá khó nắm nếu chưa xem các ứng dụng cụ thể.

Trước hết, ta xét ba bài đơn giản có thể giải "trên giấy" để minh họa cách dùng nguyên lý, sau đó mới đến các bài thực tế khó giải nếu không có bao hàm – loại trừ.

Đặc biệt nên chú ý những bài yêu cầu "tìm **số** cách", bởi đôi khi chúng dẫn tới lời giải đa thức chứ không nhất thiết phải là lời giải mũ.

### Một bài đơn giản về hoán vị

Bài toán: đếm số hoán vị của các số từ $0$ đến $9$ sao cho phần tử đầu tiên lớn hơn $1$ và phần tử cuối cùng nhỏ hơn $8$.

Ta đếm số hoán vị "xấu", tức các hoán vị có phần tử đầu tiên $\leq 1$ và/hoặc phần tử cuối cùng $\geq 8$.

Ký hiệu $X$ là tập các hoán vị có phần tử đầu tiên $\leq 1$, còn $Y$ là tập các hoán vị có phần tử cuối cùng $\geq 8$. Theo công thức bao hàm – loại trừ, số hoán vị "xấu" là:

$$ |X \cup Y| = |X| + |Y| - |X \cap Y| $$

Sau một phép đếm tổ hợp đơn giản, ta có:

$$ 2 \cdot 9! + 2 \cdot 9! - 2 \cdot 2 \cdot 8! $$

Cuối cùng chỉ cần lấy tổng số $10!$ hoán vị trừ đi giá trị này để được số hoán vị "tốt".

### Một bài đơn giản về dãy (0, 1, 2)

Bài toán: đếm số dãy độ dài $n$ chỉ gồm các số $0,1,2$ sao cho mỗi số xuất hiện **ít nhất một lần**.

Một lần nữa, chuyển sang bài toán bù: tính số dãy **không chứa ít nhất một** trong ba số.

Ký hiệu $A_i (i = 0,1,2)$ là tập các dãy không chứa chữ số $i$.
Công thức bao hàm – loại trừ cho số dãy "xấu" là:

$$ |A_0 \cup A_1 \cup A_2| = |A_0| + |A_1| + |A_2| - |A_0 \cap A_1| - |A_0 \cap A_2| - |A_1 \cap A_2| + |A_0 \cap A_1 \cap A_2| $$

* Kích thước mỗi $A_i$ là $2^n$, vì mỗi dãy chỉ có thể dùng hai chữ số còn lại.
* Kích thước mỗi giao từng cặp $A_i \cap A_j$ bằng $1$, vì chỉ còn một chữ số để tạo dãy.
* Kích thước giao của cả ba tập bằng $0$, vì không còn chữ số nào để tạo dãy.

Vì ta vừa giải bài toán bù, lấy tổng $3^n$ dãy trừ số dãy xấu:

$$3^n - (3 \cdot 2^n - 3 \cdot 1 + 0)$$

<div id="the-number-of-integer-solutions-to-the-equation"></div>
### Số nghiệm nguyên có chặn trên {: #number-of-upper-bound-integer-sums }

Xét phương trình:

$$x_1 + x_2 + x_3 + x_4 + x_5 + x_6 = 20$$

với $0 \le x_i \le 8 ~ (i = 1,2,\ldots 6)$.

Bài toán: đếm số nghiệm của phương trình.

Tạm bỏ điều kiện chặn trên của $x_i$ và chỉ đếm số nghiệm không âm. Có thể làm dễ dàng bằng [Stars and Bars](stars_and_bars.md):
ta cần chia một dãy $20$ đơn vị thành $6$ nhóm, tương đương với việc sắp xếp $5$ _thanh_ và $20$ _sao_:

$$N_0 = \binom{25}{5}$$

Bây giờ ta tính số nghiệm "xấu" bằng nguyên lý bao hàm – loại trừ. Nghiệm "xấu" là những nghiệm có một hoặc nhiều $x_i$ lớn hơn hoặc bằng $9$.

Ký hiệu $A_k ~ (k = 1,2\ldots 6)$ là tập các nghiệm có $x_k \ge 9$, còn các biến khác thỏa $x_i \ge 0 ~ (i \ne k)$ (chúng có thể $\ge 9$ hoặc không). Để tính kích thước $A_k$, lưu ý rằng về bản chất ta có cùng bài toán tổ hợp như hai đoạn trên, chỉ khác là $9$ đơn vị đã được lấy khỏi các ô trống và chắc chắn thuộc nhóm đầu tiên. Do đó:

$$ | A_k | = \binom{16}{5} $$

Tương tự, kích thước giao của hai tập $A_k$ và $A_p$ (với $k \ne p$) là:

$$ \left| A_k \cap A_p \right| = \binom{7}{5}$$

Mỗi giao của ba tập có kích thước bằng không, vì $20$ đơn vị không đủ để ba biến trở lên cùng lớn hơn hoặc bằng $9$.

Ghép tất cả vào công thức bao hàm – loại trừ, đồng thời nhớ rằng ta đang giải bài toán bù, ta thu được đáp án:

$$\binom{25}{5} - \left(\binom{6}{1} \cdot \binom{16}{5} - \binom{6}{2} \cdot \binom{7}{5}\right) $$

Bài toán dễ dàng tổng quát cho $d$ số có tổng bằng $s$ với điều kiện $0 \le x_i \le b$:

$$\sum_{i=0}^d (-1)^i \binom{d}{i} \binom{s+d-1-(b+1)i}{d-1}$$

Như trên, ta coi các hệ số nhị thức có chỉ số trên âm bằng không.

Bài toán này cũng có thể giải bằng quy hoạch động hoặc hàm sinh. Đáp án bằng bao hàm – loại trừ được tính trong $O(d)$ thời gian (giả sử các phép toán như tính hệ số nhị thức mất thời gian hằng số), còn một cách quy hoạch động đơn giản sẽ mất $O(ds)$.

### Số lượng số nguyên tố cùng nhau trong một đoạn

Bài toán: cho hai số $n$ và $r$, đếm số số nguyên trong đoạn $[1;r]$ nguyên tố cùng nhau với n (ước chung lớn nhất của chúng bằng $1$).

Ta giải bài toán bù — đếm số phần tử không nguyên tố cùng nhau với $n$.

Ký hiệu các thừa số nguyên tố của $n$ là $p_i (i = 1\cdots k)$.

Có bao nhiêu số trong đoạn $[1;r]$ chia hết cho $p_i$? Đáp án là:

$$ \left\lfloor \frac{ r }{ p_i } \right\rfloor $$

Tuy nhiên, nếu chỉ cộng các lượng này, một số số sẽ bị tính nhiều lần (những số chứa nhiều $p_i$ làm thừa số). Vì vậy cần dùng nguyên lý bao hàm – loại trừ.

Ta duyệt tất cả $2^k$ tập con của các $p_i$, tính tích của chúng rồi cộng hoặc trừ số bội của tích đó.

Dưới đây là cài đặt C++:

```cpp
int solve (int n, int r) {
	vector<int> p;
	for (int i=2; i*i<=n; ++i)
		if (n % i == 0) {
			p.push_back (i);
			while (n % i == 0)
				n /= i;
		}
	if (n > 1)
		p.push_back (n);

	int sum = 0;
	for (int msk=1; msk<(1<<p.size()); ++msk) {
		int mult = 1,
			bits = 0;
		for (int i=0; i<(int)p.size(); ++i)
			if (msk & (1<<i)) {
				++bits;
				mult *= p[i];
			}

		int cur = r / mult;
		if (bits % 2 == 1)
			sum += cur;
		else
			sum -= cur;
	}

	return r - sum;
}
```

Độ phức tạp tiệm cận của lời giải là $O (\sqrt{n})$.

### Số lượng số nguyên trong một đoạn chia hết cho ít nhất một số đã cho

Cho $n$ số $a_i$ và một số $r$. Cần đếm số số nguyên trong đoạn $[1; r]$ chia hết cho ít nhất một trong các $a_i$.

Thuật toán gần như giống hệt bài trước — xây dựng công thức bao hàm – loại trừ trên các số $a_i$, tức mỗi hạng tử trong công thức là số lượng số chia hết cho một tập con đã cho của các $a_i$ (hay nói cách khác, chia hết cho [bội chung nhỏ nhất](../algebra/euclid-algorithm.md) của chúng).

Ta duyệt tất cả $2^n$ tập con của các số $a_i$, dùng $O(n \log r)$ phép toán để tìm bội chung nhỏ nhất của chúng, rồi cộng hoặc trừ số bội tương ứng trong đoạn. Độ phức tạp là $O (2^n\cdot n\cdot \log r)$.

### Số xâu thỏa một mẫu đã cho

Xét $n$ mẫu xâu có cùng độ dài, chỉ gồm các chữ cái ($a...z$) hoặc dấu hỏi. Ngoài ra cho một số $k$. Một xâu khớp với một mẫu nếu có cùng độ dài với mẫu và ở mỗi vị trí, hoặc hai ký tự tương ứng bằng nhau, hoặc ký tự trong mẫu là dấu hỏi. Bài toán là đếm số xâu khớp đúng $k$ mẫu (bài thứ nhất) và ít nhất $k$ mẫu (bài thứ hai).

Trước hết, ta dễ dàng đếm số xâu đồng thời thỏa tất cả các mẫu đã chỉ định. Chỉ cần "chồng" các mẫu lên nhau: duyệt từng vị trí ("ô") và xét ký tự tại vị trí đó trên mọi mẫu. Nếu mọi mẫu đều có dấu hỏi ở vị trí này, ký tự có thể là bất kỳ chữ nào từ $a$ tới $z$. Ngược lại, ký tự tại vị trí này được xác định duy nhất bởi các mẫu không chứa dấu hỏi.

Bây giờ giải phiên bản thứ nhất: xâu phải thỏa đúng $k$ mẫu.

Duyệt và cố định một tập con cụ thể $X$ của tập các mẫu, gồm $k$ mẫu. Ta cần đếm số xâu thỏa tập mẫu này và **chỉ** thỏa nó, tức không thỏa bất kỳ mẫu nào khác. Ta dùng nguyên lý bao hàm – loại trừ theo một cách hơi khác: cộng trên mọi siêu tập $Y$ (các tập con của tập mẫu ban đầu có chứa $X$), rồi lần lượt cộng hoặc trừ số xâu tương ứng khỏi đáp án hiện tại:

$$ ans(X) = \sum_{Y \supseteq X} (-1)^{|Y|-k} \cdot f(Y) $$

Trong đó $f(Y)$ là số xâu khớp với $Y$ (ít nhất là toàn bộ $Y$).

(Nếu khó hình dung, hãy thử vẽ biểu đồ Venn.)

Cộng trên mọi $ans(X)$ sẽ cho đáp án cuối cùng:

$$ ans = \sum_{X ~ : ~ |X| = k} ans(X) $$

Tuy nhiên, độ phức tạp của lời giải này là $O(3^k \cdot k)$. Để cải thiện, lưu ý rằng các phép tính $ans(X)$ khác nhau thường dùng chung rất nhiều tập $Y$.

Ta đảo thứ tự cộng trong công thức bao hàm – loại trừ và cộng theo các tập $Y$. Khi đó có thể thấy cùng một tập $Y$ được tính trong $ans(X)$ của $\binom{|Y|}{k}$ tập với cùng dấu $(-1)^{|Y| - k}$.

$$ ans = \sum_{Y ~ : ~ |Y| \ge k} (-1)^{|Y|-k} \cdot \binom{|Y|}{k} \cdot f(Y) $$

Lúc này lời giải có độ phức tạp $O(2^k \cdot k)$.

Ta tiếp tục giải phiên bản thứ hai: tìm số xâu khớp **ít nhất** $k$ mẫu.

Dĩ nhiên, có thể dùng lời giải của phiên bản thứ nhất rồi cộng đáp án cho mọi kích thước tập lớn hơn $k$. Tuy nhiên, trong bài này một tập |Y| được xét trong công thức cho mọi tập có kích thước $\ge k$ nằm trong $Y$. Vì vậy, phần biểu thức nhân với $f(Y)$ có thể viết thành:


$$ (-1)^{|Y|-k} \cdot \binom{|Y|}{k} + (-1)^{|Y|-k-1} \cdot \binom{|Y|}{k+1} + (-1)^{|Y|-k-2} \cdot \binom{|Y|}{k+2} + \cdots + (-1)^{|Y|-|Y|} \cdot \binom{|Y|}{|Y|} $$

Theo công thức quen thuộc trong sách của Graham (Graham, Knuth, Patashnik. "Concrete mathematics" [1998] ) về [hệ số nhị thức](binomial-coefficients.md):

$$ \sum_{k=0}^m (-1)^k \cdot \binom{n}{k} = (-1)^m \cdot \binom{n-1}{m} $$

Áp dụng ở đây, toàn bộ tổng hệ số nhị thức được rút gọn thành:

$$ (-1)^{|Y|-k} \cdot \binom{|Y|-1}{|Y|-k} $$

Vì vậy, bài này cũng có lời giải với độ phức tạp $O(2^k \cdot k)$:

$$ ans = \sum_{Y ~ : ~ |Y| \ge k} (-1)^{|Y|-k} \cdot \binom{|Y|-1}{|Y|-k} \cdot f(Y) $$

**Ghi chú bản dịch:** Ở tiểu mục này, đầu bài dùng n là số mẫu và k là số mẫu cần khớp, nhưng các dòng độ phức tạp của nguồn lại dùng k như kích thước toàn bộ tập mẫu. Theo các vòng duyệt mô tả trong chính bài, các cận độ phức tạp này phải phụ thuộc vào n (ví dụ dạng $O(2^n\cdot n)$ sau khi đảo tổng), không phải chỉ vào k. Bản dịch giữ nguyên các biểu thức của nguồn hiện tại; vấn đề này đã được gửi đề xuất sửa ở bản tiếng Anh.

### Số cách đi từ một ô tới một ô khác

Cho một bảng $n \times m$ có $k$ ô là tường không thể đi qua. Robot ban đầu ở ô $(1,1)$ (góc dưới trái), chỉ được đi sang phải hoặc đi lên và cuối cùng phải tới ô $(n,m)$ mà không đi qua chướng ngại vật. Cần đếm số cách đi.

Giả sử $n$ và $m$ rất lớn (chẳng hạn $10^9$), còn $k$ nhỏ (khoảng $100$).

Trước hết, sắp xếp các chướng ngại vật theo tọa độ $x$, nếu bằng nhau thì theo tọa độ $y$.

Ta cũng cần biết cách giải bài toán khi không có chướng ngại vật, tức đếm số cách đi từ một ô tới ô khác. Theo một trục ta cần đi qua $x$ ô, theo trục kia là $y$ ô. Từ tổ hợp cơ bản, ta có công thức bằng [hệ số nhị thức](binomial-coefficients.md):

$$\binom{x+y}{x}$$

Để đếm số cách đi từ một ô tới ô khác mà tránh mọi chướng ngại vật, có thể dùng bao hàm – loại trừ cho bài toán bù: đếm số đường đi giẫm lên một tập con chướng ngại vật rồi trừ khỏi tổng số đường đi.

Khi duyệt một tập con các chướng ngại vật mà đường đi sẽ giẫm lên, ta chỉ cần nhân số đường đi từ ô xuất phát tới chướng ngại vật được chọn đầu tiên, từ chướng ngại vật thứ nhất tới thứ hai, v.v., rồi cộng hoặc trừ giá trị này khỏi đáp án theo công thức bao hàm – loại trừ chuẩn.

Tuy nhiên, cách này vẫn có độ phức tạp không đa thức $O(2^k \cdot k)$.

Sau đây là một lời giải đa thức:

Ta dùng quy hoạch động. Để tiện, thêm (1,1) vào đầu và (n,m) vào cuối mảng chướng ngại vật. Tính $d[i]$ — số cách đi từ điểm xuất phát (phần tử thứ $0-th$) tới điểm thứ $i-th$ mà không đi qua bất kỳ chướng ngại vật nào khác (ngoại trừ chính $i$). Ta tính giá trị này cho mọi ô chướng ngại vật và cả ô đích.

Tạm quên các chướng ngại vật và chỉ đếm số đường đi từ ô $0$ tới $i$. Ta cần xét các đường đi "xấu", tức các đường đi đi qua chướng ngại vật, rồi trừ chúng khỏi tổng số cách đi từ $0$ tới $i$.

Xét một chướng ngại vật $t$ nằm giữa $0$ và $i$ ($0 < t < i$) mà ta có thể đi qua. Số đường đi từ $0$ tới $i$ đi qua $t$ và có $t$ là **chướng ngại vật đầu tiên giữa điểm xuất phát và $i$** bằng $d[t]$ nhân với số đường đi tùy ý từ $t$ tới $i$. Cộng giá trị này cho mọi $t$ giữa $0$ và $i$ ta thu được số đường đi "xấu".

Có thể tính mỗi $d[i]$ trong $O(k)$ cho $O(k)$ chướng ngại vật, nên lời giải có độ phức tạp $O(k^2)$.

### Số bộ bốn nguyên tố cùng nhau

Cho $n$ số: $a_1, a_2, \ldots, a_n$. Cần đếm số cách chọn bốn số sao cho ước chung lớn nhất của cả bốn bằng một.

Ta giải bài toán bù — đếm số bộ bốn "xấu", tức các bộ bốn mà mọi số đều chia hết cho một số $d > 1$.

Ta dùng nguyên lý bao hàm – loại trừ khi cộng trên mọi nhóm bốn số chia hết cho một ước $d$.

$$ans = \sum_{d \ge 2} (-1)^{deg(d)-1} \cdot f(d)$$

trong đó $deg(d)$ là số số nguyên tố trong phân tích thừa số của $d$, còn $f(d)$ là số bộ bốn chia hết cho $d$.

**Ghi chú bản dịch:** Công thức nguồn ở trên chỉ đúng khi tổng chạy trên các số d không chia hết cho bình phương của bất kỳ số nguyên tố nào, tức d là tích của các số nguyên tố phân biệt. Các lũy thừa như 4 hoặc 8 không tạo thêm một giao mới trong bao hàm – loại trừ. Bản dịch giữ nguyên công thức nguồn hiện tại; vấn đề này đã được gửi đề xuất sửa ở bản tiếng Anh.

Để tính $f(d)$, chỉ cần đếm số bội của $d$ (như ở bài trước) rồi dùng [hệ số nhị thức](binomial-coefficients.md) để đếm số cách chọn bốn số trong đó.

Vì vậy, theo công thức bao hàm – loại trừ, ta cộng số nhóm bốn chia hết cho một số nguyên tố, trừ số bộ bốn chia hết cho tích của hai số nguyên tố, cộng số bộ bốn chia hết cho tích của ba số nguyên tố, v.v.


### Số bộ ba harmonic

Cho một số $n \le 10^6$. Cần đếm số bộ ba $2 \le a < b < c \le n$ thỏa một trong hai điều kiện:

* hoặc ${\rm gcd}(a,b) = {\rm gcd}(a,c) = {\rm gcd}(b,c) = 1$,
* hoặc ${\rm gcd}(a,b) > 1, {\rm gcd}(a,c) > 1, {\rm gcd}(b,c) > 1$.

Trước hết, chuyển ngay sang bài toán bù — đếm số bộ ba không harmonic.

Tiếp theo, lưu ý rằng mọi bộ ba không harmonic gồm một cặp nguyên tố cùng nhau và một số thứ ba không nguyên tố cùng nhau với ít nhất một phần tử của cặp.

Vì vậy, số bộ ba không harmonic chứa $i$ bằng số số nguyên từ $2$ tới $n$ nguyên tố cùng nhau với $i$ nhân với số số nguyên không nguyên tố cùng nhau với $i$.

Hoặc $gcd(a,b) = 1 \wedge gcd(a,c) > 1 \wedge gcd(b,c) > 1$

hoặc $gcd(a,b) = 1 \wedge gcd(a,c) = 1 \wedge gcd(b,c) > 1$

Trong cả hai trường hợp, mỗi bộ ba bị tính hai lần. Trường hợp thứ nhất được tính khi $i = a$ và khi $i = b$. Trường hợp thứ hai được tính khi $i = b$ và khi $i = c$. Do đó, để tính số bộ ba không harmonic, ta cộng biểu thức trên cho mọi $i$ từ $2$ tới $n$ rồi chia cho $2$.

Bây giờ chỉ còn bài toán đếm số phần tử nguyên tố cùng nhau với $i$ trong đoạn $[2;n]$. Dù bài toán này đã xuất hiện ở trên, lời giải trước đó không phù hợp ở đây — ta sẽ phải phân tích từng số nguyên từ $2$ tới $n$ rồi duyệt mọi tập con các thừa số nguyên tố của nó.

Có thể giải nhanh hơn bằng biến thể sau của sàng Eratosthenes:

1. Trước hết, tìm mọi số trong đoạn $[2;n]$ mà phân tích thừa số nguyên tố không chứa một thừa số nguyên tố hai lần. Với mỗi số như vậy, ta cũng cần biết nó có bao nhiêu thừa số.
    * Duy trì mảng $deg[i]$ lưu số số nguyên tố trong phân tích của $i$, và mảng $good[i]$ đánh dấu $i$ có chứa mỗi thừa số nhiều nhất một lần ($good[i] = 1$) hay không ($good[i] = 0$). Khi duyệt từ $2$ tới $n$, nếu gặp một số có $deg$ bằng $0$ thì đó là số nguyên tố và đặt $deg$ của nó bằng $1$.
    * Trong sàng Eratosthenes, duyệt $i$ từ $2$ tới $n$. Khi xử lý một số nguyên tố, đi qua mọi bội của nó và tăng $deg[]$. Nếu một bội đồng thời là bội của bình phương $i$, đặt $good$ thành false.

2. Tiếp theo, cần tính đáp án cho mọi $i$ từ $2$ tới $n$, tức mảng $cnt[]$ — số lượng số nguyên không nguyên tố cùng nhau với $i$.
    * Để làm vậy, nhớ lại công thức bao hàm – loại trừ hoạt động như thế nào — ở đây ta cài đặt cùng ý tưởng nhưng đảo chiều: duyệt một thành phần (tích của các số nguyên tố trong phân tích) rồi cộng hoặc trừ hạng tử tương ứng vào công thức bao hàm – loại trừ của mỗi bội của nó.
    * Giả sử đang xử lý một số $i$ có $good[i] = true$, tức nó tham gia công thức bao hàm – loại trừ. Duyệt mọi số là bội của $i$, rồi cộng hoặc trừ $\lfloor N/i \rfloor$ vào $cnt[]$ của chúng (dấu phụ thuộc vào $deg[i]$: nếu $deg[i]$ lẻ thì cộng, ngược lại thì trừ).

**Ghi chú bản dịch:** Ở gạch đầu dòng cuối, nguồn dùng ký hiệu N trong biểu thức lấy phần nguyên, trong khi toàn bộ tiểu mục và đoạn mã bên dưới dùng n. Đây là lỗi ký hiệu; bản dịch giữ nguyên biểu thức nguồn hiện tại và vấn đề này đã được gửi đề xuất sửa ở bản tiếng Anh.

Dưới đây là cài đặt C++:

```cpp
int n;
bool good[MAXN];
int deg[MAXN], cnt[MAXN];

long long solve() {
	memset (good, 1, sizeof good);
	memset (deg, 0, sizeof deg);
	memset (cnt, 0, sizeof cnt);

	long long ans_bad = 0;
	for (int i=2; i<=n; ++i) {
		if (good[i]) {
			if (deg[i] == 0)  deg[i] = 1;
			for (int j=1; i*j<=n; ++j) {
				if (j > 1 && deg[i] == 1)
					if (j % i == 0)
						good[i*j] = false;
					else
						++deg[i*j];
				cnt[i*j] += (n / i) * (deg[i]%2==1 ? +1 : -1);
			}
		}
		ans_bad += (cnt[i] - 1) * 1ll * (n-1 - cnt[i]);
	}

	return (n-1) * 1ll * (n-2) * (n-3) / 6 - ans_bad / 2;
}
```

Độ phức tạp của lời giải là $O(n \log n)$, vì với gần như mọi số không vượt quá $n$ ta thực hiện $n/i$ lượt trong vòng lặp lồng nhau.

### Số hoán vị không có điểm cố định (derangement)

Chứng minh rằng số hoán vị độ dài $n$ không có điểm cố định (tức không có số $i$ nào nằm ở vị trí $i$ — còn gọi là derangement) bằng:

$$n! - \binom{n}{1} \cdot (n-1)! + \binom{n}{2} \cdot (n-2)! - \binom{n}{3} \cdot (n-3)! + \cdots \pm \binom{n}{n} \cdot (n-n)! $$

và xấp xỉ bằng:

$$ \frac{ n! }{ e } $$

(nếu làm tròn biểu thức này tới số nguyên gần nhất, ta nhận được đúng số hoán vị không có điểm cố định).

Ký hiệu $A_k$ là tập các hoán vị độ dài $n$ có điểm cố định tại vị trí $k$ ($1 \le k \le n$), tức phần tử $k$ nằm ở vị trí $k$.

Ta dùng công thức bao hàm – loại trừ để đếm số hoán vị có ít nhất một điểm cố định. Để làm vậy, cần tính kích thước giao của các tập $A_i$:

$$\begin{eqnarray}
\left| A_p \right| &=& (n-1)!\ , \\
\left| A_p \cap A_q \right| &=& (n-2)!\ , \\
\left| A_p \cap A_q \cap A_r \right| &=& (n-3)!\ , \\
\cdots ,
\end{eqnarray}$$

bởi nếu biết số điểm cố định bằng $x$, ta đã biết vị trí của $x$ phần tử trong hoán vị, còn $(n-x)$ phần tử khác có thể được sắp tùy ý.

Thay vào công thức bao hàm – loại trừ, đồng thời số cách chọn một tập con kích thước $x$ từ $n$ phần tử là $\binom{n}{x}$, ta thu được công thức cho số hoán vị có ít nhất một điểm cố định:

$$\binom{n}{1} \cdot (n-1)! - \binom{n}{2} \cdot (n-2)! + \binom{n}{3} \cdot (n-3)! - \cdots \pm \binom{n}{n} \cdot (n-n)! $$

Do đó, số hoán vị không có điểm cố định bằng:

$$n! - \binom{n}{1} \cdot (n-1)! + \binom{n}{2} \cdot (n-2)! - \binom{n}{3} \cdot (n-3)! + \cdots \pm \binom{n}{n} \cdot (n-n)! $$

Rút gọn biểu thức này, ta thu được **biểu thức chính xác và gần đúng cho số hoán vị không có điểm cố định**:

$$ n! \left( 1 - \frac{1}{1!} + \frac{1}{2!} - \frac{1}{3!} + \cdots \pm \frac{1}{n!} \right ) \approx \frac{n!}{e} $$

(vì tổng trong ngoặc là $n+1$ hạng đầu của khai triển Taylor của $e^{-1}$).

Đáng chú ý, một bài toán tương tự cũng có thể giải theo cách này: yêu cầu các điểm cố định không nằm trong $m$ phần tử đầu tiên của hoán vị (thay vì không nằm ở bất kỳ vị trí nào như bài vừa giải). Công thức thu được giống công thức chính xác ở trên, nhưng tổng chỉ chạy đến $k$ thay vì $n$.

**Ghi chú bản dịch:** Ở câu trên, nguồn đặt tham số là m nhưng sau đó lại nói tổng chạy đến k; k không được định nghĩa trong biến thể này. Với m vị trí bị cấm làm điểm cố định, bao hàm – loại trừ phải chạy trên m biến cố tương ứng, nên giới hạn đúng là m. Bản dịch giữ nguyên cách viết của nguồn hiện tại; vấn đề này đã được gửi đề xuất sửa ở bản tiếng Anh.

## Bài tập luyện tập

Danh sách các bài có thể giải bằng nguyên lý bao hàm – loại trừ:

* [UVA #10325 "The Lottery" [difficulty: low]](http://uva.onlinejudge.org/index.php?option=onlinejudge&page=show_problem&problem=1266)
* [UVA #11806 "Cheerleaders" [difficulty: low]](http://uva.onlinejudge.org/index.php?option=com_onlinejudge&Itemid=8&page=show_problem&problem=2906)
* [TopCoder SRM 477 "CarelessSecretary" [difficulty: low]](http://www.topcoder.com/stat?c=problem_statement&pm=10875)
* [TopCoder TCHS 16 "Divisibility" [difficulty: low]](http://community.topcoder.com/stat?c=problem_statement&pm=6658&rd=10068)
* [SPOJ #6285 NGM2 , "Another Game With Numbers" [difficulty: low]](http://www.spoj.com/problems/NGM2/)
* [TopCoder SRM 382 "CharmingTicketsEasy" [difficulty: medium]](http://community.topcoder.com/stat?c=problem_statement&pm=8470)
* [TopCoder SRM 390 "SetOfPatterns" [difficulty: medium]](http://www.topcoder.com/stat?c=problem_statement&pm=8307)
* [TopCoder SRM 176 "Deranged" [difficulty: medium]](http://community.topcoder.com/stat?c=problem_statement&pm=2013)
* [TopCoder SRM 457 "TheHexagonsDivOne" [difficulty: medium]](http://community.topcoder.com/stat?c=problem_statement&pm=10702&rd=14144&rm=303184&cr=22697599)
* [SPOJ #4191 MSKYCODE "Sky Code" [difficulty: medium]](http://www.spoj.com/problems/MSKYCODE/)
* [SPOJ #4168 SQFREE "Square-free integers" [difficulty: medium]](http://www.spoj.com/problems/SQFREE/)
* [CodeChef "Count Relations" [difficulty: medium]](http://www.codechef.com/JAN11/problems/COUNTREL/)
* [SPOJ - Almost Prime Numbers Again](http://www.spoj.com/problems/KPRIMESB/)
* [SPOJ - Find number of Pair of Friends](http://www.spoj.com/problems/IITKWPCH/)
* [SPOJ - Balanced Cow Subsets](http://www.spoj.com/problems/SUBSET/)
* [SPOJ - EASY MATH [difficulty: medium]](http://www.spoj.com/problems/EASYMATH/)
* [SPOJ - MOMOS - FEASTOFPIGS [difficulty: easy]](https://www.spoj.com/problems/MOMOS/)
* [Atcoder - Grid 2 [difficulty: easy]](https://atcoder.jp/contests/dp/tasks/dp_y/)
* [Codeforces - Count GCD](https://codeforces.com/contest/1750/problem/D)