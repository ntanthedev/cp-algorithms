---
tags:
  - Translated
e_maxx_link: circle_tangents
translation:
  source: geometry/tangents-to-two-circles.md
  source_commit: 546150a6238fbda47e50e13eff2869ddb964f75e
  status: draft
  last_synced: 2026-11-16
---

# Tìm các tiếp tuyến chung của hai đường tròn

Cho hai đường tròn. Hãy tìm tất cả các tiếp tuyến chung của chúng, tức là những đường thẳng tiếp xúc với cả hai đường tròn.

Thuật toán dưới đây cũng hoạt động khi một hoặc cả hai đường tròn suy biến thành điểm. Vì vậy, ta cũng có thể dùng thuật toán để tìm các tiếp tuyến của một đường tròn đi qua một điểm cho trước.


## Số lượng tiếp tuyến chung
Số tiếp tuyến chung của hai đường tròn có thể là **0, 1, 2, 3, 4** hoặc **vô số**.
Hình sau minh họa các trường hợp khác nhau.
<div style="text-align: center;">
  <img src="tangents-to-two-circles.png" alt=""Different cases of tangents common to two circles"">
</div>

Ở đây, ta không xét các trường hợp **suy biến**, tức là *hai đường tròn trùng nhau (khi đó có vô số tiếp tuyến chung), hoặc một đường tròn nằm trong đường tròn kia (khi đó không có tiếp tuyến chung, hoặc có một tiếp tuyến chung nếu hai đường tròn tiếp xúc nhau).*

Trong phần lớn trường hợp, hai đường tròn có **bốn** tiếp tuyến chung.

Nếu hai đường tròn **tiếp xúc nhau** thì chúng có ba tiếp tuyến chung. Có thể hiểu đây là trường hợp suy biến khi hai tiếp tuyến trùng nhau.

Hơn nữa, thuật toán bên dưới vẫn hoạt động khi một hoặc cả hai đường tròn có bán kính bằng không: khi đó tương ứng sẽ có hai hoặc một tiếp tuyến chung.

Tóm lại, ta luôn tìm **bốn tiếp tuyến** trong mọi trường hợp trừ trường hợp có vô số tiếp tuyến (trường hợp này cần xử lý riêng và không được bàn ở đây). Trong các trường hợp suy biến, một số tiếp tuyến sẽ trùng nhau, nhưng vẫn phù hợp với cách tiếp cận chung.



## Thuật toán
Để đơn giản hóa thuật toán, không mất tính tổng quát, ta giả sử tâm đường tròn thứ nhất có tọa độ $(0, 0)$. (Nếu chưa như vậy, ta chỉ cần tịnh tiến toàn bộ hình và sau khi tìm được lời giải thì tịnh tiến các đường thẳng thu được trở lại.)

Gọi $r_1$ và $r_2$ là bán kính của đường tròn thứ nhất và thứ hai, còn $(v_x,v_y)$ là tọa độ tâm của đường tròn thứ hai; điểm $v$ khác gốc tọa độ. (Lưu ý: ta không xét trường hợp hai đường tròn trùng nhau.)

Ta giải bài toán bằng phương pháp hoàn toàn **đại số**. Cần tìm mọi đường thẳng dạng $ax + by + c = 0$ có khoảng cách đến gốc tọa độ là $r_1$ và đến điểm $v$ là $r_2$. Ngoài ra, ta chuẩn hóa đường thẳng: tổng bình phương các hệ số phải bằng một (điều này cần thiết vì nếu không, cùng một đường thẳng sẽ có vô số biểu diễn dạng $ax + by + c = 0$). Ta thu được hệ phương trình sau cho các hệ số $a, b, c$ cần tìm:

$$\begin{align}
a^2 + b^2 &= 1 \\
\mid a \cdot 0 + b \cdot 0 + c \mid &= r_1 \\
\mid a \cdot v_x + b \cdot v_y + c \mid &= r_2
\end{align}$$

**Ghi chú bản dịch:** Điều kiện chuẩn hóa trong hệ trên chỉ áp dụng cho hai hệ số a và b, không gồm c.

Để bỏ dấu giá trị tuyệt đối, nhận xét rằng chỉ có bốn cách bỏ dấu trong hệ này. Ta có thể xét chung các cách đó bằng cách cho phép nhân vế phải với -1. Nói cách khác, ta chuyển sang hệ:

$$\begin{align}
a^2 + b^2 &= 1 \\
c &= \pm r_1 \\
a \cdot v_x + b \cdot v_y + c &= \pm r_2
\end{align}$$


Đặt $d_1 = \pm r_1$ và $d_2 = \pm r_2$, ta đi đến kết luận rằng hệ phải có bốn nghiệm:

$$\begin{align}
a^2 + b^2 &= 1 \\
c &= d_1 \\
a \cdot v_x + b \cdot v_y + c &= d_2
\end{align}$$

Giải hệ này quy về giải một phương trình bậc hai. Ta bỏ qua các phép tính dài dòng và nêu ngay kết quả:

$$\begin{align}
a &= {( d_2 - d_1 ) v_x \pm v_y \sqrt{v_x^2 + v_y^2-(d_2-d_1)^2} \over {v_x^2 + v_y^2} } \\
b &= {( d_2 - d_1 ) v_y \pm v_x \sqrt{v_x^2 + v_y^2-(d_2-d_1)^2} \over {v_x^2 + v_y^2} } \\
c &= d_1
\end{align}$$

**Ghi chú bản dịch:** Hai dấu cộng trừ trong công thức của a và b phải được chọn trái nhau để thỏa hệ phương trình phía trên. Chẳng hạn, nếu v = (1, 1) và d₂ − d₁ = 0, chọn cùng dấu cho a và b thì vế trái của phương trình cuối khác không. Mã dưới đây dùng dấu trái nhau.

Tổng cộng ta thu được tám nghiệm thay vì bốn. Tuy nhiên, dễ hiểu vì sao xuất hiện các nghiệm thừa: ở hệ sau cùng, chỉ cần lấy một nghiệm (chẳng hạn nghiệm thứ nhất). Ý nghĩa hình học của việc lấy $\pm r_1$ và $\pm r_2$ là ta đang xét đường thẳng nằm về phía nào của mỗi đường tròn. Vì vậy, hai cách xuất hiện khi giải hệ sau cùng là dư thừa: chỉ cần chọn một trong hai nghiệm, nhưng phải chọn cùng một họ nghiệm trong cả bốn trường hợp.

Điều cuối cùng ta chưa xét là **cách tịnh tiến các đường thẳng** khi tâm đường tròn thứ nhất ban đầu không ở gốc tọa độ. Từ tính tuyến tính của phương trình đường thẳng, ta cần trừ giá trị $a \cdot x_0 + b \cdot y_0$ khỏi hệ số $c$, trong đó $x_0$ và $y_0$ là tọa độ tâm ban đầu của đường tròn thứ nhất.

##Cài đặt
Trước tiên, ta mô tả các cấu trúc dữ liệu và định nghĩa phụ trợ cần thiết:

```point-line-circle-struct
struct pt {
    double x, y;

    pt operator- (pt p) {
        pt res = { x-p.x, y-p.y };
        return res;
    }
};

struct circle : pt {
    double r;
};

struct line {
    double a, b, c;
};

const double EPS = 1E-9;

double sqr (double a) {
    return a * a;
}
```
Sau đó có thể viết lời giải như sau (hàm thứ hai là hàm chính để gọi, còn hàm thứ nhất là hàm phụ trợ):

```find-tangents-to-two-circles
void tangents (pt c, double r1, double r2, vector<line> & ans) {
    double r = r2 - r1;
    double z = sqr(c.x) + sqr(c.y);
    double d = z - sqr(r);
    if (d < -EPS)  return;
    d = sqrt (abs (d));
    line l;
    l.a = (c.x * r + c.y * d) / z;
    l.b = (c.y * r - c.x * d) / z;
    l.c = r1;
    ans.push_back (l);
}

vector<line> tangents (circle a, circle b) {
    vector<line> ans;
    for (int i=-1; i<=1; i+=2)
        for (int j=-1; j<=1; j+=2)
            tangents (b-a, a.r*i, b.r*j, ans);
    for (size_t i=0; i<ans.size(); ++i)
        ans[i].c -= ans[i].a * a.x + ans[i].b * a.y;
    return ans;
}
```

## Bài tập

[TIMUS 1163 Chapaev](https://acm.timus.ru/problem.aspx?space=1&num=1163)
