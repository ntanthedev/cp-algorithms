---
tags:
  - Translated
e_maxx_link: rmq_linear
translation:
  source: graph/rmq_linear.md
  source_commit: 115a730d307171f3f4e803a2372fcdd78550461d
  status: draft
  last_synced: 2026-11-15
---

# Giải RMQ (truy vấn giá trị nhỏ nhất trên đoạn) bằng cách tìm LCA (tổ tiên chung gần nhất)

Cho mảng `A[0..N-1]`.
Với mỗi truy vấn dạng `[L, R]`, ta cần tìm giá trị nhỏ nhất trong mảng `A` từ vị trí `L` đến vị trí `R`.
Ta giả sử mảng `A` không thay đổi trong quá trình xử lý; do đó, bài viết này trình bày lời giải cho bài toán RMQ tĩnh.

Sau đây là một lời giải tối ưu về mặt tiệm cận.
Lời giải này khác hẳn các phương pháp RMQ khác:
ta rút gọn bài toán RMQ thành bài toán LCA, rồi dùng [thuật toán Farach-Colton và Bender](lca_farachcoltonbender.md), thuật toán này lại rút gọn LCA thành một bài toán RMQ chuyên biệt và giải bài toán đó.

## Thuật toán

Ta dựng một **cây Cartesian** từ mảng `A`.
Cây Cartesian của mảng `A` là cây nhị phân thỏa tính chất min-heap, tức giá trị của nút cha không lớn hơn giá trị các nút con; đồng thời, phép duyệt theo thứ tự trái–nút–phải đi qua các nút theo đúng thứ tự của chúng trong mảng `A`.

Nói cách khác, cây Cartesian là một cấu trúc dữ liệu được định nghĩa đệ quy.
Ta chia mảng `A` thành ba phần: đoạn đầu đến trước phần tử nhỏ nhất, chính phần tử nhỏ nhất đó, và đoạn còn lại phía sau.
Gốc cây là nút ứng với phần tử nhỏ nhất của mảng `A`; cây con trái là cây Cartesian của đoạn đầu, còn cây con phải là cây Cartesian của đoạn phía sau.

Trong hình dưới đây là một mảng có độ dài 10 và cây Cartesian tương ứng.
<div style="text-align: center;">
  <img src="CartesianTree.png" alt="Minh họa cây Cartesian">
</div>

Truy vấn tìm giá trị nhỏ nhất trên đoạn `[l, r]` tương đương với truy vấn tổ tiên chung gần nhất của hai nút `[l', r']`, trong đó `l'` là nút ứng với phần tử `A[l]` và `r'` là nút ứng với phần tử `A[r]`.
Nút ứng với phần tử nhỏ nhất trong đoạn phải là tổ tiên của mọi nút trong đoạn, nên cũng là tổ tiên của `l'` và `r'`.
Điều này suy ra trực tiếp từ tính chất đống tối tiểu.
Nút đó cũng phải là tổ tiên chung thấp nhất; nếu không, `l'` và `r'` sẽ cùng nằm trong cây con trái hoặc cùng nằm trong cây con phải, dẫn đến mâu thuẫn vì khi ấy phần tử nhỏ nhất không thể nằm trong đoạn truy vấn.

Hình dưới đây minh họa các truy vấn LCA ứng với hai truy vấn RMQ `[1, 3]` và `[5, 9]`.
Trong truy vấn thứ nhất, LCA của các nút `A[1]` và `A[3]` là nút ứng với `A[2]`, có giá trị 2.
Trong truy vấn thứ hai, LCA của các nút `A[5]` và `A[9]` là nút ứng với `A[8]`, có giá trị 3.

<div style="text-align: center;">
  <img src="CartesianTreeLCA.png" alt="Các truy vấn LCA trên cây Cartesian">
</div>

Ta có thể dựng cây này trong $O(N)$ thời gian; thuật toán Farach-Colton và Bender tiền xử lý cây trong $O(N)$ và trả lời mỗi truy vấn LCA trong $O(1)$.

## Dựng cây Cartesian

Ta dựng cây Cartesian bằng cách lần lượt thêm từng phần tử.
Mỗi bước, ta duy trì một cây Cartesian hợp lệ chứa tất cả phần tử đã xử lý.
Dễ thấy khi thêm phần tử `s[i]`, chỉ các nút trên đường biên phải của cây mới có thể thay đổi — đường đi bắt đầu từ gốc rồi liên tục đi theo cạnh con phải.
Cây con của nút có giá trị nhỏ nhất nhưng lớn hơn hoặc bằng `s[i]` trở thành cây con trái của `s[i]`.
Cây có gốc là `s[i]` sẽ trở thành cây con phải mới của nút có giá trị lớn nhất nhưng nhỏ hơn `s[i]`.

Ta có thể cài đặt cách này bằng một ngăn xếp lưu chỉ số của các nút trên đường biên phải.

```cpp
vector<int> parent(n, -1);
stack<int> s;
for (int i = 0; i < n; i++) {
    int last = -1;
    while (!s.empty() && A[s.top()] >= A[i]) {
        last = s.top();
        s.pop();
    }
    if (!s.empty())
        parent[i] = s.top();
    if (last >= 0)
        parent[last] = i;
    s.push(i);
}
```
