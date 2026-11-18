---
tags:
    - Original
translation:
  source: num_methods/simulated_annealing.md
  source_commit: fd7dde44cc21761d73c8865ba49721770c176e35
  status: draft
  last_synced: 2026-11-16
---

# Luyện kim mô phỏng

**Luyện kim mô phỏng (Simulated Annealing, SA)** là thuật toán ngẫu nhiên dùng để xấp xỉ cực trị toàn cục của một hàm. Thuật toán sử dụng yếu tố ngẫu nhiên trong quá trình tìm kiếm, nên với cùng một đầu vào, kết quả có thể khác nhau.

## Bài toán

Cho hàm $E(s)$ tính năng lượng của trạng thái $s$. Nhiệm vụ là tìm trạng thái $s_{best}$ mà tại đó $E(s)$ nhỏ nhất. **SA** phù hợp với những bài toán có trạng thái rời rạc và $E(s)$ có nhiều cực tiểu địa phương. Ta sẽ xét ví dụ [bài toán người du lịch (TSP)](https://en.wikipedia.org/wiki/Travelling_salesman_problem).

### Bài toán người du lịch (TSP)

Cho một tập đỉnh trong không gian hai chiều. Mỗi đỉnh được xác định bởi tọa độ $x$ và $y$. Hãy tìm một thứ tự các đỉnh sao cho quãng đường đi qua chúng theo thứ tự đó là nhỏ nhất.

## Động cơ
Ủ là một quá trình luyện kim: vật liệu được nung nóng rồi để nguội, cho phép các nguyên tử bên trong sắp xếp lại theo cấu hình có nội năng nhỏ nhất, từ đó làm thay đổi tính chất vật liệu. Trạng thái là cách sắp xếp các nguyên tử và nội năng là hàm cần cực tiểu hóa. Có thể xem trạng thái ban đầu của các nguyên tử là một cực tiểu địa phương của nội năng. Để các nguyên tử sắp xếp lại, vật liệu phải vượt qua một vùng có nội năng chưa đạt cực tiểu để tới cực tiểu toàn cục. Việc nung nóng vật liệu lên nhiệt độ cao tạo điều kiện cho điều này.

Luyện kim mô phỏng mô phỏng đúng quá trình đó. Ta bắt đầu với một trạng thái ngẫu nhiên (vật liệu) và đặt nhiệt độ cao (nung nóng). Khi đó, nhờ nhiệt độ cao, thuật toán có thể chấp nhận trạng thái có năng lượng cao hơn trạng thái hiện tại. Điều này giúp thuật toán tránh mắc kẹt ở cực tiểu địa phương và tiến tới cực tiểu toàn cục. Theo thời gian, thuật toán nguội dần, từ chối các trạng thái năng lượng cao hơn và tiến về cực tiểu gần nhất đã tìm thấy.

### Hàm năng lượng E(s)

$E(s)$ là hàm cần cực tiểu hóa hoặc cực đại hóa. Nó ánh xạ mỗi trạng thái thành một số thực. Trong TSP, $E(s)$ trả về quãng đường đi hết một vòng theo thứ tự các đỉnh trong trạng thái.

### Trạng thái

Không gian trạng thái là miền xác định của hàm năng lượng $E(s)$; trạng thái là một phần tử bất kỳ thuộc không gian đó. Với TSP, không gian trạng thái gồm tất cả các đường đi có thể dùng để thăm mọi đỉnh, và mỗi đường đi như vậy là một trạng thái.

### Trạng thái lân cận

Đó là một trạng thái trong không gian trạng thái nằm gần trạng thái trước đó. Thông thường ta có thể thu được trạng thái lân cận từ trạng thái ban đầu bằng một phép biến đổi đơn giản. Với TSP, ta chọn ngẫu nhiên 2 đỉnh và đổi chỗ chúng trong trạng thái hiện tại.

## Thuật toán

Ta bắt đầu với trạng thái ngẫu nhiên $s$. Ở mỗi bước, chọn trạng thái lân cận $s_{next}$ của trạng thái hiện tại $s$. Nếu $E(s_{next}) < E(s)$, ta cập nhật $s = s_{next}$. Nếu không, ta dùng hàm xác suất chấp nhận $P(E(s),E(s_{next}),T)$ để quyết định chuyển sang $s_{next}$ hay giữ nguyên $s$. T là nhiệt độ, ban đầu được đặt cao rồi giảm dần sau mỗi bước. Nhiệt độ càng cao thì khả năng chuyển sang $s_{next}$ càng lớn. Đồng thời, ta lưu trạng thái tốt nhất $s_{best}$ trong tất cả các vòng lặp. Tiếp tục cho đến khi hội tụ hoặc hết thời gian.

<center>
<img src="https://upload.wikimedia.org/wikipedia/commons/d/d5/Hill_Climbing_with_Simulated_Annealing.gif" width="800px">
<br>
<i>Minh họa luyện kim mô phỏng tìm cực đại của một hàm có nhiều cực đại địa phương.</i>
<br>
</center>

### Nhiệt độ (T) và hệ số giảm (u)

Nhiệt độ biểu thị mức độ sẵn sàng chấp nhận một trạng thái có năng lượng cao hơn. Hệ số giảm là hằng số biểu thị "tốc độ làm nguội" của thuật toán. Tốc độ làm nguội chậm hơn ($u$ lớn hơn) được biết là cho kết quả tốt hơn.

## Hàm xác suất chấp nhận (PAF)

$P(E,E_{next},T) = 
    \begin{cases}
       \text{True} &\quad\text{if }  \mathcal{U}_{[0,1]} \le \exp(-\frac{E_{next}-E}{T}) \\
       \text{False} &\quad\text{otherwise}\\
     \end{cases}$

Ở đây $\mathcal{U}_{[0,1]}$ là giá trị ngẫu nhiên liên tục phân phối đều trên $[0,1]$. Hàm nhận trạng thái hiện tại, trạng thái kế tiếp và nhiệt độ, rồi trả về giá trị Boolean cho biết nên chuyển tới $s_{next}$ hay giữ nguyên $s$. Lưu ý khi $E_{next} < E$ hàm luôn trả về True; trong trường hợp còn lại, nó vẫn có thể chuyển với xác suất $\exp(-\frac{E_{next}-E}{T})$, tương ứng với [độ đo Gibbs](https://en.wikipedia.org/wiki/Gibbs_measure).

```cpp
bool P(double E,double E_next,double T,mt19937 rng){
    double prob =  exp(-(E_next-E)/T);
    if(prob > 1) return true;
    else{
        bernoulli_distribution d(prob); 
        return d(rng);
    }
}
```

**Ghi chú bản dịch:** Hàm xác suất trong mã nguồn nhận bộ sinh ngẫu nhiên bằng giá trị, nên trạng thái bộ sinh gốc không được cập nhật sau lời gọi. Nếu trạng thái bộ sinh gốc không đổi giữa các lời gọi thì chúng nhận cùng trạng thái và tạo cùng mẫu ngẫu nhiên; một cách khắc phục là truyền bộ sinh bằng tham chiếu.

## Mẫu mã

```cpp
class state {
    public:
    state() {
        // Generate the initial state
    }
    state next() {
        state s_next;
        // Modify s_next to a random neighboring state
        return s_next;
    }
    double E() {
        // Implement the energy function here
    };
};


pair<double, state> simAnneal() {
    state s = state();
    state best = s;
    double T = 10000; // Initial temperature
    double u = 0.995; // decay rate
    double E = s.E();
    double E_next;
    double E_best = E;
    mt19937 rng(chrono::steady_clock::now().time_since_epoch().count());
    while (T > 1) {
        state next = s.next();
        E_next = next.E();
        if (P(E, E_next, T, rng)) {
            s = next;
            if (E_next < E_best) {
                best = s;
                E_best = E_next;
            }
            E = E_next;
        }
        T *= u;
    }
    return {E_best, best};
}

```
## Cách sử dụng:
Điền các hàm của lớp trạng thái cho phù hợp. Nếu cần tìm cực đại toàn cục thay vì cực tiểu, hãy đảm bảo hàm $E()$ trả về số đối của hàm cần cực đại hóa và cuối cùng in ra $-E_{best}$. Đặt các tham số dưới đây theo nhu cầu.

### Tham số
- $T$ : Nhiệt độ ban đầu. Chọn giá trị cao hơn nếu muốn tìm kiếm chạy lâu hơn.
- $u$ : Hệ số giảm, quyết định tốc độ làm nguội. Làm nguội chậm hơn (u lớn hơn) thường cho kết quả tốt hơn nhưng chạy lâu hơn. Đảm bảo $u < 1$.

**Ghi chú bản dịch:** Với lịch làm nguội nhân như mã trên và công thức logarit bên dưới, hệ số giảm phải dương và nhỏ hơn một; điều kiện nhỏ hơn một trong nguồn chưa đủ. Công thức số vòng cũng giả sử nhiệt độ ban đầu lớn hơn một; khi nhiệt độ ban đầu không lớn hơn một, vòng lặp trong mã không chạy.

Số vòng lặp được cho bởi biểu thức

$N =   \lceil -\log_{u}{T} \rceil$ 

Gợi ý chọn $T$ và $u$: nếu có nhiều cực tiểu địa phương và không gian trạng thái rộng, đặt $u = 0.999$ để làm nguội chậm và cho thuật toán khám phá nhiều khả năng hơn. Ngược lại, nếu không gian hẹp hơn, $u = 0.99$ có thể đủ. Nếu không chắc chắn, hãy chọn an toàn với $u = 0.998$ hoặc lớn hơn. Tính độ phức tạp thời gian của một vòng lặp, từ đó ước lượng $N$ để tránh TLE, rồi dùng công thức dưới đây để tìm $T$.

$T = u^{-N}$

### Ví dụ cài đặt cho TSP
```cpp

class state {
    public:
    vector<pair<int, int>> points;
	std::mt19937 mt{ static_cast<std::mt19937::result_type>(
		std::chrono::steady_clock::now().time_since_epoch().count()
		) };
    state() {
        points = {%raw%} {{0,0},{2,2},{0,2},{2,0},{0,1},{1,2},{2,1},{1,0}} {%endraw%};
    }
    state next() {
        state s_next;
        s_next.points = points;
        uniform_int_distribution<> choose(0, points.size()-1);
        int a = choose(mt);
        int b = choose(mt);
        s_next.points[a].swap(s_next.points[b]);
        return s_next;
    }

    double euclidean(pair<int, int> a, pair<int, int> b) {
        return hypot(a.first - b.first, a.second - b.second);
    }
    
    double E() {
        double dist = 0;
        int n = points.size();
        for (int i = 0;i < n; i++)
            dist += euclidean(points[i], points[(i+1)%n]);
        return dist;
    };
};

int main() {
    pair<double, state> res;
    res = simAnneal();
    double E_best = res.first;
    state best = res.second;
    cout << "Length of shortest path found : " << E_best << "\n";
    cout << "Order of points in shortest path : \n";
    for(auto x: best.points) {
        cout << x.first << " " << x.second << "\n";
    }
}
```

## Các cách điều chỉnh thêm:

- Thêm điều kiện dừng theo thời gian vào vòng lặp while để tránh TLE.
- Hệ số giảm ở trên tạo quá trình giảm theo hàm mũ. Có thể thay bằng một hàm giảm khác tùy nhu cầu.
- Hàm xác suất chấp nhận ở trên ưu tiên chấp nhận trạng thái có năng lượng thấp hơn nhờ thừa số $E_{next} - E$ ở tử số của số mũ. Có thể bỏ thừa số này để PAF không phụ thuộc vào chênh lệch năng lượng.
- Có thể tăng hoặc giảm ảnh hưởng của chênh lệch năng lượng $E_{next} - E$ lên PAF bằng cách tăng hoặc giảm cơ số của hàm mũ như sau:
```cpp
bool P(double E, double E_next, double T, mt19937 rng) {
    double e = 2; // set e to any real number greater than 1
    double prob =  pow(e,-(E_next-E)/T);
    if (prob > 1)
        return true;
    else {
        bernoulli_distribution d(prob); 
        return d(rng);
    }
}
```

## Bài tập

- [USACO Jan 2017 - Subsequence Reversal](https://usaco.org/index.php?page=viewproblem2&cpid=698)
- [Deltix Summer 2021 - DIY Tree](https://codeforces.com/contest/1556/problem/H)
- [AtCoder Contest Scheduling](https://atcoder.jp/contests/intro-heuristics/tasks/intro_heuristics_a)

