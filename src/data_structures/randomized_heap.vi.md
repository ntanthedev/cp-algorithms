---
tags:
  - Translated
e_maxx_link: randomized_heap
translation:
  source: data_structures/randomized_heap.md
  source_commit: c9e10a7837d2c93357ec8b85838ac26a6e1bdf22
  status: draft
  last_synced: 2026-11-16
---

# Heap ngẫu nhiên

Heap ngẫu nhiên là một heap sử dụng tính ngẫu nhiên để thực hiện mọi thao tác trong thời gian kỳ vọng logarit.

**Min heap** là một cây nhị phân trong đó giá trị của mỗi đỉnh không lớn hơn giá trị của các đỉnh con.
Vì vậy giá trị nhỏ nhất của cây luôn nằm ở đỉnh gốc.

Ta có thể định nghĩa max heap tương tự bằng cách thay quan hệ nhỏ hơn bằng lớn hơn.

Các thao tác thông thường của heap là:

- Thêm một giá trị
- Lấy giá trị nhỏ nhất
- Xóa giá trị nhỏ nhất
- Gộp hai heap (không xóa các phần tử trùng nhau)
- Xóa một phần tử bất kỳ (nếu biết vị trí của nó trong cây)

Heap ngẫu nhiên có thể thực hiện tất cả các thao tác này trong thời gian kỳ vọng $O(\log n)$ với cách cài đặt rất đơn giản.

## Cấu trúc dữ liệu

Ta có thể mô tả ngay cấu trúc của heap nhị phân:

```{.cpp file=randomized_heap_structure}
struct Tree {
    int value;
    Tree * l = nullptr;
    Tree * r = nullptr;
};
```

Tại mỗi đỉnh ta lưu một giá trị.
Ngoài ra, ta có các con trỏ tới đỉnh con trái và phải, mang giá trị null nếu đỉnh con tương ứng không tồn tại.

## Các thao tác

Dễ thấy mọi thao tác đều có thể đưa về một thao tác duy nhất: **gộp** hai heap thành một.
Thật vậy, thêm một giá trị vào heap tương đương với gộp heap đó với một heap chỉ gồm một đỉnh có giá trị ấy.
Tìm giá trị nhỏ nhất không cần thao tác gì: nó chính là giá trị ở gốc.
Xóa giá trị nhỏ nhất tương đương với kết quả gộp hai cây con trái và phải của đỉnh gốc.
Việc xóa một phần tử bất kỳ cũng tương tự.
Ta gộp hai cây con của đỉnh đó rồi thay đỉnh bằng kết quả gộp.

Vì vậy ta chỉ cần cài đặt thao tác gộp hai heap.
Tất cả thao tác khác đều dễ dàng đưa về thao tác này.

Cho hai heap $T_1$ và $T_2$.
Rõ ràng gốc của mỗi heap chứa giá trị nhỏ nhất của nó.
Vì vậy gốc của heap kết quả sẽ chứa giá trị nhỏ hơn trong hai giá trị đó.
Ta so sánh hai giá trị và chọn giá trị nhỏ hơn làm gốc mới.
Bây giờ ta cần kết hợp các cây con của đỉnh được chọn với heap còn lại.
Để làm vậy, ta chọn một trong hai cây con và gộp nó với heap còn lại.
Như vậy ta lại có thao tác gộp hai heap.
Quá trình này cuối cùng sẽ kết thúc (số bước như vậy bị chặn bởi tổng chiều cao của hai heap).

Để đạt độ phức tạp logarit trung bình, ta cần chọn một trong hai cây con sao cho độ dài đường đi trung bình là logarit.
Dễ đoán rằng ta sẽ quyết định điều này một cách **ngẫu nhiên**.
Do đó, thao tác gộp được cài đặt như sau:

```{.cpp file=randomized_heap_merge}
Tree* merge(Tree* t1, Tree* t2) {
    if (!t1 || !t2)
        return t1 ? t1 : t2;
    if (t2->value < t1->value)
        swap(t1, t2);
    if (rand() & 1)
        swap(t1->l, t1->r);
    t1->l = merge(t1->l, t2);
    return t1;
}
```

Đầu tiên ta kiểm tra xem một trong hai heap có rỗng hay không; nếu có thì không cần thực hiện thao tác gộp nào.
Ngược lại, ta đưa heap có giá trị nhỏ hơn về `t1` (bằng cách hoán đổi `t1` và `t2` nếu cần).
Ta muốn gộp cây con trái của `t1` với `t2`, nên ta hoán đổi ngẫu nhiên hai cây con của `t1`, rồi thực hiện phép gộp.

## Độ phức tạp

Ta đưa vào biến ngẫu nhiên $h(T)$, biểu thị **độ dài đường đi ngẫu nhiên** từ gốc đến lá (độ dài tính bằng số cạnh).
Rõ ràng thuật toán `merge` thực hiện $O(h(T_1) + h(T_2))$ bước.
Do đó, để hiểu độ phức tạp của các thao tác, ta cần xét biến ngẫu nhiên $h(T)$.

### Giá trị kỳ vọng

Ta giả sử kỳ vọng của $h(T)$ có thể được chặn trên bởi logarit của số đỉnh trong heap:

$$\mathbf{E} h(T) \le \log(n+1)$$

Điều này dễ được chứng minh bằng quy nạp.
Gọi $L$ và $R$ là cây con trái và phải của gốc $T$, còn $n_L$ và $n_R$ là số đỉnh trong chúng ($n = n_L + n_R + 1$).

Bước quy nạp như sau:

$$\begin{align}
\mathbf{E} h(T) &= 1 + \frac{\mathbf{E} h(L) + \mathbf{E} h(R)}{2} 
\le 1 + \frac{\log(n_L + 1) + \log(n_R + 1)}{2} \\\\
&= 1 + \log\sqrt{(n_L + 1)(n_R + 1)} = \log 2\sqrt{(n_L + 1)(n_R + 1)} \\\\
&\le \log \frac{2\left((n_L + 1) + (n_R + 1)\right)}{2} = \log(n_L + n_R + 2) = \log(n+1)
\end{align}$$

### Vượt quá giá trị kỳ vọng

Tất nhiên ta vẫn chưa hài lòng.
Giá trị kỳ vọng của $h(T)$ không cho biết điều gì về trường hợp xấu nhất.
Với một cây cụ thể, độ dài trung bình của các đường đi từ gốc tới các đỉnh vẫn có thể lớn hơn rất nhiều so với $\log(n + 1)$.

Hãy chứng minh xác suất vượt quá giá trị kỳ vọng thực sự rất nhỏ:

$${\cal P}(h(T) > (c+1) \log n) < \frac{1}{n^c}$$

với mọi hằng số dương $c$.

Ở đây $P$ là tập các đường đi từ gốc heap đến các lá có độ dài lớn hơn $(c+1) \log n$.
Với mỗi đường đi $p$ có độ dài $|p|$, xác suất nó được chọn làm đường đi ngẫu nhiên là $2^{-|p|}$.
Do đó:

$${\cal P}(h(T) > (c+1) \log n) = \sum_{p \in P} 2^{-|p|} < \sum_{p \in P} 2^{-(c+1) \log n} = |P| n^{-(c+1)} \le n^{-c}$$

### Độ phức tạp của thuật toán

Vậy thuật toán `merge`, và do đó tất cả các thao tác được biểu diễn bằng nó, có thể được thực hiện trong thời gian trung bình $O(\log n)$.

Hơn nữa, với mọi hằng số dương $\epsilon$, tồn tại hằng số dương $c$ sao cho xác suất một thao tác cần nhiều hơn $c \log n$ bước nhỏ hơn $n^{-\epsilon}$ (theo một nghĩa nào đó điều này mô tả hành vi trường hợp xấu nhất của thuật toán).
