# Bắt đầu dịch bằng prompt ngắn

Chọn model **6.1 Terra** hoặc **6.0 Luna** cho phiên làm việc, rồi gửi:

```text
Tự chọn gói bài phù hợp và dịch theo workflow của repo.
```

Trong một phiên reviewer riêng, chỉ cần thay tên nhánh thật vào câu:

```text
Review nhánh "agent/vi-graph".
```

[AGENTS.md](AGENTS.md) dẫn tới đúng hướng dẫn theo vai trò. Tác giả tự chọn bài,
chạy kiểm tra và chuẩn bị Draft PR; reviewer tự lấy PR, base/head SHA và nguồn.
Không cần người dùng điền URL/SHA hay chuyển một prompt review dài.
Giữ luồng cũ: **dịch → review độc lập → sửa → duyệt merge → gói tiếp theo**.

## Chọn kích thước gói

Đây là cấu hình vận hành thận trọng, không phải khẳng định về năng lực model.
Hai model dùng cùng quy tắc chất lượng và gate:

| Profile | Gói khởi đầu | Khi bài phức tạp |
|---|---|---|
| Terra — 6.1 Terra | 2–3 bài vừa hoặc 3–5 bài ngắn cùng chủ đề | Một bài dài/nặng chứng minh mỗi gói |
| Luna — 6.0 Luna | 1–2 bài ngắn/vừa, ít cấu trúc đặc biệt | Một bài mỗi gói; ghi rõ điểm cần reviewer kiểm kỹ |

Nếu không biết model/profile, chọn 1–2 bài ngắn/vừa, không cần hỏi lại. Có thể ghi
“Dịch tiếp, profile Luna.” để chọn cỡ gói; câu này không tự đổi model của phiên.
“Hàng loạt” là nhiều gói có thể review, không gom toàn bộ bài còn lại vào một PR.
Mỗi lượt hoàn thiện gói hiện tại rồi dừng để review/duyệt.

## Nhánh và các phiên song song

| Phiên | Nhánh dùng lại | Phạm vi tương đối từ `src/` |
|---|---|---|
| Không ghi số — tuần tự | `agent/vi-work` | Tự chọn một chủ đề; chỉ dùng khi không có tác giả song song |
| 1 — Đồ thị | `agent/vi-graph` | `graph/` |
| 2 — Số học và cấu trúc dữ liệu | `agent/vi-math-ds` | `algebra/`, `combinatorics/`, `data_structures/`, `dynamic_programming/`, `sequences/` |
| 3 — Các chủ đề còn lại | `agent/vi-geometry-other` | `geometry/`, `linear_algebra/`, `num_methods/`, `others/`, `schedules/`, `game_theory/`, `string/` |

Gửi “Dịch phiên 1.”, “Dịch phiên 2.” hoặc “Dịch phiên 3.” vào các chat riêng nếu
muốn chạy song song; không mở hai tác giả cùng số. Tối đa ba PR dịch, một PR mỗi
phiên. Chỉ ghi `.vi.md` trong phạm vi được giao. PR ở phạm vi khác không chặn phiên
mình; vẫn loại mọi bài đang được xử lý khỏi danh sách chọn mới.

Mỗi tác giả dùng checkout/worktree riêng. Nếu nhánh đã có việc của chính phiên
mình hoặc được bàn giao rõ ràng thì tiếp tục; không suy ra nhánh cũ vô chủ vì PR
đã đóng. Khi phiên khác đang review/dọn nhánh đó, để nguyên và chỉ hỏi phần phân
công còn thiếu nếu không tìm được phạm vi độc lập. Không tự chọn nhánh khác để
lách một gói đang chờ review. Sau merge, chỉ fast-forward nhánh khi không còn
commit riêng cần giữ; không tự xóa nhánh.

Trước gói mới, fetch rồi đối chiếu cả local và remote của lane. Trong checkout
riêng sạch, nếu tip lane là ancestor của `origin/master`
(`git merge-base --is-ancestor HEAD origin/master` trả 0), cập nhật bằng
`git merge --ff-only origin/master`. Nếu local/remote phân kỳ thì đối chiếu commit
trước khi ghi, không tự reset. Việc review/sửa gói đang mở có nguồn còn khớp được
tiếp tục dù repo có nợ đồng bộ ở bài khác; nợ đó chỉ chặn chọn bài mới. Nếu chính
nguồn của gói lệch, bàn giao các cặp EN/VI cho bảo trì và chờ đồng bộ trước khi chốt review.

## File cần có trong phiên

Các file: `AGENTS.md`, `START_HERE_VI.md`, `WORKFLOW_VI.md`, `TRANSLATING_VI.md`,
`docs/translation/TRANSLATE_VI.md`, `docs/translation/REVIEW_VI.md`.
[PROMPTS_VI.md](PROMPTS_VI.md) chỉ là danh sách câu lệnh sao chép, không bắt buộc
đọc mỗi lượt. Nếu môi trường không tự đọc AGENTS.md, thêm “Đọc AGENTS.md trước.”
vào prompt lần đầu. Nếu nhánh cũ chưa có bộ file này, cung cấp bản hiện hành từ
checkout chung hoặc đính kèm chúng; không giả định file đã có trên remote.

File đính kèm là snapshot; luôn xác minh Git/PR thật. Báo cáo trong
`docs/translation/` có ngày tháng là lịch sử, không phải hàng đợi hiện tại.
