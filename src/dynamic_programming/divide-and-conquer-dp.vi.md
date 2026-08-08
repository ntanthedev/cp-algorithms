---
tags:
  - Original
translation:
  source: dynamic_programming/divide-and-conquer-dp.md
  source_commit: b0cbeff561dfec321c6f615a22bf78941ace6b5e
  status: draft
  last_synced: 2026-08-08
---

# Quy hoạch động chia để trị (Divide and Conquer DP)

Chia để trị là một kỹ thuật tối ưu quy hoạch động.

### Điều kiện áp dụng
Một số bài toán quy hoạch động có công thức truy hồi dạng sau: 

$$
dp(i, j) = \min_{0 \leq k \leq j} \\{ dp(i - 1, k - 1) + C(k, j) \\}
$$

trong đó $C(k, j)$ là hàm chi phí và $dp(i, j) = 0$ khi $j \lt 0$. 

Giả sử $0 \leq i \lt m$ và $0 \leq j \lt n$, đồng thời việc tính $C$ mất $O(1)$ thời gian. Khi đó, cách tính trực tiếp công thức truy hồi trên có độ phức tạp $O(m n^2)$. Có $m \times n$ trạng thái và mỗi trạng thái có $n$ chuyển trạng thái.

Gọi $opt(i, j)$ là giá trị $k$ làm biểu thức trên đạt giá trị nhỏ nhất. Nếu hàm chi phí thỏa mãn bất đẳng thức tứ giác, ta có thể chứng minh rằng $opt(i, j) \leq opt(i, j + 1)$ với mọi $i, j$. Tính chất này được gọi là _điều kiện đơn điệu_. Khi đó, ta có thể áp dụng quy hoạch động chia để trị. Với một $i$ cố định, "điểm chia" tối ưu không giảm khi $j$ tăng.

Nhờ vậy, ta có thể tính mọi trạng thái hiệu quả hơn. Giả sử ta đã tính $opt(i, j)$ với một $i$ và $j$ cố định. Khi đó, với mọi $j' < j$, ta biết $opt(i, j') \leq opt(i, j)$. Điều này có nghĩa là khi tính $opt(i, j')$, ta không cần xét nhiều điểm chia như trước.

Để giảm thời gian chạy, ta áp dụng tư tưởng chia để trị. Trước tiên, tính $opt(i, n / 2)$. Sau đó, tính $opt(i, n / 4)$, biết rằng nó không lớn hơn $opt(i, n / 2)$, và tính $opt(i, 3 n / 4)$, biết rằng nó không nhỏ hơn $opt(i, n / 2)$. Bằng cách đệ quy và luôn duy trì cận dưới, cận trên của $opt$, ta đạt thời gian chạy $O(m n \log n)$. Hãy xem phần cài đặt bên dưới để biết chi tiết.

Để chứng minh độ phức tạp của quá trình chia để trị, trước hết lưu ý rằng đệ quy có $O(\log{n})$ tầng. Ta sẽ chứng minh rằng mỗi tầng thực hiện $O(n)$ bước. Gọi tổng độ dài của các khoảng $\text{opt}$ (được ký hiệu bởi $optl$ và $optr$ trong mã nguồn) ở tầng thứ $k$ là $S_k$. Quan sát rằng mỗi khi một khoảng ở tầng $k$ có độ dài $x$ bị chia, tổng độ dài của các khoảng kết quả không vượt quá $x + 1$. Hơn nữa, ở tầng $k$ có nhiều nhất $2^k$ lần chia, vì vậy ta có $S_{k + 1} \leq S_k + 2^k$. Áp dụng cận này bằng quy nạp với $S_0 = n$, ta có với mỗi tầng $k$,

$$
S_k < n + 2^k \in O(n).
$$

Do đó, độ phức tạp của mỗi lần chia để trị là $O(n\log{n})$, còn độ phức tạp của toàn bộ quá trình tính DP là $O(mn\log{n})$.

## Cài đặt tổng quát

Dù cài đặt cụ thể thay đổi theo từng bài toán, dưới đây là một mẫu cài đặt khá tổng quát.
Hàm `compute` tính hàng thứ $i$ của bảng DP, lưu kết quả vào `dp_cur`, dựa trên hàng thứ $i-1$ được lưu trong `dp_before`.
Cần gọi hàm này bằng `compute(0, n-1, 0, n-1)`. Hàm `solve` tính `m` hàng và trả về kết quả.

```{.cpp file=divide_and_conquer_dp}
int m, n;
vector<long long> dp_before, dp_cur;

long long C(int i, int j);

// compute dp_cur[l], ... dp_cur[r] (inclusive)
void compute(int l, int r, int optl, int optr) {
    if (l > r)
        return;

    int mid = (l + r) >> 1;
    pair<long long, int> best = {LLONG_MAX, -1};

    for (int k = optl; k <= min(mid, optr); k++) {
        best = min(best, {(k ? dp_before[k - 1] : 0) + C(k, mid), k});
    }

    dp_cur[mid] = best.first;
    int opt = best.second;

    compute(l, mid - 1, optl, opt);
    compute(mid + 1, r, opt, optr);
}

long long solve() {
    dp_before.assign(n,0);
    dp_cur.assign(n,0);

    for (int i = 0; i < n; i++)
        dp_before[i] = C(0, i);

    for (int i = 1; i < m; i++) {
        compute(0, n - 1, 0, n - 1);
        dp_before = dp_cur;
    }

    return dp_before[n - 1];
}
```

### Những điểm cần lưu ý

Khó khăn lớn nhất của các bài quy hoạch động chia để trị là chứng minh tính đơn điệu của $opt$. Một trường hợp đặc biệt mà tính chất này đúng là khi hàm chi phí thỏa mãn bất đẳng thức tứ giác, tức $C(a, c) + C(b, d) \leq C(a, d) + C(b, c)$ với mọi $a \leq b \leq c \leq d$. 
Nhiều bài toán quy hoạch động chia để trị cũng có thể giải bằng kỹ thuật bao lồi (Convex Hull Trick) hoặc ngược lại. Biết và hiểu cả hai kỹ thuật sẽ rất hữu ích! 

## Bài tập luyện tập
- [AtCoder - Yakiniku Restaurants](https://atcoder.jp/contests/arc067/tasks/arc067_d)
- [CodeForces - Ciel and Gondolas](https://codeforces.com/contest/321/problem/E) (Cẩn thận với I/O!)
- [CodeForces - Levels And Regions](https://codeforces.com/problemset/problem/673/E)
- [CodeForces - Partition Game](https://codeforces.com/contest/1527/problem/E)
- [CodeForces - The Bakery](https://codeforces.com/problemset/problem/834/D)
- [CodeForces - Yet Another Minimization Problem](https://codeforces.com/contest/868/problem/F)
- [Codechef - CHEFAOR](https://www.codechef.com/problems/CHEFAOR)
- [CodeForces - GUARDS](https://codeforces.com/gym/103536/problem/A) (Đây chính là bài toán được dùng trong bài viết này.)
- [Hackerrank - Guardians of the Lunatics](https://www.hackerrank.com/contests/ioi-2014-practice-contest-2/challenges/guardians-lunatics-ioi14)
- [Hackerrank - Mining](https://www.hackerrank.com/contests/world-codesprint-5/challenges/mining)
- [Kattis - Money (ACM ICPC World Finals 2017)](https://open.kattis.com/problems/money)
- [SPOJ - ADAMOLD](https://www.spoj.com/problems/ADAMOLD/)
- [SPOJ - LARMY](https://www.spoj.com/problems/LARMY/)
- [SPOJ - NKLEAVES](https://www.spoj.com/problems/NKLEAVES/)
- [Timus - Bicolored Horses](https://acm.timus.ru/problem.aspx?space=1&num=1167)
- [USACO - Circular Barn](https://usaco.org/index.php?page=viewproblem2&cpid=626)
- [UVA - Arranging Heaps](https://onlinejudge.org/external/125/12524.pdf)
- [UVA - Naming Babies](https://onlinejudge.org/external/125/12594.pdf)



## Tài liệu tham khảo
- [Quora Answer by Michael Levin](https://www.quora.com/What-is-divide-and-conquer-optimization-in-dynamic-programming)
- [Video Tutorial by "Sothe" the Algorithm Wolf](https://www.youtube.com/watch?v=wLXEWuDWnzI)