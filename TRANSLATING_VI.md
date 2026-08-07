# Quy trình dịch tiếng Việt

Tài liệu này là nguồn quy tắc chuẩn cho việc tạo, đồng bộ và review bản dịch tiếng Việt của cp-algorithms.

## 0. Cổng bắt đầu một batch dịch mới

Không bắt đầu dịch ngay sau khi chọn tên bài. Mỗi batch phải hoàn tất các bước chuẩn bị sau:

1. Xác nhận nhánh mặc định `master` mới nhất đang build xanh.
   - Chỉ duy trì một nhánh làm việc lâu dài cho bản dịch: `agent/vi-work`, và tối đa một PR dịch đang mở tại một thời điểm.
   - Nếu đang có một PR dịch cũ dùng tên branch khác, hoàn tất PR đó trước; không mở batch mới và không reset branch đang chứa thay đổi chưa merge.
   - Sau khi PR đã merge, chỉ reset/di chuyển `agent/vi-work` về `master` mới nhất khi đã xác nhận branch không còn commit riêng chưa merge.
   - Không force-push hoặc reset `master`.
   - Stacked PR chỉ dùng trong trường hợp phụ thuộc kỹ thuật thực sự không thể tránh; phải giải thích lý do trước và vẫn không được để nhiều batch dịch độc lập cùng mở nếu không cần thiết.
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
9. Trước khi bắt đầu batch tiếp theo, kiểm tra tất cả PR dịch đang mở:
   - nếu còn một PR dịch chưa merge, **không bắt đầu batch mới**;
   - xử lý và resolve mọi review thread/comment có hành động cụ thể trước khi tiếp tục;
   - kiểm tra cả inline review threads, review submissions và PR conversation comments;
   - reviewer tự động như GitHub Copilot có thể gửi comment trễ, nên trạng thái sạch phải được xác nhận lại sau commit cuối cùng và sau CI.
10. Sau commit cuối cùng của batch và trước khi báo công việc hoàn tất, **kiểm tra lại** tất cả PR dịch đang mở và review mới nhất. Mọi comment có hành động cụ thể xuất hiện trong lúc làm batch phải được xử lý hoặc ghi rõ blocker trước khi bàn giao.

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
| amortized complexity | độ phức tạp khấu hao |
| associativity | tính kết hợp |
| greatest common divisor | ước chung lớn nhất |
| least common multiple | bội chung nhỏ nhất |
| extended Euclidean algorithm | thuật toán Euclid mở rộng |
| Bézout's identity / lemma | đồng nhất thức / bổ đề Bézout |
| coprime / relatively prime | nguyên tố cùng nhau |
| pairwise coprime | đôi một nguyên tố cùng nhau |
| congruence | đồng dư |
| modulus | mô-đun |
| modular multiplicative inverse | nghịch đảo nhân mô-đun; sau lần đầu có thể dùng nghịch đảo mô-đun |
| linear Diophantine equation | phương trình Diophantine tuyến tính |
| binary exponentiation | lũy thừa nhị phân |
| Euler's totient function | phi hàm Euler; còn gọi hàm phi Euler |
| Euclidean division | phép chia Euclid |
| Chinese Remainder Theorem | Định lý Thặng dư Trung Hoa (CRT); cũng gặp Định lý số dư Trung Hoa |
| multiplicative order | bậc nhân |
| primitive root | căn nguyên thủy |
| mixed radix representation | biểu diễn cơ số hỗn hợp |
| Sieve of Eratosthenes | Sàng Eratosthenes |
| segmented sieve | sàng phân đoạn |
| connected component | thành phần liên thông |
| shortest path | đường đi ngắn nhất |
| single-source shortest path | đường đi ngắn nhất từ một nguồn |
| relaxation | phép nới lỏng |
| predecessor | đỉnh trước |
| negative weight edge | cạnh có trọng số âm |
| negative cycle | chu trình âm |
| distance matrix | ma trận khoảng cách |
| dense graph | đồ thị dày |
| sparse graph | đồ thị thưa |
| priority queue | hàng đợi ưu tiên |
| Fibonacci heap | heap Fibonacci |
| walk | hành trình |
| cycle | chu trình |
| directed acyclic graph | đồ thị có hướng không chu trình |
| topological ordering | thứ tự tô-pô |
| bipartite graph | đồ thị hai phía |
| spanning tree | cây khung |
| minimum spanning tree | cây khung nhỏ nhất |
| maximum spanning tree | cây khung lớn nhất |
| Disjoint Set Union | hợp các tập rời nhau |
| representative / leader | phần tử đại diện |
| path compression | nén đường đi |
| union by size | hợp theo kích thước |
| union by rank | hợp theo hạng |
| inverse Ackermann function | hàm Ackermann nghịch đảo |
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
- với mỗi file `.vi.md` được thêm hoặc sửa trong PR/commit hiện tại, từng biểu thức LaTeX phải giữ nguyên nội dung và số lần xuất hiện so với nguồn; validator so sánh theo multiset nên cho phép đổi thứ tự các biểu thức khi cấu trúc câu tiếng Việt yêu cầu; nội dung được đánh dấu `Ghi chú bản dịch` không được coi là công thức của nguồn;
- Jinja/MkDocs expression;
- cấu trúc HTML và thuộc tính không thể dịch;
- số lượng, thứ tự và mức thụt lề của MkDocs tabs;
- marker admonition.

Nếu cần thay đổi cấu trúc, phải giải thích và cập nhật validator có chủ đích; không xóa kiểm tra chỉ để CI xanh.

## 6. Trách nhiệm của các workflow CI

### `Vietnamese translations`

Chạy validator cấu trúc bằng `scripts/check_vi_translations.py`. Workflow này phải nhẹ và không build MkDocs lần thứ hai. Trong pull request, checkout đủ lịch sử tối thiểu để validator xác định chính xác các file `.vi.md` đã thay đổi và áp kiểm tra LaTeX nghiêm ngặt cho chúng mà không biến nợ định dạng của bản dịch legacy chưa chạm tới thành blocker của PR mới.

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

- [ ] Dùng `agent/vi-work` làm branch dịch lâu dài; nếu đang hoàn tất một PR legacy dùng branch khác thì không mở batch mới cho tới khi PR đó merge.
- [ ] Tối đa một PR dịch đang mở.
- [ ] Tất cả review thread/comment có hành động cụ thể trên PR dịch đang mở đã được xử lý hoặc có lý do rõ ràng để chưa xử lý.
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
- [ ] Đã kiểm tra lại review thread/comment sau commit cuối cùng của batch và xử lý mọi comment mới có hành động cụ thể.
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
