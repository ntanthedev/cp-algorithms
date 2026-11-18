---
tags:
  - Original
translation:
  source: algebra/continued-fractions.md
  source_commit: 011137d80287c0116e30a51704815fba9331be0f
  status: draft
  last_synced: 2026-11-17
---

<!--?title Continued fractions -->
# Liên phân số

**Liên phân số** là cách biểu diễn một số thực bằng một dãy hội tụ đặc biệt gồm các số hữu tỉ. Liên phân số hữu ích trong lập trình thi đấu vì dễ tính và có thể được sử dụng hiệu quả để tìm phép xấp xỉ hữu tỉ tốt nhất của số thực đã cho (trong số các phân số có mẫu không vượt quá một giá trị cho trước).

Ngoài ra, liên phân số có quan hệ chặt chẽ với thuật toán Euclid, nhờ đó hữu ích trong nhiều bài toán số học.

## Biểu diễn liên phân số

!!! info "Định nghĩa"
    Cho $a_0, a_1, \dots, a_k \in \mathbb Z$ và $a_1, a_2, \dots, a_k \geq 1$. Khi đó biểu thức

    $$r=a_0 + \frac{1}{a_1 + \frac{1}{\dots + \frac{1}{a_k}}},$$

    được gọi là **biểu diễn liên phân số** của số hữu tỉ $r$ và được viết ngắn gọn là $r=[a_0;a_1,a_2,\dots,a_k]$.

??? example
    Cho $r = \frac{5}{3}$. Có hai cách biểu diễn số này dưới dạng liên phân số:

    $$
    \begin{align}
    r = [1;1,1,1] &= 1+\frac{1}{1+\frac{1}{1+\frac{1}{1}}},\\
    r = [1;1,2] &= 1+\frac{1}{1+\frac{1}{2}}.
    \end{align}
    $$

Có thể chứng minh rằng mỗi số hữu tỉ có đúng $2$ cách biểu diễn dưới dạng liên phân số:

$$r = [a_0;a_1,\dots,a_k,1] = [a_0;a_1,\dots,a_k+1].$$

Hơn nữa, với $r=\frac{p}{q}$, độ dài $k$ của liên phân số như vậy được ước lượng là $k = O(\log \min(p, q))$.

Lý do sẽ trở nên rõ ràng khi ta xét chi tiết cách xây dựng liên phân số.

!!! info "Định nghĩa"
    Cho $a_0,a_1,a_2, \dots$ là một dãy số nguyên thỏa mãn $a_1, a_2, \dots \geq 1$. Đặt $r_k = [a_0; a_1, \dots, a_k]$. Khi đó biểu thức

    $$r = a_0 + \frac{1}{a_1 + \frac{1}{a_2+\dots}} = \lim\limits_{k \to \infty} r_k.$$

    được gọi là **biểu diễn liên phân số** của số vô tỉ $r$ và được viết ngắn gọn là $r = [a_0;a_1,a_2,\dots]$.

Lưu ý rằng với $r=[a_0;a_1,\dots]$ và số nguyên $k$, ta có $r+k = [a_0+k; a_1, \dots]$.

Một nhận xét quan trọng khác là $\frac{1}{r}=[0;a_0, a_1, \dots]$ khi $a_0 > 0$ và $\frac{1}{r} = [a_1; a_2, \dots]$ khi $a_0 = 0$.

!!! info "Định nghĩa"
    Trong định nghĩa trên, các số hữu tỉ $r_0, r_1, r_2, \dots$ được gọi là các **phân số hội tụ** (convergents) của $r$.

    Tương ứng, mỗi $r_k = [a_0; a_1, \dots, a_k] = \frac{p_k}{q_k}$ được gọi là **phân số hội tụ** thứ $k$ của $r$.

??? example
    Xét $r = [1; 1, 1, 1, \dots]$. Có thể chứng minh bằng quy nạp rằng $r_k = \frac{F_{k+2}}{F_{k+1}}$, trong đó $F_k$ là dãy Fibonacci được xác định bởi $F_0 = 0$, $F_1 = 1$ và $F_{k} = F_{k-1} + F_{k-2}$. Từ công thức Binet, ta biết rằng

    $$r_k = \frac{\phi^{k+2} - \psi^{k+2}}{\phi^{k+1} - \psi^{k+1}},$$

    trong đó $\phi = \frac{1+\sqrt{5}}{2} \approx 1.618$ là tỉ lệ vàng và $\psi = \frac{1-\sqrt{5}}{2} = -\frac{1}{\phi} \approx -0.618$. Do đó,

    $$r = 1+\frac{1}{1+\frac{1}{1+\dots}}=\lim\limits_{k \to \infty} r_k = \phi = \frac{1+\sqrt{5}}{2}.$$

    Lưu ý rằng trong trường hợp cụ thể này, một cách khác để tìm $r$ là giải phương trình

    $$r = 1+\frac{1}{r} \implies r^2 = r + 1. $$


!!! info "Định nghĩa"
    Cho $r_k = [a_0; a_1, \dots, a_{k-1}, a_k]$. Các số $[a_0; a_1, \dots, a_{k-1}, t]$ với $1 \leq t \leq a_k$ được gọi là **bán hội tụ** (semiconvergents).

    Ta thường gọi các phân số (bán) hội tụ lớn hơn $r$ là phân số (bán) hội tụ **trên**, còn những phân số nhỏ hơn $r$ là phân số (bán) hội tụ **dưới**.

!!! info "Định nghĩa"
    Bên cạnh các phân số hội tụ, ta định nghĩa **[thương đầy đủ](https://en.wikipedia.org/wiki/Complete_quotient)** là $s_k = [a_k; a_{k+1}, a_{k+2}, \dots]$.

    Tương ứng, mỗi $s_k$ được gọi là thương đầy đủ thứ $k$ của $r$.

Từ các định nghĩa trên, ta suy ra $s_k \geq 1$ với $k \geq 1$.

Xem $[a_0; a_1, \dots, a_k]$ là một biểu thức đại số hình thức và cho phép $a_i$ nhận giá trị thực bất kỳ, ta được

$$r = [a_0; a_1, \dots, a_{k-1}, s_k].$$

Đặc biệt, $r = [s_0] = s_0$. Mặt khác, ta có thể biểu diễn $s_k$ dưới dạng

$$s_k = [a_k; s_{k+1}] = a_k + \frac{1}{s_{k+1}},$$

nghĩa là ta có thể tính $a_k = \lfloor s_k \rfloor$ và $s_{k+1} = (s_k - a_k)^{-1}$ từ $s_k$.

Dãy $a_0, a_1, \dots$ được xác định rõ trừ khi $s_k=a_k$, điều chỉ xảy ra khi $r$ là số hữu tỉ.

Do đó, biểu diễn liên phân số được xác định duy nhất với mọi số vô tỉ $r$.

### Cài đặt

Trong các đoạn mã, ta chủ yếu giả sử các liên phân số là hữu hạn.

Từ $s_k$, bước chuyển sang $s_{k+1}$ có dạng

$$s_k =\left\lfloor s_k \right\rfloor + \frac{1}{s_{k+1}}.$$

Từ biểu thức này, ta thu được thương đầy đủ tiếp theo $s_{k+1}$ là

$$s_{k+1} = \left(s_k-\left\lfloor s_k\right\rfloor\right)^{-1}.$$

Với $s_k=\frac{p}{q}$, điều đó có nghĩa là

$$
s_{k+1} = \left(\frac{p}{q}-\left\lfloor \frac{p}{q} \right\rfloor\right)^{-1} = \frac{q}{p-q\cdot \lfloor \frac{p}{q} \rfloor} = \frac{q}{p \bmod q}.
$$

Vì vậy, việc tính biểu diễn liên phân số của $r=\frac{p}{q}$ đi theo các bước của thuật toán Euclid đối với $p$ và $q$.

Từ đó cũng suy ra $\gcd(p_k, q_k) = 1$ với $\frac{p_k}{q_k} = [a_0; a_1, \dots, a_k]$. Do đó, các phân số hội tụ luôn tối giản.

=== "C++"
    ```cpp
    auto fraction(int p, int q) {
        vector<int> a;
        while(q) {
            a.push_back(p / q);
            tie(p, q) = make_pair(q, p % q);
        }
        return a;
    }
    ```
=== "Python"
    ```py
    def fraction(p, q):
        a = []
        while q:
            a.append(p // q)
            p, q = q, p % q
        return a
    ```

## Các kết quả chính

Để tạo động lực tìm hiểu sâu hơn về liên phân số, trước hết ta nêu một số kết quả quan trọng.

??? note "Công thức truy hồi"
    Các phân số hội tụ $r_k = \frac{p_k}{q_k}$ thỏa mãn công thức truy hồi sau, cho phép tính chúng nhanh chóng:

    $$\frac{p_k}{q_k}=\frac{a_k p_{k-1} + p_{k-2}}{a_k q_{k-1} + q_{k-2}},$$

    trong đó $\frac{p_{-1}}{q_{-1}}=\frac{1}{0}$ và $\frac{p_{-2}}{q_{-2}}=\frac{0}{1}$.

??? note "Sai lệch"
    Nhìn chung, sai lệch giữa $r_k = \frac{p_k}{q_k}$ và $r$ có thể được ước lượng như sau:

    $$\left|\frac{p_k}{q_k}-r\right| \leq \frac{1}{q_k q_{k+1}} \leq \frac{1}{q_k^2}.$$

    Nhân hai vế với $q_k$, ta được một ước lượng khác:

    $$|p_k - q_k r| \leq \frac{1}{q_{k+1}}.$$

    Từ công thức truy hồi trên, suy ra $q_k$ tăng ít nhất nhanh bằng các số Fibonacci.

    Hình dưới đây minh họa cách các phân số hội tụ $r_k$ tiến gần tới $r=\frac{1+\sqrt 5}{2}$:

    ![](https://upload.wikimedia.org/wikipedia/commons/b/b4/Golden_ration_convergents.svg)

    $r=\frac{1+\sqrt 5}{2}$ được biểu diễn bằng đường nét đứt màu xanh. Các phân số hội tụ có chỉ số lẻ tiến gần từ phía trên và các phân số có chỉ số chẵn tiến gần từ phía dưới.

??? note "Bao lồi điểm nguyên"
    Xét bao lồi của các điểm phía trên và phía dưới đường thẳng $y=rx$.

    Các phân số hội tụ chỉ số lẻ $(q_k;p_k)$ là các đỉnh của bao lồi trên, còn các phân số chỉ số chẵn $(q_k;p_k)$ là các đỉnh của bao lồi dưới.

    Tất cả các đỉnh nguyên trên những bao lồi này có dạng $(q;p)$ sao cho

    $$\frac{p}{q} = \frac{tp_{k-1} + p_{k-2}}{tq_{k-1} + q_{k-2}}$$

    với số nguyên $0 \leq t \leq a_k$. Nói cách khác, tập các điểm nguyên trên bao lồi tương ứng với tập các bán hội tụ.

    Hình dưới đây thể hiện các phân số hội tụ và bán hội tụ (các điểm màu xám ở giữa) của $r=\frac{9}{7}$.

    ![](https://upload.wikimedia.org/wikipedia/commons/9/92/Continued_convergents_geometry.svg)

??? note "Xấp xỉ tốt nhất"
    Cho $\frac{p}{q}$ là phân số làm cực tiểu $\left|r-\frac{p}{q}\right|$ với điều kiện $q \leq x$ cho một giá trị $x$ nào đó.

    Khi đó $\frac{p}{q}$ là một bán hội tụ của $r$.

Kết quả cuối cùng cho phép tìm các xấp xỉ hữu tỉ tốt nhất của $r$ bằng cách kiểm tra các bán hội tụ của nó.

Dưới đây là phần giải thích chi tiết hơn, cùng một số trực giác và cách diễn giải những kết quả này.

## Phân số hội tụ

Hãy xét kỹ hơn các phân số hội tụ đã được định nghĩa ở trên. Với $r=[a_0, a_1, a_2, \dots]$, các phân số hội tụ của nó là

\begin{gather}
r_0=[a_0],\\r_1=[a_0, a_1],\\ \dots,\\ r_k=[a_0, a_1, \dots, a_k].
\end{gather}

Phân số hội tụ là khái niệm cốt lõi của liên phân số, vì vậy việc nghiên cứu các tính chất của chúng rất quan trọng.

Với số $r$, phân số hội tụ thứ $k$ của nó là $r_k = \frac{p_k}{q_k}$ có thể được tính bằng

$$r_k = \frac{P_k(a_0,a_1,\dots,a_k)}{P_{k-1}(a_1,\dots,a_k)} = \frac{a_k p_{k-1} + p_{k-2}}{a_k q_{k-1} + q_{k-2}},$$

trong đó $P_k(a_0,\dots,a_k)$ là [continuant](https://en.wikipedia.org/wiki/Continuant_(mathematics)), một đa thức nhiều biến được định nghĩa bởi

$$P_k(x_0,x_1,\dots,x_k) = \det \begin{bmatrix}
x_k & 1 & 0 & \dots & 0 \\
-1 & x_{k-1} & 1 & \dots & 0 \\
0 & -1 & x_2 & . & \vdots \\
\vdots & \vdots & . & \ddots & 1 \\
0 & 0 & \dots & -1 & x_0
\end{bmatrix}_{\textstyle .}$$

Do đó, $r_k$ là [phân số trung gian](https://en.wikipedia.org/wiki/Mediant_(mathematics)) (mediant) có trọng số của $r_{k-1}$ và $r_{k-2}$.

Để thống nhất, ta định nghĩa thêm hai phân số hội tụ $r_{-1} = \frac{1}{0}$ và $r_{-2} = \frac{0}{1}$.

??? hint "Giải thích chi tiết"

    Tử số và mẫu số của $r_k$ có thể được xem là các đa thức nhiều biến theo $a_0, a_1, \dots, a_k$:

    $$r_k = \frac{P_k(a_0, a_1, \dots, a_k)}{Q_k(a_0,a_1, \dots, a_k)}.$$

    Theo định nghĩa của phân số hội tụ,

    $$r_k = a_0 + \frac{1}{[a_1;a_2,\dots, a_k]}= a_0 + \frac{Q_{k-1}(a_1, \dots, a_k)}{P_{k-1}(a_1, \dots, a_k)} = \frac{a_0 P_{k-1}(a_1, \dots, a_k) + Q_{k-1}(a_1, \dots, a_k)}{P_{k-1}(a_1, \dots, a_k)}.$$

    Từ đây suy ra $Q_k(a_0, \dots, a_k) = P_{k-1}(a_1, \dots, a_k)$. Điều này cho ta hệ thức

    $$P_k(a_0, \dots, a_k) = a_0 P_{k-1}(a_1, \dots, a_k) + P_{k-2}(a_2, \dots, a_k).$$

    Ban đầu, $r_0 = \frac{a_0}{1}$ và $r_1 = \frac{a_0 a_1 + 1}{a_1}$, do đó

    $$\begin{align}P_0(a_0)&=a_0,\\ P_1(a_0, a_1) &= a_0 a_1 + 1.\end{align}$$

    Để thống nhất, ta có thể định nghĩa $P_{-1} = 1$ và $P_{-2}=0$, đồng thời viết một cách hình thức rằng $r_{-1} = \frac{1}{0}$ và $r_{-2}=\frac{0}{1}$.

    Trong giải tích số, ta biết rằng định thức của một ma trận ba đường chéo bất kỳ

    $$T_k = \det \begin{bmatrix}
    a_0 & b_0 & 0 & \dots & 0 \\
    c_0 & a_1 & b_1 & \dots & 0 \\
    0 & c_1 & a_2 & . & \vdots \\
    \vdots & \vdots & . & \ddots & c_{k-1} \\
    0 & 0 & \dots & b_{k-1} & a_k
    \end{bmatrix}$$

    có thể được tính theo truy hồi $T_k = a_k T_{k-1} - b_{k-1} c_{k-1} T_{k-2}$. So sánh với $P_k$, ta có biểu thức trực tiếp

    $$P_k = \det \begin{bmatrix}
    x_k & 1 & 0 & \dots & 0 \\
    -1 & x_{k-1} & 1 & \dots & 0 \\
    0 & -1 & x_2 & . & \vdots \\
    \vdots & \vdots & . & \ddots & 1 \\
    0 & 0 & \dots & -1 & x_0
    \end{bmatrix}_{\textstyle .}$$

    Đa thức này còn được gọi là [continuant](https://en.wikipedia.org/wiki/Continuant_(mathematics)) do có quan hệ chặt chẽ với liên phân số. Giá trị của nó không đổi nếu đảo ngược dãy trên đường chéo chính. Từ đó ta có một công thức khác để tính:

    $$P_k(a_0, \dots, a_k) = a_k P_{k-1}(a_0, \dots, a_{k-1}) + P_{k-2}(a_0, \dots, a_{k-2}).$$

### Cài đặt

Ta sẽ tính các phân số hội tụ dưới dạng một cặp dãy $p_{-2}, p_{-1}, p_0, p_1, \dots, p_k$ và $q_{-2}, q_{-1}, q_0, q_1, \dots, q_k$:

=== "C++"
    ```cpp
    auto convergents(vector<int> a) {
        vector<int> p = {0, 1};
        vector<int> q = {1, 0};
        for(auto it: a) {
            p.push_back(p[p.size() - 1] * it + p[p.size() - 2]);
            q.push_back(q[q.size() - 1] * it + q[q.size() - 2]);
        }
        return make_pair(p, q);
    }
    ```
=== "Python"
    ```py
    def convergents(a):
        p = [0, 1]
        q = [1, 0]
        for it in a:
            p.append(p[-1]*it + p[-2])
            q.append(q[-1]*it + q[-2])
        return p, q
    ```

## Các cây liên phân số

Có hai cách chính để tập hợp tất cả các liên phân số vào những cấu trúc cây hữu ích.

### Cây Stern-Brocot

[Cây Stern-Brocot](../others/stern_brocot_tree_farey_sequences.md) là một cây tìm kiếm nhị phân chứa tất cả các số hữu tỉ dương phân biệt.

Cây có dạng tổng quát như sau:

<figure>
<img src="https://upload.wikimedia.org/wikipedia/commons/3/37/SternBrocotTree.svg">
<figcaption>
<a href="https://commons.wikimedia.org/wiki/File:SternBrocotTree.svg">Hình ảnh</a> của <a href="https://commons.wikimedia.org/wiki/User:Aaron_Rotenberg">Aaron Rotenberg</a> được cấp phép theo <a href="https://creativecommons.org/licenses/by-sa/3.0/deed.en">CC BY-SA 3.0</a>
</figcaption>
</figure>

Các phân số $\frac{0}{1}$ và $\frac{1}{0}$ được giữ "ảo" tương ứng ở phía trái và phía phải của cây.

Khi đó, phân số tại một nút là phân số trung gian $\frac{a+c}{b+d}$ của hai phân số $\frac{a}{b}$ và $\frac{c}{d}$ ở phía trên nút đó.

Công thức truy hồi $\frac{p_k}{q_k}=\frac{a_k p_{k-1} + p_{k-2}}{a_k q_{k-1} + q_{k-2}}$ cho thấy biểu diễn liên phân số mã hóa đường đi đến $\frac{p_k}{q_k}$ trong cây. Để tìm $[a_0; a_1, \dots, a_{k}, 1]$, ta cần đi $a_0$ bước sang phải, $a_1$ bước sang trái, $a_2$ bước sang phải và tiếp tục như vậy đến $a_k$.

Khi đó, nút cha của $[a_0; a_1, \dots, a_k,1]$ là phân số thu được bằng cách lùi một bước theo hướng vừa đi cuối cùng.

Nói cách khác, đó là $[a_0; a_1, \dots, a_k-1,1]$ khi $a_k > 1$ và $[a_0; a_1, \dots, a_{k-1}, 1]$ khi $a_k = 1$.

Vì vậy, các nút con của $[a_0; a_1, \dots, a_k, 1]$ là $[a_0; a_1, \dots, a_k+1, 1]$ và $[a_0; a_1, \dots, a_k, 1, 1]$.

Hãy đánh chỉ số các nút của cây Stern-Brocot. Gốc được gán chỉ số $1$. Với một nút $v$, chỉ số của con trái được xác định bằng cách thay bit đầu của $v$ từ $1$ thành $10$, còn chỉ số của con phải được xác định bằng cách thay bit đầu từ $1$ thành $11$:

<figure><img src="https://upload.wikimedia.org/wikipedia/commons/1/18/Stern-brocot-index.svg" width="500px"/></figure>

Với cách đánh chỉ số này, biểu diễn liên phân số của một số hữu tỉ cho biết [mã hóa độ dài loạt](https://en.wikipedia.org/wiki/Run-length_encoding) (run-length encoding) của chỉ số nhị phân tương ứng.

Với $\frac{5}{2} = [2;2] = [2;1,1]$, chỉ số là $1011_2$ và mã hóa độ dài loạt, xét các bit theo thứ tự tăng dần, là $[2;1,1]$.

Một ví dụ khác là $\frac{2}{5} = [0;2,2]=[0;2,1,1]$, có chỉ số $1100_2$ và mã hóa độ dài loạt đúng là $[0;2,2]$.

Thực ra cây Stern-Brocot là một [treap](../data_structures/treap.md): nó là cây tìm kiếm nhị phân theo $\frac{p}{q}$, đồng thời là heap theo cả $p$ lẫn $q$.

!!! example "So sánh các liên phân số"
    Cho $A=[a_0; a_1, \dots, a_n]$ và $B=[b_0; b_1, \dots, b_m]$. Phân số nào nhỏ hơn?
??? hint "Lời giải"
    Trước hết, giả sử $A$ và $B$ là số vô tỉ và các biểu diễn liên phân số của chúng chỉ một đường đi xuống vô hạn trong cây Stern-Brocot.

    Như đã nói, trong biểu diễn này $a_0$ là số lần rẽ phải trên đường đi xuống, $a_1$ là số lần rẽ trái liên tiếp tiếp theo, v.v. Do đó, khi so sánh $a_k$ và $b_k$, nếu $a_k = b_k$ thì ta tiếp tục so sánh $a_{k+1}$ và $b_{k+1}$. Ngược lại, để xác định $A < B$, ta kiểm tra $a_k < b_k$ nếu đang đi sang phải, hoặc $a_k > b_k$ nếu đang đi sang trái.

    Nói cách khác, với $A$ và $B$ vô tỉ, $A < B$ khi và chỉ khi $(a_0, -a_1, a_2, -a_3, \dots) < (b_0, -b_1, b_2, -b_3, \dots)$ theo thứ tự từ điển.

    Bây giờ, bằng cách dùng $\infty$ một cách hình thức như một phần tử trong biểu diễn liên phân số, ta có thể mô phỏng các số vô tỉ $A-\varepsilon$ và $A+\varepsilon$, tức là những phần tử nhỏ hơn (lớn hơn) $A$ nhưng lớn hơn (nhỏ hơn) mọi số thực khác. Cụ thể, với $A=[a_0; a_1, \dots, a_n]$, một trong hai phần tử này có thể được mô phỏng bằng $[a_0; a_1, \dots, a_n, \infty]$ và phần tử còn lại bằng $[a_0; a_1, \dots, a_n - 1, 1, \infty]$.

    Ta có thể xác định phần tử nào tương ứng với $A-\varepsilon$, phần tử nào tương ứng với $A+\varepsilon$ dựa vào tính chẵn lẻ của $n$ hoặc bằng cách so sánh chúng như các số vô tỉ.

    === "Python"
        ```py
        # check if a < b assuming that a[-1] = b[-1] = infty and a != b
        def less(a, b):
            a = [(-1)**i*a[i] for i in range(len(a))]
            b = [(-1)**i*b[i] for i in range(len(b))]
            return a < b

        # [a0; a1, ..., ak] -> [a0, a1, ..., ak-1, 1]
        def expand(a):
            if a: # empty a = inf
                a[-1] -= 1
                a.append(1)
            return a

        # return a-eps, a+eps
        def pm_eps(a):
            b = expand(a.copy())
            a.append(float('inf'))
            b.append(float('inf'))
            return (a, b) if less(a, b) else (b, a)
        ```

!!! example "Điểm trong tốt nhất"
    Cho $\frac{0}{1} \leq \frac{p_0}{q_0} < \frac{p_1}{q_1} \leq \frac{1}{0}$. Tìm số hữu tỉ $\frac{p}{q}$ sao cho $(q; p)$ nhỏ nhất theo thứ tự từ điển và $\frac{p_0}{q_0} < \frac{p}{q} < \frac{p_1}{q_1}$.

??? hint "Lời giải"
    Theo cây Stern-Brocot, điều này có nghĩa là ta cần tìm tổ tiên chung gần nhất (LCA) của $\frac{p_0}{q_0}$ và $\frac{p_1}{q_1}$. Do mối liên hệ giữa cây Stern-Brocot và liên phân số, LCA này gần tương ứng với tiền tố chung dài nhất của các biểu diễn liên phân số của $\frac{p_0}{q_0}$ và $\frac{p_1}{q_1}$.

    Vì vậy, nếu $\frac{p_0}{q_0} = [a_0; a_1, \dots, a_{k-1}, a_k, \dots]$ và $\frac{p_1}{q_1} = [a_0; a_1, \dots, a_{k-1}, b_k, \dots]$ là các số vô tỉ thì LCA là $[a_0; a_1, \dots, \min(a_k, b_k)+1]$.

    Với $r_0$ và $r_1$ hữu tỉ, một trong hai có thể chính là LCA, buộc ta phải xét riêng trường hợp đó. Để đơn giản hóa lời giải cho $r_0$ và $r_1$ hữu tỉ, ta có thể dùng biểu diễn liên phân số của $r_0 + \varepsilon$ và $r_1 - \varepsilon$ đã được suy ra ở bài toán trước.

    === "Python"
        ```py
        # finds lexicographically smallest (q, p)
        # such that p0/q0 < p/q < p1/q1
        def middle(p0, q0, p1, q1):
            a0 = pm_eps(fraction(p0, q0))[1]
            a1 = pm_eps(fraction(p1, q1))[0]
            a = []
            for i in range(min(len(a0), len(a1))):
                a.append(min(a0[i], a1[i]))
                if a0[i] != a1[i]:
                    break
            a[-1] += 1
            p, q = convergents(a)
            return p[-1], q[-1]
        ```

!!! example "[GCJ 2019, Round 2 - New Elements: Part 2](https://codingcompetitions.withgoogle.com/codejam/round/0000000000051679/0000000000146184)"
    Cho $N$ cặp số nguyên dương $(C_i, J_i)$. Cần tìm một cặp số nguyên dương $(x, y)$ sao cho $C_i x + J_i y$ là một dãy tăng nghiêm ngặt.

    Trong các cặp như vậy, hãy tìm cặp nhỏ nhất theo thứ tự từ điển.
??? hint "Lời giải"
    Viết lại đề bài, $A_i x + B_i y$ phải dương với mọi $i$, trong đó $A_i = C_i - C_{i-1}$ và $B_i = J_i - J_{i-1}$.

    Với $A_i x + B_i y > 0$, ta có bốn nhóm đáng chú ý:

    1. Có thể bỏ qua $A_i, B_i > 0$ vì ta tìm $x, y > 0$.
    2. Với $A_i, B_i \leq 0$, câu trả lời là "IMPOSSIBLE".
    3. $A_i > 0$, $B_i \leq 0$. Các ràng buộc này tương đương với $\frac{y}{x} < \frac{A_i}{-B_i}$.
    4. $A_i \leq 0$, $B_i > 0$. Các ràng buộc này tương đương với $\frac{y}{x} > \frac{-A_i}{B_i}$.

    Gọi $\frac{p_0}{q_0}$ là giá trị $\frac{-A_i}{B_i}$ lớn nhất ở nhóm thứ tư và $\frac{p_1}{q_1}$ là giá trị $\frac{A_i}{-B_i}$ nhỏ nhất ở nhóm thứ ba.

    Bài toán giờ đây là, cho $\frac{p_0}{q_0} < \frac{p_1}{q_1}$, tìm phân số $\frac{p}{q}$ sao cho $(q;p)$ nhỏ nhất theo thứ tự từ điển và $\frac{p_0}{q_0} < \frac{p}{q} < \frac{p_1}{q_1}$.
    === "Python"
        ```py
            def solve():
            n = int(input())
            C = [0] * n
            J = [0] * n
            # p0/q0 < y/x < p1/q1
            p0, q0 = 0, 1
            p1, q1 = 1, 0
            fail = False
            for i in range(n):
                C[i], J[i] = map(int, input().split())
                if i > 0:
                    A = C[i] - C[i-1]
                    B = J[i] - J[i-1]
                    if A <= 0 and B <= 0:
                        fail = True
                    elif B > 0 and A < 0: # y/x > (-A)/B if B > 0
                        if (-A)*q0 > p0*B:
                            p0, q0 = -A, B
                    elif B < 0 and A > 0: # y/x < A/(-B) if B < 0
                        if A*q1 < p1*(-B):
                            p1, q1 = A, -B
            if p0*q1 >= p1*q0 or fail:
                return 'IMPOSSIBLE'

            p, q = middle(p0, q0, p1, q1)
            return str(q) + ' ' + str(p)
        ```

### Cây Calkin-Wilf

Một cách đơn giản hơn đôi chút để tổ chức các liên phân số thành cây nhị phân là [cây Calkin-Wilf](https://en.wikipedia.org/wiki/Calkin–Wilf_tree).

Cây có dạng tổng quát như sau:

<figure>
<img src="https://upload.wikimedia.org/wikipedia/commons/8/82/Calkin–Wilf_tree.svg" width="500px"/>
<figcaption><a href="https://commons.wikimedia.org/wiki/File:Calkin–Wilf_tree.svg">Hình ảnh</a> của <a href="https://commons.wikimedia.org/wiki/User:Olli_Niemitalo">Olli Niemitalo</a>, <a href="https://commons.wikimedia.org/wiki/User:Proz">Proz</a> được cấp phép theo <a href="https://creativecommons.org/publicdomain/zero/1.0/deed.en">CC0 1.0</a></figcaption>
</figure>

Tại gốc của cây là số $\frac{1}{1}$. Với nút mang số $\frac{p}{q}$, các nút con là $\frac{p}{p+q}$ và $\frac{p+q}{q}$.

Khác với cây Stern-Brocot, cây Calkin-Wilf không phải là cây _tìm kiếm_ nhị phân, vì vậy không thể dùng nó để tìm kiếm nhị phân trên các số hữu tỉ.

Trong cây Calkin-Wilf, nút cha trực tiếp của phân số $\frac{p}{q}$ là $\frac{p-q}{q}$ khi $p>q$ và là $\frac{p}{q-p}$ trong trường hợp còn lại.

Với cây Stern-Brocot, ta đã dùng công thức truy hồi của các phân số hội tụ. Để liên hệ liên phân số với cây Calkin-Wilf, hãy nhớ lại công thức truy hồi của các thương đầy đủ. Nếu $s_k = \frac{p}{q}$ thì $s_{k+1} = \frac{q}{p \mod q} = \frac{q}{p-\lfloor p/q \rfloor \cdot q}$.

Mặt khác, nếu liên tiếp đi từ $s_k = \frac{p}{q}$ lên nút cha trong cây Calkin-Wilf khi $p > q$, ta sẽ đến $\frac{p \mod q}{q} = \frac{1}{s_{k+1}}$. Tiếp tục như vậy, ta sẽ đến $s_{k+2}$, rồi $\frac{1}{s_{k+3}}$, v.v. Từ đó ta suy ra:

1. Khi $a_0> 0$, nút cha trực tiếp của $[a_0; a_1, \dots, a_k]$ trong cây Calkin-Wilf là $\frac{p-q}{q}=[a_0 - 1; a_1, \dots, a_k]$.
2. Khi $a_0 = 0$ và $a_1 > 1$, nút cha trực tiếp là $\frac{p}{q-p} = [0; a_1 - 1, a_2, \dots, a_k]$.
3. Khi $a_0 = 0$ và $a_1 = 1$, nút cha trực tiếp là $\frac{p}{q-p} = [a_2; a_3, \dots, a_k]$.

Tương ứng, các nút con của $\frac{p}{q} = [a_0; a_1, \dots, a_k]$ là

1. $\frac{p+q}{q}=1+\frac{p}{q}$, tức $[a_0+1; a_1, \dots, a_k]$,
2. $\frac{p}{p+q} = \frac{1}{1+\frac{q}{p}}$, tức $[0, 1, a_0, a_1, \dots, a_k]$ với $a_0 > 0$ và $[0, a_1+1, a_2, \dots, a_k]$ với $a_0=0$.

Nếu đánh số các nút của cây Calkin-Wilf theo thứ tự tìm kiếm theo chiều rộng (nghĩa là gốc có số $1$, và các con của nút $v$ có chỉ số tương ứng là $2v$ và $2v+1$), thì chỉ số của mỗi số hữu tỉ trong cây Calkin-Wilf sẽ giống với trong cây Stern-Brocot.

Do đó, các số ở cùng một mức trong cây Stern-Brocot và cây Calkin-Wilf là như nhau, nhưng thứ tự của chúng khác nhau theo [hoán vị đảo bit](https://en.wikipedia.org/wiki/Bit-reversal_permutation).
## Sự hội tụ

Với số $r$ và phân số hội tụ thứ $k$ của nó là $r_k=\frac{p_k}{q_k}$, ta có công thức:

$$r_k = a_0 + \sum\limits_{i=1}^k \frac{(-1)^{i-1}}{q_i q_{i-1}}.$$

Đặc biệt, điều đó có nghĩa là

$$r_k - r_{k-1} = \frac{(-1)^{k-1}}{q_k q_{k-1}}$$

và

$$p_k q_{k-1} - p_{k-1} q_k = (-1)^{k-1}.$$

Từ đây ta có thể kết luận rằng

$$\left| r-\frac{p_k}{q_k} \right| \leq \frac{1}{q_{k+1}q_k} \leq \frac{1}{q_k^2}.$$

Bất đẳng thức sau cùng có được vì $r_k$ và $r_{k+1}$ thường nằm ở hai phía khác nhau của $r$, do đó

$$|r-r_k| = |r_k-r_{k+1}|-|r-r_{k+1}| \leq |r_k - r_{k+1}|.$$

??? tip "Giải thích chi tiết"

    Để ước lượng $|r-r_k|$, ta bắt đầu bằng cách ước lượng hiệu giữa hai phân số hội tụ liên tiếp. Theo định nghĩa,

    $$\frac{p_k}{q_k} - \frac{p_{k-1}}{q_{k-1}} = \frac{p_k q_{k-1} - p_{k-1} q_k}{q_k q_{k-1}}.$$

    Thay $p_k$ và $q_k$ trong tử số bằng công thức truy hồi của chúng, ta được

    $$\begin{align} p_k q_{k-1} - p_{k-1} q_k &= (a_k p_{k-1} + p_{k-2}) q_{k-1} - p_{k-1} (a_k q_{k-1} + q_{k-2})
    \\&= p_{k-2} q_{k-1} - p_{k-1} q_{k-2},\end{align}$$

    do đó tử số của $r_k - r_{k-1}$ luôn là số đối của tử số của $r_{k-1} - r_{k-2}$. Tử số này bằng $1$ trong trường hợp

    $$r_1 - r_0=\left(a_0+\frac{1}{a_1}\right)-a_0=\frac{1}{a_1},$$

    do đó

    $$r_k - r_{k-1} = \frac{(-1)^{k-1}}{q_k q_{k-1}}.$$

    Từ đây ta có một cách biểu diễn khác của $r_k$ dưới dạng tổng riêng của một chuỗi vô hạn:

    $$r_k = (r_k - r_{k-1}) + \dots + (r_1 - r_0) + r_0
    = a_0 + \sum\limits_{i=1}^k \frac{(-1)^{i-1}}{q_i q_{i-1}}.$$

    Từ hệ thức truy hồi suy ra $q_k$ tăng đơn điệu ít nhất nhanh bằng các số Fibonacci, do đó

    $$r = \lim\limits_{k \to \infty} r_k = a_0 + \sum\limits_{i=1}^\infty \frac{(-1)^{i-1}}{q_i q_{i-1}}$$

    luôn được xác định rõ, vì chuỗi tương ứng luôn hội tụ. Đáng chú ý, chuỗi dư

    $$r-r_k = \sum\limits_{i=k+1}^\infty \frac{(-1)^{i-1}}{q_i q_{i-1}}$$

    có cùng dấu với $(-1)^k$ do tốc độ giảm của $q_i q_{i-1}$. Vì vậy, $r_k$ có chỉ số chẵn tiến đến $r$ từ phía dưới, còn $r_k$ có chỉ số lẻ tiến đến từ phía trên:

    <figure><img src="https://upload.wikimedia.org/wikipedia/commons/b/b4/Golden_ration_convergents.svg" width="600px"/>
    <figcaption>_Các phân số hội tụ của $r=\phi = \frac{1+\sqrt{5}}{2}=[1;1,1,\dots]$ và khoảng cách từ chúng đến $r$._</figcaption></figure>

    Từ hình này ta thấy rằng

    $$|r-r_k| = |r_k - r_{k+1}| - |r-r_{k+1}| \leq |r_k - r_{k+1}|,$$

    do đó khoảng cách giữa $r$ và $r_k$ không bao giờ lớn hơn khoảng cách giữa $r_k$ và $r_{k+1}$:

    $$\left|r-\frac{p_k}{q_k}\right| \leq \frac{1}{q_k q_{k+1}} \leq \frac{1}{q_k^2}.$$

!!! example "Euclid mở rộng?"
    Cho $A, B, C \in \mathbb Z$. Tìm $x, y \in \mathbb Z$ sao cho $Ax + By = C$.
??? hint "Lời giải"
    Mặc dù bài toán này thường được giải bằng [thuật toán Euclid mở rộng](../algebra/extended-euclid-algorithm.md), cũng có một lời giải đơn giản và trực tiếp bằng liên phân số.

    Đặt $\frac{A}{B}=[a_0; a_1, \dots, a_k]$. Ở trên ta đã chứng minh $p_k q_{k-1} - p_{k-1} q_k = (-1)^{k-1}$. Thay $p_k$ và $q_k$ bằng $A$ và $B$, ta được

    $$Aq_{k-1} - Bp_{k-1} = (-1)^{k-1} g,$$

    trong đó $g = \gcd(A, B)$. Nếu $C$ chia hết cho $g$, một nghiệm là $x = (-1)^{k-1}\frac{C}{g} q_{k-1}$ và $y = (-1)^{k}\frac{C}{g} p_{k-1}$.
    
    === "Python"
        ```py
        # return (x, y) such that Ax+By=C
        # assumes that such (x, y) exists
        def dio(A, B, C):
            p, q = convergents(fraction(A, B))
            C //= A // p[-1] # divide by gcd(A, B)
            t = (-1) if len(p) % 2 else 1
            return t*C*q[-2], -t*C*p[-2]
        ```

## Phép biến đổi phân tuyến tính

Một khái niệm quan trọng khác đối với liên phân số là các [phép biến đổi phân tuyến tính](https://en.wikipedia.org/wiki/Linear_fractional_transformation).

!!! info "Định nghĩa"
    Một **phép biến đổi phân tuyến tính** là hàm $f : \mathbb R \to \mathbb R$ sao cho $f(x) = \frac{ax+b}{cx+d}$ với một số $a,b,c,d \in \mathbb R$.

Hợp $(L_0 \circ L_1)(x) = L_0(L_1(x))$ của hai phép biến đổi phân tuyến tính $L_0(x)=\frac{a_0 x + b_0}{c_0 x + d_0}$ và $L_1(x)=\frac{a_1 x + b_1}{c_1 x + d_1}$ cũng là một phép biến đổi phân tuyến tính:

$$\frac{a_0\frac{a_1 x + b_1}{c_1 x + d_1} + b_0}{c_0 \frac{a_1 x + b_1}{c_1 x + d_1} + d_0} = \frac{a_0(a_1 x + b_1) + b_0 (c_1 x + d_1)}{c_0 (a_1 x + b_1) + d_0 (c_1 x + d_1)} = \frac{(a_0 a_1 + b_0 c_1) x + (a_0 b_1 + b_0 d_1)}{(c_0 a_1 + d_0 c_1) x + (c_0 b_1 + d_0 d_1)}.$$

Phép biến đổi ngược của một phép biến đổi phân tuyến tính cũng là một phép biến đổi phân tuyến tính:

$$y = \frac{ax+b}{cx+d} \iff y(cx+d) = ax + b \iff x = -\frac{dy-b}{cy-a}.$$
!!! example "[DMOPC '19 Contest 7 P4 - Bob and Continued Fractions](https://dmoj.ca/problem/dmopc19c7p4)"
    Cho một mảng các số nguyên dương $a_1, \dots, a_n$. Cần trả lời $m$ truy vấn; mỗi truy vấn yêu cầu tính $[a_l; a_{l+1}, \dots, a_r]$.
??? hint "Lời giải"
    Ta có thể giải bài toán bằng cây đoạn nếu có thể nối các liên phân số.

    Nói chung, ta có $[a_0; a_1, \dots, a_k, b_0, b_1, \dots, b_k] = [a_0; a_1, \dots, a_k, [b_1; b_2, \dots, b_k]]$.

    Đặt $L_{k}(x) = [a_k; x] = a_k + \frac{1}{x} = \frac{a_k\cdot x+1}{1\cdot x + 0}$. Lưu ý $L_k(\infty) = a_k$. Với ký hiệu này, ta có

    $$[a_0; a_1, \dots, a_k, x] = [a_0; [a_1; [\dots; [a_k; x]]]] = (L_0 \circ L_1 \circ \dots \circ L_k)(x) = \frac{p_k x + p_{k-1}}{q_k x + q_{k-1}}.$$

    Do đó, bài toán quy về việc tính

    $$(L_l \circ L_{l+1} \circ \dots \circ L_r)(\infty).$$

    Phép hợp các biến đổi có tính kết hợp, nên tại mỗi nút của cây đoạn ta có thể tính hợp các biến đổi trong cây con của nó.

!!! example "Biến đổi phân tuyến tính của một liên phân số"
    Cho $L(x) = \frac{ax+b}{cx+d}$. Tính biểu diễn liên phân số $[b_0; b_1, \dots, b_m]$ của $L(A)$ với $A=[a_0; a_1, \dots, a_n]$.

    _Điều này cho phép tính $A + \frac{p}{q} = \frac{qA + p}{q}$ và $A \cdot \frac{p}{q} = \frac{p A}{q}$ với mọi $\frac{p}{q}$._

??? hint "Lời giải"
    Như đã thấy ở trên, $[a_0; a_1, \dots, a_k] = (L_{a_0} \circ L_{a_1} \circ \dots \circ L_{a_k})(\infty)$, do đó $L([a_0; a_1, \dots, a_k]) = (L \circ L_{a_0} \circ L_{a_1} \circ \dots L_{a_k})(\infty)$.

    Vì vậy, bằng cách lần lượt thêm $L_{a_0}$, $L_{a_1}$, v.v., ta có thể tính

    $$(L \circ L_{a_0} \circ \dots \circ L_{a_k})(x) = L\left(\frac{p_k x + p_{k-1}}{q_k x + q_{k-1}}\right)=\frac{a_k x + b_k}{c_k x + d_k}.$$

    Vì $L(x)$ khả nghịch nên nó cũng đơn điệu theo $x$. Do đó, với mọi $x \geq 0$, $L(\frac{p_k x + p_{k-1}}{q_k x + q_{k-1}})$ nằm giữa $L(\frac{p_k}{q_k}) = \frac{a_k}{c_k}$ và $L(\frac{p_{k-1}}{q_{k-1}}) = \frac{b_k}{d_k}$.

    Hơn nữa, với $x=[a_{k+1}; \dots, a_n]$, giá trị này bằng $L(A)$. Vậy $b_0 = \lfloor L(A) \rfloor$ nằm giữa $\lfloor L(\frac{p_k}{q_k}) \rfloor$ và $\lfloor L(\frac{p_{k-1}}{q_{k-1}}) \rfloor$. Khi hai giá trị này bằng nhau, chúng cũng bằng $b_0$.

    Lưu ý $L(A) = (L_{b_0} \circ L_{b_1} \circ \dots \circ L_{b_m})(\infty)$. Khi biết $b_0$, ta có thể hợp $L_{b_0}^{-1}$ với phép biến đổi hiện tại và tiếp tục thêm $L_{a_{k+1}}$, $L_{a_{k+2}}$, v.v., tìm các giá trị lấy phần nguyên mới trùng nhau. Từ đó ta suy ra $b_1$ và tiếp tục cho đến khi tìm được mọi giá trị của $[b_0; b_1, \dots, b_m]$.

!!! example "Số học trên liên phân số"
    Cho $A=[a_0; a_1, \dots, a_n]$ và $B=[b_0; b_1, \dots, b_m]$. Tính các biểu diễn liên phân số của $A+B$ và $A \cdot B$.
??? hint "Lời giải"
    Ý tưởng tương tự bài trước, nhưng thay vì $L(x) = \frac{ax+b}{cx+d}$, hãy xét phép biến đổi phân song tuyến tính $L(x, y) = \frac{axy+bx+cy+d}{exy+fx+gy+h}$.

    Thay vì $L(x) \mapsto L(L_{a_k}(x))$, ta thay đổi phép biến đổi hiện tại theo $L(x, y) \mapsto L(L_{a_k}(x), y)$ hoặc $L(x, y) \mapsto L(x, L_{b_k}(y))$.

    Sau đó, kiểm tra $\lfloor \frac{a}{e} \rfloor = \lfloor \frac{b}{f} \rfloor = \lfloor \frac{c}{g} \rfloor = \lfloor \frac{d}{h} \rfloor$. Nếu tất cả bằng nhau, dùng giá trị này làm $c_k$ trong liên phân số kết quả và thay đổi phép biến đổi thành

    $$L(x, y) \mapsto \frac{1}{L(x, y) - c_k}.$$

!!! info "Định nghĩa"
    Liên phân số $x = [a_0; a_1, \dots]$ được gọi là **tuần hoàn** nếu $x = [a_0; a_1, \dots, a_k, x]$ với một $k$ nào đó.

    Liên phân số $x = [a_0; a_1, \dots]$ được gọi là **tuần hoàn từ một vị trí nào đó** nếu $x = [a_0; a_1, \dots, a_k, y]$, trong đó $y$ tuần hoàn.

Với $x = [1; 1, 1, \dots]$, ta có $x = 1 + \frac{1}{x}$, nên $x^2 = x + 1$. Có một mối liên hệ tổng quát giữa liên phân số tuần hoàn và phương trình bậc hai. Xét phương trình sau:

$$ x = [a_0; a_1, \dots, a_k, x].$$

Một mặt, phương trình này có nghĩa là biểu diễn liên phân số của $x$ tuần hoàn với chu kỳ $k+1$.

Mặt khác, dùng công thức cho các phân số hội tụ, phương trình này có nghĩa là

$$x = \frac{p_k x + p_{k-1}}{q_k x + q_{k-1}}.$$

Tức là $x$ là một phép biến đổi phân tuyến tính của chính nó. Từ phương trình suy ra $x$ là nghiệm của phương trình bậc hai:

$$q_k x^2 + (q_{k-1}-p_k)x - p_{k-1} = 0.$$

Lập luận tương tự áp dụng cho liên phân số tuần hoàn từ một vị trí nào đó, tức $x = [a_0; a_1, \dots, a_k, y]$ với $y=[b_0; b_1, \dots, b_k, y]$. Thật vậy, từ phương trình đầu suy ra $x = L_0(y)$ và từ phương trình thứ hai suy ra $y = L_1(y)$, trong đó $L_0$ và $L_1$ là các phép biến đổi phân tuyến tính. Do đó,

$$x = (L_0 \circ L_1)(y) = (L_0 \circ L_1 \circ L_0^{-1})(x).$$

Có thể chứng minh thêm (điều này được Lagrange chứng minh đầu tiên) rằng với phương trình bậc hai bất kỳ $ax^2+bx+c=0$ có hệ số nguyên, nghiệm $x$ của nó là một liên phân số tuần hoàn từ một vị trí nào đó.

**Ghi chú bản dịch:** Ví dụ số vô tỉ bậc hai bên dưới có một số công thức trong nguồn chưa đúng tổng quát: công thức thương đầy đủ lệch chỉ số, phép lấy phần nguyên không thể luôn thay căn bằng phần nguyên của nó, và phép khử căn dùng nhầm hệ số. Vì vậy không nên áp dụng trực tiếp hàm bước được mô tả cho biểu diễn tùy ý.

!!! example "Số vô tỉ bậc hai"
    Tìm liên phân số của $\alpha = \frac{x+y\sqrt{n}}{z}$, trong đó $x, y, z, n \in \mathbb Z$ và $n > 0$ không phải số chính phương.
??? hint "Lời giải"
    Nói chung, với thương đầy đủ thứ $k$ là $s_k$ của số này, ta có

    $$\alpha = [a_0; a_1, \dots, a_{k-1}, s_k] = \frac{s_k p_{k-1} + p_{k-2}}{s_k q_{k-1} + q_{k-2}}.$$

    Do đó,

    $$s_k = -\frac{\alpha q_{k-1} - p_{k-1}}{\alpha q_k - p_k} = -\frac{q_{k-1} y \sqrt n + (x q_{k-1} - z p_{k-1})}{q_k y \sqrt n + (xq_k-zp_k)}.$$

    Nhân tử và mẫu với $(xq_k - zp_k) - q_k y \sqrt n$, ta khử được $\sqrt n$ ở mẫu, vì vậy các thương đầy đủ có dạng

    $$s_k = \frac{x_k + y_k \sqrt n}{z_k}.$$

    Hãy tìm $s_{k+1}$, giả sử đã biết $s_k$.

    Trước hết, $a_k = \lfloor s_k \rfloor = \left\lfloor \frac{x_k + y_k \lfloor \sqrt n \rfloor}{z_k} \right\rfloor$. Khi đó,

    $$s_{k+1} = \frac{1}{s_k-a_k} = \frac{z_k}{(x_k - z_k a_k) + y_k \sqrt n} = \frac{z_k (x_k - y_k a_k) - y_k z_k \sqrt n}{(x_k - y_k a_k)^2 - y_k^2 n}.$$

    Do đó, nếu đặt $t_k = x_k - y_k a_k$ thì ta có

    \begin{align}x_{k+1} &=& z_k t_k, \\ y_{k+1} &=& -y_k z_k, \\ z_{k+1} &=& t_k^2 - y_k^2 n.\end{align}

    Ưu điểm của biểu diễn này là nếu chia $x_{k+1}, y_{k+1}, z_{k+1}$ cho ước chung lớn nhất của chúng thì kết quả sẽ là duy nhất. Do đó, ta có thể dùng nó để kiểm tra trạng thái hiện tại đã lặp lại hay chưa và chỉ số trước đó có trạng thái này là bao nhiêu.

    Dưới đây là mã tính biểu diễn liên phân số của $\alpha = \sqrt n$:

    === "Python"
        ```py
        # compute the continued fraction of sqrt(n)
        def sqrt(n):
            n0 = math.floor(math.sqrt(n))
            x, y, z = 1, 0, 1
            a = []
            def step(x, y, z):
                a.append((x * n0 + y) // z)
                t = y - a[-1]*z
                x, y, z = -z*x, z*t, t**2 - n*x**2
                g = math.gcd(x, math.gcd(y, z))
                return x // g, y // g, z // g

            used = dict()
            for i in range(n):
                used[x, y, z] = i
                x, y, z = step(x, y, z)
                if (x, y, z) in used:
                    return a
        ```

    Dùng cùng hàm `step` nhưng thay đổi $x$, $y$ và $z$ ban đầu, ta có thể tính biểu diễn cho $\frac{x+y \sqrt{n}}{z}$ bất kỳ.

!!! example "[Tavrida NU Akai Contest - Continued Fraction](https://timus.online/problem.aspx?space=1&num=1814)"
    Cho $x$ và $k$, với $x$ không phải số chính phương. Đặt $\sqrt x = [a_0; a_1, \dots]$, hãy tìm $\frac{p_k}{q_k}=[a_0; a_1, \dots, a_k]$ với $0 \leq k \leq 10^9$.
??? hint "Lời giải"
    Sau khi tính chu kỳ của $\sqrt x$, có thể tính $a_k$ bằng lũy thừa nhị phân trên phép biến đổi phân tuyến tính do biểu diễn liên phân số tạo ra. Để tìm phép biến đổi kết quả, ta nén chu kỳ độ dài $T$ thành một phép biến đổi và lặp lại nó $\lfloor \frac{k-1}{T}\rfloor$ lần, sau đó kết hợp trực tiếp với các phép biến đổi còn lại.

    === "Python"
        ```py
        x, k = map(int, input().split())

        mod = 10**9+7
        
        # compose (A[0]*x + A[1]) / (A[2]*x + A[3]) and (B[0]*x + B[1]) / (B[2]*x + B[3])
        def combine(A, B):
            return [t % mod for t in [A[0]*B[0]+A[1]*B[2], A[0]*B[1]+A[1]*B[3], A[2]*B[0]+A[3]*B[2], A[2]*B[1]+A[3]*B[3]]]

        A = [1, 0, 0, 1] # (x + 0) / (0*x + 1) = x

        a = sqrt(x)

        T = len(a) - 1 # period of a

        # apply ak + 1/x = (ak*x+1)/(1x+0) to (Ax + B) / (Cx + D)
        for i in reversed(range(1, len(a))):
            A = combine([a[i], 1, 1, 0], A)

        def bpow(A, n):
            return [1, 0, 0, 1] if not n else combine(A, bpow(A, n-1)) if n % 2 else bpow(combine(A, A), n // 2)


        C = (0, 1, 0, 0) # = 1 / 0
        while k % T:
            i = k % T
            C = combine([a[i], 1, 1, 0], C)
            k -= 1

        C = combine(bpow(A, k // T), C)
        C = combine([a[0], 1, 1, 0], C)
        print(str(C[1]) + '/' + str(C[3]))
        ```

## Diễn giải hình học

Đặt $\vec r_k = (q_k;p_k)$ với phân số hội tụ $r_k = \frac{p_k}{q_k}$. Khi đó ta có công thức truy hồi:

$$\vec r_k = a_k \vec r_{k-1} + \vec r_{k-2}.$$

Đặt $\vec r = (1;r)$. Khi đó, mỗi vectơ $(x;y)$ tương ứng với một số bằng hệ số góc $\frac{y}{x}$ của nó.

Với khái niệm [tích giả vô hướng](../geometry/basic-geometry.md) $(x_1;y_1) \times (x_2;y_2) = x_1 y_2 - x_2 y_1$, có thể chỉ ra (xem phần giải thích bên dưới) rằng

$$s_k = -\frac{\vec r_{k-2} \times \vec r}{\vec r_{k-1} \times \vec r} = \left|\frac{\vec r_{k-2} \times \vec r}{\vec r_{k-1} \times \vec r}\right|.$$

Đẳng thức cuối có được vì $r_{k-1}$ và $r_{k-2}$ nằm ở hai phía khác nhau của $r$, do đó các tích giả vô hướng của $\vec r_{k-1}$ và $\vec r_{k-2}$ với $\vec r$ trái dấu. Nhớ rằng $a_k = \lfloor s_k \rfloor$, công thức của $\vec r_k$ giờ có dạng

$$\vec r_k = \vec r_{k-2} + \left\lfloor \left| \frac{\vec r \times \vec r_{k-2}}{\vec r \times \vec r_{k-1}}\right|\right\rfloor \vec r_{k-1}.$$

Lưu ý $\vec r_k \times r = (q;p) \times (1;r) = qr - p$, do đó

$$a_k = \left\lfloor \left| \frac{q_{k-1}r-p_{k-1}}{q_{k-2}r-p_{k-2}} \right| \right\rfloor.$$

??? hint "Giải thích"
    Như đã thấy, $a_k = \lfloor s_k \rfloor$, trong đó $s_k = [a_k; a_{k+1}, a_{k+2}, \dots]$. Mặt khác, từ công thức truy hồi của phân số hội tụ, ta suy ra

    $$r = [a_0; a_1, \dots, a_{k-1}, s_k] = \frac{s_k p_{k-1} + p_{k-2}}{s_k q_{k-1} + q_{k-2}}.$$

    Viết lại dưới dạng vectơ, ta có

    $$\vec r \parallel s_k \vec r_{k-1} + \vec r_{k-2},$$

    nghĩa là $\vec r$ và $s_k \vec r_{k-1} + \vec r_{k-2}$ cùng phương (tức là có cùng hệ số góc). Lấy [tích giả vô hướng](../geometry/basic-geometry.md) của hai vế với $\vec r$, ta được

    $$0 = s_k (\vec r_{k-1} \times \vec r) + (\vec r_{k-2} \times \vec r),$$

    từ đó suy ra công thức cuối cùng

    $$s_k = -\frac{\vec r_{k-2} \times \vec r}{\vec r_{k-1} \times \vec r}.$$

!!! example "Thuật toán kéo dài mũi"
    Mỗi lần cộng $\vec r_{k-1}$ vào vectơ $\vec p$, giá trị của $\vec p \times \vec r$ tăng thêm $\vec r_{k-1} \times \vec r$.

    Do đó, $a_k=\lfloor s_k \rfloor$ là số lượng lớn nhất các vectơ $\vec r_{k-1}$ có thể cộng vào $\vec r_{k-2}$ mà không làm đổi dấu tích có hướng với $\vec r$.

    Nói cách khác, $a_k$ là số lần lớn nhất ta có thể cộng $\vec r_{k-1}$ vào $\vec r_{k-2}$ mà không vượt qua đường thẳng xác định bởi $\vec r$:

    <figure><img src="https://upload.wikimedia.org/wikipedia/commons/9/92/Continued_convergents_geometry.svg" width="700px"/>
    <figcaption>_Các phân số hội tụ của $r=\frac{7}{9}=[0;1,3,2]$. Các bán hội tụ tương ứng với những điểm trung gian giữa các mũi tên màu xám._</figcaption></figure>

    Trong hình trên, $\vec r_2 = (4;3)$ thu được bằng cách liên tiếp cộng $\vec r_1 = (1;1)$ vào $\vec r_0 = (1;0)$.

    Khi không thể tiếp tục cộng $\vec r_1$ vào $\vec r_0$ mà không vượt qua đường thẳng $y=rx$, ta sang phía bên kia và liên tiếp cộng $\vec r_2$ vào $\vec r_1$ để thu được $\vec r_3 = (9;7)$.

    Quá trình này tạo ra các vectơ có độ dài tăng theo hàm mũ và tiến gần đường thẳng.

    Vì tính chất này, Boris Delaunay gọi quá trình sinh các vectơ hội tụ liên tiếp là **thuật toán kéo dài mũi** (nose stretching algorithm).

Xét tam giác có các đỉnh $\vec r_{k-2}$, $\vec r_{k}$ và $\vec 0$, ta thấy diện tích nhân đôi của nó là

$$|\vec r_{k-2} \times \vec r_k| = |\vec r_{k-2} \times (\vec r_{k-2} + a_k \vec r_{k-1})| = a_k |\vec r_{k-2} \times \vec r_{k-1}| = a_k.$$

Kết hợp với [định lý Pick](../geometry/picks-theorem.md), điều này có nghĩa là không có điểm nguyên nào nằm thực sự bên trong tam giác, và các điểm nguyên duy nhất trên biên của nó là $\vec 0$ và $\vec r_{k-2} + t \cdot \vec r_{k-1}$ với mọi số nguyên $t$ sao cho $0 \leq t \leq a_k$. Gộp lại với mọi $k$ có thể, ta thấy không có điểm nguyên trong miền giữa các đa giác tạo bởi những vectơ hội tụ chỉ số chẵn và chỉ số lẻ.

Từ đó suy ra các $\vec r_k$ với chỉ số lẻ tạo thành bao lồi của các điểm nguyên có $x \geq 0$ phía trên đường thẳng $y=rx$, còn các $\vec r_k$ với chỉ số chẵn tạo thành bao lồi của các điểm nguyên có $x > 0$ phía dưới đường thẳng $y=rx$.


!!! info "Định nghĩa"

    Những đa giác này còn được gọi là **đa giác Klein**, theo tên Felix Klein, người đầu tiên đề xuất cách diễn giải hình học này cho liên phân số.

## Các bài toán ví dụ

Sau khi đã giới thiệu các kết quả và khái niệm quan trọng nhất, ta sẽ đi vào những bài toán ví dụ cụ thể.

!!! example "Bao lồi bên dưới đường thẳng"
    Tìm bao lồi của các điểm nguyên $(x;y)$ thỏa mãn $0 \leq x \leq N$ và $0 \leq y \leq rx$ với $r=[a_0;a_1,\dots,a_k]=\frac{p_k}{q_k}$.

??? hint "Lời giải"
    Nếu xét tập không bị chặn $0 \leq x$, bao lồi trên sẽ chính là đường thẳng $y=rx$.

    Tuy nhiên, với ràng buộc thêm $x \leq N$, cuối cùng ta cần đi lệch khỏi đường thẳng để giữ được bao lồi phù hợp.

    Đặt $t = \lfloor \frac{N}{q_k}\rfloor$, khi đó $t$ điểm nguyên đầu tiên trên bao lồi sau $(0;0)$ là $\alpha \cdot (q_k; p_k)$ với số nguyên $1 \leq \alpha \leq t$.

    Tuy nhiên $(t+1)(q_k; p_k)$ không thể là điểm nguyên tiếp theo vì $(t+1)q_k$ lớn hơn $N$.

    Để đến các điểm nguyên tiếp theo trên bao lồi, ta cần đến điểm $(x;y)$ lệch khỏi $y=rx$ ít nhất, đồng thời thỏa mãn $x \leq N$.

    <figure><img src="https://upload.wikimedia.org/wikipedia/commons/b/b1/Lattice-hull.svg" width="500px"/>
    <figcaption>Bao lồi của các điểm nguyên dưới $y=\frac{4}{7}x$ với $0 \leq x \leq 19$ gồm các điểm $(0;0), (7;4), (14;8), (16;9), (18;10), (19;10)$.</figcaption></figure>

    Gọi $(x; y)$ là điểm cuối hiện tại trên bao lồi. Khi đó điểm tiếp theo $(x'; y')$ thỏa mãn $x' \leq N$ và $(x'; y') - (x; y) = (\Delta x; \Delta y)$ gần đường thẳng $y=rx$ nhất có thể. Nói cách khác, $(\Delta x; \Delta y)$ cực đại hóa $r \Delta x - \Delta y$ với các ràng buộc $\Delta x \leq N - x$ và $\Delta y \leq r \Delta x$.

    Các điểm như vậy nằm trên bao lồi của những điểm nguyên dưới $y=rx$. Nói cách khác, $(\Delta x; \Delta y)$ phải là một bán hội tụ dưới của $r$.

    Cụ thể, $(\Delta x; \Delta y)$ có dạng $(q_{i-1}; p_{i-1}) + t \cdot (q_i; p_i)$ với một số lẻ $i$ và $0 \leq t < a_i$.

    Để tìm $i$ như vậy, ta có thể duyệt mọi $i$ có thể từ lớn nhất và dùng $t = \lfloor \frac{N-x-q_{i-1}}{q_i} \rfloor$ với $i$ thỏa mãn $N-x-q_{i-1} \geq 0$.

    Với $(\Delta x; \Delta y) = (q_{i-1}; p_{i-1}) + t \cdot (q_i; p_i)$, điều kiện $\Delta y \leq r \Delta x$ được bảo toàn nhờ tính chất của bán hội tụ.

    Ngoài ra $t < a_i$ đúng vì ta đã dùng hết các bán hội tụ thu được từ $i+2$, do đó $x + q_{i-1} + a_i q_i = x+q_{i+1}$ lớn hơn $N$.

    Ta có thể cộng $(\Delta x; \Delta y)$ vào $(x;y)$ $k = \lfloor \frac{N-x}{\Delta x} \rfloor$ lần trước khi vượt quá $N$, sau đó thử bán hội tụ tiếp theo.

    === "C++"
        ```cpp
        // returns [ah, ph, qh] such that points r[i]=(ph[i], qh[i]) constitute upper convex hull
        // of lattice points on 0 <= x <= N and 0 <= y <= r * x, where r = [a0; a1, a2, ...]
        // and there are ah[i]-1 integer points on the segment between r[i] and r[i+1]
        auto hull(auto a, int N) {
            auto [p, q] = convergents(a);
            int t = N / q.back();
            vector ah = {t};
            vector ph = {0, t*p.back()};
            vector qh = {0, t*q.back()};

            for(int i = q.size() - 1; i >= 0; i--) {
                if(i % 2) {
                    while(qh.back() + q[i - 1] <= N) {
                        t = (N - qh.back() - q[i - 1]) / q[i];
                        int dp = p[i - 1] + t * p[i];
                        int dq = q[i - 1] + t * q[i];
                        int k = (N - qh.back()) / dq;
                        ah.push_back(k);
                        ph.push_back(ph.back() + k * dp);
                        qh.push_back(qh.back() + k * dq);
                    }
                }
            }
            return make_tuple(ah, ph, qh);
        }
        ```
    === "Python"
        ```py
        # returns [ah, ph, qh] such that points r[i]=(ph[i], qh[i]) constitute upper convex hull
        # of lattice points on 0 <= x <= N and 0 <= y <= r * x, where r = [a0; a1, a2, ...]
        # and there are ah[i]-1 integer points on the segment between r[i] and r[i+1]
        def hull(a, N):
            p, q = convergents(a)
            t = N // q[-1]
            ah = [t]
            ph = [0, t*p[-1]]
            qh = [0, t*q[-1]]
            for i in reversed(range(len(q))):
                if i % 2 == 1:
                    while qh[-1] + q[i-1] <= N:
                        t = (N - qh[-1] - q[i-1]) // q[i]
                        dp = p[i-1] + t*p[i]
                        dq = q[i-1] + t*q[i]
                        k = (N - qh[-1]) // dq
                        ah.append(k)
                        ph.append(ph[-1] + k * dp)
                        qh.append(qh[-1] + k * dq)
            return ah, ph, qh
        ```

!!! example "[Timus - Crime and Punishment](https://timus.online/problem.aspx?space=1&num=1430)"
    Cho các số nguyên $A$, $B$ và $N$. Tìm $x \geq 0$ và $y \geq 0$ sao cho $Ax + By \leq N$ và $Ax + By$ lớn nhất có thể.

??? hint "Lời giải"
    Trong bài toán này, $1 \leq A, B, N \leq 2 \cdot 10^9$, nên có thể giải trong $O(\sqrt N)$. Tuy nhiên, có một lời giải $O(\log N)$ bằng liên phân số.

    Để thuận tiện, ta đảo chiều của $x$ bằng phép thay $x \mapsto \lfloor \frac{N}{A}\rfloor - x$. Khi đó cần tìm điểm $(x; y)$ sao cho $0 \leq x \leq \lfloor \frac{N}{A} \rfloor$, $By - Ax \leq N \;\bmod\; A$ và $By - Ax$ lớn nhất có thể. Với mỗi $x$, giá trị $y$ tối ưu là $\lfloor \frac{Ax + (N \bmod A)}{B} \rfloor$.

    Để xử lý tổng quát hơn, ta viết một hàm tìm điểm tốt nhất với $0 \leq x \leq N$ và $y = \lfloor \frac{Ax+B}{C} \rfloor$.

    Ý tưởng cốt lõi về cơ bản lặp lại bài toán trước, nhưng thay vì dùng các bán hội tụ dưới để đi lệch khỏi đường thẳng, ta dùng các bán hội tụ trên để tiến gần đường thẳng mà không vượt qua nó và không vi phạm $x \leq N$. Khác với bài trước, ta cần bảo đảm không vượt qua đường $y=\frac{Ax+B}{C}$ khi tiến gần, vì vậy phải lưu ý điều này khi tính hệ số $t$ của bán hội tụ.

    === "Python"
        ```py
        # (x, y) such that y = (A*x+B) // C,
        # Cy - Ax is max and 0 <= x <= N.
        def closest(A, B, C, N):
            # y <= (A*x + B)/C <=> diff(x, y) <= B
            def diff(x, y):
                return C*y-A*x
            a = fraction(A, C)
            p, q = convergents(a)
            ph = [B // C]
            qh = [0]
            for i in range(2, len(q) - 1):
                if i % 2 == 0:
                    while diff(qh[-1] + q[i+1], ph[-1] + p[i+1]) <= B:
                        t = 1 + (diff(qh[-1] + q[i-1], ph[-1] + p[i-1]) - B - 1) // abs(diff(q[i], p[i]))
                        dp = p[i-1] + t*p[i]
                        dq = q[i-1] + t*q[i]
                        k = (N - qh[-1]) // dq
                        if k == 0:
                            return qh[-1], ph[-1]
                        if diff(dq, dp) != 0:
                            k = min(k, (B - diff(qh[-1], ph[-1])) // diff(dq, dp))
                        qh.append(qh[-1] + k*dq)
                        ph.append(ph[-1] + k*dp)
            return qh[-1], ph[-1]

        def solve(A, B, N):
            x, y = closest(A, N % A, B, N // A)
            return N // A - x, y
        ```

!!! example "[June Challenge 2017 - Euler Sum](https://www.codechef.com/problems/ES)"
    Tính $\sum\limits_{x=1}^N \lfloor ex \rfloor$, trong đó $e = [2; 1, 2, 1, 1, 4, 1, 1, 6, 1, \dots, 1, 2n, 1, \dots]$ là số Euler và $N \leq 10^{4000}$.

??? hint "Lời giải"
    Tổng này bằng số điểm nguyên $(x;y)$ thỏa mãn $1 \leq x \leq N$ và $1 \leq y \leq ex$.

    Sau khi dựng bao lồi của các điểm dưới $y=ex$, có thể tính số lượng này bằng [định lý Pick](../geometry/picks-theorem.md):

    === "C++"
        ```cpp
        // sum floor(k * x) for k in [1, N] and x = [a0; a1, a2, ...]
        int sum_floor(auto a, int N) {
            N++;
            auto [ah, ph, qh] = hull(a, N);

            // The number of lattice points within a vertical right trapezoid
            // on points (0; 0) - (0; y1) - (dx; y2) - (dx; 0) that has
            // a+1 integer points on the segment (0; y1) - (dx; y2).
            auto picks = [](int y1, int y2, int dx, int a) {
                int b = y1 + y2 + a + dx;
                int A = (y1 + y2) * dx;
                return (A - b + 2) / 2 + b - (y2 + 1);
            };

            int ans = 0;
            for(size_t i = 1; i < qh.size(); i++) {
                ans += picks(ph[i - 1], ph[i], qh[i] - qh[i - 1], ah[i - 1]);
            }
            return ans - N;
        }
        ```
    === "Python"
        ```py
        # sum floor(k * x) for k in [1, N] and x = [a0; a1, a2, ...]
        def sum_floor(a, N):
            N += 1
            ah, ph, qh = hull(a, N)

            # The number of lattice points within a vertical right trapezoid
            # on points (0; 0) - (0; y1) - (dx; y2) - (dx; 0) that has
            # a+1 integer points on the segment (0; y1) - (dx; y2).
            def picks(y1, y2, dx, a):
                b = y1 + y2 + a + dx
                A = (y1 + y2) * dx
                return (A - b + 2) // 2 + b - (y2 + 1)

            ans = 0
            for i in range(1, len(qh)):
                ans += picks(ph[i-1], ph[i], qh[i]-qh[i-1], ah[i-1])
            return ans - N
        ``` 

!!! example "[NAIPC 2019 - It's a Mod, Mod, Mod, Mod World](https://open.kattis.com/problems/itsamodmodmodmodworld)"
    Cho $p$, $q$ và $n$, tính $\sum\limits_{i=1}^n [p \cdot i \bmod q]$.

??? hint "Lời giải"
    Bài toán này quy về bài trước nếu nhận thấy $a \bmod b = a - \lfloor \frac{a}{b} \rfloor b$. Từ đó, tổng trở thành

    $$\sum\limits_{i=1}^n \left(p \cdot i - \left\lfloor \frac{p \cdot i}{q} \right\rfloor q\right) = \frac{pn(n+1)}{2}-q\sum\limits_{i=1}^n \left\lfloor \frac{p \cdot i}{q}\right\rfloor.$$

    Việc tính tổng $\lfloor rx \rfloor$ với $x$ từ $1$ đến $N$ đã được giải trong bài toán trước.

    === "C++"
        ```cpp
        void solve(int p, int q, int N) {
            cout << p * N * (N + 1) / 2 - q * sum_floor(fraction(p, q), N) << "\n";
        }
        ```
    === "Python"
        ```py
        def solve(p, q, N):
            return p * N * (N + 1) // 2 - q * sum_floor(fraction(p, q), N)
        ``` 

!!! example "[Library Checker - Sum of Floor of Linear](https://judge.yosupo.jp/problem/sum_of_floor_of_linear)"
    Cho $N$, $M$, $A$ và $B$, tính $\sum\limits_{i=0}^{N-1} \lfloor \frac{A \cdot i + B}{M} \rfloor$.

??? hint "Lời giải"
    Đây là bài toán phức tạp nhất về mặt kỹ thuật từ đầu đến giờ.

    Có thể dùng cùng cách tiếp cận và dựng toàn bộ bao lồi của các điểm bên dưới đường thẳng $y = \frac{Ax+B}{M}$.

    Ta đã biết cách giải khi $B = 0$. Hơn nữa, ta cũng biết cách dựng bao lồi này đến điểm nguyên gần đường thẳng nhất trên đoạn $[0, N-1]$ (như đã thực hiện trong bài "Crime and Punishment" ở trên).

    Khi đã đến điểm gần đường thẳng nhất, ta có thể coi đường thẳng thực sự đi qua điểm đó, vì không có điểm nguyên nào khác trên $[0, N-1]$ nằm giữa đường thẳng ban đầu và đường thẳng được dịch nhẹ xuống dưới để đi qua điểm gần nhất.

    Do đó, để dựng toàn bộ bao lồi dưới đường thẳng $y=\frac{Ax+B}{M}$ trên $[0, N-1]$, ta có thể dựng đến điểm gần đường thẳng nhất trên $[0, N-1]$, rồi tiếp tục như thể đường thẳng đi qua điểm này, dùng lại thuật toán dựng bao lồi với $B=0$:

    === "Python"
        ```py
        # hull of lattice (x, y) such that C*y <= A*x+B
        def hull(A, B, C, N):
            def diff(x, y):
                return C*y-A*x
            a = fraction(A, C)
            p, q = convergents(a)
            ah = []
            ph = [B // C]
            qh = [0]

            def insert(dq, dp):
                k = (N - qh[-1]) // dq
                if diff(dq, dp) > 0:
                    k = min(k, (B - diff(qh[-1], ph[-1])) // diff(dq, dp))
                ah.append(k)
                qh.append(qh[-1] + k*dq)
                ph.append(ph[-1] + k*dp)

            for i in range(1, len(q) - 1):
                if i % 2 == 0:
                    while diff(qh[-1] + q[i+1], ph[-1] + p[i+1]) <= B:
                        t = (B - diff(qh[-1] + q[i+1], ph[-1] + p[i+1])) // abs(diff(q[i], p[i]))
                        dp = p[i+1] - t*p[i]
                        dq = q[i+1] - t*q[i]
                        if dq < 0 or qh[-1] + dq > N:
                            break
                        insert(dq, dp)

            insert(q[-1], p[-1])

            for i in reversed(range(len(q))):
                if i % 2 == 1:
                    while qh[-1] + q[i-1] <= N:
                        t = (N - qh[-1] - q[i-1]) // q[i]
                        dp = p[i-1] + t*p[i]
                        dq = q[i-1] + t*q[i]
                        insert(dq, dp)
            return ah, ph, qh
        ```

!!! example "[OKC 2 - From Modular to Rational](https://codeforces.com/gym/102354/problem/I)"
    Có một số hữu tỉ $\frac{p}{q}$ thỏa mãn $1 \leq p, q \leq 10^9$. Bạn có thể hỏi giá trị của $p q^{-1}$ theo modulo $m \sim 10^9$ với một số số nguyên tố $m$. Hãy khôi phục $\frac{p}{q}$.

    _Phát biểu tương đương:_ Tìm $x$ làm cực tiểu $Ax \;\bmod\; M$ với $1 \leq x \leq N$.

??? hint "Lời giải"
    Theo định lý số dư Trung Hoa, hỏi kết quả modulo một số số nguyên tố tương đương với hỏi modulo tích của chúng. Do đó, không mất tính tổng quát, ta giả sử đã biết số dư modulo một số $m$ đủ lớn.

    Với một số dư $r$ cho trước, có thể có nhiều nghiệm $(p, q)$ của $p \equiv qr \pmod m$. Tuy nhiên, nếu $(p_1, q_1)$ và $(p_2, q_2)$ đều là nghiệm thì $p_1 q_2 \equiv p_2 q_1 \pmod m$. Giả sử $\frac{p_1}{q_1} \neq \frac{p_2}{q_2}$ thì điều này có nghĩa là $|p_1 q_2 - p_2 q_1|$ ít nhất bằng $m$.

    Theo đề bài, $1 \leq p, q \leq 10^9$, nên nếu cả $p_1, q_1$ và $p_2, q_2$ không vượt quá $10^9$, hiệu này nhiều nhất là $10^{18}$. Với $m > 10^{18}$, điều đó có nghĩa là nghiệm $\frac{p}{q}$ thỏa mãn $1 \leq p, q \leq 10^9$ là duy nhất xét dưới dạng số hữu tỉ.

    Vậy, với $r$ modulo $m$ đã cho, bài toán quy về tìm một $q$ bất kỳ sao cho $1 \leq q \leq 10^9$ và $qr \;\bmod\; m \leq 10^9$.

    Điều này về bản chất tương đương với tìm $q$ cho giá trị $qr \bmod m$ nhỏ nhất có thể với $1 \leq q \leq 10^9$.

    Với $qr = km + b$, điều đó có nghĩa là cần tìm một cặp $(q, m)$ sao cho $1 \leq q \leq 10^9$ và $qr - km \geq 0$ nhỏ nhất có thể.

    Vì $m$ là hằng số, ta có thể chia cho nó và phát biểu lại: tìm $q$ sao cho $1 \leq q \leq 10^9$ và $\frac{r}{m} q - k \geq 0$ nhỏ nhất có thể.

    Theo liên phân số, điều đó có nghĩa là $\frac{k}{q}$ là phép xấp xỉ Diophantine tốt nhất của $\frac{r}{m}$ và chỉ cần kiểm tra các bán hội tụ dưới của $\frac{r}{m}$.

    === "Python"
        ```py
        # find Q that minimizes Q*r mod m for 1 <= k <= n < m 
        def mod_min(r, n, m):
            a = fraction(r, m)
            p, q = convergents(a)
            for i in range(2, len(q)):
                if i % 2 == 1 and (i + 1 == len(q) or q[i+1] > n):
                    t = (n - q[i-1]) // q[i]
                    return q[i-1] + t*q[i]
        ```

## Bài tập luyện tập

* [UVa OJ - Continued Fractions](https://onlinejudge.org/index.php?option=com_onlinejudge&Itemid=8&page=show_problem&problem=775)
* [ProjectEuler+ #64: Odd period square roots](https://www.hackerrank.com/contests/projecteuler/challenges/euler064/problem)
* [Codeforces Round #184 (Div. 2) - Continued Fractions](https://codeforces.com/contest/305/problem/B)
* [Codeforces Round #201 (Div. 1) - Doodle Jump](https://codeforces.com/contest/346/problem/E)
* [Codeforces Round #325 (Div. 1) - Alice, Bob, Oranges and Apples](https://codeforces.com/contest/585/problem/C)
* [POJ Founder Monthly Contest 2008.03.16 - A Modular Arithmetic Challenge](http://poj.org/problem?id=3530)
* [2019 Multi-University Training Contest 5 - fraction](http://acm.hdu.edu.cn/showproblem.php?pid=6624)
* [SnackDown 2019 Elimination Round - Election Bait](https://www.codechef.com/SNCKEL19/problems/EBAIT)
* [Code Jam 2019 round 2 - Continued Fraction](https://github.com/google/coding-competitions-archive/blob/main/codejam/2019/round_2/new_elements_part_2/statement.pdf)
