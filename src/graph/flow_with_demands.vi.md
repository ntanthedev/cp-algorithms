---
tags:
  - Translated
e_maxx_link: flow_with_limits
translation:
  source: graph/flow_with_demands.md
  source_commit: a3f458d419dc1003af9c4d99cdaf168cece131ba
  status: draft
  last_synced: 2026-11-15
---

# Luồng có cận dưới

Trong mạng luồng thông thường, luồng trên một cạnh chỉ bị chặn trên bởi khả năng thông qua $c(e)$ và chặn dưới bởi 0.
Bài này xét mạng luồng có thêm yêu cầu về lượng luồng trên mỗi cạnh, tức là luồng bị chặn dưới bởi một hàm **nhu cầu** $d(e)$:

$$ d(e) \le f(e) \le c(e)$$

Do đó mỗi cạnh có một giá trị luồng tối thiểu phải đi qua cạnh ấy.

Đây là dạng tổng quát của bài toán luồng thông thường, vì đặt $d(e) = 0$ cho mọi cạnh $e$ sẽ cho ta mạng luồng thông thường.
Trong mạng luồng thông thường, việc tìm một luồng hợp lệ rất đơn giản: chỉ cần đặt $f(e) = 0$.
Tuy nhiên, khi luồng trên mỗi cạnh phải đáp ứng một nhu cầu, việc tìm luồng hợp lệ trở nên khá phức tạp.

Ta sẽ xét hai bài toán:

1. tìm một luồng bất kỳ thỏa mãn mọi ràng buộc
2. tìm một luồng nhỏ nhất thỏa mãn mọi ràng buộc

## Tìm một luồng bất kỳ

Ta thay đổi mạng như sau.
Thêm nguồn mới $s'$, đích mới $t'$, một cạnh từ $s'$ tới mỗi đỉnh khác, một cạnh từ mỗi đỉnh tới $t'$, và một cạnh từ $t$ tới $s$.
Đồng thời định nghĩa hàm khả năng thông qua mới $c'$ như sau:

- $c'((s', v)) = \sum_{u \in V} d((u, v))$ với mỗi cạnh $(s', v)$.
- $c'((v, t')) = \sum_{w \in V} d((v, w))$ với mỗi cạnh $(v, t')$.
- $c'((u, v)) = c((u, v)) - d((u, v))$ với mỗi cạnh $(u, v)$ trong mạng cũ.
- $c'((t, s)) = \infty$

Nếu mạng mới có luồng bão hòa (mỗi cạnh đi ra từ $s'$ đều đầy, tương đương với mỗi cạnh đi vào $t'$ đều đầy), thì mạng có nhu cầu có một luồng hợp lệ, và có thể dễ dàng khôi phục luồng đó từ mạng mới.
Ngược lại, không tồn tại luồng thỏa mãn mọi điều kiện.
Vì luồng bão hòa phải là luồng cực đại, ta có thể tìm nó bằng bất kỳ thuật toán luồng cực đại nào, chẳng hạn [thuật toán Edmonds-Karp](edmonds_karp.md) hoặc [thuật toán Push-relabel](push-relabel.md).

Tính đúng đắn của các phép biến đổi này khó hiểu hơn.
Ta có thể hình dung như sau:
Ban đầu, mỗi cạnh $e = (u, v)$ có $d(e) > 0$ được thay bằng hai cạnh: một cạnh có khả năng thông qua $d(i)$, cạnh còn lại có khả năng thông qua $c(i) - d(i)$.
**Ghi chú bản dịch:** Ký hiệu $i$ trong $d(i)$ và $c(i)$ ở câu trên chưa được nguồn định nghĩa; theo ngữ cảnh, các biểu thức này tương ứng với $d(e)$ và $c(e)$.

Ta muốn tìm một luồng bão hòa cạnh thứ nhất (tức luồng trên cạnh này phải bằng khả năng thông qua của nó).
Cạnh thứ hai ít quan trọng hơn: luồng trên nó có thể tùy ý, miễn là không vượt quá khả năng thông qua.
Với mỗi cạnh cần bão hòa, ta thực hiện thao tác sau:
vẽ cạnh từ nguồn mới $s'$ đến điểm cuối $v$, vẽ cạnh từ điểm đầu $u$ đến đích mới $t'$, xóa chính cạnh đó, và vẽ một cạnh có khả năng thông qua vô hạn từ đích cũ $t$ đến nguồn cũ $s$.
Các thao tác này mô phỏng việc cạnh đó bão hòa: từ $v$ sẽ có thêm $d(e)$ luồng đi ra (ta mô phỏng bằng nguồn mới cấp đúng lượng luồng cho $v$), còn $u$ cũng đẩy thêm $d(e)$ luồng (nhưng thay vì theo cạnh cũ, lượng luồng này đi thẳng tới đích mới $t'$).
Một luồng có giá trị $d(e)$ vốn đi theo đường $s - \dots - u - v - \dots t$ giờ có thể đi theo đường mới $s' - v - \dots - t - s - \dots - u - t'$.
Định nghĩa mạng mới chỉ đơn giản hóa ở chỗ: nếu quá trình tạo ra nhiều cạnh giữa cùng một cặp đỉnh, chúng được gộp thành một cạnh với khả năng thông qua bằng tổng của chúng.

## Luồng nhỏ nhất

Lưu ý rằng toàn bộ luồng của mạng cũ tương ứng đi qua cạnh $(t, s)$ (từ đích cũ tới nguồn cũ) có khả năng thông qua $\infty$.
Tức là khả năng thông qua của cạnh này ảnh hưởng tới giá trị luồng của mạng cũ.
Khi cho cạnh này khả năng thông qua đủ lớn (tức $\infty$), luồng của mạng cũ không bị giới hạn.
Khi giới hạn cạnh này bằng các khả năng thông qua nhỏ hơn, giá trị luồng sẽ giảm.
Tuy nhiên, nếu giới hạn quá nhỏ, mạng sẽ không có lời giải bão hòa; chẳng hạn lời giải tương ứng của mạng ban đầu sẽ không đáp ứng nhu cầu của các cạnh.
Có thể dùng tìm kiếm nhị phân để tìm giá trị nhỏ nhất mà tại đó mọi ràng buộc vẫn được thỏa mãn.
Giá trị đó cho ta luồng nhỏ nhất của mạng ban đầu.

**Ghi chú bản dịch:** Cách thêm cạnh $(t, s)$ ở trên xét luồng $s$–$t$ có giá trị không âm. Nếu cho phép giá trị âm, phép dựng này có thể bỏ sót nghiệm: chẳng hạn mạng chỉ có cạnh từ $t$ đến $s$ với cận dưới và cận trên đều bằng 1. Tìm kiếm nhị phân chính xác cần miền giá trị rời rạc, ví dụ các cận nguyên và tìm trên số nguyên, đồng thời cần kiểm tra trước rằng có luồng hợp lệ. Với miền số thực, cần xác định sai số tìm kiếm.
