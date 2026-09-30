---
tags:
  - Translated
e_maxx_link: catalan_numbers
translation:
  source: combinatorics/catalan-numbers.md
  source_commit: 4283eb29b38cc82d5ee088ad0a38b84ee3c37bb1
  status: draft
  last_synced: 2026-09-29
---

# Số Catalan
Số Catalan là một dãy số xuất hiện trong nhiều bài toán tổ hợp, đặc biệt là các bài liên quan tới những đối tượng được định nghĩa đệ quy.

Dãy số này được đặt theo tên nhà toán học Bỉ [Catalan](https://en.wikipedia.org/wiki/Eug%C3%A8ne_Charles_Catalan), sống ở thế kỷ 19. (Thực ra dãy số đã được Euler, người sống trước Catalan một thế kỷ, biết tới từ trước đó).

Một vài số Catalan đầu tiên $C_n$ (bắt đầu từ chỉ số không):

 $1, 1, 2, 5, 14, 42, 132, 429, 1430, \ldots$

### Ứng dụng trong một số bài toán tổ hợp

Số Catalan $C_n$ là đáp án của các bài toán sau:

- Số dãy ngoặc đúng gồm $n$ dấu ngoặc mở và $n$ dấu ngoặc đóng.
- Số cây nhị phân đầy đủ có gốc với $n + 1$ lá (các đỉnh không được đánh số). Một cây nhị phân có gốc là đầy đủ nếu mỗi đỉnh hoặc có đúng hai con, hoặc không có con nào.
- Số cách đặt đầy đủ dấu ngoặc cho $n + 1$ thừa số.
- Số cách tam giác hóa một đa giác lồi có $n + 2$ cạnh (tức số cách chia đa giác thành các tam giác không giao nhau bằng các đường chéo).
- Số cách nối $2n$ điểm trên một đường tròn thành $n$ dây cung đôi một không giao nhau.
- Số cây nhị phân đầy đủ [không đẳng cấu](https://en.wikipedia.org/wiki/Graph_isomorphism) có $n$ đỉnh trong (tức các đỉnh có ít nhất một con).
- Số đường đi đơn điệu trên lưới từ điểm $(0, 0)$ tới điểm $(n, n)$ trong lưới vuông kích thước $n \times n$, không đi lên phía trên đường chéo chính (tức đường nối $(0, 0)$ với $(n, n)$).
- Số hoán vị độ dài $n$ có thể được [sắp xếp bằng ngăn xếp](https://en.wikipedia.org/wiki/Stack-sortable_permutation) (có thể chứng minh rằng một hoán vị sắp xếp được bằng ngăn xếp khi và chỉ khi không tồn tại các chỉ số $i < j < k$ sao cho $a_k < a_i < a_j$ ).
- Số [phân hoạch không cắt nhau](https://en.wikipedia.org/wiki/Noncrossing_partition) của một tập có $n$ phần tử.
- Số cách phủ chiếc thang $1 \ldots n$ bằng $n$ hình chữ nhật (chiếc thang gồm $n$ cột, trong đó cột thứ $i^{th}$ có chiều cao $i$).


## Cách tính

Có hai công thức để tính số Catalan: **truy hồi và giải tích**. Vì ta tin rằng các bài toán nêu trên là tương đương (có cùng đáp án), khi chứng minh các công thức dưới đây ta sẽ chọn bài toán dễ lập luận nhất.

### Công thức truy hồi
 
$$C_0 = C_1 = 1$$

$$C_n = \sum_{k = 0}^{n-1} C_k C_{n-1-k} , {n} \geq 2$$

Có thể suy ra công thức truy hồi dễ dàng từ bài toán dãy ngoặc đúng.

Dấu ngoặc mở ngoài cùng bên trái $l$ tương ứng với một dấu ngoặc đóng $r$ nào đó. Giả sử có $k$ cặp ngoặc nằm giữa $l$ và $r$. Xâu con nằm giữa chúng có thể là bất kỳ dãy ngoặc đúng nào gồm $k$ cặp, còn phần phía sau $r$ có thể là bất kỳ dãy ngoặc đúng nào gồm $n-1-k$ cặp. Do đó, với $k$ cố định, có đúng $C_k C_{n-1-k}$ dãy ngoặc như vậy. Cộng trên mọi $k=0,1,\ldots,n-1$ cho ta hệ thức truy hồi của $C_n$.

Tương đương, mọi dãy ngoặc đúng không rỗng đều có cách phân tách duy nhất thành $(A)B$, trong đó $A$ và $B$ là các dãy ngoặc đúng. Nếu $A$ chứa $k$ cặp thì $B$ chứa $n-1-k$ cặp, cho ta cùng hệ thức truy hồi.

#### Cài đặt C++

```cpp
const int MOD = ....
const int MAX = ....
int catalan[MAX];
void init(int n) {
    catalan[0] = catalan[1] = 1;
    for (int i=2; i<=n; i++) {
        catalan[i] = 0;
        for (int j=0; j < i; j++) {
            catalan[i] += (catalan[j] * catalan[i-j-1]) % MOD;
            if (catalan[i] >= MOD) {
                catalan[i] -= MOD;
            }
        }
    }
}
```

### Công thức giải tích

$$C_n = \frac{1}{n + 1} {\binom{2n}{n}}$$

(ở đây $\binom{n}{k}$ là hệ số nhị thức thông thường, tức số cách chọn $k$ đối tượng từ một tập gồm $n$ đối tượng).

Có thể suy ra công thức trên dễ dàng từ bài toán đường đi đơn điệu trên lưới vuông. Tổng số đường đi đơn điệu trong lưới kích thước $n \times n$ là $\binom{2n}{n}$.

Bây giờ ta đếm số đường đi đơn điệu cắt qua đường chéo chính. Xét một đường đi như vậy và tìm cạnh đầu tiên nằm phía trên đường chéo. Phản xạ phần đường đi kể từ sau cạnh này qua đường chéo. Kết quả luôn là một đường đi đơn điệu trong lưới $(n - 1) \times (n + 1)$. Ngược lại, mọi đường đi đơn điệu trong lưới $(n - 1) \times (n + 1)$ đều phải cắt đường chéo. Như vậy, ta đã đếm được toàn bộ các đường đi đơn điệu cắt đường chéo chính trong lưới $n \times n$.

Số đường đi đơn điệu trong lưới $(n - 1) \times (n + 1)$ là $\binom{2n}{n-1}$. Gọi các đường đi này là các đường đi "xấu". Do đó, để tính số đường đi đơn điệu không cắt đường chéo chính, ta lấy tổng số đường đi trừ số đường đi "xấu", thu được công thức:

$$C_n = \binom{2n}{n} - \binom{2n}{n-1} = \frac{1}{n + 1} \binom{2n}{n} , {n} \geq 0$$

## Tài liệu tham khảo

- [Catalan Number by Tom Davis](http://www.geometer.org/mathcircles/catalan.pdf)
- [Catalan Numbers and Catalan Convolution](https://codeforces.com/blog/entry/87585)

## Bài tập luyện tập
- [Codechef - PANSTACK](https://www.codechef.com/APRIL12/problems/PANSTACK/)
- [Spoj - Skyline](http://www.spoj.com/problems/SKYLINE/)
- [UVA - Safe Salutations](https://uva.onlinejudge.org/index.php?option=com_onlinejudge&Itemid=8&page=show_problem&problem=932)
- [Codeforces - How many trees?](http://codeforces.com/problemset/problem/9/D)
- [SPOJ - FUNPROB](http://www.spoj.com/problems/FUNPROB/)
* [LOJ - 1170 - Counting Perfect BST](http://lightoj.com/volume_showproblem.php?problem=1170)
* [UVA - 12887 - The Soldier's Dilemma](https://uva.onlinejudge.org/index.php?option=com_onlinejudge&Itemid=8&page=show_problem&problem=4752)