---
tags:
  - Translated
e_maxx_link: matrix_rank
translation:
  source: linear_algebra/rank-matrix.md
  source_commit: ea446f196bce1580daffc2bea84bb742c9462375
  status: draft
  last_synced: 2026-11-15
---

# Tìm hạng của ma trận

**Hạng của ma trận** là số lượng lớn nhất các hàng hoặc các cột độc lập tuyến tính. Hạng không chỉ được định nghĩa cho ma trận vuông.

Hạng của ma trận còn có thể được định nghĩa là cấp lớn nhất của một định thức con (minor) khác 0.

Xét ma trận chữ nhật có kích thước $N \times M$.
Lưu ý rằng nếu ma trận vuông có định thức khác 0, thì hạng của nó bằng $N$ ($=M$); nếu không, hạng sẽ nhỏ hơn. Nói chung, hạng của ma trận không vượt quá $\min (N, M)$.

## Thuật toán

Ta có thể tìm hạng bằng phép khử Gauss như trong [bài giải hệ phương trình tuyến tính](linear-system-gauss.md). Ta thực hiện các phép biến đổi giống như khi giải hệ hoặc tính định thức. Tuy nhiên, nếu trong cột thứ $i$ không có hàng nào chưa được chọn chứa phần tử khác 0, ta bỏ qua bước này.
Ngược lại, nếu trong bước thứ $i$ ta tìm được một hàng có phần tử khác 0 ở cột thứ $i$, ta đánh dấu hàng đó là đã chọn, tăng hạng lên một (ban đầu hạng bằng $0$), rồi thực hiện phép biến đổi thông thường: trừ bội của hàng này khỏi các hàng còn lại.

## Độ phức tạp

Thuật toán này chạy trong thời gian $\mathcal{O}(n^3)$.

**Ghi chú bản dịch:** Trong mã dưới đây, n là số hàng và m là số cột. Với ma trận chữ nhật không rỗng, thời gian chạy phụ thuộc cả hai kích thước và có cận trên $O(nm\min(n,m))$. Khi ma trận vuông, cận này trở thành $O(n^3)$.

## Cài đặt

```{.cpp file=matrix-rank}
const double EPS = 1E-9;

int compute_rank(vector<vector<double>> A) {
    int n = A.size();
    int m = A[0].size();

    int rank = 0;
    vector<bool> row_selected(n, false);
    for (int i = 0; i < m; ++i) {
        int j;
        for (j = 0; j < n; ++j) {
            if (!row_selected[j] && abs(A[j][i]) > EPS)
                break;
        }

        if (j != n) {
            ++rank;
            row_selected[j] = true;
            for (int p = i + 1; p < m; ++p)
                A[j][p] /= A[j][i];
            for (int k = 0; k < n; ++k) {
                if (k != j && abs(A[k][i]) > EPS) {
                    for (int p = i + 1; p < m; ++p)
                        A[k][p] -= A[j][p] * A[k][i];
                }
            }
        }
    }
    return rank;
}
```
## Bài tập

 * [TIMUS1041 Nikifor](http://acm.timus.ru/problem.aspx?space=1&num=1041)
