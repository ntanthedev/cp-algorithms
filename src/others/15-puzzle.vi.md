---
tags:
  - Translated
e_maxx_link: 15_puzzle
translation:
  source: others/15-puzzle.md
  source_commit: a957d92a5f96cc23a96611ea8d52feaab0b3173c
  status: draft
  last_synced: 2026-11-15
---

# Trò chơi 15-puzzle: bài toán có lời giải hay không

Trò chơi này diễn ra trên một bảng $4 \times 4$. Trên bảng có $15$ quân được đánh số từ 1 đến 15. Một ô để trống (ký hiệu là 0). Mục tiêu là đưa bảng về trạng thái dưới đây bằng cách lần lượt di chuyển một quân vào ô trống:

$$\begin{matrix} 1 & 2 & 3 & 4 \\ 5 & 6 & 7 & 8 \\ 9 & 10 & 11 & 12 \\ 13 & 14 & 15 & 0 \end{matrix}$$

Trò chơi "15 Puzzle" do Noyes Chapman tạo ra vào năm 1880.

## Tồn tại lời giải

Xét bài toán sau: cho một trạng thái trên bảng, hãy xác định liệu có tồn tại một dãy nước đi đưa bảng về trạng thái đích hay không.

Giả sử ta có một trạng thái như sau:

$$\begin{matrix} a_1 & a_2 & a_3 & a_4 \\ a_5 & a_6 & a_7 & a_8 \\ a_9 & a_{10} & a_{11} & a_{12} \\ a_{13} & a_{14} & a_{15} & a_{16} \end{matrix}$$

trong đó một phần tử bằng 0 và biểu thị ô trống $a_z  = 0$.

Xét hoán vị:

$$a_1 a_2 ... a_{z-1} a_{z+1} ... a_{15} a_{16}$$

tức là hoán vị của các số tương ứng với vị trí trên bảng sau khi bỏ phần tử 0.

Gọi $N$ là số nghịch thế của hoán vị này (tức số cặp phần tử $a_i$ và $a_j$ sao cho $i < j$ nhưng $a_i  > a_j$).

Gọi $K$ là chỉ số hàng chứa ô trống (theo quy ước của ta, $K = (z - 1) \div \ 4 + 1$).

Khi đó, **bài toán có lời giải khi và chỉ khi $N + K$ chẵn**.

## Cài đặt

Đoạn mã dưới đây minh họa thuật toán trên:

```cpp
int a[16];
for (int i=0; i<16; ++i)
    cin >> a[i];

int inv = 0;
for (int i=0; i<16; ++i)
    if (a[i])
        for (int j=0; j<i; ++j)
            if (a[j] > a[i])
                ++inv;
for (int i=0; i<16; ++i)
    if (a[i] == 0)
        inv += 1 + i / 4;

puts ((inv & 1) ? "No Solution" : "Solution Exists");
```

## Chứng minh

Năm 1879, Johnson chứng minh rằng nếu $N + K$ lẻ thì bài toán không có lời giải; cùng năm đó, Story chứng minh rằng mọi trạng thái có $N + K$ chẵn đều có lời giải.

Tuy nhiên, các chứng minh này khá phức tạp.

Năm 1999, Archer đưa ra một chứng minh đơn giản hơn nhiều (có thể tải bài báo của ông [tại đây](http://www.cs.cmu.edu/afs/cs/academic/class/15859-f01/www/notes/15-puzzle.pdf)).

## Bài tập thực hành

* [Hackerrank - N-puzzle](https://www.hackerrank.com/challenges/n-puzzle)
