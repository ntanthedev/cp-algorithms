---
tags:
  - Translated
translation:
  source: algebra/fft.md
  source_commit: 38ed620a54a9749b2abee3f035d48e9f2f91b56f
  status: draft
  last_synced: 2026-11-17
e_maxx_link: fft_multiply
---

# Biến đổi Fourier nhanh

Trong bài này, ta sẽ xét một thuật toán nhân hai đa thức có độ dài $n$ trong thời gian $O(n \log n)$, tốt hơn cách nhân trực tiếp cần $O(n^2)$ thời gian.
Ta cũng có thể quy phép nhân hai số lớn về phép nhân đa thức, vì vậy có thể nhân hai số lớn trong thời gian $O(n \log n)$ (với $n$ là số chữ số của các số đó).

Việc phát hiện **biến đổi Fourier nhanh (FFT)** thường được ghi công cho Cooley và Tukey, những người đã công bố một thuật toán vào năm 1965.
Thực ra FFT đã được phát hiện nhiều lần trước đó, nhưng tầm quan trọng của nó chưa được nhận ra trước khi máy tính hiện đại ra đời.
Một số nhà nghiên cứu ghi công phát hiện FFT cho Runge và König vào năm 1924.
Tuy nhiên, Gauss thực sự đã phát triển một phương pháp như vậy từ năm 1805 nhưng chưa từng công bố.

Lưu ý rằng thuật toán FFT trình bày ở đây chạy trong thời gian $O(n \log n)$, nhưng không thể dùng để nhân đa thức có kích thước và hệ số lớn tùy ý hoặc nhân các số nguyên lớn tùy ý.
Thuật toán có thể dễ dàng xử lý các đa thức kích thước $10^5$ với hệ số nhỏ hoặc nhân hai số kích thước $10^6$, thường là đủ cho các bài toán lập trình thi đấu. Khi nhân các số có nhiều hơn cỡ $10^6$ bit, miền giá trị và độ chính xác của số dấu phẩy động trong quá trình tính sẽ không còn đủ để cho kết quả cuối chính xác, dù có những biến thể phức tạp hơn có thể nhân đa thức hoặc số nguyên lớn tùy ý.
Ví dụ, năm 1971 Schönhage và Strasser phát triển một biến thể nhân các số lớn tùy ý, áp dụng FFT đệ quy trong các cấu trúc vành với thời gian $O(n \log n \log \log n)$.
Gần đây hơn, vào năm 2019, Harvey và van der Hoeven đã công bố một thuật toán thực sự chạy trong $O(n \log n)$.

## Biến đổi Fourier rời rạc

Cho một đa thức bậc $n - 1$:

$$A(x) = a_0 x^0 + a_1 x^1 + \dots + a_{n-1} x^{n-1}$$

Không mất tính tổng quát, giả sử $n$ — số hệ số — là một lũy thừa của $2$.
Nếu $n$ không phải lũy thừa của $2$, ta chỉ cần thêm các số hạng còn thiếu $a_i x^i$ và đặt hệ số $a_i$ bằng $0$.

Theo lý thuyết số phức, phương trình $x^n = 1$ có $n$ nghiệm phức (gọi là các căn bậc $n$ của đơn vị), có dạng $w_{n, k} = e^{\frac{2 k \pi i}{n}}$ với $k = 0 \dots n-1$.
Những số phức này còn có một số tính chất thú vị:
chẳng hạn căn bậc $n$ chính $w_n = w_{n, 1} = e^{\frac{2 \pi i}{n}}$ có thể biểu diễn mọi căn bậc $n$ còn lại: $w_{n, k} = (w_n)^k$.

**Biến đổi Fourier rời rạc (DFT)** của đa thức $A(x)$ (hay tương đương là vector hệ số $(a_0, a_1, \dots, a_{n-1})$) được định nghĩa là các giá trị của đa thức tại những điểm $x = w_{n, k}$, tức là vector:

$$\begin{align}
\text{DFT}(a_0, a_1, \dots, a_{n-1}) &= (y_0, y_1, \dots, y_{n-1}) \\
&= (A(w_{n, 0}), A(w_{n, 1}), \dots, A(w_{n, n-1})) \\
&= (A(w_n^0), A(w_n^1), \dots, A(w_n^{n-1}))
\end{align}$$

Tương tự, **biến đổi Fourier rời rạc ngược** được định nghĩa như sau:
DFT ngược của các giá trị đa thức $(y_0, y_1, \dots, y_{n-1})$ là các hệ số của đa thức $(a_0, a_1, \dots, a_{n-1})$.

$$\text{InverseDFT}(y_0, y_1, \dots, y_{n-1}) = (a_0, a_1, \dots, a_{n-1})$$

Như vậy, nếu DFT thuận tính giá trị của đa thức tại các căn bậc $n$, thì DFT ngược có thể khôi phục hệ số của đa thức từ những giá trị đó.

### Ứng dụng DFT: nhân đa thức nhanh

Cho hai đa thức $A$ và $B$.
Ta tính DFT cho từng đa thức: $\text{DFT}(A)$ và $\text{DFT}(B)$.

Điều gì xảy ra khi nhân hai đa thức này?
Tại mỗi điểm, các giá trị của chúng được nhân với nhau, tức là

$$(A \cdot B)(x) = A(x) \cdot B(x).$$

Điều này có nghĩa là nếu nhân các vector $\text{DFT}(A)$ và $\text{DFT}(B)$ — bằng cách nhân từng phần tử của một vector với phần tử tương ứng của vector kia — ta thu được chính DFT của đa thức $\text{DFT}(A \cdot B)$:

$$\text{DFT}(A \cdot B) = \text{DFT}(A) \cdot \text{DFT}(B)$$

Cuối cùng, áp dụng DFT ngược, ta thu được:

$$A \cdot B = \text{InverseDFT}(\text{DFT}(A) \cdot \text{DFT}(B))$$

Ở vế phải, tích của hai DFT được hiểu là tích từng cặp phần tử tương ứng của hai vector.
Có thể tính tích này trong thời gian $O(n)$.
Nếu tính được DFT và DFT ngược trong $O(n \log n)$, ta cũng tính được tích của hai đa thức (và do đó cả hai số lớn) với cùng độ phức tạp.

Cần lưu ý rằng hai đa thức phải có cùng bậc.
Nếu không, hai vector kết quả DFT sẽ có độ dài khác nhau.
Ta có thể làm điều này bằng cách thêm các hệ số có giá trị $0$.

Ngoài ra, do tích của hai đa thức là một đa thức bậc $2 (n - 1)$, ta cần tăng gấp đôi bậc của mỗi đa thức (vẫn bằng cách đệm các số $0$).
Từ một vector có $n$ giá trị, ta không thể khôi phục đa thức cần tìm với $2n - 1$ hệ số.

### Biến đổi Fourier nhanh

**Biến đổi Fourier nhanh** là phương pháp cho phép tính DFT trong thời gian $O(n \log n)$.
Ý tưởng cơ bản của FFT là áp dụng chia để trị.
Ta chia vector hệ số của đa thức thành hai vector, tính DFT đệ quy cho từng vector, rồi kết hợp các kết quả để tính DFT của toàn bộ đa thức.

Xét đa thức $A(x)$ bậc $n - 1$, trong đó $n$ là một lũy thừa của $2$ và $n > 1$:

$$A(x) = a_0 x^0 + a_1 x^1 + \dots + a_{n-1} x^{n-1}$$

Ta chia nó thành hai đa thức nhỏ hơn: một đa thức chỉ chứa các hệ số ở vị trí chẵn, đa thức còn lại chứa các hệ số ở vị trí lẻ:

$$\begin{align}
A_0(x) &= a_0 x^0 + a_2 x^1 + \dots + a_{n-2} x^{\frac{n}{2}-1} \\
A_1(x) &= a_1 x^0 + a_3 x^1 + \dots + a_{n-1} x^{\frac{n}{2}-1}
\end{align}$$

Dễ thấy rằng

$$A(x) = A_0(x^2) + x A_1(x^2).$$

Hai đa thức $A_0$ và $A_1$ chỉ có số hệ số bằng một nửa đa thức $A$.
Nếu tính được $\text{DFT}(A)$ trong thời gian tuyến tính từ $\text{DFT}(A_0)$ và $\text{DFT}(A_1)$, ta có hệ thức truy hồi độ phức tạp $T_{\text{DFT}}(n) = 2 T_{\text{DFT}}\left(\frac{n}{2}\right) + O(n)$, từ đó suy ra $T_{\text{DFT}}(n) = O(n \log n)$ theo **định lý chủ** (master theorem).

Hãy xem cách thực hiện điều đó.

Giả sử đã tính các vector $\left(y_k^0\right)_{k=0}^{n/2-1} = \text{DFT}(A_0)$ và $\left(y_k^1\right)_{k=0}^{n/2-1} = \text{DFT}(A_1)$.
Ta sẽ tìm biểu thức cho $\left(y_k\right)_{k=0}^{n-1} = \text{DFT}(A)$.

Với $\frac{n}{2}$ giá trị đầu, ta có thể dùng ngay đẳng thức đã nêu $A(x) = A_0(x^2) + x A_1(x^2)$:

$$y_k = y_k^0 + w_n^k y_k^1, \quad k = 0 \dots \frac{n}{2} - 1.$$

Tuy nhiên với $\frac{n}{2}$ giá trị sau, ta cần tìm một biểu thức hơi khác:

$$\begin{align}
y_{k+n/2} &= A\left(w_n^{k+n/2}\right) \\
&= A_0\left(w_n^{2k+n}\right) + w_n^{k + n/2} A_1\left(w_n^{2k+n}\right) \\
&= A_0\left(w_n^{2k} w_n^n\right) + w_n^k w_n^{n/2} A_1\left(w_n^{2k} w_n^n\right) \\
&= A_0\left(w_n^{2k}\right) - w_n^k A_1\left(w_n^{2k}\right) \\
&= y_k^0 - w_n^k y_k^1
\end{align}$$

Ở đây ta lại dùng $A(x) = A_0(x^2) + x A_1(x^2)$ cùng hai đẳng thức $w_n^n = 1$ và $w_n^{n/2} = -1$.

Do đó, ta nhận được các công thức cần tìm để tính toàn bộ vector $(y_k)$:

$$\begin{align}
y_k &= y_k^0 + w_n^k y_k^1, &\quad k = 0 \dots \frac{n}{2} - 1, \\
y_{k+n/2} &= y_k^0 - w_n^k y_k^1, &\quad k = 0 \dots \frac{n}{2} - 1.
\end{align}$$

(Mẫu phép tính $a + b$ và $a - b$ này đôi khi được gọi là **butterfly**.)

Vậy ta đã biết cách tính DFT trong thời gian $O(n \log n)$.

### FFT ngược

Cho vector $(y_0, y_1, \dots y_{n-1})$ gồm các giá trị của đa thức $A$ bậc $n - 1$ tại những điểm $x = w_n^k$.
Ta muốn khôi phục các hệ số $(a_0, a_1, \dots, a_{n-1})$ của đa thức.
Bài toán quen thuộc này được gọi là **nội suy** (interpolation), và có các thuật toán tổng quát để giải.
Nhưng trong trường hợp đặc biệt này, vì đã biết giá trị tại các căn của đơn vị, ta có một thuật toán đơn giản hơn nhiều, gần như giống FFT thuận.

Theo định nghĩa, ta có thể viết DFT dưới dạng ma trận:

$$
\begin{pmatrix}
w_n^0 & w_n^0 & w_n^0 & w_n^0 & \cdots & w_n^0 \\
w_n^0 & w_n^1 & w_n^2 & w_n^3 & \cdots & w_n^{n-1} \\
w_n^0 & w_n^2 & w_n^4 & w_n^6 & \cdots & w_n^{2(n-1)} \\
w_n^0 & w_n^3 & w_n^6 & w_n^9 & \cdots & w_n^{3(n-1)} \\
\vdots & \vdots & \vdots & \vdots & \ddots & \vdots \\
w_n^0 & w_n^{n-1} & w_n^{2(n-1)} & w_n^{3(n-1)} & \cdots & w_n^{(n-1)(n-1)}
\end{pmatrix} \begin{pmatrix}
a_0 \\ a_1 \\ a_2 \\ a_3 \\ \vdots \\ a_{n-1}
\end{pmatrix} = \begin{pmatrix}
y_0 \\ y_1 \\ y_2 \\ y_3 \\ \vdots \\ y_{n-1}
\end{pmatrix}
$$

Ma trận này được gọi là **ma trận Vandermonde**.

Do đó ta có thể tính vector $(a_0, a_1, \dots, a_{n-1})$ bằng cách nhân ma trận nghịch đảo với vector $(y_0, y_1, \dots y_{n-1})$ đặt bên phải:

$$
\begin{pmatrix}
a_0 \\ a_1 \\ a_2 \\ a_3 \\ \vdots \\ a_{n-1}
\end{pmatrix} = \begin{pmatrix}
w_n^0 & w_n^0 & w_n^0 & w_n^0 & \cdots & w_n^0 \\
w_n^0 & w_n^1 & w_n^2 & w_n^3 & \cdots & w_n^{n-1} \\
w_n^0 & w_n^2 & w_n^4 & w_n^6 & \cdots & w_n^{2(n-1)} \\
w_n^0 & w_n^3 & w_n^6 & w_n^9 & \cdots & w_n^{3(n-1)} \\
\vdots & \vdots & \vdots & \vdots & \ddots & \vdots \\
w_n^0 & w_n^{n-1} & w_n^{2(n-1)} & w_n^{3(n-1)} & \cdots & w_n^{(n-1)(n-1)}
\end{pmatrix}^{-1} \begin{pmatrix}
y_0 \\ y_1 \\ y_2 \\ y_3 \\ \vdots \\ y_{n-1}
\end{pmatrix}
$$

Có thể kiểm tra nhanh rằng ma trận nghịch đảo có dạng sau:

$$
\frac{1}{n}
\begin{pmatrix}
w_n^0 & w_n^0 & w_n^0 & w_n^0 & \cdots & w_n^0 \\
w_n^0 & w_n^{-1} & w_n^{-2} & w_n^{-3} & \cdots & w_n^{-(n-1)} \\
w_n^0 & w_n^{-2} & w_n^{-4} & w_n^{-6} & \cdots & w_n^{-2(n-1)} \\
w_n^0 & w_n^{-3} & w_n^{-6} & w_n^{-9} & \cdots & w_n^{-3(n-1)} \\
\vdots & \vdots & \vdots & \vdots & \ddots & \vdots \\
w_n^0 & w_n^{-(n-1)} & w_n^{-2(n-1)} & w_n^{-3(n-1)} & \cdots & w_n^{-(n-1)(n-1)}
\end{pmatrix}
$$

Từ đó ta có công thức:

$$a_k = \frac{1}{n} \sum_{j=0}^{n-1} y_j w_n^{-k j}$$

So sánh với công thức tính $y_k$

$$y_k = \sum_{j=0}^{n-1} a_j w_n^{k j},$$

ta thấy hai bài toán gần như giống nhau, nên các hệ số $a_k$ có thể được tìm bằng cùng thuật toán chia để trị như FFT thuận, chỉ khác là dùng $w_n^{-k}$ thay cho $w_n^k$, và cuối cùng chia các hệ số thu được cho $n$.

Vì vậy, cách tính DFT ngược gần như giống DFT thuận và cũng thực hiện được trong $O(n \log n)$ thời gian.

### Cài đặt

Dưới đây là một **cài đặt FFT** đệ quy đơn giản và FFT ngược trong cùng một hàm, vì hai phép biến đổi chỉ khác nhau rất ít.
Ta dùng kiểu complex trong STL của C++ để lưu số phức.

```{.cpp file=fft_recursive}
using cd = complex<double>;
const double PI = acos(-1);

void fft(vector<cd> & a, bool invert) {
    int n = a.size();
    if (n == 1)
        return;

    vector<cd> a0(n / 2), a1(n / 2);
    for (int i = 0; 2 * i < n; i++) {
        a0[i] = a[2*i];
        a1[i] = a[2*i+1];
    }
    fft(a0, invert);
    fft(a1, invert);

    double ang = 2 * PI / n * (invert ? -1 : 1);
    cd w(1), wn(cos(ang), sin(ang));
    for (int i = 0; 2 * i < n; i++) {
        a[i] = a0[i] + w * a1[i];
        a[i + n/2] = a0[i] - w * a1[i];
        if (invert) {
            a[i] /= 2;
            a[i + n/2] /= 2;
        }
        w *= wn;
    }
}
```

Hàm nhận một vector hệ số, tính DFT hoặc DFT ngược rồi lưu kết quả vào chính vector đó.
Tham số $\text{invert}$ cho biết cần tính DFT thuận hay DFT ngược.
Trong hàm, trước tiên ta kiểm tra độ dài vector có bằng một không; nếu có thì không cần làm gì.
Nếu không, ta chia vector $a$ thành hai vector $a0$ và $a1$ rồi tính DFT cho cả hai bằng đệ quy.
Tiếp theo, ta khởi tạo giá trị $wn$ và biến $w$ để lưu lũy thừa hiện tại của $wn$.
Sau đó các giá trị của DFT kết quả được tính theo những công thức trên.

Nếu cờ $\text{invert}$ được bật, ta thay $wn$ bằng $wn^{-1}$ và chia mỗi giá trị kết quả cho $2$ (vì việc này được thực hiện ở mỗi mức đệ quy nên cuối cùng các giá trị sẽ được chia cho $n$).

Dùng hàm này, ta có thể tạo hàm **nhân hai đa thức**:

```{.cpp file=fft_multiply}
vector<int> multiply(vector<int> const& a, vector<int> const& b) {
    vector<cd> fa(a.begin(), a.end()), fb(b.begin(), b.end());
    int n = 1;
    while (n < a.size() + b.size()) 
        n <<= 1;
    fa.resize(n);
    fb.resize(n);

    fft(fa, false);
    fft(fb, false);
    for (int i = 0; i < n; i++)
        fa[i] *= fb[i];
    fft(fa, true);

    vector<int> result(n);
    for (int i = 0; i < n; i++)
        result[i] = round(fa[i].real());
    return result;
}
```

Hàm này hoạt động với đa thức có hệ số nguyên, nhưng cũng có thể điều chỉnh cho các kiểu khác.
Do tính toán với số phức có sai số, ta cần làm tròn các hệ số kết quả ở cuối.

Cuối cùng, hàm **nhân** hai số lớn gần như không khác hàm nhân đa thức.
Việc duy nhất cần làm sau đó là chuẩn hóa số:

```cpp
    int carry = 0;
    for (int i = 0; i < n; i++)
        result[i] += carry;
        carry = result[i] / 10;
        result[i] %= 10;
    }
```

**Ghi chú bản dịch:** Đoạn mã nguồn trên thiếu dấu ngoặc nhọn mở sau vòng lặp. Vì vậy chỉ phép cộng đầu tiên thuộc vòng lặp; biến chỉ số nằm ngoài phạm vi ở hai dòng tiếp theo và dấu ngoặc đóng không có dấu mở tương ứng.

Vì độ dài tích của hai số không bao giờ vượt quá tổng độ dài của chúng, kích thước vector đủ để thực hiện mọi phép nhớ.

### Cải tiến cài đặt: tính toán tại chỗ

Để tăng hiệu quả, ta chuyển từ cài đặt đệ quy sang cài đặt lặp.
Trong cài đặt đệ quy ở trên, ta tách tường minh vector $a$ thành hai vector: các phần tử ở vị trí chẵn được gán vào một vector tạm, còn các phần tử ở vị trí lẻ vào vector kia.
Tuy nhiên, nếu sắp xếp lại các phần tử theo một cách nhất định, ta không cần tạo các vector tạm này (nghĩa là có thể thực hiện mọi phép tính “tại chỗ”, ngay trong vector $A$).

Ở mức đệ quy đầu tiên, các phần tử có bit thấp nhất của vị trí bằng không được gán vào vector $a_0$, còn những phần tử có bit thấp nhất bằng một được gán vào $a_1$.
Ở mức đệ quy thứ hai cũng vậy, nhưng xét bit thấp thứ hai, và tiếp tục tương tự.
Vì thế, nếu đảo ngược các bit trong vị trí của từng hệ số rồi sắp xếp theo các giá trị đã đảo này, ta nhận được thứ tự mong muốn, gọi là hoán vị đảo bit.

Ví dụ, thứ tự mong muốn với $n = 8$ có dạng:

$$a = \bigg\{ \Big[ (a_0, a_4), (a_2, a_6) \Big], \Big[ (a_1, a_5), (a_3, a_7) \Big] \bigg\}$$

Thật vậy, ở mức đệ quy đầu tiên (được bao bởi ngoặc nhọn), vector được chia thành hai phần $[a_0, a_2, a_4, a_6]$ và $[a_1, a_3, a_5, a_7]$.
Trong hoán vị đảo bit, điều này tương ứng với việc chia vector thành hai nửa: $\frac{n}{2}$ phần tử đầu và $\frac{n}{2}$ phần tử cuối.
Sau đó ta gọi đệ quy cho mỗi nửa.
Giả sử DFT thu được của mỗi nửa được trả về ngay tại vị trí các phần tử của nửa đó (tương ứng là nửa đầu và nửa sau của vector $a$).

$$a = \bigg\{ \Big[y_0^0, y_1^0, y_2^0, y_3^0\Big], \Big[y_0^1, y_1^1, y_2^1, y_3^1 \Big] \bigg\}$$

Giờ ta muốn kết hợp hai DFT thành một DFT cho toàn bộ vector.
Thứ tự các phần tử đã phù hợp, và ta cũng có thể thực hiện phép kết hợp ngay trong vector này.
Ta có thể lấy các phần tử $y_0^0$ và $y_0^1$ rồi thực hiện phép biến đổi butterfly.
Hai giá trị thu được nằm tại vị trí của hai giá trị ban đầu, do đó ta có:

$$a = \bigg\{ \Big[y_0^0 + w_n^0 y_0^1, y_1^0, y_2^0, y_3^0\Big], \Big[y_0^0 - w_n^0 y_0^1, y_1^1, y_2^1, y_3^1\Big] \bigg\}$$

Tương tự, ta tính phép biến đổi butterfly cho $y_1^0$ và $y_1^1$, đặt kết quả vào vị trí của chúng, rồi tiếp tục như vậy.
Kết quả là:

$$a = \bigg\{ \Big[y_0^0 + w_n^0 y_0^1, y_1^0 + w_n^1 y_1^1, y_2^0 + w_n^2 y_2^1, y_3^0 + w_n^3 y_3^1\Big], \Big[y_0^0 - w_n^0 y_0^1, y_1^0 - w_n^1 y_1^1, y_2^0 - w_n^2 y_2^1, y_3^0 - w_n^3 y_3^1\Big] \bigg\}$$

Như vậy ta đã tính được DFT cần tìm từ vector $a$.

Ở đây ta chỉ mô tả quá trình tính DFT tại mức đệ quy đầu tiên, nhưng cách làm tương tự cũng áp dụng cho mọi mức khác.
Vì vậy, sau khi áp dụng hoán vị đảo bit, ta có thể tính DFT tại chỗ mà không cần thêm bộ nhớ.

Điều này còn cho phép loại bỏ đệ quy.
Ta bắt đầu từ mức thấp nhất, tức là chia vector thành các cặp và áp dụng phép biến đổi butterfly cho chúng.
Khi đó ta có vector $a$ sau khi đã thực hiện công việc của mức cuối.
Ở bước tiếp theo, ta chia vector thành các vector kích thước $4$ và tiếp tục áp dụng phép biến đổi butterfly, thu được DFT cho từng khối kích thước $4$.
Cứ tiếp tục như vậy.
Cuối cùng, ở bước cuối, ta có kết quả DFT của hai nửa $a$; áp dụng phép biến đổi butterfly sẽ cho DFT của toàn bộ vector $a$.

```{.cpp file=fft_implementation_iterative}
using cd = complex<double>;
const double PI = acos(-1);

int reverse(int num, int lg_n) {
    int res = 0;
    for (int i = 0; i < lg_n; i++) {
        if (num & (1 << i))
            res |= 1 << (lg_n - 1 - i);
    }
    return res;
}

void fft(vector<cd> & a, bool invert) {
    int n = a.size();
    int lg_n = 0;
    while ((1 << lg_n) < n)
        lg_n++;

    for (int i = 0; i < n; i++) {
        if (i < reverse(i, lg_n))
            swap(a[i], a[reverse(i, lg_n)]);
    }

    for (int len = 2; len <= n; len <<= 1) {
        double ang = 2 * PI / len * (invert ? -1 : 1);
        cd wlen(cos(ang), sin(ang));
        for (int i = 0; i < n; i += len) {
            cd w(1);
            for (int j = 0; j < len / 2; j++) {
                cd u = a[i+j], v = a[i+j+len/2] * w;
                a[i+j] = u + v;
                a[i+j+len/2] = u - v;
                w *= wlen;
            }
        }
    }

    if (invert) {
        for (cd & x : a)
            x /= n;
    }
}
```

Đầu tiên ta áp dụng hoán vị đảo bit bằng cách đổi chỗ mỗi phần tử với phần tử ở vị trí đảo bit của nó.
Sau đó, ở $\log n - 1$ giai đoạn của thuật toán, ta tính DFT cho từng khối có kích thước tương ứng $\text{len}$.
Mọi khối này đều dùng cùng căn của đơn vị $\text{wlen}$.
Ta duyệt qua tất cả các khối và thực hiện phép biến đổi butterfly trên từng khối.

**Ghi chú bản dịch:** Với độ dài là lũy thừa của 2, vòng lặp trên chạy qua các kích thước 2, 4, …, n, nên số giai đoạn là logarit cơ số 2 của n. Chẳng hạn, với n bằng 8 có ba giai đoạn, không phải hai.

Ta có thể tiếp tục tối ưu việc đảo bit.
Trong cài đặt trước, ta duyệt từng bit của chỉ số để tạo chỉ số có thứ tự bit đảo ngược.
Tuy nhiên, có một cách khác để đảo bit.

Giả sử $j$ đã chứa dạng đảo bit của $i$.
Khi chuyển sang $i + 1$, ta cần tăng $i$ và cũng phải tăng $j$, nhưng trong một hệ đếm “đảo ngược”.
Cộng một trong hệ nhị phân thông thường tương đương đổi mọi bit một ở cuối thành không, rồi đổi bit không ngay trước chúng thành một.
Tương tự, trong hệ đếm “đảo ngược”, ta đổi mọi bit một ở đầu, rồi đổi cả bit không kế tiếp.

Từ đó có cài đặt sau:

```{.cpp file=fft_implementation_iterative_opt}
using cd = complex<double>;
const double PI = acos(-1);

void fft(vector<cd> & a, bool invert) {
    int n = a.size();

    for (int i = 1, j = 0; i < n; i++) {
        int bit = n >> 1;
        for (; j & bit; bit >>= 1)
            j ^= bit;
        j ^= bit;

        if (i < j)
            swap(a[i], a[j]);
    }

    for (int len = 2; len <= n; len <<= 1) {
        double ang = 2 * PI / len * (invert ? -1 : 1);
        cd wlen(cos(ang), sin(ang));
        for (int i = 0; i < n; i += len) {
            cd w(1);
            for (int j = 0; j < len / 2; j++) {
                cd u = a[i+j], v = a[i+j+len/2] * w;
                a[i+j] = u + v;
                a[i+j+len/2] = u - v;
                w *= wlen;
            }
        }
    }

    if (invert) {
        for (cd & x : a)
            x /= n;
    }
}
```

Ngoài ra, ta có thể tính trước hoán vị đảo bit.
Điều này đặc biệt hữu ích khi kích thước $n$ giống nhau trong mọi lần gọi.
Nhưng ngay cả khi chỉ có ba lần gọi, như khi nhân hai đa thức, hiệu quả vẫn đáng kể.
Ta cũng có thể tính trước mọi căn của đơn vị và các lũy thừa của chúng.

## Biến đổi lý thuyết số

Bây giờ ta thay đổi mục tiêu một chút.
Ta vẫn muốn nhân hai đa thức trong $O(n \log n)$ thời gian, nhưng lần này cần tính các hệ số theo modulo một số nguyên tố $p$.
Dĩ nhiên ta có thể dùng DFT thông thường rồi lấy modulo kết quả.
Tuy nhiên, cách này có thể dẫn đến sai số làm tròn, đặc biệt khi xử lý các số lớn.
**Biến đổi lý thuyết số (NTT)** có ưu điểm là chỉ làm việc với số nguyên, do đó kết quả được đảm bảo chính xác.
 
Biến đổi Fourier rời rạc dựa trên số phức và các căn bậc $n$ của đơn vị.
Để tính hiệu quả, ta sử dụng nhiều tính chất của các căn này, chẳng hạn tồn tại một căn sinh ra mọi căn khác bằng phép nâng lũy thừa.

Nhưng những tính chất tương tự cũng đúng với các căn bậc $n$ của đơn vị trong số học modulo.
Một căn bậc $n$ của đơn vị trên trường nguyên tố là số $w_n$ thỏa mãn:

$$\begin{align}
(w_n)^n &= 1 \pmod{p}, \\
(w_n)^k &\ne 1 \pmod{p}, \quad 1 \le k < n.
\end{align}$$

Có thể thu được $n-1$ căn còn lại dưới dạng các lũy thừa của căn $w_n$.

Để áp dụng vào thuật toán FFT, ta cần có căn cho một giá trị $n$ là lũy thừa của $2$ và cho mọi lũy thừa nhỏ hơn.
Ta nhận thấy tính chất thú vị sau:

$$\begin{align}
(w_n^2)^m = w_n^n &= 1 \pmod{p}, \quad \text{with } m = \frac{n}{2}\\
(w_n^2)^k = w_n^{2k} &\ne 1 \pmod{p}, \quad 1 \le k < m.
\end{align}$$

Như vậy nếu $w_n$ là một căn bậc $n$ của đơn vị thì $w_n^2$ là một căn bậc $\frac{n}{2}$ của đơn vị.
Do đó, với mọi lũy thừa nhỏ hơn của hai đều tồn tại căn có bậc cần thiết, và có thể tính chúng từ $w_n$.

Để tính DFT ngược, ta cần phần tử nghịch đảo $w_n^{-1}$ của $w_n$.
Với modulo nguyên tố, phần tử nghịch đảo luôn tồn tại.

Như vậy, mọi tính chất cần dùng của căn phức cũng có trong số học modulo, miễn là ta có modulo $p$ đủ lớn sao cho tồn tại căn bậc $n$ của đơn vị.

Ví dụ, ta có thể lấy modulo $p = 7340033$, $w_{2^{20}} = 5$.
Nếu modulo này chưa đủ, ta cần tìm một cặp khác.
Ta có thể dùng thực tế rằng với modulo dạng $p = c 2^k + 1$ (và $p$ là số nguyên tố), luôn tồn tại căn bậc $2^k$ của đơn vị.
Có thể chứng minh $g^c$ là một căn bậc $2^k$ của đơn vị như vậy, trong đó $g$ là một [căn nguyên thủy](primitive-root.md) của $p$.

```{.cpp file=fft_implementation_modular_arithmetic}
const int mod = 7340033;
const int root = 5;
const int root_1 = 4404020;
const int root_pw = 1 << 20;

void fft(vector<int> & a, bool invert) {
    int n = a.size();

    for (int i = 1, j = 0; i < n; i++) {
        int bit = n >> 1;
        for (; j & bit; bit >>= 1)
            j ^= bit;
        j ^= bit;

        if (i < j)
            swap(a[i], a[j]);
    }

    for (int len = 2; len <= n; len <<= 1) {
        int wlen = invert ? root_1 : root;
        for (int i = len; i < root_pw; i <<= 1)
            wlen = (int)(1LL * wlen * wlen % mod);

        for (int i = 0; i < n; i += len) {
            int w = 1;
            for (int j = 0; j < len / 2; j++) {
                int u = a[i+j], v = (int)(1LL * a[i+j+len/2] * w % mod);
                a[i+j] = u + v < mod ? u + v : u + v - mod;
                a[i+j+len/2] = u - v >= 0 ? u - v : u - v + mod;
                w = (int)(1LL * w * wlen % mod);
            }
        }
    }

    if (invert) {
        int n_1 = inverse(n, mod);
        for (int & x : a)
            x = (int)(1LL * x * n_1 % mod);
    }
}
```

Ở đây hàm `inverse` tính nghịch đảo modulo (xem [Nghịch đảo modulo](module-inverse.md)).
Các hằng số `mod`, `root`, `root_pw` xác định modulo và căn, còn `root_1` là nghịch đảo của `root` theo modulo `mod`.

Trên thực tế, cài đặt này chậm hơn cài đặt dùng số phức do số lượng lớn phép lấy modulo, nhưng có một số ưu điểm như dùng ít bộ nhớ hơn và không có sai số làm tròn.

## Phép nhân với modulo tùy ý

Ta muốn đạt cùng mục tiêu như phần trước.
Đó là nhân hai đa thức $A(x)$ và $B(x)$, rồi tính các hệ số theo modulo một số $M$.
Biến đổi lý thuyết số chỉ hoạt động với một số số nguyên tố nhất định.
Nếu modulo không có dạng mong muốn thì sao?

Một cách là thực hiện nhiều phép biến đổi lý thuyết số với các số nguyên tố khác nhau có dạng $c 2^k + 1$, sau đó áp dụng [Định lý số dư Trung Hoa](chinese-remainder-theorem.md) để tính các hệ số cuối.

Một cách khác là tách mỗi đa thức $A(x)$ và $B(x)$ thành hai đa thức nhỏ hơn

$$\begin{align}
A(x) &= A_1(x) + A_2(x) \cdot C \\
B(x) &= B_1(x) + B_2(x) \cdot C
\end{align}$$

với $C \approx \sqrt{M}$.

Khi đó tích của $A(x)$ và $B(x)$ được biểu diễn thành:

$$A(x) \cdot B(x) = A_1(x) \cdot B_1(x) + \left(A_1(x) \cdot B_2(x) + A_2(x) \cdot B_1(x)\right)\cdot C + \left(A_2(x) \cdot B_2(x)\right)\cdot C^2$$

Các đa thức $A_1(x)$, $A_2(x)$, $B_1(x)$ và $B_2(x)$ chỉ chứa các hệ số nhỏ hơn $\sqrt{M}$, nên hệ số của mọi tích xuất hiện đều nhỏ hơn $M \cdot n$, thường đủ nhỏ để xử lý bằng các kiểu số dấu phẩy động thông thường.

Vì vậy, cách tiếp cận này cần tính tích các đa thức có hệ số nhỏ hơn bằng FFT thông thường và FFT ngược, rồi khôi phục tích ban đầu bằng phép cộng và nhân modulo trong thời gian $O(n)$.

## Ứng dụng

DFT có thể được dùng trong rất nhiều bài toán khác mà thoạt nhìn không liên quan đến nhân đa thức.

### Tất cả các tổng có thể

Cho hai mảng $a[]$ và $b[]$.
Ta cần tìm mọi tổng có thể có $a[i] + b[j]$, đồng thời đếm số lần xuất hiện của từng tổng.

Chẳng hạn, với $a = [1,~ 2,~ 3]$ và $b = [2,~ 4]$ ta có:
tổng $3$ đạt được theo $1$ cách, tổng $4$ cũng theo $1$ cách, $5$ theo $2$ cách, $6$ theo $1$ cách, $7$ theo $1$ cách.

Ta xây dựng hai đa thức $A$ và $B$ cho hai mảng $a$ và $b$.
Các số trong mảng đóng vai trò số mũ trong đa thức ($a[i] \Rightarrow x^{a[i]}$); hệ số của số hạng tương ứng là số lần số đó xuất hiện trong mảng.

Nhân hai đa thức này trong thời gian $O(n \log n)$, ta được đa thức $C$ mà các số mũ cho biết những tổng có thể đạt được và các hệ số cho biết số cách đạt được.
Minh họa trên ví dụ:

$$(1 x^1 + 1 x^2 + 1 x^3) (1 x^2 + 1 x^4) = 1 x^3 + 1 x^4 + 2 x^5 + 1 x^6 + 1 x^7$$

### Tất cả các tích vô hướng có thể

Cho hai mảng $a[]$ và $b[]$ có độ dài $n$.
Ta cần tính tích của $a$ với mỗi phép dịch vòng của $b$.

Ta tạo hai mảng mới kích thước $2n$:
Đảo ngược $a$ rồi nối thêm $n$ số không vào cuối.
Với $b$, ta nối thêm chính nó vào cuối.
Khi nhân hai mảng này như các đa thức và xét các hệ số $c[n-1],~ c[n],~ \dots,~ c[2n-2]$ của tích $c$, ta được:

$$c[k] = \sum_{i+j=k} a[i] b[j]$$

Do mọi phần tử $a[i] = 0$ với $i \ge n$:

$$c[k] = \sum_{i=0}^{n-1} a[i] b[k-i]$$

Dễ thấy tổng này chính là tích vô hướng của vector $a$ với phép dịch vòng sang trái thứ $(k - (n - 1))$ của $b$.
Vậy các hệ số này là đáp án và ta vẫn tìm được chúng trong thời gian $O(n \log n)$.
Lưu ý rằng $c[2n-1]$ cũng cho phép dịch vòng thứ $n$, nhưng phép này giống phép dịch vòng thứ $0$ nên không cần xét riêng vào đáp án.

### Hai dải

Cho hai dải Boolean $a$ và $b$ (các mảng vòng gồm giá trị $0$ và $1$).
Ta muốn tìm mọi cách ghép dải thứ nhất vào dải thứ hai sao cho không có vị trí nào mà một giá trị $1$ của dải đầu nằm cạnh một giá trị $1$ của dải thứ hai.

Bài toán này thực ra không khác nhiều so với bài trước.
Ghép hai dải tương ứng với dịch vòng mảng thứ hai; ta có thể ghép chúng nếu tích vô hướng của hai mảng bằng $0$.

### So khớp chuỗi

Cho hai chuỗi gồm các chữ cái thường: văn bản $T$ và mẫu $P$.
Ta cần tìm tất cả các vị trí xuất hiện của mẫu trong văn bản.

Ta tạo một đa thức cho mỗi chuỗi ($T[i]$ và $P[I]$ là các số từ $0$ đến $25$ tương ứng với $26$ chữ cái):

$$A(x) = a_0 x^0 + a_1 x^1 + \dots + a_{n-1} x^{n-1}, \quad n = |T|$$

với

$$a_i = \cos(\alpha_i) + i \sin(\alpha_i), \quad \alpha_i = \frac{2 \pi T[i]}{26}.$$

Và

$$B(x) = b_0 x^0 + b_1 x^1 + \dots + b_{m-1} x^{m-1}, \quad m = |P|$$

với

$$b_i = \cos(\beta_i) - i \sin(\beta_i), \quad \beta_i = \frac{2 \pi P[m-i-1]}{26}.$$

Lưu ý biểu thức $P[m-i-1]$ đảo ngược thứ tự của mẫu một cách tường minh.

Hệ số thứ $(m-1+i)$ của tích hai đa thức $C(x) = A(x) \cdot B(x)$ cho biết mẫu có xuất hiện trong văn bản tại vị trí $i$ hay không.

$$c_{m-1+i} = \sum_{j = 0}^{m-1} a_{i+j} \cdot b_{m-1-j} = \sum_{j=0}^{m-1} \left(\cos(\alpha_{i+j}) + i \sin(\alpha_{i+j})\right) \cdot \left(\cos(\beta_j) - i \sin(\beta_j)\right)$$

với $\alpha_{i+j} = \frac{2 \pi T[i+j]}{26}$ và $\beta_j = \frac{2 \pi P[j]}{26}$

Nếu khớp, ta có $T[i+j] = P[j]$, do đó $\alpha_{i+j} = \beta_j$.
Khi đó, dùng đẳng thức lượng giác Pythagoras, ta được:

$$\begin{align}
c_{m-1+i} &= \sum_{j = 0}^{m-1}  \left(\cos(\alpha_{i+j}) + i \sin(\alpha_{i+j})\right) \cdot \left(\cos(\alpha_{i+j}) - i \sin(\alpha_{i+j})\right) \\
&= \sum_{j = 0}^{m-1} \cos(\alpha_{i+j})^2 + \sin(\alpha_{i+j})^2 = \sum_{j = 0}^{m-1} 1 = m
\end{align}$$

Nếu không khớp, ít nhất một ký tự khác nhau, dẫn tới một trong các tích $a_{i+1} \cdot b_{m-1-j}$ khác $1$, và do đó hệ số $c_{m-1+i} \ne m$.

### So khớp chuỗi với ký tự đại diện

Đây là phần mở rộng của bài toán trước.
Lần này mẫu được phép chứa ký tự đại diện $\*$ có thể khớp với mọi chữ cái.
Ví dụ, mẫu $a*c$ xuất hiện trong văn bản $abccaacc$ tại đúng ba vị trí: chỉ số $0$, chỉ số $4$ và chỉ số $5$.

Ta tạo các đa thức giống hệt như trên, ngoại trừ đặt $b_i = 0$ nếu $P[m-i-1] = *$.
Nếu $x$ là số ký tự đại diện trong $P$, mẫu $P$ sẽ khớp với $T$ tại chỉ số $i$ nếu $c_{m-1+i} = m - x$.

## Bài tập

- [SPOJ - POLYMUL](http://www.spoj.com/problems/POLYMUL/)
- [SPOJ - MAXMATCH](http://www.spoj.com/problems/MAXMATCH/)
- [SPOJ - ADAMATCH](http://www.spoj.com/problems/ADAMATCH/)
- [Codeforces - Yet Another String Matching Problem](http://codeforces.com/problemset/problem/954/I)
- [Codeforces - Lightsabers (hard)](http://codeforces.com/problemset/problem/958/F3)
- [Codeforces - Running Competition](https://codeforces.com/contest/1398/problem/G)
- [Kattis - A+B Problem](https://open.kattis.com/problems/aplusb)
- [Kattis - K-Inversions](https://open.kattis.com/problems/kinversions)
- [Codeforces - Dasha and cyclic table](http://codeforces.com/contest/754/problem/E)
- [CodeChef - Expected Number of Customers](https://www.codechef.com/COOK112A/problems/MMNN01)
- [CodeChef - Power Sum](https://www.codechef.com/SEPT19A/problems/PSUM)
- [Codeforces - Centroid Probabilities](https://codeforces.com/problemset/problem/1667/E)
