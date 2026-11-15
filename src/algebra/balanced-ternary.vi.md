---
tags:
  - Translated
e_maxx_link: balanced_ternary
translation:
  source: algebra/balanced-ternary.md
  source_commit: 6c887d02bf8d047fd22d637e886c32a5f827307b
  status: draft
  last_synced: 2026-11-15
---

# Hệ tam phân cân bằng

!["Máy tính Setun sử dụng hệ tam phân cân bằng"](https://earltcampbell.files.wordpress.com/2014/12/setun.jpeg?w=300)

Đây là một **hệ ghi số** không phổ biến nhưng vẫn là hệ định vị. Điểm đặc biệt là các chữ số có thể nhận một trong ba giá trị `-1`, `0` và `1`.
Tuy vậy, cơ số của hệ vẫn là `3` (vì có ba giá trị chữ số có thể có). Do viết `-1` thành một chữ số không thuận tiện,
ở phần sau ta dùng chữ cái `Z` để biểu diễn giá trị này. Nếu thấy hệ này khá lạ, hãy xem hình: một trong những máy tính đã sử dụng nó.

Dưới đây là một vài số đầu tiên viết trong **hệ tam phân cân bằng (balanced ternary)**:

```nohighlight
    0    0
    1    1
    2    1Z
    3    10
    4    11
    5    1ZZ
    6    1Z0
    7    1Z1
    8    10Z
    9    100
```

Hệ này cho phép viết số âm mà không cần dấu trừ đứng đầu: chỉ cần đổi dấu các chữ số của một số dương bất kỳ.

```nohighlight
    -1   Z
    -2   Z1
    -3   Z0
    -4   ZZ
    -5   Z11
```

Lưu ý rằng số âm bắt đầu bằng `Z`, còn số dương bắt đầu bằng `1`.

## Thuật toán chuyển đổi

Ta có thể dễ dàng biểu diễn một số cho trước trong **hệ tam phân cân bằng** bằng cách tạm thời biểu diễn nó trong hệ tam phân thông thường. Trong
hệ tam phân thông thường, các chữ số là `0`, `1` hoặc `2`. Duyệt từ chữ số thấp nhất, ta có thể giữ nguyên các chữ số `0` và `1`,
nhưng phải đổi `2` thành `Z` và cộng `1` vào chữ số kế tiếp bên trái. Các chữ số `3` được đổi thành `0` theo cách tương tự: ban đầu số không có chữ số 3, nhưng chúng có thể xuất hiện sau khi tăng một chữ số `2`.

**Ví dụ 1:** Hãy đổi `64` sang hệ tam phân cân bằng. Trước hết, ta viết lại số trong hệ tam phân thông thường:

$$ 64_{10} = 02101_{3} $$

Ta xử lý từ chữ số thấp nhất (ngoài cùng bên phải):

- Giữ nguyên `1`, `0` và `1`. (Vì `0` và `1` đều là chữ số hợp lệ trong hệ tam phân cân bằng.)
- Đổi `2` thành `Z` và tăng chữ số bên trái lên 1; ta được `1Z101`.

Kết quả cuối cùng là `1Z101`.

Ta có thể đổi số này về hệ thập phân bằng cách cộng các giá trị theo vị trí:

$$ 1Z101 = 81 \cdot 1 + 27 \cdot (-1) + 9 \cdot 1 + 3 \cdot 0 + 1 \cdot 1 = 64_{10} $$

**Ví dụ 2:** Hãy đổi `237` sang hệ tam phân cân bằng. Trước hết, ta viết lại số trong hệ tam phân thông thường:

$$ 237_{10} = 22210_{3} $$

Ta xử lý từ chữ số thấp nhất (ngoài cùng bên phải):

- Giữ nguyên `0` và `1`. (Vì `0` và `1` đều là chữ số hợp lệ trong hệ tam phân cân bằng.)
- Đổi `2` thành `Z` và tăng chữ số bên trái lên 1; ta được `23Z10`.
- Đổi `3` thành `0` và tăng chữ số bên trái lên 1; ta được `30Z10`.
- Tiếp tục đổi `3` thành `0` và tăng chữ số bên trái lên 1 (mặc định chữ số này là `0`), ta được `100Z10`.

Kết quả cuối cùng là `100Z10`.

Ta có thể đổi số này về hệ thập phân bằng cách cộng các giá trị theo vị trí:

$$ 100Z10 = 243 \cdot 1 + 81 \cdot 0 + 27 \cdot 0 + 9 \cdot (-1) + 3 \cdot 1 + 1 \cdot 0 = 237_{10} $$

## Bài tập thực hành

* [Topcoder SRM 604, Div1-250](http://community.topcoder.com/stat?c=problem_statement&pm=12917&rd=15837)
