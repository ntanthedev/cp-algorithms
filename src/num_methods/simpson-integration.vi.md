---
tags:
  - Translated
e_maxx_link: simpson_integrating
translation:
  source: num_methods/simpson-integration.md
  source_commit: f22f2b9a25d7fe89ee11f3134e289ca5c2b87b06
  status: draft
  last_synced: 2026-08-09
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

Xét một đoạn $[x_ {2i-2}, x_ {2i}],  i = 1 \ldots n$. Ta thay hàm $f(x)$ trên đoạn đó bằng một parabol $P(x)$ đi qua 3 điểm tương ứng $(x_ {2i-2}, x_ {2i-1}, x_ {2i})$. Parabol như vậy luôn tồn tại và là duy nhất; ta có thể tìm nó bằng phép tính giải tích.
Chẳng hạn, ta có thể xây dựng nó bằng nội suy đa thức Lagrange.
Việc còn lại chỉ là lấy tích phân của đa thức này.
Với một hàm tổng quát $f$, ta thu được biểu thức đơn giản đáng chú ý:

$$\int_{x_ {2i-2}} ^ {x_ {2i}} f (x) ~dx \approx \int_{x_ {2i-2}} ^ {x_ {2i}} P (x) ~dx = \left(f(x_{2i-2}) + 4f(x_{2i-1})+(f(x_{2i})\right)\frac {h} {3} $$

Cộng các giá trị trên mọi đoạn, ta thu được **công thức Simpson** cuối cùng:

$$\int_a ^ b f (x) dx \approx \left(f (x_0) + 4 f (x_1) + 2 f (x_2) + 4f(x_3) + 2 f(x_4) + \ldots + 4 f(x_{2N-1}) + f(x_{2N}) \right)\frac {h} {3} $$

**Ghi chú bản dịch:** Nguồn có hai lỗi trình bày trong các công thức ngay phía trên: công thức trên một đoạn có một dấu ngoặc mở thừa trước hạng cuối, và công thức tổng dùng chữ N trong chỉ số dù phần định nghĩa trước đó dùng chữ n. Bản dịch giữ nguyên LaTeX để đồng bộ chính xác với source; các lỗi này được đề xuất sửa riêng upstream.

## Sai số

Sai số khi xấp xỉ một tích phân bằng công thức Simpson là

$$ -\tfrac{1}{90} \left(\tfrac{b-a}{2}\right)^5 f^{(4)}(\xi)$$

trong đó $\xi$ là một số nào đó nằm giữa $a$ và $b$.

Sai số tỉ lệ tiệm cận với $(b-a)^5$. Tuy nhiên, các suy luận phía trên gợi ý sai số tỉ lệ với $(b-a)^4$. Quy tắc Simpson đạt thêm một bậc chính xác vì các điểm dùng để đánh giá hàm dưới dấu tích phân được phân bố đối xứng trên đoạn $[a, b]$.

**Ghi chú bản dịch:** Công thức sai số nguồn nêu ở đoạn này là sai số của một lần áp dụng quy tắc Simpson trên một panel gồm hai khoảng con. Với công thức Simpson ghép nhiều panel như phần cài đặt bên dưới, sai số toàn cục phụ thuộc vào bước lưới và có dạng khác; vì vậy không nên đọc công thức trên như sai số tổng của toàn bộ phép chia nhiều đoạn.

## Cài đặt

Ở đây, $f(x)$ là một hàm do người dùng định nghĩa.

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
