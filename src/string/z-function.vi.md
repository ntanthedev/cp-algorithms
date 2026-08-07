---
tags:
  - Translated
e_maxx_link: z_function
translation:
  source: string/z-function.md
  source_commit: 4408f1ad7471da89df3f6aae27a9180790bf3a9f
  status: draft
  last_synced: 2026-08-07
---

# Hàm Z và cách tính

Giả sử ta được cho một chuỗi $s$ có độ dài $n$. **Hàm Z** của chuỗi này là một mảng có độ dài $n$, trong đó phần tử thứ $i$ bằng số ký tự lớn nhất tính từ vị trí $i$ trùng với các ký tự đầu tiên của $s$.

Nói cách khác, $z[i]$ là độ dài của chuỗi dài nhất đồng thời là một tiền tố của $s$ và là tiền tố của hậu tố của $s$ bắt đầu tại $i$.

**Lưu ý.** Trong bài viết này, để tránh nhập nhằng, ta dùng chỉ số bắt đầu từ $0$; tức ký tự đầu tiên của $s$ có chỉ số $0$ và ký tự cuối cùng có chỉ số $n-1$.

Phần tử đầu tiên của hàm Z, $z[0]$, thường không được định nghĩa thống nhất. Trong bài này ta quy ước nó bằng 0 (dù điều này không ảnh hưởng đến cài đặt thuật toán).

Bài viết trình bày thuật toán tính hàm Z trong $O(n)$ thời gian cùng nhiều ứng dụng của nó.

## Ví dụ

Ví dụ, dưới đây là các giá trị hàm Z của một số chuỗi:

* "aaaaa" - $[0, 4, 3, 2, 1]$
* "aaabaab" - $[0, 2, 1, 0, 2, 1, 0]$
* "abacaba" - $[0, 0, 1, 0, 3, 0, 1]$

## Thuật toán ngây thơ

Định nghĩa hình thức có thể được cài đặt trực tiếp bằng thuật toán $O(n^2)$ sau.

```cpp
vector<int> z_function_trivial(string s) {
	int n = s.size();
	vector<int> z(n);
	for (int i = 1; i < n; i++) {
		while (i + z[i] < n && s[z[i]] == s[i + z[i]]) {
			z[i]++;
		}
	}
	return z;
}
```

Ta chỉ duyệt từng vị trí $i$ và cập nhật $z[i]$, bắt đầu từ $z[i] = 0$ rồi tăng dần cho tới khi gặp một ký tự không khớp (hoặc đi tới cuối chuỗi).

Rõ ràng đây chưa phải cài đặt hiệu quả. Tiếp theo ta sẽ xây dựng một cách làm tốt hơn.

## Thuật toán hiệu quả để tính hàm Z

Để có thuật toán hiệu quả, ta lần lượt tính các giá trị $z[i]$ từ $i = 1$ tới $n - 1$, đồng thời khi tính một giá trị mới sẽ tận dụng tối đa các giá trị đã biết.

Để ngắn gọn, gọi **đoạn khớp** là những chuỗi con trùng với một tiền tố của $s$. Ví dụ, giá trị hàm Z cần tìm $z[i]$ chính là độ dài đoạn khớp bắt đầu tại vị trí $i$ (và kết thúc tại vị trí $i + z[i] - 1$).

Ta sẽ duy trì **các chỉ số $[l, r)$ của đoạn khớp nằm xa bên phải nhất**. Nghĩa là trong mọi đoạn đã phát hiện, ta giữ đoạn có điểm kết thúc xa bên phải nhất. Có thể xem chỉ số $r$ là "biên" mà thuật toán đã quét tới trong chuỗi $s$; mọi thứ bên phải đó vẫn chưa được biết.

Nếu chỉ số hiện tại (vị trí cần tính giá trị hàm Z tiếp theo) là $i$, ta có hai trường hợp:

*   $i \geq r$ -- vị trí hiện tại nằm **ngoài** phần đã xử lý.

    Khi đó ta tính $z[i]$ bằng **thuật toán ngây thơ** (so sánh từng ký tự một). Lưu ý rằng cuối cùng, nếu $z[i] > 0$, ta phải cập nhật chỉ số của đoạn nằm xa bên phải nhất, vì chắc chắn $r = i + z[i]$ mới tốt hơn $r$ trước đó.

*   $i < r$ -- vị trí hiện tại nằm bên trong đoạn khớp $[l, r)$.

    Khi đó có thể dùng các giá trị Z đã tính để "khởi tạo" $z[i]$ bằng một giá trị nào đó (chắc chắn tốt hơn bắt đầu từ 0), thậm chí có thể khá lớn.

    Ta nhận thấy các chuỗi con $s[l \dots r)$ và $s[0 \dots r-l)$ **trùng nhau**. Vì vậy, một xấp xỉ ban đầu cho $z[i]$ có thể lấy từ giá trị đã tính cho đoạn tương ứng trong $s[0 \dots r-l)$, tức $z[i-l]$.

    Tuy nhiên $z[i-l]$ có thể quá lớn: khi áp dụng tại vị trí $i$, nó có thể vượt qua chỉ số $r$. Điều này không hợp lệ vì ta chưa biết gì về các ký tự bên phải $r$: chúng có thể không khớp với các ký tự cần thiết.

    Đây là **một ví dụ** cho tình huống như vậy:

    $$ s = "aaaabaa" $$

    Khi tới vị trí cuối cùng ($i = 6$), đoạn khớp hiện tại sẽ là $[5, 7)$. Vị trí $6$ khi đó tương ứng với vị trí $6 - 5 = 1$, nơi giá trị hàm Z là $z[1] = 3$. Rõ ràng ta không thể khởi tạo $z[6]$ thành $3$, vì như vậy sẽ sai hoàn toàn. Giá trị lớn nhất có thể khởi tạo là $1$ -- vì đó là giá trị lớn nhất không đưa ta vượt qua chỉ số $r$ của đoạn khớp $[l, r)$.

    Vì vậy, một **xấp xỉ ban đầu** an toàn cho $z[i]$ là:

    $$ z_0[i] = \min(r - i,\; z[i-l]) $$

    Sau khi khởi tạo $z[i]$ bằng $z_0[i]$, ta thử tăng $z[i]$ bằng **thuật toán ngây thơ** — bởi nhìn chung, sau biên $r$ ta không thể biết đoạn còn tiếp tục khớp hay không.

Như vậy toàn bộ thuật toán được chia thành hai trường hợp chỉ khác nhau ở **giá trị khởi tạo** của $z[i]$: trong trường hợp thứ nhất là 0, còn trường hợp thứ hai được xác định bằng các giá trị đã tính trước theo công thức trên. Sau đó cả hai nhánh đều quy về việc chạy **thuật toán ngây thơ**, bắt đầu ngay sau khi giá trị ban đầu đã được xác định.

Thuật toán cuối cùng rất đơn giản. Mặc dù ở mỗi vòng lặp ta vẫn chạy thuật toán ngây thơ, cách tận dụng thông tin cũ giúp tổng thời gian trở thành tuyến tính. Phần sau sẽ chứng minh điều này.

## Cài đặt

Cài đặt khá ngắn gọn:

```cpp
vector<int> z_function(string s) {
    int n = s.size();
    vector<int> z(n);
    int l = 0, r = 0;
    for(int i = 1; i < n; i++) {
        if(i < r) {
            z[i] = min(r - i, z[i - l]);
        }
        while(i + z[i] < n && s[z[i]] == s[i + z[i]]) {
            z[i]++;
        }
        if(i + z[i] > r) {
            l = i;
            r = i + z[i];
        }
    }
    return z;
}
```

### Giải thích cài đặt

Toàn bộ lời giải được viết thành một hàm trả về mảng độ dài $n$ — chính là hàm Z của $s$.

Mảng $z$ ban đầu toàn số 0. Đoạn khớp nằm xa bên phải nhất hiện tại được giả sử là $[0; 0)$ (một đoạn cố ý rất nhỏ, không chứa bất kỳ $i$ nào).

Trong vòng lặp $i = 1 \dots n - 1$, trước hết ta xác định giá trị khởi tạo $z[i]$ — nó hoặc vẫn bằng 0, hoặc được tính theo công thức phía trên.

Sau đó thuật toán ngây thơ cố gắng tăng $z[i]$ nhiều nhất có thể.

Cuối cùng, nếu cần (tức nếu $i + z[i] > r$), ta cập nhật đoạn khớp nằm xa bên phải nhất $[l, r)$.

## Độ phức tạp tiệm cận của thuật toán

Ta sẽ chứng minh thuật toán trên chạy trong thời gian tuyến tính theo độ dài chuỗi, tức là $O(n)$.

Chứng minh khá đơn giản.

Ta chỉ cần quan tâm vòng lặp `while` lồng bên trong, vì mọi phần còn lại chỉ gồm các thao tác hằng số và cộng lại thành $O(n)$.

Ta sẽ chứng minh rằng **mỗi lần lặp** của vòng `while` đều làm biên phải $r$ của đoạn khớp tăng lên.

Để làm vậy, xét cả hai nhánh của thuật toán:

*   $i \geq r$

    Trong trường hợp này, vòng `while` hoặc không chạy lần nào (nếu $s[0] \ne s[i]$), hoặc chạy một vài lần bắt đầu tại vị trí $i$, mỗi lần tiến sang phải một ký tự. Sau đó biên phải $r$ chắc chắn được cập nhật.

    Vì vậy, khi $i \geq r$, mỗi lần lặp của vòng `while` đều làm chỉ số $r$ mới tăng lên.

*   $i < r$

    Trong trường hợp này, ta khởi tạo $z[i]$ bằng một giá trị $z_0$ theo công thức trên. Hãy so sánh giá trị ban đầu $z_0$ với $r - i$. Có ba trường hợp:

      *   $z_0 < r - i$

          Ta chứng minh rằng trong trường hợp này vòng `while` sẽ không chạy lần nào.

          Có thể chứng minh dễ dàng bằng phản chứng: nếu vòng `while` chạy ít nhất một lần thì xấp xỉ ban đầu $z[i] = z_0$ là chưa chính xác (nhỏ hơn độ dài khớp thực sự). Nhưng vì $s[l \dots r)$ và $s[0 \dots r-l)$ giống nhau, điều này kéo theo $z[i-l]$ đang chứa giá trị sai (nhỏ hơn giá trị đúng).

          Do đó, vì $z[i-l]$ đúng và nhỏ hơn $r - i$, giá trị này chính là giá trị cần tìm $z[i]$.

      *   $z_0 = r - i$

          Khi đó vòng `while` có thể chạy vài lần, nhưng mỗi lần đều làm chỉ số $r$ tăng vì ta bắt đầu so sánh từ $s[r]$, rồi tiến ra ngoài đoạn $[l, r)$.

      *   $z_0 > r - i$

          Trường hợp này không thể xảy ra theo định nghĩa của $z_0$.

Như vậy ta đã chứng minh mỗi lần lặp của vòng bên trong đều làm con trỏ $r$ tiến sang phải. Vì biên phải r tăng mỗi lần và không vượt quá n, tổng số lần lặp của vòng bên trong là tuyến tính theo độ dài chuỗi.

**Ghi chú bản dịch:** Nguồn kết luận rằng r không thể lớn hơn n-1 và vì thế vòng lặp bên trong không chạy quá n-1 lần. Với cách biểu diễn đoạn nửa mở [l, r), r thực ra có thể bằng n. Cận đúng là r không vượt quá n; điều này vẫn đủ để suy ra độ phức tạp tuyến tính.

Phần còn lại của thuật toán hiển nhiên chạy trong $O(n)$, do đó toàn bộ thuật toán tính hàm Z chạy trong thời gian tuyến tính.

## Ứng dụng

Tiếp theo ta xét một số ứng dụng cụ thể của hàm Z.

Các ứng dụng này phần lớn tương tự những ứng dụng của [hàm tiền tố](prefix-function.md).

### Tìm chuỗi con

Để tránh nhầm lẫn, gọi $t$ là **chuỗi văn bản** và $p$ là **mẫu**. Bài toán là tìm mọi lần mẫu $p$ xuất hiện trong văn bản $t$.

Để giải, ta tạo chuỗi mới $s = p + \diamond + t$, tức nối $p$ và $t$ nhưng chèn thêm ký tự phân cách $\diamond$ ở giữa (chọn $\diamond$ sao cho chắc chắn không xuất hiện trong $p$ hay $t$).

Tính hàm Z của $s$. Sau đó, với mỗi $i$ trong đoạn $[0; \; \operatorname{length}(t) - 1]$, xét giá trị tương ứng $k = z[i + \operatorname{length}(p) + 1]$. Nếu $k$ bằng $\operatorname{length}(p)$ thì có một lần xuất hiện của $p$ tại vị trí thứ $i$ trong $t$; nếu không thì không có lần xuất hiện nào của $p$ tại vị trí thứ $i$ trong $t$.

Thời gian chạy (và lượng bộ nhớ sử dụng) là $O(\operatorname{length}(t) + \operatorname{length}(p))$.

### Số lượng chuỗi con phân biệt trong một chuỗi

Cho chuỗi $s$ có độ dài $n$, hãy đếm số chuỗi con phân biệt của $s$.

Ta giải bài toán theo cách lặp dần: giả sử biết số chuỗi con khác nhau hiện tại, hãy tính lại số lượng sau khi thêm một ký tự vào cuối $s$.

Gọi $k$ là số chuỗi con phân biệt hiện tại của $s$. Ta thêm ký tự mới $c$ vào $s$. Hiển nhiên có thể xuất hiện một số chuỗi con mới kết thúc bằng ký tự $c$ này (cụ thể là các chuỗi kết thúc bằng ký tự đó mà ta chưa gặp trước đây).

Lấy chuỗi $t = s + c$ rồi đảo ngược nó. Bài toán lúc này là đếm bao nhiêu tiền tố của $t$ không xuất hiện ở nơi nào khác trong $t$. Tính hàm Z của $t$ và tìm giá trị lớn nhất $z_{max}$. Rõ ràng tiền tố của $t$ có độ dài $z_{max}$ cũng xuất hiện ở đâu đó giữa $t$, và mọi tiền tố ngắn hơn cũng vậy.

Do đó số chuỗi con mới xuất hiện khi thêm ký tự $c$ vào $s$ bằng $\operatorname{length}(t) - z_{max}$.

Suy ra lời giải có thời gian chạy $O(n^2)$ với chuỗi độ dài $n$.

Cũng theo đúng cách này, ta vẫn có thể cập nhật số chuỗi con phân biệt trong $O(n)$ thời gian khi thêm một ký tự vào đầu chuỗi hoặc xóa một ký tự ở đầu hay cuối.

### Nén chuỗi

Cho chuỗi $s$ có độ dài $n$. Hãy tìm biểu diễn "nén" ngắn nhất của nó, tức tìm chuỗi $t$ có độ dài nhỏ nhất sao cho $s$ có thể được biểu diễn bằng cách nối một hoặc nhiều bản sao của $t$.

Lời giải là tính hàm Z của $s$, duyệt mọi $i$ sao cho $i$ chia hết $n$, rồi dừng tại $i$ đầu tiên thỏa $i + z[i] = n$. Khi đó chuỗi $s$ có thể được nén xuống độ dài $i$.

Chứng minh của tính chất này giống lời giải dùng [hàm tiền tố](prefix-function.md).

## Bài tập luyện tập

* [CSES - Finding Borders](https://cses.fi/problemset/task/1732)
* [eolymp - Blocks of string](https://www.eolymp.com/en/problems/1309)
* [Codeforces - Password [Difficulty: Easy]](http://codeforces.com/problemset/problem/126/B)
* [UVA # 455 "Periodic Strings" [Difficulty: Medium]](http://uva.onlinejudge.org/index.php?option=onlinejudge&page=show_problem&problem=396)
* [UVA # 11022 "String Factoring" [Difficulty: Medium]](http://uva.onlinejudge.org/index.php?option=onlinejudge&page=show_problem&problem=1963)
* [UVa 11475 - Extend to Palindrome](http://uva.onlinejudge.org/index.php?option=com_onlinejudge&Itemid=8&category=24&page=show_problem&problem=2470)
* [LA 6439 - Pasti Pas!](https://icpcarchive.ecs.baylor.edu/index.php?option=com_onlinejudge&Itemid=8&category=588&page=show_problem&problem=4450)
* [Codechef - Chef and Strings](https://www.codechef.com/problems/CHSTR)
* [Codeforces - Prefixes and Suffixes](http://codeforces.com/problemset/problem/432/D)
* [Codeforces - "a" String Problem](https://codeforces.com/contest/1984/problem/D)