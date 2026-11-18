# Kiểm chứng chéo review tổ hợp — snapshot 1bc738ed8de2b42d8a5905d56e1ee204728bebbf

Đối chiếu trực tiếp EN/VI các đoạn được nêu và thử lại các phản ví dụ; đây là kiểm chứng phát hiện, không phải review toàn văn hay render.

## review-133-134

- inclusion/exclusion, mẫu `a`/`b`: **xác nhận**. EN 245 / VI 250 thiếu trường hợp các ký tự cố định xung đột; không có xâu khớp cả hai, nên f(Y)=0.
- Bộ ba harmonic: **xác nhận nhưng cần ghi chính xác miền đếm**. Với n=6, bộ {2,3,6}, ở i=6 không có số nào trong {2,..,6} nguyên tố cùng nhau với 6 nên tích bằng 0 dù bộ chứa 6. Tích đếm cặp j,k phân biệt khác i với gcd(i,j)=1 và gcd(i,k)>1; tự i không thể là j vì i≥2. Mỗi bộ không harmonic có đúng hai đỉnh như vậy, nên tổng chia 2 đúng.
- Hoán vị điểm cố định: **xác nhận** ví dụ n=3 và cố định vị trí 1 có hai hoán vị, chỉ một có đúng một điểm cố định. EN 421 / VI 426 cần hiểu là x vị trí xác định được cố định, không phải đúng x điểm. Công thức giao và tổng vẫn đúng.
- Dãy độ dài n=0: **xác nhận nếu cho phép n=0**. Dãy rỗng thuộc cả ba tập A_i và không thỏa mỗi số xuất hiện; công thức nguồn ra 1. Nếu n được ngầm định dương thì chỉ là thiếu giả thiết. Nhóm A_k phải là nhóm k; nguồn và bản dịch đều nói nhóm đầu.
- Đường đi: **đồng ý chỉ là thiếu rõ ràng**, không đủ để khẳng định sai: x,y là số bước, hoặc số ô mới đi qua, thì công thức đúng. O(k²) phụ thuộc chi phí tính tổ hợp/số học; n,m rất lớn cần nêu mô hình và tiền xử lý/modulo.
- BC-1: **xác nhận lỗi dịch** EN 179 / VI 184. Với x=5,p=2,c=3 thì 8 | 120 nhưng 8 không chia hết cho 120. Sửa thành “x! chia hết cho p^c” hoặc “p^c là ước của x!”.
- Pascal EN 105 / VI 110: **xác nhận** n=5,k=5; bảng chứa C(5,2)=10 > 1, trong khi code tính toàn bảng. Tuy nhiên phát biểu vẫn đúng cho một số cách tính hạn chế tập phụ thuộc; lỗi gắn với cách viết tổng quát/code nguồn.
- Modulo p^b: **xác nhận cảnh báo có điều kiện**, không khẳng định phương pháp nghịch đảo sai. Ví dụ 4^7 mod 9=4 còn inverse(4)=7; nguyên nhân là áp dụng mù số mũ Fermat m−2 cho hợp số. Tính nghịch đảo bằng Euclid mở rộng là hợp lệ; phần trước cũng nêu thuật toán nghịch đảo khác, do đó xem đây là chỗ cần làm rõ chứ không khẳng định mọi cách dùng phương pháp trước đều sai.

## review-135-136

- BS-1: **xác nhận có thay đổi ý nguồn và chưa có note**. EN 76 nói không vi phạm điều kiện “có nhiều ngoặc đóng hơn ngoặc mở”; VI 81 nói hậu tố có thể hoàn thành, tránh điều kiện ngược đó. Dãy tiền tố `)` không thể hoàn thành. Đây là một sửa ý nguồn có cơ sở nhưng cần ghi note theo quy tắc; không nên khôi phục câu sai như một lời khuyên đơn lẻ.
- Note thứ hạng/tràn VI 168: **xác nhận** code dùng ≥ k, k 1-based; n=0,k=1 trả xâu rỗng; int và shift có thể tràn. Không suy ra an toàn với k không hợp lệ.
- Nhiều loại ngoặc: **xác nhận thiếu điều kiện** ở EN 151 / VI 156: thử dấu đóng phải khớp ngoặc trên đỉnh stack; prefix `[` rồi `)` là sai dù độ sâu số học trở lại 0. Đây là thiếu sót nguồn.
- Song ánh DP bán cân bằng: **xác nhận**, đảo thứ tự hậu tố và đổi mở/đóng cho song ánh với d[L][depth]; yêu cầu bổ sung là giải thích tùy chọn, không phải lỗi công thức.
- Burnside note VI 275: **xác nhận** lcm(0,n)/0 không xác định; identity có n chu trình. Trong code p1 chu kỳ n, p2 chu kỳ m nên số mũ văn xuôi EN 213 / VI 218 đảo so với code; identity 4×8 có 32 chu trình, `1 << 32` không hợp lệ khi int 32 bit.
- Burnside đóng của nhóm: **hạ mức nhận định**. Trong ngữ cảnh đây là tập không rỗng hữu hạn gồm các hoán vị, tính đóng đã kéo theo đơn vị và nghịch đảo (lũy thừa của mỗi hoán vị hữu hạn), do đó EN 64 / VI 69 không sai về lập luận nếu sử dụng định lý này. Có thể thêm một câu chứng minh, không nên xếp thành lỗi thiếu giả thiết.
- Đối xứng hình xuyến: **giữ nghi vấn, chưa xác nhận lỗi**. Những phép nêu đúng là một nhóm sinh theo mô hình đang dùng, nhưng nguồn không định nghĩa đủ chặt đối tượng và phép xoay cho phép; không thể kết luận có hay thiếu phép chỉ từ mô tả.

Không tra lịch sử issue hoặc nguồn upstream cho các phát hiện; chưa kết luận tính mới.
