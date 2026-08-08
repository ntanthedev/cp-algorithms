---
tags:
  - Original
translation:
  source: geometry/minkowski.md
  source_commit: f2661d86750662dd835ff1f81cff4ca8f6261de9
  status: draft
  last_synced: 2026-08-09
---

# Tổng Minkowski của các đa giác lồi

## Định nghĩa
Xét hai tập điểm $A$ và $B$ trên mặt phẳng. Tổng Minkowski $A + B$ được định nghĩa là $\{a + b| a \in A, b \in B\}$.
Ở đây, ta xét trường hợp $A$ và $B$ là các đa giác lồi $P$ và $Q$ cùng với phần bên trong của chúng.
Trong toàn bộ bài viết, ta sẽ xem đa giác như một dãy có thứ tự các đỉnh, nhờ đó các ký hiệu như $|P|$ hoặc
$P_i$ có nghĩa.
Có thể chứng minh rằng tổng của hai đa giác lồi $P$ và $Q$ là một đa giác lồi có nhiều nhất $|P| + |Q|$ đỉnh.

## Thuật toán

Ở đây, ta xem các đa giác được đánh chỉ số theo chu kỳ, tức là $P_{|P|} = P_0,\ Q_{|Q|} = Q_0$ và tương tự.

Vì kích thước của tổng là tuyến tính theo kích thước của hai đa giác ban đầu, ta nên hướng tới một thuật toán thời gian tuyến tính.
Giả sử cả hai đa giác đều được sắp theo thứ tự ngược chiều kim đồng hồ. Xét các dãy cạnh $\{\overrightarrow{P_iP_{i+1}}\}$
và $\{\overrightarrow{Q_jQ_{j+1}}\}$ được sắp theo góc cực. Ta khẳng định rằng dãy cạnh của $P + Q$ có thể thu được bằng cách trộn
hai dãy này mà vẫn giữ thứ tự góc cực, đồng thời thay các vector liên tiếp cùng hướng bằng tổng của chúng. Áp dụng trực tiếp ý tưởng này cho ta
một thuật toán thời gian tuyến tính. Tuy nhiên, để khôi phục các đỉnh của $P + Q$ từ dãy cạnh, ta phải cộng vector nhiều lần,
điều này có thể gây ra sai số không mong muốn nếu làm việc với tọa độ dấu phẩy động. Vì vậy, ta sẽ mô tả một
biến thể nhỏ của ý tưởng trên.


Trước hết, ta cần sắp xếp lại các đỉnh sao cho đỉnh đầu tiên
của mỗi đa giác có tọa độ y nhỏ nhất (nếu có nhiều đỉnh như vậy, chọn đỉnh có tọa độ x nhỏ nhất). Sau đó, các cạnh của cả hai đa giác
sẽ được sắp sẵn theo góc cực nên không cần sắp xếp thủ công.
Bây giờ, tạo hai con trỏ $i$ (trỏ tới một đỉnh của $P$) và $j$ (trỏ tới một đỉnh của $Q$), ban đầu đều bằng 0.
Lặp các bước sau trong khi $i < |P|$ hoặc $j < |Q|$.

1. Thêm $P_i + Q_j$ vào $P + Q$.

2. So sánh góc cực của $\overrightarrow{P_iP_{i + 1}}$ và $\overrightarrow{Q_jQ_{j+1}}$.

3. Tăng con trỏ tương ứng với góc nhỏ hơn (nếu hai góc bằng nhau, tăng cả hai).

## Minh họa

Dưới đây là một hình minh họa giúp hình dung thuật toán đang làm gì.

<div style="text-align: center;">
  <img src="minkowski.gif" alt="Minh họa tổng Minkowski">
</div>

## Khoảng cách giữa hai đa giác
Một trong những ứng dụng phổ biến nhất của tổng Minkowski là tính khoảng cách giữa hai đa giác lồi (hoặc đơn giản là kiểm tra chúng có giao nhau hay không).
Khoảng cách giữa hai đa giác lồi $P$ và $Q$ được định nghĩa là $\min\limits_{a \in P, b \in Q} ||a - b||$. Có thể nhận thấy rằng
khoảng cách luôn đạt được giữa hai đỉnh hoặc giữa một đỉnh và một cạnh, nên ta có thể dễ dàng tìm khoảng cách trong $O(|P||Q|)$. Tuy nhiên,
nếu sử dụng tổng Minkowski một cách khéo léo, ta có thể giảm độ phức tạp xuống $O(|P| + |Q|)$.

**Ghi chú bản dịch:** Mệnh đề “khoảng cách luôn đạt được giữa hai đỉnh hoặc giữa một đỉnh và một cạnh” trong nguồn thiếu trường hợp hai đa giác giao nhau: khoảng cách khi đó bằng 0 và có thể đạt tại giao điểm nằm trong phần trong của hai cạnh. Phương pháp Minkowski ngay dưới vẫn xử lý đúng trường hợp giao nhau bằng cách kiểm tra gốc tọa độ có nằm trong hoặc trên biên đa giác tổng hay không. Vấn đề này được đề xuất sửa riêng ở bản tiếng Anh.

Nếu phản xạ $Q$ qua điểm $(0, 0)$ để thu được đa giác $-Q$, bài toán trở thành tìm khoảng cách nhỏ nhất giữa một điểm trong
$P + (-Q)$ và $(0, 0)$. Ta có thể tìm khoảng cách đó trong thời gian tuyến tính bằng ý tưởng sau.
Nếu $(0, 0)$ nằm bên trong hoặc trên biên của đa giác, khoảng cách bằng $0$; nếu không, khoảng cách đạt được giữa $(0, 0)$ và một đỉnh hoặc cạnh nào đó của đa giác.
Vì tổng Minkowski có thể được tính
trong thời gian tuyến tính, ta thu được một thuật toán thời gian tuyến tính để tìm khoảng cách giữa hai đa giác lồi.

## Cài đặt
Dưới đây là cài đặt tổng Minkowski cho các đa giác có các đỉnh nguyên. Lưu ý rằng trong trường hợp này, mọi phép tính đều có thể thực hiện bằng số nguyên vì
thay vì tính trực tiếp các góc cực rồi so sánh chúng, ta có thể xét dấu của tích có hướng giữa hai vector.

```{.cpp file=minkowski}
struct pt{
    long long x, y;
    pt operator + (const pt & p) const {
        return pt{x + p.x, y + p.y};
    }
    pt operator - (const pt & p) const {
        return pt{x - p.x, y - p.y};
    }
    long long cross(const pt & p) const {
        return x * p.y - y * p.x;
    }
};

void reorder_polygon(vector<pt> & P){
    size_t pos = 0;
    for(size_t i = 1; i < P.size(); i++){
        if(P[i].y < P[pos].y || (P[i].y == P[pos].y && P[i].x < P[pos].x))
            pos = i;
    }
    rotate(P.begin(), P.begin() + pos, P.end());
}

vector<pt> minkowski(vector<pt> P, vector<pt> Q){
    // the first vertex must be the lowest
    reorder_polygon(P);
    reorder_polygon(Q);
    // we must ensure cyclic indexing
    P.push_back(P[0]);
    P.push_back(P[1]);
    Q.push_back(Q[0]);
    Q.push_back(Q[1]);
    // main part
    vector<pt> result;
    size_t i = 0, j = 0;
    while(i < P.size() - 2 || j < Q.size() - 2){
        result.push_back(P[i] + Q[j]);
        auto cross = (P[i + 1] - P[i]).cross(Q[j + 1] - Q[j]);
        if(cross >= 0 && i < P.size() - 2)
            ++i;
        if(cross <= 0 && j < Q.size() - 2)
            ++j;
    }
    return result;
}

```

## Bài tập
 * [Codeforces 87E Mogohu-Rea Idol](https://codeforces.com/problemset/problem/87/E)
 * [Codeforces 1195F Geometers Anonymous Club](https://codeforces.com/contest/1195/problem/F)
 * [TIMUS 1894 Non-Flying Weather](https://acm.timus.ru/problem.aspx?space=1&num=1894)
