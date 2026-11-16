---
tags:
  - Translated
e_maxx_link: triangles_union
translation:
  source: geometry/vertical_decomposition.md
  source_commit: 96853994fc29a65dda114dd117527076bd026b88
  status: draft
  last_synced: 2026-11-17
---

# Phân hoạch theo phương thẳng đứng

## Tổng quan
Phân hoạch theo phương thẳng đứng (vertical decomposition) là một kỹ thuật hữu ích trong nhiều bài toán hình học. Ý tưởng chung là chia mặt phẳng thành các dải thẳng đứng có một số tính chất “tốt”, rồi giải bài toán độc lập trên từng dải. Ta sẽ minh họa ý tưởng này qua một số ví dụ.

## Diện tích hợp của các tam giác
Giả sử có $n$ tam giác trên mặt phẳng và cần tìm diện tích hợp của chúng. Bài toán sẽ dễ nếu các tam giác không giao nhau. Vì vậy, ta loại bỏ các giao điểm này bằng cách chia mặt phẳng thành các dải thẳng đứng: vẽ những đường thẳng đứng đi qua mọi đỉnh và mọi giao điểm giữa các cạnh của những tam giác khác nhau. Có thể có $O(n^2)$ đường như vậy, nên ta thu được $O(n^2)$ dải. Xét một dải bất kỳ. Mỗi đoạn không thẳng đứng hoặc cắt dải từ trái sang phải, hoặc hoàn toàn không cắt dải.
Ngoài ra, không có hai đoạn nào giao nhau ở phần trong thực sự của dải. Do đó, phần hợp của các tam giác nằm trong dải gồm các hình thang không giao nhau, có hai đáy nằm trên hai biên của dải.
Tính chất này cho phép tính diện tích trong mỗi dải bằng thuật toán đường quét sau. Mỗi đoạn cắt dải là đoạn trên hoặc đoạn dưới, tùy theo phần trong của tam giác tương ứng nằm phía trên hay phía dưới đoạn đó. Ta có thể hình dung mỗi đoạn trên là một dấu ngoặc mở, mỗi đoạn dưới là một dấu ngoặc đóng, rồi chia dải thành các hình thang bằng cách phân tách dãy ngoặc thành những dãy ngoặc đúng nhỏ hơn. Thuật toán này cần $O(n^3\log n)$ thời gian và $O(n^2)$ bộ nhớ.

### Tối ưu 1
Trước tiên, ta giảm thời gian chạy xuống $O(n^2\log n)$. Thay vì tạo các hình thang cho từng dải, hãy cố định một cạnh tam giác (đoạn $s = (s_0, s_1)$) và tìm tập các dải mà đoạn này là một cạnh của hình thang. Lưu ý rằng khi đó ta chỉ cần tìm các dải mà độ cân bằng của dãy ngoặc phía dưới (hoặc phía trên nếu là đoạn dưới) $s$ bằng không. Do vậy, thay vì quét theo phương thẳng đứng cho từng dải, ta có thể quét theo phương ngang qua mọi phần của các đoạn khác ảnh hưởng đến độ cân bằng ngoặc đối với $s$.
Để đơn giản, ta trình bày cách xử lý đoạn trên; thuật toán cho đoạn dưới tương tự. Xét một đoạn không thẳng đứng khác $t = (t_0, t_1)$ và tìm giao $[x_1, x_2]$ của hình chiếu của $s$ và $t$ lên $Ox$. Nếu giao này rỗng hoặc chỉ gồm một điểm, có thể bỏ qua $t$ vì $s$ và $t$ không cùng giao phần trong của một dải nào. Ngược lại, xét giao $I$ của $s$ và $t$. Có ba trường hợp.

1.  $I = \varnothing$

    Trong trường hợp này $t$ nằm hoàn toàn phía trên hoặc phía dưới $s$ trên $[x_1, x_2]$. Nếu $t$ nằm phía trên thì nó không ảnh hưởng đến việc $s$ có phải là cạnh của một hình thang hay không.
    Nếu $t$ nằm phía dưới $s$, ta cần cộng $1$ hoặc $-1$ vào độ cân bằng của dãy ngoặc cho mọi dải trong $[x_1, x_2]$, tùy theo $t$ là đoạn trên hay đoạn dưới.

2.  $I$ gồm một điểm duy nhất $p$

    Ta có thể đưa trường hợp này về trường hợp trước bằng cách chia $[x_1, x_2]$ thành $[x_1, p_x]$ và $[p_x, x_2]$.

3.  $I$ là một đoạn $l$

    Trường hợp này nghĩa là các phần của $s$ và $t$ ứng với $x\in[x_1, x_2]$ trùng nhau. Nếu $t$ là đoạn dưới thì rõ ràng $s$ không phải là cạnh của một hình thang.
    Ngược lại, có thể cả $s$ và $t$ đều được coi là cạnh của một hình thang. Để giải quyết sự nhập nhằng này, ta có thể quyết định chỉ xét đoạn có chỉ số nhỏ nhất làm cạnh (ở đây giả sử các cạnh tam giác được đánh số theo một cách nào đó). Vì vậy, nếu $index(s) < index(t)$, ta bỏ qua trường hợp này; nếu không, ta đánh dấu rằng $s$ không bao giờ có thể là cạnh trên $[x_1, x_2]$ (ví dụ bằng cách thêm một sự kiện tương ứng với độ cân bằng $-2$).

Hình sau minh họa ba trường hợp.

<div style="text-align: center;">
  <img src="triangle_union.png" alt="Hình minh họa">
</div>

Cuối cùng, xét việc xử lý tất cả các phép cộng $1$ hoặc $-1$ trên mọi dải trong $[x_1, x_2]$. Với mỗi phép cộng $w$ trên $[x_1, x_2]$, ta có thể tạo các sự kiện $(x_1, w),\ (x_2, -w)$ và xử lý tất cả bằng đường quét.

### Tối ưu 2
Lưu ý rằng sau khi áp dụng tối ưu trước, ta không còn phải tìm tường minh tất cả các dải. Điều này giảm bộ nhớ cần dùng xuống $O(n)$.

## Giao của các đa giác lồi
Một ứng dụng khác của phân hoạch theo phương thẳng đứng là tính giao của hai đa giác lồi trong thời gian tuyến tính. Giả sử mặt phẳng được chia thành các dải thẳng đứng bởi những đường thẳng đứng đi qua từng đỉnh của mỗi đa giác. Khi đó, giao của một đa giác đầu vào với một dải bất kỳ là một hình thang, một tam giác hoặc một điểm. Vì vậy, ta có thể tính giao của các hình này trong từng dải thẳng đứng, rồi ghép các phần giao thành một đa giác duy nhất.

## Cài đặt

Dưới đây là mã tính diện tích hợp của một tập tam giác trong $O(n^2\log n)$ thời gian và $O(n)$ bộ nhớ.

```{.cpp file=triangle_union}
typedef double dbl;

const dbl eps = 1e-9;
 
inline bool eq(dbl x, dbl y){
    return fabs(x - y) < eps;
}
 
inline bool lt(dbl x, dbl y){
    return x < y - eps;
}
 
inline bool gt(dbl x, dbl y){
    return x > y + eps;
}
 
inline bool le(dbl x, dbl y){
    return x < y + eps;
}
 
inline bool ge(dbl x, dbl y){
    return x > y - eps;
}
 
struct pt{
    dbl x, y;
    inline pt operator - (const pt & p)const{
        return pt{x - p.x, y - p.y};
    }
    inline pt operator + (const pt & p)const{
        return pt{x + p.x, y + p.y};
    }
    inline pt operator * (dbl a)const{
        return pt{x * a, y * a};
    }
    inline dbl cross(const pt & p)const{
        return x * p.y - y * p.x;
    }
    inline dbl dot(const pt & p)const{
        return x * p.x + y * p.y;
    }
    inline bool operator == (const pt & p)const{
        return eq(x, p.x) && eq(y, p.y);
    }
};
 
struct Line{
    pt p[2];
    Line(){}
    Line(pt a, pt b):p{a, b}{}
    pt vec()const{
        return p[1] - p[0];
    }
    pt& operator [](size_t i){
        return p[i];
    }
};
 
inline bool lexComp(const pt & l, const pt & r){
	if(fabs(l.x - r.x) > eps){
		return l.x < r.x;
	}
	else return l.y < r.y;
}
 
vector<pt> interSegSeg(Line l1, Line l2){
    if(eq(l1.vec().cross(l2.vec()), 0)){
        if(!eq(l1.vec().cross(l2[0] - l1[0]), 0))
            return {};
        if(!lexComp(l1[0], l1[1]))
            swap(l1[0], l1[1]);
        if(!lexComp(l2[0], l2[1]))
            swap(l2[0], l2[1]);
        pt l = lexComp(l1[0], l2[0]) ? l2[0] : l1[0];
        pt r = lexComp(l1[1], l2[1]) ? l1[1] : l2[1];
        if(l == r)
            return {l};
        else return lexComp(l, r) ? vector<pt>{l, r} : vector<pt>();
    }
    else{
        dbl s = (l2[0] - l1[0]).cross(l2.vec()) / l1.vec().cross(l2.vec());
        pt inter = l1[0] + l1.vec() * s;
        if(ge(s, 0) && le(s, 1) && le((l2[0] - inter).dot(l2[1] - inter), 0))
            return {inter};
        else
            return {};
    }
}
inline char get_segtype(Line segment, pt other_point){
    if(eq(segment[0].x, segment[1].x))
        return 0;
    if(!lexComp(segment[0], segment[1]))
        swap(segment[0], segment[1]);
    return (segment[1] - segment[0]).cross(other_point - segment[0]) > 0 ? 1 : -1;
}
 
dbl union_area(vector<tuple<pt, pt, pt> > triangles){
    vector<Line> segments(3 * triangles.size());
    vector<char> segtype(segments.size());
    for(size_t i = 0; i < triangles.size(); i++){
        pt a, b, c;
        tie(a, b, c) = triangles[i];
        segments[3 * i] = lexComp(a, b) ? Line(a, b) : Line(b, a);
        segtype[3 * i] = get_segtype(segments[3 * i], c);
        segments[3 * i + 1] = lexComp(b, c) ? Line(b, c) : Line(c, b);
        segtype[3 * i + 1] = get_segtype(segments[3 * i + 1], a);
        segments[3 * i + 2] = lexComp(c, a) ? Line(c, a) : Line(a, c);
        segtype[3 * i + 2] = get_segtype(segments[3 * i + 2], b);
    }
    vector<dbl> k(segments.size()), b(segments.size());
    for(size_t i = 0; i < segments.size(); i++){
        if(segtype[i]){
            k[i] = (segments[i][1].y - segments[i][0].y) / (segments[i][1].x - segments[i][0].x);
            b[i] = segments[i][0].y - k[i] * segments[i][0].x;
        }
    }
    dbl ans = 0;
    for(size_t i = 0; i < segments.size(); i++){
        if(!segtype[i])
            continue;
        dbl l = segments[i][0].x, r = segments[i][1].x;
        vector<pair<dbl, int> > evts;
        for(size_t j = 0; j < segments.size(); j++){
            if(!segtype[j] || i == j)
                continue;
            dbl l1 = segments[j][0].x, r1 = segments[j][1].x;
            if(ge(l1, r) || ge(l, r1))
                continue;
            dbl common_l = max(l, l1), common_r = min(r, r1);
            auto pts = interSegSeg(segments[i], segments[j]);
            if(pts.empty()){
                dbl yl1 = k[j] * common_l + b[j];
                dbl yl = k[i] * common_l + b[i];
                if(lt(yl1, yl) == (segtype[i] == 1)){
                    int evt_type = -segtype[i] * segtype[j];
                    evts.emplace_back(common_l, evt_type);
                    evts.emplace_back(common_r, -evt_type);
                }
            }
            else if(pts.size() == 1u){
                dbl yl = k[i] * common_l + b[i], yl1 = k[j] * common_l + b[j];
                int evt_type = -segtype[i] * segtype[j];
                if(lt(yl1, yl) == (segtype[i] == 1)){
                    evts.emplace_back(common_l, evt_type);
                    evts.emplace_back(pts[0].x, -evt_type);
                }
                yl = k[i] * common_r + b[i], yl1 = k[j] * common_r + b[j];
                if(lt(yl1, yl) == (segtype[i] == 1)){
                    evts.emplace_back(pts[0].x, evt_type);
                    evts.emplace_back(common_r, -evt_type);
                }
            }
            else{
                if(segtype[j] != segtype[i] || j > i){
                    evts.emplace_back(common_l, -2);
                    evts.emplace_back(common_r, 2);
                }
            }
        }
        evts.emplace_back(l, 0);
        sort(evts.begin(), evts.end());
        size_t j = 0;
        int balance = 0;
        while(j < evts.size()){
            size_t ptr = j;
            while(ptr < evts.size() && eq(evts[j].first, evts[ptr].first)){
                balance += evts[ptr].second;
                ++ptr;
            }
            if(!balance && !eq(evts[j].first, r)){
                dbl next_x = ptr == evts.size() ? r : evts[ptr].first;
                ans -= segtype[i] * (k[i] * (next_x + evts[j].first) + 2 * b[i]) * (next_x - evts[j].first);
            }
            j = ptr;
        }
    }
    return ans/2;
}

```


## Bài tập
 * [Codeforces 62C Inquisition](https://codeforces.com/contest/62/problem/C)
 * [Codeforces 107E Darts](https://codeforces.com/contest/107/problem/E)
