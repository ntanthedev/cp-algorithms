---
tags:
  - Translated
e_maxx_link: treap
translation:
  source: data_structures/treap.md
  source_commit: feccb477db1b297864acde90c74639f8b68a51c2
  status: draft
  last_synced: 2026-08-08
---

# Treap (cây Cartesian)

Treap là một cấu trúc dữ liệu kết hợp cây nhị phân và heap nhị phân (vì thế có tên: tree + heap $\Rightarrow$ Treap).

Cụ thể hơn, Treap là cấu trúc dữ liệu lưu các cặp $(X, Y)$ trong một cây nhị phân sao cho cây là cây tìm kiếm nhị phân theo $X$ và là heap theo $Y$.
Nếu một nút của cây chứa các giá trị $(X_0, Y_0)$, mọi nút trong cây con trái có $X \leq X_0$, mọi nút trong cây con phải có $X_0 \leq X$, và mọi nút trong cả cây con trái lẫn cây con phải đều có $Y \leq Y_0$.

Treap cũng thường được gọi là "cây Cartesian", vì ta có thể dễ dàng biểu diễn nó trên mặt phẳng Cartesian:

<center>
<img src="https://upload.wikimedia.org/wikipedia/commons/e/e4/Treap.svg" width="350px"/>
</center>

Treap được Raimund Siedel và Cecilia Aragon đề xuất vào năm 1989.

## Ưu điểm của cách tổ chức dữ liệu này

Trong cách cài đặt này, các giá trị $X$ là **khóa** (đồng thời cũng là các giá trị được lưu trong Treap), còn các giá trị $Y$ được gọi là **độ ưu tiên**. Nếu không có độ ưu tiên, Treap chỉ là một cây tìm kiếm nhị phân thông thường theo $X$; với cùng một tập giá trị $X$ có thể có rất nhiều cây khác nhau, trong đó có những cây bị suy biến (chẳng hạn có dạng danh sách liên kết), và vì thế rất chậm (các thao tác chính sẽ có độ phức tạp $O(N)$).

Trong khi đó, **độ ưu tiên** (khi chúng đôi một khác nhau) cho phép xác định **duy nhất** cây sẽ được dựng (dĩ nhiên cây không phụ thuộc vào thứ tự thêm các giá trị), điều này có thể chứng minh bằng một định lý tương ứng. Rõ ràng, nếu ta **chọn độ ưu tiên ngẫu nhiên**, trung bình ta sẽ thu được các cây không suy biến, từ đó bảo đảm độ phức tạp $O(\log N)$ cho các thao tác chính. Vì vậy, cấu trúc dữ liệu này còn có tên khác là **cây tìm kiếm nhị phân ngẫu nhiên hóa**.

## Các thao tác

Treap hỗ trợ các thao tác sau:

- **Insert (X,Y)** trong $O(\log N)$.  
  Thêm một nút mới vào cây. Một biến thể là chỉ truyền $X$ và sinh ngẫu nhiên $Y$ ngay trong thao tác.
- **Search (X)** trong $O(\log N)$.  
  Tìm nút có giá trị khóa $X$ cho trước. Cách cài đặt giống cây tìm kiếm nhị phân thông thường.
- **Erase (X)** trong $O(\log N)$.  
  Tìm nút có giá trị khóa $X$ cho trước và xóa nó khỏi cây.
- **Build ($X_1$, ..., $X_N$)** trong $O(N)$.  
  Dựng cây từ một danh sách giá trị. Có thể thực hiện trong thời gian tuyến tính (giả sử $X_1, ..., X_N$ đã được sắp xếp).
- **Union ($T_1$, $T_2$)** trong $O(M \log (N/M))$.  
  Hợp nhất hai cây, giả sử mọi phần tử đều khác nhau. Ta vẫn có thể đạt cùng độ phức tạp nếu cần loại bỏ các phần tử trùng trong quá trình hợp nhất.
- **Intersect ($T_1$, $T_2$)** trong $O(M \log (N/M))$.  
  Tìm giao của hai cây (tức các phần tử chung của chúng). Bài viết này không xét phần cài đặt thao tác đó.

Ngoài ra, do Treap là một cây tìm kiếm nhị phân, nó còn có thể hỗ trợ những thao tác khác, chẳng hạn tìm phần tử lớn thứ $K$ hoặc tìm chỉ số của một phần tử.

## Mô tả cài đặt

Về mặt cài đặt, mỗi nút chứa $X$, $Y$ và các con trỏ tới nút con trái ($L$) và nút con phải ($R$).

Ta sẽ cài đặt tất cả các thao tác cần thiết chỉ bằng hai thao tác phụ trợ: Split và Merge.

### Tách (Split)

<center>
<img src="https://upload.wikimedia.org/wikipedia/commons/6/69/Treap_split.svg" width="450px"/>
</center>

**Split ($T$, $X$)** tách cây $T$ thành 2 cây con $L$ và $R$ (là các giá trị trả về của split), sao cho $L$ chứa mọi phần tử có khóa $X_L \le X$, còn $R$ chứa mọi phần tử có khóa $X_R > X$. Thao tác này có độ phức tạp $O (\log N)$ và được cài đặt bằng một phép đệ quy gọn:

1. Nếu giá trị của nút gốc (R) là $\le X$, thì `L` ít nhất sẽ gồm `R->L` và `R`. Sau đó ta gọi split trên `R->R`, ký hiệu kết quả tách là `L'` và `R'`. Cuối cùng, `L` sẽ chứa thêm `L'`, còn `R = R'`.
2. Nếu giá trị của nút gốc (R) là $> X$, thì `R` ít nhất sẽ gồm `R` và `R->R`. Sau đó ta gọi split trên `R->L`, ký hiệu kết quả tách là `L'` và `R'`. Cuối cùng, `L=L'`, còn `R` sẽ chứa thêm `R'`.

Do đó, thuật toán split là:

1. quyết định nút gốc sẽ thuộc cây con nào (trái hay phải)
2. gọi đệ quy split trên một trong hai nút con
3. dựng kết quả cuối cùng bằng cách tái sử dụng kết quả của lời gọi split đệ quy.

### Hợp nhất (Merge)

<center>
<img src="https://upload.wikimedia.org/wikipedia/commons/a/a8/Treap_merge.svg" width="500px"/>
</center>

**Merge ($T_1$, $T_2$)** kết hợp hai cây con $T_1$ và $T_2$ rồi trả về cây mới. Thao tác này cũng có độ phức tạp $O (\log N)$. Nó giả sử $T_1$ và $T_2$ đã có thứ tự phù hợp (mọi khóa $X$ trong $T_1$ đều nhỏ hơn các khóa trong $T_2$). Vì vậy, ta cần kết hợp hai cây mà không phá vỡ thứ tự độ ưu tiên $Y$. Để làm điều đó, ta chọn làm gốc cây có nút gốc mang độ ưu tiên $Y$ lớn hơn, rồi gọi Merge đệ quy cho cây còn lại với cây con tương ứng của nút gốc đã chọn.

### Chèn (Insert)

<center>
<img src="https://upload.wikimedia.org/wikipedia/commons/3/35/Treap_insert.svg" width="500px"/>
</center>

Bây giờ cách cài đặt **Insert ($X$, $Y$)** trở nên khá rõ ràng. Trước hết ta đi xuống cây (như trong cây tìm kiếm nhị phân thông thường theo X), và dừng tại nút đầu tiên có giá trị độ ưu tiên nhỏ hơn $Y$. Ta đã tìm được vị trí để chèn phần tử mới. Tiếp theo, ta gọi **Split (T, X)** trên cây con bắt đầu tại nút vừa tìm được, rồi dùng hai cây con $L$ và $R$ được trả về làm con trái và con phải của nút mới.

Một cách khác là chèn bằng cách tách Treap ban đầu theo $X$, rồi thực hiện $2$ lần merge với nút mới (xem hình).


### Xóa (Erase)

<center>
<img src="https://upload.wikimedia.org/wikipedia/commons/6/62/Treap_erase.svg" width="500px"/>
</center>

Cách cài đặt **Erase ($X$)** cũng khá rõ ràng. Trước hết ta đi xuống cây (như trong cây tìm kiếm nhị phân thông thường theo $X$) để tìm phần tử cần xóa. Khi tìm thấy nút đó, ta gọi **Merge** trên hai cây con của nó và đặt giá trị trả về vào vị trí của phần tử đang bị xóa.

Một cách khác là tách riêng cây con chứa $X$ bằng $2$ thao tác split rồi hợp nhất các Treap còn lại (xem hình).

### Dựng cây (Build)

Ta cài đặt thao tác **Build** với độ phức tạp $O (N \log N)$ bằng $N$ lần gọi **Insert**.

### Hợp (Union)

**Union ($T_1$, $T_2$)** có độ phức tạp lý thuyết $O (M \log (N / M))$, nhưng trên thực tế chạy rất tốt, có lẽ với một hằng số ẩn rất nhỏ. Không mất tính tổng quát, giả sử $T_1 \rightarrow Y > T_2 \rightarrow Y$, tức gốc của $T_1$ sẽ là gốc của kết quả. Để thu được kết quả, ta cần kết hợp các cây $T_1 \rightarrow L$, $T_1 \rightarrow R$ và $T_2$ thành hai cây có thể làm con của gốc $T_1$. Ta gọi Split ($T_2$, $T_1\rightarrow X$), qua đó tách $T_2$ thành hai phần L và R; sau đó lần lượt kết hợp đệ quy chúng với các con của $T_1$: Union ($T_1 \rightarrow L$, $L$) và Union ($T_1 \rightarrow R$, $R$), từ đó thu được cây con trái và cây con phải của kết quả.

## Cài đặt

```cpp
struct item {
	int key, prior;
	item *l, *r;
	item () { }
	item (int key) : key(key), prior(rand()), l(NULL), r(NULL) { }
	item (int key, int prior) : key(key), prior(prior), l(NULL), r(NULL) { }
};
typedef item* pitem;
```

Đây là định nghĩa nút của chúng ta. Lưu ý có hai con trỏ tới nút con, một khóa kiểu số nguyên (cho BST) và một độ ưu tiên kiểu số nguyên (cho heap). Độ ưu tiên được gán bằng một bộ sinh số ngẫu nhiên.

```cpp
void split (pitem t, int key, pitem & l, pitem & r) {
	if (!t)
		l = r = NULL;
	else if (t->key <= key)
        split (t->r, key, t->r, r),  l = t;
	else
        split (t->l, key, l, t->l),  r = t;
}
```

`t` là Treap cần tách, còn `key` là giá trị BST dùng làm mốc tách. Lưu ý rằng ta không `return` các giá trị kết quả ở đâu cả; thay vào đó, ta chỉ sử dụng chúng như sau:

```cpp
pitem l = nullptr, r = nullptr;
split(t, 5, l, r);
if (l) cout << "Left subtree size: " << (l->size) << endl;
if (r) cout << "Right subtree size: " << (r->size) << endl;
```

Ghi chú bản dịch: Đoạn ví dụ trên truy cập trường size, nhưng cấu trúc item được khai báo ngay trước đó chưa định nghĩa trường này. Đây là lỗi của mã nguồn tiếng Anh hiện tại; bản dịch giữ nguyên code để đồng bộ với nguồn.

Hàm `split` này có thể khá khó hiểu vì nó vừa có con trỏ (`pitem`), vừa có tham chiếu tới các con trỏ đó (`pitem &l`). Ta hãy diễn giải bằng lời ý nghĩa của lời gọi `split(t, k, l, r)`: "tách Treap `t` theo giá trị `k` thành hai Treap, rồi lưu Treap bên trái vào `l` và Treap bên phải vào `r`". Tốt! Bây giờ, hãy áp dụng định nghĩa này cho hai lời gọi đệ quy theo các trường hợp đã phân tích ở phần trước: (Điều kiện if đầu tiên chỉ là trường hợp cơ sở đơn giản khi Treap rỗng)

1. Khi giá trị nút gốc là $\le$ key, ta gọi `split (t->r, key, t->r, r)`, nghĩa là: "tách Treap `t->r` (cây con phải của `t`) theo giá trị `key`, lưu cây con trái vào `t->r` và cây con phải vào `r`". Sau đó ta đặt `l = t`. Lúc này giá trị kết quả `l` đã chứa `t->l`, `t` và cả `t->r` (là kết quả từ lời gọi đệ quy vừa thực hiện), tất cả đã được hợp nhất theo đúng thứ tự! Bạn nên dừng lại một chút để chắc chắn rằng kết quả `l` và `r` đúng với phần Mô tả cài đặt ở trên.
2. Khi giá trị nút gốc lớn hơn key, ta gọi `split (t->l, key, l, t->l)`, nghĩa là: "tách Treap `t->l` (cây con trái của `t`) theo giá trị `key`, lưu cây con trái vào `l` và cây con phải vào `t->l`". Sau đó ta đặt `r = t`. Lúc này giá trị kết quả `r` đã chứa `t->l` (là kết quả từ lời gọi đệ quy vừa thực hiện), `t` và `t->r`, tất cả đã được hợp nhất theo đúng thứ tự! Bạn nên dừng lại một chút để chắc chắn rằng kết quả `l` và `r` đúng với phần Mô tả cài đặt ở trên.

Nếu vẫn thấy khó hiểu phần cài đặt, bạn nên nhìn nó theo hướng _quy nạp_, nghĩa là: *đừng* cố bung các lời gọi đệ quy lặp đi lặp lại. Hãy giả sử cài đặt split hoạt động đúng với Treap rỗng, rồi thử chạy với Treap một nút, sau đó hai nút, và cứ thế tiếp tục; ở mỗi bước, tái sử dụng hiểu biết rằng split đã đúng trên các Treap nhỏ hơn.

```cpp
void insert (pitem & t, pitem it) {
	if (!t)
		t = it;
	else if (it->prior > t->prior)
		split (t, it->key, it->l, it->r),  t = it;
	else
		insert (t->key <= it->key ? t->r : t->l, it);
}

void merge (pitem & t, pitem l, pitem r) {
	if (!l || !r)
		t = l ? l : r;
	else if (l->prior > r->prior)
		merge (l->r, l->r, r),  t = l;
	else
		merge (r->l, l, r->l),  t = r;
}

void erase (pitem & t, int key) {
	if (t->key == key) {
		pitem th = t;
		merge (t, t->l, t->r);
		delete th;
	}
	else
		erase (key < t->key ? t->l : t->r, key);
}

pitem unite (pitem l, pitem r) {
	if (!l || !r)  return l ? l : r;
	if (l->prior < r->prior)  swap (l, r);
	pitem lt, rt;
	split (r, l->key, lt, rt);
	l->l = unite (l->l, lt);
	l->r = unite (l->r, rt);
	return l;
}
```

## Duy trì kích thước cây con

Để mở rộng chức năng của Treap, ta thường cần lưu số nút trong cây con của mỗi nút — trường `int cnt` trong cấu trúc `item`. Chẳng hạn, có thể dùng nó để tìm phần tử lớn thứ K của cây trong $O (\log N)$, hoặc tìm chỉ số của phần tử trong danh sách đã sắp xếp với cùng độ phức tạp. Cách cài đặt các thao tác này giống như với cây tìm kiếm nhị phân thông thường.

Khi cây thay đổi (thêm hoặc xóa nút, v.v.), `cnt` của một số nút phải được cập nhật tương ứng. Ta sẽ tạo hai hàm: `cnt()` trả về giá trị `cnt` hiện tại, hoặc 0 nếu nút không tồn tại; `upd_cnt()` cập nhật giá trị `cnt` cho nút này, giả sử các giá trị `cnt` của hai nút con L và R đã được cập nhật. Rõ ràng chỉ cần thêm các lời gọi `upd_cnt()` vào cuối `insert`, `erase`, `split` và `merge` để giữ các giá trị `cnt` luôn đúng.

```cpp
int cnt (pitem t) {
	return t ? t->cnt : 0;
}

void upd_cnt (pitem t) {
	if (t)
		t->cnt = 1 + cnt(t->l) + cnt (t->r);
}
```

## Dựng Treap trong $O (N)$ ở chế độ offline {data-toc-label="Building a Treap in O(N) in offline mode"}

Với một danh sách khóa đã sắp xếp, ta có thể dựng Treap nhanh hơn so với chèn từng khóa một — cách đó mất $O(N \log N)$. Do các khóa đã được sắp xếp, ta có thể dễ dàng dựng một cây tìm kiếm nhị phân cân bằng trong thời gian tuyến tính. Các giá trị heap $Y$ được khởi tạo ngẫu nhiên, sau đó có thể heapify độc lập với các khóa $X$ để [dựng heap](https://en.wikipedia.org/wiki/Binary_heap#Building_a_heap) trong $O(N)$.

```cpp
void heapify (pitem t) {
	if (!t) return;
	pitem max = t;
	if (t->l != NULL && t->l->prior > max->prior)
		max = t->l;
	if (t->r != NULL && t->r->prior > max->prior)
		max = t->r;
	if (max != t) {
		swap (t->prior, max->prior);
		heapify (max);
	}
}

pitem build (int * a, int n) {
	// Construct a treap on values {a[0], a[1], ..., a[n - 1]}
	if (n == 0) return NULL;
	int mid = n / 2;
	pitem t = new item (a[mid], rand ());
	t->l = build (a, mid);
	t->r = build (a + mid + 1, n - mid - 1);
	heapify (t);
	upd_cnt(t)
	return t;
}
```

Ghi chú bản dịch: Trong mã nguồn hiện tại, dòng gọi upd_cnt(t) ở đoạn trên thiếu dấu chấm phẩy, vì vậy snippet sẽ không biên dịch nguyên trạng. Bản dịch không sửa code nguồn.

Lưu ý: lời gọi `upd_cnt(t)` chỉ cần thiết nếu bạn cần kích thước cây con.

Cách tiếp cận trên luôn tạo ra một cây cân bằng hoàn hảo, nhìn chung tốt trong thực tế, nhưng đổi lại nó không giữ nguyên các độ ưu tiên đã được gán ban đầu cho mỗi nút. Vì vậy, cách này không phù hợp để giải bài toán sau:

!!! example "[acmsguru - Cartesian Tree](https://codeforces.com/problemsets/acmsguru/problem/99999/155)"
    Cho một dãy các cặp $(x_i, y_i)$, hãy dựng cây Cartesian từ chúng. Mọi $x_i$ và mọi $y_i$ đều đôi một khác nhau.

Lưu ý rằng trong bài toán này các độ ưu tiên không ngẫu nhiên, vì thế việc chỉ chèn từng đỉnh một có thể dẫn tới lời giải bậc hai.

Một lời giải khả dĩ là, với mỗi phần tử, tìm phần tử gần nhất bên trái và bên phải có độ ưu tiên nhỏ hơn độ ưu tiên của phần tử đó. Trong hai phần tử này, phần tử có độ ưu tiên lớn hơn phải là cha của phần tử hiện tại.

Bài toán này có thể giải bằng một biến thể của [ngăn xếp cực tiểu](./stack_queue_modification.md) trong thời gian tuyến tính:

```cpp
void connect(auto from, auto to) {
    vector<pitem> st;
    for(auto it: ranges::subrange(from, to)) {
        while(!st.empty() && st.back()->prior > it->prior) {
            st.pop_back();
        }
        if(!st.empty()) {
            if(!it->p || it->p->prior < st.back()->prior) {
                it->p = st.back();
            }
        }
        st.push_back(it);
    }
}

pitem build(int *x, int *y, int n) {
    vector<pitem> nodes(n);
    for(int i = 0; i < n; i++) {
        nodes[i] = new item(x[i], y[i]);
    }
    connect(nodes.begin(), nodes.end());
    connect(nodes.rbegin(), nodes.rend());
    for(int i = 0; i < n; i++) {
        if(nodes[i]->p) {
            if(nodes[i]->p->key < nodes[i]->key) {
                nodes[i]->p->r = nodes[i];
            } else {
                nodes[i]->p->l = nodes[i];
            }
        }
    }
    return nodes[min_element(y, y + n) - y];
}
```

Ghi chú bản dịch: Đoạn cài đặt tuyến tính này dùng trường p làm con trỏ cha, nhưng cấu trúc item đã khai báo trước đó không có trường p. Ngoài ra, đoạn này dùng quy ước heap cực tiểu theo độ ưu tiên, khác với quy ước heap cực đại ở phần Treap thông thường phía trên. Bản dịch giữ nguyên code và đang xử lý correction riêng cho nguồn tiếng Anh.

## Implicit Treap

Implicit Treap là một biến thể đơn giản nhưng rất mạnh của Treap thông thường. Trên thực tế, có thể xem Implicit Treap như một mảng hỗ trợ các thao tác sau (tất cả đều trong $O (\log N)$ ở chế độ online):

- Chèn một phần tử vào vị trí bất kỳ trong mảng
- Xóa một phần tử bất kỳ
- Tìm tổng, phần tử nhỏ nhất / lớn nhất, v.v. trên một đoạn bất kỳ
- Cộng, tô (gán) trên một đoạn bất kỳ
- Đảo ngược các phần tử trên một đoạn bất kỳ

Ý tưởng là các khóa phải là **chỉ số** bắt đầu từ 0 của các phần tử trong mảng. Tuy nhiên, ta sẽ không lưu các giá trị này một cách tường minh (nếu không, chẳng hạn việc chèn một phần tử sẽ khiến khóa của $O (N)$ nút trong cây phải thay đổi).

Lưu ý rằng khóa của một nút là số nút nhỏ hơn nó (các nút như vậy có thể không chỉ nằm trong cây con trái của nó mà còn trong các cây con trái của các tổ tiên).
Cụ thể hơn, **khóa ẩn** của một nút T là số đỉnh $cnt (T \rightarrow L)$ trong cây con trái của nút này, cộng với các giá trị tương tự $cnt (P \rightarrow L) + 1$ đối với mỗi tổ tiên P của nút T nếu T nằm trong cây con phải của P.

Bây giờ ta có thể thấy cách tính nhanh khóa ẩn của nút hiện tại. Do trong mọi thao tác ta đều đi tới một nút bằng cách đi xuống cây, ta chỉ cần tích lũy tổng này và truyền nó vào hàm. Nếu đi sang cây con trái, tổng tích lũy không đổi; nếu đi sang cây con phải, nó tăng thêm $cnt (T \rightarrow L) +1$.

Dưới đây là cài đặt mới của **Split** và **Merge**:

```cpp
void merge (pitem & t, pitem l, pitem r) {
	if (!l || !r)
		t = l ? l : r;
	else if (l->prior > r->prior)
		merge (l->r, l->r, r),  t = l;
	else
		merge (r->l, l, r->l),  t = r;
	upd_cnt (t);
}

void split (pitem t, pitem & l, pitem & r, int key, int add = 0) {
	if (!t)
		return void( l = r = 0 );
	int cur_key = add + cnt(t->l); //implicit key
	if (key <= cur_key)
		split (t->l, l, t->l, key, add),  r = t;
	else
		split (t->r, t->r, r, key, add + 1 + cnt(t->l)),  l = t;
	upd_cnt (t);
}
```

Trong cài đặt trên, sau lời gọi $split(T, T_1, T_2, k)$, cây $T_1$ sẽ gồm $k$ phần tử đầu tiên của $T$ (tức các phần tử có khóa ẩn nhỏ hơn $k$), còn $T_2$ sẽ gồm tất cả các phần tử còn lại.

Bây giờ hãy xét cách cài đặt các thao tác khác nhau trên Implicit Treap:

- **Chèn phần tử**.  
  Giả sử ta cần chèn một phần tử vào vị trí $pos$. Ta chia Treap thành hai phần tương ứng với các mảng $[0..pos-1]$ và $[pos..sz]$; để làm vậy, gọi $split(T, T_1, T_2, pos)$. Sau đó ta có thể kết hợp cây $T_1$ với nút mới bằng lời gọi $merge(T_1, T_1, \text{new item})$ (dễ thấy mọi điều kiện tiên quyết đều được thỏa). Cuối cùng, ta kết hợp hai cây $T_1$ và $T_2$ trở lại thành $T$ bằng lời gọi $merge(T, T_1, T_2)$.
- **Xóa phần tử**.  
 Thao tác này còn đơn giản hơn: tìm phần tử cần xóa $T$, thực hiện merge hai cây con $L$ và $R$ của nó, rồi thay phần tử $T$ bằng kết quả của merge. Thực ra, xóa phần tử trong Implicit Treap giống hệt trong Treap thông thường.
- Tìm **tổng / giá trị nhỏ nhất**, v.v. trên đoạn.  
 Trước hết, tạo thêm trường $F$ trong cấu trúc `item` để lưu giá trị của hàm mục tiêu cho cây con của nút này. Trường này có thể được duy trì tương tự như kích thước cây con: tạo một hàm tính giá trị này cho một nút dựa trên các giá trị ở hai nút con rồi thêm lời gọi hàm đó vào cuối mọi hàm làm thay đổi cây.  
 Thứ hai, ta cần biết cách xử lý truy vấn trên một đoạn bất kỳ $[A; B]$.  
 Để lấy phần cây tương ứng với đoạn $[A; B]$, ta cần gọi $split(T, T_2, T_3, B+1)$, sau đó $split(T_2, T_1, T_2, A)$: sau hai thao tác này, $T_2$ sẽ gồm toàn bộ và chỉ những phần tử trong đoạn $[A; B]$. Vì vậy, đáp án truy vấn được lưu trong trường $F$ của gốc $T_2$. Sau khi trả lời truy vấn, phải khôi phục cây bằng cách gọi $merge(T, T_1, T_2)$ và $merge(T, T, T_3)$.
- **Cộng / tô (gán)** trên đoạn.  
 Ta làm tương tự đoạn trước, nhưng thay vì trường F, ta lưu một trường `add` chứa giá trị cần cộng cho cây con (hoặc giá trị mà cây con sẽ được tô thành). Trước khi thực hiện bất kỳ thao tác nào, ta phải "push" giá trị này xuống đúng cách — tức thay đổi $T \rightarrow L \rightarrow add$ và $T \rightarrow R \rightarrow add$, rồi xóa `add` ở nút cha. Nhờ vậy, thông tin sẽ không bị mất sau các thay đổi trên cây.
- **Đảo ngược** trên đoạn.  
 Thao tác này lại tương tự thao tác trước: ta cần thêm cờ Boolean `rev` và đặt nó thành true khi cây con của nút hiện tại phải bị đảo ngược. Việc "push" giá trị này phức tạp hơn một chút — ta đổi chỗ hai nút con của nút này và đặt cờ tương ứng thành true cho chúng.

Dưới đây là một cài đặt mẫu của Implicit Treap hỗ trợ đảo ngược một đoạn. Với mỗi nút, ta lưu trường `value`, là giá trị thực tế của phần tử mảng tại vị trí hiện tại. Ta cũng cung cấp cài đặt hàm `output()`, hàm này xuất ra mảng tương ứng với trạng thái hiện tại của Implicit Treap.

```cpp
typedef struct item * pitem;
struct item {
	int prior, value, cnt;
	bool rev;
	pitem l, r;
};

int cnt (pitem it) {
	return it ? it->cnt : 0;
}

void upd_cnt (pitem it) {
	if (it)
		it->cnt = cnt(it->l) + cnt(it->r) + 1;
}

void push (pitem it) {
	if (it && it->rev) {
		it->rev = false;
		swap (it->l, it->r);
		if (it->l)  it->l->rev ^= true;
		if (it->r)  it->r->rev ^= true;
	}
}

void merge (pitem & t, pitem l, pitem r) {
	push (l);
	push (r);
	if (!l || !r)
		t = l ? l : r;
	else if (l->prior > r->prior)
		merge (l->r, l->r, r),  t = l;
	else
		merge (r->l, l, r->l),  t = r;
	upd_cnt (t);
}

void split (pitem t, pitem & l, pitem & r, int key, int add = 0) {
	if (!t)
		return void( l = r = 0 );
	push (t);
	int cur_key = add + cnt(t->l);
	if (key <= cur_key)
		split (t->l, l, t->l, key, add),  r = t;
	else
		split (t->r, t->r, r, key, add + 1 + cnt(t->l)),  l = t;
	upd_cnt (t);
}

void reverse (pitem t, int l, int r) {
	pitem t1, t2, t3;
	split (t, t1, t2, l);
	split (t2, t2, t3, r-l+1);
	t2->rev ^= true;
	merge (t, t1, t2);
	merge (t, t, t3);
}

void output (pitem t) {
	if (!t)  return;
	push (t);
	output (t->l);
	printf ("%d ", t->value);
	output (t->r);
}
```

## Tài liệu tham khảo

* [Blelloch, Reid-Miller "Fast Set Operations Using Treaps"](https://www.cs.cmu.edu/~scandal/papers/treaps-spaa98.pdf)

## Bài tập luyện tập

* [SPOJ - Ada and Aphids](http://www.spoj.com/problems/ADAAPHID/)
* [SPOJ - Ada and Harvest](http://www.spoj.com/problems/ADACROP/)
* [Codeforces - Radio Stations](http://codeforces.com/contest/762/problem/E)
* [SPOJ - Ghost Town](http://www.spoj.com/problems/COUNT1IT/)
* [SPOJ - Arrangement Validity](http://www.spoj.com/problems/IITWPC4D/)
* [SPOJ - All in One](http://www.spoj.com/problems/ALLIN1/)
* [Codeforces - Dog Show](http://codeforces.com/contest/847/problem/D)
* [Codeforces - Yet Another Array Queries Problem](http://codeforces.com/contest/863/problem/D)
* [SPOJ - Mean of Array](http://www.spoj.com/problems/MEANARR/)
* [SPOJ - TWIST](http://www.spoj.com/problems/TWIST/)
* [SPOJ - KOILINE](http://www.spoj.com/problems/KOILINE/)
* [CodeChef - The Prestige](https://www.codechef.com/problems/PRESTIGE)
* [Codeforces - T-Shirts](https://codeforces.com/contest/702/problem/F)
* [Codeforces - Wizards and Roads](https://codeforces.com/problemset/problem/167/D)
* [Codeforces - Yaroslav and Points](https://codeforces.com/contest/295/problem/E)