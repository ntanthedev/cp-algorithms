---
tags:
  - Translated
e_maxx_link: maximum_average_segment
translation:
  source: others/maximum_average_segment.md
  source_commit: d9c59fb53129f6e3bba6c1664079f824444a50d2
  status: draft
  last_synced: 2026-11-16
---

# Tìm đoạn con có tổng lớn nhất hoặc nhỏ nhất

Ta xét bài toán tìm đoạn con có tổng lớn nhất và một số biến thể, bao gồm thuật toán giải trực tuyến.

## Phát biểu bài toán

Cho mảng số $a[1 \ldots n]$. Hãy tìm đoạn con $a[l \ldots r]$ có tổng lớn nhất:

$$ \max_{ 1 \le l \le r \le n } \sum_{i=l}^{r} a[i].$$

Ví dụ, nếu mọi số nguyên trong mảng $a[]$ đều không âm thì đáp án là cả mảng. Tuy nhiên, khi mảng có thể chứa cả số dương lẫn số âm, lời giải không còn hiển nhiên.

Rõ ràng bài toán tìm đoạn con có tổng **nhỏ nhất** về cơ bản giống hệt: chỉ cần đổi dấu mọi số.

## Thuật toán 1

Trước tiên ta xét một thuật toán gần như hiển nhiên. Sau đó ta sẽ xem thuật toán khác khó nghĩ ra hơn một chút nhưng có cài đặt ngắn hơn.

### Mô tả thuật toán

Thuật toán rất đơn giản.

Để thuận tiện, ta dùng **ký hiệu**: $s[i] = \sum_{j=1}^{i} a[j]$. Nghĩa là mảng $s[i]$ chứa tổng tiền tố của mảng $a[]$. Đặt thêm $s[0] = 0$.

Giờ ta duyệt chỉ số $r = 1 \ldots n$ và tìm cách nhanh chóng xác định $l$ tối ưu cho mỗi giá trị $r$ hiện tại, sao cho tổng trên đoạn con $[l, r]$ là lớn nhất.

Cụ thể, với $r$ hiện tại, ta cần tìm $l$ không vượt quá $r$ sao cho $s[r] - s[l-1]$ lớn nhất. Sau một phép biến đổi đơn giản, ta thấy cần tìm giá trị nhỏ nhất trong mảng $s[]$ trên đoạn $[0, r-1]$.

Từ đây ta có ngay lời giải: chỉ cần lưu vị trí giá trị nhỏ nhất hiện tại trong mảng $s[]$. Dựa vào giá trị này, ta tìm được chỉ số $l$ tối ưu hiện tại trong $O(1)$. Khi chuyển từ chỉ số $r$ sang chỉ số kế tiếp, ta cập nhật giá trị nhỏ nhất.

Rõ ràng thuật toán chạy trong $O(n)$ và tối ưu về mặt tiệm cận.

### Cài đặt

Ta thậm chí không cần lưu tường minh mảng tổng tiền tố $s[]$; chỉ cần phần tử hiện tại của nó.

Phần cài đặt dùng chỉ số từ 0, khác với cách đánh số từ 1 trong phần mô tả.

Trước hết, ta đưa ra lời giải chỉ tìm giá trị đáp án mà không tìm các chỉ số của đoạn:

```cpp
int ans = a[0], sum = 0, min_sum = 0;

for (int r = 0; r < n; ++r) {
    sum += a[r];
    ans = max(ans, sum - min_sum);
    min_sum = min(min_sum, sum);
}
```

Sau đây là phiên bản đầy đủ, tìm thêm hai đầu mút của đoạn cần tìm:

```cpp
int ans = a[0], ans_l = 0, ans_r = 0;
int sum = 0, min_sum = 0, min_pos = -1;

for (int r = 0; r < n; ++r) {
    sum += a[r];
    int cur = sum - min_sum;
    if (cur > ans) {
        ans = cur;
        ans_l = min_pos + 1;
        ans_r = r;
    }
    if (sum < min_sum) {
        min_sum = sum;
        min_pos = r;
    }
}
```

## Thuật toán 2

Giờ ta xét một thuật toán khác. Thuật toán này khó hiểu hơn một chút nhưng có ý tưởng thanh thoát hơn và cài đặt ngắn hơn. Jay Kadane đề xuất thuật toán này năm 1984.

### Mô tả thuật toán

Ta duyệt mảng và tích lũy tổng hiện tại vào một biến $s$. Nếu tại một thời điểm $s$ âm, ta gán $s=0$. Có thể chứng minh giá trị lớn nhất mà biến $s$ nhận trong quá trình chạy chính là đáp án.

**Ghi chú của người dịch:** Cần lấy giá trị lớn nhất sau khi cộng phần tử và trước khi đặt tổng âm về không, như trong mã bên dưới. Nếu tính cả giá trị không sau khi đặt lại thì kết quả có thể sai với mảng toàn số âm.

**Chứng minh:**

Xét chỉ số đầu tiên tại đó tổng $s$ trở nên âm. Bắt đầu từ tổng bằng không, ta cuối cùng nhận được tổng âm; vì thế toàn bộ tiền tố này, cũng như bất kỳ hậu tố nào của nó, đều có tổng âm. Do đó đoạn con này không bao giờ đóng góp có lợi vào tổng của một đoạn con nhận nó làm tiền tố, nên có thể bỏ đi.

Tuy nhiên, điều này chưa đủ chứng minh thuật toán. Trong thuật toán, ta thực sự chỉ tìm đáp án trong những đoạn bắt đầu ngay sau vị trí từng xảy ra $s<0$.

Xét một đoạn bất kỳ $[l, r]$ mà $l$ không ở vị trí "tới hạn" như vậy, tức $l > p+1$ với $p$ là vị trí cuối cùng thỏa $s<0$. Vì vị trí tới hạn cuối cùng nằm trước hẳn $l-1$, tổng của $a[p+1 \ldots l-1]$ không âm. Do đó, chuyển $l$ về $p+1$ sẽ làm tổng tăng lên hoặc ít nhất không đổi.

Vì vậy, khi tìm đáp án, ta có thể chỉ xét các đoạn bắt đầu ngay sau những vị trí xuất hiện $s<0$. Điều này chứng minh tính đúng đắn của thuật toán.

### Cài đặt

Như thuật toán 1, trước tiên ta đưa ra phiên bản đơn giản chỉ tìm giá trị đáp án mà không tìm các đầu mút:

```cpp
int ans = a[0], sum = 0;

for (int r = 0; r < n; ++r) {
    sum += a[r];
    ans = max(ans, sum);
    sum = max(sum, 0);
}
```

Lời giải đầy đủ, lưu cả chỉ số hai đầu mút của đoạn tương ứng:

```cpp
int ans = a[0], ans_l = 0, ans_r = 0;
int sum = 0, minus_pos = -1;

for (int r = 0; r < n; ++r) {
    sum += a[r];
    if (sum > ans) {
        ans = sum;
        ans_l = minus_pos + 1;
        ans_r = r;
    }
    if (sum < 0) {
        sum = 0;
        minus_pos = r;
    }
}
```

## Các bài toán liên quan

### Tìm đoạn con có tổng lớn nhất hoặc nhỏ nhất với ràng buộc

Nếu đề bài áp đặt thêm ràng buộc lên đoạn $[l, r]$ cần tìm, chẳng hạn độ dài $r-l+1$ phải nằm trong giới hạn cho trước, thuật toán trên thường có thể mở rộng cho những trường hợp đó: về bản chất ta vẫn cần tìm giá trị nhỏ nhất trong mảng $s[]$ với các ràng buộc bổ sung tương ứng.

### Trường hợp hai chiều: tìm ma trận con có tổng lớn nhất hoặc nhỏ nhất

Bài toán trong bài viết có thể mở rộng tự nhiên sang nhiều chiều. Chẳng hạn, trong hai chiều, ta cần tìm ma trận con $[l_1 \ldots r_1, l_2 \ldots r_2]$ có tổng các phần tử lớn nhất.

Dùng lời giải một chiều, ta dễ dàng có thuật toán $O(n^3)$ cho trường hợp hai chiều: duyệt mọi giá trị có thể của $l_1$ và $r_1$, tính tổng từ $l_1$ đến $r_1$ trên từng hàng. Ta thu được bài toán một chiều tìm $l_2$ và $r_2$ trong mảng này, có thể giải trong thời gian tuyến tính.

Có các thuật toán **nhanh hơn**, nhưng không nhanh hơn nhiều so với $O(n^3)$ và rất phức tạp; hằng số ẩn khiến nhiều thuật toán trong số đó kém hơn cách thông thường ở mọi giới hạn đầu vào hợp lý. Hiện thuật toán tốt nhất được biết đến chạy trong thời gian $O\left(n^3 \frac{ \log^3 \log n }{ \log^2 n} \right)$ (T. Chan, 2007, "More algorithms for all-pairs shortest paths in weighted graphs").

Thuật toán của Chan và nhiều kết quả khác trong lĩnh vực này thực chất mô tả **phép nhân ma trận nhanh**, trong đó phép nhân được sửa đổi: lấy giá trị nhỏ nhất thay cho phép cộng và lấy phép cộng thay cho phép nhân. Bài toán tìm ma trận con có tổng lớn nhất có thể quy về tìm đường đi ngắn nhất giữa mọi cặp đỉnh; bài toán đó lại quy được về phép nhân ma trận như trên.

### Tìm đoạn con có trung bình lớn nhất hoặc nhỏ nhất

Bài toán yêu cầu tìm đoạn $a[l, r]$ có giá trị trung bình lớn nhất:

$$ \max_{l \le r} \frac{ 1 }{ r-l+1 } \sum_{i=l}^{r} a[i].$$

Nếu không có điều kiện bổ sung cho đoạn $[l, r]$, đáp án luôn là đoạn độ dài $1$ tại phần tử lớn nhất. Bài toán chỉ có ý nghĩa khi có thêm ràng buộc, chẳng hạn độ dài đoạn cần tìm có cận dưới.

Trong trường hợp này, ta áp dụng **kỹ thuật chuẩn** cho các bài toán giá trị trung bình: tìm giá trị trung bình lớn nhất bằng **tìm kiếm nhị phân**.

Ta cần giải bài toán con sau: cho số $x$, kiểm tra xem có đoạn con nào của mảng $a[]$ thỏa mọi ràng buộc bổ sung và có trung bình lớn hơn $x$ hay không.

Để giải, trừ $x$ khỏi từng phần tử của mảng $a[]$. Khi đó bài toán con trở thành kiểm tra xem có đoạn con nào có tổng dương hay không; ta đã biết cách giải bài toán này.

Như vậy ta có lời giải với độ phức tạp $O(T(n) \log W)$, trong đó $W$ là độ chính xác cần đạt và $T(n)$ là thời gian giải bài toán con trên mảng độ dài $n$, có thể thay đổi tùy các ràng buộc cụ thể.

**Ghi chú của người dịch:** Số bước tìm kiếm nhị phân còn phụ thuộc độ rộng khoảng tìm kiếm ban đầu và sai số cho phép. Với khoảng độ rộng D và sai số tuyệt đối epsilon dương, số bước tỷ lệ logarit của D chia cho epsilon; vì vậy cách viết theo W ở nguồn cần làm rõ quy ước về độ chính xác và khoảng tìm kiếm.

### Giải bài toán trực tuyến

Cho một mảng gồm $n$ số và một số $L$. Với mỗi truy vấn dạng $(l,r)$, cần tìm một đoạn con của đoạn $[l, r]$ có độ dài không nhỏ hơn $L$ và có trung bình cộng lớn nhất có thể.

Thuật toán giải bài toán này khá phức tạp. KADR (Yaroslav Tverdokhleb) đã mô tả thuật toán của mình trên [diễn đàn tiếng Nga](http://e-maxx.ru/forum/viewtopic.php?id=410).
