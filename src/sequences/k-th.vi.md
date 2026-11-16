---
title: K-th order statistic in O(N)
tags:
  - Translated
e_maxx_link: kth_order_statistics
translation:
  source: sequences/k-th.md
  source_commit: 0f588c5cbef193c61d2e4634e5a0b2eed98c4177
  status: draft
  last_synced: 2026-11-15
---
# Thống kê thứ tự thứ $K$ trong $O(N)$

Cho một mảng $A$ có kích thước $N$ và một số $K$. Bài toán là tìm số lớn thứ $K$ trong mảng, tức thống kê thứ tự thứ $K$.

Ý tưởng cơ bản là dùng ý tưởng của thuật toán quick sort. Bản thân thuật toán đơn giản; phần khó hơn là chứng minh thời gian chạy trung bình của nó là $O(N)$, khác với quick sort.

## Cài đặt (không đệ quy)

```cpp
template <class T>
T order_statistics (std::vector<T> a, unsigned n, unsigned k)
{
    using std::swap;
    for (unsigned l=1, r=n; ; )
    {
        if (r <= l+1)
        {
            // the current part size is either 1 or 2, so it is easy to find the answer
            if (r == l+1 && a[r] < a[l])
                swap (a[l], a[r]);
            return a[k];
        }

        // ordering a[l], a[l+1], a[r]
        unsigned mid = (l + r) >> 1;
        swap (a[mid], a[l+1]);
        if (a[l] > a[r])
            swap (a[l], a[r]);
        if (a[l+1] > a[r])
            swap (a[l+1], a[r]);
        if (a[l] > a[l+1])
            swap (a[l], a[l+1]);

        // performing division
        // barrier is a[l + 1], i.e. median among a[l], a[l + 1], a[r]
        unsigned
            i = l+1,
            j = r;
        const T
            cur = a[l+1];
        for (;;)
        {
            while (a[++i] < cur) ;
            while (a[--j] > cur) ;
            if (i > j)
                break;
            swap (a[i], a[j]);
        }

        // inserting the barrier
        a[l+1] = a[j];
        a[j] = cur;
        
        // we continue to work in that part, which must contain the required element
        if (j >= k)
            r = j-1;
        if (j <= k)
            l = i;
    }
}
```

## Ghi chú
* Thuật toán ngẫu nhiên ở trên được gọi là [quickselect](https://en.wikipedia.org/wiki/Quickselect). Nên xáo trộn ngẫu nhiên $A$ trước khi gọi hoặc dùng một phần tử ngẫu nhiên làm chốt để thuật toán hoạt động đúng cách. Cũng có những thuật toán tất định giải bài toán đã nêu trong thời gian tuyến tính, chẳng hạn [median of medians](https://en.wikipedia.org/wiki/Median_of_medians).
* [std::nth_element](https://en.cppreference.com/w/cpp/algorithm/nth_element) giải bài toán này trong C++, nhưng bản cài đặt của gcc chạy trong thời gian $O(n \log n )$ ở trường hợp xấu nhất.
* Có thể quy việc tìm $K$ phần tử nhỏ nhất về tìm phần tử thứ $K$ với chi phí bổ sung tuyến tính, vì chúng chính là các phần tử nhỏ hơn phần tử thứ $K$.

Ghi chú bản dịch: Code dùng chỉ số từ 1 đến n và trả về phần tử thứ k theo thứ tự không giảm, trong khi phần mở đầu nói số lớn thứ K. Cần cấp phát mảng có phần tử tại các chỉ số này và chọn 1 ≤ k ≤ n. Xáo trộn ngẫu nhiên giúp đạt thời gian kỳ vọng tuyến tính; code với chốt tất định vẫn đúng trên đầu vào hợp lệ nhưng có thể mất thời gian bậc hai trong trường hợp xấu nhất. Mệnh đề cuối ở trên cũng cần xét giá trị bằng phần tử thứ K: để lấy đủ K phần tử nhỏ nhất, cần chọn cả một số phần tử bằng ngưỡng nếu có giá trị trùng nhau.

## Bài tập luyện tập
- [Leetcode: Kth Largest Element in an Array](https://leetcode.com/problems/kth-largest-element-in-an-array/description/)
- [CODECHEF: Median](https://www.codechef.com/problems/CD1IT1)
