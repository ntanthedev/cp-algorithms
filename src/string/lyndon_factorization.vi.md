---
tags:
  - Translated
e_maxx_link: duval_algorithm
translation:
  source: string/lyndon_factorization.md
  source_commit: e3d5e7671235327198551b08f313e778a910a200
  status: draft
  last_synced: 2026-08-07
---

# Phân rã Lyndon

## Phân rã Lyndon

Trước hết, ta định nghĩa khái niệm phân rã Lyndon.

Một xâu được gọi là **đơn giản** (hay một từ Lyndon) nếu nó **nhỏ hơn nghiêm ngặt** mọi **hậu tố** không tầm thường của chính nó.
Ví dụ về các xâu đơn giản: $a$, $b$, $ab$, $aab$, $abb$, $ababb$, $abcd$.
Có thể chứng minh một xâu là đơn giản khi và chỉ khi nó **nhỏ hơn nghiêm ngặt** mọi **phép dịch vòng** không tầm thường của chính nó.

Tiếp theo, cho một xâu $s$.
**Phân rã Lyndon** của xâu $s$ là một cách phân tích $s = w_1 w_2 \dots w_k$, trong đó mọi xâu $w_i$ đều đơn giản và được sắp theo thứ tự không tăng $w_1 \ge w_2 \ge \dots \ge w_k$.

Có thể chứng minh rằng với mọi xâu, cách phân rã như vậy luôn tồn tại và là duy nhất.

## Thuật toán Duval

Thuật toán Duval xây dựng phân rã Lyndon trong $O(n)$ thời gian và dùng $O(1)$ bộ nhớ bổ sung.

Trước hết, ta đưa ra thêm một khái niệm:
xâu $t$ được gọi là **tiền đơn giản (pre-simple)** nếu có dạng $t = w w \dots w \overline{w}$, trong đó $w$ là một xâu đơn giản và $\overline{w}$ là một tiền tố của $w$ (có thể rỗng).
Một xâu đơn giản cũng là tiền đơn giản.

Thuật toán Duval hoạt động theo chiến lược tham lam.
Ở mọi thời điểm, xâu $s$ được chia thành ba phần $s = s_1 s_2 s_3$: phân rã Lyndon của $s_1$ đã được tìm và cố định, xâu $s_2$ là tiền đơn giản (và ta biết độ dài của xâu đơn giản trong nó), còn $s_3$ hoàn toàn chưa được xử lý.
Trong mỗi vòng lặp, thuật toán Duval lấy ký tự đầu tiên của $s_3$ và thử nối nó vào $s_2$.
Nếu $s_2$ không còn tiền đơn giản, phân rã Lyndon của một phần trong $s_2$ sẽ được xác định; phần đó được chuyển sang $s_1$.

Ta mô tả thuật toán chi tiết hơn.
Con trỏ $i$ luôn trỏ tới đầu xâu $s_2$.
Vòng lặp ngoài chạy chừng nào $i < n$.
Bên trong vòng lặp, ta dùng hai con trỏ bổ sung: $j$ trỏ tới đầu $s_3$, còn $k$ trỏ tới ký tự hiện tại đang được dùng để so sánh.
Ta muốn thêm ký tự $s[j]$ vào xâu $s_2$, nên cần so sánh nó với ký tự $s[k]$.
Có ba trường hợp:

- $s[j] = s[k]$: khi đó, thêm ký tự $s[j]$ vào $s_2$ không làm mất tính tiền đơn giản.
  Vì vậy chỉ cần tăng cả hai con trỏ $j$ và $k$.
- $s[j] > s[k]$: lúc này xâu $s_2 + s[j]$ trở thành đơn giản.
  Ta có thể tăng $j$ và đặt lại $k$ về đầu $s_2$, để ký tự tiếp theo được so sánh với đầu của từ đơn giản.
- $s[j] < s[k]$: xâu $s_2 + s[j]$ không còn tiền đơn giản.
  Vì vậy ta tách xâu tiền đơn giản $s_2$ thành các xâu đơn giản cùng phần dư, có thể rỗng.
  Xâu đơn giản có độ dài $j - k$.
  Ở vòng tiếp theo, ta bắt đầu lại với phần $s_2$ còn lại.

### Cài đặt

Dưới đây là cài đặt thuật toán Duval, trả về phân rã Lyndon cần tìm của xâu $s$.

```{.cpp file=duval_algorithm}
vector<string> duval(string const& s) {
    int n = s.size();
    int i = 0;
    vector<string> factorization;
    while (i < n) {
        int j = i + 1, k = i;
        while (j < n && s[k] <= s[j]) {
            if (s[k] < s[j])
                k = i;
            else
                k++;
            j++;
        }
        while (i <= k) {
            factorization.push_back(s.substr(i, j - k));
            i += j - k;
        }
    }
    return factorization;
}
```

### Độ phức tạp

Ta ước lượng thời gian chạy của thuật toán.

**Vòng while ngoài** không chạy quá $n$ lần vì cuối mỗi vòng $i$ đều tăng.
Vòng while trong thứ hai cũng chạy tổng cộng trong $O(n)$ vì nó chỉ xuất ra phân rã cuối cùng.

Vì vậy ta chỉ cần quan tâm tới **vòng while trong thứ nhất**.
Trong trường hợp xấu nhất, nó chạy bao nhiêu lần?
Dễ thấy các từ đơn giản được xác định ở mỗi vòng của vòng lặp ngoài dài hơn phần dư mà ta phải so sánh thêm.
Do đó tổng độ dài các phần dư cũng nhỏ hơn $n$, nghĩa là vòng while trong thứ nhất chỉ chạy nhiều nhất $O(n)$ lần.
Thực tế, tổng số phép so sánh ký tự không vượt quá $4n - 3$.

## Tìm phép dịch vòng nhỏ nhất

Cho một xâu $s$.
Ta xây dựng phân rã Lyndon cho xâu $s + s$ (trong $O(n)$ thời gian).
Ta tìm một xâu đơn giản trong phân rã bắt đầu tại vị trí nhỏ hơn $n$ (tức bắt đầu trong bản sao đầu tiên của $s$) và kết thúc tại vị trí lớn hơn hoặc bằng $n$ (tức nằm sang bản sao thứ hai) của $s$.
Có thể khẳng định vị trí bắt đầu của xâu đơn giản này chính là vị trí bắt đầu của phép dịch vòng nhỏ nhất cần tìm.
Điều này có thể kiểm chứng trực tiếp từ định nghĩa phân rã Lyndon.

Ta dễ dàng tìm được đầu khối đơn giản: chỉ cần nhớ con trỏ $i$ ở đầu mỗi vòng của vòng lặp ngoài, tức vị trí bắt đầu của xâu tiền đơn giản hiện tại.

Do đó ta có cài đặt sau:

```{.cpp file=smallest_cyclic_string}
string min_cyclic_string(string s) {
    s += s;
    int n = s.size();
    int i = 0, ans = 0;
    while (i < n / 2) {
        ans = i;
        int j = i + 1, k = i;
        while (j < n && s[k] <= s[j]) {
            if (s[k] < s[j])
                k = i;
            else
                k++;
            j++;
        }
        while (i <= k)
            i += j - k;
    }
    return s.substr(ans, n / 2);
}
```

## Bài tập

- [UVA #719 - Glass Beads](https://uva.onlinejudge.org/index.php?option=onlinejudge&page=show_problem&problem=660)