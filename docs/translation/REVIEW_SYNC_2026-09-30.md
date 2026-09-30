# Prompt review đợt đồng bộ

Sao chép nguyên khối dưới đây vào phiên reviewer. Không cần điền thêm trường nào.

```text
Hãy review độc lập PR https://github.com/ntanthedev/cp-algorithms/pull/33.
Đây là PR đồng bộ upstream và bản dịch Việt trên agent/vi-work vào master, giữ Draft; không merge, không push, không đăng review/comment GitHub.

Đọc WORKFLOW_VI.md, TRANSLATING_VI.md và docs/translation/SYNC_2026-09-30.md từ branch PR. Fetch PR và lấy head/base SHA thật tại thời điểm review. Base khảo sát là 3cff374c22250aea8b9182904f08543a7f146141; upstream đã nhập là f06f7d5e5630f0b811e37d9e657562ba38c41f6a. Nếu các ref đã thay đổi, ghi rõ snapshot mới và không coi kết quả cũ là review của head mới.

Code head trước báo cáo là 4e483bdd; commit dịch 4740a611 cập nhật 49 bản dịch bị lệch nguồn (47 bài đã có trên master và Newton/Simpson trong PR cũ). Có tổng cộng 89 bản dịch, tất cả draft. PR cũng giữ Ternary Search, workflow/prompt/tooling đã chuẩn bị và các merge upstream; phải xét toàn bộ diff base–head, không chỉ commit cuối. Lấy source blob đủ 40 ký tự trực tiếp từ metadata và Git, không yêu cầu tôi nhập chúng.

Tự xác minh: upstream ancestry; không mất file VI/i18n/Pages; blob metadata và ngày đồng bộ; code, công thức, heading, links, HTML/SVG, tabs/admonitions khớp nguồn; đủ nghĩa và tiếng Việt tự nhiên; các note lỗi nguồn cũ đã được xóa/cập nhật đúng. Các file chỉ đổi metadata phải thực sự chỉ có delta nguồn không làm đổi nghĩa của bản dịch.

Ưu tiên kỹ thuật: Segment Tree với đoạn nửa mở; LCA động và phương pháp bộ nhớ tuyến tính; Parallel Binary Search; Primality Tests bảy cơ số; LIS và khôi phục dãy; Knapsack; 0–1 BFS hai vector; Newton 0/overflow; Simpson single-panel/composite error. Rà cả các file nhỏ còn lại, đừng kết luận toàn PR PASS chỉ từ vài bài lớn.

Kiểm tra test/extract_snippets.py chỉ lấy nguồn English và regression test tương ứng. Chạy validators cho toàn bộ PR, strict build và kiểm render. Tác giả đã chạy local suite C++ 66 PASS/1 FAIL do assertion thời gian Manhattan MST trên máy; đọc CI thật ở head hiện tại để phân biệt timing, hạ tầng và correctness. Các focused tests được nêu trong báo cáo là chứng cứ tác giả, bạn cần tự kiểm chứng phần thuộc phạm vi review của mình. Không tin PR body như bằng chứng đã chạy test.

Trả REVIEW_RESULT với repo/PR/base/head/upstream SHA thực tế, phạm vi full/delta, danh sách file đã kiểm, technical/language coverage, findings có ID+mức ảnh hưởng+file/đoạn+bằng chứng+cách sửa, test/kết quả và phần chưa kiểm. Verdict PASS/CHANGES_REQUIRED/BLOCKED chỉ áp dụng đúng snapshot và phạm vi. Nếu chưa đủ thời gian review toàn bộ gói, ghi PARTIAL coverage và bàn giao phần còn lại, không báo toàn PR PASS. Báo cáo này sẽ được dán nguyên về phiên tác giả để tự xử lý; không bắt người dùng điền lại URL/SHA.
```
