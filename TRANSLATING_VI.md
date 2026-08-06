# Quy trình dịch tiếng Việt

Tài liệu này quy định cách bắt đầu, tạo, đồng bộ và review bản dịch tiếng Việt của cp-algorithms.

## 0. Cổng bắt đầu một batch dịch mới

Không bắt đầu dịch ngay sau khi chọn tên bài. Mỗi batch phải hoàn tất các bước chuẩn bị sau:

1. Xác nhận nhánh `master` mới nhất đang build xanh và branch dịch được tạo từ `master`.
2. Chọn phạm vi có thể review:
   - một bài dài hoặc nhiều công thức/cấu trúc đặc biệt;
   - tối đa ba bài cỡ vừa;
   - từ ba đến năm bài ngắn, cùng nhóm kiến thức.
3. Đọc toàn bộ file nguồn trước khi dịch và lập kiểm kê các thành phần nhạy cảm:
   - front matter;
   - chuỗi cấp heading;
   - code fence và ngôn ngữ code;
   - inline code;
   - công thức khối `$$`;
   - Markdown link, image và link tham chiếu;
   - HTML;
   - MkDocs tabs, admonition, attribute list, Jinja hoặc macro.
4. Chốt thuật ngữ mới trước khi viết. Nếu thuật ngữ chưa có trong bảng chung, ghi lựa chọn và lý do trong PR.
5. Lấy **Git blob SHA** của từng file nguồn tại thời điểm bắt đầu, không dùng SHA của commit chứa toàn repository:

   ```bash
   git rev-parse HEAD:src/algebra/euclid-algorithm.md
   ```

6. Sao chép file nguồn thành file `.vi.md`, giữ nguyên toàn bộ cấu trúc trước, rồi mới thêm metadata dịch và dịch phần văn xuôi.
7. Mọi file mới bắt đầu với `status: draft`.
8. Chưa mở PR nếu chưa chạy được preflight. Trường hợp chỉ có môi trường connector và không thể build cục bộ, PR bắt buộc là Draft và không được merge trước khi CI xanh.

### Preflight bắt buộc trước khi mở PR

```bash
python scripts/check_vi_translations.py
python scripts/check_vi_staleness.py
MKDOCS_ENABLE_GIT_REVISION_DATE=False \
MKDOCS_ENABLE_GIT_COMMITTERS=False \
mkdocs build --strict
```

Sau khi build, mở ít nhất một bài trên bản tiếng Việt và kiểm tra:

- chuyển ngôn ngữ;
- mục lục;
- code tabs;
- công thức;
- link nội bộ;
- hình ảnh;
- giao diện desktop và mobile.

## 1. Cấu trúc file

- Giữ nguyên file tiếng Anh làm nguồn chuẩn, ví dụ: `src/num_methods/binary_search.md`.
- Tạo bản tiếng Việt bằng hậu tố `.vi.md`, ví dụ: `src/num_methods/binary_search.vi.md`.
- Không sửa code, công thức, URL, shortcode, thuộc tính HTML cấu trúc hoặc MkDocs directive chỉ để phù hợp văn phong dịch.
- Không dịch tên hàm, tên biến, API, tên bài tập hoặc identifier trong code.
- Giữ nguyên thứ tự đoạn và phạm vi nội dung. Không gộp hai đoạn kỹ thuật thành một nếu việc đó làm khó đối chiếu nguồn.
- Mỗi commit nên chứa một bài dịch hoặc một thay đổi quy tắc độc lập để dễ xác định lỗi CI.

## 2. Metadata bắt buộc

Mỗi file `.vi.md` phải giữ nguyên metadata của file nguồn và thêm block `translation`:

```yaml
---
tags:
  - Translated
e_maxx_link: binary_search
translation:
  source: num_methods/binary_search.md
  source_commit: <Git blob SHA của file nguồn khi bắt đầu dịch>
  status: draft
  last_synced: YYYY-MM-DD
---
```

Tên `source_commit` được giữ để tương thích với hệ thống hiện tại, nhưng giá trị của nó là **blob SHA của file nguồn**, không phải commit SHA của repository.

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
7. Không thay đổi code mẫu, kể cả comment trong code block. Nếu comment tiếng Anh cần giải thích, thêm lời giải thích ở ngoài code block.
8. Giữ nguyên link nguồn, attribution của hình ảnh và giấy phép.
9. Không dùng các từ dịch mơ hồ nếu thuật ngữ tiếng Anh đã phổ biến trong cộng đồng competitive programming.
10. Không dùng văn phong máy dịch hoặc câu quá dài.
11. Dùng quan hệ chia hết chính xác:
    - `a chia hết cho b`;
    - `b là ước của a`;
    - không viết `b chia hết a`.
12. Tránh cách so sánh số lần gây mơ hồ như `nhỏ hơn hai lần`. Viết rõ `không vượt quá một nửa`, `giảm còn một nửa` hoặc dùng bất đẳng thức.
13. Phân biệt thuật ngữ đồ thị:
    - `walk`: hành trình;
    - `path`: đường đi;
    - `cycle`: chu trình;
    - `connected component`: thành phần liên thông.
14. Có thể dịch nội dung của thuộc tính HTML `alt`, `title`, `aria-label`; không được đổi tên thuộc tính hoặc các thuộc tính cấu trúc như `src`, `href`, `class`, `id`, `style`, `data-*`.
15. Heading được dịch, nhưng cấp và thứ tự heading phải giữ nguyên.
16. Inline code như `` `std::gcd` ``, `` `used[]` `` và `` `O(n + m)` `` phải giữ nguyên.

## 4. Thuật ngữ mặc định

| English | Tiếng Việt đề xuất |
|---|---|
| binary search | tìm kiếm nhị phân |
| breadth-first search | tìm kiếm theo chiều rộng |
| depth-first search | tìm kiếm theo chiều sâu |
| lower bound | cận dưới |
| upper bound | cận trên |
| predicate | vị từ / hàm điều kiện |
| monotonic | đơn điệu |
| loop invariant | bất biến vòng lặp |
| half-open interval | đoạn nửa mở |
| time complexity | độ phức tạp thời gian |
| space complexity | độ phức tạp bộ nhớ |
| greatest common divisor | ước chung lớn nhất |
| least common multiple | bội chung nhỏ nhất |
| Sieve of Eratosthenes | Sàng Eratosthenes |
| segmented sieve | sàng phân đoạn |
| connected component | thành phần liên thông |
| shortest path | đường đi ngắn nhất |
| walk | hành trình |
| cycle | chu trình |
| spanning tree | cây khung |
| dynamic programming | quy hoạch động |

Nếu cần đổi thuật ngữ chung, sửa bảng này trong một PR riêng hoặc giải thích rõ trong PR dịch.

## 5. Những phần phải giữ nguyên cấu trúc

CI sẽ kiểm tra các cấu trúc sau giữa file nguồn và bản dịch:

- metadata nguồn ngoài block `translation`;
- chuỗi cấp heading (`#`, `##`, `###`, ...);
- code fence và ngôn ngữ của code fence;
- nội dung trong các code block;
- inline code;
- đích của Markdown link và image;
- block công thức `$$`;
- Jinja/MkDocs expression như `{% ... %}` và `{{ ... }}`;
- cấu trúc thẻ HTML và các thuộc tính không thể dịch;
- số lượng, thứ tự và mức thụt lề của MkDocs tabs;
- marker admonition như `!!! note` hoặc `??? example`.

Nội dung `alt`, `title`, `aria-label` được phép dịch nhưng thuộc tính phải còn tồn tại đúng vị trí.

Nếu thật sự cần thay đổi cấu trúc, phải giải thích trong PR và cập nhật validator có chủ đích; không được né CI bằng cách xóa kiểm tra.

## 6. Checklist cho người dịch

- [ ] Nhánh dịch được tạo từ `master` mới nhất và CI của `master` đang xanh.
- [ ] Phạm vi batch tuân thủ giới hạn một bài dài, tối đa ba bài vừa hoặc 3–5 bài ngắn.
- [ ] Đã đọc toàn bộ nguồn và kiểm kê cấu trúc nhạy cảm.
- [ ] Đã chốt thuật ngữ mới trước khi dịch.
- [ ] Đã điền đúng `source`, blob SHA trong `source_commit`, `last_synced`.
- [ ] Metadata nguồn được giữ nguyên.
- [ ] Không thay đổi code, comment trong code và công thức.
- [ ] Inline code còn nguyên.
- [ ] Tất cả link, hình ảnh và attribution còn nguyên.
- [ ] HTML chỉ thay đổi nội dung thuộc tính có thể dịch.
- [ ] Thuật ngữ nhất quán với tài liệu này.
- [ ] Không bỏ sót đoạn, caption, note, alt text hoặc nội dung trong tab.
- [ ] Chạy `python scripts/check_vi_translations.py`.
- [ ] Chạy `python scripts/check_vi_staleness.py`.
- [ ] Chạy `mkdocs build --strict`.
- [ ] Đọc lại trang đã render trên desktop và mobile.
- [ ] Mỗi bài nằm trong commit riêng khi có thể.
- [ ] PR được mở ở trạng thái Draft.

## 7. Checklist review kỹ thuật

- [ ] Đối chiếu từng định nghĩa, điều kiện biên và invariant với bản gốc.
- [ ] Kiểm tra chiều của quan hệ chia hết và quan hệ bất đẳng thức.
- [ ] Kiểm tra ví dụ, chỉ số mảng, dấu bất đẳng thức và ký hiệu toán học.
- [ ] Kiểm tra độ phức tạp và kết luận thuật toán.
- [ ] Kiểm tra phân biệt `walk`, `path`, `trail`, `cycle` nếu bài có dùng.
- [ ] Build strict thành công.
- [ ] Không có code, inline code hoặc link bị thay đổi ngoài chủ đích.
- [ ] Đặt trạng thái `technical-reviewed` nếu đạt.

## 8. Checklist review ngôn ngữ

- [ ] Câu tiếng Việt tự nhiên, không tối nghĩa.
- [ ] Không có cấu trúc dịch máy hoặc câu bám sát trật tự tiếng Anh.
- [ ] Thuật ngữ nhất quán.
- [ ] Không dùng cách nói mơ hồ như `nhỏ hơn/lớn hơn X lần`.
- [ ] Quan hệ chia hết được diễn đạt đúng chiều.
- [ ] Không bỏ sót đoạn, caption, note, alt text hoặc nhãn tab.
- [ ] Không thêm ý mới như thể thuộc nội dung gốc.
- [ ] Đặt trạng thái `language-reviewed` nếu đạt.

Sau khi cả hai review hoàn tất, một maintainer mới đổi trạng thái thành `ready`.

## 9. Đồng bộ upstream

1. Đồng bộ fork với `cp-algorithms/cp-algorithms` định kỳ.
2. Mỗi lần file tiếng Anh thay đổi, so sánh blob SHA mới với `source_commit` trong bản dịch.
3. Nếu thay đổi chỉ là format hoặc typo không ảnh hưởng nghĩa, cập nhật bản dịch và `source_commit` trong PR nhỏ.
4. Nếu thay đổi nội dung thuật toán, đánh dấu `status: stale` trước, sau đó dịch lại phần liên quan và review kỹ thuật.
5. Không merge tự động nội dung dịch do AI tạo mà chưa có người đọc lại.
6. PR đồng bộ upstream không được đồng thời chứa batch dịch mới, trừ khi thay đổi nguồn là bắt buộc để giải quyết xung đột của chính batch đó.

## 10. Quy tắc dùng AI

AI có thể:

- đề xuất phạm vi batch;
- tạo bản nháp;
- đối chiếu cấu trúc;
- phát hiện phần chưa đồng bộ;
- đề xuất glossary;
- hỗ trợ review kỹ thuật và ngôn ngữ.

AI không được:

- tự đánh dấu `ready`;
- tự bỏ qua hoặc nới lỏng validator để làm CI xanh;
- tự sửa code nguồn trong PR dịch;
- khẳng định đã review kỹ thuật độc lập nếu chỉ một tác nhân tạo và tự đọc lại bản dịch.

Người review chịu trách nhiệm cuối cùng về:

- tính đúng đắn thuật toán;
- thuật ngữ tiếng Việt;
- code, công thức và link;
- tuân thủ CC BY-SA 4.0;
- việc đánh dấu nội dung là bản dịch cộng đồng, không phải bản chính thức.
