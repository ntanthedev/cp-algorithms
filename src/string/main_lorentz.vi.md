---
tags:
  - Translated
e_maxx_link: string_tandems
translation:
  source: string/main_lorentz.md
  source_commit: 75cd8e80b96a9a49efce4d0192fd79ac5a36b732
  status: draft
  last_synced: 2026-11-16
---

# Tìm các đoạn lặp

Cho một chuỗi $s$ có độ dài $n$.

Một **đoạn lặp** là hai lần xuất hiện liên tiếp của cùng một chuỗi.
Nói cách khác, có thể mô tả một đoạn lặp bằng cặp chỉ số $i < j$ sao cho xâu con $s[i \dots j]$ gồm hai chuỗi giống hệt nhau viết liên tiếp.

Thử thách là **tìm tất cả các đoạn lặp** trong chuỗi $s$ cho trước.
Hoặc một bài toán đơn giản hơn: tìm **một** đoạn lặp bất kỳ hoặc tìm đoạn lặp **dài nhất**.

Thuật toán được mô tả ở đây do Main và Lorentz công bố năm 1982.

## Ví dụ

Xét các đoạn lặp trong chuỗi ví dụ sau:

$$acababaee$$

Chuỗi chứa ba đoạn lặp sau:

- $s[2 \dots 5] = abab$
- $s[3 \dots 6] = baba$
- $s[7 \dots 8] = ee$

Một ví dụ khác:

$$abaaba$$

Ở đây chỉ có hai đoạn lặp

- $s[0 \dots 5] = abaaba$
- $s[2 \dots 3] = aa$

## Số lượng đoạn lặp

Nói chung, một chuỗi độ dài $n$ có thể có tới $O(n^2)$ đoạn lặp.
Một ví dụ rõ ràng là chuỗi gồm $n$ lần cùng một chữ cái: khi đó mọi xâu con có độ dài chẵn đều là đoạn lặp.
Nói chung, bất kỳ chuỗi tuần hoàn nào có chu kỳ ngắn đều chứa nhiều đoạn lặp.

Mặt khác, điều này không ngăn ta tính số đoạn lặp trong thời gian $O(n \log n)$, vì thuật toán có thể đưa ra các đoạn lặp dưới dạng nén, mỗi lần biểu diễn một nhóm nhiều đoạn.

Thậm chí có một khái niệm mô tả các nhóm xâu con tuần hoàn bằng các bộ bốn phần tử.
Người ta đã chứng minh số nhóm như vậy nhiều nhất là tuyến tính theo độ dài chuỗi.

Một số kết quả thú vị khác liên quan đến số lượng đoạn lặp:

  - Số đoạn lặp nguyên thủy (các đoạn mà mỗi nửa không phải đoạn lặp) không vượt quá $O(n \log n)$.
  - Nếu mã hóa các đoạn lặp bằng các bộ số (gọi là bộ ba Crochemore) $(i,~ p,~ r)$ (trong đó $i$ là vị trí bắt đầu, $p$ là độ dài xâu con lặp, còn $r$ là số lần lặp), thì có thể mô tả mọi đoạn lặp bằng $O(n \log n)$ bộ ba như vậy.
  - Các chuỗi Fibonacci được định nghĩa là
    
    \[\begin{align}
    t_0 &= a, \\\\
    t_1 &= b, \\\\
    t_i &= t_{i-1} + t_{i-2},
    \end{align}\]
    
    có tính tuần hoàn "mạnh".
    Số đoạn lặp trong chuỗi Fibonacci $f_i$, kể cả khi đã nén bằng bộ ba Crochemore, là $O(f_n \log f_n)$.
    Số đoạn lặp nguyên thủy cũng là $O(f_n \log f_n)$.

## Thuật toán Main-Lorentz

Ý tưởng của thuật toán Main-Lorentz là **chia để trị**.

Thuật toán chia chuỗi ban đầu thành hai nửa và dùng hai lời gọi đệ quy để tính số đoạn lặp nằm hoàn toàn trong từng nửa.
Sau đó là phần khó.
Thuật toán tìm tất cả các đoạn lặp bắt đầu ở nửa đầu và kết thúc ở nửa sau (ta gọi chúng là **đoạn lặp băng qua**).
Đây là phần cốt lõi của thuật toán Main-Lorentz và ta sẽ thảo luận chi tiết ở đây.

Độ phức tạp của các thuật toán chia để trị đã được nghiên cứu kỹ.
[Định lý tổng quát](https://en.wikipedia.org/wiki/Master_theorem_(analysis_of_algorithms)) cho biết ta sẽ có thuật toán $O(n \log n)$ nếu tìm được các đoạn lặp băng qua trong thời gian $O(n)$.

### Tìm các đoạn lặp băng qua

Ta muốn tìm tất cả các đoạn lặp bắt đầu ở nửa đầu chuỗi, gọi là $u$, và kết thúc ở nửa sau, gọi là $v$:

$$s = u + v$$

Độ dài của mỗi nửa xấp xỉ bằng độ dài của $s$ chia hai.

Xét một đoạn lặp bất kỳ và nhìn vào ký tự giữa (chính xác hơn là ký tự đầu tiên của nửa sau đoạn lặp).
Tức nếu đoạn lặp là xâu con $s[i \dots j]$, thì ký tự giữa ở vị trí $(i + j + 1) / 2$.

Ta gọi đoạn lặp là **trái** hoặc **phải** tùy ký tự này nằm trong chuỗi nào: $u$ hay $v$.
Nói cách khác, một chuỗi được gọi là trái nếu phần lớn của nó nằm trong $u$, ngược lại ta gọi nó là phải.

Bây giờ ta sẽ bàn cách tìm **tất cả các đoạn lặp trái**.
Có thể tìm tất cả các đoạn lặp phải theo cách tương tự.

Gọi độ dài đoạn lặp trái là $2l$ (tức mỗi nửa đoạn lặp có độ dài $l$).
Xét ký tự đầu tiên của đoạn lặp nằm trong chuỗi $v$ (nó ở vị trí $|u|$ trong chuỗi $s$).
Nó trùng với ký tự cách đó $l$ vị trí về trước; gọi vị trí này là $cntr$.

Ta cố định vị trí $cntr$ và **tìm mọi đoạn lặp tại vị trí** $cntr$ này.

Ví dụ:

$$c ~ \underset{cntr}{a} ~ c ~ | ~ a ~ d ~ a$$

Vạch đứng chia hai nửa.
Ở đây ta cố định vị trí $cntr = 1$ và tại vị trí này tìm được đoạn lặp $caca$.

Rõ ràng khi cố định vị trí $cntr$, ta đồng thời cố định độ dài của các đoạn lặp có thể có: $l = |u| - cntr$.
Khi đã biết cách tìm các đoạn lặp này, ta sẽ duyệt mọi giá trị có thể của $cntr$ từ $0$ đến $|u|-1$ và tìm tất cả các đoạn lặp trái băng qua có độ dài $l = |u|,~ |u|-1,~ \dots, 1$.

### Điều kiện cho các đoạn lặp trái băng qua

Vậy làm sao tìm mọi đoạn lặp như vậy với $cntr$ đã cố định?
Hãy nhớ rằng vẫn có thể có nhiều đoạn lặp như vậy.

Hãy xem lại một hình minh họa, lần này cho đoạn lặp $abcabc$:

$$\overbrace{a}^{l_1} ~ \overbrace{\underset{cntr}{b} ~ c}^{l_2} ~ \overbrace{a}^{l_1} ~ | ~ \overbrace{b ~ c}^{l_2}$$

Ở đây ta ký hiệu độ dài hai phần của đoạn lặp là $l_1$ và $l_2$:
$l_1$ là độ dài phần từ đầu đoạn lặp tới vị trí $cntr-1$, còn $l_2$ là độ dài phần từ $cntr$ tới cuối nửa đoạn lặp.
Tổng độ dài đoạn lặp là $2l = l_1 + l_2 + l_1 + l_2$.

Ta đưa ra các điều kiện **cần và đủ** để có một đoạn lặp tại vị trí $cntr$ với độ dài $2l = 2(l_1 + l_2) = 2(|u| - cntr)$:

- Gọi $k_1$ là số lớn nhất sao cho $k_1$ ký tự trước vị trí $cntr$ trùng với $k_1$ ký tự cuối của chuỗi $u$:
  
$$
u[cntr - k_1 \dots cntr - 1] = u[|u| - k_1 \dots |u| - 1]
$$
  
- Gọi $k_2$ là số lớn nhất sao cho $k_2$ ký tự bắt đầu tại vị trí $cntr$ trùng với $k_2$ ký tự đầu của chuỗi $v$:

$$  
  u[cntr \dots cntr + k_2 - 1] = v[0 \dots k_2 - 1]
$$
  
- Khi đó, ta có một đoạn lặp với mỗi cặp $(l_1,~ l_2)$ thỏa mãn

$$
  \begin{align}
  l_1 &\le k_1, \\\\
  l_2 &\le k_2. \\\\
  \end{align}
$$

Tóm lại:

- Ta cố định một vị trí $cntr$ cụ thể.
- Tất cả các đoạn lặp tìm được lúc này có độ dài $2l = 2(|u| - cntr)$.
  Có thể có nhiều đoạn lặp như vậy; chúng phụ thuộc vào độ dài $l_1$ và $l_2 = l - l_1$.
- Ta tìm $k_1$ và $k_2$ như mô tả ở trên.
- Khi đó các đoạn lặp phù hợp là những đoạn có độ dài hai phần $l_1$ và $l_2$ thỏa mãn các điều kiện:

$$
  \begin{align}
  l_1 + l_2 &= l = |u| - cntr \\\\
  l_1 &\le k_1, \\\\
  l_2 &\le k_2. \\\\
  \end{align}
$$

Vì vậy, phần còn lại chỉ là cách tính nhanh $k_1$ và $k_2$ cho mỗi vị trí $cntr$.
May mắn là ta có thể tính chúng trong $O(1)$ bằng [hàm Z](../string/z-function.md):

- Có thể tìm giá trị $k_1$ cho mỗi vị trí bằng cách tính hàm Z cho chuỗi $\overline{u}$ (tức chuỗi $u$ đảo ngược).
  Khi đó giá trị $k_1$ ứng với một $cntr$ cụ thể sẽ bằng giá trị tương ứng trong mảng hàm Z.
- Để tính trước mọi giá trị $k_2$, ta tính hàm Z cho chuỗi $v + \# + u$ (tức chuỗi $u$ nối với ký tự phân cách $\#$ và chuỗi $v$).
  Một lần nữa, ta chỉ cần tra giá trị tương ứng trong hàm Z để lấy $k_2$.

**Ghi chú bản dịch:** Ở gạch đầu dòng thứ hai, công thức và phần mô tả bằng lời trong nguồn ghi thứ tự ghép ngược nhau; cài đặt bên dưới dùng v, ký tự phân cách, rồi u.

Như vậy là đủ để tìm mọi đoạn lặp trái băng qua.

### Các đoạn lặp phải băng qua

Để tính các đoạn lặp phải băng qua, ta làm tương tự:
định nghĩa tâm $cntr$ là ký tự tương ứng với ký tự cuối cùng trong chuỗi $u$.

Khi đó độ dài $k_1$ được định nghĩa là số ký tự lớn nhất trước vị trí $cntr$ (kể cả vị trí đó) trùng với các ký tự cuối của chuỗi $u$.
Độ dài $k_2$ được định nghĩa là số ký tự lớn nhất bắt đầu từ $cntr + 1$ trùng với các ký tự của chuỗi $v$.

Như vậy ta có thể tìm các giá trị $k_1$ và $k_2$ bằng cách tính hàm Z cho các chuỗi $\overline{u} + \# + \overline{v}$ và $v$.

Sau đó ta tìm các đoạn lặp bằng cách xét mọi vị trí $cntr$ và dùng cùng điều kiện như đối với các đoạn lặp trái băng qua.

### Cài đặt

Cài đặt của thuật toán Main-Lorentz tìm mọi đoạn lặp dưới dạng các bộ bốn đặc biệt: $(cntr,~ l,~ k_1,~ k_2)$ trong thời gian $O(n \log n)$.
Nếu chỉ muốn tìm số đoạn lặp trong chuỗi hoặc chỉ muốn tìm đoạn lặp dài nhất, thông tin này là đủ và thời gian chạy vẫn là $O(n \log n)$.

Lưu ý rằng nếu muốn khai triển các bộ này để lấy vị trí bắt đầu và kết thúc của từng đoạn lặp thì thời gian chạy sẽ là $O(n^2)$ (nhớ rằng có thể có $O(n^2)$ đoạn lặp).
Trong cài đặt này, ta sẽ làm vậy và lưu tất cả các đoạn lặp tìm được trong một vector các cặp chỉ số bắt đầu và kết thúc.

**Ghi chú bản dịch:** Cài đặt dưới đây cần chuỗi đầu vào không rỗng và không chứa ký tự phân cách #. Với chuỗi rỗng, điều kiện dừng không được thỏa nên lời gọi đệ quy không kết thúc; nếu chuỗi chứa ký tự phân cách, kết quả có thể sai.

```{.cpp file=main_lorentz}
vector<int> z_function(string const& s) {
    int n = s.size();
    vector<int> z(n);
    for (int i = 1, l = 0, r = 0; i < n; i++) {
        if (i <= r)
            z[i] = min(r-i+1, z[i-l]);
        while (i + z[i] < n && s[z[i]] == s[i+z[i]])
            z[i]++;
        if (i + z[i] - 1 > r) {
            l = i;
            r = i + z[i] - 1;
        }
    }
    return z;
}

int get_z(vector<int> const& z, int i) {
    if (0 <= i && i < (int)z.size())
        return z[i];
    else
        return 0;
}

vector<pair<int, int>> repetitions;

void convert_to_repetitions(int shift, bool left, int cntr, int l, int k1, int k2) {
    for (int l1 = max(1, l - k2); l1 <= min(l, k1); l1++) {
        if (left && l1 == l) break;
        int l2 = l - l1;
        int pos = shift + (left ? cntr - l1 : cntr - l - l1 + 1);
        repetitions.emplace_back(pos, pos + 2*l - 1);
    }
}

void find_repetitions(string s, int shift = 0) {
    int n = s.size();
    if (n == 1)
        return;

    int nu = n / 2;
    int nv = n - nu;
    string u = s.substr(0, nu);
    string v = s.substr(nu);
    string ru(u.rbegin(), u.rend());
    string rv(v.rbegin(), v.rend());

    find_repetitions(u, shift);
    find_repetitions(v, shift + nu);

    vector<int> z1 = z_function(ru);
    vector<int> z2 = z_function(v + '#' + u);
    vector<int> z3 = z_function(ru + '#' + rv);
    vector<int> z4 = z_function(v);

    for (int cntr = 0; cntr < n; cntr++) {
        int l, k1, k2;
        if (cntr < nu) {
            l = nu - cntr;
            k1 = get_z(z1, nu - cntr);
            k2 = get_z(z2, nv + 1 + cntr);
        } else {
            l = cntr - nu + 1;
            k1 = get_z(z3, nu + 1 + nv - 1 - (cntr - nu));
            k2 = get_z(z4, (cntr - nu) + 1);
        }
        if (k1 + k2 >= l)
            convert_to_repetitions(shift, cntr < nu, cntr, l, k1, k2);
    }
}
```
