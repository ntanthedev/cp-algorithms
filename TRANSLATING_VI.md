# Quy trình dịch tiếng Việt

Tài liệu này là nguồn quy tắc chuẩn cho việc tạo, đồng bộ và review bản dịch tiếng Việt của cp-algorithms.

## 0. Cổng bắt đầu một batch dịch mới

Không bắt đầu dịch ngay sau khi chọn tên bài. Mỗi batch phải hoàn tất các bước chuẩn bị sau:

1. Xác nhận nhánh mặc định `master` mới nhất đang build xanh và mặc định tạo branch dịch từ `master`.
   - Ngoại lệ: nếu batch mới phụ thuộc trực tiếp vào glossary, validator hoặc quy tắc đang nằm trong một Draft PR dịch khác **đã xanh toàn bộ CI bắt buộc**, có thể tạo stacked branch từ head của PR đó và mở PR mới nhắm vào branch phụ thuộc. Sau khi PR phụ thuộc merge, phải retarget PR stacked về `master` trước khi merge.
2. Chọn phạm vi có thể review:
   - tối đa ba bài dài hoặc có nhiều công thức/cấu trúc đặc biệt;
   - tối đa năm bài cỡ vừa;
   - từ năm đến mười bài ngắn thuộc cùng nhóm kiến thức.
3. Đọc toàn bộ từng file nguồn và kiểm kê:
   - front matter;
   - cấp và thứ tự heading;
   - code fence, ngôn ngữ code và nội dung code;
   - inline code;
   - công thức LaTeX;
   - Markdown link, image và link tham chiếu;
   - HTML;
   - MkDocs tabs, admonition, attribute list, Jinja hoặc macro.
4. Chốt thuật ngữ mới trước khi viết. Thuật ngữ chưa có trong glossary phải được giải thích trong PR.
5. Lấy **Git blob SHA** của từng file nguồn, không dùng SHA của commit toàn repository:

   ```bash
   git rev-parse HEAD:src/algebra/euclid-algorithm.md
   ```

6. Sao chép file nguồn thành file `.vi.md`, giữ nguyên cấu trúc, rồi mới thêm metadata dịch và dịch phần văn xuôi.
7. Mọi bản dịch mới bắt đầu với `status: draft`.
8. Mở PR ở trạng thái Draft nếu chưa có đủ kết quả CI.

### Preflight cục bộ

```bash
python3 scripts/check_vi_translations.py
python3 scripts/check_vi_staleness.py
MKDOCS_ENABLE_GIT_REVISION_DATE=False \
MKDOCS_ENABLE_GIT_COMMITTERS=False \
mkdocs build --strict
```

Sau khi build, mở ít nhất một trang tiếng Việt và kiểm tra mục lục, code tabs, công thức, link, hình ảnh, chuyển ngôn ngữ và giao diện mobile.

## 1. Cấu trúc file

- Giữ file tiếng Anh làm nguồn chuẩn, ví dụ `src/num_methods/binary_search.md`.
- Tạo bản tiếng Việt bằng hậu tố `.vi.md`, ví dụ `src/num_methods/binary_search.vi.md`.
- Không sửa code, công thức, URL, shortcode, thuộc tính HTML cấu trúc hoặc MkDocs directive chỉ để phù hợp văn phong dịch.
- Không dịch tên hàm, biến, API, identifier trong code hoặc output của chương trình.
- Giữ thứ tự đoạn và phạm vi nội dung để reviewer có thể đối chiếu với nguồn.
- Mỗi commit nên chứa một bài dịch hoặc một thay đổi quy tắc độc lập.

## 2. Metadata bắt buộc

Mỗi file `.vi.md` phải giữ front matter của nguồn và thêm block `translation`:

```yaml
---
tags:
  - Translated
e_maxx_link: binary_search
translation:
  source: num_methods/binary_search.md
  source_commit: <Git blob SHA của file nguồn>
  status: draft
  last_synced: YYYY-MM-DD
---
```

`source_commit` hiện lưu **blob SHA của file nguồn** dù tên trường được giữ để tương thích với hệ thống hiện tại.

Front matter nguồn phải giữ nguyên thứ tự khóa và giá trị, ngoại trừ khoảng trắng cuối dòng; validator chỉ cho phép bổ sung block `translation`. Quy tắc nghiêm ngặt này nhằm tránh làm thay đổi metadata build, tag hoặc liên kết e-maxx ngoài chủ đích.

Các trạng thái hợp lệ:

- `draft`: đang dịch hoặc chưa review;
- `technical-reviewed`: đã kiểm tra thuật toán, code, công thức và độ phức tạp;
- `language-reviewed`: đã kiểm tra tiếng Việt và thuật ngữ;
- `ready`: đã qua cả hai loại review;
- `stale`: nguồn đã thay đổi và cần đồng bộ.

Không đặt `ready` trong cùng lượt tạo bản dịch nếu chưa có review độc lập.

## 3. Nguyên tắc dịch

1. Dịch đúng ý, không dịch từng chữ.
2. Viết cho học sinh THPT đã biết C++ cơ bản, nhưng không đơn giản hóa làm sai nội dung kỹ thuật.
3. Lần đầu xuất hiện thuật ngữ quan trọng, dùng dạng `tiếng Việt (English)` khi hữu ích.
4. Sau lần đầu, dùng thuật ngữ nhất quán trong toàn bài.
5. Giữ nguyên ký hiệu toán học, chỉ số, điều kiện biên và độ phức tạp.
6. Không tự thêm khẳng định kỹ thuật mới. Giải thích bổ sung phải được đánh dấu là `Ghi chú bản dịch`.
7. Không thay đổi code mẫu, kể cả comment trong code block.
8. Giữ nguyên URL, attribution hình ảnh và giấy phép.
9. Tránh văn phong máy dịch, câu quá dài và cách nói mơ hồ.
10. Dùng quan hệ chia hết đúng chiều:
    - `a chia hết cho b`;
    - `b là ước của a`;
    - không viết `b chia hết a`.
11. Không viết `nhỏ hơn hai lần`; dùng `không vượt quá một nửa`, `giảm còn một nửa` hoặc bất đẳng thức.
12. Phân biệt thuật ngữ đồ thị:
    - `walk`: hành trình;
    - `trail`: đường đi không lặp cạnh;
    - `path`: đường đi;
    - `cycle`: chu trình;
    - `connected component`: thành phần liên thông.
13. Có thể dịch nội dung của `alt`, `title`, `aria-label`; không đổi `src`, `href`, `class`, `id`, `style`, `data-*` hoặc tên thuộc tính.
14. Heading được dịch nhưng cấp và thứ tự phải giữ nguyên.
15. Inline code như `` `std::gcd` ``, `` `used[]` `` phải giữ nguyên.
16. Tên bài tập và tên riêng nên giữ theo nguồn; chỉ sửa typo của nguồn khi ghi rõ trong PR hoặc thực hiện ở PR sửa nguồn riêng.

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
| single-source shortest path | đường đi ngắn nhất từ một nguồn |
| relaxation | phép nới lỏng |
| negative cycle | chu trình âm |
| distance matrix | ma trận khoảng cách |
| walk | hành trình |
| cycle | chu trình |
| directed acyclic graph | đồ thị có hướng không chu trình |
| topological ordering | thứ tự tô-pô |
| bipartite graph | đồ thị hai phía |
| spanning tree | cây khung |
| dynamic programming | quy hoạch động |

Thay đổi thuật ngữ chung phải được giải thích rõ trong PR.

## 5. Những phần phải giữ nguyên cấu trúc

Validator so sánh giữa nguồn và bản dịch:

- front matter nguồn ngoài block `translation`;
- chuỗi cấp heading;
- code fence, ngôn ngữ và nội dung code block;
- inline code ngoài fenced code block;
- đích Markdown link và image;
- số lượng delimiter công thức khối `$$`;
- Jinja/MkDocs expression;
- cấu trúc HTML và thuộc tính không thể dịch;
- số lượng, thứ tự và mức thụt lề của MkDocs tabs;
- marker admonition.

Nếu cần thay đổi cấu trúc, phải giải thích và cập nhật validator có chủ đích; không xóa kiểm tra chỉ để CI xanh.

## 6. Trách nhiệm của các workflow CI

### `Vietnamese translations`

Chạy validator cấu trúc bằng `scripts/check_vi_translations.py`. Workflow này phải nhẹ và không build MkDocs lần thứ hai.

### `Vietnamese translation sync`

Kiểm tra `source_commit` còn khớp blob SHA hiện tại của file nguồn.

### `Build`

Chạy `mkdocs build --strict`, kiểm tra toàn bộ website song ngữ và tạo preview artifact.

### `Test`

Biên dịch và chạy code-test của các bài nguồn tiếng Anh. Workflow này chỉ cần chạy khi thay đổi:

- file tiếng Anh trong `src/`;
- thư mục `test/`;
- chính `.github/workflows/test.yml`.

PR chỉ thay `.vi.md`, glossary, validator hoặc quy tắc dịch không cần chạy `Test`, vì validator đã yêu cầu code block trong bản dịch giống hệt nguồn. Với PR dịch thuần túy, ba cổng bắt buộc là `Vietnamese translations`, `Vietnamese translation sync` và `Build`.

Lỗi `Service Unavailable` hoặc `Failed to resolve action download info` tại `Set up job` là lỗi hạ tầng GitHub; không sửa code để đối phó với lỗi này.

## 7. Checklist cho người dịch

- [ ] Branch được tạo từ `master` mới nhất, hoặc là stacked branch hợp lệ theo ngoại lệ ở mục 0.
- [ ] Phạm vi batch đúng giới hạn.
- [ ] Đã đọc toàn bộ nguồn và kiểm kê cấu trúc.
- [ ] Đã chốt thuật ngữ mới.
- [ ] `source`, blob SHA, `last_synced` và `status` chính xác.
- [ ] Front matter nguồn được giữ nguyên.
- [ ] Code, comment trong code, công thức và inline code còn nguyên.
- [ ] Link, hình ảnh và attribution còn nguyên.
- [ ] Không bỏ sót đoạn, caption, note, alt text hoặc nội dung tab.
- [ ] Chạy validator, staleness check và strict build.
- [ ] Kiểm tra trang đã render.
- [ ] Mỗi bài nằm trong commit riêng khi có thể.
- [ ] PR ở trạng thái Draft cho đến khi review xong.

## 8. Checklist review kỹ thuật

- [ ] Đối chiếu định nghĩa, invariant và điều kiện biên với nguồn.
- [ ] Kiểm tra chiều quan hệ chia hết và bất đẳng thức.
- [ ] Kiểm tra ví dụ, chỉ số, công thức và độ phức tạp.
- [ ] Phân biệt đúng `walk`, `trail`, `path`, `cycle` nếu xuất hiện.
- [ ] Các workflow bắt buộc đã xanh.
- [ ] Không có code, inline code hoặc link bị đổi ngoài chủ đích.

Chỉ đặt `technical-reviewed` sau khi đạt checklist này.

## 9. Checklist review ngôn ngữ

- [ ] Câu tiếng Việt tự nhiên và phù hợp học sinh.
- [ ] Không bám máy móc theo trật tự câu tiếng Anh.
- [ ] Thuật ngữ nhất quán.
- [ ] Không có cách nói so sánh hoặc chia hết mơ hồ.
- [ ] Không bỏ sót đoạn, caption, note, alt text hoặc nhãn tab.
- [ ] Không thêm ý mới như thể thuộc nội dung nguồn.

Chỉ đặt `language-reviewed` sau khi đạt checklist này. Maintainer đổi sang `ready` sau khi cả hai review hoàn tất.

## 10. Đồng bộ upstream

1. Đồng bộ fork với `cp-algorithms/cp-algorithms` định kỳ.
2. Khi nguồn tiếng Anh đổi, so sánh blob SHA mới với `source_commit`.
3. Thay đổi format/typo không ảnh hưởng nghĩa có thể đồng bộ trong PR nhỏ.
4. Thay đổi nội dung thuật toán phải chuyển bản dịch sang `stale`, cập nhật nội dung và review kỹ thuật lại.
5. Không merge tự động nội dung dịch do AI tạo mà chưa có người đọc lại.
6. Không trộn PR đồng bộ upstream với batch dịch mới nếu không cần thiết để giải quyết xung đột.

## 11. Quy tắc dùng AI

AI có thể đề xuất batch, tạo bản nháp, kiểm tra cấu trúc, phát hiện stale, đề xuất glossary và hỗ trợ review.

AI không được:

- tự đánh dấu `ready`;
- nới lỏng validator chỉ để CI xanh;
- tự sửa code nguồn trong PR dịch;
- tự nhận là reviewer độc lập của chính bản dịch do nó tạo;
- tự merge PR nếu chưa được người duy trì phê duyệt.

Người review chịu trách nhiệm cuối cùng về tính đúng đắn thuật toán, thuật ngữ, code, công thức, link, CC BY-SA 4.0 và việc ghi rõ đây là bản dịch cộng đồng.
