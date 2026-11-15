---
tags:
  - Translated
e_maxx_link: johnson_problem_2
translation:
  source: schedules/schedule_two_machines.md
  source_commit: 4f7fe2b03835a7c897f8e0b9527e0b8a10793b65
  status: draft
  last_synced: 2026-11-15
---

# Lập lịch công việc trên hai máy

Bài toán là tìm lịch tối ưu cho $n$ công việc trên hai máy.
Mỗi công việc phải được xử lý trên máy thứ nhất trước, sau đó trên máy thứ hai.
Công việc thứ $i$ mất thời gian $a_i$ trên máy thứ nhất và $b_i$ trên máy thứ hai.
Mỗi máy chỉ có thể xử lý một công việc tại một thời điểm.

Ta muốn tìm thứ tự tối ưu của các công việc sao cho thời điểm hoàn thành cuối cùng nhỏ nhất có thể.

Lời giải được trình bày ở đây gọi là quy tắc Johnson (đặt theo tên S. M. Johnson).

Lưu ý rằng bài toán trở thành NP-đầy đủ nếu có nhiều hơn hai máy.

## Xây dựng thuật toán

Trước hết, ta có thể giả sử thứ tự công việc trên máy thứ nhất và máy thứ hai trùng nhau.
Thật vậy, các công việc chỉ có thể được đưa vào máy thứ hai sau khi xử lý ở máy thứ nhất; nếu có nhiều công việc cùng sẵn sàng cho máy thứ hai thì tổng thời gian xử lý chúng bằng tổng các $b_i$, bất kể thứ tự.
Do đó, sẽ chỉ có lợi khi đưa các công việc vào máy thứ hai theo cùng thứ tự đã đưa vào máy thứ nhất.

Xét thứ tự công việc trùng với thứ tự đầu vào $1, 2, \dots, n$.

Ký hiệu $x_i$ là **thời gian nhàn rỗi** của máy thứ hai ngay trước khi xử lý công việc $i$.
Mục tiêu là **cực tiểu hóa tổng thời gian nhàn rỗi**:

$$F(x) = \sum x_i ~ \rightarrow \min$$

Với công việc đầu tiên, ta có $x_1 = a_1$.
Với công việc thứ hai, do nó được đưa tới máy tại thời điểm $a_1 + a_2$, còn máy thứ hai rảnh tại thời điểm $x_1 + b_1$, ta có $x_2 = \max\left((a_1 + a_2) - (x_1 + b_1), 0\right)$.
Tổng quát, ta có công thức:

$$x_k = \max\left(\sum_{i=1}^k a_i - \sum_{i=1}^{k-1} b_i - \sum_{i=1}^{k-1} x_i, 0 \right)$$

Bây giờ ta tính **tổng thời gian nhàn rỗi** $F(x)$.
Ta khẳng định nó có dạng

$$F(x) = \max_{k=1 \dots n} K_i,$$

trong đó

$$K_i = \sum_{i=1}^k a_i - \sum_{i=1}^{k-1} b_i.$$

**Ghi chú bản dịch:** Hai công thức trên dùng chỉ số chưa nhất quán. Để chỉ số được xác định, có thể viết $K_k = \sum_{i=1}^k a_i - \sum_{i=1}^{k-1} b_i$ và $F(x) = \max_{1 \le k \le n} K_k$.

Có thể dễ dàng kiểm chứng điều này bằng quy nạp.

Bây giờ ta dùng **phương pháp hoán đổi**:
đổi chỗ hai công việc kề nhau $j$ và $j+1$ rồi xem tổng thời gian nhàn rỗi thay đổi thế nào.

Từ dạng biểu thức của $K_i$, rõ ràng chỉ $K_j$ và $K_{j+1}$ thay đổi; ký hiệu các giá trị mới tương ứng là $K_j'$ và $K_{j+1}'$.

Nếu việc đổi chỗ hai công việc $j$ và $j+1$ làm tăng tổng thời gian nhàn rỗi, thì phải có:

$$\max(K_j, K_{j+1}) \le \max(K_j', K_{j+1}')$$

(Việc đổi chỗ hai công việc cũng có thể không ảnh hưởng gì.
Điều kiện trên chỉ là điều kiện đủ, không phải điều kiện cần.)

**Ghi chú bản dịch:** Bất đẳng thức trên là điều kiện đủ để tổng thời gian nhàn rỗi sau khi đổi chỗ không giảm (có thể bằng trước). Nó không cần thiết cho kết luận không giảm này: một giá trị $K$ ngoài cặp có thể chi phối giá trị lớn nhất cả trước và sau khi đổi chỗ.

Sau khi trừ $\sum_{i=1}^{j+1} a_i - \sum_{i=1}^{j-1} b_i$ ở cả hai vế, ta được:

$$\max(-a_{j+1}, -b_j) \le \max(-b_{j+1}, -a_j)$$

Sau khi bỏ các dấu âm:

$$\min(a_j, b_{j+1}) \le \min(b_j, a_{j+1})$$

Như vậy ta thu được một **tiêu chí so sánh**:
sắp xếp các công việc theo tiêu chí này cho ta một thứ tự tối ưu, trong đó không thể đổi chỗ hai công việc để cải thiện thời điểm hoàn thành cuối cùng.

Tuy nhiên, có thể **đơn giản hóa** việc sắp xếp hơn nữa bằng cách nhìn tiêu chí so sánh từ một góc độ khác.
Có thể diễn giải tiêu chí như sau:
Nếu trong bốn thời gian $(a_j, a_{j+1}, b_j, b_{j+1})$, giá trị nhỏ nhất ứng với máy thứ nhất thì công việc tương ứng nên được thực hiện trước.
Nếu thời gian nhỏ nhất thuộc máy thứ hai thì công việc tương ứng nên được thực hiện sau.
Do đó ta có thể sắp xếp các công việc theo $\min(a_i, b_i)$; nếu thời gian xử lý công việc hiện tại trên máy thứ nhất nhỏ hơn trên máy thứ hai thì công việc đó phải được thực hiện trước tất cả công việc còn lại, ngược lại thì thực hiện sau tất cả công việc còn lại.

Như vậy, quy tắc Johnson giải bài toán bằng cách sắp xếp các công việc, với độ phức tạp thời gian $O(n \log n)$.

## Cài đặt

Ở đây ta cài đặt biến thể thứ hai của thuật toán đã mô tả.

```{.cpp file=johnsons_rule}
struct Job {
    int a, b, idx;

    bool operator<(Job o) const {
        return min(a, b) < min(o.a, o.b);
    }
};

vector<Job> johnsons_rule(vector<Job> jobs) {
    sort(jobs.begin(), jobs.end());
    vector<Job> a, b;
    for (Job j : jobs) {
        if (j.a < j.b)
            a.push_back(j);
        else
            b.push_back(j);
    }
    a.insert(a.end(), b.rbegin(), b.rend());
    return a;
}

pair<int, int> finish_times(vector<Job> const& jobs) {
    int t1 = 0, t2 = 0;
    for (Job j : jobs) {
        t1 += j.a;
        t2 = max(t2, t1) + j.b;
    }
    return make_pair(t1, t2);
}
```

Mọi thông tin về mỗi công việc được lưu trong struct.
Hàm thứ nhất sắp xếp mọi công việc và tính lịch tối ưu.
Hàm thứ hai tính thời điểm hoàn thành của cả hai máy theo một lịch cho trước.
