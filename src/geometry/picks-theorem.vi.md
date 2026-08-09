---
tags:
  - Translated
e_maxx_link: pick_grid_theorem
translation:
  source: geometry/picks-theorem.md
  source_commit: 79a985b71c0fa41eb6ff55453460c0d4910c27ee
  status: draft
  last_synced: 2026-08-09
---

# Định lý Pick

Một đa giác không tự cắt được gọi là đa giác lưới nếu tất cả các đỉnh của nó có tọa độ nguyên trên một lưới hai chiều nào đó. Định lý Pick cho phép tính diện tích của đa giác này thông qua số đỉnh nằm trên biên và số đỉnh nằm hoàn toàn bên trong đa giác.

**Ghi chú bản dịch:** Ở câu trên, nguồn dùng từ “vertices”. Tuy nhiên, Định lý Pick thực tế sử dụng số **điểm nguyên** nằm trên biên và nằm hoàn toàn bên trong đa giác. Phần Công thức bên dưới đã ghi rõ $I$ đếm các điểm có tọa độ nguyên, nhưng câu định nghĩa $B$ của nguồn vẫn thiếu điều kiện này. Các cách diễn đạt này đang được đề xuất sửa riêng ở bản tiếng Anh.

## Công thức

Cho một đa giác lưới có diện tích khác không.

Ký hiệu diện tích của nó là $S$, số điểm có tọa độ nguyên nằm hoàn toàn bên trong đa giác là $I$ và số điểm nằm trên các cạnh của đa giác là $B$.

**Ghi chú bản dịch:** Trong công thức Pick, $B$ phải được hiểu là số **điểm nguyên** nằm trên biên đa giác; câu nguồn hiện chỉ viết “points lying on polygon sides”.

Khi đó, **công thức Pick** phát biểu:

$$S=I+\frac{B}{2}-1$$

Đặc biệt, nếu đã biết các giá trị $I$ và $B$ của một đa giác, ta có thể tính diện tích trong $O(1)$ mà thậm chí không cần biết các đỉnh.

Công thức này được nhà toán học người Áo Georg Alexander Pick phát hiện và chứng minh vào năm 1899.

## Chứng minh

Chứng minh được thực hiện qua nhiều bước, từ các đa giác đơn giản đến trường hợp tổng quát:

- Một hình vuông: $S=1, I=0, B=4$, thỏa mãn công thức.

- Một hình chữ nhật không suy biến bất kỳ có các cạnh song song với các trục tọa độ: Giả sử $a$ và $b$ là độ dài hai cạnh của hình chữ nhật. Khi đó, $S=ab, I=(a-1)(b-1), B=2(a+b)$. Thay vào, ta thấy công thức đúng.

- Một góc vuông có các cạnh song song với các trục: Để chứng minh điều này, lưu ý rằng một tam giác như vậy có thể thu được bằng cách cắt một hình chữ nhật theo đường chéo. Ký hiệu số điểm nguyên nằm trên đường chéo là $c$, có thể chứng minh rằng công thức Pick đúng cho tam giác này bất kể $c$ bằng bao nhiêu.

- Một tam giác bất kỳ: Lưu ý rằng có thể biến một tam giác như vậy thành hình chữ nhật bằng cách ghép thêm các tam giác vuông có hai cạnh góc vuông song song với các trục (không cần quá 3 tam giác như vậy). Từ đây, ta suy ra công thức đúng cho mọi tam giác.

- Một đa giác bất kỳ: Để chứng minh, hãy tam giác hóa nó, tức chia thành các tam giác có các đỉnh tọa độ nguyên. Hơn nữa, có thể chứng minh rằng Định lý Pick vẫn đúng khi ghép thêm một tam giác vào đa giác. Như vậy, ta đã chứng minh công thức Pick cho đa giác bất kỳ.

**Ghi chú bản dịch:** Ở bullet đầu, các giá trị $S=1, I=0, B=4$ tương ứng với một hình vuông đơn vị, trong khi nguồn chỉ viết “A single square”. Ở bullet thứ ba, nguồn viết “A right angle with legs parallel to the axes”, nhưng lập luận ngay sau đó nói về một tam giác được tạo bằng cách cắt hình chữ nhật theo đường chéo; đối tượng cần xét là một **tam giác vuông**, không phải một góc vuông. Hai cách diễn đạt này đang được đề xuất làm rõ riêng ở bản tiếng Anh.

## Khái quát lên số chiều cao hơn

Đáng tiếc, công thức đơn giản và đẹp này không thể được khái quát trực tiếp lên số chiều cao hơn.

John Reeve đã chỉ ra điều này vào năm 1957 bằng một tứ diện (**tứ diện Reeve**) có các đỉnh:

$$A=(0,0,0),
B=(1,0,0),
C=(0,1,0),
D=(1,1,k),$$

trong đó $k$ có thể là một số tự nhiên bất kỳ. Khi đó, với mọi $k$, tứ diện $ABCD$ không chứa điểm nguyên nào bên trong và chỉ có $4$ điểm trên biên là $A, B, C, D$. Vì vậy, thể tích và diện tích bề mặt có thể thay đổi dù số điểm bên trong và trên biên không đổi. Do đó, Định lý Pick không cho phép kiểu khái quát trực tiếp này.

Tuy nhiên, trong số chiều cao hơn vẫn có một dạng khái quát sử dụng **đa thức Ehrhart**, nhưng chúng khá phức tạp và không chỉ phụ thuộc vào các điểm bên trong mà còn phụ thuộc vào biên của đa diện.

## Tài liệu bổ sung
Có thể xem một vài ví dụ đơn giản và một chứng minh ngắn của Định lý Pick [tại đây](http://www.geometer.org/mathcircles/pick.pdf).
