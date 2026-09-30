# Bắt đầu 2–3 phiên dịch song song

PR đồng bộ [#33](https://github.com/ntanthedev/cp-algorithms/pull/33) đã merge ngày 2026-09-30. Đây là hướng dẫn vận hành hiện hành; các báo cáo ngày 2026-09-28 là lịch sử, không phải hàng đợi công việc chưa hoàn tất.

Mỗi phiên dùng **một prompt riêng dưới đây**, không cần điền đường dẫn bài, URL PR hoặc SHA. Hai phiên thì dùng 1 và 2; ba phiên thì thêm 3. Mỗi phiên tự chọn bài trong phạm vi riêng. Không mở hai phiên tác giả cùng một số.

| Phiên | Nhánh dùng lại | Thư mục nguồn được chọn |
|---|---|---|
| 1 — Đồ thị | `agent/vi-graph` | `graph/` |
| 2 — Số học và cấu trúc dữ liệu | `agent/vi-math-ds` | `algebra/`, `combinatorics/`, `data_structures/`, `dynamic_programming/`, `sequences/` |
| 3 — Hình học và các chủ đề còn lại | `agent/vi-geometry-other` | `geometry/`, `linear_algebra/`, `num_methods/`, `others/`, `schedules/`, `game_theory/`, `string/` |

Các đường dẫn trong bảng tương đối từ `src/`. Ba phạm vi không giao nhau. `agent/vi-work` được giữ cho bảo trì chung hoặc chạy tuần tự; không chạy thêm tác giả ở nhánh này đồng thời với ba phiên trên.

## Quy tắc chung cho chế độ song song

1. Mỗi nhánh chỉ có một phiên tác giả và tối đa một Draft PR mở vào `master`. Tối đa ba PR dịch song song; PR của phiên khác không chặn phiên mình. Dùng nhiều lượt chat để hoàn thiện cùng gói, không tạo PR theo mỗi lần trả lời.
2. Mỗi phiên chỉ tạo/sửa `src/**/*.vi.md` trong phạm vi của mình. Không sửa nguồn EN, glossary, workflow, scripts, cấu hình site hoặc tài liệu chung. Đề xuất thuật ngữ mới và lỗi nguồn ghi trong PR body/bàn giao; bảo trì chung xử lý chúng riêng.
3. Fetch và kiểm tra PR/nhánh của chính phiên trước. Nếu đã có PR thì tiếp tục nó. Nếu branch có commit riêng chưa được xử lý, đọc và tiếp tục công việc đó, không reset. Nếu một phiên khác đang là tác giả của cùng nhánh, không cùng ghi; dùng reviewer chỉ đọc hoặc yêu cầu làm rõ.
4. Mỗi phiên dùng checkout/môi trường riêng nếu có Git. Không để hai phiên đổi branch hoặc sửa chung một working tree. Không suy ra rằng mỗi chat mặc nhiên có checkout riêng; kiểm tra trước khi thao tác.
5. Nếu nguồn đã dịch trên `master` lệch upstream, ngừng chọn bài mới và báo cần bảo trì nguồn chung; không để ba phiên tự merge upstream riêng rẽ. Nhánh bảo trì phải được phối hợp sau khi các phạm vi đang làm đã được ghi nhận.
6. Khi không còn nợ đồng bộ, tự chọn gói 1–3 bài dài, tối đa 5 bài vừa hoặc 5–10 bài ngắn cùng chủ đề; một bài rất dài đi riêng. Loại redirect, bài đã có VI và bài đang được dịch. Các gợi ý khởi đầu dưới đây không phải danh sách bắt buộc; phải kiểm tra trạng thái thật.
7. Giữ `status: draft`; chạy đủ kiểm tra theo `TRANSLATING_VI.md`. Chỉ cập nhật source blob sau khi thực sự dịch/đồng bộ. Không coi metadata `draft` của các bài cũ là hàng đợi để tự viết lại mọi bài.
8. Tạo sẵn prompt reviewer chứa URL PR, base/head SHA thật, nguồn và phạm vi. Người dùng chỉ chuyển prompt sang chat reviewer rồi dán kết quả trở lại. Nếu cùng Project, reviewer vẫn phải tự đối chiếu nguồn/diff thay vì tin kết luận tác giả.
9. Merge lần lượt, không merge đồng thời. Trước mỗi merge, fetch `master`, tích hợp base mới bằng merge thông thường nếu cần và kiểm tra lại head/gate. Review cũ không bao phủ delta mới. Chỉ merge khi người duy trì cho phép.
10. Sau merge, giữ nhánh để dùng lại; fast-forward về `master` nếu được và chắc chắn không có công việc riêng cần giữ. Không force-push `master`, không tự xóa nhánh của phiên khác.

## Phiên 1 — Sao chép nguyên khối

```text
Tôi giao cho bạn phiên dịch số 1 — Đồ thị của ntanthedev/cp-algorithms.
Fork: https://github.com/ntanthedev/cp-algorithms, base master.
Upstream: https://github.com/cp-algorithms/cp-algorithms, main.
Nhánh riêng của phiên: agent/vi-graph. Chỉ được tạo/sửa bản dịch .vi.md thuộc src/graph/.

Đọc START_HERE_VI.md, WORKFLOW_VI.md, TRANSLATING_VI.md và PROMPTS_VI.md từ master mới nhất hoặc file dự án. Áp dụng prompt 0 theo chế độ song song của START_HERE_VI.md: chỉ tiếp tục PR của nhánh phiên mình; PR ở hai phiên khác không phải lý do dừng hay nhận việc của họ. Không ghi vào agent/vi-work, nguồn EN, glossary hoặc cấu hình chung.

Tự fetch, xác minh quyền và checkout riêng, kiểm tra nguồn còn đồng bộ, rồi tự chọn gói chưa dịch trong phạm vi. Gợi ý đầu tiên là search-for-connected-components.md, mst_kruskal_with_dsu.md và second_best_mst.md nếu vẫn chưa dịch; điều chỉnh số bài theo độ dài và prerequisite, không hỏi tôi điền tên bài. Nếu nhánh đã có công việc/PR thì hoàn thiện nó trước. Không reset công việc chưa merge.

Được phép dịch, kiểm tra, commit/push nhánh riêng và tạo/cập nhật một Draft PR vào master. Tuân thủ glossary, code/LaTeX/links/metadata và giấy phép. Không tự merge/ready. Nếu thiếu công cụ ghi, xuất file/patch và bàn giao thật, không bịa thao tác GitHub.

Khi đủ điều kiện review, xuất prompt review hoàn chỉnh đã điền URL/SHA/phạm vi thật. Khi tôi dán review trở lại, tự kiểm chứng và sửa findings đúng, chạy lại gate, cập nhật cùng PR và tạo prompt tái-review nếu head đổi. Không cần tôi điền URL hoặc viết thêm yêu cầu sửa. Dừng sau gói hiện tại để review/duyệt; không mở hàng loạt PR.
```

## Phiên 2 — Sao chép nguyên khối

```text
Tôi giao cho bạn phiên dịch số 2 — Số học và cấu trúc dữ liệu của ntanthedev/cp-algorithms.
Fork: https://github.com/ntanthedev/cp-algorithms, base master.
Upstream: https://github.com/cp-algorithms/cp-algorithms, main.
Nhánh riêng của phiên: agent/vi-math-ds. Chỉ được tạo/sửa bản dịch .vi.md trong src/algebra/, src/combinatorics/, src/data_structures/, src/dynamic_programming/ và src/sequences/.

Đọc START_HERE_VI.md, WORKFLOW_VI.md, TRANSLATING_VI.md và PROMPTS_VI.md từ master mới nhất hoặc file dự án. Áp dụng prompt 0 theo chế độ song song của START_HERE_VI.md: chỉ tiếp tục PR của nhánh phiên mình; PR ở hai phiên khác không phải lý do dừng hay nhận việc của họ. Không ghi vào agent/vi-work, nguồn EN, glossary hoặc cấu hình chung.

Tự fetch, xác minh quyền và checkout riêng, kiểm tra nguồn còn đồng bộ, rồi tự chọn gói chưa dịch trong phạm vi. Gợi ý đầu tiên là combinatorics/generating_combinations.md, combinatorics/stars_and_bars.md và combinatorics/bracket_sequences.md nếu vẫn chưa dịch; điều chỉnh số bài theo độ dài và prerequisite, không hỏi tôi điền tên bài. Nếu nhánh đã có công việc/PR thì hoàn thiện nó trước. Không reset công việc chưa merge.

Được phép dịch, kiểm tra, commit/push nhánh riêng và tạo/cập nhật một Draft PR vào master. Tuân thủ glossary, code/LaTeX/links/metadata và giấy phép. Không tự merge/ready. Nếu thiếu công cụ ghi, xuất file/patch và bàn giao thật, không bịa thao tác GitHub.

Khi đủ điều kiện review, xuất prompt review hoàn chỉnh đã điền URL/SHA/phạm vi thật. Khi tôi dán review trở lại, tự kiểm chứng và sửa findings đúng, chạy lại gate, cập nhật cùng PR và tạo prompt tái-review nếu head đổi. Không cần tôi điền URL hoặc viết thêm yêu cầu sửa. Dừng sau gói hiện tại để review/duyệt; không mở hàng loạt PR.
```

## Phiên 3 — Sao chép nguyên khối

```text
Tôi giao cho bạn phiên dịch số 3 — Hình học và các chủ đề còn lại của ntanthedev/cp-algorithms.
Fork: https://github.com/ntanthedev/cp-algorithms, base master.
Upstream: https://github.com/cp-algorithms/cp-algorithms, main.
Nhánh riêng của phiên: agent/vi-geometry-other. Chỉ được tạo/sửa bản dịch .vi.md trong src/geometry/, src/linear_algebra/, src/num_methods/, src/others/, src/schedules/, src/game_theory/ và src/string/.

Đọc START_HERE_VI.md, WORKFLOW_VI.md, TRANSLATING_VI.md và PROMPTS_VI.md từ master mới nhất hoặc file dự án. Áp dụng prompt 0 theo chế độ song song của START_HERE_VI.md: chỉ tiếp tục PR của nhánh phiên mình; PR ở hai phiên khác không phải lý do dừng hay nhận việc của họ. Không ghi vào agent/vi-work, nguồn EN, glossary hoặc cấu hình chung.

Tự fetch, xác minh quyền và checkout riêng, kiểm tra nguồn còn đồng bộ, rồi tự chọn gói chưa dịch trong phạm vi. Ưu tiên geometry/basic-geometry.md nếu vẫn chưa dịch: đây là bài nền tảng dài nên có thể dành riêng cả gói. Nếu bài này đã xong, tự chọn bài tiếp theo theo prerequisite và độ hữu ích, không hỏi tôi điền tên bài. Nếu nhánh đã có công việc/PR thì hoàn thiện nó trước. Không reset công việc chưa merge.

Được phép dịch, kiểm tra, commit/push nhánh riêng và tạo/cập nhật một Draft PR vào master. Tuân thủ glossary, code/LaTeX/links/metadata và giấy phép. Không tự merge/ready. Nếu thiếu công cụ ghi, xuất file/patch và bàn giao thật, không bịa thao tác GitHub.

Khi đủ điều kiện review, xuất prompt review hoàn chỉnh đã điền URL/SHA/phạm vi thật. Khi tôi dán review trở lại, tự kiểm chứng và sửa findings đúng, chạy lại gate, cập nhật cùng PR và tạo prompt tái-review nếu head đổi. Không cần tôi điền URL hoặc viết thêm yêu cầu sửa. Dừng sau gói hiện tại để review/duyệt; không mở hàng loạt PR.
```

## File dự án và bàn giao

Nếu dùng Project trên web, cập nhật bộ file chung thành bản mới nhất của `START_HERE_VI.md`, `PROMPTS_VI.md`, `WORKFLOW_VI.md`, `TRANSLATING_VI.md`. Bản tải lên là snapshot, nên prompt luôn yêu cầu kiểm GitHub trước khi hành động. Không đặt prompt của riêng phiên 1/2/3 vào instructions chung của Project; chỉ gửi vào chat tương ứng. Phiên review nhận gói bàn giao của đúng PR, không tự chọn nhánh khác.

Tạo Project không tự cung cấp quyền ghi GitHub hoặc checkout riêng. Nếu công cụ không có khả năng thao tác repo, tác giả phải bàn giao file/patch để phiên có quyền ghi tiếp nhận. Không cần và không nên dán token vào prompt.
