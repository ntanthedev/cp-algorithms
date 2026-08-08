---
tags:
  - Original
translation:
  source: geometry/convex_hull_trick.md
  source_commit: 052073e2caf6766ce5f22aeb1d44d59e7bf4f2b5
  status: draft
  last_synced: 2026-08-08
---

# Kỹ thuật bao lồi và cây Li Chao

Xét bài toán sau. Có $n$ thành phố. Bạn muốn đi ô tô từ thành phố $1$ đến thành phố $n$. Để làm được điều đó, bạn phải mua xăng. Biết rằng một lít xăng có giá $cost_k$ tại thành phố $k^{th}$. Ban đầu bình xăng rỗng và xe tiêu thụ một lít xăng cho mỗi ki-lô-mét. Các thành phố nằm trên cùng một đường thẳng theo thứ tự tăng dần, trong đó thành phố $k^{th}$ có tọa độ $x_k$. Ngoài ra, bạn phải trả phí $toll_k$ để đi vào thành phố $k^{th}$. Mục tiêu là hoàn thành chuyến đi với chi phí nhỏ nhất có thể. Có thể thấy lời giải được tính bằng quy hoạch động:

$$dp_i = toll_i+\min\limits_{j<i}(cost_j \cdot (x_i - x_j)+dp_j)$$

Cách làm trực tiếp có độ phức tạp $O(n^2)$, có thể cải thiện xuống $O(n \log n)$ hoặc $O(n \log [C \varepsilon^{-1}])$, trong đó $C$ là giá trị lớn nhất có thể của $|x_i|$ và $\varepsilon$ là độ chính xác dùng để xét $x_i$ ($\varepsilon = 1$ với số nguyên, là trường hợp thường gặp). Để làm được điều này, hãy nhận thấy bài toán có thể quy về việc thêm các hàm tuyến tính $k \cdot x + b$ vào một tập và tìm giá trị nhỏ nhất của các hàm tại một điểm $x$ cho trước. Có hai cách tiếp cận chính.

## Kỹ thuật bao lồi

Ý tưởng của cách tiếp cận này là duy trì bao lồi dưới của các hàm tuyến tính.
Thực ra, sẽ thuận tiện hơn một chút nếu không xem chúng là các hàm tuyến tính mà xem mỗi hàm như một điểm $(k;b)$ trên mặt phẳng. Khi đó, ta cần tìm điểm có tích vô hướng nhỏ nhất với điểm cho trước $(x;1)$, tức là tìm điểm làm $kx+b$ nhỏ nhất, đúng như bài toán ban đầu.
Giá trị nhỏ nhất đó nhất thiết đạt được tại biên dưới của bao lồi các điểm này, như hình minh họa:

<div style="text-align: center;">
  <img src="convex_hull_trick.png" alt="bao lồi dưới">
</div>

Ta cần duy trì các điểm trên bao lồi và các vector pháp tuyến của các cạnh bao lồi.
Khi có truy vấn $(x;1)$, ta cần tìm vector pháp tuyến gần nó nhất xét theo góc giữa hai vector; hàm tuyến tính tối ưu khi đó sẽ tương ứng với một trong hai đầu mút của cạnh đó.
Để thấy điều này, lưu ý rằng các điểm có tích vô hướng không đổi với $(x;1)$ nằm trên một đường thẳng vuông góc với $(x;1)$. Vì vậy, hàm tuyến tính tối ưu chính là điểm mà tại đó tiếp tuyến của bao lồi, song song với vector pháp tuyến của $(x;1)$, tiếp xúc với bao lồi.
Đó là điểm sao cho các pháp tuyến của cạnh nằm bên trái và bên phải nó hướng về hai phía khác nhau của $(x;1)$.

Cách tiếp cận này hữu ích khi các truy vấn thêm hàm tuyến tính có $k$ đơn điệu, hoặc khi xử lý offline, tức là ta có thể thêm tất cả các hàm trước rồi mới trả lời truy vấn.
Vì vậy, ta không thể giải bài toán thành phố/xăng ở trên theo cách này.
Bài toán đó đòi hỏi phải xử lý truy vấn online.
Với truy vấn online, việc cài đặt sẽ phức tạp hơn và thường cần một cấu trúc dữ liệu dạng tập để duy trì bao lồi đúng cách.
Bài viết này không xét cách tiếp cận online đó vì khá phức tạp, đồng thời cách tiếp cận thứ hai (cây Li Chao) cho phép giải bài toán đơn giản hơn nhiều.
Cũng cần nhắc rằng ta vẫn có thể dùng cách tiếp cận này online mà không quá phức tạp bằng chia căn.
Cụ thể, cứ sau mỗi $\sqrt n$ đường thẳng mới, ta dựng lại bao lồi từ đầu. 

Để cài đặt cách tiếp cận này, trước hết cần một số hàm tiện ích hình học. Ở đây ta dùng kiểu số phức của C++.

```cpp
typedef int ftype;
typedef complex<ftype> point;
#define x real
#define y imag
 
ftype dot(point a, point b) {
	return (conj(a) * b).x();
}
 
ftype cross(point a, point b) {
	return (conj(a) * b).y();
}
```

Ta giả sử khi thêm các hàm tuyến tính thì $k$ chỉ tăng, và ta muốn tìm giá trị nhỏ nhất.
Ta lưu các điểm trong vector $hull$ và các vector pháp tuyến trong vector $vecs$.
Khi thêm một điểm mới, ta xét góc tạo bởi cạnh cuối cùng của bao lồi và vector từ điểm cuối cùng của bao lồi đến điểm mới.
Góc này phải quay theo chiều ngược kim đồng hồ; tương đương, tích vô hướng của vector pháp tuyến cuối cùng trong bao lồi (hướng vào trong bao lồi) với vector từ điểm cuối cùng đến điểm mới phải không âm.
Chừng nào điều này chưa đúng, ta xóa điểm cuối cùng của bao lồi cùng cạnh tương ứng.

```cpp
vector<point> hull, vecs;
 
void add_line(ftype k, ftype b) {
    point nw = {k, b};
    while(!vecs.empty() && dot(vecs.back(), nw - hull.back()) < 0) {
        hull.pop_back();
        vecs.pop_back();
    }
    if(!hull.empty()) {
        vecs.push_back(1i * (nw - hull.back()));
    }
    hull.push_back(nw);
}
 
```
Bây giờ, để lấy giá trị nhỏ nhất tại một điểm, ta tìm vector pháp tuyến đầu tiên trên bao lồi nằm theo chiều ngược kim đồng hồ so với $(x;1)$. Đầu mút bên trái của cạnh đó sẽ cho đáp án. Để kiểm tra vector $a$ không nằm theo chiều ngược kim đồng hồ so với vector $b$, ta kiểm tra tích có hướng $[a,b]$ của chúng có dương hay không.
```cpp
int get(ftype x) {
    point query = {x, 1};
    auto it = lower_bound(vecs.begin(), vecs.end(), query, [](point a, point b) {
        return cross(a, b) > 0;
    });
    return dot(query, hull[it - vecs.begin()]);
}
```

## Cây Li Chao

Giả sử ta có một tập hàm sao cho mỗi cặp hàm giao nhau nhiều nhất một lần. Ta lưu tại mỗi đỉnh của một cây phân đoạn một hàm theo cách sao cho khi đi từ gốc đến một lá, chắc chắn một trong các hàm gặp trên đường đi là hàm cho giá trị nhỏ nhất tại lá đó. Ta sẽ xem cách xây dựng cấu trúc này.

Giả sử ta đang ở một đỉnh tương ứng với đoạn nửa mở $[l,r)$, tại đó đang lưu hàm $f_{old}$ và ta muốn thêm hàm $f_{new}$. Khi đó, giao điểm của hai hàm sẽ nằm trong $[l;m)$ hoặc $[m;r)$, với $m=\left\lfloor\tfrac{l+r}{2}\right\rfloor$. Ta có thể xác định nửa chứa giao điểm một cách hiệu quả bằng cách so sánh giá trị hai hàm tại $l$ và $m$. Nếu hàm chiếm ưu thế thay đổi thì giao điểm nằm trong $[l;m)$; nếu không, nó nằm trong $[m;r)$. Với nửa không chứa giao điểm, ta chọn hàm thấp hơn và lưu nó tại đỉnh hiện tại. Có thể thấy đó luôn là hàm thấp hơn tại điểm $m$. Sau đó, ta đệ quy sang nửa còn lại với hàm trước đó nằm phía trên. Như vậy, tính đúng đắn được giữ nguyên ở nửa đầu, còn ở nửa kia sẽ được duy trì trong lời gọi đệ quy. Do đó, ta có thể thêm hàm và truy vấn giá trị nhỏ nhất tại một điểm trong $O(\log [C\varepsilon^{-1}])$.

Hình sau minh họa những gì xảy ra tại một đỉnh khi thêm hàm mới:

<div style="text-align: center;">
  <img src="li_chao_vertex.png" alt="đỉnh của cây Li Chao">
</div>

Bây giờ chuyển sang phần cài đặt. Một lần nữa, ta dùng số phức để lưu các hàm tuyến tính.

```{.cpp file=lichaotree_line_definition}
typedef long long ftype;
typedef complex<ftype> point;
#define x real
#define y imag
 
ftype dot(point a, point b) {
    return (conj(a) * b).x();
}
 
ftype f(point a,  ftype x) {
    return dot(a, {x, 1});
}
```
Ta lưu các hàm trong mảng $line$ và dùng cách đánh chỉ số nhị phân của cây phân đoạn. Nếu muốn làm việc với các số lớn hoặc số thực kiểu double, bạn nên dùng cây phân đoạn động. 
Cây phân đoạn cần được khởi tạo bằng các giá trị mặc định, chẳng hạn các đường thẳng $0x + \infty$.

```{.cpp file=lichaotree_addline}
const int maxn = 2e5;
 
point line[4 * maxn];
 
void add_line(point nw, int v = 1, int l = 0, int r = maxn) {
    int m = (l + r) / 2;
    bool lef = f(nw, l) < f(line[v], l);
    bool mid = f(nw, m) < f(line[v], m);
    if(mid) {
        swap(line[v], nw);
    }
    if(r - l == 1) {
        return;
    } else if(lef != mid) {
        add_line(nw, 2 * v, l, m);
    } else {
        add_line(nw, 2 * v + 1, m, r);
    }
}
```
Để lấy giá trị nhỏ nhất tại một điểm $x$, ta chỉ cần chọn giá trị nhỏ nhất dọc theo đường đi đến điểm đó.
```{.cpp file=lichaotree_getminimum}
ftype get(int x, int v = 1, int l = 0, int r = maxn) {
    int m = (l + r) / 2;
    if(r - l == 1) {
        return f(line[v], x);
    } else if(x < m) {
        return min(f(line[v], x), get(x, 2 * v, l, m));
    } else {
        return min(f(line[v], x), get(x, 2 * v + 1, m, r));
    }
}
```

## Bài tập

* [Codebreaker - TROUBLES](https://codeforces.com/gym/103536/problem/B) (ứng dụng đơn giản của Convex Hull Trick sau một vài nhận xét)
* [CS Academy - Squared Ends](https://csacademy.com/contest/archive/task/squared-ends)
* [Codeforces - Escape Through Leaf](http://codeforces.com/contest/932/problem/F)
* [CodeChef - Polynomials](https://www.codechef.com/NOV17/problems/POLY)
* [Codeforces - Kalila and Dimna in the Logging Industry](https://codeforces.com/problemset/problem/319/C)
* [Codeforces - Product Sum](https://codeforces.com/problemset/problem/631/E)
* [Codeforces - Bear and Bowling 4](https://codeforces.com/problemset/problem/660/F)
* [APIO 2010 - Commando](https://dmoj.ca/problem/apio10p1)
