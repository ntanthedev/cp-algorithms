---
tags:
  - Translated
e_maxx_link: maximum_zero_submatrix
translation:
  source: dynamic_programming/zero_matrix.md
  source_commit: 46093c4e209add821898fbf53c803c6bb10b1ecc
  status: draft
  last_synced: 2026-11-15
---

# Tìm ma trận con toàn số 0 lớn nhất

Cho một ma trận có `n` hàng và `m` cột. Hãy tìm ma trận con lớn nhất chỉ gồm các số 0 (ma trận con là một vùng hình chữ nhật của ma trận).

## Thuật toán

Gọi các phần tử của ma trận là `a[i][j]`, với `i = 0...n - 1`, `j = 0... m - 1`. Để đơn giản, ta coi mọi phần tử khác 0 đều bằng 1.

### Bước 1: Quy hoạch động phụ

Trước tiên, ta tính ma trận phụ `d[i][j]`: hàng gần nhất phía trên `a[i][j]` có phần tử bằng 1. Cụ thể, `d[i][j]` là chỉ số hàng lớn nhất (từ `0` đến `i - 1`) có phần tử bằng `1` ở cột thứ `j`.
Khi duyệt từ trên trái xuống dưới phải, tại hàng `i`, ta đã biết các giá trị của hàng trước nên chỉ cần cập nhật các phần tử có giá trị `1`. Ta có thể lưu các giá trị trong một mảng đơn giản `d[i]`, `i = 1...m - 1`, vì ở phần sau thuật toán xử lý từng hàng và chỉ cần các giá trị của hàng hiện tại.

Ghi chú bản dịch: Mã cập nhật cả hàng hiện tại: sau khi cập nhật, d[j] là chỉ số hàng gần nhất không vượt quá i có giá trị 1 ở cột j, hoặc -1 nếu không có. Mảng được truy cập với chỉ số từ 0 đến m - 1. Mã chỉ kiểm tra phần tử bằng 1; đầu vào có giá trị khác 0 cần được chuẩn hóa thành 1 trước khi gọi hàm. Mã cũng giả sử ma trận có ít nhất một hàng vì truy cập a[0].

```cpp
vector<int> d(m, -1);
for (int i = 0; i < n; ++i) {
    for (int j = 0; j < m; ++j) {
        if (a[i][j] == 1) {
            d[j] = i;
        }
    }
}
```

### Bước 2: Giải bài toán

Ta có thể giải trong $O(n m^2)$ bằng cách duyệt từng hàng và xét mọi cặp cột trái, phải của ma trận con. Cạnh dưới của hình chữ nhật là hàng hiện tại, còn `d[i][j]` giúp ta tìm hàng trên cùng. Tuy nhiên, ta có thể cải thiện đáng kể độ phức tạp.

Ma trận con toàn số 0 cần tìm bị chặn ở cả bốn phía bởi các số 1, khiến ta không thể mở rộng nó để cải thiện đáp án. Vì vậy, ta sẽ không bỏ sót đáp án nếu làm như sau: với mỗi ô `j` của hàng `i` (hàng dưới cùng của một ma trận con toàn số 0 có thể chọn), lấy `d[i][j]` làm hàng trên cùng của ma trận con hiện tại. Khi đó, ta cần xác định biên trái và phải tối ưu, tức mở rộng ma trận con này sang trái và phải của cột `j` nhiều nhất có thể.

Mở rộng tối đa sang trái nghĩa là gì? Ta tìm chỉ số `k1` sao cho `d[i][k1] > d[i][j]`, đồng thời `k1` gần `j` nhất về phía trái. Khi đó `k1 + 1` là chỉ số cột trái của ma trận con cần tìm. Nếu không có chỉ số như vậy, đặt `k1` = `-1` (nghĩa là có thể mở rộng sang trái đến tận biên ma trận `a`).

Tương tự, chỉ số `k2` cho biên phải là chỉ số gần `j` nhất về phía phải thỏa mãn `d[i][k2] > d[i][j]` (hoặc `m` nếu không có).

Nếu tìm hiệu quả được `k1` và `k2`, ta sẽ có mọi thông tin cần thiết về ma trận con toàn số 0 hiện tại. Cụ thể, diện tích của nó bằng `(i - d[i][j]) * (k2 - k1 - 1)`.

Ghi chú bản dịch: Với cách định nghĩa và mã ở trên, d[i][j] là hàng chặn ngay phía trên ma trận con; hàng trên cùng của ma trận con là d[i][j] + 1. Biên ma trận cũng có thể giới hạn khả năng mở rộng.

Làm thế nào để tìm hiệu quả các chỉ số `k1` và `k2` với `i` và `j` cố định? Ta có thể làm trong thời gian trung bình $O(1)$.

Để đạt độ phức tạp này, ta dùng stack như sau. Trước tiên xét cách tìm `k1` và lưu giá trị của nó ứng với mỗi chỉ số `j` trong hàng hiện tại `i` vào ma trận `d1[i][j]`. Ta duyệt các cột `j` từ trái sang phải và chỉ giữ trong stack các cột có `d[][]` lớn hơn hẳn `d[i][j]`. Khi chuyển từ cột `j` sang cột tiếp theo, ta cần cập nhật stack. Khi phần tử trên đỉnh stack không còn phù hợp (tức là `d[][] <= d[i][j]`), lấy nó ra. Chỉ cần lấy phần tử ở đỉnh, không cần lấy ở vị trí khác, vì stack chứa một dãy cột có `d` tăng dần.

Giá trị `d1[i][j]` của mỗi `j` bằng giá trị ở đỉnh stack tại thời điểm đó.

Quy hoạch động `d2[i][j]` để tìm `k2` được tính tương tự, chỉ khác là duyệt các cột từ phải sang trái.

Vì mỗi hàng có đúng `m` phần tử được đưa vào stack nên số lần lấy ra cũng không thể nhiều hơn. Tổng độ phức tạp là tuyến tính, do đó độ phức tạp cuối cùng của thuật toán là $O(nm)$.

Thuật toán cũng dùng $O(m)$ bộ nhớ (không tính dữ liệu đầu vào là ma trận `a[][]`).

Ghi chú bản dịch: Trong mã, khi stack rỗng, d1 và d2 lần lượt nhận -1 và m. Độ phức tạp bộ nhớ nêu trên không tính bản sao ma trận do tham số a được truyền theo giá trị. Các giá trị d trong stack giảm dần từ đáy lên đỉnh.

### Cài đặt

```cpp
int zero_matrix(vector<vector<int>> a) {
    int n = a.size();
    int m = a[0].size();

    int ans = 0;
    vector<int> d(m, -1), d1(m), d2(m);
    stack<int> st;
    for (int i = 0; i < n; ++i) {
        for (int j = 0; j < m; ++j) {
            if (a[i][j] == 1)
                d[j] = i;
        }

        for (int j = 0; j < m; ++j) {
            while (!st.empty() && d[st.top()] <= d[j])
                st.pop();
            d1[j] = st.empty() ? -1 : st.top();
            st.push(j);
        }
        while (!st.empty())
            st.pop();

        for (int j = m - 1; j >= 0; --j) {
            while (!st.empty() && d[st.top()] <= d[j])
                st.pop();
            d2[j] = st.empty() ? m : st.top();
            st.push(j);
        }
        while (!st.empty())
            st.pop();

        for (int j = 0; j < m; ++j)
            ans = max(ans, (i - d[j]) * (d2[j] - d1[j] - 1));
    }
    return ans;
}
```
