---
tags:
  - Translated
e_maxx_link: convex_hull_graham
translation:
  source: geometry/convex-hull.md
  source_commit: 0b2fe2fe9f67149c4d220420a9194078290c52ae
  status: draft
  last_synced: 2026-08-08
---

# Xây dựng bao lồi

Trong bài viết này, ta sẽ xét bài toán xây dựng bao lồi từ một tập điểm.

Cho $N$ điểm trên mặt phẳng. Mục tiêu là tạo bao lồi, tức đa giác lồi nhỏ nhất chứa tất cả các điểm đã cho.

Ta sẽ tìm hiểu thuật toán **Graham's scan** do Graham công bố năm 1972 và thuật toán **Monotone chain** do Andrew công bố năm 1979. Cả hai đều có độ phức tạp $\mathcal{O}(N \log N)$ và tối ưu về mặt tiệm cận (đã chứng minh không tồn tại thuật toán tốt hơn về mặt tiệm cận), ngoại trừ một số bài toán có xử lý song song hoặc online.

## Thuật toán Graham's scan
Thuật toán trước hết tìm điểm thấp nhất $P_0$. Nếu có nhiều điểm cùng tọa độ Y, ta chọn điểm có tọa độ X nhỏ hơn. Bước này mất $\mathcal{O}(N)$ thời gian.

Tiếp theo, sắp xếp tất cả các điểm còn lại theo góc cực theo chiều kim đồng hồ.
Nếu hai hay nhiều điểm có cùng góc cực, ta sắp xếp tiếp theo khoảng cách đến $P_0$ tăng dần.

Sau đó, ta lần lượt duyệt từng điểm và bảo đảm rằng điểm hiện tại cùng hai điểm trước nó tạo thành một lần rẽ theo chiều kim đồng hồ. Nếu không, điểm trước đó bị loại vì nó sẽ làm hình thu được không còn lồi. Có thể kiểm tra hướng quay theo hoặc ngược chiều kim đồng hồ bằng [orientation](oriented-triangle-area.md).

Ta dùng một ngăn xếp để lưu các điểm. Khi đi đến điểm ban đầu $P_0$, thuật toán kết thúc và trả về ngăn xếp chứa các điểm của bao lồi theo thứ tự chiều kim đồng hồ.

Nếu cần giữ cả các điểm thẳng hàng khi thực hiện Graham scan, ta cần thêm một bước sau khi sắp xếp. Hãy lấy các điểm có “khoảng cách cực” lớn nhất đến $P_0$ (chúng nằm ở cuối vector đã sắp xếp) và thẳng hàng.
Các điểm trên đường thẳng này cần được đảo thứ tự để ta có thể đưa tất cả các điểm thẳng hàng vào kết quả; nếu không, thuật toán sẽ lấy điểm gần nhất trên đường này rồi dừng xử lý phần còn lại. Không nên thực hiện bước này ở phiên bản không giữ điểm thẳng hàng, vì khi đó kết quả sẽ không còn là bao lồi nhỏ nhất.

**Ghi chú bản dịch:** Ở đoạn trên, nguồn dùng cụm “biggest polar distance”. Tuy nhiên, cài đặt thực tế lấy dãy điểm ở cuối thứ tự góc cực, tức các điểm thẳng hàng theo hướng có góc cực lớn nhất. Cách diễn đạt này đang được đề xuất làm rõ riêng ở bản tiếng Anh.

### Cài đặt

```{.cpp file=graham_scan}
struct pt {
    double x, y;
    bool operator == (pt const& t) const {
        return x == t.x && y == t.y;
    }
};

int orientation(pt a, pt b, pt c) {
    double v = a.x*(b.y-c.y)+b.x*(c.y-a.y)+c.x*(a.y-b.y);
    if (v < 0) return -1; // clockwise
    if (v > 0) return +1; // counter-clockwise
    return 0;
}

bool cw(pt a, pt b, pt c, bool include_collinear) {
    int o = orientation(a, b, c);
    return o < 0 || (include_collinear && o == 0);
}
bool collinear(pt a, pt b, pt c) { return orientation(a, b, c) == 0; }

void convex_hull(vector<pt>& a, bool include_collinear = false) {
    pt p0 = *min_element(a.begin(), a.end(), [](pt a, pt b) {
        return make_pair(a.y, a.x) < make_pair(b.y, b.x);
    });
    sort(a.begin(), a.end(), [&p0](const pt& a, const pt& b) {
        int o = orientation(p0, a, b);
        if (o == 0)
            return (p0.x-a.x)*(p0.x-a.x) + (p0.y-a.y)*(p0.y-a.y)
                < (p0.x-b.x)*(p0.x-b.x) + (p0.y-a.y)*(p0.y-a.y);
        return o < 0;
    });
    if (include_collinear) {
        int i = (int)a.size()-1;
        while (i >= 0 && collinear(p0, a[i], a.back())) i--;
        reverse(a.begin()+i+1, a.end());
    }

    vector<pt> st;
    for (int i = 0; i < (int)a.size(); i++) {
        while (st.size() > 1 && !cw(st[st.size()-2], st.back(), a[i], include_collinear))
            st.pop_back();
        st.push_back(a[i]);
    }

    if (include_collinear == false && st.size() == 2 && st[0] == st[1])
        st.pop_back();

    a = st;
}
```

## Thuật toán Monotone chain
Thuật toán trước hết tìm điểm trái nhất và phải nhất, ký hiệu là A và B. Nếu có nhiều điểm như vậy, ta chọn điểm thấp nhất trong các điểm trái nhất (tọa độ Y nhỏ nhất) làm A, và điểm cao nhất trong các điểm phải nhất (tọa độ Y lớn nhất) làm B. Rõ ràng A và B đều phải thuộc bao lồi vì chúng là các điểm nằm xa nhất về hai phía và không thể bị chứa bởi bất kỳ đường thẳng nào đi qua một cặp điểm trong tập đã cho.

**Ghi chú bản dịch:** Cách giải thích “the farthest away” và “contained by any line” trong nguồn khá mơ hồ. Với cách chọn A và B ở đây, lý do trực tiếp là chúng là hai điểm cực trị theo tọa độ x, nên phải nằm trên biên của bao lồi. Cách diễn đạt nguồn đang được đề xuất làm rõ riêng ở bản tiếng Anh.

Bây giờ, kẻ đường thẳng qua AB. Đường này chia tất cả các điểm còn lại thành hai tập S1 và S2, trong đó S1 chứa tất cả các điểm phía trên đường nối A và B, còn S2 chứa tất cả các điểm phía dưới. Các điểm nằm trên đường thẳng AB có thể thuộc một trong hai tập. Hai điểm A và B thuộc cả hai tập. Thuật toán lần lượt xây dựng tập trên S1 và tập dưới S2 rồi kết hợp chúng để thu được đáp án. 

Để xây dựng tập trên, ta sắp xếp tất cả các điểm theo tọa độ x. Với mỗi điểm, ta kiểm tra một trong hai điều kiện: điểm hiện tại là điểm cuối cùng (đã định nghĩa là B), hoặc hướng quay giữa đoạn từ A đến điểm hiện tại và đoạn từ điểm hiện tại đến B là theo chiều kim đồng hồ. Trong các trường hợp đó, điểm hiện tại thuộc tập trên S1. Có thể kiểm tra hướng quay theo hoặc ngược chiều kim đồng hồ bằng [orientation](oriented-triangle-area.md).

Nếu điểm đã cho thuộc tập trên, ta xét góc tạo bởi đoạn nối điểm áp chót với điểm cuối cùng của bao lồi trên và đoạn nối điểm cuối cùng đó với điểm hiện tại. Nếu góc không quay theo chiều kim đồng hồ, ta loại điểm vừa được thêm gần nhất khỏi bao lồi trên, vì sau khi điểm hiện tại được thêm vào, nó sẽ khiến điểm trước đó nằm bên trong phần bao.

Logic tương tự áp dụng cho tập dưới S2. Nếu điểm hiện tại là B, hoặc hướng quay của hai đoạn tạo bởi A với điểm hiện tại và điểm hiện tại với B là ngược chiều kim đồng hồ, thì điểm đó thuộc S2.

Nếu điểm đã cho thuộc tập dưới, ta xử lý tương tự như với tập trên nhưng kiểm tra hướng ngược chiều kim đồng hồ thay vì theo chiều kim đồng hồ. Vì vậy, nếu góc tạo bởi đoạn nối điểm áp chót với điểm cuối cùng của bao lồi dưới và đoạn nối điểm cuối cùng đó với điểm hiện tại không quay ngược chiều kim đồng hồ, ta loại điểm vừa được thêm gần nhất khỏi bao lồi dưới, vì sau khi thêm điểm hiện tại, điểm trước đó sẽ nằm bên trong phần bao.

Bao lồi cuối cùng là hợp của bao lồi trên và bao lồi dưới, tạo thành một bao lồi theo chiều kim đồng hồ. Cài đặt như sau.

Nếu cần giữ các điểm thẳng hàng, ta chỉ cần kiểm tra chúng trong các hàm xác định chiều kim đồng hồ/ngược chiều kim đồng hồ.
Tuy nhiên, điều này tạo ra một trường hợp suy biến khi tất cả điểm đầu vào cùng nằm trên một đường thẳng: thuật toán sẽ xuất hiện các điểm lặp lại trong kết quả.
Để xử lý, ta kiểm tra xem bao lồi trên có chứa tất cả các điểm hay không; nếu có, chỉ cần trả về các điểm theo thứ tự đảo ngược, giống kết quả mà cài đặt Graham trả về trong trường hợp này.

### Cài đặt

```{.cpp file=monotone_chain}
struct pt {
    double x, y;
};

int orientation(pt a, pt b, pt c) {
    double v = a.x*(b.y-c.y)+b.x*(c.y-a.y)+c.x*(a.y-b.y);
    if (v < 0) return -1; // clockwise
    if (v > 0) return +1; // counter-clockwise
    return 0;
}

bool cw(pt a, pt b, pt c, bool include_collinear) {
    int o = orientation(a, b, c);
    return o < 0 || (include_collinear && o == 0);
}
bool ccw(pt a, pt b, pt c, bool include_collinear) {
    int o = orientation(a, b, c);
    return o > 0 || (include_collinear && o == 0);
}

void convex_hull(vector<pt>& a, bool include_collinear = false) {
    if (a.size() == 1)
        return;

    sort(a.begin(), a.end(), [](pt a, pt b) {
        return make_pair(a.x, a.y) < make_pair(b.x, b.y);
    });
    pt p1 = a[0], p2 = a.back();
    vector<pt> up, down;
    up.push_back(p1);
    down.push_back(p1);
    for (int i = 1; i < (int)a.size(); i++) {
        if (i == a.size() - 1 || cw(p1, a[i], p2, include_collinear)) {
            while (up.size() >= 2 && !cw(up[up.size()-2], up[up.size()-1], a[i], include_collinear))
                up.pop_back();
            up.push_back(a[i]);
        }
        if (i == a.size() - 1 || ccw(p1, a[i], p2, include_collinear)) {
            while (down.size() >= 2 && !ccw(down[down.size()-2], down[down.size()-1], a[i], include_collinear))
                down.pop_back();
            down.push_back(a[i]);
        }
    }

    if (include_collinear && up.size() == a.size()) {
        reverse(a.begin(), a.end());
        return;
    }
    a.clear();
    for (int i = 0; i < (int)up.size(); i++)
        a.push_back(up[i]);
    for (int i = down.size() - 2; i > 0; i--)
        a.push_back(down[i]);
}
```

## Bài tập luyện tập

* [Kattis - Convex Hull](https://open.kattis.com/problems/convexhull)
* [Kattis - Keep the Parade Safe](https://open.kattis.com/problems/parade)
* [Codeforces - I. Birthday](https://codeforces.com/contest/2172/problem/I)
* [Latin American Regionals 2006 - Onion Layers](https://matcomgrader.com/problem/9413/onion-layers/)
* [Timus 1185: Wall](http://acm.timus.ru/problem.aspx?space=1&num=1185)
* [Usaco 2014 January Contest, Gold - Cow Curling](http://usaco.org/index.php?page=viewproblem2&cpid=382)
