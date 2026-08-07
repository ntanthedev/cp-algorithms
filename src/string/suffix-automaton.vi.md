---
tags:
  - Translated
e_maxx_link: suffix_automata
translation:
  source: string/suffix-automaton.md
  source_commit: ed7685593e2eaa4dd6cb7c2a76253390ffb4968a
  status: draft
  last_synced: 2026-08-07
---

# Suffix Automaton

**Suffix Automaton** là một cấu trúc dữ liệu mạnh, cho phép giải nhiều bài toán liên quan đến xâu. 

Ví dụ, ta có thể tìm mọi lần xuất hiện của một xâu trong xâu khác, hoặc đếm số xâu con phân biệt của một xâu cho trước.
Cả hai bài toán đều có thể giải trong thời gian tuyến tính nhờ Suffix Automaton.

Trực giác, có thể xem Suffix Automaton là một dạng nén của **toàn bộ các xâu con** của một xâu cho trước.
Điều đáng chú ý là nó lưu toàn bộ thông tin này ở dạng rất cô đọng.
Với xâu có độ dài $n$, cấu trúc chỉ cần $O(n)$ bộ nhớ.
Hơn nữa, nó cũng có thể được xây dựng trong $O(n)$ thời gian nếu coi kích thước $k$ của bảng chữ cái là hằng số; nếu không, cả bộ nhớ và độ phức tạp thời gian sẽ là $O(n \log k)$.

Tính tuyến tính của kích thước Suffix Automaton lần đầu được Blumer và cộng sự phát hiện năm 1983, và đến năm 1985, Crochemore cùng Blumer trình bày các thuật toán xây dựng tuyến tính đầu tiên.

## Định nghĩa Suffix Automaton

Suffix Automaton của một xâu $s$ là **DFA** tối tiểu (deterministic finite automaton / deterministic finite state machine) chấp nhận tất cả các hậu tố của xâu $s$.

Nói cách khác:

 -  Suffix Automaton là một đồ thị có hướng không chu trình.
    Các đỉnh được gọi là **trạng thái**, còn các cạnh được gọi là **phép chuyển** giữa các trạng thái.
 -  Một trạng thái $t_0$ là **trạng thái ban đầu**, và nó phải là nguồn của đồ thị (mọi trạng thái khác đều đi tới được từ $t_0$).
 -  Mỗi **phép chuyển** được gắn nhãn bằng một ký tự.
    Mọi phép chuyển đi ra từ cùng một trạng thái phải có nhãn **khác nhau**.
 -  Một hoặc nhiều trạng thái được đánh dấu là **trạng thái kết thúc**.
    Nếu bắt đầu từ trạng thái ban đầu $t_0$ và đi theo các phép chuyển tới một trạng thái kết thúc, chuỗi nhãn trên các phép chuyển đã đi qua phải tạo thành một hậu tố của xâu $s$.
    Mỗi hậu tố của $s$ phải có thể được tạo bởi một đường đi từ $t_0$ tới một trạng thái kết thúc.
 -  Trong tất cả automaton thỏa các điều kiện trên, Suffix Automaton có số đỉnh nhỏ nhất.

### Tính chất xâu con

Tính chất đơn giản và quan trọng nhất của Suffix Automaton là nó chứa thông tin về mọi xâu con của $s$.
Mọi đường đi bắt đầu từ trạng thái ban đầu $t_0$, nếu viết lại nhãn của các phép chuyển, đều tạo thành một **xâu con** của $s$.
Ngược lại, mọi xâu con của $s$ đều tương ứng với một đường đi nào đó bắt đầu tại $t_0$.

Để đơn giản phần giải thích, ta nói xâu con **tương ứng** với đường đi đó (đường đi bắt đầu tại $t_0$ và các nhãn ghép lại thành xâu con).
Ngược lại, ta nói mọi đường đi **tương ứng** với xâu được tạo bởi các nhãn của nó.

Một hoặc nhiều đường đi có thể dẫn tới cùng một trạng thái.
Do đó, ta nói một trạng thái **tương ứng** với tập các xâu tương ứng với những đường đi đó.

### Ví dụ Suffix Automaton đã xây dựng

Dưới đây là một số ví dụ Suffix Automaton cho các xâu đơn giản.

Ta ký hiệu trạng thái ban đầu bằng màu xanh dương và các trạng thái kết thúc bằng màu xanh lá.

Với xâu $s =~ \text{""}$:

![Suffix Automaton cho ""](SA.png)

Với xâu $s =~ \text{"a"}$:

![Suffix Automaton cho "a"](SAa.png)

Với xâu $s =~ \text{"aa"}$:

![Suffix Automaton cho "aa"](SAaa.png)

Với xâu $s =~ \text{"ab"}$:

![Suffix Automaton cho "ab"](SAab.png)

Với xâu $s =~ \text{"aba"}$:

![Suffix Automaton cho "aba"](SAaba.png)

Với xâu $s =~ \text{"abb"}$:

![Suffix Automaton cho "abb"](SAabb.png)

Với xâu $s =~ \text{"abbb"}$:

![Suffix Automaton cho "abbb"](SAabbb.png)

## Xây dựng trong thời gian tuyến tính

Trước khi mô tả thuật toán xây dựng Suffix Automaton trong thời gian tuyến tính, ta cần đưa ra một số khái niệm mới và các chứng minh đơn giản, nhưng rất quan trọng để hiểu cách xây dựng.

### Các vị trí kết thúc $endpos$ {data-toc-label="End positions"}

Xét một xâu con không rỗng bất kỳ $t$ của xâu $s$.
Ta ký hiệu $endpos(t)$ là tập tất cả vị trí trong xâu $s$ mà tại đó một lần xuất hiện của $t$ kết thúc. Chẳng hạn, với xâu $\text{"abcbc"}$ ta có $endpos(\text{"bc"}) = \{2, 4\}$.

Ta gọi hai xâu con $t_1$ và $t_2$ là tương đương theo $endpos$ nếu tập vị trí kết thúc của chúng trùng nhau: $endpos(t_1) = endpos(t_2)$.
Vì vậy, mọi xâu con không rỗng của $s$ có thể được chia thành các **lớp tương đương** theo tập $endpos$.

Hóa ra trong Suffix Automaton, các xâu con tương đương theo $endpos$ **tương ứng với cùng một trạng thái**.
Nói cách khác, số trạng thái trong Suffix Automaton bằng số lớp tương đương của mọi xâu con, cộng thêm trạng thái ban đầu.
Mỗi trạng thái của Suffix Automaton tương ứng với một hoặc nhiều xâu con có cùng giá trị $endpos$.

Sau này ta sẽ mô tả thuật toán xây dựng dựa trên nhận xét này.
Khi đó ta sẽ thấy mọi tính chất cần thiết của Suffix Automaton, ngoại trừ tính tối tiểu, đều được thỏa mãn.
Tính tối tiểu suy ra từ định lý Nerode (không được chứng minh trong bài này).

Ta có một số nhận xét quan trọng về các giá trị $endpos$:

**Bổ đề 1**:
Hai xâu con không rỗng $u$ và $w$ (với $length(u) \le length(w)$) tương đương theo $endpos$ khi và chỉ khi xâu $u$ chỉ xuất hiện trong $s$ dưới dạng hậu tố của $w$.

Chứng minh khá trực tiếp.
Nếu $u$ và $w$ có cùng giá trị $endpos$, thì $u$ là hậu tố của $w$ và trong $s$ chỉ xuất hiện dưới dạng hậu tố của $w$.
Ngược lại, nếu $u$ là hậu tố của $w$ và trong $s$ chỉ xuất hiện dưới dạng hậu tố của $w$, thì theo định nghĩa các giá trị $endpos$ bằng nhau.

**Bổ đề 2**:
Xét hai xâu con không rỗng $u$ và $w$ (với $length(u) \le length(w)$).
Hai tập $endpos$ của chúng hoặc hoàn toàn không giao nhau, hoặc $endpos(w)$ là tập con của $endpos(u)$.
Điều này phụ thuộc vào việc $u$ có phải hậu tố của $w$ hay không.

$$\begin{cases}
endpos(w) \subseteq endpos(u) & \text{if } u \text{ is a suffix of } w \\\\
endpos(w) \cap endpos(u) = \emptyset & \text{otherwise}
\end{cases}$$

Chứng minh:
Nếu hai tập $endpos(u)$ và $endpos(w)$ có ít nhất một phần tử chung thì hai xâu $u$ và $w$ cùng kết thúc tại vị trí đó, tức $u$ là hậu tố của $w$.
Khi đó, ở mỗi lần xuất hiện của $w$ cũng xuất hiện xâu con $u$, nên $endpos(w)$ là tập con của $endpos(u)$.

**Bổ đề 3**:
Xét một lớp tương đương theo $endpos$.
Sắp xếp mọi xâu con trong lớp theo độ dài giảm dần.
Khi đó, trong dãy thu được, mỗi xâu ngắn hơn xâu trước đúng một ký tự và đồng thời là hậu tố của xâu trước.
Nói cách khác, trong cùng một lớp tương đương, các xâu con ngắn hơn là hậu tố của các xâu con dài hơn, và chúng có đủ mọi độ dài trong một đoạn $[x; y]$.

Chứng minh:
Cố định một lớp tương đương theo $endpos$.
Nếu lớp chỉ chứa một xâu thì bổ đề hiển nhiên đúng.
Giờ giả sử lớp chứa nhiều hơn một xâu.

Theo Bổ đề 1, với hai xâu khác nhau nhưng tương đương theo $endpos$, xâu ngắn hơn luôn là hậu tố thực sự của xâu dài hơn.
Do đó không thể có hai xâu cùng độ dài trong một lớp tương đương.

Gọi $w$ là xâu dài nhất và $u$ là xâu ngắn nhất trong lớp tương đương.
Theo Bổ đề 1, xâu $u$ là hậu tố thực sự của xâu $w$.
Xét một hậu tố bất kỳ của $w$ có độ dài thuộc đoạn $[length(u); length(w)]$.
Dễ thấy hậu tố này cũng thuộc cùng lớp tương đương.
Lý do là hậu tố này chỉ có thể xuất hiện trong $s$ dưới dạng hậu tố của $w$ (vì ngay cả hậu tố ngắn hơn $u$ cũng chỉ xuất hiện trong $s$ dưới dạng hậu tố của $w$).
Do đó, theo Bổ đề 1, hậu tố này tương đương theo $endpos$ với xâu $w$.

### Liên kết hậu tố $link$ {data-toc-label="Suffix links"}

Xét một trạng thái $v \ne t_0$ trong automaton.
Như đã biết, trạng thái $v$ tương ứng với lớp các xâu có cùng giá trị $endpos$.
Nếu ký hiệu $w$ là xâu dài nhất trong lớp này thì mọi xâu còn lại đều là hậu tố của $w$.

Ta cũng biết một số hậu tố dài nhất đầu tiên của $w$ (nếu xét các hậu tố theo độ dài giảm dần) đều thuộc lớp tương đương này, còn mọi hậu tố tiếp theo (ít nhất có một — hậu tố rỗng) thuộc các lớp khác.
Ta ký hiệu $t$ là hậu tố dài nhất như vậy trong lớp khác và tạo một liên kết hậu tố tới nó.

Nói cách khác, **liên kết hậu tố** $link(v)$ dẫn tới trạng thái tương ứng với **hậu tố dài nhất** của $w$ nằm trong một lớp tương đương $endpos$ khác.

Ở đây ta giả sử trạng thái ban đầu $t_0$ thuộc một lớp tương đương riêng (chỉ chứa xâu rỗng), và để thuận tiện đặt $endpos(t_0) = \{-1, 0, \dots, length(s)-1\}$.

**Bổ đề 4**:
Các liên kết hậu tố tạo thành một **cây** có gốc $t_0$.

Chứng minh:
Xét một trạng thái bất kỳ $v \ne t_0$.
Liên kết hậu tố $link(v)$ dẫn tới một trạng thái tương ứng với các xâu có độ dài nhỏ hơn nghiêm ngặt (điều này suy ra từ định nghĩa liên kết hậu tố và Bổ đề 3).
Vì vậy, nếu liên tục đi theo các liên kết hậu tố, sớm hay muộn ta sẽ tới trạng thái ban đầu $t_0$, tương ứng với xâu rỗng.

**Bổ đề 5**:
Nếu xây dựng một cây từ các tập $endpos$ (theo quy tắc tập của nút cha chứa các tập của mọi nút con), thì cấu trúc này trùng với cây liên kết hậu tố.

Chứng minh:
Việc có thể xây một cây từ các tập $endpos$ suy ra trực tiếp từ Bổ đề 2 (hai tập bất kỳ hoặc không giao nhau, hoặc một tập chứa tập kia).

Xét một trạng thái bất kỳ $v \ne t_0$ và liên kết hậu tố $link(v)$ của nó.
Từ định nghĩa liên kết hậu tố và Bổ đề 2, ta có

$$endpos(v) \subseteq endpos(link(v)),$$

kết hợp với bổ đề trước sẽ chứng minh khẳng định:
cây liên kết hậu tố về bản chất chính là cây bao hàm của các tập $endpos$.

Dưới đây là một **ví dụ** về cây liên kết hậu tố trong Suffix Automaton xây cho xâu $\text{"abcbc"}$.
Các nút được gắn nhãn bằng xâu dài nhất trong lớp tương đương tương ứng.

![Suffix Automaton cho "abcbc" với các liên kết hậu tố](SA_suffix_links.png)

### Tóm tắt

Trước khi đi vào thuật toán, ta tóm tắt các kiến thức đã có và đưa ra một số ký hiệu phụ trợ.

- Các xâu con của $s$ có thể được chia thành các lớp tương đương theo vị trí kết thúc $endpos$.
- Suffix Automaton gồm trạng thái ban đầu $t_0$ và một trạng thái cho mỗi lớp tương đương theo $endpos$.
- Mỗi trạng thái $v$ tương ứng với một hoặc nhiều xâu con.
  Ta ký hiệu $longest(v)$ là xâu dài nhất như vậy và $len(v)$ là độ dài của nó.
  Ta ký hiệu $shortest(v)$ là xâu con ngắn nhất như vậy và độ dài của nó là $minlen(v)$.
  Khi đó mọi xâu tương ứng với trạng thái này là các hậu tố khác nhau của xâu $longest(v)$, với đủ mọi độ dài trong đoạn $[minlen(v); len(v)]$.
- Với mỗi trạng thái $v \ne t_0$, liên kết hậu tố được định nghĩa là liên kết dẫn tới trạng thái tương ứng với hậu tố của xâu $longest(v)$ có độ dài $minlen(v) - 1$.
  Các liên kết hậu tố tạo thành một cây có gốc $t_0$, đồng thời cây này biểu diễn quan hệ bao hàm giữa các tập $endpos$.
- Ta có thể biểu diễn $minlen(v)$ với $v \ne t_0$ thông qua liên kết hậu tố $link(v)$:
  
$$minlen(v) = len(link(v)) + 1$$

- Nếu bắt đầu từ một trạng thái bất kỳ $v_0$ và đi theo các liên kết hậu tố, sớm hay muộn ta sẽ tới trạng thái ban đầu $t_0$.
  Khi đó ta thu được một dãy các đoạn rời nhau $[minlen(v_i); len(v_i)]$, mà hợp của chúng tạo thành đoạn liên tục $[0; len(v_0)]$.

### Thuật toán

Giờ ta có thể đi vào thuật toán.
Thuật toán hoạt động **online**, tức ta thêm từng ký tự của xâu theo thứ tự và cập nhật automaton sau mỗi bước.

Để dùng bộ nhớ tuyến tính, ở mỗi trạng thái ta chỉ lưu các giá trị $len$, $link$ và danh sách phép chuyển.
Ta chưa đánh dấu các trạng thái kết thúc (sau này sẽ trình bày cách đánh dấu sau khi xây xong Suffix Automaton).

Ban đầu automaton chỉ có một trạng thái $t_0$, mang chỉ số $0$ (các trạng thái còn lại sẽ nhận chỉ số $1, 2, \dots$).
Ta gán $len = 0$ và $link = -1$ cho trạng thái này để thuận tiện ($-1$ là một trạng thái giả không tồn tại).

Bây giờ toàn bộ bài toán quy về việc cài đặt thao tác **thêm một ký tự** $c$ vào cuối xâu hiện tại.
Ta mô tả quá trình này như sau:

  - Gọi $last$ là trạng thái tương ứng với toàn bộ xâu trước khi thêm ký tự $c$.
    (Ban đầu đặt $last = 0$, và ở bước cuối của thuật toán ta sẽ cập nhật $last$ tương ứng.)
  - Tạo trạng thái mới $cur$ và gán $len(cur) = len(last) + 1$.
    Lúc này chưa biết giá trị $link(cur)$.
  - Tiếp theo thực hiện quy trình sau:
    Bắt đầu tại trạng thái $last$.
    Khi chưa có phép chuyển theo ký tự $c$, ta thêm một phép chuyển tới trạng thái $cur$, rồi đi theo liên kết hậu tố.
    Nếu tại một thời điểm đã có phép chuyển theo ký tự $c$, ta dừng lại và gọi trạng thái đó là $p$.
  - Nếu không tìm được trạng thái $p$ như vậy, tức đã tới trạng thái giả $-1$, ta chỉ cần gán $link(cur) = 0$ rồi kết thúc.
  - Giả sử đã tìm được trạng thái $p$ có phép chuyển theo ký tự $c$.
    Gọi trạng thái mà phép chuyển đó dẫn tới là $q$.
  - Lúc này có hai trường hợp: $len(p) + 1 = len(q)$ hoặc không.
  - Nếu $len(p) + 1 = len(q)$, ta chỉ cần gán $link(cur) = q$ rồi kết thúc.
  - Nếu không, tình huống phức tạp hơn một chút.
    Ta phải **clone** trạng thái $q$:
    tạo trạng thái mới $clone$, sao chép mọi dữ liệu từ $q$ (liên kết hậu tố và các phép chuyển) ngoại trừ giá trị $len$.
    Ta gán $len(clone) = len(p) + 1$.

    Sau khi clone, ta hướng liên kết hậu tố của $cur$ tới $clone$, đồng thời hướng liên kết hậu tố của $q$ tới clone.

    Cuối cùng, ta đi ngược từ trạng thái $p$ bằng các liên kết hậu tố, chừng nào vẫn còn một phép chuyển theo $c$ tới trạng thái $q$, và chuyển hướng mọi phép chuyển như vậy sang trạng thái $clone$.

  - Trong cả ba trường hợp, sau khi hoàn tất quy trình, ta cập nhật $last$ thành trạng thái $cur$.

Nếu muốn biết trạng thái nào là **trạng thái kết thúc**, ta có thể xác định chúng sau khi xây xong Suffix Automaton cho toàn bộ xâu $s$.
Ta lấy trạng thái tương ứng với toàn bộ xâu (được lưu trong biến $last$), rồi liên tục đi theo các liên kết hậu tố cho đến trạng thái ban đầu.
Ta đánh dấu tất cả trạng thái đã đi qua là trạng thái kết thúc.
Dễ thấy cách này đánh dấu chính xác các trạng thái tương ứng với mọi hậu tố của xâu $s$, tức chính xác các trạng thái kết thúc.

Ở mục tiếp theo, ta sẽ xem chi tiết từng bước và chứng minh **tính đúng đắn**.

Ở đây chỉ cần lưu ý rằng vì mỗi ký tự của $s$ chỉ tạo thêm một hoặc hai trạng thái mới, Suffix Automaton có **số trạng thái tuyến tính**.

Tính tuyến tính của số phép chuyển và nói chung là thời gian chạy tuyến tính của thuật toán kém hiển nhiên hơn; chúng sẽ được chứng minh sau phần tính đúng đắn.

### Tính đúng đắn

  - Ta gọi phép chuyển $(p, q)$ là **liên tục** nếu $len(p) + 1 = len(q)$.
    Ngược lại, nếu $len(p) + 1 < len(q)$, ta gọi phép chuyển là **không liên tục**.

    Như có thể thấy từ mô tả thuật toán, hai loại phép chuyển này dẫn tới các trường hợp xử lý khác nhau.
    Phép chuyển liên tục là cố định và sẽ không bao giờ thay đổi nữa.
    Ngược lại, phép chuyển không liên tục có thể thay đổi khi thêm ký tự mới vào xâu (đầu cuối của cạnh chuyển có thể thay đổi).

  - Để tránh nhập nhằng, ta ký hiệu xâu mà Suffix Automaton đã được xây trước khi thêm ký tự hiện tại $c$ là $s$.

  - Thuật toán bắt đầu bằng việc tạo trạng thái mới $cur$, tương ứng với toàn bộ xâu $s + c$.
    Lý do phải tạo trạng thái mới là rõ ràng.
    Cùng với ký tự mới, một lớp tương đương mới được tạo ra.

  - Sau khi tạo trạng thái mới, ta duyệt các liên kết hậu tố bắt đầu từ trạng thái tương ứng với toàn bộ xâu $s$.
    Với mỗi trạng thái, ta cố thêm phép chuyển theo ký tự $c$ tới trạng thái mới $cur$.
    Như vậy, ta nối ký tự $c$ vào từng hậu tố của $s$.
    Tuy nhiên chỉ có thể thêm các phép chuyển mới nếu chúng không xung đột với một phép chuyển đã tồn tại.
    Vì thế ngay khi gặp một phép chuyển theo $c$ đã có, ta phải dừng.

  - Trong trường hợp đơn giản nhất, ta tới trạng thái giả $-1$.
    Điều này nghĩa là ta đã thêm phép chuyển theo $c$ cho mọi hậu tố của $s$.
    Nó cũng có nghĩa ký tự $c$ chưa từng xuất hiện trong xâu $s$ trước đó.
    Vì vậy liên kết hậu tố của $cur$ phải trỏ tới trạng thái $0$.

  - Trong trường hợp thứ hai, ta gặp một phép chuyển $(p, q)$ đã tồn tại.
    Điều này nghĩa là ta đang cố thêm xâu $x + c$ (trong đó $x$ là một hậu tố của $s$) vào automaton, nhưng xâu đó **đã tồn tại** trong automaton (xâu $x + c$ đã xuất hiện như một xâu con của $s$).
    Vì giả sử automaton của xâu $s$ đã được xây đúng, ta không nên thêm một phép chuyển mới tại đây.

    Tuy nhiên vẫn còn một khó khăn.
    Liên kết hậu tố của trạng thái $cur$ nên dẫn tới đâu?
    Ta cần liên kết hậu tố tới một trạng thái mà xâu dài nhất của nó chính xác là $x + c$, tức $len$ của trạng thái đó phải bằng $len(p) + 1$.
    Nhưng có thể trạng thái như vậy chưa tồn tại, tức $len(q) > len(p) + 1$.
    Khi đó ta phải tạo ra nó bằng cách **tách** trạng thái $q$.

  - Nếu phép chuyển $(p, q)$ là liên tục thì $len(q) = len(p) + 1$.
    Khi đó mọi thứ đơn giản.
    Ta hướng liên kết hậu tố của $cur$ tới trạng thái $q$.

  - Ngược lại, phép chuyển không liên tục nghĩa là $len(q) > len(p) + 1$.
    Điều này cho thấy trạng thái $q$ không chỉ tương ứng với hậu tố của $s + c$ có độ dài $len(p) + 1$, mà còn tương ứng với các xâu con dài hơn của $s$.
    Không còn cách nào khác ngoài việc **tách** trạng thái $q$ thành hai trạng thái con, sao cho trạng thái đầu tiên có độ dài $len(p) + 1$.

    Làm thế nào để tách một trạng thái?
    Ta **clone** trạng thái $q$, tạo ra trạng thái $clone$, rồi đặt $len(clone) = len(p) + 1$.
    Ta sao chép toàn bộ phép chuyển từ $q$ sang $clone$ vì không muốn thay đổi các đường đi đi qua $q$.
    Đồng thời, ta đặt liên kết hậu tố của $clone$ tới đích của liên kết hậu tố của $q$, rồi đặt liên kết hậu tố của $q$ tới $clone$.

    Sau khi tách trạng thái, ta đặt liên kết hậu tố của $cur$ tới $clone$.

    Ở bước cuối, ta thay đổi một số phép chuyển đang dẫn tới $q$ và chuyển chúng sang $clone$.
    Cần đổi những phép chuyển nào?
    Chỉ cần chuyển hướng các phép chuyển tương ứng với mọi hậu tố của xâu $w + c$ (trong đó $w$ là xâu dài nhất của $p$), tức tiếp tục đi theo các liên kết hậu tố bắt đầu từ đỉnh $p$ cho đến khi tới trạng thái giả $-1$ hoặc gặp một phép chuyển dẫn tới trạng thái khác $q$.

### Số phép toán tuyến tính

Trước hết ta giả sử ngay rằng kích thước bảng chữ cái là **hằng số**.
Nếu không, ta không thể nói độ phức tạp thời gian là tuyến tính.
Danh sách các phép chuyển từ một đỉnh sẽ được lưu bằng cây cân bằng, cho phép tìm khóa và thêm khóa nhanh.
Do đó, nếu ký hiệu $k$ là kích thước bảng chữ cái, độ phức tạp tiệm cận của thuật toán là $O(n \log k)$ với $O(n)$ bộ nhớ.
Tuy nhiên, nếu bảng chữ cái đủ nhỏ, ta có thể đánh đổi bộ nhớ để không dùng cây cân bằng: lưu các phép chuyển của mỗi đỉnh bằng một mảng độ dài $k$ (để tìm nhanh theo khóa) và một danh sách động (để duyệt nhanh mọi khóa hiện có).
Nhờ đó, thuật toán đạt $O(n)$ thời gian, với chi phí bộ nhớ $O(n k)$.

Vì vậy, từ đây ta coi kích thước bảng chữ cái là hằng số, tức mọi thao tác tìm phép chuyển theo một ký tự, thêm phép chuyển, tìm phép chuyển tiếp theo đều thực hiện được trong $O(1)$.

Nếu xét toàn bộ thuật toán, có ba vị trí mà độ phức tạp tuyến tính chưa hiển nhiên:

  - Thứ nhất là việc duyệt các liên kết hậu tố từ trạng thái $last$ và thêm phép chuyển theo ký tự $c$.
  - Thứ hai là sao chép các phép chuyển khi clone trạng thái $q$ thành trạng thái mới $clone$.
  - Thứ ba là thay đổi các phép chuyển đang dẫn tới $q$ để chuyển chúng sang $clone$.

Ta dùng thực tế rằng kích thước Suffix Automaton — cả số trạng thái lẫn số phép chuyển — là **tuyến tính**.
(Nguồn viết rằng chứng minh tính tuyến tính của số trạng thái là chính thuật toán, và chứng minh tính tuyến tính của số trạng thái được đưa ra phía dưới, sau phần cài đặt thuật toán.)

**Ghi chú bản dịch:** Trong câu trên, nguồn lặp lại “number of states”; theo mạch lập luận, vế thứ hai rõ ràng đang nói tới tính tuyến tính của số phép chuyển. Bản dịch giữ thông tin nguồn và ghi chú điểm này thay vì âm thầm sửa source English.

Do đó, tổng độ phức tạp của **vị trí thứ nhất và thứ hai** là hiển nhiên, vì xét khấu hao thì mỗi thao tác chỉ thêm một phép chuyển mới vào automaton.

Còn lại là ước lượng tổng độ phức tạp của **vị trí thứ ba**, nơi ta chuyển hướng các phép chuyển ban đầu trỏ tới $q$ sang $clone$.
Ta ký hiệu $v = longest(p)$.
Đây là một hậu tố của xâu $s$, và sau mỗi vòng lặp độ dài của nó giảm đi — vì vậy vị trí của $v$ khi xem là hậu tố của xâu $s$ tăng đơn điệu sau mỗi vòng.
Trong trường hợp này, nếu trước vòng đầu tiên, xâu tương ứng $v$ ở độ sâu $k$ ($k \ge 2$) tính từ $last$ (độ sâu tính theo số liên kết hậu tố), thì sau vòng cuối, xâu $v + c$ sẽ nằm ở liên kết hậu tố thứ $2$ trên đường đi từ $cur$ (và $cur$ sẽ trở thành giá trị $last$ mới).

Vì vậy, mỗi vòng của vòng lặp này làm vị trí của xâu $longest(link(link(last))$ khi xem là hậu tố của xâu hiện tại tăng đơn điệu.
Do đó vòng lặp không thể chạy quá $n$ lần, đúng như cần chứng minh.

### Cài đặt

Trước tiên, ta mô tả cấu trúc dữ liệu lưu mọi thông tin của một trạng thái cụ thể ($len$, $link$ và danh sách phép chuyển).
Nếu cần, có thể bổ sung cờ trạng thái kết thúc cũng như các thông tin khác.
Ta lưu danh sách phép chuyển bằng $map$, nhờ đó toàn bộ xâu dùng $O(n)$ bộ nhớ và $O(n \log k)$ thời gian xử lý.

```{.cpp file=suffix_automaton_struct}
struct state {
    int len, link;
    map<char, int> next;
};
```

Suffix Automaton được lưu trong một mảng các cấu trúc $state$.
Ta lưu kích thước hiện tại $sz$ cùng biến $last$, tức trạng thái tương ứng với toàn bộ xâu tại thời điểm hiện tại.

```{.cpp file=suffix_automaton_def}
const int MAXLEN = 100000;
state st[MAXLEN * 2];
int sz, last;
```

Ta viết hàm khởi tạo Suffix Automaton, tức tạo một automaton chỉ có một trạng thái.

```{.cpp file=suffix_automaton_init}
void sa_init() {
    st[0].len = 0;
    st[0].link = -1;
    sz++;
    last = 0;
}
```

Cuối cùng là cài đặt hàm chính — thêm ký tự tiếp theo vào cuối xâu hiện tại và xây lại automaton cho phù hợp.

```{.cpp file=suffix_automaton_extend}
void sa_extend(char c) {
    int cur = sz++;
    st[cur].len = st[last].len + 1;
    int p = last;
    while (p != -1 && !st[p].next.count(c)) {
        st[p].next[c] = cur;
        p = st[p].link;
    }
    if (p == -1) {
        st[cur].link = 0;
    } else {
        int q = st[p].next[c];
        if (st[p].len + 1 == st[q].len) {
            st[cur].link = q;
        } else {
            int clone = sz++;
            st[clone].len = st[p].len + 1;
            st[clone].next = st[q].next;
            st[clone].link = st[q].link;
            while (p != -1 && st[p].next[c] == q) {
                st[p].next[c] = clone;
                p = st[p].link;
            }
            st[q].link = st[cur].link = clone;
        }
    }
    last = cur;
}
```

Như đã nói ở trên, nếu chấp nhận dùng nhiều bộ nhớ hơn ($O(n k)$, trong đó $k$ là kích thước bảng chữ cái), ta có thể đạt thời gian xây automaton là $O(n)$, ngay cả với bảng chữ cái có kích thước $k$ bất kỳ.
Để làm vậy, mỗi trạng thái cần lưu một mảng kích thước $k$ (để nhảy nhanh theo ký tự) và thêm một danh sách mọi phép chuyển (để duyệt nhanh qua chúng).

## Các tính chất bổ sung

### Số trạng thái

Số trạng thái trong Suffix Automaton của xâu $s$ độ dài $n$ **không vượt quá** $2n - 1$ (với $n \ge 2$).

Chứng minh đầu tiên chính là thuật toán xây dựng: ban đầu automaton có một trạng thái; ở bước lặp thứ nhất và thứ hai chỉ tạo một trạng thái mới, còn trong $n-2$ bước còn lại, mỗi bước tạo nhiều nhất $2$ trạng thái.

Tuy nhiên, ta cũng có thể **chứng minh** cận này **mà không cần biết thuật toán**.
Nhắc lại rằng số trạng thái bằng số tập $endpos$ khác nhau.
Ngoài ra, các tập $endpos$ tạo thành một cây (tập của đỉnh cha chứa toàn bộ tập của các đỉnh con).
Xét cây này và biến đổi một chút:
miễn là còn một đỉnh trong chỉ có một con (nghĩa là tập của đỉnh con thiếu ít nhất một vị trí so với tập của đỉnh cha), ta tạo một đỉnh con mới chứa tập các vị trí bị thiếu.
Cuối cùng thu được một cây mà mỗi đỉnh trong có bậc lớn hơn một, còn số lá không vượt quá $n$.
Do đó cây có không quá $2n - 1$ đỉnh.

Cận số trạng thái này thực sự đạt được với mọi $n$.
Một xâu ví dụ là:

$$\text{"abbb}\dots \text{bbb"}$$

Từ vòng lặp thứ ba trở đi, ở mỗi bước thuật toán sẽ tách một trạng thái, tạo ra đúng $2n - 1$ trạng thái.

### Số phép chuyển

Số phép chuyển trong Suffix Automaton của xâu $s$ độ dài $n$ **không vượt quá** $3n - 4$ (với $n \ge 3$).

Ta chứng minh như sau:

Trước tiên, ước lượng số phép chuyển liên tục.
Xét một cây khung của các đường đi dài nhất trong automaton bắt đầu tại trạng thái $t_0$.
Khung này chỉ gồm các cạnh liên tục, nên số cạnh nhỏ hơn số trạng thái, tức không vượt quá $2n - 2$.

Tiếp theo, ước lượng số phép chuyển không liên tục.
Xét phép chuyển không liên tục hiện tại $(p, q)$ mang ký tự $c$.
Ta lấy xâu tương ứng $u + c + w$, trong đó $u$ tương ứng với đường đi dài nhất từ trạng thái ban đầu tới $p$, còn $w$ tương ứng với đường đi dài nhất từ $q$ tới một trạng thái kết thúc bất kỳ.
Một mặt, mỗi xâu $u + c + w$ như vậy ứng với mỗi xâu không hoàn chỉnh sẽ khác nhau (vì các xâu $u$ và $w$ chỉ được tạo bởi các phép chuyển hoàn chỉnh).
Mặt khác, theo định nghĩa trạng thái kết thúc, mỗi xâu $u + c + w$ như vậy là một hậu tố của toàn bộ xâu $s$.
Vì $s$ chỉ có $n$ hậu tố không rỗng và không xâu $u + c + w$ nào có thể chứa $s$ (vì toàn bộ xâu chỉ gồm các phép chuyển hoàn chỉnh), tổng số phép chuyển không hoàn chỉnh không vượt quá $n - 1$.

Kết hợp hai ước lượng cho cận $3n - 3$.
Tuy nhiên, vì số trạng thái cực đại chỉ đạt được với test $\text{"abbb\dots bbb"}$ và trường hợp này rõ ràng có ít hơn $3n - 3$ phép chuyển, ta thu được cận chặt hơn $3n - 4$ cho số phép chuyển của Suffix Automaton.

Cận này cũng có thể đạt được với xâu:

$$\text{"abbb}\dots \text{bbbc"}$$

## Ứng dụng

Ở đây ta xét một số bài toán có thể giải bằng Suffix Automaton.
Để đơn giản, giả sử kích thước bảng chữ cái $k$ là hằng số, cho phép coi chi phí thêm ký tự và duyệt phép chuyển là hằng số.

### Kiểm tra sự xuất hiện

Cho một văn bản $T$ và nhiều mẫu $P$.
Ta cần kiểm tra các xâu $P$ có xuất hiện như xâu con của $T$ hay không.

Ta xây Suffix Automaton của văn bản $T$ trong $O(length(T))$ thời gian.
Để kiểm tra một mẫu $P$ có xuất hiện trong $T$ hay không, ta bắt đầu từ $t_0$ và đi theo các phép chuyển tương ứng với từng ký tự của $P$.
Nếu tại một thời điểm không tồn tại phép chuyển cần thiết thì mẫu $P$ không xuất hiện như xâu con của $T$.
Nếu xử lý được toàn bộ $P$ theo cách này thì xâu đó xuất hiện trong $T$.

Rõ ràng mỗi xâu $P$ cần $O(length(P))$ thời gian.
Ngoài ra, thuật toán thực chất còn tìm được độ dài tiền tố dài nhất của $P$ xuất hiện trong văn bản.

### Số xâu con phân biệt

Cho một xâu $S$.
Ta muốn tính số xâu con phân biệt.

Hãy xây Suffix Automaton cho xâu $S$.

Mỗi xâu con của $S$ tương ứng với một đường đi trong automaton.
Do đó số xâu con phân biệt bằng số đường đi khác nhau trong automaton bắt đầu tại $t_0$.

Vì Suffix Automaton là đồ thị có hướng không chu trình, ta có thể dùng quy hoạch động để đếm số đường đi khác nhau.

Cụ thể, gọi $d[v]$ là số đường đi bắt đầu tại trạng thái $v$ (kể cả đường đi độ dài bằng không).
Ta có công thức truy hồi:

$$d[v] = 1 + \sum_{w : (v, w, c) \in DAWG} d[w]$$

Tức $d[v]$ bằng một cộng tổng đáp án của mọi đỉnh cuối của các phép chuyển đi ra từ $v$.

Số xâu con phân biệt là $d[t_0] - 1$ (vì không tính xâu rỗng).

Tổng độ phức tạp thời gian: $O(length(S))$


Một cách khác là tận dụng tính chất mỗi trạng thái $v$ tương ứng với các xâu con có độ dài $[minlen(v),len(v)]$.
Vì $minlen(v) = 1 + len(link(v))$, tổng số xâu con phân biệt tại trạng thái $v$ là $len(v) - minlen(v) + 1 = len(v) - (1 + len(link(v))) + 1 = len(v) - len(link(v))$.

Cài đặt ngắn gọn như sau:

```cpp
long long get_diff_strings(){
    long long tot = 0;
    for(int i = 1; i < sz; i++) {
        tot += st[i].len - st[st[i].link].len;
    }
    return tot;
}
```

Cách này cũng là $O(length(S))$, nhưng không cần bộ nhớ phụ và không dùng lời gọi đệ quy, nên thực tế chạy nhanh hơn.

### Tổng độ dài của mọi xâu con phân biệt

Cho một xâu $S$.
Ta muốn tính tổng độ dài của tất cả xâu con phân biệt của nó.

Lời giải tương tự bài trước, chỉ khác là trong phần quy hoạch động cần xét hai đại lượng:
số xâu con phân biệt $d[v]$ và tổng độ dài của chúng $ans[v]$.

Ta đã mô tả cách tính $d[v]$ ở bài trước.
Giá trị $ans[v]$ có thể tính bằng công thức truy hồi:

$$ans[v] = \sum_{w : (v, w, c) \in DAWG} d[w] + ans[w]$$

Ta lấy đáp án của từng đỉnh kề $w$ và cộng thêm $d[w]$ (vì mỗi xâu con dài thêm một ký tự khi bắt đầu từ trạng thái $v$).

Bài này cũng có thể giải trong $O(length(S))$ thời gian.

Một lần nữa, ta có thể tận dụng tính chất mỗi trạng thái $v$ tương ứng với các xâu con có độ dài $[minlen(v),len(v)]$.
Vì $minlen(v) = 1 + len(link(v))$ và công thức cấp số cộng $S_n = n \cdot \frac{a_1+a_n}{2}$ (trong đó $S_n$ là tổng của $n$ số hạng, $a_1$ là số hạng đầu và $a_n$ là số hạng cuối), ta có thể tính tổng độ dài các xâu con tại một trạng thái trong thời gian hằng số. Sau đó cộng các giá trị này trên mọi trạng thái $v \neq t_0$ trong automaton. Cài đặt như sau:

```cpp
long long get_tot_len_diff_substings() {
    long long tot = 0;
    for(int i = 1; i < sz; i++) {
        long long shortest = st[st[i].link].len + 1;
        long long longest = st[i].len;
        
        long long num_strings = longest - shortest + 1;
        long long cur = num_strings * (longest + shortest) / 2;
        tot += cur;
    }
    return tot;
}
```

Cách này chạy trong $O(length(S))$ thời gian, và theo thực nghiệm chạy nhanh hơn khoảng 20 lần so với phiên bản quy hoạch động có memo trên các xâu ngẫu nhiên. Nó không cần bộ nhớ phụ và không dùng đệ quy.

### Xâu con thứ $k$ theo thứ tự từ điển {data-toc-label="Lexicographically k-th substring"}

Cho một xâu $S$.
Ta cần trả lời nhiều truy vấn.
Với mỗi số $K_i$, cần tìm xâu thứ $K_i$ trong danh sách mọi xâu con được sắp theo thứ tự từ điển.

Lời giải dựa trên ý tưởng của hai bài trước.
Xâu con thứ $k$ theo thứ tự từ điển tương ứng với đường đi thứ $k$ theo thứ tự từ điển trong Suffix Automaton.
Vì vậy, sau khi đếm số đường đi từ mỗi trạng thái, ta có thể dễ dàng tìm đường đi thứ $k$ bắt đầu từ gốc automaton.

Việc tiền xử lý tốn $O(length(S))$ thời gian, sau đó mỗi truy vấn tốn $O(length(ans) \cdot k)$ (trong đó $ans$ là đáp án của truy vấn và $k$ là kích thước bảng chữ cái).

### Phép dịch vòng nhỏ nhất

Cho một xâu $S$.
Ta muốn tìm phép dịch vòng nhỏ nhất theo thứ tự từ điển.

Ta xây Suffix Automaton cho xâu $S + S$.
Khi đó automaton chứa mọi phép dịch vòng của xâu $S$ dưới dạng các đường đi.

Vì vậy, bài toán quy về tìm đường đi nhỏ nhất theo thứ tự từ điển có độ dài $length(S)$; có thể làm trực tiếp bằng cách bắt đầu tại trạng thái ban đầu và tham lam đi theo phép chuyển có ký tự nhỏ nhất.

Tổng độ phức tạp thời gian là $O(length(S))$.

### Số lần xuất hiện

Với một văn bản $T$ cho trước,
ta cần trả lời nhiều truy vấn.
Với mỗi mẫu $P$, cần tìm số lần xâu $P$ xuất hiện như một xâu con của $T$.

Ta xây Suffix Automaton cho văn bản $T$.

Tiếp theo thực hiện tiền xử lý:
với mỗi trạng thái $v$ trong automaton, ta tính $cnt[v]$ bằng kích thước của tập $endpos(v)$.
Thực tế, mọi xâu tương ứng với cùng một trạng thái $v$ xuất hiện trong văn bản $T$ cùng số lần, bằng số vị trí trong tập $endpos$.

Tuy nhiên, ta không thể xây tường minh các tập $endpos$, nên chỉ xét kích thước $cnt$ của chúng.

Ta tính như sau.
Với mỗi trạng thái, nếu nó không được tạo bằng thao tác clone (và không phải trạng thái ban đầu $t_0$), khởi tạo $cnt = 1$.
Sau đó duyệt mọi trạng thái theo thứ tự giảm dần của độ dài $len$ và cộng giá trị hiện tại $cnt[v]$ vào trạng thái qua liên kết hậu tố:

$$cnt[link(v)] \text{ += } cnt[v]$$

Cách này cho giá trị đúng ở mọi trạng thái.

Tại sao đúng?
Tổng số trạng thái không được tạo bằng clone chính xác bằng $length(T)$, và $i$ trạng thái đầu tiên trong số đó xuất hiện khi ta thêm $i$ ký tự đầu.
Do đó, với mỗi trạng thái này, ta đếm vị trí tương ứng tại thời điểm nó được xử lý.
Vì vậy ban đầu $cnt = 1$ cho mỗi trạng thái như vậy và $cnt = 0$ cho tất cả trạng thái còn lại.

Sau đó, với mỗi $v$, ta thực hiện phép toán $cnt[link(v)] \text{ += } cnt[v]$.
Ý nghĩa là nếu một xâu $v$ xuất hiện $cnt[v]$ lần thì mọi hậu tố của nó cũng xuất hiện tại chính các vị trí kết thúc đó, tức cũng $cnt[v]$ lần.

Tại sao quy trình này không đếm trùng, tức không đếm một vị trí hai lần?
Vì ta chỉ cộng các vị trí của một trạng thái vào đúng một trạng thái khác, nên không thể xảy ra trường hợp một trạng thái gửi cùng các vị trí tới trạng thái khác theo hai đường khác nhau.

Nhờ vậy, ta tính được $cnt$ cho mọi trạng thái trong automaton trong $O(length(T))$ thời gian.

Sau đó, để trả lời truy vấn, chỉ cần lấy $cnt[t]$, trong đó $t$ là trạng thái tương ứng với mẫu nếu trạng thái đó tồn tại.
Nếu không, đáp án là $0$.
Mỗi truy vấn tốn $O(length(P))$ thời gian.

### Vị trí xuất hiện đầu tiên

Cho văn bản $T$ và nhiều truy vấn.
Với mỗi xâu truy vấn $P$, ta muốn tìm vị trí bắt đầu của lần xuất hiện đầu tiên của $P$ trong xâu $T$.

Ta lại xây Suffix Automaton.
Ngoài ra, ta tính trước vị trí $firstpos$ cho mọi trạng thái, tức với mỗi trạng thái $v$, cần tìm vị trí $firstpos[v]$ là vị trí kết thúc của lần xuất hiện đầu tiên.
Nói cách khác, ta muốn biết trước phần tử nhỏ nhất của mỗi tập $endpos$ (vì rõ ràng không thể lưu tường minh mọi tập $endpos$).

Để duy trì các vị trí $firstpos$, ta mở rộng hàm `sa_extend()`.
Khi tạo trạng thái mới $cur$, ta đặt:

$$firstpos(cur) = len(cur) - 1$$

Khi clone một đỉnh $q$ thành $clone$, ta đặt:

$$firstpos(clone) = firstpos(q)$$

(vì lựa chọn còn lại duy nhất là $firstpos(cur)$, chắc chắn quá lớn)

Vì vậy, đáp án cho một truy vấn chỉ là $firstpos(t) - length(P) + 1$, trong đó $t$ là trạng thái tương ứng với xâu $P$.
Mỗi truy vấn vẫn chỉ tốn $O(length(P))$ thời gian.

### Tất cả vị trí xuất hiện

Lần này ta cần in ra mọi vị trí xuất hiện trong xâu $T$.

Ta lại xây Suffix Automaton cho văn bản $T$.
Tương tự bài trước, ta tính vị trí $firstpos$ cho mọi trạng thái.

Rõ ràng $firstpos(t)$ thuộc đáp án nếu $t$ là trạng thái tương ứng với xâu truy vấn $P$.
Như vậy ta đã xét trạng thái của automaton chứa $P$.
Còn phải xét những trạng thái nào khác?
Đó là mọi trạng thái tương ứng với các xâu mà $P$ là hậu tố.
Nói cách khác, ta cần tìm tất cả trạng thái có thể đi tới trạng thái $t$ qua các liên kết hậu tố.

Do đó, để giải bài toán, ta cần lưu với mỗi trạng thái danh sách các liên kết hậu tố dẫn tới nó.
Đáp án truy vấn sẽ gồm mọi $firstpos$ của các trạng thái tìm được bằng DFS / BFS bắt đầu từ trạng thái $t$ và chỉ đi theo các liên kết hậu tố ngược.

Tổng thể, tiền xử lý tốn $O(length (T))$, còn mỗi truy vấn tốn $O(length(P) + answer(P))$, trong đó $answer(P)$ — là kích thước đáp án.

Đầu tiên, ta đi trong automaton theo từng ký tự của mẫu để tìm nút bắt đầu, tốn $O(length(P))$. Sau đó, cách duyệt phía trên chạy trong $O(answer(P))$, vì không trạng thái nào bị thăm hai lần (mỗi trạng thái chỉ có một liên kết hậu tố đi ra, nên không thể có hai đường khác nhau dẫn tới cùng một trạng thái theo cây liên kết ngược).

Ta chỉ cần lưu ý rằng hai trạng thái khác nhau có thể có cùng giá trị $firstpos$.
Điều này xảy ra nếu một trạng thái được tạo bằng cách clone trạng thái khác.
Tuy nhiên, điều này không làm hỏng độ phức tạp vì mỗi trạng thái có nhiều nhất một clone.

Hơn nữa, ta có thể loại các vị trí trùng bằng cách không in vị trí từ các trạng thái clone.
Thực tế, trạng thái mà một trạng thái clone có thể đi tới cũng có thể được đi tới từ trạng thái gốc.
Vì vậy, nếu lưu cờ `is_cloned` cho mỗi trạng thái, ta chỉ việc bỏ qua các trạng thái clone và chỉ in $firstpos$ của các trạng thái còn lại.

Một số phác thảo cài đặt:

```cpp
struct state {
    ...
    bool is_clone;
    int first_pos;
    vector<int> inv_link;
};

// after constructing the automaton
for (int v = 1; v < sz; v++) {
    st[st[v].link].inv_link.push_back(v);
}

// output all positions of occurrences
void output_all_occurrences(int v, int P_length) {
    if (!st[v].is_clone)
        cout << st[v].first_pos - P_length + 1 << endl;
    for (int u : st[v].inv_link)
        output_all_occurrences(u, P_length);
}
```

### Xâu ngắn nhất không xuất hiện

Cho một xâu $S$ và một bảng chữ cái xác định.
Ta cần tìm xâu có độ dài nhỏ nhất không xuất hiện trong $S$.

Ta dùng quy hoạch động trên Suffix Automaton xây cho xâu $S$.

Gọi $d[v]$ là đáp án tại nút $v$: ta đã xử lý một phần xâu con, hiện ở trạng thái $v$, và muốn tìm số ký tự ít nhất cần thêm để gặp một phép chuyển không tồn tại.
Việc tính $d[v]$ rất đơn giản.
Nếu thiếu phép chuyển theo ít nhất một ký tự của bảng chữ cái thì $d[v] = 1$.
Nếu không, một ký tự là chưa đủ, nên ta lấy giá trị nhỏ nhất trong đáp án của mọi phép chuyển:

$$d[v] = 1 + \min_{w:(v,w,c) \in SA} d[w].$$

Đáp án của bài toán là $d[t_0]$, và xâu cụ thể có thể được khôi phục từ mảng $d[]$ đã tính.

### Xâu con chung dài nhất của hai xâu

Cho hai xâu $S$ và $T$.
Ta cần tìm xâu con chung dài nhất, tức một xâu $X$ xuất hiện như xâu con trong cả $S$ và $T$.

Ta xây Suffix Automaton cho xâu $S$.

Tiếp theo, duyệt xâu $T$ và với mỗi tiền tố tìm hậu tố dài nhất của tiền tố đó xuất hiện trong $S$.
Nói cách khác, với mỗi vị trí trong xâu $T$, ta muốn tìm xâu con chung dài nhất của $S$ và $T$ kết thúc tại vị trí đó.

Ta dùng hai biến: **trạng thái hiện tại** $v$ và **độ dài hiện tại** $l$.
Hai biến này mô tả phần đang khớp: độ dài và trạng thái tương ứng.

Ban đầu $v = t_0$ và $l = 0$, tức phần khớp rỗng.

Bây giờ xét cách thêm ký tự $T[i]$ và tính lại đáp án:

  - Nếu có phép chuyển từ $v$ theo ký tự $T[i]$, ta chỉ cần đi theo phép chuyển và tăng $l$ thêm một.
  - Nếu không có phép chuyển như vậy, ta phải rút ngắn phần đang khớp, tức đi theo liên kết hậu tố: $v = link(v)$.
    Đồng thời, độ dài hiện tại cũng phải giảm.
    Rõ ràng ta cần đặt $l = len(v)$, vì sau khi đi theo liên kết hậu tố, ta tới trạng thái mà xâu dài nhất tương ứng là một xâu con.
  - Nếu vẫn chưa có phép chuyển theo ký tự cần thiết, ta tiếp tục lặp: đi theo liên kết hậu tố và giảm $l$ cho đến khi tìm thấy phép chuyển hoặc tới trạng thái giả $-1$ (nghĩa là ký tự $T[i]$ hoàn toàn không xuất hiện trong $S$, khi đó đặt $v = l = 0$).

Đáp án là giá trị lớn nhất trong mọi giá trị $l$.

Độ phức tạp của phần này là $O(length(T))$, vì mỗi bước hoặc tăng $l$ thêm một, hoặc đi nhiều lần theo liên kết hậu tố, mà mỗi lần như vậy đều làm giảm $l$.

Cài đặt:

```cpp
string lcs (string S, string T) {
    sa_init();
    for (int i = 0; i < S.size(); i++)
        sa_extend(S[i]);
 
    int v = 0, l = 0, best = 0, bestpos = 0;
    for (int i = 0; i < T.size(); i++) {
        while (v && !st[v].next.count(T[i])) {
            v = st[v].link ;
            l = st[v].len;
        }
        if (st[v].next.count(T[i])) {
            v = st [v].next[T[i]];
            l++;
        }
        if (l > best) {
            best = l;
            bestpos = i;
        }
    }
    return T.substr(bestpos - best + 1, best);
} 
```

### Xâu con chung lớn nhất của nhiều xâu

Cho $k$ xâu $S_i$.
Ta cần tìm xâu con chung dài nhất, tức xâu $X$ xuất hiện như xâu con trong mọi xâu $S_i$.

Ta nối mọi xâu thành một xâu lớn $T$, ngăn cách các xâu bằng những ký tự đặc biệt $D_i$ (mỗi xâu dùng một ký tự riêng):

$$T = S_1 + D_1 + S_2 + D_2 + \dots + S_k + D_k.$$

Sau đó xây Suffix Automaton cho xâu $T$.

Bây giờ cần tìm một xâu trong automaton xuất hiện trong mọi xâu $S_i$; có thể làm bằng các ký tự đặc biệt đã thêm.
Lưu ý rằng nếu một xâu con nằm trong một xâu $S_j$, thì trong Suffix Automaton tồn tại một đường đi bắt đầu từ xâu con này, chứa ký tự $D_j$ và không chứa các ký tự khác $D_1, \dots, D_{j-1}, D_{j+1}, \dots, D_k$.

Vì vậy ta cần tính tính đạt được, cho biết với mỗi trạng thái của automaton và mỗi ký hiệu $D_i$ liệu có tồn tại một đường đi như vậy hay không.
Có thể tính dễ dàng bằng DFS hoặc BFS kết hợp quy hoạch động.
Sau đó, đáp án là xâu $longest(v)$ của trạng thái $v$ mà từ đó tồn tại các đường đi cho mọi ký tự đặc biệt.

## Bài tập

  - [CSES - Finding Patterns](https://cses.fi/problemset/task/2102)
  - [CSES - Counting Patterns](https://cses.fi/problemset/task/2103)
  - [CSES - String Matching](https://cses.fi/problemset/task/1753)
  - [CSES - Patterns Positions](https://cses.fi/problemset/task/2104)
  - [CSES - Distinct Substrings](https://cses.fi/problemset/task/2105)
  - [CSES - Word Combinations](https://cses.fi/problemset/task/1731)
  - [CSES - String Distribution](https://cses.fi/problemset/task/2110)
  - [AtCoder - K-th Substring](https://atcoder.jp/contests/abc097/tasks/arc097_a)
  - [SPOJ - SUBLEX](https://www.spoj.com/problems/SUBLEX/)
  - [Codeforces - Cyclical Quest](https://codeforces.com/problemset/problem/235/C)
  - [Codeforces - String](https://codeforces.com/contest/128/problem/B)