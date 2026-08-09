---
title: Factorial modulo p
tags:
  - Translated
e_maxx_link: modular_factorial
translation:
  source: algebra/factorial-modulo.md
  source_commit: 86961ba33631e453e3a2840e65d1ceb2da752e2f
  status: draft
  last_synced: 2026-08-09
---

# Giai thừa modulo $p$

Trong một số bài toán, ta cần xét theo modulo một số nguyên tố $p$ các công thức phức tạp có chứa giai thừa ở cả tử số và mẫu số, chẳng hạn như công thức hệ số nhị thức.
Ở đây ta xét trường hợp $p$ tương đối nhỏ.
Bài toán này chỉ có ý nghĩa khi các giai thừa xuất hiện ở cả tử và mẫu của phân số.
Nếu không, từ $p!$ trở đi các giá trị đều trở thành 0 theo modulo $p$.
Nhưng trong một phân số, các thừa số $p$ ở tử và mẫu có thể triệt tiêu nhau, nên biểu thức cuối cùng vẫn có thể khác 0 modulo $p$.

Vì vậy, phát biểu chính thức của bài toán là: ta muốn tính $n! \bmod p$ nhưng bỏ qua mọi thừa số $p$ xuất hiện trong giai thừa.
Hãy tưởng tượng ta phân tích $n!$ thành thừa số nguyên tố, loại bỏ tất cả thừa số $p$, rồi tính tích còn lại modulo $p$.
Ta gọi đại lượng này là *giai thừa biến đổi (modified factorial)* và ký hiệu $n!_{\%p}$.
Chẳng hạn $7!_{\%p} \equiv 1 \cdot 2 \cdot \underbrace{1}_{3} \cdot 4 \cdot 5 \underbrace{2}_{6} \cdot 7 \equiv 2 \bmod 3$.

Biết cách tính hiệu quả giai thừa biến đổi giúp ta nhanh chóng tính nhiều công thức tổ hợp khác nhau (ví dụ [hệ số nhị thức](../combinatorics/binomial-coefficients.md)).

## Thuật toán
Hãy viết tường minh giai thừa biến đổi này.

$$\begin{eqnarray}
n!_{\%p} &=& 1 \cdot 2 \cdot 3 \cdot \ldots \cdot (p-2) \cdot (p-1) \cdot \underbrace{1}_{p} \cdot (p+1) \cdot (p+2) \cdot \ldots \cdot (2p-1) \cdot \underbrace{2}_{2p} \\\
 & &\quad \cdot (2p+1) \cdot \ldots \cdot (p^2-1) \cdot \underbrace{1}_{p^2} \cdot (p^2 +1) \cdot \ldots \cdot n \pmod{p} \\\\
&=& 1 \cdot 2 \cdot 3 \cdot \ldots \cdot (p-2) \cdot (p-1) \cdot \underbrace{1}_{p} \cdot 1 \cdot 2 \cdot \ldots \cdot (p-1) \cdot \underbrace{2}_{2p} \cdot 1 \cdot 2 \\\
& &\quad \cdot \ldots \cdot (p-1) \cdot \underbrace{1}_{p^2} \cdot 1 \cdot 2 \cdot \ldots \cdot (n \bmod p) \pmod{p}
\end{eqnarray}$$

Có thể thấy rõ rằng giai thừa được chia thành nhiều khối có cùng độ dài, ngoại trừ khối cuối cùng.

$$\begin{eqnarray}
n!_{\%p}&=& \underbrace{1 \cdot 2 \cdot 3 \cdot \ldots \cdot (p-2) \cdot (p-1) \cdot 1}_{1\text{st}} \cdot \underbrace{1 \cdot 2 \cdot 3 \cdot \ldots \cdot (p-2) \cdot (p-1) \cdot 2}_{2\text{nd}} \cdot \ldots \\\\
& & \cdot \underbrace{1 \cdot 2 \cdot 3 \cdot \ldots \cdot (p-2) \cdot (p-1) \cdot 1}_{p\text{th}} \cdot \ldots \cdot \quad \underbrace{1 \cdot 2 \cdot \cdot \ldots \cdot (n \bmod p)}_{\text{tail}} \pmod{p}.
\end{eqnarray}$$

Phần chính của mỗi khối rất dễ tính — đó chính là $(p-1)!\ \mathrm{mod}\ p$.
Ta có thể tính trực tiếp bằng chương trình hoặc áp dụng định lý Wilson, theo đó $(p-1)! \bmod p = -1$ với mọi số nguyên tố $p$.

Có đúng $\lfloor \frac{n}{p} \rfloor$ khối như vậy, nên ta cần nâng $-1$ lên lũy thừa $\lfloor \frac{n}{p} \rfloor$.
Có thể thực hiện trong thời gian logarit bằng [lũy thừa nhị phân](binary-exp.md); tuy nhiên, cũng có thể nhận ra kết quả chỉ luân phiên giữa $-1$ và $1$, nên ta chỉ cần xét tính chẵn lẻ của số mũ và nhân với $-1$ khi số mũ lẻ.
Thay vì thực hiện phép nhân, ta cũng có thể chỉ cần lấy $p$ trừ đi kết quả hiện tại.

Giá trị của khối cuối cùng chưa đủ độ dài có thể được tính riêng trong $O(p)$.


Giờ chỉ còn phần tử cuối của mỗi khối.
Nếu ẩn các phần tử đã xử lý, ta thấy mẫu sau:

$$n!_{\%p} = \underbrace{ \ldots \cdot 1 } \cdot \underbrace{ \ldots \cdot 2} \cdot \ldots \cdot \underbrace{ \ldots \cdot (p-1)} \cdot \underbrace{ \ldots \cdot 1 } \cdot \underbrace{ \ldots \cdot 1} \cdot \underbrace{ \ldots \cdot 2} \cdots$$

Đây lại là một giai thừa biến đổi, nhưng có kích thước nhỏ hơn nhiều.
Cụ thể, đó là $\lfloor n / p \rfloor !_{\%p}$.

Như vậy, trong quá trình tính giai thừa biến đổi $n\!_{\%p}$, ta thực hiện $O(p)$ phép toán rồi còn lại bài toán tính $\lfloor n / p \rfloor !_{\%p}$.
Ta thu được một công thức đệ quy.
Độ sâu đệ quy là $O(\log_p n)$, nên độ phức tạp tổng thể của thuật toán là $O(p \log_p n)$.

Lưu ý rằng nếu tính trước các giai thừa $0!,~ 1!,~ 2!,~ \dots,~ (p-1)!$ modulo $p$, độ phức tạp sẽ chỉ còn $O(\log_p n)$.


## Cài đặt

Ta không cần dùng đệ quy vì đây là trường hợp đệ quy đuôi và có thể dễ dàng chuyển thành vòng lặp.
Trong cài đặt dưới đây, ta tính trước các giai thừa $0!,~ 1!,~ 2!,~ \dots,~ (p-1)!$, nên thời gian chạy là $O(p + \log_p n)$.
Nếu cần gọi hàm nhiều lần, có thể đưa phần tiền xử lý ra ngoài hàm và mỗi lần tính $n!_{\%p}$ chỉ mất $O(\log_p n)$.

```cpp
int factmod(int n, int p) {
    vector<int> f(p);
    f[0] = 1;
    for (int i = 1; i < p; i++)
        f[i] = f[i-1] * i % p;

    int res = 1;
    while (n > 1) {
        if ((n/p) % 2)
            res = p - res;
        res = res * f[n%p] % p;
        n /= p;
    }
    return res;
}
```

Ngoài ra, nếu bộ nhớ bị giới hạn và không thể lưu toàn bộ các giai thừa, ta có thể chỉ ghi nhớ những giá trị giai thừa thực sự cần dùng, sắp xếp chúng, rồi tính trong một lượt bằng cách duyệt $0!,~ 1!,~ 2!,~ \dots,~ (p-1)!$ mà không lưu tường minh tất cả giá trị.

## Số mũ của $p$

Nếu muốn tính hệ số nhị thức modulo $p$, ta còn cần biết số lần $p$ xuất hiện trong $n$, tức số lần $p$ xuất hiện trong phân tích thừa số nguyên tố của $n$, hay số lần ta đã xóa $p$ trong quá trình tính giai thừa biến đổi.

**Ghi chú bản dịch:** Câu nguồn phía trên dùng $n$, nhưng ngữ cảnh, công thức Legendre ngay dưới và quá trình xóa các thừa số $p$ đều đang xét $n!$. Đại lượng cần dùng ở đây là số mũ của $p$ trong phân tích thừa số nguyên tố của $n!$. Vấn đề này được đề xuất sửa riêng ở bản tiếng Anh.

[Công thức Legendre](https://en.wikipedia.org/wiki/Legendre%27s_formula) cho phép tính đại lượng này trong thời gian $O(\log_p n)$.
Công thức cho số mũ $\nu_p$ là:

$$\nu_p(n!) = \sum_{i=1}^{\infty} \left\lfloor \frac{n}{p^i} \right\rfloor$$

Từ đó ta có cài đặt:

```cpp
int multiplicity_factorial(int n, int p) {
    int count = 0;
    do {
        n /= p;
        count += n;
    } while (n);
    return count;
}
```

Có thể chứng minh công thức này rất dễ bằng chính các ý tưởng ở những phần trước.
Loại bỏ mọi phần tử không chứa thừa số $p$.
Còn lại $\lfloor n/p \rfloor$ phần tử.
Nếu loại một thừa số $p$ khỏi mỗi phần tử đó, ta thu được tích $1 \cdot 2 \cdots \lfloor n/p \rfloor = \lfloor n/p \rfloor !$, và lại quay về một bài toán đệ quy.
