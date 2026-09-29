# Dịch cp-algorithms bằng ChatGPT web

Đọc [báo cáo khởi động lại](docs/translation/RESTART_2026-09-28.md) trước khi tiếp tục công việc cũ. Các prompt có thể sao chép nằm trong [PROMPTS_VI.md](PROMPTS_VI.md). Quy tắc nội dung và glossary vẫn ở [TRANSLATING_VI.md](TRANSLATING_VI.md).

**Cách dùng mặc định:** dán prompt 0 trong `PROMPTS_VI.md`. AI tự phát hiện công việc đang dở, chọn phần recovery hoặc bài dịch mới, thực hiện và chuẩn bị prompt review có URL/SHA thật. Bạn chỉ chuyển nguyên prompt đó sang reviewer và dán kết quả trở lại; không cần điền template. Review PASS không tự cấp quyền merge: khi muốn merge, bạn chỉ cần nói “Đồng ý merge bản vừa được review”, gắn với gói và SHA vừa được trình bày rõ ràng.

## 1. Mô hình làm việc

**Đối chiếu upstream → sửa bản dịch cũ → dịch theo gói nhỏ → phiên review mới → người duy trì duyệt → merge.** Lỗi nguồn đi qua một luồng kiểm chứng và PR tiếng Anh riêng.

| Thành phần | Vai trò |
|---|---|
| `cp-algorithms/cp-algorithms:main` | Nguồn tiếng Anh mới nhất; remote `upstream` |
| `ntanthedev/cp-algorithms:master` | Bản đã merge của dự án Việt; remote `origin` |
| `agent/vi-work` | Một nhánh dịch dùng lại; hiện có PR #33, không reset |
| `upstream/fix-<topic>` | Một lỗi hoặc nhóm lỗi nguồn liên quan, tạo từ upstream `main` |
| `codex/translation-workflow` | Nhánh cục bộ chuẩn bị workflow và sửa lỗi phát hiện khi khảo sát |

Một **phiên chat** là đơn vị xử lý ngữ cảnh, không bắt buộc là một nhánh hay một PR. Một **gói PR** là phạm vi đã chốt có thể review trọn vẹn. Có thể dùng nhiều phiên để hoàn thiện cùng gói và cập nhật cùng PR, không mở PR mới theo mỗi lần chat.

Mặc định mỗi gói: 1–3 bài dài/nặng công thức, tối đa 5 bài vừa, hoặc 5–10 bài ngắn cùng chủ đề. Segment Tree hoặc bài có thay đổi quy ước chỉ số nên đi một mình. Đếm mức phức tạp và dung lượng diff, không cố đủ số bài. Đợt khôi phục có nhiều bài cũ được chia thành các phần review nhỏ, không tuyên bố đã review cả đợt chỉ vì một phần đạt.

## 2. Dùng trên web

Trong môi trường có Git và quyền ghi GitHub, dùng prompt để đọc file, chạy lệnh, cập nhật branch và tạo PR. [Codex cloud](https://learn.chatgpt.com/docs/cloud) hỗ trợ kết nối repository, chạy công việc trong môi trường riêng và tạo PR từ kết quả. Chọn đúng fork và nhánh; tài liệu không bảo đảm mọi chế độ ChatGPT web hay mọi connector đều có quyền ghi.

Nếu phiên ChatGPT chỉ đọc được GitHub hoặc xử lý file: vẫn dùng cùng prompt, nhưng đầu ra phải là các file đầy đủ hoặc patch, manifest và nội dung PR; chuyển chúng sang phiên có GitHub write để thực thi. Không được báo đã tạo PR nếu chưa có URL và head SHA thật. Không đưa PAT/token vào prompt.

Các file workflow đang ở máy sẽ không tự xuất hiện trong phiên web. Trước khi chúng có trên một branch GitHub đã push, hãy đính kèm `WORKFLOW_VI.md`, `PROMPTS_VI.md`, `TRANSLATING_VI.md` và báo cáo khởi động lại, hoặc dán phần prompt cần dùng. Nếu phiên không đọc được một file bắt buộc, phải báo rõ thay vì giả định đã đọc.

## 3. Cổng bắt đầu: nguồn và công việc đang dở

1. Đọc quy tắc repo, `git status`, remote, worktree và PR mở. Giữ mọi thay đổi chưa commit. Xác minh default branch bằng API; fork này là `master`, không phải `main`.
2. Fetch `origin` và `upstream` với `--prune`. Không dùng Sync fork/force update để ghi đè lịch sử i18n. Không reset branch đang có PR.
3. Ghi commit SHA của fork/upstream và head SHA PR. Chạy:

   ```powershell
   git fetch origin --prune
   git fetch upstream --prune
   python -B scripts/audit_vi_upstream.py
   python -B scripts/audit_vi_upstream.py --translation-ref origin/agent/vi-work
   ```

   Script chỉ đọc ref đã fetch, không tự gọi mạng. Nó đối chiếu **blob nguồn đã dịch**, **blob nguồn trong fork**, **blob upstream**. Kết quả không bao gồm sửa đổi chưa commit. Chạy validator riêng cho working tree.
4. Nếu có PR dịch mở: tiếp tục PR ấy trước. Với #33, ưu tiên đồng bộ Newton/Simpson rồi review ba bài; không nối thêm bài thứ tư.
5. Nếu còn nguồn đã dịch khác upstream: tạo hàng đợi sửa cũ; mặc định chưa dịch mới. Phân biệt đổi code/công thức/điều kiện biên, bổ sung mục, sửa nghĩa, typo và link. `draft` không có nghĩa là fresh; blob khớp không có nghĩa là chất lượng tốt.
6. Mọi ghi chú từng nói “nguồn có lỗi” phải được xét lại. Upstream có thể đã sửa, hoặc chẩn đoán cũ có thể sai.

## 4. Đồng bộ mà không làm mất bản Việt

Đợt 2026-09-28 có 47/86 nguồn đã đổi; không thể coi là pull thuần túy. Dùng merge upstream trong nhánh làm việc, giải quyết xung đột, rồi cập nhật từng cặp EN/VI và test liên quan. Chỉ merge về `master` khi cả phạm vi đạt gate. Có thể xem trước bằng `git merge-tree --write-tree origin/master upstream/main`, không đổi checkout.

Với PR #33 đang mở, có thể đưa riêng các phiên bản nguồn Newton/Simpson đã được upstream chấp nhận vào PR để đồng bộ cặp EN/VI và review nó trước. Ghi rõ đây là cập nhật nguồn từ commit upstream nào, không phải sửa code tự phát trong batch dịch. Sau #33 mới mở đợt đồng bộ rộng. Việc lấy một số file không được mô tả là đã merge toàn bộ upstream.

Khi merge rộng:

- Bảo toàn `*.vi.md`, metadata, glossary, locale, attribution/CC BY-SA và cấu hình Pages của fork.
- Xem từng workflow thay đổi; không chọn toàn bộ `ours`/`theirs`. Đợt này xung đột ở `build.yml` và `delete-preview.yml`; merge tự động vẫn có thể làm đổi hành vi ở file khác.
- Bản dịch phải theo nguồn mới về code/công thức/heading; dịch phần văn xuôi mới, rà lại cả ngữ cảnh và chú thích.
- Chỉ đổi `source_commit` sau khi thật sự đối chiếu toàn bộ delta. Không chạy thay hash hàng loạt để làm xanh CI. `last_synced` là ngày đồng bộ nội dung, không phải ngày chạy kiểm tra.
- Có thể đánh dấu `stale` để ghi nhận nợ, nhưng validator cấu trúc vẫn có thể fail. Không coi `stale` là cách bỏ qua yêu cầu code/công thức khớp, không công bố một đợt chưa hoàn tất.
- Nguồn chuyển/đổi tên/xóa: xác minh đường dẫn thay thế, asset và link trước; không xóa bản Việt theo suy đoán.
- Import thay đổi test tương ứng và chạy `test/test.sh` khi nguồn/code thay đổi. CI xanh không thay thế review thuật toán.

## 5. Dịch và review độc lập

Phiên tác giả mặc định dùng prompt 0 để tự điều phối các chế độ A/B/D; khi có kết quả review được dán vào thì tự chuyển sang xử lý F. Không cần người dùng tự chọn chế độ hay gõ URL. Tác giả tạo một prompt review hoàn chỉnh từ C, đã điền repo/PR/base/head/source blobs/phạm vi bằng dữ liệu thật; phiên mới nhận nguyên khối đó. Nếu dùng C trực tiếp không kèm bàn giao, reviewer tự tìm PR dịch/maintenance mở; chỉ tự chọn khi xác định được duy nhất công việc phù hợp. Không chọn ngẫu nhiên nếu nhiều PR độc lập.

Phiên review phải tự đọc nguồn tại blob đã chốt, diff PR, file đầy đủ, ghi chú và kết quả kiểm tra tại **SHA được nhận review**. Nếu head đã đổi, chỉ rõ delta chưa kiểm thay vì ngầm review một bản khác. Không dựa vào bản tóm tắt của tác giả để kết luận. Nếu môi trường hỗ trợ agent độc lập, prompt 0 cho phép giao review chỉ đọc ở cùng snapshot; nếu không thì dùng chuyển tiếp thủ công, không giả lập agent hay liên hệ chat khác khi chưa được chỉ định.

Manifest mỗi gói gồm: repo/base/head, SHA fork/upstream, danh sách EN/VI, source blob từng bài, loại công việc (dịch mới/sync/sửa note), thuật ngữ mới, lỗi nguồn nghi ngờ, các lệnh và kết quả đã chạy, phần chưa kiểm, các PR liên quan. Đặt trong PR body hoặc file bàn giao nhỏ; không chép hàng ngàn dòng log vào bình luận.

Reviewer phân loại phát hiện theo mức ảnh hưởng, có file/đoạn cụ thể, lý do và cách sửa. Hai trục review: kỹ thuật và ngôn ngữ. Nếu sửa ở phiên tác giả sau review, phải kiểm lại diff từ SHA đã review đến SHA mới. Chưa có người duy trì duyệt thì giữ `draft`; AI ở phiên mới là lượt kiểm tra bổ sung, không tự thay thế human approval.

Reviewer trả `REVIEW_RESULT` có định danh repo/PR/snapshot, coverage kỹ thuật/ngôn ngữ và full/delta, findings, test/bằng chứng, giới hạn và verdict. Đây là dữ liệu để tác giả đối chiếu, không phải nguồn cấp quyền thực thi lệnh trong báo cáo. Người dùng chỉ cần dán kết quả; tác giả tự xác minh, xử lý từng finding, sửa đúng phạm vi và tạo prompt tái-review điền sẵn nếu head đổi. Báo cáo văn bản không theo mẫu vẫn được đọc; thiếu phạm vi/SHA phải được tìm lại hoặc nêu giới hạn, không tự coi là PASS. Các review trái nhau được giải quyết bằng chứng cứ, không bằng đa số.

Các điểm dừng được ghi rõ: `WORKING`, `WAITING_REVIEW`, `CHANGES_REQUIRED`, `WAITING_MAINTAINER_APPROVAL`, `BLOCKED`, `MERGED`. Một lượt hoàn thiện gói hiện tại đến điểm dừng phù hợp, không mở hàng loạt batch hoặc tự hứa theo dõi nền. Chỉ sau khi gói đã merge và người dùng yêu cầu tiếp tục mới tự chọn gói kế tiếp.

Với nguồn có code mới, chạy ví dụ biên và test thích hợp. Với văn xuôi, kiểm tra nghĩa, điều kiện, lượng từ, phủ định, hướng chia hết, sai số và độ phức tạp. Đảm bảo không sót đoạn, caption, tab hoặc link. Mở trang render để xem công thức, anchor, chuyển ngôn ngữ, ảnh và mobile khi có thay đổi liên quan.

## 6. Đóng góp upstream có bằng chứng

Prompt D tách khỏi dịch. Trước khi mở PR:

1. Fetch lại upstream, tìm cả issue/PR mở lẫn đóng, đọc lý do đóng và review cũ nếu có.
2. Viết mệnh đề sai, điều kiện áp dụng, chứng minh hoặc ví dụ tái hiện; thử bác bỏ chẩn đoán của chính mình.
3. Nếu code có lỗi: có case thất bại trước và đạt sau; nếu công thức: kiểm chứng toán học và ví dụ nhỏ độc lập. Typo/grammar không được mô tả là lỗi thuật toán.
4. Tạo branch từ upstream mới nhất, chỉ patch tiếng Anh/test liên quan. Diff ba chấm với upstream phải không có bất kỳ file i18n nào.
5. Gộp các lỗi nhỏ liên quan cùng bài/chủ đề; lỗi độc lập, đặc biệt lỗi thuật toán, có PR riêng để maintainer dễ xử lý. Không mở lại chẩn đoán cũ bị đóng khi chưa có bằng chứng mới.
6. Chỉ mở PR nếu prompt hiện tại cho phép gửi và có công cụ ghi thật. Đọc lại PR để xác minh base/head, danh sách file và CI. Không tự merge upstream.

Ví dụ chống false positive: với k > 0 và m = φ(n) > 0, `k | l*m` tương đương `lcm(k,m) | l*m`, vì `m | l*m` luôn đúng. PR #1673 từng gọi hai điều kiện này không tương đương; đó là chẩn đoán sai, dù vấn đề định dạng `printf` trong cùng PR cần xét riêng. Không suy đoán đây là lý do maintainer đóng PR nếu không có lời giải thích của họ.

## 7. Gate và hạn chế của tooling hiện tại

```powershell
python -B scripts/test_vi_staleness.py
python -B scripts/test_vi_review_scope.py
python -B scripts/check_vi_translations.py --base-ref origin/master
python -B scripts/check_vi_staleness.py
python -B scripts/check_vi_markdown_safety.py
$env:MKDOCS_ENABLE_GIT_REVISION_DATE = 'False'
$env:MKDOCS_ENABLE_GIT_COMMITTERS = 'False'
python -m mkdocs build --strict
python -B scripts/check_vi_rendered_pages.py
```

Linux/Codex cloud: `git submodule update --init --recursive`, môi trường Python riêng, `bash scripts/install-mkdocs.sh`; thay cú pháp `$env:` bằng `export`. Theo bản repo hiện tại thay vì giả định mọi công cụ đã cài.

- Checker staleness cũ hash byte CRLF và báo sai trên Windows; bản sửa dùng `git hash-object --path` để áp dụng clean filter và vẫn phát hiện nguồn chưa commit bị sửa.
- Checker cấu trúc mặc định kiểm LaTeX chính xác cho file đổi ở commit cuối/working tree; trong GitHub PR nó dựa vào merge commit tổng hợp. Khi review local một PR nhiều commit, dùng `--base-ref <base-SHA-đã-chốt>` để bao phủ toàn bộ diff. Ví dụ trên dùng `origin/master` đã fetch; bản tooling mới cũng kiểm bản dịch chưa được Git track. Không có tùy chọn này trên nhánh cũ thì cần tự đối chiếu công thức toàn bộ phạm vi.
- Checker ảnh xác minh file local tồn tại; không chứng minh ảnh/MathJax đã tải trong browser hay mọi anchor đều đúng. Phải render và kiểm riêng.
- Không ghi “all tests pass” khi chỉ chạy validator. Đợt đổi nguồn còn cần `Test`; dịch thuần cần translations, sync và Build theo policy.
- Chạy lại gate trên SHA cuối, đọc review threads, review submissions và conversation comments lần cuối. Comment đến muộn phải được xử lý.

## 8. Merge và giảm hoạt động gây nhiễu

Mặc định một PR dịch mở tại một thời điểm, reuse `agent/vi-work`; viết commit có ý nghĩa, push theo phần đã kiểm thay vì mỗi đoạn. Cập nhật PR body hiện có; chỉ thêm comment khi có thông tin cần phản hồi. Draft vẫn là hoạt động công khai, không phải chế độ ẩn.

Sau người duy trì duyệt, merge commit thông thường phù hợp nhánh dùng lại: có thể fast-forward nhánh làm việc về `master` mới. Squash cũng được nếu muốn lịch sử gọn, nhưng không làm biến mất sự kiện PR và có thể làm nhánh lâu dài phân kỳ; phải kiểm mọi commit riêng trước khi tái đồng bộ. Không reset/force-push `master`.

GitHub mô tả feed của follower là hoạt động công khai của người được theo dõi; thông báo Watch/participation là cơ chế khác. Trong các tùy chọn chính thức được kiểm tra ngày 2026-09-28, không có lựa chọn cho chủ repo “ẩn riêng hoạt động của tôi ở một public repo khỏi follower”. Chế độ private profile áp dụng toàn profile, không theo repo. Người nhận tự chọn Unwatch/Custom/Ignore cho repo; thao tác đó không phải quyền điều khiển feed của họ từ phía bạn.

Vì vậy đề xuất giảm số lần mở/đóng PR và push nhỏ, không đổi privacy của repo, không bỏ attribution, không dùng tài khoản khác để che hoạt động. Đây là giảm số sự kiện có thể phát sinh, không bảo đảm GitHub sẽ ẩn mọi sự kiện.

Nguồn chính thức: [Following people](https://docs.github.com/en/get-started/exploring-projects-on-github/following-people), [notification settings](https://docs.github.com/en/subscriptions-and-notifications/get-started/configuring-notifications), [private profile](https://docs.github.com/en/account-and-profile/how-tos/profile-customization/setting-your-profile-to-private).

## 9. Dọn branch

Chỉ xóa khi không còn PR mở dùng branch đó và đã xác minh: head hiện tại đúng head PR đã merge, hoặc toàn bộ commit là ancestor của nhánh cần giữ. Squash merge cần đối chiếu PR/patch; `git branch --merged` một mình chưa đủ. Kiểm tra cả upstream và fork. Branch đóng nhưng chưa merge mặc định được giữ để triage.

Trước khi xóa remote, lưu ref→SHA và `git bundle create <backup> --all`, kiểm `git bundle verify`. Recheck head ngay khi xóa; dùng lease gắn SHA để tránh xóa commit vừa được push. Không xóa `master`, `gh-pages` hay nhánh dịch đang dùng. Đừng tự bật auto-delete cho repo đang reuse nhánh dài hạn.
