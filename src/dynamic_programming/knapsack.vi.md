---
tags:
  - Original
translation:
  source: dynamic_programming/knapsack.md
  source_commit: b3a017bcab9b5504ccc4c1805d1a7aeda5afd03b
  status: draft
  last_synced: 2026-08-08
---

# Bài toán cái túi (Knapsack)
Kiến thức cần có: [Nhập môn Quy hoạch động](https://cp-algorithms.com/dynamic_programming/intro-to-dp.html)

## Giới thiệu
Xét ví dụ sau:

### [[USACO07 Dec] Charm Bracelet](https://www.acmicpc.net/problem/6144) 
Có $n$ vật phân biệt và một chiếc túi có sức chứa $W$. Mỗi vật có 2 thuộc tính: trọng lượng ($w_{i}$) và giá trị ($v_{i}$).
Ta cần chọn một tập con các vật để cho vào túi sao cho tổng trọng lượng không vượt quá sức chứa $W$ và tổng giá trị là lớn nhất.

Trong ví dụ trên, mỗi vật chỉ có hai trạng thái (chọn hoặc không chọn),
tương ứng với hai giá trị nhị phân 0 và 1. Vì vậy dạng bài này được gọi là "bài toán Knapsack 0-1".

## Knapsack 0-1

### Giải thích

Trong ví dụ trên, đầu vào của bài toán gồm: trọng lượng của vật thứ $i^{th}$ là $w_{i}$, giá trị của vật thứ $i^{th}$ là $v_{i}$, và sức chứa tổng cộng của túi là $W$.

Gọi $f_{i, j}$ là trạng thái quy hoạch động lưu tổng giá trị lớn nhất mà chiếc túi sức chứa $j$ có thể đạt được khi chỉ xét $i$ vật đầu tiên.

Giả sử mọi trạng thái của $i-1$ vật đầu đã được xử lý. Với vật thứ $i^{th}$, ta có những lựa chọn nào?

- Nếu không cho vật này vào túi, sức chứa còn lại không đổi và tổng giá trị cũng không đổi. Vì vậy giá trị lớn nhất trong trường hợp này là $f_{i-1, j}$
- Nếu cho vật này vào túi, sức chứa còn lại giảm $w_{i}$ và tổng giá trị tăng $v_{i}$,
  nên giá trị lớn nhất trong trường hợp này là $f_{i-1, j-w_i} + v_i$

Từ đó ta suy ra công thức chuyển trạng thái:

$$f_{i, j} = \max(f_{i-1, j}, f_{i-1, j-w_i} + v_i)$$

Hơn nữa, vì $f_{i}$ chỉ phụ thuộc vào $f_{i-1}$, ta có thể bỏ chiều thứ nhất. Khi đó quy tắc chuyển trở thành

$$f_j \gets \max(f_j, f_{j-w_i}+v_i)$$

và phải được thực hiện theo thứ tự **giảm dần** của $j$ (để $f_{j-w_i}$ ngầm tương ứng với $f_{i-1,j-w_i}$ chứ không phải $f_{i,j-w_i}$).

**Điều quan trọng là phải hiểu quy tắc chuyển này, vì phần lớn các công thức chuyển của bài toán Knapsack đều được suy ra theo cách tương tự.**

### Cài đặt

Thuật toán trên có thể được cài đặt trong $O(nW)$ như sau:

```.c++
for (int i = 1; i <= n; i++)
  for (int j = W; j >= w[i]; j--)
    f[j] = max(f[j], f[j - w[i]] + v[i]);
```

Một lần nữa, hãy chú ý thứ tự thực hiện. Thứ tự này phải được tuân thủ nghiêm ngặt để bảo đảm bất biến sau: ngay trước khi cặp $(i, j)$ được xử lý, $f_k$ tương ứng với $f_{i,k}$ khi $k > j$, nhưng tương ứng với $f_{i-1,k}$ khi $k < j$. Nhờ đó $f_{j-w_i}$ được lấy từ bước thứ $(i-1)$ chứ không phải bước thứ $i$.

## Knapsack không giới hạn

Mô hình Knapsack không giới hạn tương tự Knapsack 0-1; điểm khác biệt duy nhất là mỗi loại vật có thể được chọn không giới hạn số lần thay vì chỉ một lần.

Ta có thể dựa trên ý tưởng của Knapsack 0-1 để định nghĩa trạng thái $f_{i, j}$: giá trị lớn nhất chiếc túi có thể đạt được với sức chứa tối đa $j$ khi dùng $i$ loại vật đầu tiên.

Cần lưu ý rằng dù định nghĩa trạng thái giống Knapsack 0-1, quy tắc chuyển trạng thái lại khác.

### Giải thích

Cách trực tiếp là, với $i$ loại vật đầu tiên, duyệt số lần lấy mỗi loại. Độ phức tạp thời gian của cách này là $O(n^2W)$.

**Ghi chú bản dịch:** Cận độ phức tạp ở câu trên của nguồn không đúng trong trường hợp tổng quát. Với mỗi trạng thái, số lần lấy vật có thể phải duyệt tới bậc $W$, nên cận tệ nhất là $O(nW^2)$. Lỗi này đã có một pull request riêng đang mở ở upstream; bản dịch vẫn giữ nguyên biểu thức của nguồn để bảo đảm đồng bộ.

Ta thu được công thức chuyển sau:

$$f_{i, j} = \max\limits_{k=0}^{\infty}(f_{i-1, j-k\cdot w_i} + k\cdot v_i)$$

Đồng thời, công thức trên có thể rút gọn thành dạng "phẳng":

$$f_{i, j} = \max(f_{i-1, j},f_{i, j-w_i} + v_i)$$

Lý do là $f_{i, j-w_i}$ đã được cập nhật từ $f_{i, j-2\cdot w_i}$, và cứ tiếp tục như vậy.

Tương tự Knapsack 0-1, ta có thể bỏ chiều thứ nhất để tối ưu bộ nhớ. Khi đó ta nhận được cùng quy tắc chuyển như Knapsack 0-1.

$$f_j \gets \max(f_j, f_{j-w_i}+v_i)$$

### Cài đặt

Thuật toán trên có thể được cài đặt trong $O(nW)$ như sau:

```.c++
for (int i = 1; i <= n; i++)
  for (int j = w[i]; j <= W; j++)
    f[j] = max(f[j], f[j - w[i]] + v[i]);
```

Dù có cùng quy tắc chuyển, đoạn mã trên lại không đúng cho Knapsack 0-1.

Quan sát kỹ đoạn mã, với vật $i$ đang được xử lý và trạng thái hiện tại $f_{i,j}$,
khi $j\geqslant w_{i}$ thì $f_{i,j}$ sẽ chịu ảnh hưởng của $f_{i,j-w_{i}}$.
Điều này tương đương với việc cho phép đưa vật $i$ vào túi nhiều lần, phù hợp với bài toán Knapsack không giới hạn chứ không phải Knapsack 0-1.

## Knapsack có giới hạn số lượng

Knapsack có giới hạn số lượng cũng là một biến thể của Knapsack 0-1. Điểm khác biệt chính là có $k_i$ bản sao của mỗi loại vật thay vì chỉ $1$.

### Giải thích

Một ý tưởng rất đơn giản là: "chọn mỗi loại vật $k_i$ lần" tương đương với việc "$k_i$ vật giống nhau được xét lần lượt từng cái". Vì vậy ta có thể chuyển bài toán về mô hình Knapsack 0-1 với công thức chuyển:

$$f_{i, j} = \max_{k=0}^{k_i}(f_{i-1,j-k\cdot w_i} + k\cdot v_i)$$

Độ phức tạp thời gian của quá trình này là $O(W\sum\limits_{i=1}^{n}k_i)$

### Tối ưu bằng phân nhóm nhị phân

Ta vẫn xét cách chuyển mô hình Knapsack có giới hạn số lượng thành Knapsack 0-1 để tối ưu. Thành phần $O(Wn)$ của độ phức tạp không thể tiếp tục được cải thiện bằng cách trên, nên ta tập trung vào thành phần $O(\sum k_i)$.

Gọi $A_{i, j}$ là vật thứ $j^{th}$ được tách ra từ loại vật thứ $i^{th}$. Trong cách trực tiếp ở trên, mọi $A_{i, j}$ với $j \leq k_i$ đều biểu diễn cùng một vật. Nguyên nhân chính khiến cách này kém hiệu quả là có quá nhiều công việc lặp lại. Chẳng hạn, việc chọn $\{A_{i, 1},A_{i, 2}\}$ và việc chọn $\{A_{i, 2}, A_{i, 3}\}$ là hoàn toàn tương đương. Vì vậy, tối ưu cách tách nhóm sẽ làm giảm đáng kể độ phức tạp.

Ta có thể phân nhóm hiệu quả hơn bằng cách dùng các nhóm có kích thước theo lũy thừa của hai.

Cụ thể, $A_{i, j}$ đại diện cho $2^j$ vật riêng lẻ ($j\in[0,\lfloor \log_2(k_i+1)\rfloor-1]$). Nếu $k_i + 1$ không phải một lũy thừa nguyên của $2$, ta dùng thêm một nhóm có kích thước $k_i-(2^{\lfloor \log_2(k_i+1)\rfloor}-1)$ để bù phần còn lại.

Với cách tách trên, ta có thể tạo ra mọi tổng số vật $\leq k_i$ bằng cách chọn một số $A_{i, j}$. Sau khi tách từng loại vật theo cách này, chỉ cần dùng phương pháp Knapsack 0-1 để giải bài toán mới.

Tối ưu này cho độ phức tạp $O(W\sum\limits_{i=1}^{n}\log k_i)$.

### Cài đặt

```c++
index = 0;
for (int i = 1; i <= n; i++) {
  int c = 1, p, h, k;
  cin >> p >> h >> k;
  while (k > c) {
    k -= c;
    list[++index].w = c * p;
    list[index].v = c * h;
    c *= 2;
  }
  list[++index].w = p * k;
  list[index].v = h * k;
}
```

### Tối ưu bằng hàng đợi đơn điệu

Trong tối ưu này, ta muốn chuyển bài toán Knapsack thành một bài toán [hàng đợi cực đại](https://cp-algorithms.com/data_structures/stack_queue_modification.html).

Để thuận tiện khi trình bày, đặt $g_{x, y} = f_{i, x \cdot w_i + y} ,\space g'_{x, y} = f_{i-1, x \cdot w_i + y}$. Khi đó quy tắc chuyển có thể viết thành:

$$g_{x, y} = \max_{k=0}^{k_i}(g'_{x-k, y} + v_i \cdot k)$$

Tiếp theo, đặt $G_{x, y} = g'_{x, y} - v_i \cdot x$. Khi đó quy tắc chuyển có thể biểu diễn thành:

$$g_{x, y} \gets \max_{k=0}^{k_i}(G_{x-k, y}) + v_i \cdot x$$

Bài toán được đưa về dạng tối ưu hàng đợi đơn điệu kinh điển. $G_{x, y}$ có thể được tính trong $O(1)$, nên với $y$ cố định, ta có thể tính $g_{x, y}$ trong $O(\lfloor \frac{W}{w_i} \rfloor)$ thời gian.
Vì vậy, độ phức tạp để tìm toàn bộ $g_{x, y}$ là $O(\lfloor \frac{W}{w_i} \rfloor) \times O(w_i) = O(W)$.
Theo cách này, tổng độ phức tạp của thuật toán giảm xuống $O(nW)$.

## Knapsack hỗn hợp

Bài toán Knapsack hỗn hợp kết hợp ba dạng bài đã trình bày ở trên. Cụ thể, có vật chỉ được lấy một lần, có vật được lấy không giới hạn, và có vật được lấy nhiều nhất $k$ lần.

Bài toán có thể trông phức tạp, nhưng chỉ cần hiểu ý tưởng cốt lõi của các dạng Knapsack ở trên rồi kết hợp chúng lại. Mã giả của lời giải như sau:

```c++
for (each item) {
  if (0-1 knapsack)
    Apply 0-1 knapsack code;
  else if (complete knapsack)
    Apply complete knapsack code;
  else if (multiple knapsack)
    Apply multiple knapsack code;
}
```

## Bài tập luyện tập

- [Atcoder: Knapsack-1](https://atcoder.jp/contests/dp/tasks/dp_d)
- [Atcoder: Knapsack-2](https://atcoder.jp/contests/dp/tasks/dp_e)
- [LeetCode - 494. Target Sum](https://leetcode.com/problems/target-sum)
- [LeetCode - 416. Partition Equal Subset Sum](https://leetcode.com/problems/partition-equal-subset-sum)
- [LeetCode - 474. Ones and Zeroes](https://leetcode.com/problems/ones-and-zeroes)
- [CSES: Book Shop II](https://cses.fi/problemset/task/1159)
- [DMOJ: Knapsack-3](https://dmoj.ca/problem/knapsack)
- [DMOJ: Knapsack-4](https://dmoj.ca/problem/knapsack4)
