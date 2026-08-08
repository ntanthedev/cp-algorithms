---
tags:
  - Original
translation:
  source: dynamic_programming/intro-to-dp.md
  source_commit: e3b2772b04dd5a282e889c9d794e7a0a6b3bda34
  status: draft
  last_synced: 2026-08-08
---

# Nhập môn Quy hoạch động

Cốt lõi của quy hoạch động là tránh tính toán lặp lại. Các bài toán quy hoạch động thường có thể được giải một cách tự nhiên bằng đệ quy. Trong những trường hợp đó, cách dễ nhất thường là viết lời giải đệ quy trước, rồi lưu lại các trạng thái đã tính vào một bảng tra cứu. Cách làm này được gọi là quy hoạch động từ trên xuống (top-down) với ghi nhớ (memoization), hay thường gọi là **đệ quy có nhớ**. Lưu ý từ tiếng Anh là "memoization" (giống như ghi vào một tờ memo), không phải "memorization".

Một trong những ví dụ cơ bản và kinh điển nhất là dãy Fibonacci. Công thức đệ quy của nó là $f(n) = f(n-1) + f(n-2)$ với $n \ge 2$, $f(0)=0$ và $f(1)=1$. Trong C++, ta có thể viết:

```cpp
int f(int n) {
    if (n == 0) return 0;
    if (n == 1) return 1;
    return f(n - 1) + f(n - 2);
}
```

Thời gian chạy của hàm đệ quy này là hàm mũ — xấp xỉ $O(2^n)$, bởi một lời gọi hàm ( $f(n)$ ) lại sinh ra 2 lời gọi có kích thước gần tương tự ($f(n-1)$ và $f(n-2)$ ).

## Tăng tốc Fibonacci bằng Quy hoạch động (Ghi nhớ)

Hàm đệ quy hiện tại giải Fibonacci trong thời gian hàm mũ. Điều này có nghĩa là ta chỉ xử lý được các giá trị đầu vào nhỏ trước khi lượng tính toán trở nên quá lớn. Chẳng hạn, $f(29)$ dẫn tới *hơn 1 triệu* lời gọi hàm!

Để tăng tốc, ta nhận thấy số bài toán con chỉ là $O(n)$. Cụ thể, để tính $f(n)$ ta chỉ cần biết $f(n-1),f(n-2), \dots ,f(0)$. Vì vậy, thay vì tính lại các bài toán con này nhiều lần, ta giải mỗi bài toán đúng một lần rồi lưu kết quả vào bảng tra cứu. Các lời gọi sau đó sẽ dùng bảng này và trả kết quả ngay, nhờ đó loại bỏ lượng công việc hàm mũ!

Mỗi lời gọi đệ quy sẽ kiểm tra bảng tra cứu để xem giá trị đã được tính hay chưa. Việc này mất $O(1)$ thời gian. Nếu đã tính, ta trả ngay kết quả; nếu chưa, ta tính hàm như bình thường. Tổng thời gian chạy là $O(n)$. Đây là một cải thiện rất lớn so với thuật toán thời gian hàm mũ ban đầu!

```cpp
const int MAXN = 100;
bool found[MAXN];
int memo[MAXN];

int f(int n) {
    if (found[n]) return memo[n];
    if (n == 0) return 0;
    if (n == 1) return 1;

    found[n] = true;
    return memo[n] = f(n - 1) + f(n - 2);
}
```

Với hàm đệ quy có nhớ mới, $f(29)$ trước đây cần *hơn 1 triệu lời gọi*, còn giờ chỉ cần *57* lời gọi — ít hơn gần *20.000 lần*! Trớ trêu là lúc này giới hạn lại nằm ở kiểu dữ liệu. $f(46)$ là số Fibonacci cuối cùng còn biểu diễn được bằng số nguyên có dấu 32 bit.

Thông thường, nếu có thể, ta cố gắng lưu trạng thái trong mảng vì thời gian tra cứu là $O(1)$ với chi phí phụ rất nhỏ. Tuy nhiên, tổng quát hơn, ta có thể lưu trạng thái theo bất kỳ cách nào phù hợp. Một số lựa chọn khác là cây tìm kiếm nhị phân (`map` trong C++) hoặc bảng băm (`unordered_map` trong C++).

Ví dụ với bảng băm:

```cpp
unordered_map<int, int> memo;
int f(int n) {
    if (memo.count(n)) return memo[n];
    if (n == 0) return 0;
    if (n == 1) return 1;

    return memo[n] = f(n - 1) + f(n - 2);
}
```

Hoặc tương tự với cây tìm kiếm nhị phân:

```cpp
map<int, int> memo;
int f(int n) {
    if (memo.count(n)) return memo[n];
    if (n == 0) return 0;
    if (n == 1) return 1;

    return memo[n] = f(n - 1) + f(n - 2);
}
```

Trong một hàm đệ quy có nhớ thông thường, cả hai cách này hầu như luôn chậm hơn phiên bản dùng mảng.
Các cách lưu trạng thái thay thế chủ yếu hữu ích khi trạng thái cần chứa vector hoặc xâu.

Một cách đơn giản để phân tích thời gian chạy của hàm đệ quy có nhớ là:

$$\text{work per subproblem} * \text{number of subproblems}$$

Nếu dùng cây tìm kiếm nhị phân (map trong C++) để lưu trạng thái, độ phức tạp thực tế sẽ là $O(n \log n)$ vì mỗi lần tra cứu và chèn tốn $O(\log n)$, và với $O(n)$ bài toán con khác nhau ta có tổng thời gian $O(n \log n)$.

Cách tiếp cận này được gọi là **từ trên xuống**, bởi ta gọi hàm với giá trị cần truy vấn rồi phép tính đi từ phía trên (giá trị được hỏi) xuống phía dưới (các trường hợp cơ sở của đệ quy), đồng thời dùng ghi nhớ để đi tắt qua các trạng thái đã biết.

## Quy hoạch động từ dưới lên

Cho tới đây, ta mới chỉ thấy quy hoạch động từ trên xuống với ghi nhớ. Tuy nhiên, bài toán cũng có thể được giải bằng quy hoạch động **từ dưới lên** (bottom-up).
Cách từ dưới lên hoàn toàn ngược với từ trên xuống: bắt đầu từ đáy (các trường hợp cơ sở của đệ quy), rồi lần lượt mở rộng tới các giá trị lớn hơn.

Để xây dựng cách từ dưới lên cho dãy Fibonacci, ta khởi tạo các trường hợp cơ sở trong một mảng. Sau đó chỉ cần áp dụng trực tiếp công thức truy hồi lên mảng:

```cpp
const int MAXN = 100;
int fib[MAXN];

int f(int n) {
    fib[0] = 0;
    fib[1] = 1;
    for (int i = 2; i <= n; i++) fib[i] = fib[i - 1] + fib[i - 2];

    return fib[n];
}
```

Dĩ nhiên, cách viết trên hơi thừa thãi vì hai lý do:
Thứ nhất, ta làm lại công việc cũ nếu gọi hàm nhiều hơn một lần.
Thứ hai, để tính phần tử hiện tại ta chỉ cần hai giá trị trước đó. Vì vậy có thể giảm bộ nhớ từ $O(n)$ xuống $O(1)$.

Một lời giải Fibonacci từ dưới lên dùng $O(1)$ bộ nhớ có thể viết như sau:

```cpp
const int MAX_SAVE = 3;
int fib[MAX_SAVE];

int f(int n) {
    fib[0] = 0;
    fib[1] = 1;
    for (int i = 2; i <= n; i++)
        fib[i % MAX_SAVE] = fib[(i - 1) % MAX_SAVE] + fib[(i - 2) % MAX_SAVE];

    return fib[n % MAX_SAVE];
}
```

Lưu ý rằng ta đã đổi hằng số từ `MAXN` thành `MAX_SAVE`. Lý do là tổng số phần tử cần truy cập chỉ còn 3. Con số này không tăng theo kích thước đầu vào nên theo định nghĩa, bộ nhớ là $O(1)$. Ngoài ra, ta dùng một mẹo quen thuộc (phép lấy dư) để chỉ duy trì những giá trị thực sự cần thiết.

Vậy là đủ cho phần cơ bản của quy hoạch động: **đừng làm lại công việc mà ta đã làm trước đó**.

Một trong những cách hiệu quả để tiến bộ với quy hoạch động là học các bài toán kinh điển.

## Các bài toán Quy hoạch động kinh điển
| Tên                                           | Mô tả/Ví dụ                                                                                                                                                                                                            |
| ---------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| [0-1 Knapsack](../dynamic_programming/knapsack.md)                                   | Cho $N$ vật có trọng lượng $w_i$, giá trị $v_i$ và sức chứa tối đa $W$. Giá trị lớn nhất $\sum_{i=1}^{k} v_i$ có thể đạt được khi chọn một tập con gồm $k$ vật ($1 \le k \le N$) và vẫn bảo đảm $\sum_{i=1}^{k} w_i \le W$ là bao nhiêu?                  |
| Subset Sum                                     | Cho $N$ số nguyên và $T$, hãy xác định có tồn tại một tập con của tập đã cho sao cho tổng các phần tử bằng $T$ hay không.                                                                                                         |
| [Longest Increasing Subsequence (LIS)](../dynamic_programming/longest_increasing_subsequence.md)           | Cho một mảng gồm $N$ số nguyên. Hãy tìm LIS của mảng, tức một dãy con mà mỗi phần tử đều lớn hơn phần tử đứng trước nó.                                                       |
| Counting Paths in a 2D Array                   | Cho $N$ và $M$, đếm mọi đường đi phân biệt từ $(1,1)$ tới $(N, M)$, trong đó mỗi bước chỉ được đi từ $(i,j)$ tới $(i+1,j)$ hoặc $(i,j+1)$.                                                                               |
| Longest Common Subsequence                     | Cho hai xâu $s$ và $t$. Tìm độ dài xâu dài nhất là dãy con của cả $s$ và $t$.                                                                                                            |
| Longest Path in a Directed Acyclic Graph (DAG) | Tìm đường đi dài nhất trong đồ thị có hướng không chu trình (DAG).                                                                                                                                                                      |
| Longest Palindromic Subsequence                | Tìm dãy con đối xứng dài nhất (LPS) của một xâu đã cho.                                                                                                                                                           |
| Rod Cutting                                    | Cho một thanh dài $n$ đơn vị và mảng số nguyên cuts, trong đó cuts[i] là một vị trí cần cắt. Chi phí của một lần cắt bằng độ dài đoạn thanh đang bị cắt. Hãy tìm tổng chi phí nhỏ nhất để thực hiện các vết cắt. |
| Edit Distance                                  | Khoảng cách chỉnh sửa giữa hai xâu là số phép toán ít nhất cần để biến xâu này thành xâu kia. Các phép toán gồm ["Add", "Remove", "Replace"]                                                         |

## Chủ đề liên quan
* [Quy hoạch động bitmask](../dynamic_programming/profile-dynamics.md)
* Quy hoạch động chữ số
* Quy hoạch động trên cây

Dĩ nhiên, mẹo quan trọng nhất vẫn là luyện tập.

## Bài tập luyện tập
* [LeetCode - 1137. N-th Tribonacci Number](https://leetcode.com/problems/n-th-tribonacci-number/description/)
* [LeetCode - 118. Pascal's Triangle](https://leetcode.com/problems/pascals-triangle/description/)
* [LeetCode - 1025. Divisor Game](https://leetcode.com/problems/divisor-game/description/)
* [Codeforces - Vacations](https://codeforces.com/problemset/problem/699/C)
* [Codeforces - Hard problem](https://codeforces.com/problemset/problem/706/C)
* [Codeforces - Zuma](https://codeforces.com/problemset/problem/607/b)
* [LeetCode - 221. Maximal Square](https://leetcode.com/problems/maximal-square/description/)
* [LeetCode - 1039. Minimum Score Triangulation of Polygon](https://leetcode.com/problems/minimum-score-triangulation-of-polygon/description/)

## Các cuộc thi về DP
* [Atcoder - Educational DP Contest](https://atcoder.jp/contests/dp/tasks)
* [CSES - Dynamic Programming](https://cses.fi/problemset/list/)
