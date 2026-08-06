# Quy trình dịch tiếng Việt

Tài liệu này quy định cách tạo, đồng bộ và review bản dịch tiếng Việt của cp-algorithms.

## 1. Cấu trúc file

- Giữ nguyên file tiếng Anh làm nguồn chuẩn, ví dụ: `src/num_methods/binary_search.md`.
- Tạo bản tiếng Việt bằng hậu tố `.vi.md`, ví dụ: `src/num_methods/binary_search.vi.md`.
- Không sửa code, công thức, URL, shortcode, thẻ HTML hoặc MkDocs directive chỉ để phù hợp văn phong dịch.
- Không dịch tên hàm, tên biến, API, tên bài tập hoặc identifier trong code.

## 2. Metadata bắt buộc

Mỗi file `.vi.md` phải có front matter sau:

```yaml
---
translation:
  source: num_methods/binary_search.md
  source_commit: <SHA của file nguồn khi bắt đầu dịch>
  status: draft
  last_synced: YYYY-MM-DD
---
```

Các trạng thái hợp lệ:

- `draft`: bản dịch đang làm hoặc chưa review kỹ thuật.
- `technical-reviewed`: đã kiểm tra thuật toán, code, công thức và độ phức tạp.
- `language-reviewed`: đã kiểm tra tiếng Việt và thuật ngữ.
- `ready`: đã qua cả review kỹ thuật và ngôn ngữ.
- `stale`: file nguồn đã thay đổi và bản dịch cần đồng bộ.

Không tự đặt `ready` trong cùng PR tạo bản dịch. Cần ít nhất một lượt review độc lập.

## 3. Nguyên tắc dịch

1. Dịch đúng ý, không dịch từng chữ.
2. Câu văn phải dễ đọc với học sinh THPT đã biết C++ cơ bản.
3. Lần xuất hiện đầu tiên của thuật ngữ quan trọng dùng dạng `tiếng Việt (English)`.
4. Sau lần đầu có thể dùng thuật ngữ tiếng Việt hoặc tên tiếng Anh phổ biến, nhưng phải nhất quán trong cả bài.
5. Giữ nguyên ký hiệu toán học, chỉ số, điều kiện biên và độ phức tạp.
6. Không tự thêm khẳng định kỹ thuật mới vào nội dung gốc. Phần giải thích bổ sung phải đặt trong admonition `Ghi chú bản dịch`.
7. Không thay đổi code mẫu, trừ PR riêng sửa lỗi upstream và có giải thích rõ.
8. Giữ nguyên link nguồn, attribution của hình ảnh và giấy phép.
9. Không dùng các từ dịch mơ hồ nếu thuật ngữ tiếng Anh đã phổ biến trong cộng đồng competitive programming.
10. Không dùng văn phong máy dịch hoặc câu quá dài.

## 4. Thuật ngữ mặc định

| English | Tiếng Việt đề xuất |
|---|---|
| binary search | tìm kiếm nhị phân |
| lower bound | cận dưới |
| upper bound | cận trên |
| predicate | vị từ / hàm điều kiện |
| monotonic | đơn điệu |
| loop invariant | bất biến vòng lặp |
| half-open interval | đoạn nửa mở |
| time complexity | độ phức tạp thời gian |
| space complexity | độ phức tạp bộ nhớ |
| connected component | thành phần liên thông |
| shortest path | đường đi ngắn nhất |
| spanning tree | cây khung |
| dynamic programming | quy hoạch động |

Nếu cần đổi thuật ngữ chung, sửa bảng này trong một PR riêng hoặc giải thích rõ trong PR dịch.

## 5. Những phần phải giữ nguyên cấu trúc

CI sẽ kiểm tra các cấu trúc sau giữa file nguồn và bản dịch:

- chuỗi cấp heading (`#`, `##`, `###`, ...);
- code fence và ngôn ngữ của code fence;
- nội dung trong các code block;
- đích của Markdown link và image;
- block công thức `$$`;
- Jinja/MkDocs expression như `{% ... %}` và `{{ ... }}`;
- thẻ HTML quan trọng;
- marker admonition như `!!! note` hoặc `??? example`.

Nếu thật sự cần thay đổi cấu trúc, phải giải thích trong PR và cập nhật validator có chủ đích; không được né CI bằng cách xóa kiểm tra.

## 6. Checklist cho người dịch

- [ ] Đã lấy file nguồn mới nhất từ `master`.
- [ ] Đã điền đúng `source`, `source_commit`, `last_synced`.
- [ ] Không thay đổi code và công thức.
- [ ] Tất cả link, hình ảnh và attribution còn nguyên.
- [ ] Thuật ngữ nhất quán với tài liệu này.
- [ ] Chạy `python scripts/check_vi_translations.py`.
- [ ] Chạy `mkdocs build --strict`.
- [ ] Đọc lại trang đã render, gồm desktop và mobile.
- [ ] PR chỉ chứa một bài dài hoặc tối đa 3–5 bài ngắn.

## 7. Checklist review kỹ thuật

- [ ] Đối chiếu từng định nghĩa, điều kiện biên và invariant với bản gốc.
- [ ] Kiểm tra ví dụ, chỉ số mảng, dấu bất đẳng thức và ký hiệu toán học.
- [ ] Kiểm tra độ phức tạp và kết luận thuật toán.
- [ ] Build strict thành công.
- [ ] Không có code hoặc link bị thay đổi ngoài chủ đích.
- [ ] Đặt trạng thái `technical-reviewed` nếu đạt.

## 8. Checklist review ngôn ngữ

- [ ] Câu tiếng Việt tự nhiên, không tối nghĩa.
- [ ] Thuật ngữ nhất quán.
- [ ] Không bỏ sót đoạn, caption, note hoặc alt text.
- [ ] Không thêm ý mới như thể thuộc nội dung gốc.
- [ ] Đặt trạng thái `language-reviewed` nếu đạt.

Sau khi cả hai review hoàn tất, một maintainer mới đổi trạng thái thành `ready`.

## 9. Đồng bộ upstream

1. Đồng bộ fork với `cp-algorithms/cp-algorithms` định kỳ.
2. Mỗi lần file tiếng Anh thay đổi, so sánh commit mới với `source_commit` trong bản dịch.
3. Nếu thay đổi chỉ là format hoặc typo không ảnh hưởng nghĩa, cập nhật bản dịch và `source_commit` trong PR nhỏ.
4. Nếu thay đổi nội dung thuật toán, đánh dấu `status: stale` trước, sau đó dịch lại phần liên quan và review kỹ thuật.
5. Không merge tự động nội dung dịch do AI tạo mà chưa có người đọc lại.

## 10. Quy tắc dùng AI

AI có thể tạo bản nháp, đối chiếu cấu trúc và phát hiện phần chưa đồng bộ. Người review chịu trách nhiệm cuối cùng về:

- tính đúng đắn thuật toán;
- thuật ngữ tiếng Việt;
- code, công thức và link;
- tuân thủ CC BY-SA 4.0;
- việc đánh dấu nội dung là bản dịch cộng đồng, không phải bản chính thức.
