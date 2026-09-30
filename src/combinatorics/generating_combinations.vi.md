---
title: Generating all K-combinations
tags:
  - Translated
e_maxx_link: generating_combinations
translation:
  source: combinatorics/generating_combinations.md
  source_commit: d2d5513d186a4a28d367b4f9c72fb84d396dc6a5
  status: draft
  last_synced: 2026-09-30
---
# Sinh tất cả tổ hợp $K$ phần tử

Trong bài viết này, ta sẽ xét bài toán sinh tất cả các tổ hợp $K$ phần tử.
Cho hai số tự nhiên $N$ và $K$, xét tập các số từ $1$ đến $N$.
Nhiệm vụ là liệt kê tất cả **các tập con có kích thước $K$**.

## Sinh tổ hợp $K$ phần tử kế tiếp theo thứ tự từ điển {data-toc-label="Generate next lexicographical K-combination"}

Trước tiên, ta sẽ sinh các tổ hợp theo thứ tự từ điển.
Thuật toán cho việc này khá đơn giản. Tổ hợp đầu tiên là ${1, 2, ..., K}$. Bây giờ hãy xem cách
tìm tổ hợp đứng ngay sau tổ hợp hiện tại theo thứ tự từ điển. Ta xét tổ hợp hiện tại và tìm
phần tử ngoài cùng bên phải chưa đạt giá trị lớn nhất có thể của nó. Sau khi tìm được phần tử này,
ta tăng nó thêm $1$, rồi gán cho tất cả các phần tử phía sau những giá trị hợp lệ nhỏ nhất.

```{.cpp file=next_combination}
bool next_combination(vector<int>& a, int n) {
    int k = (int)a.size();
    for (int i = k - 1; i >= 0; i--) {
        if (a[i] < n - k + i + 1) {
            a[i]++;
            for (int j = i + 1; j < k; j++)
                a[j] = a[j - 1] + 1;
            return true;
        }
    }
    return false;
}
```

## Sinh tất cả tổ hợp $K$ phần tử sao cho hai tổ hợp kề nhau chỉ khác một phần tử {data-toc-label="Generate all K-combinations such that adjacent combinations differ by one element"}

Lần này, ta muốn sinh tất cả các tổ hợp $K$ phần tử theo một thứ tự sao cho
hai tổ hợp kề nhau khác nhau đúng một phần tử.

Ta có thể giải bài toán này bằng [mã Gray](../algebra/gray-code.md):
Nếu gán một bitmask cho mỗi tập con, thì bằng cách sinh và duyệt các bitmask theo mã Gray, ta có thể thu được đáp án.

Bài toán sinh các tổ hợp $K$ phần tử cũng có thể được giải bằng mã Gray theo một cách khác:
Sinh các mã Gray cho các số từ $0$ đến $2^N - 1$ và chỉ giữ lại những mã chứa $K$ bit $1$.
Điều đáng chú ý là trong dãy thu được gồm các mask có $K$ bit được bật, mọi cặp mask kề nhau (kể cả
mask đầu tiên và cuối cùng, nếu coi chúng kề nhau theo chu kỳ) sẽ khác nhau đúng hai bit, đúng với mục tiêu của ta (xóa
một số và thêm một số).

Ta sẽ chứng minh điều này:

Trong chứng minh, ta nhắc lại rằng dãy $G(N)$ (biểu diễn mã Gray thứ $N$<sup></sup>) có thể
được xây dựng như sau:

$$G(N) = 0G(N-1) \cup 1G(N-1)^\text{R}$$

Tức là, lấy dãy mã Gray với $N-1$ bit và thêm tiền tố $0$ vào trước mỗi phần tử. Sau đó lấy
dãy mã Gray với $N-1$ bit theo thứ tự đảo ngược, thêm tiền tố $1$ vào trước mỗi mask, rồi
nối hai dãy này lại.

Bây giờ ta có thể tiến hành chứng minh.

Trước hết, ta chứng minh rằng mask đầu tiên và mask cuối cùng khác nhau đúng hai bit. Chỉ cần nhận xét
rằng mask đầu tiên của dãy $G(N)$ có dạng $N-K$ bit $0$, tiếp theo là $K$ bit $1$. Cụ thể,
bit đầu tiên là $0$, sau đó là $(N-K-1)$ bit $0$, rồi đến $K$ bit được bật; còn mask cuối cùng có dạng $1$, tiếp theo là $(N-K)$ bit $0$, rồi đến $K-1$ bit $1$.
Áp dụng nguyên lý quy nạp toán học cùng công thức của $G(N)$ sẽ hoàn tất chứng minh.

Tiếp theo, ta cần chỉ ra rằng mọi cặp mã kề nhau cũng khác nhau đúng hai bit. Ta có thể làm điều này bằng cách xét phương trình đệ quy để sinh mã Gray. Giả sử mệnh đề đã đúng với nội dung của hai nửa được tạo từ $G(N-1)$. Khi đó chỉ còn phải chứng minh rằng cặp phần tử kề mới xuất hiện tại điểm nối của hai nửa cũng hợp lệ, tức là chúng khác nhau đúng hai bit.

Điều này suy ra từ việc ta biết mask cuối cùng của nửa thứ nhất và mask đầu tiên của nửa thứ hai. Mask cuối cùng của nửa thứ nhất có dạng $1$, tiếp theo là $(N-K-1)$ bit $0$, rồi đến $K-1$ bit $1$. Mask đầu tiên của nửa thứ hai có dạng $0$, tiếp theo là $(N-K-2)$ bit $0$, rồi đến $K$ bit $1$. Vì vậy, khi so sánh hai mask này, ta thấy có đúng hai bit khác nhau.

Dưới đây là một cài đặt đơn giản bằng cách sinh toàn bộ $2^{n}$ tập con có thể có rồi chọn những tập con có kích thước
$K$.

```{.cpp file=generate_all_combinations_naive}
int gray_code (int n) {
    return n ^ (n >> 1);
}

int count_bits (int n) {
    int res = 0;
    for (; n; n >>= 1)
        res += n & 1;
    return res;
}

void all_combinations (int n, int k) {
    for (int i = 0; i < (1 << n); i++) {
        int cur = gray_code (i);
        if (count_bits(cur) == k) {
            for (int j = 0; j < n; j++) {
                if (cur & (1 << j))
                    cout << j + 1;
            }
            cout << "\n";
        }
    }
}
```

Cũng cần nhắc rằng có một cài đặt hiệu quả hơn, chỉ xây dựng các tổ hợp hợp lệ và do đó
chạy trong $O\left(N \cdot \binom{N}{K}\right)$. Tuy nhiên, cách này dùng đệ quy và với các giá trị $N$ nhỏ, hệ số hằng số
có thể lớn hơn lời giải trước.

Cài đặt này được suy ra từ công thức:

$$G(N, K) = 0G(N-1, K) \cup 1G(N-1, K-1)^\text{R}$$

Công thức này thu được bằng cách điều chỉnh phương trình tổng quát dùng để xác định mã Gray, rồi chọn
dãy con gồm các phần tử phù hợp.

Cài đặt như sau:

```{.cpp file=generate_all_combinations_fast}
vector<int> ans;

void gen(int n, int k, int idx, bool rev) {
    if (k > n || k < 0)
        return;

    if (!n) {
        for (int i = 0; i < idx; ++i) {
            if (ans[i])
                cout << i + 1;
        }
        cout << "\n";
        return;
    }

    ans[idx] = rev;
    gen(n - 1, k - rev, idx + 1, false);
    ans[idx] = !rev;
    gen(n - 1, k - !rev, idx + 1, true);
}

void all_combinations(int n, int k) {
    ans.resize(n);
    gen(n, k, 0, false);
}
```
