---
tags:
  - Translated
e_maxx_link: simpson_integrating
translation:
  source: num_methods/simpson-integration.md
  source_commit: 5a78b3762585b11071235bde0425575edaf30ded
  status: draft
  last_synced: 2026-09-29
---

# Tích phân bằng công thức Simpson

Ta sẽ tính giá trị của một tích phân xác định

$$\int_a ^ b f (x) dx$$

Phương pháp được trình bày ở đây xuất hiện trong một luận văn của **Thomas Simpson** vào năm 1743.

## Công thức Simpson

Gọi $n$ là một số tự nhiên. Ta chia đoạn lấy tích phân $[a, b]$ thành $2n$ phần bằng nhau:

$$x_i = a + i h, ~~ i = 0 \ldots 2n,$$

$$h = \frac {b-a} {2n}.$$

Tiếp theo, ta tính tích phân riêng trên từng đoạn $[x_ {2i-2}, x_ {2i}]$, $i = 1 \ldots n$, rồi cộng tất cả các giá trị lại.

Xét một đoạn $[x_ {2i-2}, x_ {2i}],  i = 1 \ldots n$. Ta thay hàm $f(x)$ trên đoạn đó bằng một parabol $P(x)$ đi qua ba điểm trên đồ thị $(x_{2i-2}, f(x_{2i-2}))$, $(x_{2i-1}, f(x_{2i-1}))$ và $(x_{2i}, f(x_{2i}))$. Parabol như vậy luôn tồn tại và là duy nhất; ta có thể tìm nó bằng phép tính giải tích.
Chẳng hạn, ta có thể xây dựng nó bằng nội suy đa thức Lagrange.
Việc còn lại chỉ là lấy tích phân của đa thức này.
Với một hàm tổng quát $f$, ta thu được biểu thức đơn giản đáng chú ý:

$$\int_{x_ {2i-2}} ^ {x_ {2i}} f (x) ~dx \approx \int_{x_ {2i-2}} ^ {x_ {2i}} P (x) ~dx = \left(f(x_{2i-2}) + 4f(x_{2i-1}) + f(x_{2i})\right)\frac {h} {3} $$

Cộng các giá trị trên mọi đoạn, ta thu được **công thức Simpson** cuối cùng:

$$\int_a ^ b f (x) dx \approx \left(f (x_0) + 4 f (x_1) + 2 f (x_2) + 4f(x_3) + 2 f(x_4) + \ldots + 4 f(x_{2n-1}) + f(x_{2n}) \right)\frac {h} {3} $$

## Sai số

Với một panel Simpson trên đoạn $[a,b]$, sai số là

$$ -\tfrac{1}{90} \left(\tfrac{b-a}{2}\right)^5 f^{(4)}(\xi)$$

trong đó $\xi$ là một số nào đó nằm giữa $a$ và $b$.

Như vậy, sai số của một panel có bậc năm theo độ rộng của panel. Trong công thức ghép ở trên, đoạn được chia thành các panel có độ rộng $2h$. Giả sử đạo hàm bậc bốn bị chặn, cộng các sai số trên từng panel cho ta sai số toàn cục bậc $O((b-a)h^4)$. Quy tắc Simpson đạt thêm một bậc chính xác so với ước lượng trực tiếp từ sai số nội suy vì các điểm dùng để tính hàm dưới dấu tích phân được phân bố đối xứng trong mỗi panel.

## Cài đặt

Ở đây, $f(x)$ là một hàm do người dùng định nghĩa. Số bước $N$ phải chẵn.

```cpp
const int N = 1000 * 1000; // number of steps (already multiplied by 2)

double simpson_integration(double a, double b){
    double h = (b - a) / N;
    double s = f(a) + f(b); // a = x_0 and b = x_2n
    for (int i = 1; i <= N - 1; ++i) { // Refer to final Simpson's formula
        double x = a + h * i;
        s += f(x) * ((i & 1) ? 4 : 2);
    }
    s *= h / 3;
    return s;
}
```

## Bài tập luyện tập

* [Latin American Regionals 2012 - Environment Protection](https://matcomgrader.com/problem/9335/environment-protection/)
