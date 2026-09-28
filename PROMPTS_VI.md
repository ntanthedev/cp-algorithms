# Bộ prompt dùng trên ChatGPT web

Thứ tự hiện tại: **A → C cho PR #33 → A để phục hồi phần còn lại → B → C**. D chạy khi phát hiện lỗi nguồn đã xác minh. E chỉ dùng lúc người duy trì thật sự muốn merge. Mỗi khối dưới đây là một prompt hoàn chỉnh; thay những ô `<...>` trước khi gửi. Có thể đính kèm các file hướng dẫn nếu chúng chưa có trên branch GitHub.

## A — Khôi phục và đồng bộ bản dịch cũ

```text
Bạn đang bảo trì bản dịch tiếng Việt của ntanthedev/cp-algorithms cho học sinh THPT biết C++ cơ bản.
Fork: https://github.com/ntanthedev/cp-algorithms, default branch master.
Upstream: https://github.com/cp-algorithms/cp-algorithms, default branch main.
Đọc WORKFLOW_VI.md, TRANSLATING_VI.md, CONTRIBUTING.md và quy tắc agent nếu có. Nếu thiếu file/quyền đọc thì nói rõ.

Mục tiêu phiên này: tiếp tục công việc đang dở, xác định và sửa bản dịch bị lệch nguồn; chưa dịch bài mới.
Phạm vi khởi động lại: PR #33 nếu còn mở. Nếu đã xử lý xong thì chọn phần ưu tiên cao tiếp theo từ báo cáo audit hiện tại.

1. Kiểm tra quyền công cụ, Git status, worktree, default branch, remote và các PR đang mở. Fetch origin/upstream; ghi SHA thật. Không ghi đè thay đổi cục bộ, không reset agent/vi-work khi còn PR, không force-push master.
2. Chạy scripts/audit_vi_upstream.py cho origin/master và branch PR. Nếu script chưa có, tự đối chiếu translation.source_commit (blob SHA) với blob nguồn trong fork và upstream. Đọc báo cáo docs/translation/RESTART_2026-09-28.md như checkpoint lịch sử, phải xác minh lại các trạng thái có thể đổi.
3. Xếp hàng sửa: lỗi nội dung bản dịch/ghi chú sai; thay đổi code/công thức/biên; bổ sung mục; sửa nghĩa; typo/link. Đọc các PR upstream được chấp nhận, không gửi lại lỗi đã sửa. Chẩn đoán cũ bị đóng chưa merge phải kiểm lại, không mặc định maintainer đồng ý.
4. Nếu PR #33 còn mở: giữ 3 bài ternary_search, roots_newton, simpson-integration. So sánh từng blob cũ với upstream mới. Đồng bộ nguồn Newton/Simpson đã được upstream sửa, cập nhật bản VI và ghi chú, giữ ternary theo kết quả diff thực tế. Chú ý sửa upstream có thể giữ nguyên tên lỗi nhưng nội dung khác patch cũ. Không mở PR mới cho cùng việc.
5. Với đợt sync rộng sau #33: dùng nhánh làm việc, xem trước merge upstream, giải quyết xung đột giữ i18n/Pages của fork, chia phần review có thể hoàn tất. Không công bố đã đồng bộ cả repo khi mới nhập một vài file. Không sửa hash metadata cho file chưa được đồng bộ nội dung.
6. Code/công thức/HTML/link phải theo nguồn được chốt, giữ glossary. Mọi thay đổi nội dung làm mất hiệu lực review cũ phải ghi lại. Giữ draft, không tự ready hay merge.
7. Chạy validator, staleness, Markdown safety, strict build, rendered image check và test thuật toán phù hợp với nguồn đã đổi. Đọc lại review threads/submissions/conversation sau head cuối; phân biệt check đã chạy, chưa chạy và lỗi môi trường.
8. Được phép cập nhật branch và PR hiện có đúng phạm vi. Nếu không có quyền ghi, xuất patch/file đầy đủ, manifest và PR body để bàn giao; không giả vờ đã push/tạo PR. Không mở thêm bài mới khi phạm vi recovery chưa xong.

Đầu ra: SHA đầu/cuối, file đã đồng bộ, blob cũ/mới, thay đổi cần human review, test với kết quả thật, URL PR nếu có, danh sách còn lại và một prompt bàn giao ngắn cho phiên review mới. Không tự merge.
```

## B — Chọn và dịch một gói

```text
Hãy dịch một gói bài cho ntanthedev/cp-algorithms (base master), nguồn cp-algorithms/cp-algorithms (main).
Đọc WORKFLOW_VI.md và TRANSLATING_VI.md từ repo hoặc file tôi đính kèm, cùng CONTRIBUTING.md/quy tắc agent. Bản dịch là tài liệu học miễn phí cho học sinh THPT biết C++ cơ bản.

Phạm vi: <danh sách đường dẫn, hoặc “tự chọn gói tiếp theo theo dependency và độ cần thiết”>.
Nhánh dịch: agent/vi-work. Tối đa một PR dịch/maintenance đang mở.

Trước khi dịch:
- Xác minh quyền đọc/ghi; fetch fork/upstream, ghi SHA và kiểm tra PR mở. Nếu còn PR khác chưa xong thì tiếp tục nó, không tạo batch/branch chồng lên.
- Đối chiếu blob nguồn đã dịch với upstream. Nếu còn nợ đồng bộ, dừng lựa chọn bài mới và thực hiện phần recovery phù hợp trước.
- Khi được chọn bài mới, loại bài đã dịch hoặc đang có PR; chốt 1–3 bài dài, tối đa 5 bài vừa hoặc 5–10 bài ngắn cùng chủ đề. Một bài rất dài có thể chiếm cả gói. Báo phạm vi rồi thực hiện, không cần hỏi lại các lựa chọn thông thường.
- Đọc toàn văn nguồn từ Git tại SHA đã chốt; không dịch từ kết quả search hay trí nhớ. Nguồn fork phải tương ứng upstream được dùng; nếu chưa khớp thì xử lý sync trước.

Thực hiện:
1. Kiểm kê front matter, headings, code/inline code, LaTeX, link/image/raw HTML, tab, admonition và macro. Chốt glossary; thuật ngữ chưa chắc đối chiếu VNOI Wiki, ghi nguồn thật.
2. Tạo *.vi.md cạnh nguồn. Dịch đủ văn xuôi với tiếng Việt tự nhiên; bảo toàn code kể cả comment, ký hiệu/công thức, URL, file= snippet IDs và cấu trúc. Giữ attribution và giấy phép. Không tự đơn giản hóa thuật toán.
3. Metadata translation: source tương đối từ src/, source_commit là Git blob SHA đủ 40 ký tự của nguồn, status draft, last_synced ngày đồng bộ. Không dùng repository commit SHA thay cho blob.
4. Không âm thầm sửa nguồn trong PR dịch. Nếu nghi lỗi, ghi mệnh đề, giả thiết, chứng minh/case và trạng thái “nghi ngờ” cho đến khi xác minh. Ghi chú bản dịch có lý do rõ ràng, đặt ngoài list ở cột 1. Không tạo note kết luận nguồn sai từ trực giác.
5. Kiểm tra toàn bộ diff của gói, không chỉ commit cuối. Chạy các gate trong WORKFLOW_VI.md; xem trang render, MathJax, ảnh thật, anchors, chuyển ngôn ngữ, mobile. Giữ nguyên validator, không nới để lấy CI xanh.
6. Được phép commit/push branch làm việc và tạo hoặc cập nhật đúng một Draft PR vào fork/master khi gói hoàn chỉnh. Không mở PR chỉ để báo đang bắt đầu. Không tự ready/merge. Nếu công cụ chỉ đọc, xuất file/patch và PR body, ghi giới hạn rõ ràng.
7. Lỗi nguồn đã có bằng chứng có thể đi sang prompt D/phiên riêng. Chỉ gửi PR upstream sau duplicate-check và kiểm chứng đầy đủ; giữ thay đổi upstream tách khỏi nhánh i18n.

PR body và bàn giao phải gọn, gồm danh sách bài + blob, thuật ngữ mới, source findings, kiểm tra thực tế với head SHA cuối, phần chưa kiểm, link PR liên quan. Đọc lại cả review threads, submissions và conversation sau CI cuối. Đưa một prompt để phiên chat mới review độc lập. Không tự nhận bản dịch đã được review độc lập.
```

## C — Review trong một phiên chat mới

```text
Hãy review độc lập PR <URL PR> của ntanthedev/cp-algorithms. Đây là lượt kiểm tra kỹ thuật và tiếng Việt, không tự merge.
Đọc WORKFLOW_VI.md, TRANSLATING_VI.md, CONTRIBUTING.md và toàn bộ file trong diff. Lấy dữ liệu trực tiếp từ Git/GitHub; không tin PR body như bằng chứng kiểm tra.

1. Ghi repo, base/head SHA hiện tại, source blobs và upstream SHA. Đọc PR conversation, review submissions và inline threads. Nếu PR body trỏ SHA cũ, đánh dấu chứng cứ đó là lịch sử.
2. Xác minh các bản VI được review đúng nguồn đã chốt và so với upstream mới. Đọc toàn văn EN/VI, đặc biệt đoạn xung quanh mọi thay đổi, không chỉ diff hẹp. Nếu nhiều commit, bao phủ toàn bộ diff base–head.
3. Review kỹ thuật: định nghĩa, giả thiết, bất biến, lượng từ/phủ định, chỉ số, chiều chia hết, công thức, sai số, độ phức tạp, code/inline code, điều kiện biên và ví dụ. Phân biệt lỗi có sẵn ở nguồn với lỗi do dịch. Mọi translator note phải được kiểm chứng lại.
4. Review ngôn ngữ: đủ nội dung; tiếng Việt tự nhiên; glossary nhất quán; thuật ngữ phù hợp người học; không tự thêm khẳng định. Rà caption, alt text, tab, chú thích và links.
5. Chạy lại gate trên đúng head. Với code/nguồn thay đổi, dùng test phù hợp và case tái hiện. Kiểm trang render có công thức, ảnh, anchors, code tabs, language switch; kiểm mobile khi layout có liên quan. CI cấu trúc xanh không chứng minh nghĩa đúng.
6. Báo phát hiện theo ảnh hưởng với file/đoạn, trích ngắn lỗi, giải thích và cách sửa. Phân biệt blocker thật, khuyến nghị và phần chưa kiểm. Không tạo nhận xét hình thức chỉ để đủ số lượng.
7. Đây là phiên review: không sửa file, không push, không tự đánh dấu ready, không đăng comment lên GitHub trừ khi tôi yêu cầu riêng. Nếu không thể đọc nguồn/PR hoặc chạy gate, ghi giới hạn và kết luận tương ứng.

Kết luận: PASS hoặc CHANGES REQUIRED hoặc BLOCKED, luôn gắn head SHA và phạm vi. PASS chỉ là kết quả lượt review này, không thay cho human approval. Liệt kê lệnh/kết quả, kỹ thuật và ngôn ngữ, phần chưa kiểm, và prompt sửa lỗi cho tác giả. Nếu head thay đổi trong lúc review, chỉ rõ SHA nào đã được kiểm và phần nào cần kiểm lại.
```

## D — Kiểm chứng lỗi nguồn và tạo PR upstream

```text
Hãy kiểm chứng rồi, nếu có lỗi thật, tạo PR đóng góp cho https://github.com/cp-algorithms/cp-algorithms, base main.
Phát hiện cần kiểm: <mệnh đề/case/đường dẫn cụ thể và link liên quan>.
Được phép push nhánh sửa lỗi vào fork ntanthedev/cp-algorithms và gửi PR upstream sau khi đủ bằng chứng. Không tự merge. Không gửi issue/PR “có thể sai” để nhờ maintainer kiểm chứng thay.

1. Fetch upstream/main mới nhất, ghi SHA, đọc CONTRIBUTING.md và quy tắc repo. Tìm cả PR/issue mở và đã đóng liên quan, kể cả những PR cũ của tôi. Nếu lỗi đã sửa, không mở lại. Nếu từng bị đóng, đọc trao đổi và kiểm lại lý do kỹ thuật; không đoán lý do đóng.
2. Cố gắng bác bỏ chẩn đoán: viết rõ giả thiết và miền đầu vào; kiểm các phát biểu tương đương về toán học. Với code, có input làm bản cũ sai và oracle độc lập; với công thức/lập luận, có chứng minh hoặc phản ví dụ tối thiểu. Không coi cách viết khác/không tối ưu là lỗi correctness.
3. Ví dụ cần tránh: viết đúng chiều “k là ước của l*phi(n)”. Với k,phi(n)>0, điều kiện l*phi(n) chia hết cho lcm(k,phi(n)) không mạnh hơn điều kiện chia hết cho k, vì tử số vốn là bội của phi(n). PR #1673 có chẩn đoán cũ sai ở điểm này; vấn đề printf phải được triage riêng.
4. Nếu không chứng minh được lỗi: kết luận không đủ bằng chứng hoặc false positive, không gửi PR. Nếu là typo/clarity, gọi đúng loại, sửa tối thiểu.
5. Tạo nhánh upstream/fix-<topic> từ đúng upstream/main, không từ master/agent/vi-work. Chỉ sửa nguồn tiếng Anh và test cần thiết. Kiểm diff ba chấm để bảo đảm không mang theo file VI, glossary, workflow hay cấu hình fork. Gom lỗi liên quan, không trộn lỗi độc lập.
6. Kiểm bản cũ thất bại/bản mới đạt khi áp dụng được, chạy test/build phù hợp, giữ log gọn. Fetch lại trước khi gửi và duplicate-check lần cuối.
7. Tạo PR bằng tiếng Anh: vấn đề và ảnh hưởng, ví dụ/chứng minh, thay đổi tối thiểu, validation thật và giới hạn. Không nhắc dự án dịch nếu không cần giải thích bản sửa. Không tuyên bố test đã chạy khi chỉ suy luận.
8. Đọc lại PR đã tạo: URL, base repo/main, head SHA, danh sách file, diff và CI. Nếu có quyền ghi hạn chế hoặc UI cần nút Create PR, xuất patch và body để tôi thao tác; không báo đã tạo PR khi chưa có URL.

Đầu ra: VALID / FALSE POSITIVE / INSUFFICIENT EVIDENCE, lý do, bằng chứng, test, URL PR nếu có và bản dịch nào cần cập nhật sau khi upstream chấp nhận. Việc gửi PR không có nghĩa là upstream đã chấp nhận.
```

## E — Merge sau khi người duy trì đã duyệt

```text
Tôi đã đọc và duyệt PR <URL>, head <SHA tôi đã duyệt>. Hãy kiểm tra gate cuối và merge đúng PR này vào ntanthedev/cp-algorithms:master bằng merge commit nếu mọi điều kiện đạt.

Đọc WORKFLOW_VI.md và TRANSLATING_VI.md. Kiểm head thực tế đúng SHA được duyệt; nếu đổi thì không coi approval cũ bao phủ code mới. Đọc lại toàn bộ review threads/submissions/conversation, kiểm không còn blocker, merge conflict hoặc CI bắt buộc đang pending/fail. Xác minh review kỹ thuật và ngôn ngữ có phạm vi/SHA rõ ràng. Không dựa vào dấu xanh lịch sử trong PR body.

Nếu đạt thì merge, xác minh master đã chứa commit và báo URL/SHA. Theo dõi workflow deploy mới để phân biệt đã merge với đã deploy thành công. Không xóa agent/vi-work vì đây là nhánh dùng lại; sau khi xác minh không còn commit riêng cần giữ, chỉ fast-forward nó theo master nếu được. Không reset/force-push master. Nếu gate chưa đạt, báo blocker cụ thể và để PR mở, không tự vượt gate.
```

## Bàn giao tối thiểu giữa hai phiên

```text
Repo/base: ...
PR/branch: ...
Head đã kiểm: ...
Upstream commit đã dùng: ...
EN → VI và source blob từng bài: ...
Phạm vi đã hoàn tất / còn lại: ...
Test/build/render: lệnh, kết quả, head; phần chưa chạy: ...
Source findings: confirmed / suspected / rejected; URL PR nếu có: ...
Review kỹ thuật/ngôn ngữ/human approval: có hay chưa, tại SHA nào: ...
Việc duy nhất cần làm tiếp: ...
```
