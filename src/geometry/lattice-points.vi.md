---
tags:
  - Original
translation:
  source: geometry/lattice-points.md
  source_commit: e3d6faf7e06373d81f10e2c87c518d9664f6d046
  status: draft
  last_synced: 2026-11-16
---

# Điểm nguyên bên trong đa giác không phải đa giác lưới

Với đa giác lưới, ta có công thức Pick để đếm các điểm nguyên bên trong đa giác.
Vậy với đa giác có các đỉnh tùy ý thì sao?

Ta xử lý riêng từng cạnh của đa giác, sau đó cộng số điểm nguyên phía dưới mỗi cạnh, chọn dấu theo hướng của cạnh đó (tương tự cách tính diện tích đa giác bằng các hình thang).

Trước hết, nếu cạnh đang xét có hai đầu mút $A=(x_1;y_1)$ và $B=(x_2;y_2)$, ta có thể biểu diễn nó bằng một hàm bậc nhất:

$$y=y_1+(y_2-y_1) \cdot \dfrac{x-x_1}{x_2-x_1}=\left(\dfrac{y_2-y_1}{x_2-x_1}\right)\cdot x + \left(\dfrac{y_1x_2-x_1y_2}{x_2-x_1}\right)$$

$$y = k \cdot x + b,~k = \dfrac{y_2-y_1}{x_2-x_1},~b = \dfrac{y_1x_2-x_1y_2}{x_2-x_1}$$

Ta đổi biến $x=x'+\lceil x_1 \rceil$, khi đó $b' = b + k \cdot \lceil x_1 \rceil$.
Nhờ đó ta làm việc với $x_1'=0$ và $x_2'=x_2 - \lceil x_1 \rceil$.
Đặt $n = \lfloor x_2' \rfloor$.

Để thuật toán nhất quán, ta không tính các điểm tại $x = n$ và trên $y = 0$.
Có thể cộng thêm các điểm đó sau.
Vậy ta cần tính tổng $\sum\limits_{x'=0}^{n - 1} \lfloor k' \cdot x' + b'\rfloor$. Ta cũng giả sử $k' \geq 0$ và $b'\geq 0$.
Nếu không, ta cần đổi biến $x'=-t$ và cộng $\lceil|b'|\rceil$ vào $b'$.

Ta xét cách tính tổng $\sum\limits_{x=0}^{n - 1} \lfloor k \cdot x + b\rfloor$.
Có hai trường hợp:

  - $k \geq 1$ hoặc $b \geq 1$.
  
    Khi đó, trước tiên ta đếm các điểm phía dưới $y=\lfloor k \rfloor \cdot x + \lfloor b \rfloor$. Số điểm này bằng
    
    \[ \sum\limits_{x=0}^{n - 1} \lfloor k \rfloor \cdot x + \lfloor b \rfloor=\dfrac{(\lfloor k \rfloor(n-1)+2\lfloor b \rfloor) n}{2}. \]
    
    Bây giờ ta chỉ quan tâm đến các điểm $(x;y)$ thỏa mãn $\lfloor k \rfloor \cdot x + \lfloor b \rfloor < y \leq k\cdot x + b$.
    Số lượng này bằng số điểm thỏa mãn $0 < y \leq (k - \lfloor k \rfloor) \cdot x + (b - \lfloor b \rfloor)$.
    Vậy ta đưa bài toán về $k'= k - \lfloor k \rfloor$, $b' = b - \lfloor b \rfloor$, trong đó cả $k'$ và $b'$ đều nhỏ hơn $1$.
    Hình sau minh họa: ta vừa đếm các điểm màu xanh và trừ hàm bậc nhất màu xanh khỏi hàm màu đen để đưa bài toán về các giá trị $k$ và $b$ nhỏ hơn:
    <div style="text-align: center;">
  <img src="lattice.png" alt="Trừ hàm bậc nhất đã lấy phần nguyên">
</div>

  - $k < 1$ và $b < 1$.

    Nếu $\lfloor k \cdot n + b\rfloor$ bằng $0$, ta có thể trả về $0$.
    Nếu không, ta có thể nói rằng không có điểm nguyên nào thỏa mãn $x < 0$ và $0 < y \leq k \cdot x + b$.
    Vì vậy kết quả không đổi nếu ta xét hệ tọa độ mới có $O'=(n;\lfloor k\cdot n + b\rfloor)$, trục $x'$ hướng xuống và trục $y'$ hướng sang trái.
    Trong hệ tọa độ này, ta quan tâm đến các điểm nguyên thuộc tập
    
    \[ \left\{(x;y)~\bigg|~0 \leq x < \lfloor k \cdot n + b\rfloor,~ 0 < y \leq \dfrac{x+(k\cdot n+b)-\lfloor k\cdot n + b \rfloor}{k}\right\} \]
    
    từ đó đưa ta trở lại trường hợp $k>1$.
    Hình dưới cho thấy gốc tọa độ mới $O'$ và các trục $X'$ và $Y'$:
    <div style="text-align: center;">
  <img src="mirror.png" alt="Gốc tọa độ và các trục mới">
</div>
    Trong hệ tọa độ mới, hàm bậc nhất có hệ số $\tfrac 1 k$ và nghiệm tại $\lfloor k\cdot n + b \rfloor-(k\cdot n+b)$, nên công thức trên là đúng.

## Phân tích độ phức tạp

Ta cần đếm nhiều nhất $\dfrac{(k(n-1)+2b)n}{2}$ điểm.
Trong số đó, ngay ở bước đầu ta đếm được $\dfrac{\lfloor k \rfloor (n-1)+2\lfloor b \rfloor}{2}$ điểm.
Có thể coi $b$ rất nhỏ vì ta có thể bắt đầu bằng cách đưa nó xuống dưới $1$.
Khi đó có thể nói ta đếm được khoảng $\dfrac{\lfloor k \rfloor}{k} \geq \dfrac 1 2$ tổng số điểm.
Vì vậy thuật toán kết thúc sau $O(\log n)$ bước.

## Cài đặt

Hàm đơn giản sau tính số điểm nguyên $(x;y)$ thỏa mãn $0 \leq x < n$ và $0 < y \leq \lfloor k x+b\rfloor$:

```cpp
int count_lattices(Fraction k, Fraction b, long long n) {
    auto fk = k.floor();
    auto fb = b.floor();
    auto cnt = 0LL;
    if (k >= 1 || b >= 1) {
        cnt += (fk * (n - 1) + 2 * fb) * n / 2;
        k -= fk;
        b -= fb;
    }
    auto t = k * n + b;
    auto ft = t.floor();
    if (ft >= 1) {
        cnt += count_lattices(1 / k, (t - t.floor()) / k, t.floor());
    }
    return cnt;
}
```

Ở đây `Fraction` là một lớp xử lý số hữu tỉ.
Trong thực tế, dường như nếu trị tuyệt đối của mọi tử số và mẫu số không vượt quá $C$, thì trong các lời gọi đệ quy chúng sẽ không vượt quá $C^2$ nếu luôn chia tử và mẫu cho ước chung lớn nhất của chúng.
Với giả định đó, ta có thể dùng số thực double và yêu cầu độ chính xác $\varepsilon^2$, trong đó $\varepsilon$ là độ chính xác của $k$ và $b$ đầu vào.
Nghĩa là khi lấy phần nguyên dưới, ta nên coi một số là số nguyên nếu nó cách một số nguyên không quá $\varepsilon^2$.
