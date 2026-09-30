# Validation — workflow restart 2026-09-28

Phạm vi: patch workflow/tooling và một ghi chú trong `discrete-root.vi.md`, trên fork base `3cff374c22250aea8b9182904f08543a7f146141`. Các bài tiếng Anh và code thuật toán không thay đổi trong patch này. Chưa chạy CI remote cho patch vì chưa push.

| Kiểm tra | Kết quả |
|---|---|
| `python -B scripts/test_vi_staleness.py` | PASS: CRLF và LF có cùng Git blob; sửa nội dung chưa commit làm đổi hash |
| `python -B scripts/test_vi_review_scope.py` | PASS: phạm vi hai commit + bản dịch chưa track; base không tồn tại bị từ chối |
| `python -B scripts/check_vi_translations.py --base-ref origin/master` | PASS: 86 file; exact LaTeX cho Discrete Root là file VI thay đổi trong patch |
| `python -B scripts/check_vi_staleness.py` | PASS: 86 metadata khớp nguồn fork; không có nghĩa là khớp upstream |
| `python -B scripts/check_vi_markdown_safety.py` | PASS |
| `python -m mkdocs build --strict` | PASS, exit 0, khoảng 110 giây trên máy này |
| `python -B scripts/check_vi_rendered_pages.py` | PASS: 587 tham chiếu ảnh local dưới `public/vi/` |
| Audit master / PR #33 | 86/47 và 89/49 (tổng bản dịch / nguồn khác upstream) |
| Audit đối chứng cùng ref master/master | PASS: 86 bản dịch, 0 stale |
| Checker với base không tồn tại | Exit 2 đúng dự kiến; không im lặng bỏ qua |
| Discrete Root: kiểm chứng số học bổ sung | 210.000 tổ hợp k,m ∈ [1,100], l ∈ [-10,10] đều thỏa tương đương; chứng minh vẫn là căn cứ chính |
| Browser local | Trang Discrete Root tải được, MathJax render, mục lục đưa đến đúng mục; ghi chú mới là đoạn riêng, nhìn rõ trong screenshot |
| `git diff --check` | PASS |
| Git bundle trước dọn branch | `git bundle verify` PASS; bundle có complete history |

Môi trường build riêng ở `.git/translation-restart-20260928/venv`, Python 3.13; submodule checkout đúng commit `35e2f65a913888006067faf4aac126ebcdf8e509`. CI đang dùng Python 3.11, nên kết quả local không được gọi là đã chạy CI. Log build và dependency ở cùng thư mục `.git` đó. Không cài thêm package vào Python global.

## Giới hạn và nợ đã thấy

- Chưa review kỹ thuật/ngôn ngữ toàn bộ 86 bài; chưa cập nhật 47 nguồn lệch upstream. Metadata `draft` được giữ.
- Không chạy bộ C++ toàn repo vì patch này không đổi code/nguồn thuật toán. Đợt sync nguồn tới phải chạy test tương ứng và full gate theo policy.
- Browser kiểm trang có ghi chú sửa; không phải đợt QA mobile/toàn website. Bộ kiểm ảnh chỉ kiểm file local, không xác minh toàn bộ tài nguyên ngoài mạng.
- Strict build thành công nhưng log có INFO về **hai fragment link cũ không có anchor**: `extended-euclid-algorithm.vi.md` → `euclid-algorithm.md#implementation`, và `phi-function.vi.md` → `sieve-of-eratosthenes.md#segmented-sieve`. Cần sửa routing/anchor alias có chủ đích trong maintenance, không tự đổi mọi URL của bản dịch hay nới validator.
- Log còn có trang redirect `sequences/longest_increasing_subsequence.md` ngoài nav và thông tin định dạng locale alternate link. Không kết luận toàn site “không có lỗi” từ exit 0.
- Upstream merge preview có conflict build/delete-preview; chưa apply merge vào working branch hoặc master.
- Không tạo PR mới, không gửi review/comment upstream, không thay profile/privacy/notification settings.
