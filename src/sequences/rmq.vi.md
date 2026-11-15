---
tags:
  - Translated
e_maxx_link: rmq
translation:
  source: sequences/rmq.md
  source_commit: cb4fa522d29fee5c2ed5c2b8f660874b0fecd07b
  status: draft
  last_synced: 2026-11-15
---

# Truy vấn giá trị nhỏ nhất trên đoạn

Cho một mảng $A[1..N]$.
Ta cần trả lời các truy vấn dạng $(L, R)$: tìm phần tử nhỏ nhất trong mảng $A$ từ vị trí $L$ đến $R$, tính cả hai đầu mút.

RMQ có thể xuất hiện trực tiếp trong bài toán hoặc được áp dụng vào các bài toán khác, chẳng hạn bài toán [tổ tiên chung thấp nhất](../graph/lca.md).

## Lời giải

Có nhiều cách tiếp cận và cấu trúc dữ liệu có thể dùng để giải bài toán RMQ.

Dưới đây là những cách được giải thích trên trang này.

Trước hết là các cách cho phép thay đổi mảng giữa các truy vấn.

- [Phân hoạch căn bậc hai](../data_structures/sqrt_decomposition.md) - trả lời mỗi truy vấn trong $O(\sqrt{N})$, tiền xử lý trong $O(N)$.
  Ưu điểm: cấu trúc dữ liệu rất đơn giản. Nhược điểm: độ phức tạp kém hơn.
- [Cây đoạn](../data_structures/segment_tree.md) - trả lời mỗi truy vấn trong $O(\log N)$, tiền xử lý trong $O(N)$.
  Ưu điểm: độ phức tạp thời gian tốt. Nhược điểm: lượng code lớn hơn so với các cấu trúc dữ liệu khác.
- [Cây Fenwick](../data_structures/fenwick.md) - trả lời mỗi truy vấn trong $O(\log N)$, tiền xử lý trong $O(N \log N)$.
  Ưu điểm: code ngắn nhất, độ phức tạp thời gian tốt. Nhược điểm: cây Fenwick chuẩn cho RMQ chỉ hỗ trợ truy vấn tiền tố ($L = 1$).

Tiếp theo là các cách chỉ hoạt động trên mảng tĩnh, tức là không thể thay đổi một giá trị trong mảng mà không tính lại toàn bộ cấu trúc dữ liệu.

- [Sparse Table](../data_structures/sparse-table.md) - trả lời mỗi truy vấn trong $O(1)$, tiền xử lý trong $O(N \log N)$.
  Ưu điểm: cấu trúc dữ liệu đơn giản, độ phức tạp thời gian rất tốt.
- [Sqrt Tree](../data_structures/sqrt-tree.md) - trả lời truy vấn trong $O(1)$, tiền xử lý trong $O(N \log \log N)$. Ưu điểm: nhanh. Nhược điểm: cài đặt phức tạp.
- [Disjoint Set Union / thủ thuật Arpa](../data_structures/disjoint_set_union.md#arpa) - trả lời truy vấn trong $O(1)$, tiền xử lý trong $O(n)$. Ưu điểm: ngắn gọn, nhanh. Nhược điểm: chỉ hoạt động nếu biết trước tất cả truy vấn, tức là chỉ hỗ trợ xử lý offline.
- [Cây Cartesian](../graph/rmq_linear.md) và [thuật toán Farach-Colton và Bender](../graph/lca_farachcoltonbender.md) - trả lời truy vấn trong $O(1)$, tiền xử lý trong $O(n)$. Ưu điểm: độ phức tạp tối ưu. Nhược điểm: lượng code lớn.

Lưu ý: Tiền xử lý là bước xử lý ban đầu mảng đã cho bằng cách xây dựng cấu trúc dữ liệu tương ứng.

## Bài tập luyện tập
- [SPOJ: Range Minimum Query](http://www.spoj.com/problems/RMQSQ/)
- [CODECHEF: Chef And Array](https://www.codechef.com/problems/FRMQ)
- [Codeforces:  Array Partition](https://codeforces.com/contest/1454/problem/F)
