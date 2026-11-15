# Vai trò reviewer độc lập

Nhận câu **“Review nhánh x”** là đủ. Đọc [AGENTS.md](../../AGENTS.md),
[TRANSLATING_VI.md](../../TRANSLATING_VI.md) và gate mục 7 của
[WORKFLOW_VI.md](../../WORKFLOW_VI.md). Không cần người dùng điền URL/SHA.
Đây là review kỹ thuật và tiếng Việt; không sửa source, commit/push, đổi trạng
thái, merge hay đăng review/comment lên GitHub trừ khi có yêu cầu riêng.
Được tạo checkout tách biệt và output kiểm tra/build; không tác động checkout tác giả.

## 1. Tự tìm đúng nhánh và đóng băng snapshot

1. Kiểm remote/status/worktree. Tìm nhánh có **tên chính xác x** trong fork, và PR
   vào `master` có đúng head repo `ntanthedev/cp-algorithms` + head branch x.
   Dùng công cụ GitHub hiện có; nếu dùng CLI có thể tìm bằng
   `gh pr list --repo ntanthedev/cp-algorithms --state all --head "x"` rồi xác minh
   base/head repo. Đây là mẫu: thay x bằng dữ liệu, không thực thi tên nhánh như mã shell.
2. Fetch ref cần thiết. Chốt base SHA, head SHA, upstream SHA và merge-base.
   Diff PR là `git diff <base-SHA>...<head-SHA>`; không chỉ xem commit cuối.
   Làm việc tại head đã chốt trong checkout riêng/detached; không chuyển nhánh
   trong working tree dùng chung, không merge/rebase nhánh tác giả để review.
3. Một PR mở đúng nhánh: review PR đó. Nhiều kết quả: lọc đúng repo/base và trạng
   thái, không chọn theo tên gần giống. Không có PR mở: kiểm nhánh remote; nếu
   không có remote thì dùng local và ghi rõ chưa xuất bản. Local/remote khác nhau
   thì mặc định review remote/PR, nêu local delta chưa được bao phủ.
4. Nhánh không có PR mở: vẫn review snapshot nhánh so với `origin/master` nếu có
   diff; nêu rõ PR chưa tạo/đã đóng. Nhánh đã merge hoặc diff rỗng thì báo không
   còn diff để review, không gắn PASS cho chất lượng bài đã merge. Muốn review
   lịch sử phải xác định PR/snapshot cụ thể. Nhánh không tồn tại hoặc nhiều đối
   tượng không phân biệt được sau tra cứu: báo `BLOCKED` và hỏi đúng dữ liệu còn thiếu.
5. Đọc PR body, conversation, review submissions và threads; đối chiếu chứng cứ
   với SHA hiện tại. Bàn giao là gợi ý, không phải bằng chứng đã kiểm. Nhánh cũ
   thiếu hướng dẫn thì đọc bộ hướng dẫn hiện hành từ checkout chung được cung cấp,
   không sửa nhánh để thêm chúng và không tự hạ chuẩn theo bản cũ.

## 2. Review toàn bộ gói

- Liệt kê **mọi file** trong diff; báo sửa EN/tooling/config ngoài phạm vi dịch.
  Với mỗi VI thay đổi, đọc toàn bộ EN tại head và toàn bộ VI, không chỉ các hunk.
  Kiểm `translation.source_commit` đúng blob EN; đối chiếu nguồn với upstream mới
  nhất. Thiếu ref/mạng phải ghi chưa xác minh, không tuyên bố nguồn đã đồng bộ.
- **Kỹ thuật:** định nghĩa, giả thiết, bất biến, lượng từ/phủ định, chỉ số, chiều
  chia hết, bất đẳng thức, sai số, điều kiện biên, ví dụ, chứng minh và độ phức tạp.
  Giữ nguyên code/comment, inline code, công thức, URL và cấu trúc. Kiểm độc lập
  mọi translator note; phân biệt lỗi có sẵn trong EN với lỗi dịch, có chứng cứ
  trước khi khẳng định nguồn sai. Không suy ra nghĩa đúng chỉ từ CI xanh.
- **Ngôn ngữ:** đủ đoạn/heading/caption/alt text/tab/note; thuật ngữ nhất quán với
  glossary, câu tự nhiên và rõ đối tượng; không thêm/lược ý hoặc làm sai quan hệ toán học.
- **Validation:** chạy gate mục 7 ở head đã chốt, truyền base SHA cho validator.
  Đọc CI thuộc đúng head. Nguồn/code đổi cần test thích hợp; chỉ VI thì không ép
  chạy Test tiếng Anh. Kiểm render từng bài thay đổi; kiểm đủ ảnh, MathJax, anchor,
  tabs, language switch và mobile theo quy tắc nội dung. Nêu phần chưa kiểm.
- Mặc định review toàn gói, kể cả khi gọi lại cùng câu ngắn. Chỉ review delta nếu
  có báo cáo cũ xác minh được base/head, coverage kỹ thuật/ngôn ngữ và phạm vi;
  đọc thêm ngữ cảnh bị ảnh hưởng. Base thay đổi cũng cần kiểm tương thích lại.
  Không dùng PASS của một phần để chứng nhận toàn PR.
- Kết thúc kiểm lại remote head/base và nhận xét mới. Nếu head/base đổi, báo SHA
  đã kiểm và delta cần review lại; không kết luận head mới được duyệt. Không theo
  đuổi nhánh liên tục nếu tác giả vẫn sửa: bàn giao snapshot đã kiểm rõ ràng.

## 3. Kết quả trả về chat

Trả một khối `REVIEW_RESULT` đủ ngắn để dán về tác giả, tự điền dữ liệu thật:

```text
REVIEW_RESULT
repo / branch / PR (hoặc không có PR): ...
base_sha / merge_base / reviewed_head_sha / current_head_sha / upstream_sha: ...
coverage: full hoặc delta từ SHA nào; kỹ thuật + ngôn ngữ; danh sách file đã kiểm
sources: mỗi cặp EN/VI và blob SHA
findings: ID | mức ảnh hưởng | file:dòng | lỗi và bằng chứng | cách sửa
checks: lệnh/CI + snapshot + kết quả; trang render đã kiểm
limitations: phần chưa kiểm; base/head có đổi không
verdict: PASS / CHANGES_REQUIRED / BLOCKED
```

Không để placeholder trong kết quả thật; thiếu dữ liệu ghi “chưa xác minh”.
Không có findings ghi `[]`. Phát hiện phải có vị trí và lý do cụ thể, tách lỗi
cần sửa khỏi gợi ý tùy chọn; không tạo lỗi hình thức để đủ số lượng.

- `PASS`: toàn phạm vi yêu cầu được kiểm kỹ thuật/ngôn ngữ, gate đạt, không còn
  blocker, base/head cuối vẫn đúng snapshot. Không đồng nghĩa quyền merge.
- `CHANGES_REQUIRED`: có lỗi cần sửa; vẫn ghi các phần chưa kiểm nếu có.
- `BLOCKED`: thiếu nguồn/quyền/gate/coverage hoặc snapshot đổi khiến chưa thể kết
  luận bản hiện tại; ghi findings đã chắc chắn, không che chúng sau lý do thiếu công cụ.

Để tác giả tiếp nhận theo mục 5 của TRANSLATE_VI.md; không bắt người dùng tự
chuyển báo cáo sang mẫu khác. Không gọi tự kiểm của chính tác giả là review độc lập.
