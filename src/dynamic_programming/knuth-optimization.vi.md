---
tags:
  - Original
translation:
  source: dynamic_programming/knuth-optimization.md
  source_commit: e873732d699a211748066082d25cf785268eb86c
  status: draft
  last_synced: 2026-08-08
---

# Tối ưu Knuth (Knuth's Optimization)

Tối ưu Knuth (Knuth's optimization), còn được gọi là tăng tốc Knuth-Yao (Knuth-Yao Speedup), là một trường hợp đặc biệt của quy hoạch động trên đoạn, cho phép giảm độ phức tạp thời gian đi một hệ số tuyến tính: từ $O(n^3)$ với quy hoạch động trên đoạn thông thường xuống $O(n^2)$.

## Điều kiện áp dụng

Phương pháp tăng tốc này áp dụng cho các chuyển trạng thái có dạng

$$dp(i, j) = \min_{i \leq k < j} [ dp(i, k) + dp(k+1, j) + C(i, j) ].$$

Tương tự [quy hoạch động chia để trị](./divide-and-conquer-dp.md), gọi $opt(i, j)$ là giá trị lớn nhất của $k$ làm biểu thức trong chuyển trạng thái đạt giá trị nhỏ nhất (trong phần còn lại của bài, $opt$ được gọi là "điểm chia tối ưu"). Phép tối ưu yêu cầu bất đẳng thức sau đúng:

$$opt(i, j-1) \leq opt(i, j) \leq opt(i+1, j).$$

Ta có thể chứng minh điều này khi hàm chi phí $C$ thỏa mãn các điều kiện sau với $a \leq b \leq c \leq d$:

1. $C(b, c) \leq C(a, d)$;

2. $C(a, c) + C(b, d) \leq C(a, d) + C(b, c)$ (bất đẳng thức tứ giác [QI]).

Kết quả này sẽ được chứng minh ở phần dưới.

## Thuật toán

Ta xử lý các trạng thái dp theo thứ tự sao cho $dp(i, j-1)$ và $dp(i+1, j)$ được tính trước $dp(i, j)$; đồng thời ta cũng tính $opt(i, j-1)$ và $opt(i+1, j)$. Khi đó, để tính $opt(i, j)$, thay vì thử mọi giá trị $k$ từ $i$ đến $j-1$, ta chỉ cần thử từ $opt(i, j-1)$ đến $opt(i+1, j)$. Để xử lý các cặp $(i,j)$ theo thứ tự này, chỉ cần dùng hai vòng lặp lồng nhau, trong đó $i$ đi từ giá trị lớn nhất xuống nhỏ nhất, còn $j$ đi từ $i+1$ đến giá trị lớn nhất.

### Cài đặt tổng quát

Cách cài đặt có thể thay đổi theo từng bài toán, nhưng dưới đây là một ví dụ khá tổng quát. Cấu trúc phần cài đặt gần như giống hệt quy hoạch động trên đoạn.

```{.cpp file=knuth_optimization}

int solve() {
    int N;
    ... // read N and input
    int dp[N][N], opt[N][N];

    auto C = [&](int i, int j) {
        ... // Implement cost function C.
    };

    for (int i = 0; i < N; i++) {
        opt[i][i] = i;
        ... // Initialize dp[i][i] according to the problem
    }

    for (int i = N-2; i >= 0; i--) {
        for (int j = i+1; j < N; j++) {
            int mn = INT_MAX;
            int cost = C(i, j);
            for (int k = opt[i][j-1]; k <= min(j-1, opt[i+1][j]); k++) {
                if (mn >= dp[i][k] + dp[k+1][j] + cost) {
                    opt[i][j] = k; 
                    mn = dp[i][k] + dp[k+1][j] + cost; 
                }
            }
            dp[i][j] = mn; 
        }
    }

    return dp[0][N-1];
}
```

### Độ phức tạp

Độ phức tạp của thuật toán có thể được ước lượng bằng tổng sau:

$$
\sum\limits_{i=1}^N \sum\limits_{j=i+1}^N [opt(i+1,j)-opt(i,j-1)] =
\sum\limits_{i=1}^N \sum\limits_{j=i}^{N-1} [opt(i+1,j+1)-opt(i,j)].
$$

Có thể thấy phần lớn các hạng tử trong biểu thức này triệt tiêu lẫn nhau, ngoại trừ các hạng tử dương có $j=N-1$ và các hạng tử âm có $i=1$. Vì vậy, toàn bộ tổng có thể được ước lượng bởi

$$
\sum\limits_{k=1}^N[opt(k,N)-opt(1,k)] = O(n^2),
$$

thay vì $O(n^3)$ như khi dùng quy hoạch động trên đoạn thông thường.

### Trong thực tế

Ứng dụng phổ biến nhất của tối ưu Knuth là quy hoạch động trên đoạn với công thức chuyển trạng thái nêu trên. Khó khăn duy nhất là chứng minh hàm chi phí thỏa mãn các điều kiện đã cho. Trường hợp đơn giản nhất là khi hàm chi phí $C(i, j)$ chính là tổng các phần tử của mảng con $S[i, i+1, ..., j]$ của một mảng nào đó (tùy bài toán). Tuy nhiên, đôi khi hàm chi phí có thể phức tạp hơn.

Quan trọng hơn cả dạng cụ thể của chuyển trạng thái dp và hàm chi phí, mấu chốt của phép tối ưu này là bất đẳng thức của điểm chia tối ưu. Trong một số bài toán, chẳng hạn bài toán cây tìm kiếm nhị phân tối ưu (cũng chính là bài toán ban đầu mà phép tối ưu này được phát triển để giải), chuyển trạng thái và hàm chi phí có thể không hiển nhiên như trong trường hợp trên; tuy nhiên, nếu vẫn chứng minh được $opt(i, j-1) \leq opt(i, j) \leq opt(i+1, j)$ thì ta vẫn có thể áp dụng phép tối ưu này.


### Chứng minh tính đúng đắn

Để chứng minh thuật toán đúng dựa trên các điều kiện của $C(i,j)$, chỉ cần chứng minh rằng

$$
opt(i, j-1) \leq opt(i, j) \leq opt(i+1, j)
$$

khi các điều kiện đã cho được thỏa mãn.

!!! lemma "Bổ đề"
    $dp(i, j)$ cũng thỏa mãn bất đẳng thức tứ giác nếu các điều kiện của bài toán được thỏa mãn.

??? hint "Chứng minh"
    Chứng minh của bổ đề này sử dụng quy nạp mạnh. Chứng minh được lấy từ bài báo <a href="https://dl.acm.org/doi/pdf/10.1145/800141.804691">Efficient Dynamic Programming Using Quadrangle Inequalities</a> của F. Frances Yao, bài báo đã giới thiệu phương pháp tăng tốc Knuth-Yao (mệnh đề cụ thể này là Bổ đề 2.1 trong bài báo). Ý tưởng là quy nạp theo độ dài $l = d - a$. Trường hợp $l = 1$ là hiển nhiên. Với $l > 1$, xét 2 trường hợp:  

    1. $b = c$  
    Bất đẳng thức rút gọn thành $dp(a, b) + dp(b, d) \leq dp(a, d)$ (điều này giả sử $dp(i, i) = 0$ với mọi $i$, đúng với mọi bài toán sử dụng phép tối ưu này). Đặt $opt(a,d) = z$. 

        - Nếu $z < j$,  
        Ta có
        
            $$
            dp(a, b) \leq dp_{z}(a, b) = dp(a, z) + dp(z+1, b) + C(a, b).
            $$
            
            Do đó,  
            
            $$
            dp(a, b) + dp(b, d) \leq dp(a, z) + dp(z+1, b) + dp(b, d) + C(a, b)
            $$

            Theo giả thiết quy nạp, $dp(z+1, b) + dp(b, d) \leq dp(z+1, d)$. Đồng thời, đề bài cho $C(a, b) \leq C(a, d)$. Kết hợp hai điều này với bất đẳng thức trên, ta thu được kết quả cần chứng minh.

        - Nếu $z \geq j$, chứng minh của trường hợp này đối xứng với trường hợp trước.

    2. $b < c$  
    Đặt $opt(b, c) = z$ và $opt(a, d) = y$. 
        
        - Nếu $z \leq y$,  
        
            $$
            dp(a, c) + dp(b, d) \leq dp_{z}(a, c) + dp_{y}(b, d)
            $$

            trong đó

            $$
            dp_{z}(a, c) + dp_{y}(b, d) = C(a, c) + C(b, d) + dp(a, z) + dp(z+1, c) + dp(b, y) + dp(y+1, d).
            $$

            Áp dụng QI cho $C$ và cho trạng thái dp với các chỉ số $z+1 \leq y+1 \leq c \leq d$ (theo giả thiết quy nạp), ta thu được kết quả cần chứng minh.
        
        - Nếu $z > y$, chứng minh của trường hợp này đối xứng với trường hợp trước.

    Như vậy bổ đề được chứng minh.

Ghi chú bản dịch: Trong trường hợp 1 của chứng minh trên, nguồn dùng các điều kiện “z < j” và “z ≥ j” dù biến j không được định nghĩa trong thiết lập đó. Theo ngữ cảnh của lập luận, mốc phân trường hợp phải là b. Bản dịch giữ nguyên ký hiệu để đồng bộ với nguồn hiện tại. Vấn đề này đã được báo và đề xuất sửa riêng ở bản tiếng Anh.

Bây giờ xét thiết lập sau. Ta có 2 chỉ số $i \leq p \leq q < j$. Đặt $dp_{k} = C(i, j) + dp(i, k) + dp(k+1, j)$.

Giả sử ta chứng minh được rằng

$$
dp_{p}(i, j-1) \geq dp_{q}(i, j-1) \implies dp_{p}(i, j) \geq dp_{q}(i, j).
$$

Đặt $q = opt(i, j-1)$. Theo định nghĩa, $dp_{p}(i, j-1) \geq dp_{q}(i, j-1)$. Vì vậy, áp dụng bất đẳng thức trên cho mọi $i \leq p \leq q$, ta suy ra $opt(i, j)$ không nhỏ hơn $opt(i, j-1)$, qua đó chứng minh nửa đầu của bất đẳng thức.

Bây giờ, áp dụng QI cho các chỉ số $p+1 \leq q+1 \leq j-1 \leq j$, ta có

$$\begin{align}
&dp(p+1, j-1) + dp(q+1, j) ≤ dp(q+1, j-1) + dp(p+1, j) \\
\implies& (dp(i, p) + dp(p+1, j-1) + C(i, j-1)) + (dp(i, q) + dp(q+1, j) + C(i, j)) \\  
\leq& (dp(i, q) + dp(q+1, j-1) + C(i, j-1)) + (dp(i, p) + dp(p+1, j) + C(i, j)) \\  
\implies& dp_{p}(i, j-1) + dp_{q}(i, j) ≤ dp_{p}(i, j) + dp_{q}(i, j-1) \\
\implies& dp_{p}(i, j-1) - dp_{q}(i, j-1) ≤ dp_{p}(i, j) - dp_{q}(i, j) \\
\end{align}$$

Cuối cùng,

$$\begin{align}
&dp_{p}(i, j-1) \geq dp_{q}(i, j-1) \\
&\implies 0 \leq dp_{p}(i, j-1) - dp_{q}(i, j-1) \leq dp_{p}(i, j) - dp_{q}(i, j) \\
&\implies dp_{p}(i, j) \geq dp_{q}(i, j)
\end{align}$$  

Điều này chứng minh phần thứ nhất của bất đẳng thức, tức $opt(i, j-1) \leq opt(i, j)$. Phần thứ hai $opt(i, j) \leq opt(i+1, j)$ có thể được chứng minh bằng cùng ý tưởng, bắt đầu từ bất đẳng thức 
$dp(i, p) + dp(i+1, q) ≤ dp(i+1, p) + dp(i, q)$.

Như vậy chứng minh hoàn tất.

## Bài tập luyện tập
- [UVA - Cutting Sticks](https://onlinejudge.org/external/100/10003.pdf)
- [UVA - Prefix Codes](https://onlinejudge.org/external/120/12057.pdf)
- [SPOJ - Breaking String](https://www.spoj.com/problems/BRKSTRNG/)
- [UVA - Optimal Binary Search Tree](https://onlinejudge.org/external/103/10304.pdf)


## Tài liệu tham khảo
- [Geeksforgeeks Article](https://www.geeksforgeeks.org/knuths-optimization-in-dynamic-programming/)
- [Doc on DP Speedups](https://home.cse.ust.hk/~golin/COMP572/Notes/DP_speedup.pdf)
- [Efficient Dynamic Programming Using Quadrangle Inequalities](https://dl.acm.org/doi/pdf/10.1145/800141.804691)