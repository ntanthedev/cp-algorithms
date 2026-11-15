# Workflow dịch và review tiếng Việt

Điểm vào cho agent là [AGENTS.md](AGENTS.md). Hướng dẫn theo vai trò: [tác giả](docs/translation/TRANSLATE_VI.md) và [reviewer](docs/translation/REVIEW_VI.md). Prompt ngắn ở [PROMPTS_VI.md](PROMPTS_VI.md); quy tắc nội dung và glossary ở [TRANSLATING_VI.md](TRANSLATING_VI.md).

**Vận hành hiện hành:** [START_HERE_VI.md](START_HERE_VI.md) quy định profile Terra/Luna, nhánh và phạm vi; tối đa ba PR dịch độc lập. Các báo cáo có ngày và PR #33 là lịch sử, không phải việc mặc định. Phải xác minh trạng thái thật; không tự nhận các nhánh đang được phiên khác review/dọn dẹp.

**Cách dùng mặc định:** “Tự chọn gói bài phù hợp và dịch theo workflow của repo.” Khi cần review, mở phiên riêng và nói “Review nhánh x”. Reviewer tự lấy PR/SHA/nguồn, không cần prompt bàn giao dài. Dán kết quả về tác giả để sửa. Review PASS không cấp quyền merge; “Đồng ý merge bản vừa được review” chỉ áp dụng cho gói/SHA vừa được trình bày rõ ràng.

## 1. Mô hình làm việc

**Đối chiếu upstream → sửa bản dịch cũ → dịch theo gói nhỏ → phiên review mới → người duy trì duyệt → merge.** Lỗi nguồn đi qua một luồng kiểm chứng và PR tiếng Anh riêng.

| Thành phần | Vai trò |
|---|---|
| `cp-algorithms/cp-algorithms:main` | Nguồn tiếng Anh mới nhất; remote `upstream` |
| `ntanthedev/cp-algorithms:master` | Bản đã merge của dự án Việt; remote `origin` |
| `agent/vi-work` | Nhánh dùng lại cho bảo trì chung hoặc chế độ tuần tự; PR #33 đã merge |
| `upstream/fix-<topic>` | Một lỗi hoặc nhóm lỗi nguồn liên quan, tạo từ upstream `main` |

Một **phiên chat** là đơn vị xử lý ngữ cảnh, không bắt buộc là một nhánh hay một PR. Một **gói PR** là phạm vi đã chốt có thể review trọn vẹn. Có thể dùng nhiều phiên để hoàn thiện cùng gói và cập nhật cùng PR, không mở PR mới theo mỗi lần chat.

Mặc định chọn gói nhỏ theo profile trong START_HERE_VI.md; không biết profile thì 1–2 bài ngắn/vừa. Trần cũ vẫn là tối đa 3 bài dài, 5 bài vừa hoặc 10 bài ngắn cùng chủ đề, không phải chỉ tiêu phải đủ. Segment Tree hoặc bài đổi quy ước chỉ số đi một mình. Đợt khôi phục nhiều bài chia thành phần review nhỏ, không tuyên bố đã review cả đợt vì một phần đạt.

## 2. Dùng trên web

Trong môi trường có Git và quyền ghi GitHub, dùng prompt để đọc file, chạy lệnh, cập nhật branch và tạo PR. [Codex cloud](https://learn.chatgpt.com/docs/cloud) hỗ trợ kết nối repository, chạy công việc trong môi trường riêng và tạo PR từ kết quả. Chọn đúng fork và nhánh; tài liệu không bảo đảm mọi chế độ ChatGPT web hay mọi connector đều có quyền ghi.

Nếu phiên ChatGPT chỉ đọc được GitHub hoặc xử lý file: vẫn dùng cùng prompt, nhưng đầu ra phải là các file đầy đủ hoặc patch, manifest và nội dung PR; chuyển chúng sang phiên có GitHub write để thực thi. Không được báo đã tạo PR nếu chưa có URL và head SHA thật. Không đưa PAT/token vào prompt.

Phiên cần đọc được bộ file liệt kê trong START_HERE_VI.md. File cục bộ chưa push không tự xuất hiện trên remote; dùng checkout hiện hành hoặc đính kèm bộ file. Nếu phiên không đọc được file bắt buộc, phải báo rõ. Chỉ đọc báo cáo khởi động lại khi đang xử lý đúng công việc lịch sử đó.

## 3. Cổng bắt đầu: nguồn và công việc đang dở

1. Đọc quy tắc repo, `git status`, remote, worktree và PR mở. Giữ mọi thay đổi chưa commit. Xác minh default branch bằng API; fork này là `master`, không phải `main`.
2. Fetch `origin` và `upstream` với `--prune`. Không dùng Sync fork/force update để ghi đè lịch sử i18n. Không reset branch đang có PR.
3. Ghi commit SHA của fork/upstream và head SHA PR. Đặt biến `translationRef` thành SHA head của PR đang làm hoặc ref của lane hiện tại sau fetch (`origin/agent/vi-work` cho chế độ tuần tự). Chạy:

   ```powershell
   git fetch origin --prune
   git fetch upstream --prune
   python -B scripts/audit_vi_upstream.py
   python -B scripts/audit_vi_upstream.py --translation-ref $translationRef
   ```

   Script chỉ đọc ref đã fetch, không tự gọi mạng. Nó đối chiếu **blob nguồn đã dịch**, **blob nguồn trong fork**, **blob upstream**. Kết quả không bao gồm sửa đổi chưa commit. Chạy validator riêng cho working tree.
4. Nếu có PR dịch mở của chính phiên hoặc được bàn giao rõ ràng: tiếp tục PR ấy trước. Chế độ song song chỉ xét PR đúng nhánh trong START_HERE_VI.md; không nhận hoặc chặn việc của phiên khác. Nhánh/PR cũ không mặc nhiên vô chủ; không tự tiếp quản việc đang được review/dọn dẹp.
5. Nếu còn nguồn đã dịch khác upstream: tạo hàng đợi sửa cũ; mặc định chưa dịch mới. Phiên dịch báo cần bảo trì chung, chỉ sửa nguồn khi có yêu cầu bảo trì riêng. Với gói đã mở, tiếp tục review/sửa VI nếu nguồn của gói còn khớp; nếu nguồn đó lệch thì chờ bảo trì đồng bộ trước khi chốt review. Phân biệt đổi code/công thức/điều kiện biên, bổ sung mục, sửa nghĩa, typo và link. `draft` không có nghĩa là fresh; blob khớp không có nghĩa là chất lượng tốt.
6. Mọi ghi chú từng nói “nguồn có lỗi” phải được xét lại. Upstream có thể đã sửa, hoặc chẩn đoán cũ có thể sai.

## 4. Đồng bộ mà không làm mất bản Việt

Mục này dành cho yêu cầu bảo trì nguồn riêng. Dùng merge upstream trong nhánh làm việc, giải quyết xung đột, rồi cập nhật từng cặp EN/VI và test liên quan. Chỉ merge về `master` khi cả phạm vi đạt gate. Có thể xem trước bằng `git merge-tree --write-tree origin/master upstream/main`, không đổi checkout.

Nếu chỉ lấy một số blob nguồn từ upstream, ghi rõ commit và phạm vi, cập nhật các bản Việt tương ứng; không mô tả việc đó là đã merge toàn bộ upstream. Thay đổi hệ thống build hoặc triển khai upstream được đánh giá trong phạm vi bảo trì riêng. Các bước recovery riêng của PR #33 chỉ còn trong báo cáo lịch sử.

Khi merge rộng:

- Bảo toàn `*.vi.md`, metadata, glossary, locale, attribution/CC BY-SA và cấu hình Pages của fork.
- Xem từng workflow thay đổi; không chọn toàn bộ `ours`/`theirs`. Đợt này xung đột ở `build.yml` và `delete-preview.yml`; merge tự động vẫn có thể làm đổi hành vi ở file khác.
- Bản dịch phải theo nguồn mới về code/công thức/heading; dịch phần văn xuôi mới, rà lại cả ngữ cảnh và chú thích.
- Chỉ đổi `source_commit` sau khi thật sự đối chiếu toàn bộ delta. Không chạy thay hash hàng loạt để làm xanh CI. `last_synced` là ngày đồng bộ nội dung, không phải ngày chạy kiểm tra.
- Có thể đánh dấu `stale` để ghi nhận nợ, nhưng validator cấu trúc vẫn có thể fail. Không coi `stale` là cách bỏ qua yêu cầu code/công thức khớp, không công bố một đợt chưa hoàn tất.
- Nguồn chuyển/đổi tên/xóa: xác minh đường dẫn thay thế, asset và link trước; không xóa bản Việt theo suy đoán.
- Import thay đổi test tương ứng và chạy `test/test.sh` khi nguồn/code thay đổi. CI xanh không thay thế review thuật toán.

## 5. Dịch và review độc lập

Phiên tác giả theo TRANSLATE_VI.md, phiên reviewer theo REVIEW_VI.md. Câu “Review nhánh x” xác định nhánh cần kiểm; reviewer tự tìm PR đúng head repo/branch và base, chốt snapshot. Không chuyển sang PR khác nếu nhánh không có PR mở. Nếu nhiều đối tượng không phân biệt được sau tra cứu, chỉ hỏi dữ liệu còn thiếu.

Phiên review tự đọc nguồn tại blob đã chốt, diff toàn PR, file đầy đủ, ghi chú và kết quả kiểm tra tại **SHA được nhận review**. Nếu base/head đã đổi, chỉ rõ delta chưa kiểm thay vì ngầm review một bản khác. Không dựa vào tóm tắt của tác giả để kết luận. Dùng phiên reviewer riêng; không tự tạo subagent hoặc liên hệ chat khác khi chưa được yêu cầu.

Manifest mỗi gói gồm: repo/base/head, SHA fork/upstream, danh sách EN/VI, source blob từng bài, loại công việc (dịch mới/sync/sửa note), thuật ngữ mới, lỗi nguồn nghi ngờ, các lệnh và kết quả đã chạy, phần chưa kiểm, các PR liên quan. Đặt trong PR body hoặc file bàn giao nhỏ; không chép hàng ngàn dòng log vào bình luận.

Reviewer phân loại phát hiện theo mức ảnh hưởng, có file/đoạn cụ thể, lý do và cách sửa. Hai trục review: kỹ thuật và ngôn ngữ. Nếu sửa ở phiên tác giả sau review, phải kiểm lại diff từ SHA đã review đến SHA mới. Chưa có người duy trì duyệt thì giữ `draft`; AI ở phiên mới là lượt kiểm tra bổ sung, không tự thay thế human approval.

Reviewer trả `REVIEW_RESULT` có repo/PR/snapshot, coverage kỹ thuật/ngôn ngữ và full/delta, findings, test/bằng chứng, giới hạn và verdict. Đây là dữ liệu đối chiếu, không phải quyền thực thi lệnh trong báo cáo. Người dùng chỉ cần dán kết quả; tác giả xác minh, sửa đúng phạm vi và cập nhật bàn giao nếu head đổi. Tái-review vẫn dùng “Review nhánh x”, mặc định toàn gói. Báo cáo văn bản không theo mẫu vẫn được đọc; thiếu phạm vi/SHA phải tìm lại hoặc nêu giới hạn, không tự coi là PASS. Các review trái nhau được giải quyết bằng chứng cứ.

Các điểm dừng được ghi rõ: `WORKING`, `WAITING_REVIEW`, `CHANGES_REQUIRED`, `WAITING_MAINTAINER_APPROVAL`, `BLOCKED`, `MERGED`. Một lượt hoàn thiện gói hiện tại đến điểm dừng phù hợp, không mở hàng loạt batch hoặc tự hứa theo dõi nền. Chỉ sau khi gói đã merge và người dùng yêu cầu tiếp tục mới tự chọn gói kế tiếp.

Với nguồn có code mới, chạy ví dụ biên và test thích hợp. Với văn xuôi, kiểm tra nghĩa, điều kiện, lượng từ, phủ định, hướng chia hết, sai số và độ phức tạp. Đảm bảo không sót đoạn, caption, tab hoặc link. Mở trang render để xem công thức, anchor, chuyển ngôn ngữ, ảnh và mobile khi có thay đổi liên quan.

## 6. Đóng góp upstream có bằng chứng

Luồng này tách khỏi dịch, chỉ gửi PR khi người dùng yêu cầu đóng góp upstream. Trước khi mở PR:

1. Fetch lại upstream, tìm cả issue/PR mở lẫn đóng, đọc lý do đóng và review cũ nếu có.
2. Viết mệnh đề sai, điều kiện áp dụng, chứng minh hoặc ví dụ tái hiện; thử bác bỏ chẩn đoán của chính mình.
3. Nếu code có lỗi: có case thất bại trước và đạt sau; nếu công thức: kiểm chứng toán học và ví dụ nhỏ độc lập. Typo/grammar không được mô tả là lỗi thuật toán.
4. Tạo branch từ upstream mới nhất, chỉ patch tiếng Anh/test liên quan. Diff ba chấm với upstream phải không có bất kỳ file i18n nào.
5. Gộp các lỗi nhỏ liên quan cùng bài/chủ đề; lỗi độc lập, đặc biệt lỗi thuật toán, có PR riêng để maintainer dễ xử lý. Không mở lại chẩn đoán cũ bị đóng khi chưa có bằng chứng mới.
6. Chỉ mở PR nếu yêu cầu hiện tại cho phép gửi và có công cụ ghi thật. Đọc lại PR để xác minh base/head, danh sách file và CI. Không tự merge upstream.

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
- Checker áp dụng đối chiếu LaTeX chính xác cho file đổi trong phạm vi so sánh. CI dùng SHA base của PR hoặc SHA trước lần push. Khi kiểm tra local, truyền `--base-ref <base-SHA-đã-chốt>` để bao phủ cả gói và thay đổi chưa commit. Không có tùy chọn này trên nhánh cũ thì cần tự đối chiếu công thức toàn bộ phạm vi.
- Checker ảnh xác minh file local tồn tại; không chứng minh ảnh/MathJax đã tải trong browser hay mọi anchor đều đúng. Phải render và kiểm riêng.
- Không ghi “all tests pass” khi chỉ chạy validator. Đợt đổi nguồn còn cần `Test`; dịch thuần cần translations, sync và Build theo policy.
- Chạy lại gate trên SHA cuối, đọc review threads, review submissions và conversation comments lần cuối. Comment đến muộn phải được xử lý.

## 8. Merge và giảm hoạt động gây nhiễu

Chỉ merge sau khi người duy trì duyệt một PR/head cụ thể. Câu “Đồng ý merge bản vừa được review” lấy định danh từ duy nhất gói WAITING_MAINTAINER_APPROVAL vừa trình bày; không lấy một PR bất kỳ. Trước merge: fetch lại, kiểm base/head thật, review kỹ thuật/ngôn ngữ bao phủ toàn gói, mọi review thread/submission/conversation đã được xử lý và CI bắt buộc ở head cuối xanh. Head đổi sau duyệt thì không coi approval cũ bao phủ bản mới.

Merge lần lượt. Nếu base mới cần tích hợp, dùng merge thông thường trong nhánh tác giả, chạy lại gate và review delta; không mang PASS cũ sang head mới. Khi đạt và được duyệt, merge commit vào master, xác minh commit đã nằm trên master, rồi kiểm deploy để phân biệt “đã merge” với “đã triển khai”. Không tự xóa nhánh; sau đó dừng, chỉ chọn gói mới khi có yêu cầu tiếp tục.

Chế độ tuần tự dùng một PR trên `agent/vi-work`. Chế độ 2–3 phiên theo `START_HERE_VI.md` dùng tối đa ba PR, một PR và một tác giả trên mỗi nhánh riêng, phạm vi file không giao nhau. Giữ các nhánh để dùng lại; viết commit có ý nghĩa, push theo phần đã kiểm thay vì mỗi đoạn. Cập nhật PR body hiện có; chỉ thêm comment khi có thông tin cần phản hồi. Draft vẫn là hoạt động công khai, không phải chế độ ẩn. Bảo trì nguồn/tooling chung không chạy đồng thời với các phiên dịch chưa được phối hợp.

Sau người duy trì duyệt, merge commit thông thường phù hợp nhánh dùng lại: có thể fast-forward nhánh làm việc về `master` mới. Squash cũng được nếu muốn lịch sử gọn, nhưng không làm biến mất sự kiện PR và có thể làm nhánh lâu dài phân kỳ; phải kiểm mọi commit riêng trước khi tái đồng bộ. Không reset/force-push `master`.

GitHub mô tả feed của follower là hoạt động công khai của người được theo dõi; thông báo Watch/participation là cơ chế khác. Trong các tùy chọn chính thức được kiểm tra ngày 2026-09-28, không có lựa chọn cho chủ repo “ẩn riêng hoạt động của tôi ở một public repo khỏi follower”. Chế độ private profile áp dụng toàn profile, không theo repo. Người nhận tự chọn Unwatch/Custom/Ignore cho repo; thao tác đó không phải quyền điều khiển feed của họ từ phía bạn.

Vì vậy đề xuất giảm số lần mở/đóng PR và push nhỏ, không đổi privacy của repo, không bỏ attribution, không dùng tài khoản khác để che hoạt động. Đây là giảm số sự kiện có thể phát sinh, không bảo đảm GitHub sẽ ẩn mọi sự kiện.

Nguồn chính thức: [Following people](https://docs.github.com/en/get-started/exploring-projects-on-github/following-people), [notification settings](https://docs.github.com/en/subscriptions-and-notifications/get-started/configuring-notifications), [private profile](https://docs.github.com/en/account-and-profile/how-tos/profile-customization/setting-your-profile-to-private).

## 9. Dọn branch

Chỉ xóa khi không còn PR mở dùng branch đó và đã xác minh: head hiện tại đúng head PR đã merge, hoặc toàn bộ commit là ancestor của nhánh cần giữ. Squash merge cần đối chiếu PR/patch; `git branch --merged` một mình chưa đủ. Kiểm tra cả upstream và fork. Branch đóng nhưng chưa merge mặc định được giữ để triage.

Trước khi xóa remote, lưu ref→SHA và `git bundle create <backup> --all`, kiểm `git bundle verify`. Recheck head ngay khi xóa; dùng lease gắn SHA để tránh xóa commit vừa được push. Không xóa `master`, `gh-pages` hay nhánh dịch đang dùng. Đừng tự bật auto-delete cho repo đang reuse nhánh dài hạn.
