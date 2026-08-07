---
tags:
  - Translated
e_maxx_link: prime_sieve_linear
translation:
  source: algebra/prime-sieve-linear.md
  source_commit: 87deb65507552fb9ca8c3cb9dae5487c493fa646
  status: draft
  last_synced: 2026-08-07
---

# Sàng tuyến tính

Cho một số $n$, hãy tìm tất cả số nguyên tố trong đoạn $[2;n]$.

Cách chuẩn để giải bài toán này là dùng [Sàng Eratosthenes](sieve-of-eratosthenes.md). Thuật toán đó rất đơn giản, nhưng có thời gian chạy $O(n \log \log n)$.

Mặc dù đã biết nhiều thuật toán có thời gian chạy dưới tuyến tính (tức $o(n)$), thuật toán được trình bày dưới đây đáng chú ý vì tính đơn giản: nó không phức tạp hơn Sàng Eratosthenes cổ điển.

Ngoài ra, như một hệ quả phụ, thuật toán này còn tính được **phân tích thừa số của mọi số** trong đoạn $[2; n]$, điều này hữu ích trong nhiều ứng dụng thực tế.

Điểm yếu của thuật toán là dùng nhiều bộ nhớ hơn Sàng Eratosthenes cổ điển: nó cần một mảng gồm $n$ số, trong khi Sàng Eratosthenes cổ điển chỉ cần $n$ bit bộ nhớ (ít hơn 32 lần).

Vì vậy, chỉ nên dùng thuật toán này cho các giá trị cỡ $10^7$ trở xuống.

Thuật toán do Paul Pritchard đề xuất. Đây là một biến thể của Algorithm 3.3 trong (Pritchard, 1987: xem tài liệu tham khảo ở cuối bài).

## Thuật toán

Mục tiêu của ta là tính **thừa số nguyên tố nhỏ nhất** $lp [i]$ cho mọi số $i$ trong đoạn $[2; n]$.

Ngoài ra, ta cần lưu danh sách tất cả các số nguyên tố đã tìm được — gọi danh sách này là $pr []$.

Ban đầu, ta gán các giá trị $lp [i]$ bằng 0, nghĩa là tạm xem mọi số là số nguyên tố. Trong quá trình chạy thuật toán, mảng này sẽ dần được điền giá trị.

Bây giờ ta duyệt các số từ 2 đến $n$. Với số hiện tại $i$, có hai trường hợp:

- $lp[i] = 0$ - điều này có nghĩa $i$ là số nguyên tố, tức ta chưa tìm được thừa số nào nhỏ hơn của nó.  
  Vì vậy, ta gán $lp [i] = i$ và thêm $i$ vào cuối danh sách $pr[]$.

- $lp[i] \neq 0$ - điều này có nghĩa $i$ là hợp số, và thừa số nguyên tố nhỏ nhất của nó là $lp [i]$.

Trong cả hai trường hợp, ta cập nhật các giá trị của $lp []$ cho những số chia hết cho $i$. Tuy nhiên, mục tiêu là thực hiện sao cho mỗi giá trị $lp []$ chỉ được gán nhiều nhất một lần. Ta có thể làm như sau:

Xét các số $x_j = i \cdot p_j$, trong đó $p_j$ là tất cả số nguyên tố nhỏ hơn hoặc bằng $lp [i]$ (đây là lý do ta phải lưu danh sách mọi số nguyên tố).

Ta gán giá trị mới $lp [x_j] = p_j$ cho mọi số có dạng này.

Chứng minh tính đúng đắn và thời gian chạy của thuật toán được trình bày sau phần cài đặt.

## Cài đặt

```cpp
const int N = 10000000;
vector<int> lp(N+1);
vector<int> pr;
 
for (int i=2; i <= N; ++i) {
	if (lp[i] == 0) {
		lp[i] = i;
		pr.push_back(i);
	}
	for (int j = 0; i * pr[j] <= N; ++j) {
		lp[i * pr[j]] = pr[j];
		if (pr[j] == lp[i]) {
			break;
		}
	}
}
```

## Chứng minh tính đúng đắn

Ta cần chứng minh rằng thuật toán gán đúng mọi giá trị $lp []$, đồng thời mỗi giá trị chỉ được gán đúng một lần. Khi đó thuật toán có thời gian chạy tuyến tính, vì hiển nhiên tất cả thao tác còn lại đều chạy trong $O (n)$.

Nhận xét rằng mỗi số $i$ có đúng một biểu diễn dưới dạng:

$$i = lp [i] \cdot x,$$

trong đó $lp [i]$ là thừa số nguyên tố nhỏ nhất của $i$, còn số $x$ không có thừa số nguyên tố nào nhỏ hơn $lp [i]$, tức là

$$lp [i] \le lp [x].$$

Bây giờ so sánh điều này với hoạt động của thuật toán: với mỗi $x$, thuật toán thực chất duyệt qua mọi số nguyên tố mà ta có thể nhân với nó, tức tất cả số nguyên tố không vượt quá $lp [x]$, để tạo ra các số đúng theo dạng biểu diễn ở trên.

Vì vậy, thuật toán sẽ đi qua mỗi hợp số đúng một lần và gán đúng giá trị $lp []$ tại đó. Q.E.D.

## Thời gian chạy và bộ nhớ

Mặc dù thời gian chạy $O(n)$ tốt hơn $O(n \log \log n)$ của Sàng Eratosthenes cổ điển, khác biệt giữa hai thuật toán không quá lớn.
Trong thực tế, sàng tuyến tính chạy nhanh xấp xỉ một cài đặt Sàng Eratosthenes thông thường.

So với các phiên bản Sàng Eratosthenes đã được tối ưu, chẳng hạn sàng phân đoạn, nó chậm hơn đáng kể.

Xét yêu cầu bộ nhớ — một mảng $lp []$ độ dài $n$, cùng một mảng $pr []$ độ dài $\frac n {\ln n}$ — thuật toán này có vẻ kém Sàng Eratosthenes cổ điển về mọi mặt.

Tuy nhiên, ưu điểm bù lại là thuật toán tính được mảng $lp []$, nhờ đó ta có thể tìm phân tích thừa số của bất kỳ số nào trong đoạn $[2; n]$ với thời gian cùng bậc với kích thước của phân tích đó. Hơn nữa, chỉ cần thêm một mảng nữa là có thể tránh các phép chia khi tìm phân tích thừa số.

Biết sẵn phân tích thừa số của mọi số rất hữu ích trong một số bài toán, và đây là một trong số ít thuật toán cho phép tìm chúng trong thời gian tuyến tính.

## Tài liệu tham khảo

- Paul Pritchard, **Linear Prime-Number Sieves: a Family Tree**, Science of Computer Programming, vol. 9 (1987), pp.17-35.
