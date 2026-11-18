# Kiểm chứng độc lập findings strings / DP / num

Snapshot `1bc738ed8de2b42d8a5905d56e1ee204728bebbf`. Đối chiếu các vị trí và tự tính phản ví dụ dưới đây; đây không phải review toàn văn lại các bài và chưa tra issue/upstream.

## review-121-125

- Z chia hết: **xác nhận cần sửa**. EN `z-function.md:201` yêu cầu i là ước của n; VI `:208` nói «i chia hết n», vừa thiếu «cho» vừa sai chiều. n=6,i=2 hợp lệ. Sửa «n chia hết cho i» hoặc «i là ước của n».
- Z thay phát biểu nguồn: **xác nhận có sửa cách diễn đạt nguồn nhưng không đồng ý bắt buộc khôi phục câu sai**. EN `:161` viết r không quá n-1; VI `:166` công khai ghi nguồn nói vậy, nêu cận đúng và `:168` đánh dấu ghi chú bản dịch. Với s=`aa`, i=1 thì r=2=n. Do phát biểu sai của EN vẫn được nhận diện rõ và phần đính chính được gắn nhãn, đây là cách trình bày có thể chấp nhận; đoạn 166–168 lặp ý, có thể làm gọn. Quy tắc yêu cầu không âm thầm sửa, không yêu cầu lặp nguyên câu sai trước ghi chú.
- Hash rỗng: **xác nhận** `string-hashing.md:165–166` cấp 0 phần tử rồi truy cập [0] khi n=0. Rabin-Karp `:28–29` tương tự khi S=T=0; S=0,T>0 thì vòng lặp tới i=T và truy cập p_pow[i] ngoài vector kích thước T. Cần xác định miền đầu vào; có sẵn trong EN.
- Suffix tree note giới hạn 26 ký tự và N: phù hợp bảng và chỉ số; chưa thử chạy.

## review-126-127

- Intro DP: MAXN=100 và int ràng buộc chỉ số/giá trị; đây là giới hạn ví dụ nguồn, không khẳng định lỗi dịch.
- LIS-1: **xác nhận sai lệch văn xuôi/code trong nguồn**, EN :224 nói strictly greater còn :234 lower_bound là >=. Với d=[1], x=1, lower_bound ghi đè 1; nếu áp dụng literally strictly greater rồi append thì tạo [1,1] sai độ dài LIS nghiêm ngặt.
- LIS-2: **xác nhận thiếu điều kiện trong nguồn** EN :329–331; cần j<i, a[j]<a[i], chọn độ dài d[j] lớn nhất trong các j hợp lệ và có cơ sở 1 khi không có j. Dãy [2,1] xác nhận không thể dùng j=0. Câu «ending in values d[i]» cũng không đúng với định nghĩa d[i] là độ dài.
- LIS-3: **xác nhận** hai hàm nêu trong báo cáo đọc d[0] khi đầu vào rỗng; nguồn cần n>0 hoặc nhánh riêng.

## review-128-129

- KN-1: **xác nhận** EN :117,159,163 thiếu k<=floor(j/w_i), tương đương k<=x; j=1,w=2,k=1 dùng chỉ số âm. Có thể quy ước trạng thái âm là -infinity, nhưng nguồn phải nói rõ.
- KN-2: **xác nhận cận nguyên văn không đầy đủ**. Ví dụ W=1,w=2: floor(W/w)=0 nhưng x=0 vẫn có các trạng thái; tổng O(nW) có thể giữ bằng cách xét y hợp lệ và W+1 sức chứa. Đếm đúng là floor((W-y)/w)+1 với 0<=y<=min(w-1,W).
- KNUTH-1: **xác nhận phản ví dụ** dp(i,i)=1, C=0 cho dp(i,j)=j-i+1; mọi điểm tách hòa, chọn điểm lớn nhất thỏa đơn điệu. Chứng minh trong nguồn có thể giả sử cơ sở 0 nhưng nói đó là mọi bài dùng tối ưu là quá rộng.
- KNUTH-2: **xác nhận** với S=[0,-1], C(0,0)=0 > C(0,1)=-1, vi phạm điều kiện đơn điệu bao hàm. Các phần tử không âm là điều kiện đủ, không phải điều kiện cần.

## review-146-150

- Binary search: nhận xét **đúng nếu hiểu là chưa từng đọc các chỉ số trở thành L/R về sau**, nhưng cần phân biệt: tại mỗi lần kiểm tra, A[M] được đọc trước khi M trở thành biên; không đọc trực tiếp A[L], A[R] hiện tại. Câu nguồn dễ gây hiểu lầm, không nên khẳng định thuật toán vi phạm chính cách diễn đạt theo thời điểm.
- Simulated annealing: **xác nhận nhãn** VI :76,130 khác nhãn yêu cầu «Ghi chú bản dịch» trong TRANSLATING_VI.md. P nhận rng bằng giá trị nên chính lời gọi P không cập nhật rng gốc; các lần gọi có thể nhận cùng hoặc khác trạng thái tùy việc khác dùng rng, không nên suy ra mọi lần gọi luôn giống nhau. Giả thiết 0<u<1, T>1 cho công thức số vòng là đúng.
- Ternary: **xác nhận** mỗi vòng co đoạn tối đa theo tỷ lệ 2/3, và eps chặn độ rộng/độ sai vị trí trong điều kiện cực trị còn được bao; không tự chặn sai số giá trị f(l). Ví dụ f(x)=M*x trên [0,eps], chênh lệch giá trị hai đầu là M*eps và M tùy ý lớn. Note VI :102 đúng.
- Newton: **xác nhận** f(x)=x² với x khác 0 cho bước tiếp x/2, hội tụ tuyến tính về nghiệm bội 0; cần giả thiết thích hợp như nghiệm đơn và đủ trơn cho hội tụ bậc hai. Với n<0 không có căn bậc hai thực.
- Simpson: **xác nhận giới hạn** công thức sai số dùng đạo hàm bậc bốn cần các giả thiết khả vi và bị chặn tương ứng; không thể áp dụng vô điều kiện. Chưa tự chứng minh lại toàn bộ hệ số sai số trong mục này.
