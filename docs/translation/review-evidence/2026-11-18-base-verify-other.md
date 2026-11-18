# Kiểm chứng độc lập nhận định 151–158 và hai ghi chú tổ hợp

Snapshot 1bc738ed8de2b42d8a5905d56e1ee204728bebbf; phạm vi là các nhận định được trích trong các báo cáo, không phải review lại toàn văn. Không tra issue upstream.

## 151–155

- k-th: Với [1,1], k=2 ngưỡng là 1 nhưng không có phần tử nhỏ hơn 1. Xác nhận note; để lấy hai phần tử cần lấy cả các phần tử bằng ngưỡng. Mã đánh chỉ số từ 1 như báo cáo.
- mex: Nếu đầu vào [-1], kiểm tra x <= MAX_N không loại -1 nên used[-1] ngoài phạm vi. Với lớp cập nhật, A=[-1] khởi tạo missing={0,1}; update(0,0) chèn -1 và xóa 0, trả -1 thay vì mex 1. Xác nhận hai note; N<=MAX_N là điều kiện đủ, không khẳng định cần thiết.
- rmq: Fenwick min [1,2], chỉ update bằng phép min, sau khi tăng phần tử đầu thành 3 vẫn giữ 1 thay vì min mới 2. DSU nén đường đi không cho cận O(1) xấu nhất riêng từng truy vấn: một chuỗi cha dài có thể khiến find đầu tiên đi nhiều cạnh. Xác nhận.
- games_on_graphs: đồ thị n đỉnh cô lập cần xử lý n kết quả nên O(m) không đủ khi m=0. Mảng 100x100 mà mã mã hóa ô thành n*i+j thì 11x10 đạt chỉ số 109 vượt 99. Với luật misère, đỉnh kết thúc được khởi tạo thắng cần giữ nguyên; điều kiện “mọi nước dẫn tới thắng” không được áp vào đỉnh chưa có nước một cách máy móc. Xác nhận báo cáo; giả thiết và luật cụ thể cần nêu.
- sprague-grundy-nim: Với [1,1] đã bắt đầu pha chỉ đống 0/1, xác nhận note. Với dải 0 hoặc 1 ô, g(0)=0, g(1)=1, công thức có g(n-2) chỉ dùng từ n>=2. Phản biện mạnh hơn nghi vấn báo cáo về bổ đề tăng: nếu cho thêm trạng thái một token (chưa dùng/đã dùng), từ (0,chưa dùng) được tăng lên (1,đã dùng), sau đó giảm về (0,đã dùng) kết thúc; đồ thị hữu hạn không chu trình nhưng (0,chưa dùng) là thắng còn Nim đống 0 thông thường là thua. Do đó với mô hình trạng thái phụ và quy tắc tăng tùy ý như chữ nguồn, kết luận không đúng nói chung; nước giảm không trở lại trạng thái đầy đủ ban đầu. Nếu mô hình không có trạng thái phụ, tăng rồi giảm về cùng cấu hình tạo chu trình. Lưu ý đây là phản ví dụ cho phát biểu tổng quát, không tự suy luận về các biến thể cụ thể trong bài.

## 156–158

- schedule-with-completion-duration: sắp các việc đã chọn theo deadline có lịch không ngắt nếu mọi tổng thời lượng tiền tố theo thứ tự deadline không vượt deadline tương ứng. Chứng cứ vét cạn 65.536 bộ trong báo cáo cũ hỗ trợ note, nhưng không tự chứng minh tổng quát rằng mã luôn chọn tập có tính chất đó. Đồng ý giới hạn này; câu “trong thời gian T” ở VI:20 nên hiểu là phần T còn lại sau khi đã xử lý việc khác.
- schedule_one_machine: t_i=0 làm c_i/t_i không xác định; c_i=0 làm (1-e^(alpha*t_i))/c_i không xác định. Ký hiệu trong note VI:85 khác biểu thức trước đó đúng như báo cáo; chưa chứng minh định lý phân loại tổng quát.
- schedule_two_machines: note VI:53 thay K_i bằng K_k và dùng chỉ số k nhất quán là đúng theo công thức x_k. Với max của phần không đổi C và cặp u,v: max(u,v)<=max(u',v') kéo theo max(C,u,v)<=max(C,u',v'); chiều đảo sai khi C=10, cặp cũ (3,2), cặp mới (2,1), tổng đều 10. Note VI:69 đúng cho kết luận không giảm, không phải điều kiện cần. Với kết luận tăng nghiêm ngặt thì điều kiện nêu trong câu nguồn là cần, nên cần phân biệt chặt/chưa chặt; không gọi riêng câu đó hoàn toàn sai.

## bishops-on-chessboard và generating_combinations

- bishops K=0: vector mỗi hàng có K+1=1 phần tử, truy cập D[1][1] vượt cột; nghiệm tổ hợp đúng là một cách chọn rỗng. Xác nhận.
- generating_combinations: tự sinh dãy binary-reflected Gray i xor (i>>1) và lọc trọng số k cho mọi 3<=N<=10, 2<=K<N; cặp cuối nửa đầu / đầu nửa sau luôn lần lượt bằng 01 0^(N-K-1)1^(K-1) và 11 0^(N-K)1^(K-2). Đây là kiểm hữu hạn, không thay thế chứng minh tổng quát. K=0 hoặc N có duy nhất một mask; K=1 có một bit 1 ở mỗi mask nêu trong note.
