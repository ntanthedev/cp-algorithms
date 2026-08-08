---
tags:
  - Translated
e_maxx_link: length_of_segments_union
translation:
  source: geometry/length-of-segments-union.md
  source_commit: 2c82fa39bc578f39e0aa48c1efc586c7e518ee21
  status: draft
  last_synced: 2026-08-08
---

# Độ dài hợp của các đoạn thẳng

Cho $n$ đoạn thẳng trên một đường thẳng, mỗi đoạn được mô tả bởi một cặp tọa độ $(a_{i1}, a_{i2})$.
Ta cần tìm độ dài hợp của chúng.

Thuật toán sau do Klee đề xuất vào năm 1977.
Thuật toán chạy trong $O(n\log n)$ và đã được chứng minh là tối ưu về mặt tiệm cận.

## Lời giải

Ta lưu các đầu mút của mọi đoạn vào một mảng $x$ và sắp xếp theo giá trị tọa độ.
Đồng thời, ta lưu thêm thông tin mỗi đầu mút là đầu trái hay đầu phải của một đoạn.
Sau đó duyệt mảng, duy trì một biến đếm $c$ là số đoạn hiện đang mở.
Khi phần tử hiện tại là đầu trái, ta tăng biến đếm; ngược lại, nếu là đầu phải thì giảm biến đếm.
Để tính đáp án, mỗi khi chuyển sang một tọa độ mới và hiện có ít nhất một đoạn đang mở, ta cộng độ dài giữa hai giá trị $x$ liên tiếp $x_i - x_{i-1}$ vào kết quả.

## Cài đặt

```cpp
int length_union(const vector<pair<int, int>> &a) {
    int n = a.size();
    vector<pair<int, bool>> x(n*2);
    for (int i = 0; i < n; i++) {
        x[i*2] = {a[i].first, false};
        x[i*2+1] = {a[i].second, true};
    }

    sort(x.begin(), x.end());

    int result = 0;
    int c = 0;
    for (int i = 0; i < n * 2; i++) {
        if (i > 0 && x[i].first > x[i-1].first && c > 0)
            result += x[i].first - x[i-1].first;
        if (x[i].second)
            c--;
        else
            c++;
    }
    return result;
}
```
