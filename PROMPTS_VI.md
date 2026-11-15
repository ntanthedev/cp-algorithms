# Prompt ngắn cho dịch và review

Dùng khi phiên đọc được [AGENTS.md](AGENTS.md) và các file nó dẫn tới.
Nếu không tự nạp file này, thêm `Đọc AGENTS.md trước.` ở lần đầu.
Chọn model trong phiên làm việc; profile chỉ điều chỉnh cỡ gói.

## Dịch — mặc định

```text
Tự chọn gói bài phù hợp và dịch theo workflow của repo.
```

Các biến thể, mỗi dòng là một yêu cầu riêng:

```text
Dịch tiếp, profile Luna.
Dịch phiên 1, profile Terra.
Dịch phiên 2, profile Luna.
Dịch phiên 3, profile Terra.
```

Phiên 1/2/3 có nhánh và phạm vi trong [START_HERE_VI.md](START_HERE_VI.md).
Không gửi prompt không phân phạm vi vào nhiều tác giả cùng lúc.

## Review — phiên mới, chỉ đọc

```text
Review nhánh "agent/vi-graph".
```

Thay tên nhánh bằng nhánh cần review. Reviewer tự xác minh PR/SHA và kiểm cả kỹ
thuật lẫn tiếng Việt theo [REVIEW_VI.md](docs/translation/REVIEW_VI.md).
Nếu nhánh không còn PR mở, reviewer vẫn có thể kiểm snapshot nhánh nhưng phải
nêu rõ trạng thái; không chuyển sang PR khác hay tự mở lại PR.

## Sửa sau review

Trong phiên tác giả cũ: chỉ dán báo cáo review. Trong phiên tác giả mới:

```text
Sửa theo review nhánh "agent/vi-graph".
```

Dán báo cáo kèm theo nếu review chưa được đăng trên PR. Agent tự đọc review có
sẵn, không đòi nhập lại thông tin đã tra được và không coi thiếu review là PASS.
Tái-review vẫn dùng đúng câu `Review nhánh "agent/vi-graph".`

## Merge và tiếp tục

Sau khi tác giả trình bày đúng PR/head đã qua review và gate:

```text
Đồng ý merge bản vừa được review.
```

Sau merge:

```text
Dịch tiếp.
```

Không có lệnh merge thì giữ Draft PR. Một lượt dừng sau gói hiện tại.

## Bảo trì riêng khi cần

```text
Kiểm tra và đồng bộ các bản dịch lệch upstream theo WORKFLOW_VI.md.
```

```text
Kiểm chứng phát hiện lỗi nguồn đã bàn giao và tạo PR upstream nếu đủ bằng chứng, theo WORKFLOW_VI.md.
```

Hai yêu cầu bảo trì này có phạm vi riêng; câu “dịch tiếp” không tự cấp quyền sửa
nguồn, đổi tooling hoặc gửi PR upstream. Nếu có phiên bảo trì đang làm, phối hợp
phạm vi trước khi ghi.
