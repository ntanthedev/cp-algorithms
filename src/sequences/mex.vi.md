---
tags:
    - Original
title: MEX (minimal excluded) of a sequence
translation:
  source: sequences/mex.md
  source_commit: f9976ace31aafc6cd24f5f22f7944f2a4cc657aa
  status: draft
  last_synced: 2026-11-15
---
# MEX (số không xuất hiện nhỏ nhất) của một dãy

Cho mảng $A$ gồm $N$ phần tử. Ta cần tìm số nguyên không âm nhỏ nhất không xuất hiện trong mảng. Số đó thường được gọi là **MEX** (minimal excluded).

$$
\begin{align}
\text{mex}(\{0, 1, 2, 4, 5\}) &= 3 \\
\text{mex}(\{0, 1, 2, 3, 4\}) &= 5 \\
\text{mex}(\{1, 2, 3, 4, 5\}) &= 0 \\
\end{align}
$$

Lưu ý rằng MEX của một mảng có kích thước $N$ không bao giờ lớn hơn $N$.

Cách đơn giản nhất là tạo một tập hợp chứa mọi phần tử của mảng $A$ để có thể kiểm tra nhanh một số có thuộc mảng hay không.
Sau đó, ta kiểm tra các số từ $0$ đến $N$; nếu số đang xét không thuộc tập hợp thì trả về số đó.

## Cài đặt

Thuật toán sau chạy trong thời gian $O(N \log N)$.

```{.cpp file=mex_simple}
int mex(vector<int> const& A) {
    set<int> b(A.begin(), A.end());

    int result = 0;
    while (b.count(result))
        ++result;
    return result;
}
```

Nếu cần tính MEX trong $O(N)$, ta có thể dùng mảng boolean thay cho tập hợp.
Lưu ý rằng mảng này cần có kích thước tương ứng với kích thước lớn nhất có thể của mảng đầu vào.


```{.cpp file=mex_linear}
int mex(vector<int> const& A) {
    static bool used[MAX_N+1] = { 0 };

    // mark the given numbers
    for (int x : A) {
        if (x <= MAX_N)
            used[x] = true;
    }

    // find the mex
    int result = 0;
    while (used[result])
        ++result;
 
    // clear the array again
    for (int x : A) {
        if (x <= MAX_N)
            used[x] = false;
    }

    return result;
}
```

Ghi chú bản dịch: Đoạn code trên giả sử các phần tử không âm và kích thước đầu vào không vượt quá MAX_N. Nếu có phần tử âm, phép truy cập used[x] vượt phạm vi mảng.

Cách này nhanh, nhưng chỉ hoạt động tốt khi cần tính MEX một lần.
Nếu cần tính MEX nhiều lần, ví dụ do mảng liên tục thay đổi, cách này không hiệu quả.
Khi đó ta cần một cách tốt hơn.

## MEX khi cập nhật mảng

Trong bài toán này, ta cần thay đổi từng phần tử của mảng và tính MEX mới sau mỗi lần cập nhật.

Ta cần một cấu trúc dữ liệu tốt hơn để xử lý các truy vấn này hiệu quả.

Một cách là lấy tần suất của từng số từ $0$ đến $N$ rồi xây dựng một cấu trúc dữ liệu dạng cây trên đó.
Ví dụ, ta có thể dùng cây đoạn hoặc treap.
Mỗi nút biểu diễn một khoảng các số; ngoài tổng tần suất trong khoảng, ta lưu thêm số lượng giá trị phân biệt trong khoảng đó.
Có thể cập nhật cấu trúc này trong $O(\log N)$ và tìm MEX trong $O(\log N)$ bằng tìm kiếm nhị phân trên cây.
Nếu nút biểu diễn khoảng $[0, \lfloor N/2 \rfloor)$ không chứa đủ $\lfloor N/2 \rfloor$ số phân biệt, thì có một số bị thiếu và MEX nhỏ hơn $\lfloor N/2 \rfloor$; ta tiếp tục đệ quy ở nhánh trái. Ngược lại, MEX ít nhất bằng $\lfloor N/2 \rfloor$ và ta tiếp tục ở nhánh phải.

Ta cũng có thể dùng các cấu trúc `map` và `set` trong thư viện chuẩn (dựa trên cách được giải thích [tại đây](https://codeforces.com/blog/entry/81287?#comment-677837)).
Ta dùng `map` để lưu tần suất mỗi số và `set` để biểu diễn các số hiện không có trong mảng.
Vì `set` được sắp thứ tự, `*set.begin()` sẽ là MEX.
Tổng thời gian tiền xử lý là $O(N \log N)$; sau đó có thể lấy MEX trong $O(1)$ và thực hiện một lần cập nhật trong $O(\log N)$.

```{.cpp file=mex_updates}
class Mex {
private:
    map<int, int> frequency;
    set<int> missing_numbers;
    vector<int> A;

public:
    Mex(vector<int> const& A) : A(A) {
        for (int i = 0; i <= A.size(); i++)
            missing_numbers.insert(i);

        for (int x : A) {
            ++frequency[x];
            missing_numbers.erase(x);
        }
    }

    int mex() {
        return *missing_numbers.begin();
    }

    void update(int idx, int new_value) {
        if (--frequency[A[idx]] == 0)
            missing_numbers.insert(A[idx]);
        A[idx] = new_value;
        ++frequency[new_value];
        missing_numbers.erase(new_value);
    }
};
```

Ghi chú bản dịch: Trong Mex::update, nếu giá trị cũ nằm ngoài đoạn từ 0 đến N, code vẫn đưa nó vào missing_numbers khi tần suất về 0. Vì vậy ví dụ này cần giả sử các giá trị cập nhật và ban đầu nằm trong đoạn đó; nếu không, tập hợp có thể chứa số âm và trả về MEX sai.

## Bài tập luyện tập

- [AtCoder: Neq Min](https://atcoder.jp/contests/hhkb2020/tasks/hhkb2020_c)
- [Codeforces: Informatics in MAC](https://codeforces.com/contest/1935/problem/B)
- [Codeforces: Replace by MEX](https://codeforces.com/contest/1375/problem/D)
- [Codeforces: Vitya and Strange Lesson](https://codeforces.com/problemset/problem/842/D)
- [Codeforces: MEX Queries](https://codeforces.com/contest/817/problem/F)
