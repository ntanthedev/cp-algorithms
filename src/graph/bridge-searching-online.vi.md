---
tags:
  - Translated
e_maxx_link: bridge_searching_online
translation:
  source: graph/bridge-searching-online.md
  source_commit: 279430b1814486e54cddf78e6a209f5ce015d08b
  status: draft
  last_synced: 2026-11-16
---

# Tìm cạnh cầu trực tuyến

Cho một đồ thị vô hướng.
Cạnh cầu là cạnh mà khi xóa đi thì đồ thị bị mất liên thông (hay chính xác hơn là số thành phần liên thông tăng lên).
Ta cần tìm tất cả các cạnh cầu trong đồ thị đã cho.

Có thể phát biểu bài toán một cách không hình thức như sau:
ta cần tìm tất cả các con đường "quan trọng" trên bản đồ đường sá, tức những con đường mà khi xóa bất kỳ đường nào thì một số thành phố không thể đi đến từ các thành phố khác.

Bài [Tìm cạnh cầu trong $O(N+M)$](bridge-searching.md) đã giải bài toán này bằng phép duyệt [tìm kiếm theo chiều sâu](depth-first-search.md).
Thuật toán sau đây phức tạp hơn nhiều nhưng có một ưu điểm lớn:
nó hoạt động trực tuyến, nghĩa là không cần biết trước đồ thị đầu vào.
Các cạnh được thêm vào từng cạnh một, và sau mỗi lần thêm, thuật toán đếm lại tất cả các cạnh cầu trong đồ thị hiện tại.
Nói cách khác, thuật toán được thiết kế để hoạt động hiệu quả trên đồ thị động, thay đổi theo thời gian.

Phát biểu bài toán chính xác hơn như sau:
Ban đầu đồ thị rỗng và gồm $n$ đỉnh.
Sau đó ta nhận các cặp đỉnh $(a, b)$, biểu thị một cạnh được thêm vào đồ thị.
Sau mỗi cạnh nhận được, tức sau khi thêm mỗi cạnh, hãy xuất số cạnh cầu hiện tại trong đồ thị.

Ta cũng có thể duy trì danh sách tất cả các cạnh cầu cũng như hỗ trợ tường minh các thành phần liên thông 2 cạnh.

Thuật toán dưới đây chạy trong thời gian $O(n \log n + m)$, với $m$ là số cạnh.
Thuật toán dựa trên cấu trúc dữ liệu [hợp các tập rời nhau](../data_structures/disjoint_set_union.md) (DSU).
Tuy nhiên, cài đặt trong bài chạy trong thời gian $O(n \log n + m \log n)$ vì dùng phiên bản DSU đơn giản hóa không có hợp theo hạng.

## Thuật toán

Trước tiên, định nghĩa thành phần liên thông $k$ cạnh:
đó là một thành phần liên thông vẫn liên thông mỗi khi xóa ít hơn $k$ cạnh.

Có thể dễ dàng thấy các cạnh cầu chia đồ thị thành các thành phần liên thông 2 cạnh.
Nếu co mỗi thành phần liên thông 2 cạnh thành một đỉnh và chỉ giữ các cạnh cầu làm cạnh của đồ thị đã co, ta được một đồ thị không chu trình, tức là một rừng.

Thuật toán dưới đây duy trì tường minh rừng này cùng với các thành phần liên thông 2 cạnh.

Rõ ràng ban đầu khi đồ thị rỗng, nó có $n$ thành phần liên thông 2 cạnh không nối với nhau.

Khi thêm cạnh tiếp theo $(a, b)$, có thể xảy ra ba trường hợp:

*   Hai đỉnh $a$ và $b$ thuộc cùng một thành phần liên thông 2 cạnh. Khi đó cạnh này không phải cầu và không làm thay đổi cấu trúc rừng, nên ta có thể bỏ qua.

    Do đó trong trường hợp này số cạnh cầu không đổi.

*   Các đỉnh $a$ và $b$ thuộc hai thành phần liên thông khác nhau, tức mỗi đỉnh thuộc một cây khác nhau.
    Khi đó cạnh $(a, b)$ trở thành một cạnh cầu mới, hai cây được gộp thành một (và tất cả các cạnh cầu cũ vẫn còn).

    Do đó trong trường hợp này số cạnh cầu tăng một.

*   Các đỉnh $a$ và $b$ thuộc cùng một thành phần liên thông nhưng thuộc hai thành phần liên thông 2 cạnh khác nhau.
    Khi đó cạnh này cùng một số cạnh cầu cũ tạo thành một chu trình.
    Tất cả các cạnh cầu đó không còn là cầu, và chu trình tạo thành phải được co thành một thành phần liên thông 2 cạnh mới.

    Do đó trong trường hợp này số cạnh cầu giảm một hoặc nhiều hơn.

Vì vậy, toàn bộ bài toán được quy về việc cài đặt hiệu quả các phép toán này trên rừng các thành phần liên thông 2 cạnh.

## Cấu trúc dữ liệu lưu rừng

Cấu trúc dữ liệu duy nhất ta cần là [hợp các tập rời nhau](../data_structures/disjoint_set_union.md).
Thực tế ta sẽ dùng hai bản của cấu trúc này:
một bản duy trì các thành phần liên thông, bản còn lại duy trì các thành phần liên thông 2 cạnh.
Ngoài ra, ta lưu cấu trúc các cây trong rừng thành phần liên thông 2 cạnh bằng các con trỏ:
mỗi thành phần liên thông 2 cạnh lưu chỉ số `par[]` của đỉnh cha trong cây.

Ta lần lượt phân tích từng phép toán cần cài đặt:

  * Kiểm tra hai đỉnh có cùng thành phần liên thông / thành phần liên thông 2 cạnh hay không.
    Ta dùng thuật toán DSU thông thường: tìm và so sánh các phần tử đại diện của DSU.
  
  * Nối hai cây bởi một cạnh $(a, b)$.
    Vì có thể cả $a$ và $b$ đều không phải gốc cây tương ứng, cách duy nhất để nối hai cây là đổi gốc một cây.
    Chẳng hạn ta đổi gốc cây chứa $a$ thành chính đỉnh đó, rồi gắn nó vào cây kia bằng cách đặt cha của $a$ là $b$.
  
    Tuy nhiên, cần xét hiệu quả của phép đổi gốc:
    để đổi gốc cây từ $r$ sang đỉnh $v$, ta phải duyệt tất cả các đỉnh trên đường từ $v$ đến $r$ và đảo chiều các con trỏ `par[]`, đồng thời thay đổi các tham chiếu đến cha trong DSU quản lý các thành phần liên thông.
  
    Như vậy, chi phí đổi gốc là $O(h)$, với $h$ là chiều cao cây.
    Ta có thể dùng cận kém hơn là $O(\text{size})$, với $\text{size}$ là số đỉnh trong cây.
    Độ phức tạp cuối cùng sẽ không khác.
  
    Bây giờ ta áp dụng một kỹ thuật chuẩn: đổi gốc cây chứa ít đỉnh hơn.
    Khi đó, trực giác cho thấy trường hợp xấu nhất là gộp hai cây có kích thước xấp xỉ nhau, nhưng kết quả lại là cây có kích thước gấp đôi.
    Vì vậy trường hợp này không thể xảy ra nhiều lần.
  
    Nói chung, tổng chi phí có thể viết dưới dạng truy hồi:
    
    \[ T(n) = \max_{k = 1 \ldots n-1} \left\{ T(k) + T(n - k) + O(\min(k, n - k))\right\} \]
    
    $T(n)$ là số phép toán cần để thu được một cây có $n$ đỉnh bằng cách đổi gốc và gộp cây.
    Có thể tạo cây kích thước $n$ bằng cách gộp hai cây nhỏ hơn có kích thước $k$ và $n - k$.
    Hệ thức truy hồi này có nghiệm $T(n) = O (n \log n)$.
  
    Do đó tổng thời gian dành cho mọi phép đổi gốc là $O(n \log n)$ nếu luôn đổi gốc cây nhỏ hơn.
  
    Ta phải duy trì kích thước mỗi thành phần liên thông, nhưng cấu trúc DSU cho phép làm điều đó dễ dàng.
  
  * Tìm chu trình hình thành khi thêm cạnh mới $(a, b)$.
    Vì $a$ và $b$ đã được nối trong cây, ta cần tìm [tổ tiên chung gần nhất](lca.md) của hai đỉnh $a$ và $b$.
    Chu trình gồm các đường từ $b$ đến LCA, từ LCA đến $a$ và cạnh từ $a$ đến $b$.
  
    Sau khi tìm thấy chu trình, ta co tất cả các đỉnh của nó thành một đỉnh.
    Vì vậy ta đã có độ phức tạp tỉ lệ với độ dài chu trình; ta cũng có thể dùng bất kỳ thuật toán LCA nào có độ phức tạp tỉ lệ với độ dài đó mà không cần dùng thuật toán nhanh.
  
    Vì mọi thông tin về cấu trúc cây đều có trong mảng cha `par[]`, thuật toán LCA hợp lý duy nhất là:
    đánh dấu các đỉnh $a$ và $b$ đã thăm, rồi đi đến cha của chúng là `par[a]` và `par[b]` và đánh dấu; tiếp tục đi lên các cha như vậy cho tới khi gặp một đỉnh đã được đánh dấu.
    Đỉnh này là LCA cần tìm; ta có thể tìm các đỉnh trên chu trình bằng cách duyệt lại đường từ $a$ và $b$ đến LCA.
  
    Rõ ràng độ phức tạp của thuật toán này tỉ lệ với độ dài chu trình cần tìm.
  
  * Co chu trình hình thành khi thêm cạnh $(a, b)$ trong một cây.
  
    Ta cần tạo một thành phần liên thông 2 cạnh mới gồm tất cả các đỉnh của chu trình đã tìm thấy (bản thân chu trình cũng có thể gồm một số thành phần liên thông 2 cạnh, nhưng điều đó không thay đổi gì).
    Ngoài ra, cần co chúng sao cho cấu trúc cây không bị phá vỡ, tất cả các con trỏ `par[]` và cả hai DSU vẫn đúng.
  
    Cách dễ nhất là co tất cả các đỉnh trên chu trình về LCA của chúng.
    LCA là đỉnh cao nhất trong số đó, tức con trỏ cha `par[]` của nó không đổi.
    Với các đỉnh khác trên chu trình, không cần cập nhật cha vì những đỉnh này không còn tồn tại.
    Nhưng trong DSU của các thành phần liên thông 2 cạnh, tất cả các đỉnh này sẽ trỏ đến LCA.
  
    Ta sẽ cài đặt DSU cho các thành phần liên thông 2 cạnh mà không tối ưu hợp theo hạng, vì thế độ phức tạp trung bình mỗi truy vấn là $O(\log n)$.
    Để đạt độ phức tạp trung bình $O(1)$ mỗi truy vấn, ta cần hợp các đỉnh trên chu trình theo hạng, rồi gán `par[]` tương ứng.

## Cài đặt

Dưới đây là cài đặt hoàn chỉnh của thuật toán.

Như đã nói, để đơn giản, DSU của các thành phần liên thông 2 cạnh được viết không dùng hợp theo hạng, nên độ phức tạp thu được trung bình là $O(\log n)$.

Ngoài ra, cài đặt này không lưu bản thân các cạnh cầu, mà chỉ lưu số lượng của chúng trong `bridges`.
Tuy vậy, không khó để tạo một `set` chứa tất cả các cạnh cầu.

Ban đầu gọi hàm `init()` để khởi tạo hai DSU (tạo một tập riêng cho mỗi đỉnh và đặt kích thước bằng một) và đặt các cha `par`.

Hàm chính là `add_edge(a, b)`, xử lý và thêm một cạnh mới.

```cpp
vector<int> par, dsu_2ecc, dsu_cc, dsu_cc_size;
int bridges;
int lca_iteration;
vector<int> last_visit;
 
void init(int n) {
    par.resize(n);
    dsu_2ecc.resize(n);
    dsu_cc.resize(n);
    dsu_cc_size.resize(n);
    lca_iteration = 0;
    last_visit.assign(n, 0);
    for (int i=0; i<n; ++i) {
        dsu_2ecc[i] = i;
        dsu_cc[i] = i;
        dsu_cc_size[i] = 1;
        par[i] = -1;
    }
    bridges = 0;
}
 
int find_2ecc(int v) {
    if (v == -1)
        return -1;
    return dsu_2ecc[v] == v ? v : dsu_2ecc[v] = find_2ecc(dsu_2ecc[v]);
}
 
int find_cc(int v) {
    v = find_2ecc(v);
    return dsu_cc[v] == v ? v : dsu_cc[v] = find_cc(dsu_cc[v]);
}
 
void make_root(int v) {
    int root = v;
    int child = -1;
    while (v != -1) {
        int p = find_2ecc(par[v]);
        par[v] = child;
        dsu_cc[v] = root;
        child = v;
        v = p;
    }
    dsu_cc_size[root] = dsu_cc_size[child];
}

void merge_path (int a, int b) {
    ++lca_iteration;
    vector<int> path_a, path_b;
    int lca = -1;
    while (lca == -1) {
        if (a != -1) {
            a = find_2ecc(a);
            path_a.push_back(a);
            if (last_visit[a] == lca_iteration){
                lca = a;
                break;
                }
            last_visit[a] = lca_iteration;
            a = par[a];
        }
        if (b != -1) {
            b = find_2ecc(b);
            path_b.push_back(b);
            if (last_visit[b] == lca_iteration){
                lca = b;
                break;
                }
            last_visit[b] = lca_iteration;
            b = par[b];
        }
        
    }

    for (int v : path_a) {
        dsu_2ecc[v] = lca;
        if (v == lca)
            break;
        --bridges;
    }
    for (int v : path_b) {
        dsu_2ecc[v] = lca;
        if (v == lca)
            break;
        --bridges;
    }
}
 
void add_edge(int a, int b) {
    a = find_2ecc(a);
    b = find_2ecc(b);
    if (a == b)
        return;
 
    int ca = find_cc(a);
    int cb = find_cc(b);

    if (ca != cb) {
        ++bridges;
        if (dsu_cc_size[ca] > dsu_cc_size[cb]) {
            swap(a, b);
            swap(ca, cb);
        }
        make_root(a);
        par[a] = dsu_cc[a] = b;
        dsu_cc_size[cb] += dsu_cc_size[a];
    } else {
        merge_path(a, b);
    }
}
```

DSU cho các thành phần liên thông 2 cạnh được lưu trong vector `dsu_2ecc`, và hàm trả về phần tử đại diện là `find_2ecc(v)`.
Hàm này được dùng nhiều lần trong phần còn lại của mã vì sau khi co nhiều đỉnh thành một, các đỉnh đó không còn tồn tại; thay vào đó, chỉ phần tử đại diện mới có cha `par` đúng trong rừng các thành phần liên thông 2 cạnh.

DSU cho các thành phần liên thông được lưu trong vector `dsu_cc`; ngoài ra vector `dsu_cc_size` lưu kích thước các thành phần.
Hàm `find_cc(v)` trả về phần tử đại diện của thành phần liên thông (thực ra là gốc của cây).

Phép đổi gốc cây `make_root(v)` hoạt động như đã mô tả:
nó đi từ đỉnh $v$ qua các đỉnh cha lên đến gốc, mỗi lần đảo chiều con trỏ cha `par`.
Liên kết đến phần tử đại diện của thành phần liên thông `dsu_cc` cũng được cập nhật để trỏ tới đỉnh gốc mới.
Sau khi đổi gốc, ta phải gán cho gốc mới kích thước đúng của thành phần liên thông.
Ta cũng phải chú ý gọi `find_2ecc()` để lấy phần tử đại diện của thành phần liên thông 2 cạnh, thay vì một đỉnh khác đã bị co.

Hàm tìm và co chu trình `merge_path(a, b)` cũng được cài đặt như trên.
Nó tìm LCA của $a$ và $b$ bằng cách đồng thời đi lên từ hai đỉnh này cho tới khi gặp một đỉnh lần thứ hai.
Để hiệu quả, ta chọn một mã định danh duy nhất cho mỗi lần tìm LCA và dùng mã đó đánh dấu các đỉnh đã đi qua.
Việc này chạy trong $O(1)$, trong khi các cách khác như dùng $set$ kém hiệu quả hơn.
Các đường đã đi được lưu trong vector `path_a` và `path_b`; ta dùng chúng để duyệt lại đến LCA, từ đó thu được tất cả các đỉnh trên chu trình.
Mọi đỉnh của chu trình được co bằng cách gắn vào LCA, do đó độ phức tạp trung bình là $O(\log n)$ (vì ta không dùng hợp theo hạng).
Tất cả các cạnh đi qua đều từng là cầu, nên ta trừ 1 cho mỗi cạnh trên chu trình.

Cuối cùng hàm truy vấn `add_edge(a, b)` xác định các thành phần liên thông chứa các đỉnh $a$ và $b$.
Nếu chúng thuộc các thành phần liên thông khác nhau, cây nhỏ hơn được đổi gốc và gắn vào cây lớn hơn.
Nếu $a$ và $b$ thuộc cùng một cây nhưng khác thành phần liên thông 2 cạnh, hàm `merge_path(a, b)` được gọi để tìm chu trình và co nó thành một thành phần liên thông 2 cạnh.
