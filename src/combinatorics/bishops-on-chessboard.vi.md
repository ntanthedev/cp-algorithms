---
tags:
  - Translated
e_maxx_link: bishops_arrangement
translation:
  source: combinatorics/bishops-on-chessboard.md
  source_commit: e0194a3395721e8a3e9b57f1efab1b80fd73efb4
  status: draft
  last_synced: 2026-11-15
---

# Đặt quân tượng lên bàn cờ

Đếm cách đặt $K$ quân tượng lên bàn cờ $N \times N$ sao cho không có hai quân nào ăn được nhau.

## Thuật toán

Bài toán này có thể giải bằng quy hoạch động.

Ta đánh số các đường chéo của bàn cờ như sau: các đường chéo đen có chỉ số lẻ, các đường chéo trắng có chỉ số chẵn, và các đường chéo được đánh số theo thứ tự số ô không giảm. Dưới đây là ví dụ với bàn cờ $5 \times 5$.

$$\begin{matrix}
\bf{1} & 2 & \bf{5} & 6 & \bf{9} \\\
2 & \bf{5} & 6 & \bf{9} & 8 \\\
\bf{5} & 6 & \bf{9} & 8 & \bf{7} \\\
6 & \bf{9} & 8 & \bf{7} & 4 \\\
\bf{9} & 8 & \bf{7} & 4 & \bf{3} \\\
\end{matrix}$$

Gọi `D[i][j]` là số cách đặt `j` quân tượng trên các đường chéo cùng màu với đường chéo `i`, có chỉ số không vượt quá `i`.
Khi đó, `i = 1...2N-1` và `j = 0...K`.

Ta có thể tính `D[i][j]` chỉ từ các giá trị `D[i-2]` (trừ đi 2 vì chỉ xét các đường chéo cùng màu với đường chéo $i$).
Có hai cách để tạo ra `D[i][j]`.
Ta có thể đặt cả `j` quân tượng trên các đường chéo trước đó; khi ấy có `D[i-2][j]` cách.
Hoặc đặt một quân tượng trên đường chéo `i` và `j-1` quân tượng trên các đường chéo trước đó.
Số cách đặt trong trường hợp này bằng số ô trên đường chéo `i` trừ đi `j-1`, vì mỗi trong `j-1` quân tượng đã đặt trên các đường chéo trước sẽ chặn một ô trên đường chéo hiện tại.
Số ô trên đường chéo `i` có thể được tính như sau:

```cpp
int squares (int i) {
    if (i & 1)
        return i / 4 * 2 + 1;
    else
        return (i - 1) / 4 * 2 + 2;
}
```

Điều kiện cơ sở đơn giản: `D[i][0] = 1`, `D[1][1] = 1`.

Sau khi tính xong mọi giá trị `D[i][j]`, ta có thể tìm đáp án như sau:
xét mọi số lượng quân tượng có thể đặt trên các đường chéo đen, `i=0...K`; tương ứng, số quân tượng trên các đường chéo trắng là `K-i`.
Các quân tượng đặt trên đường chéo đen và đường chéo trắng không bao giờ ăn được nhau, nên có thể chọn vị trí trên hai nhóm đường chéo độc lập.
Chỉ số của đường chéo đen cuối cùng là `2N-1`, còn của đường chéo trắng cuối cùng là `2N-2`.
Với mỗi `i`, cộng `D[2N-1][i] * D[2N-2][K-i]` vào đáp án.

## Cài đặt

```cpp
int bishop_placements(int N, int K)
{
    if (K > 2 * N - 1)
        return 0;

    vector<vector<int>> D(N * 2, vector<int>(K + 1));
    for (int i = 0; i < N * 2; ++i)
        D[i][0] = 1;
    D[1][1] = 1;
    for (int i = 2; i < N * 2; ++i)
        for (int j = 1; j <= K; ++j)
            D[i][j] = D[i-2][j] + D[i-2][j-1] * (squares(i) - j + 1);

    int ans = 0;
    for (int i = 0; i <= K; ++i)
        ans += D[N*2-1][i] * D[N*2-2][K-i];
    return ans;
}
```

**Ghi chú bản dịch:** Với K = 0, có đúng một cách đặt không quân tượng. Tuy nhiên, hàm trên truy cập D[1][1] ngoài phạm vi vì mỗi hàng của D chỉ có một phần tử. Cần xử lý riêng trường hợp này trước khi gọi hàm.
