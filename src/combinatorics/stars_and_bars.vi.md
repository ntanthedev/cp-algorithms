---
tags:
  - Original
translation:
  source: combinatorics/stars_and_bars.md
  source_commit: a8e5c395f96e7fc06ae4a06d3798e50706644414
  status: draft
  last_synced: 2026-09-30
---

# Sao và vạch (Stars and Bars)

Sao và vạch (Stars and Bars) là một kỹ thuật toán học dùng để giải một số bài toán tổ hợp.
Kỹ thuật này thường xuất hiện khi cần đếm số cách chia các vật giống hệt nhau thành các nhóm.

## Định lý

Số cách đặt $n$ vật giống hệt nhau vào $k$ hộp được gắn nhãn là

$$\binom{n + k - 1}{n}.$$

Chứng minh dựa trên việc biểu diễn các vật bằng các ngôi sao và phân cách các hộp bằng những vạch (vì thế có tên gọi này).
Chẳng hạn, ta có thể dùng $\bigstar | \bigstar \bigstar |~| \bigstar \bigstar$ để biểu diễn tình huống sau:
hộp thứ nhất có một vật, hộp thứ hai có hai vật, hộp thứ ba rỗng và hộp cuối cùng có hai vật.
Đây là một cách chia 5 vật vào 4 hộp.

Có thể thấy mỗi cách phân chia đều được biểu diễn bằng $n$ ngôi sao và $k - 1$ vạch, đồng thời mỗi hoán vị của $n$ ngôi sao và $k - 1$ vạch cũng biểu diễn đúng một cách phân chia.
Do đó, số cách chia $n$ vật giống hệt nhau vào $k$ hộp được gắn nhãn bằng số hoán vị của $n$ ngôi sao và $k - 1$ vạch.
[Hệ số nhị thức](binomial-coefficients.md) cho ta công thức cần tìm.

## Số cách biểu diễn tổng bằng các số nguyên không âm

Bài toán này là một ứng dụng trực tiếp của định lý.

Ta cần đếm số nghiệm của phương trình

$$x_1 + x_2 + \dots + x_k = n$$

với $x_i \ge 0$.

Ta lại có thể biểu diễn một nghiệm bằng sao và vạch.
Chẳng hạn, nghiệm $1 + 3 + 0 = 4$ với $n = 4$, $k = 3$ có thể được biểu diễn bằng $\bigstar | \bigstar \bigstar \bigstar |$.

Dễ thấy đây chính là định lý sao và vạch.
Vì vậy, đáp án là $\binom{n + k - 1}{n}$.

## Số cách biểu diễn tổng bằng các số nguyên dương

Một định lý thứ hai cho ta cách diễn giải gọn cho trường hợp các số nguyên dương. Xét các nghiệm của

$$x_1 + x_2 + \dots + x_k = n$$

với $x_i \ge 1$.

Ta vẫn xét $n$ ngôi sao, nhưng lần này giữa hai ngôi sao chỉ có thể đặt nhiều nhất _một vạch_, bởi hai vạch nằm giữa hai ngôi sao sẽ biểu diễn $x_i=0$, tức là một hộp rỗng.
Có $n-1$ khoảng trống giữa các ngôi sao để đặt $k-1$ vạch, nên đáp án là $\binom{n-1}{k-1}$.

## Số cách biểu diễn tổng khi có cận dưới

Ta có thể dễ dàng mở rộng kết quả cho các tổng số nguyên với những cận dưới khác nhau.
Cụ thể, ta muốn đếm số nghiệm của phương trình

$$x_1 + x_2 + \dots + x_k = n$$

với $x_i \ge a_i$.

Sau khi đặt $x_i' := x_i - a_i$, ta nhận được phương trình biến đổi

$$(x_1' + a_i) + (x_2' + a_i) + \dots + (x_k' + a_k) = n$$

$$\Leftrightarrow ~ ~ x_1' + x_2' + \dots + x_k' = n - a_1 - a_2 - \dots - a_k$$

với $x_i' \ge 0$.
Như vậy, ta đã đưa bài toán về trường hợp đơn giản hơn với $x_i' \ge 0$ và có thể áp dụng lại định lý sao và vạch.

## Số cách biểu diễn tổng khi có cận trên

Với sự hỗ trợ của [Nguyên lý bao hàm – loại trừ](./inclusion-exclusion.md), ta cũng có thể giới hạn các số nguyên bằng cận trên.
Xem mục [Số cách biểu diễn tổng số nguyên có cận trên](./inclusion-exclusion.md#number-of-upper-bound-integer-sums) trong bài viết tương ứng.

## Bài tập thực hành

* [Codeforces - Array](https://codeforces.com/contest/57/problem/C)
* [Codeforces - Kyoya and Coloured Balls](https://codeforces.com/problemset/problem/553/A)
* [Codeforces - Colorful Bricks](https://codeforces.com/contest/1081/problem/C)
* [Codeforces - Two Arrays](https://codeforces.com/problemset/problem/1288/C)
* [Codeforces - One-Dimensional Puzzle](https://codeforces.com/contest/1931/problem/G)
