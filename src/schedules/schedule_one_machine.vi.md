---
tags:
  - Translated
e_maxx_link: johnson_problem_1
translation:
  source: schedules/schedule_one_machine.md
  source_commit: 0f0af255884d7661222f68c32154a801b649f85b
  status: draft
  last_synced: 2026-11-15
---

# Lập lịch các công việc trên một máy

Xét $n$ công việc trên một máy duy nhất. Công việc $i$ cần $t_i$ đơn vị thời gian để xử lý; nếu phải chờ $t$ đơn vị thời gian trước khi bắt đầu công việc, ta phải chịu mức phạt $f_i(t)$.

Bài toán yêu cầu tìm một hoán vị các công việc sao cho tổng mức phạt là nhỏ nhất.
Nếu ký hiệu $\pi$ là hoán vị các công việc ($\pi_1$ là công việc được xử lý đầu tiên, $\pi_2$ là công việc thứ hai, v.v.), tổng mức phạt bằng:

$$F(\pi) = f_{\pi_1}(0) + f_{\pi_2}(t_{\pi_1}) + f_{\pi_3}(t_{\pi_1} + t_{\pi_2}) + \dots + f_{\pi_n}\left(\sum_{i=1}^{n-1} t_{\pi_i}\right)$$

## Lời giải cho một số trường hợp đặc biệt

### Hàm phạt tuyến tính

Trước tiên, ta xét trường hợp mọi hàm phạt $f_i(t)$ đều tuyến tính, tức có dạng $f_i(t) = c_i \cdot t$, trong đó $c_i$ là số không âm.
Lưu ý các hàm này không có hằng số tự do. Nếu có, ta có thể cộng tổng các hằng số đó vào kết quả rồi giải bài toán sau khi bỏ các hằng số.

Chọn $\pi$ bất kỳ và xét $i = 1 \dots n-1$.
Gọi $\pi'$ là hoán vị thu được từ $\pi$ bằng cách đổi chỗ hai công việc ở vị trí $i$ và $i+1$.
Ta hãy tính mức phạt thay đổi bao nhiêu.

$$F(\pi') - F(\pi) =$$

Có thể thấy chỉ số hạng thứ $i$ và thứ $(i+1)$ thay đổi:

$$\begin{align}
&= c_{\pi_i'} \cdot \sum_{k = 1}^{i-1} t_{\pi_k'} + c_{\pi_{i+1}'} \cdot \sum_{k = 1}^i t_{\pi_k'} - c_{\pi_i} \cdot \sum_{k = 1}^{i-1} t_{\pi_k} - c_{\pi_{i+1}} \cdot \sum_{k = 1}^i t_{\pi_k} \\
&= c_{\pi_{i+1}} \cdot \sum_{k = 1}^{i-1} t_{\pi_k'} + c_{\pi_i} \cdot \sum_{k = 1}^i t_{\pi_k'} - c_{\pi_i} \cdot \sum_{k = 1}^{i-1} t_{\pi_k} - c_{\pi_{i+1}} \cdot \sum_{k = 1}^i t_{\pi_k} \\
&= c_{\pi_i} \cdot t_{\pi_{i+1}} - c_{\pi_{i+1}} \cdot t_{\pi_i}
\end{align}$$

Nếu $\pi$ là một lịch tối ưu, thì mọi phép đổi chỗ các công việc kề nhau đều làm tổng mức phạt tăng lên hoặc không đổi. Vì vậy, lịch tối ưu thỏa mãn điều kiện:

$$c_{\pi_{i}} \cdot t_{\pi_{i+1}} - c_{\pi_{i+1}} \cdot t_{\pi_i} \ge 0 \quad \forall i = 1 \dots n-1$$

Biến đổi tương đương, ta được:

$$\frac{c_{\pi_i}}{t_{\pi_i}} \ge \frac{c_{\pi_{i+1}}}{t_{\pi_{i+1}}} \quad \forall i = 1 \dots n-1$$

Do đó, ta có **lịch tối ưu** bằng cách **sắp xếp** các công việc theo tỉ số $\frac{c_i}{t_i}$ theo thứ tự không tăng.

**Ghi chú bản dịch:** Tỉ số trên chỉ xác định khi thời gian xử lý khác 0. Với công việc có thời gian xử lý bằng 0, cần xử lý riêng khi sắp xếp.

Cần lưu ý rằng thuật toán này được xây dựng bằng lập luận hoán đổi (permutation method):
ta thử đổi chỗ hai phần tử kề nhau, tính mức phạt thay đổi bao nhiêu, rồi suy ra thuật toán tìm lời giải tối ưu.

### Hàm phạt mũ

Xét hàm phạt có dạng:

$$f_i(t) = c_i \cdot e^{\alpha \cdot t},$$

trong đó mọi $c_i$ không âm và hằng số $\alpha$ dương.

Áp dụng lập luận hoán đổi, ta dễ dàng xác định rằng cần sắp xếp các công việc theo giá trị sau theo thứ tự không tăng:

$$v_i = \frac{1 - e^{\alpha \cdot t_i}}{c_i}$$

**Ghi chú bản dịch:** Công thức trên chỉ xác định khi hệ số phạt khác 0. Nguồn cho phép hệ số bằng 0 nên cần xử lý riêng trường hợp đó khi sắp xếp.

### Hàm phạt đơn điệu giống nhau

Ở đây, ta xét trường hợp mọi hàm $f_i(t)$ đều giống nhau và là hàm đơn điệu tăng.

Hiển nhiên, trong trường hợp này, lịch tối ưu sắp xếp các công việc theo thời gian xử lý $t_i$ theo thứ tự không giảm.

## Định lý Livshits-Kladov

Định lý Livshits-Kladov khẳng định rằng lập luận hoán đổi chỉ áp dụng được cho ba trường hợp đã nêu, cụ thể là:

- Trường hợp tuyến tính: $f_i(t) = c_i(t) + d_i$, trong đó $c_i$ là các hằng số không âm.
- Trường hợp mũ: $f_i(t) = c_i \cdot e_{\alpha \cdot t} + d_i$, trong đó $c_i$ và $\alpha$ là các hằng số dương.
- Trường hợp hàm giống nhau: $f_i(t) = \phi(t)$, trong đó $\phi$ là hàm đơn điệu tăng.

Trong mọi trường hợp khác, phương pháp này không áp dụng được.

Định lý được chứng minh với giả thiết các hàm phạt đủ trơn (tồn tại đạo hàm cấp ba).

Trong cả ba trường hợp, ta áp dụng lập luận hoán đổi để tìm lịch tối ưu bằng cách sắp xếp, do đó độ phức tạp là $O(n \log n)$.
