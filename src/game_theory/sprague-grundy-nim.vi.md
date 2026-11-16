---
tags:
  - Translated
e_maxx_link: sprague_grundy
translation:
  source: game_theory/sprague-grundy-nim.md
  source_commit: a6a172d87803667a4e5edfc1d8a021fae95c5ede
  status: draft
  last_synced: 2026-11-16
---

# Định lý Sprague-Grundy. Trò chơi Nim

## Giới thiệu

Định lý này mô tả các trò chơi hai người **vô tư** (impartial), tức là những trò chơi mà các nước đi có thể thực hiện và việc thắng hay thua chỉ phụ thuộc vào trạng thái trò chơi. Nói cách khác, khác biệt duy nhất giữa hai người chơi là một người đi trước.

Ngoài ra, ta giả sử trò chơi có **thông tin hoàn hảo**, tức là không có thông tin nào bị giấu khỏi người chơi (họ biết luật và các nước đi có thể thực hiện).

Ta giả sử trò chơi là **hữu hạn**: sau một số nước đi, một người sẽ rơi vào trạng thái thua, từ đó không thể đi sang trạng thái khác. Ngược lại, người đưa đối thủ vào trạng thái đó sẽ thắng. Do đó trò chơi không có kết quả hòa.

Ta có thể mô tả đầy đủ những trò chơi này bằng một *đồ thị có hướng không chu trình*: các đỉnh là trạng thái trò chơi và các cạnh là những phép chuyển (nước đi). Đỉnh không có cạnh đi ra là đỉnh thua (người phải đi từ đỉnh này sẽ thua).

Vì không có hòa, ta có thể phân loại mọi trạng thái thành **thắng** hoặc **thua**. Trạng thái thắng là trạng thái có một nước đi khiến đối thủ chắc chắn thua, kể cả khi họ đáp trả tốt nhất. Trạng thái thua là trạng thái mà mọi nước đi đều dẫn đến trạng thái thắng cho đối thủ. Tóm lại, một trạng thái là thắng nếu có ít nhất một phép chuyển tới trạng thái thua và là thua nếu không có phép chuyển nào như vậy.

Nhiệm vụ của ta là phân loại các trạng thái của một trò chơi cho trước.

Lý thuyết về các trò chơi này được Roland Sprague phát triển độc lập năm 1935 và Patrick Michael Grundy năm 1939.

## Nim

Trò chơi này tuân theo các giới hạn đã mô tả ở trên. Hơn nữa, *bất kỳ* trò chơi hai người vô tư có thông tin hoàn hảo nào cũng có thể quy về Nim. Nghiên cứu trò chơi này cho phép ta giải các trò chơi tương tự khác; ta sẽ trở lại điều này sau.

Trò chơi này đã phổ biến từ thời cổ đại. Nguồn gốc của nó có lẽ là ở Trung Quốc — hoặc ít nhất trò *Jianshizi* rất giống nó. Tại châu Âu, những tài liệu nhắc đến trò chơi sớm nhất có từ thế kỷ 16. Charles Bouton đặt tên cho trò chơi và công bố phân tích đầy đủ về nó vào năm 1901.

### Mô tả trò chơi

Có một số đống, mỗi đống chứa một số viên sỏi. Trong một lượt, người chơi có thể lấy một số dương bất kỳ viên sỏi từ đúng một đống rồi bỏ chúng đi. Người chơi thua nếu không thể đi, tức là khi tất cả các đống đều rỗng.

Trạng thái trò chơi được xác định duy nhất bởi một đa tập các số nguyên dương. Một nước đi gồm việc giảm thực sự một số nguyên được chọn (nếu nó trở thành không thì loại khỏi tập).

### Lời giải

Lời giải của Charles L. Bouton như sau:

**Định lý.** Người chơi hiện tại có chiến lược thắng khi và chỉ khi tổng xor của kích thước các đống khác không. Tổng xor của dãy $a$ là $a_1 \oplus a_2 \oplus \ldots \oplus  a_n$, trong đó $\oplus$ là phép *hoặc loại trừ theo bit*.

**Chứng minh.** Mấu chốt của chứng minh là sự tồn tại của một **chiến lược đối xứng cho đối thủ**. Ta chỉ ra rằng một khi ở trạng thái có tổng xor bằng không, người chơi không thể giữ tổng xor khác không về lâu dài: nếu họ chuyển sang trạng thái có tổng xor khác không, đối thủ luôn có một nước đi đưa tổng xor trở lại không.

Ta chứng minh định lý bằng quy nạp toán học.

Với Nim rỗng (mọi đống đều rỗng, tức đa tập rỗng), tổng xor bằng không và định lý đúng.

Bây giờ giả sử trạng thái hiện tại không rỗng. Theo giả thiết quy nạp (và vì trò chơi không có chu trình), ta giả sử định lý đã được chứng minh cho mọi trạng thái có thể đạt tới từ trạng thái hiện tại.

Chứng minh chia thành hai phần: nếu tổng xor ở vị trí hiện tại là $s = 0$, ta phải chứng minh đây là trạng thái thua, tức mọi trạng thái đạt được đều có tổng xor $t \neq 0$. Nếu $s \neq 0$, ta phải chứng minh có một nước đi dẫn đến trạng thái có $t = 0$.

*   Giả sử $s = 0$ và xét một nước đi bất kỳ. Nước đi này giảm kích thước một đống từ $x$ xuống $y$. Dùng các tính chất cơ bản của $\oplus$, ta có

    \[ t = s \oplus x \oplus y = 0 \oplus x \oplus y = x \oplus y \]

    Vì $y < x$, $y \oplus x$ không thể bằng không, nên $t \neq 0$. Như vậy mọi trạng thái đạt được đều thắng (theo giả thiết quy nạp), nên trạng thái hiện tại là thua.

*   Giả sử $s \neq 0$. Xét biểu diễn nhị phân của số $s$. Gọi $d$ là chỉ số của bit khác không cao nhất (có giá trị lớn nhất). Ta đi trên một đống có bit thứ $d$ trong kích thước được bật (đống đó phải tồn tại, nếu không bit này sẽ không được bật trong $s$). Ta giảm kích thước của nó từ $x$ xuống $y = x \oplus s$. Mọi bit ở vị trí lớn hơn $d$ trong $x$ và $y$ giống nhau, còn bit $d$ được bật trong $x$ nhưng không được bật trong $y$. Do đó $y < x$, đủ để nước đi hợp lệ. Khi đó:

    \[ t = s \oplus x \oplus y = s \oplus x \oplus (s \oplus x) = 0 \]

    Như vậy ta đã tìm được một trạng thái thua có thể đạt tới (theo giả thiết quy nạp), và trạng thái hiện tại là thắng.

**Hệ quả.** Có thể thay một trạng thái Nim bằng trạng thái tương đương miễn là tổng xor không thay đổi. Hơn nữa, khi phân tích Nim với nhiều đống, ta có thể thay chúng bằng một đống duy nhất có kích thước $s$.

### Trò chơi Misère

Trong một **trò chơi misère**, mục tiêu bị đảo ngược: người lấy que cuối cùng sẽ thua. Hóa ra ta có thể chơi misère Nim tối ưu gần giống Nim thông thường. Ý tưởng là trước tiên chơi misère như trò chơi chuẩn, nhưng đổi chiến lược vào cuối trò chơi. Chiến lược mới được áp dụng khi sau nước đi tiếp theo mỗi đống sẽ chứa nhiều nhất một que.

Trong trò chơi chuẩn, ta nên chọn nước đi để sau đó có số chẵn đống chứa một que. Tuy nhiên, trong misère ta chọn nước đi để số đống chứa một que là lẻ. Chiến lược này hiệu quả vì trạng thái cần đổi chiến lược luôn xuất hiện và là trạng thái thắng: nó chứa đúng một đống có nhiều hơn một que, nên tổng Nim khác 0.

## Sự tương đương giữa trò chơi vô tư và Nim (định lý Sprague-Grundy)

Bây giờ ta sẽ tìm hiểu cách tìm, với mỗi trạng thái của một trò chơi vô tư bất kỳ, một trạng thái Nim tương ứng.

### Bổ đề về Nim cho phép tăng

Xét biến thể sau của Nim: ta còn cho phép **thêm sỏi vào một đống được chọn**. Ta **không quan tâm** đến quy tắc chính xác về cách thức và thời điểm được phép tăng, tuy nhiên quy tắc phải giữ cho trò chơi **không có chu trình**. Các phần sau xét một số trò chơi ví dụ.

**Bổ đề.** Việc thêm nước đi tăng vào Nim không làm thay đổi cách xác định các trạng thái thắng và thua. Nói cách khác, các nước tăng là vô ích và ta không cần dùng chúng trong một chiến lược thắng.

**Chứng minh.** Giả sử một người chơi thêm sỏi vào một đống. Đối thủ có thể đơn giản đảo ngược nước đi này — giảm số sỏi về giá trị trước đó. Vì trò chơi không có chu trình, sớm muộn người chơi hiện tại cũng không thể dùng nước tăng và phải thực hiện nước đi Nim thông thường.

### Định lý Sprague-Grundy

Xét một trạng thái $v$ của trò chơi hai người vô tư và gọi $v_i$ là các trạng thái đạt được từ nó (với $i \in \{ 1, 2, \dots, k \} , k \ge 0$). Ta có thể gán cho trạng thái này một trò chơi Nim hoàn toàn tương đương gồm một đống có kích thước $x$. Số $x$ được gọi là giá trị Grundy hoặc giá trị Nim của trạng thái $v$.

Hơn nữa, ta có thể tìm số này theo cách đệ quy sau:

$$ x = \text{mex}\ \{ x_1, \ldots, x_k \}, $$

trong đó $x_i$ là giá trị Grundy của trạng thái $v_i$ và hàm $\text{mex}$ (*minimum excludant*) là số nguyên không âm nhỏ nhất không có trong tập đã cho.

Khi xem trò chơi là một đồ thị, ta có thể tính dần các giá trị Grundy bắt đầu từ các đỉnh không có cạnh đi ra. Giá trị Grundy bằng không có nghĩa trạng thái là thua.

**Chứng minh.** Ta dùng chứng minh quy nạp.

Với các đỉnh không có nước đi, giá trị $x$ là $\text{mex}$ của tập rỗng, bằng không. Điều này đúng vì Nim rỗng là trạng thái thua.

Bây giờ xét một đỉnh $v$ bất kỳ khác. Theo quy nạp, giả sử các giá trị $x_i$ tương ứng với những đỉnh có thể đạt tới từ nó đã được tính.

Đặt $p = \text{mex}\ \{ x_1, \ldots, x_k \}$. Khi đó, với mọi số nguyên $i \in [0, p)$, tồn tại một đỉnh có thể đạt tới có giá trị Grundy bằng $i$. Điều này có nghĩa $v$ **tương đương với một trạng thái của Nim cho phép tăng, gồm một đống có kích thước $p$**. Trong trò chơi đó ta có phép chuyển đến các đống có mọi kích thước nhỏ hơn $p$ và có thể có phép chuyển đến các đống có kích thước lớn hơn $p$. Vì vậy $p$ chính là giá trị Grundy cần tìm của trạng thái đang xét.

## Ứng dụng của định lý

Cuối cùng, ta mô tả một thuật toán xác định thắng/thua, áp dụng được cho mọi trò chơi hai người vô tư.

Để tính giá trị Grundy của một trạng thái cho trước:

* Lấy mọi phép chuyển có thể từ trạng thái này.

* Mỗi phép chuyển có thể dẫn đến một **tổng các trò chơi độc lập** (trường hợp suy biến chỉ có một trò chơi). Tính giá trị Grundy của từng trò chơi độc lập rồi lấy tổng xor của chúng. Dĩ nhiên xor không thay đổi gì nếu chỉ có một trò chơi.

* Sau khi tính giá trị Grundy cho mỗi phép chuyển, tìm giá trị của trạng thái bằng $\text{mex}$ của những số đó.

* Nếu giá trị bằng không thì trạng thái hiện tại là thua, ngược lại là thắng.

So với phần trước, ta xét thêm khả năng các phép chuyển dẫn tới trò chơi kết hợp. Ta xem chúng như một trò Nim có các kích thước đống bằng giá trị Grundy của những trò chơi độc lập. Ta có thể lấy tổng xor như trong Nim thông thường theo định lý Bouton.

## Quy luật trong các giá trị Grundy

Khi giải những bài toán cụ thể bằng giá trị Grundy, rất thường xuyên việc **nghiên cứu bảng giá trị** để tìm quy luật là hữu ích.

Trong nhiều trò chơi có vẻ khá khó phân tích về mặt lý thuyết, các giá trị Grundy hóa ra có chu kỳ hoặc có dạng dễ hiểu. Trong phần lớn trường hợp, quy luật quan sát được là đúng và có thể chứng minh bằng quy nạp nếu muốn.

Tuy nhiên, giá trị Grundy không phải *lúc nào* cũng có những quy luật như vậy; ngay cả với một số trò chơi rất đơn giản, bài toán hỏi các quy luật đó có tồn tại hay không vẫn còn bỏ ngỏ (ví dụ "Grundy's game").

## Các trò chơi ví dụ

### Crosses-crosses

**Luật chơi.** Xét một dải ô có kích thước $1 \times n$. Mỗi nước đi, người chơi phải đặt một dấu chéo, nhưng không được đặt hai dấu cạnh nhau (trong các ô kề nhau). Như thường lệ, người không có nước đi hợp lệ sẽ thua.

**Lời giải.** Khi người chơi đặt dấu chéo vào một ô, ta có thể coi dải được chia thành hai phần độc lập: bên trái và bên phải dấu chéo. Khi đó, ô có dấu chéo và các ô liền trái, liền phải của nó bị phá hủy — không thể đặt thêm gì vào chúng. Do đó, nếu đánh số các ô từ $1$ đến $n$, việc đặt dấu chéo tại vị trí $1 < i < n$ chia dải thành hai dải có độ dài $i-2$ và $n-i-1$, tức ta chuyển tới tổng hai trò chơi $i-2$ và $n-i-1$. Với trường hợp biên khi dấu chéo được đặt tại vị trí $1$ hoặc $n$, ta chuyển tới trò chơi $n-2$.

Do đó giá trị Grundy $g(n)$ có dạng:

$$g(n) = \text{mex} \Bigl( \{ g(n-2) \} \cup \{g(i-2) \oplus g(n-i-1) \mid 2 \leq i \leq n-1\} \Bigr) .$$

Vậy ta có lời giải $O(n^2)$.

Thực tế, $g(n)$ có chu kỳ dài 34 bắt đầu từ $n=52$.

## Bài tập luyện tập

- [KATTIS S-Nim](https://open.kattis.com/problems/snim)
- [CodeForces - Marbles (2018-2019 ACM-ICPC Brazil Subregional)](https://codeforces.com/gym/101908/problem/B)
- [KATTIS - Cuboid Slicing Game](https://open.kattis.com/problems/cuboidslicinggame)
- [HackerRank - Tower Breakers, Revisited!](https://www.hackerrank.com/contests/5-days-of-game-theory/challenges/tower-breakers-2)
- [HackerRank - Tower Breakers, Again!](https://www.hackerrank.com/contests/5-days-of-game-theory/challenges/tower-breakers-3/problem)
- [HackerRank - Chessboard Game, Again!](https://www.hackerrank.com/contests/5-days-of-game-theory/challenges/a-chessboard-game)
- [Atcoder - ABC368F - Dividing Game](https://atcoder.jp/contests/abc368/tasks/abc368_f)
