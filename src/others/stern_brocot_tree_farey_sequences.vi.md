---
tags:
  - Translated
e_maxx_link: stern_brocot_farey
translation:
  source: others/stern_brocot_tree_farey_sequences.md
  source_commit: 156082b9aebd039c2aebb9d81abfbd0bbc16dc43
  status: draft
  last_synced: 2026-11-16
---

# Cây Stern-Brocot và dãy Farey

## Cây Stern-Brocot

Cây Stern-Brocot là một cách xây dựng đẹp để biểu diễn tập hợp mọi phân số dương. Nó được nhà toán học Đức Moritz Stern phát hiện năm 1858 và người thợ đồng hồ Pháp Achille Brocot phát hiện độc lập năm 1861. Tuy nhiên, một số nguồn cho rằng nhà toán học Hy Lạp cổ đại Eratosthenes đã phát hiện ra nó.

Phép xây dựng bắt đầu ở lần lặp thứ không với hai phân số

$$
    \frac{0}{1}, \frac{1}{0}
$$

trong đó cần lưu ý đại lượng thứ hai không thực sự là phân số, nhưng có thể được hiểu là phân số tối giản biểu diễn vô cực.

Ở mỗi lần lặp tiếp theo, xét mọi cặp phân số kề nhau $\frac{a}{b}$ và $\frac{c}{d}$ rồi chèn [phân số trung gian](https://en.wikipedia.org/wiki/Mediant_(mathematics)) (mediant) $\frac{a+c}{b+d}$ của chúng vào giữa.

Vài lần lặp đầu tiên như sau:

$$
    \begin{array}{c}
    \dfrac{0}{1}, \dfrac{1}{1}, \dfrac{1}{0} \\
    \dfrac{0}{1}, \dfrac{1}{2}, \dfrac{1}{1}, \dfrac{2}{1}, \dfrac{1}{0} \\
    \dfrac{0}{1}, \dfrac{1}{3}, \dfrac{1}{2}, \dfrac{2}{3}, \dfrac{1}{1}, \dfrac{3}{2}, \dfrac{2}{1}, \dfrac{3}{1}, \dfrac{1}{0}
    \end{array}
$$

Tiếp tục quá trình này đến vô hạn sẽ bao phủ *mọi* phân số dương. Ngoài ra, mọi phân số đều *không trùng nhau* và *tối giản*. Cuối cùng, các phân số cũng xuất hiện theo thứ tự tăng dần.

Trước khi chứng minh các tính chất này, ta hãy xem hình minh họa cây Stern-Brocot thay cho biểu diễn bằng danh sách. Mỗi phân số trong cây có hai con. Mỗi con là phân số trung gian của tổ tiên gần nhất bên trái và tổ tiên gần nhất bên phải.

<div style="text-align: center;">
  <img src="https://upload.wikimedia.org/wikipedia/commons/3/37/SternBrocotTree.svg" alt="Cây Stern-Brocot">
</div>

## Các chứng minh

**Thứ tự.** Việc chứng minh thứ tự khá đơn giản. Ta nhận thấy phân số trung gian của hai phân số luôn nằm giữa chúng

$$
    \frac{a}{b} \le \frac{a+c}{b+d} \le \frac{c}{d}
$$

nếu

$$
    \frac{a}{b} \le \frac{c}{d}.
$$

Có thể dễ dàng chứng minh hai bất đẳng thức bằng cách quy đồng mẫu số.

Vì thứ tự ở lần lặp thứ không là tăng dần, nó sẽ được duy trì ở mọi lần lặp sau.

**Tính tối giản.** Để chứng minh, ta chỉ ra rằng với hai phân số kề nhau bất kỳ $\frac{a}{b}$ và $\frac{c}{d}$, ta có

$$
    bc - ad = 1.
$$

Nhớ rằng phương trình Diophantine hai biến $ax+by=c$ có nghiệm khi và chỉ khi $c$ là bội của $\gcd(a,b)$. Trong trường hợp này, điều đó suy ra $\gcd(a,b) = \gcd(c,d) = 1$, đúng như điều ta muốn chứng minh.

Rõ ràng ở lần lặp thứ không, $bc - ad = 1$. Ta còn phải chứng minh các phân số trung gian giữ được tính chất này.

Giả sử hai phân số kề nhau thỏa mãn $bc - ad = 1$, sau khi thêm phân số trung gian vào danh sách

$$
    \frac{a}{b}, \frac{a+c}{b+d}, \frac{c}{d}
$$

các biểu thức mới trở thành

$$\begin{align}
    b(a+c) - a(b+d) &= 1 \\
    c(b+d) - d(a+c) &= 1
\end{align}$$

và dễ dàng chứng minh chúng đúng bằng cách dùng $bc-ad=1$.

Từ đó ta thấy tính chất luôn được duy trì, do đó mọi phân số đều tối giản.

**Sự xuất hiện của mọi phân số.** Chứng minh này liên quan chặt chẽ đến việc tìm một phân số trong cây Stern-Brocot. Từ tính chất thứ tự, cây con trái của một phân số chỉ chứa các phân số nhỏ hơn phân số cha, còn cây con phải chỉ chứa các phân số lớn hơn. Điều này nghĩa là ta có thể tìm một phân số bằng cách duyệt cây từ gốc, sang trái nếu phân số đích nhỏ hơn phân số hiện tại và sang phải nếu lớn hơn.

Chọn phân số dương đích tùy ý $\frac{x}{y}$. Nó rõ ràng nằm giữa $\frac{0}{1}$ và $\frac{1}{0}$, nên cách duy nhất để nó không nằm trong cây là cần vô hạn bước để đến được nó.

Nếu vậy, ở mọi lần lặp ta có

$$
    \frac{a}{b} \lt \frac{x}{y} \lt \frac{c}{d}
$$

và có thể viết lại (dùng tính chất với số nguyên $z \gt 0 \iff z \ge 1$) thành

$$
\begin{align}
    bx - ay &\ge 1 \\
    cy - dx &\ge 1.
\end{align}
$$

Bây giờ nhân bất đẳng thức thứ nhất với $c+d$ và bất đẳng thức thứ hai với $a+b$, rồi cộng lại:

$$
    (c+d)(bx - ay) + (a+b)(cy - dx) \ge a+b+c+d.
$$

Khai triển và dùng tính chất đã chứng minh $bc-ad=1$, ta được

$$
    x+y \ge a+b+c+d.
$$

Vì ở mỗi lần lặp ít nhất một trong $a,b,c,d$ tăng lên, quá trình tìm phân số sẽ không quá $x+y$ lần lặp. Điều này mâu thuẫn với giả thiết đường đi đến $\frac{x}{y}$ là vô hạn, nên $\frac{x}{y}$ phải thuộc cây.

## Thuật toán xây dựng cây

Để xây dựng một cây con bất kỳ của cây Stern-Brocot, chỉ cần biết tổ tiên trái và phải. Ở mức đầu tiên, tổ tiên trái và phải lần lượt là $\frac{0}{1}$ và $\frac{1}{0}$. Dùng chúng, ta tính phân số trung gian và đi sâu thêm một mức, trong đó phân số trung gian thay tổ tiên phải trong cây con trái và ngược lại.

Mã giả sau thử xây dựng toàn bộ cây vô hạn:

```cpp
void build(int a = 0, int b = 1, int c = 1, int d = 0, int level = 1) {
    int x = a + c, y = b + d;

    ... output the current fraction x/y at the current level in the tree
    
    build(a, b, x, y, level + 1);
    build(x, y, c, d, level + 1);
}
```

## Thuật toán tìm phân số

Thuật toán tìm kiếm đã được mô tả trong chứng minh mọi phân số đều xuất hiện trong cây, nhưng ta sẽ nhắc lại ở đây. Đây là thuật toán tìm kiếm nhị phân. Ban đầu ta đứng ở gốc và so sánh đích với phân số hiện tại. Nếu chúng bằng nhau, ta đã tìm thấy và dừng lại. Nếu đích nhỏ hơn, ta sang con trái; ngược lại, ta sang con phải.

### Tìm kiếm ngây thơ

Dưới đây là cài đặt trả về đường đi đến phân số $\frac{p}{q}$ dưới dạng dãy ký tự `'L'` và `'R'`, lần lượt biểu thị đi đến con trái và con phải. Dãy ký tự này xác định duy nhất mọi phân số dương và được gọi là hệ đếm Stern-Brocot.

```cpp
string find(int p, int q) {
    int pL = 0, qL = 1;
    int pR = 1, qR = 0;
    int pM = 1, qM = 1;
    string res;
    while(pM != p || qM != q) {
        if(p * qM < pM * q) {
            res += 'L';
            tie(pR, qR) = {pM, qM};
        } else {
            res += 'R';
            tie(pL, qL) = {pM, qM};
        }
        tie(pM, qM) = pair{pL + pR, qL + qR};
    }
    return res;
}
```

**Ghi chú bản dịch:** Hàm trên so sánh trực tiếp tử và mẫu, nên đầu vào cần là phân số dương đã rút gọn; nếu không, vòng lặp có thể không dừng.

Số vô tỉ trong hệ đếm Stern-Brocot tương ứng với các dãy ký tự vô hạn. Dọc đường đi vô tận tới số vô tỉ, thuật toán tìm được các phân số tối giản với mẫu số tăng dần, cho các phép xấp xỉ số vô tỉ ngày càng tốt hơn. Vì vậy, lấy một tiền tố của dãy vô hạn có thể cho phép xấp xỉ với độ chính xác mong muốn. Ứng dụng này quan trọng trong chế tạo đồng hồ, điều này giải thích tại sao cây được phát hiện trong lĩnh vực đó.

Lưu ý với phân số $\frac{p}{q}$, độ dài dãy kết quả có thể lên đến $O(p+q)$, chẳng hạn khi phân số có dạng $\frac{p}{1}$. Điều này nghĩa là **không nên dùng thuật toán trên trừ khi độ phức tạp đó có thể chấp nhận được**!

### Tìm kiếm logarithm

May mắn là có thể cải tiến thuật toán trên để bảo đảm độ phức tạp $O(\log (p+q))$. Ta cần nhận thấy rằng nếu các phân số biên hiện tại là $\frac{p_L}{q_L}$ và $\frac{p_R}{q_R}$, thì đi $a$ bước sang phải sẽ đưa ta đến phân số $\frac{p_L + a p_R}{q_L + a q_R}$, còn đi $a$ bước sang trái đưa ta đến phân số $\frac{a p_L + p_R}{a q_L + q_R}$.

Vì vậy, thay vì đi từng bước `L` hoặc `R`, ta có thể đi $k$ bước cùng hướng một lúc, sau đó đổi hướng, và cứ tiếp tục như vậy. Bằng cách này, ta có thể tìm đường đi tới phân số $\frac{p}{q}$ dưới dạng mã hóa theo độ dài đoạn (run-length encoding).

Vì các hướng luân phiên như vậy, ta luôn biết cần đi hướng nào. Do đó, để thuận tiện, ta có thể biểu diễn đường đi tới phân số $\frac{p}{q}$ bằng dãy các phân số

$$
\frac{p_0}{q_0}, \frac{p_1}{q_1}, \frac{p_2}{q_2}, \dots, \frac{p_n}{q_n}, \frac{p_{n+1}}{q_{n+1}} = \frac{p}{q}
$$

sao cho $\frac{p_{k-1}}{q_{k-1}}$ và $\frac{p_k}{q_k}$ là hai biên của khoảng tìm kiếm ở bước thứ $k$, bắt đầu với $\frac{p_0}{q_0} = \frac{0}{1}$ và $\frac{p_1}{q_1} = \frac{1}{0}$. Sau bước thứ $k$ ta chuyển tới phân số

$$
\frac{p_{k+1}}{q_{k+1}} = \frac{p_{k-1} + a_k p_k}{q_{k-1} + a_k q_k},
$$

trong đó $a_k$ là một số nguyên dương. Nếu quen với [phân số liên tục](../algebra/continued-fractions.md), bạn sẽ nhận ra rằng dãy $\frac{p_i}{q_i}$ là dãy các phân số hội tụ của $\frac{p}{q}$ và dãy $[a_1; a_2, \dots, a_{n}, 1]$ biểu diễn phân số liên tục của $\frac{p}{q}$.

Điều này cho phép tìm mã hóa theo độ dài đoạn của đường đi đến $\frac{p}{q}$ theo cách giống thuật toán tính biểu diễn phân số liên tục của phân số $\frac{p}{q}$:

```cpp
auto find(int p, int q) {
    bool right = true;
    vector<pair<int, char>> res;
    while(q) {
        res.emplace_back(p / q, right ? 'R' : 'L');
        tie(p, q) = pair{q, p % q};
        right ^= 1;
    }
    res.back().first--;
    return res;
}
```

Tuy nhiên, cách tiếp cận này chỉ hoạt động trực tiếp nếu ta đã biết $\frac{p}{q}$ và muốn tìm vị trí của nó trong cây Stern-Brocot.

Trong thực tế, thường thì $\frac{p}{q}$ không được biết trước, nhưng ta có thể kiểm tra với một $\frac{x}{y}$ cụ thể xem $\frac{x}{y} < \frac{p}{q}$ có đúng không.

Biết điều đó, ta có thể mô phỏng việc tìm kiếm trên cây Stern-Brocot bằng cách duy trì các biên hiện tại $\frac{p_{k-1}}{q_{k-1}}$ và $\frac{p_k}{q_k}$, đồng thời tìm từng $a_k$ bằng tìm kiếm nhị phân. Thuật toán khi đó phức tạp hơn một chút về mặt kỹ thuật, nhưng vẫn bảo đảm độ phức tạp $O(\log (p+q))$. Nói chung không thể cải thiện cận này, vì chỉ riêng số lượng số hạng đã là $\Theta(\log (p+q))$ trong trường hợp xấu nhất.

Để đạt cận này, mỗi $a_k$ phải được tìm bằng cách nhân đôi một giá trị ứng viên cho đến khi vượt quá, rồi mới tìm kiếm nhị phân trong khoảng cuối cùng. Việc này tốn $O(\log a_k)$ phép so sánh. Thay vào đó, tìm kiếm nhị phân mỗi $a_k$ trên một khoảng cố định sẽ tốn $O(\log (p+q))$ cho mỗi số hạng, dẫn đến cận tổng thể yếu hơn là $O(\log^2 (p+q))$.

Tổng khi đó là $O\left(\sum_k \left(1 + \log a_k\right)\right)$, và cả hai phần đều là $O(\log (p+q))$. Số lượng số hạng là $O(\log (p+q))$, vì $p_k$ và $q_k$ tăng ít nhất nhanh bằng các số Fibonacci, mức tăng chậm nhất đạt được khi mọi $a_k$ bằng $1$. Cộng hai công thức truy hồi trên cho $p_{k+1} + q_{k+1} = (p_{k-1} + q_{k-1}) + a_k (p_k + q_k) \geq a_k (p_k + q_k)$, nên $p + q \geq \prod_k a_k$ và do đó $\sum_k \log a_k \leq \log (p+q)$.

## Dãy Farey

Dãy Farey bậc $n$ là dãy các phân số từ $0$ đến $1$ được sắp xếp, có mẫu số không vượt quá $n$.

Các dãy được đặt theo tên nhà địa chất Anh John Farey, người năm 1816 phỏng đoán rằng mọi phân số trong một dãy Farey là phân số trung gian của hai phân số kề nó. Điều này được Cauchy chứng minh một thời gian sau, nhưng độc lập với cả hai người, nhà toán học Haros đã đi đến gần như cùng một kết luận năm 1802.

Bản thân các dãy Farey có nhiều tính chất thú vị, nhưng mối liên hệ với cây Stern-Brocot là rõ ràng nhất. Thực tế, có thể thu được các dãy Farey bằng cách cắt bớt các nhánh khỏi cây.

Từ thuật toán xây dựng cây Stern-Brocot, ta có thuật toán cho các dãy Farey. Bắt đầu với danh sách phân số $\frac{0}{1}, \frac{1}{0}$. Ở mỗi lần lặp tiếp theo, chỉ chèn phân số trung gian nếu mẫu số không vượt quá $n$. Đến một lúc danh sách sẽ ngừng thay đổi và ta tìm được dãy Farey mong muốn.

**Ghi chú bản dịch:** Theo định nghĩa ở trên, dãy Farey chỉ gồm các phân số trong đoạn từ 0 đến 1. Quá trình bắt đầu từ 0/1 và 1/0 như bài gốc mô tả còn chứa cận 1/0 và sinh cả các phân số lớn hơn 1; để thu được dãy Farey theo định nghĩa đó, có thể bắt đầu từ 0/1 và 1/1.

### Độ dài của dãy Farey

Một dãy Farey bậc $n$ chứa mọi phần tử của dãy Farey bậc $n-1$ cũng như mọi phân số tối giản có mẫu số $n$, mà số lượng các phân số sau chính là hàm phi Euler $\varphi(n)$. Do đó độ dài $L_n$ của dãy Farey bậc $n$ là

$$
    L_n = L_{n-1} + \varphi(n)
$$

hay tương đương, khai triển công thức truy hồi ta được

$$
    L_n = 1 + \sum_{k=1}^n \varphi(k).
$$
