# Xử lý sau review bản dịch

Tài liệu này ghi bước tiếp theo sau đợt review toàn văn các bản dịch: xác minh
phát hiện, cân nhắc sửa và so sánh thuật ngữ với VNOI Wiki. Các quy tắc về phạm
vi, tác giả, reviewer, gate và quyền merge vẫn theo [WORKFLOW_VI.md](../../WORKFLOW_VI.md)
và các hướng dẫn vai trò. Có thể phân nhiều người khi được yêu cầu; mỗi tác giả
vẫn làm việc trong checkout riêng, reviewer độc lập và PR được gom hợp lý.

## Phạm vi và tiến độ

Thứ tự trong đợt này là thứ tự của báo cáo 40 bài đầu, không phải thứ tự chữ cái.
Lô đầu là 30 bài bên dưới; sau đó xử lý 31–40 và các bài còn lại theo danh mục
đã review. Snapshot của báo cáo cũ là fork `1bc738ed8de2b42d8a5905d56e1ee204728bebbf`;
trước khi xử lý mỗi lô phải xác minh lại fork, upstream, nguồn và trạng thái công việc.

Danh sách này xác định phạm vi, **không biểu thị các bài đã xử lý xong**. Duy trì
báo cáo lô riêng với bằng chứng và trạng thái từng bài; không đánh dấu hoàn tất
theo số bài đã phân công. Các báo cáo cũ trong `output/` có thể là tệp cục bộ bị
Git bỏ qua: không giả định chúng có sẵn ở checkout khác; khi bàn giao phải lưu hoặc
đính kèm bằng chứng cần thiết ở nơi người nhận truy cập được.

1. `src/algebra/binary-exp.vi.md`
2. `src/algebra/euclid-algorithm.vi.md`
3. `src/graph/dijkstra.vi.md`
4. `src/graph/dijkstra_sparse.vi.md`
5. `src/geometry/delaunay.vi.md`
6. `src/data_structures/segment_tree.vi.md`
7. `src/algebra/continued-fractions.vi.md`
8. `src/algebra/polynomial.vi.md`
9. `src/geometry/vertical_decomposition.vi.md`
10. `src/graph/hungarian-algorithm.vi.md`
11. `src/graph/strongly-connected-components.vi.md`
12. `src/graph/2SAT.vi.md`
13. `src/graph/all-pair-shortest-path-floyd-warshall.vi.md`
14. `src/graph/bellman_ford.vi.md`
15. `src/graph/breadth-first-search.vi.md`
16. `src/graph/bridge-searching-online.vi.md`
17. `src/graph/bridge-searching.vi.md`
18. `src/graph/centroid_decomposition.vi.md`
19. `src/graph/depth-first-search.vi.md`
20. `src/graph/dinic.vi.md`
21. `src/graph/edmonds_karp.vi.md`
22. `src/graph/euler_path.vi.md`
23. `src/graph/hld.vi.md`
24. `src/graph/kuhn_maximum_bipartite_matching.vi.md`
25. `src/graph/lca.vi.md`
26. `src/graph/lca_binary_lifting.vi.md`
27. `src/graph/lca_farachcoltonbender.vi.md`
28. `src/graph/min_cost_flow.vi.md`
29. `src/graph/mpm.vi.md`
30. `src/graph/mst_kruskal.vi.md`

## Cách xử lý từng bài

1. Đọc báo cáo trước đó, kể cả phần đính chính và kiểm chứng độc lập; so với
   toàn cảnh nguồn EN/VI tại snapshot hiện hành. Ghi từng phát hiện là xác nhận,
   bác bỏ có lý do, hoặc chưa đủ bằng chứng. Một báo cáo không phát hiện lỗi
   không thay thế bước so sánh thuật ngữ bên dưới.
2. Tìm bài tương ứng hoặc bài có khái niệm liên quan trên VNOI Wiki. Với **mỗi
   bài**, ghi URL trang đã đọc, thuật ngữ VNOI, thuật ngữ hiện dùng và quyết định
   giữ/sửa kèm lý do. Nếu không tìm thấy trang tương ứng hoặc không truy cập được,
   ghi rõ phạm vi tìm và giới hạn; không bịa nguồn hay đánh dấu đã so sánh.
3. Chọn thuật ngữ dựa trên nghĩa kỹ thuật của nguồn, glossary của repo, ngữ cảnh
   và khả năng hiểu của độc giả. VNOI là nguồn tham khảo hữu ích, không phải chuẩn
   duy nhất; thuật ngữ giống nhau có thể mang nghĩa khác theo ngữ cảnh. Giữ cách
   hiện tại khi phù hợp và có thể giới thiệu tên gọi thay thế ở lần xuất hiện đầu.
4. Tác giả xác minh rồi sửa các lỗi dịch hoặc diễn đạt chưa rõ trong phạm vi được
   giao; không thay đổi code, công thức hay nguồn EN để che sai sót. Nếu nguồn có
   vấn đề, phân biệt ghi chú bản dịch có căn cứ với sửa nguồn ở luồng riêng.
5. Bàn giao từng bài: đường dẫn EN/VI, blob hoặc SHA được xét, báo cáo ban đầu,
   quyết định cho từng finding, đối chiếu VNOI, file/dòng thay đổi và phần còn mở.
   Nếu không sửa, nêu căn cứ giữ nguyên. Reviewer khác kiểm độc lập các thay đổi,
   đối chiếu nguồn và thuật ngữ; kết quả nêu phạm vi, SHA và giới hạn.

## Nghi vấn lỗi trong bài nguồn

- Kiểm lại trên `upstream/main` mới nhất, nêu mệnh đề sai và chứng minh hoặc ví dụ
  tái hiện; với code, kiểm trước/sau. Phân biệt lỗi dịch, lỗi trình bày và lỗi
  thuật toán, đồng thời thử bác bỏ chẩn đoán. Không tự coi báo cáo cũ là kết luận.
- Tìm issue **và** PR cả đang mở lẫn đã đóng bằng nhiều từ khóa phù hợp; đọc các
  mục có thể trùng, nội dung thảo luận và lý do đóng nếu có. Ghi truy vấn, ngày,
  kết quả, liên kết và phần chưa rõ. Nếu đã được báo hoặc đã có bản sửa thì dẫn
  lại, không mở trùng; không suy đoán lý do đóng.
- Khi có quyền và yêu cầu hiện hành cho phép, làm PR tiếng Anh riêng từ upstream
  mới nhất theo mục 6 của workflow. Gộp lỗi nhỏ có liên quan; lỗi độc lập cần được
  tách để dễ review. Không đưa bản dịch vào PR upstream và không tự merge upstream.
  Thiếu chứng cứ hoặc kết quả tìm trùng chưa đủ thì để mở để kiểm tiếp.

## Kiểm tra và bàn giao lô

Chạy các gate áp dụng ở mục 7 của workflow trên head cuối, gồm kiểm đối chiếu
LaTeX trong phạm vi thay đổi, strict build, staleness và Markdown; ghi đúng lỗi
đã có từ trước và lỗi mới, không nới validator. Kiểm trang render của các bài đã
thay đổi theo hướng dẫn vai trò; báo rõ kiểm bằng mắt và kiểm tự động bao phủ
những gì. CI xanh, DOM sạch hoặc một reviewer duyệt một phần không chứng nhận
toàn bộ nội dung hoặc toàn bộ trang đã được xem trực quan.

Tổng hợp một PR draft gọn trên fork khi thích hợp; nêu head, base, số bài được
đối chiếu, bài thay đổi/giữ nguyên, review độc lập, kết quả gate và việc còn mở.
PR/review upstream và vấn đề trùng được liên kết trong bàn giao; nội dung gửi
upstream viết bằng tiếng Anh. Gate merge vẫn yêu cầu duyệt PR/head cụ thể.
