---
tags:
  - Original
translation:
  source: data_structures/sqrt-tree.md
  source_commit: 19e8bc6e47580982088563f89832fb0b2d8a5526
  status: draft
  last_synced: 2026-11-17
---

# Sqrt Tree

Cho một mảng $a$ chứa $n$ phần tử và phép toán $\circ$ có tính kết hợp: $(x \circ y) \circ z = x \circ (y \circ z)$ đúng với mọi $x$, $y$, $z$.

Các phép toán như $\gcd$, $\min$, $\max$, $+$, $\text{and}$, $\text{or}$, $\text{xor}$, v.v. thỏa mãn các điều kiện này.

Ta còn có các truy vấn $q(l, r)$. Với mỗi truy vấn, ta cần tính $a_l \circ a_{l+1} \circ \dots \circ a_r$.

Sqrt Tree xử lý mỗi truy vấn như vậy trong $O(1)$, với thời gian tiền xử lý $O(n \cdot \log \log n)$ và bộ nhớ $O(n \cdot \log \log n)$.

## Mô tả

### Xây dựng phép chia căn

Hãy thực hiện [chia căn](sqrt_decomposition.md). Ta chia mảng thành $\sqrt{n}$ khối, mỗi khối có kích thước $\sqrt{n}$. Với mỗi khối, ta tính:

1. Đáp án cho các truy vấn nằm trong khối và bắt đầu từ đầu khối ($\text{prefixOp}$)
2. Đáp án cho các truy vấn nằm trong khối và kết thúc ở cuối khối ($\text{suffixOp}$)

Ta cũng tính thêm một mảng:

3. $\text{between}_{i, j}$ (với $i \le j$) - đáp án cho truy vấn bắt đầu ở đầu khối $i$ và kết thúc ở cuối khối $j$. Lưu ý ta có $\sqrt{n}$ khối, nên kích thước mảng này là $O(\sqrt{n}^2) = O(n)$.

Hãy xét một ví dụ.

Cho $\circ$ là $+$ (tức ta tính tổng trên đoạn) và có mảng $a$ sau:

`{1, 2, 3, 4, 5, 6, 7, 8, 9}`

Mảng được chia thành ba khối: `{1, 2, 3}`, `{4, 5, 6}` và `{7, 8, 9}`.

Với khối thứ nhất, $\text{prefixOp}$ là `{1, 3, 6}` và $\text{suffixOp}$ là `{6, 5, 3}`.

Với khối thứ hai, $\text{prefixOp}$ là `{4, 9, 15}` và $\text{suffixOp}$ là `{15, 11, 6}`.

Với khối thứ ba, $\text{prefixOp}$ là `{7, 15, 24}` và $\text{suffixOp}$ là `{24, 17, 9}`.

Mảng $\text{between}$ là:

~~~~~
{
    {6, 21, 45},
    {0, 15, 39},
    {0, 0,  24}
}
~~~~~

(giả sử các phần tử không hợp lệ có $i > j$ được điền bằng không)

Các mảng này có thể được tính dễ dàng trong $O(n)$ thời gian và bộ nhớ.

Ta đã có thể trả lời một số truy vấn bằng các mảng này. Nếu truy vấn không nằm gọn trong một khối, ta có thể chia nó thành ba phần: hậu tố của một khối, sau đó là một đoạn gồm các khối liên tiếp, rồi đến tiền tố của một khối. Ta trả lời bằng cách lấy một giá trị từ $\text{suffixOp}$, rồi một giá trị từ $\text{between}$ và cuối cùng một giá trị từ $\text{prefixOp}$, sau đó áp dụng phép toán theo thứ tự đó.

Tuy nhiên, nếu truy vấn nằm hoàn toàn trong một khối thì ta không thể xử lý bằng ba mảng trên. Ta cần tìm cách khác.

### Tạo cây

Những truy vấn ta chưa trả lời được là các truy vấn nằm hoàn toàn trong một khối. Nhưng **điều gì xảy ra nếu ta xây dựng cấu trúc giống như trên cho từng khối?** Ta có thể làm như vậy một cách đệ quy cho đến khi đạt kích thước khối $1$ hoặc $2$. Đáp án cho những khối này dễ dàng được tính trong $O(1)$.

Nhờ đó ta thu được một cây. Mỗi nút biểu diễn một đoạn của mảng. Nút biểu diễn đoạn có kích thước $k$ có $\sqrt{k}$ nút con -- mỗi khối tương ứng với một nút con. Mỗi nút cũng chứa ba mảng đã mô tả cho đoạn mà nó biểu diễn. Gốc cây biểu diễn toàn bộ mảng. Các nút biểu diễn đoạn có độ dài $1$ hoặc $2$ là lá.

Chiều cao của cây là $O(\log \log n)$, vì nếu một đỉnh biểu diễn mảng độ dài $k$ thì các nút con của nó có độ dài $\sqrt{k}$. Ta có $\log(\sqrt{k}) = \frac{\log{k}}{2}$, nên $\log k$ giảm một nửa sau mỗi tầng và chiều cao cây là $O(\log \log n)$. Thời gian xây dựng và bộ nhớ đều là $O(n \cdot \log \log n)$, vì mỗi phần tử của mảng xuất hiện đúng một lần trên mỗi tầng của cây.

Bây giờ ta có thể trả lời truy vấn trong $O(\log \log n)$. Ta đi xuống cây cho đến khi gặp một đoạn có độ dài $1$ hoặc $2$ (đáp án tính được trong $O(1)$) hoặc gặp đoạn đầu tiên mà truy vấn không nằm hoàn toàn trong một khối của nó. Xem mục đầu để biết cách trả lời truy vấn ở trường hợp sau.

Vậy mỗi truy vấn đã mất $O(\log \log n)$. Có thể nhanh hơn không?

### Tối ưu độ phức tạp truy vấn

Một cách tối ưu khá trực tiếp là tìm kiếm nhị phân nút cây cần dùng. Với tìm kiếm nhị phân, mỗi truy vấn đạt độ phức tạp $O(\log \log \log n)$. Có thể nhanh hơn nữa không?

Câu trả lời là có. Hãy giả sử hai điều sau:

1. Kích thước mỗi khối là lũy thừa của hai.
2. Tất cả các khối trên cùng một tầng đều bằng nhau.

Để đạt được điều này, ta có thể thêm một số phần tử bằng không vào mảng để kích thước của nó trở thành lũy thừa của hai.

Khi đó, kích thước một số khối có thể tăng gấp đôi để trở thành lũy thừa của hai, nhưng vẫn có kích thước $O(\sqrt{k})$ và ta giữ được độ phức tạp tuyến tính khi xây dựng các mảng trong một đoạn.

Bây giờ ta có thể dễ dàng kiểm tra liệu truy vấn có nằm hoàn toàn trong một khối kích thước $2^k$ hay không. Hãy viết hai đầu truy vấn $l$ và $r$ (đánh số từ 0) ở dạng nhị phân. Chẳng hạn, giả sử $k=4, l=39, r=46$. Biểu diễn nhị phân của $l$ và $r$ là:

$l = 39_{10} = 100111_2$

$r = 46_{10} = 101110_2$

Nhớ rằng các đoạn trên cùng một tầng có kích thước bằng nhau và các khối trên tầng đó cũng có kích thước bằng nhau (trong ví dụ này là $2^k = 2^4 = 16$). Các khối phủ toàn bộ mảng, nên khối đầu tiên chứa các phần tử $(0 - 15)$ (tương ứng $(000000_2 - 001111_2)$ trong hệ nhị phân), khối thứ hai chứa các phần tử $(16 - 31)$ (tương ứng $(010000_2 - 011111_2)$ trong hệ nhị phân), v.v. Chỉ số các vị trí trong cùng một khối chỉ có thể khác nhau ở $k$ (ở đây là $4$) bit cuối. Trong ví dụ này, $l$ và $r$ có các bit giống nhau ngoài bốn bit thấp nhất, nên chúng nằm trong cùng một khối.

Vậy ta cần kiểm tra xem có nhiều hơn $k$ bit thấp nhất khác nhau hay không (tương đương kiểm tra $l\ \text{xor}\ r$ không vượt quá $2^k-1$).

Dựa trên nhận xét này, ta có thể nhanh chóng tìm được tầng phù hợp để trả lời truy vấn. Cách làm như sau:

1. Với mỗi $i$ không vượt quá kích thước mảng, tìm bit cao nhất bằng $1$. Để làm nhanh, ta dùng quy hoạch động và một mảng tính trước.

2. Với mỗi $q(l, r)$, tìm bit cao nhất của $l\ \text{xor}\ r$ rồi dùng thông tin này để chọn tầng có thể xử lý truy vấn dễ dàng. Ở đây ta cũng có thể dùng một mảng tính trước.

Xem thêm chi tiết trong mã bên dưới.

Như vậy ta có thể trả lời mỗi truy vấn trong $O(1)$. Thành công! :)

## Cập nhật phần tử

Ta cũng có thể cập nhật các phần tử trong Sqrt Tree. Cấu trúc hỗ trợ cả cập nhật một phần tử lẫn cập nhật trên một đoạn.

### Cập nhật một phần tử

Xét truy vấn $\text{update}(x, val)$ thực hiện phép gán $a_x = val$. Ta cần xử lý truy vấn này đủ nhanh.

#### Cách tiếp cận trực tiếp

Trước hết, hãy xem những gì thay đổi trong cây khi một phần tử thay đổi. Xét một nút cây có độ dài $l$ và các mảng của nó: $\text{prefixOp}$, $\text{suffixOp}$ và $\text{between}$. Dễ thấy chỉ có $O(\sqrt{l})$ phần tử trong $\text{prefixOp}$ và $\text{suffixOp}$ thay đổi (chỉ bên trong khối chứa phần tử bị thay đổi). Có $O(l)$ phần tử thay đổi trong $\text{between}$. Do đó, $O(l)$ phần tử trong nút cây được cập nhật.

Mỗi phần tử $x$ xuất hiện trong đúng một nút cây ở mỗi tầng. Nút gốc (tầng $0$) có độ dài $O(n)$, các nút ở tầng $1$ có độ dài $O(\sqrt{n})$, các nút ở tầng $2$ có độ dài $O(\sqrt{\sqrt{n}})$, v.v. Vì vậy độ phức tạp thời gian mỗi lần cập nhật là $O(n + \sqrt{n} + \sqrt{\sqrt{n}} + \dots) = O(n)$.

Nhưng cách này quá chậm. Có thể nhanh hơn không?

#### Một sqrt-tree bên trong sqrt-tree

Lưu ý rằng nút thắt khi cập nhật là xây dựng lại $\text{between}$ của nút gốc. Để tối ưu, ta bỏ mảng này! Thay cho $\text{between}$, ta lưu một sqrt-tree khác cho nút gốc. Gọi cây đó là $\text{index}$. Nó đóng cùng vai trò với $\text{between}$&mdash;trả lời truy vấn trên các đoạn khối. Các nút cây còn lại không có $\text{index}$ mà vẫn giữ các mảng $\text{between}$.

Một sqrt-tree được gọi là _có chỉ mục_ nếu nút gốc có $\text{index}$. Một sqrt-tree có mảng $\text{between}$ ở nút gốc được gọi là _không có chỉ mục_. Lưu ý bản thân $\text{index}$ **là cây _không có chỉ mục_**.

Ta có thuật toán cập nhật một cây _có chỉ mục_ như sau:

* Cập nhật $\text{prefixOp}$ và $\text{suffixOp}$ trong $O(\sqrt{n})$.

* Cập nhật $\text{index}$. Cây này có độ dài $O(\sqrt{n})$ và ta chỉ cần cập nhật một phần tử trong đó (đại diện cho khối bị thay đổi). Do đó bước này có độ phức tạp $O(\sqrt{n})$. Ta có thể dùng thuật toán “chậm” đã mô tả ở đầu mục này.

* Đi vào nút con biểu diễn khối bị thay đổi và cập nhật nó trong $O(\sqrt{n})$ bằng thuật toán “chậm”.

Độ phức tạp truy vấn vẫn là $O(1)$: ta cần dùng $\text{index}$ không quá một lần trong mỗi truy vấn, và việc đó mất $O(1)$.

Vậy tổng độ phức tạp thời gian để cập nhật một phần tử là $O(\sqrt{n})$. Thành công! :)

### Cập nhật một đoạn

Sqrt-tree còn có thể thực hiện các thao tác như gán giá trị cho các phần tử trên một đoạn. $\text{massUpdate}(x, l, r)$ nghĩa là $a_i = x$ với mọi $l \le i \le r$.

Có hai cách thực hiện: cách thứ nhất xử lý $\text{massUpdate}$ trong $O(\sqrt{n}\cdot \log \log n)$, đồng thời giữ $O(1)$ cho mỗi truy vấn. Cách thứ hai xử lý $\text{massUpdate}$ trong $O(\sqrt{n})$, nhưng độ phức tạp truy vấn trở thành $O(\log \log n)$.

Ta sẽ dùng kỹ thuật lan truyền lười (lazy propagation) giống như trên cây đoạn: đánh dấu một số nút là _lười_ và đẩy các dấu khi cần thiết. Tuy nhiên có một điểm khác cây đoạn: đẩy một nút rất tốn kém, nên không thể thực hiện trong lúc truy vấn. Ở tầng $0$, đẩy một nút mất $O(\sqrt{n})$ thời gian. Vì vậy, ta không đẩy nút trong truy vấn mà chỉ xét nút hiện tại hoặc nút cha của nó có dấu _lười_ hay không, rồi tính đến dấu đó khi xử lý truy vấn.

#### Cách thứ nhất

Trong cách thứ nhất, chỉ các nút ở tầng $1$ (có độ dài $O(\sqrt{n}$) mới có thể được đánh dấu _lười_. Khi đẩy một nút như vậy, ta cập nhật toàn bộ cây con của nó, kể cả chính nó, trong $O(\sqrt{n}\cdot \log \log n)$. Quá trình $\text{massUpdate}$ như sau:

* Xét các nút ở tầng $1$ và các khối tương ứng.

* Một số khối được $\text{massUpdate}$ bao phủ hoàn toàn. Đánh dấu _lười_ cho chúng trong $O(\sqrt{n})$.

* Một số khối được bao phủ một phần. Có không quá hai khối như vậy. Xây dựng lại chúng trong $O(\sqrt{n}\cdot \log \log n)$. Nếu chúng đã có dấu _lười_, cần tính đến dấu đó.

* Cập nhật $\text{prefixOp}$ và $\text{suffixOp}$ cho các khối được bao phủ một phần trong $O(\sqrt{n})$ (vì chỉ có hai khối như vậy).

* Xây dựng lại $\text{index}$ trong $O(\sqrt{n}\cdot \log \log n)$.

Như vậy ta có thể thực hiện $\text{massUpdate}$ nhanh. Nhưng lan truyền lười ảnh hưởng đến truy vấn thế nào? Các truy vấn được thay đổi như sau:

* Nếu truy vấn nằm hoàn toàn trong một khối _lười_, tính đáp án có xét đến dấu _lười_. $O(1)$.

* Nếu truy vấn gồm nhiều khối, một số trong đó là _lười_, ta chỉ cần xét dấu _lười_ ở khối ngoài cùng bên trái và bên phải. Các khối còn lại được tính bằng $\text{index}$, vốn đã biết đáp án trên khối _lười_ (vì nó được xây dựng lại sau mỗi lần thay đổi). $O(1)$.

Độ phức tạp truy vấn vẫn là $O(1)$.

#### Cách thứ hai

Trong cách này, mọi nút đều có thể _lười_ (trừ nút gốc). Ngay cả các nút trong $\text{index}$ cũng có thể _lười_. Vì vậy khi xử lý một truy vấn, ta phải tìm dấu _lười_ ở tất cả các nút tổ tiên, tức độ phức tạp truy vấn là $O(\log \log n)$.

Nhưng $\text{massUpdate}$ trở nên nhanh hơn. Cách làm như sau:

* Một số khối được $\text{massUpdate}$ bao phủ hoàn toàn. Ta thêm dấu _lười_ cho chúng trong $O(\sqrt{n})$.

* Cập nhật $\text{prefixOp}$ và $\text{suffixOp}$ cho các khối được bao phủ một phần trong $O(\sqrt{n})$ (vì chỉ có hai khối như vậy).

* Đừng quên cập nhật chỉ mục. Việc này mất $O(\sqrt{n})$ (ta dùng cùng thuật toán $\text{massUpdate}$).

* Cập nhật mảng $\text{between}$ cho các cây con _không có chỉ mục_.

* Đi vào các nút biểu diễn khối được bao phủ một phần và gọi đệ quy $\text{massUpdate}$.

Lưu ý rằng trong lời gọi đệ quy, ta thực hiện $\text{massUpdate}$ trên tiền tố hoặc hậu tố. Với các cập nhật tiền tố và hậu tố, có không quá một nút con được bao phủ một phần. Vì vậy, ta thăm một nút ở tầng $1$, hai nút ở tầng $2$ và hai nút ở mọi tầng sâu hơn. Do đó độ phức tạp thời gian là $O(\sqrt{n} + \sqrt{\sqrt{n}} + \dots) = O(\sqrt{n})$. Cách này tương tự cập nhật hàng loạt trên cây đoạn.

## Cài đặt

Cài đặt Sqrt Tree sau đây thực hiện các thao tác: xây dựng trong $O(n \cdot \log \log n)$, trả lời truy vấn trong $O(1)$ và cập nhật một phần tử trong $O(\sqrt{n})$.

~~~~~cpp
SqrtTreeItem op(const SqrtTreeItem &a, const SqrtTreeItem &b);

inline int log2Up(int n) {
	int res = 0;
	while ((1 << res) < n) {
		res++;
	}
	return res;
}

class SqrtTree {
private:
	int n, lg, indexSz;
	vector<SqrtTreeItem> v;
	vector<int> clz, layers, onLayer;
	vector< vector<SqrtTreeItem> > pref, suf, between;
	
	inline void buildBlock(int layer, int l, int r) {
		pref[layer][l] = v[l];
		for (int i = l+1; i < r; i++) {
			pref[layer][i] = op(pref[layer][i-1], v[i]);
		}
		suf[layer][r-1] = v[r-1];
		for (int i = r-2; i >= l; i--) {
			suf[layer][i] = op(v[i], suf[layer][i+1]);
		}
	}
	
	inline void buildBetween(int layer, int lBound, int rBound, int betweenOffs) {
		int bSzLog = (layers[layer]+1) >> 1;
		int bCntLog = layers[layer] >> 1;
		int bSz = 1 << bSzLog;
		int bCnt = (rBound - lBound + bSz - 1) >> bSzLog;
		for (int i = 0; i < bCnt; i++) {
			SqrtTreeItem ans;
			for (int j = i; j < bCnt; j++) {
				SqrtTreeItem add = suf[layer][lBound + (j << bSzLog)];
				ans = (i == j) ? add : op(ans, add);
				between[layer-1][betweenOffs + lBound + (i << bCntLog) + j] = ans;
			}
		}
	}
	
	inline void buildBetweenZero() {
		int bSzLog = (lg+1) >> 1;
		for (int i = 0; i < indexSz; i++) {
			v[n+i] = suf[0][i << bSzLog];
		}
		build(1, n, n + indexSz, (1 << lg) - n);
	}
	
	inline void updateBetweenZero(int bid) {
		int bSzLog = (lg+1) >> 1;
		v[n+bid] = suf[0][bid << bSzLog];
		update(1, n, n + indexSz, (1 << lg) - n, n+bid);
	}
	
	void build(int layer, int lBound, int rBound, int betweenOffs) {
		if (layer >= (int)layers.size()) {
			return;
		}
		int bSz = 1 << ((layers[layer]+1) >> 1);
		for (int l = lBound; l < rBound; l += bSz) {
			int r = min(l + bSz, rBound);
			buildBlock(layer, l, r);
			build(layer+1, l, r, betweenOffs);
		}
		if (layer == 0) {
			buildBetweenZero();
		} else {
			buildBetween(layer, lBound, rBound, betweenOffs);
		}
	}
	
	void update(int layer, int lBound, int rBound, int betweenOffs, int x) {
		if (layer >= (int)layers.size()) {
			return;
		}
		int bSzLog = (layers[layer]+1) >> 1;
		int bSz = 1 << bSzLog;
		int blockIdx = (x - lBound) >> bSzLog;
		int l = lBound + (blockIdx << bSzLog);
		int r = min(l + bSz, rBound);
		buildBlock(layer, l, r);
		if (layer == 0) {
			updateBetweenZero(blockIdx);
		} else {
			buildBetween(layer, lBound, rBound, betweenOffs);
		}
		update(layer+1, l, r, betweenOffs, x);
	}
	
	inline SqrtTreeItem query(int l, int r, int betweenOffs, int base) {
		if (l == r) {
			return v[l];
		}
		if (l + 1 == r) {
			return op(v[l], v[r]);
		}
		int layer = onLayer[clz[(l - base) ^ (r - base)]];
		int bSzLog = (layers[layer]+1) >> 1;
		int bCntLog = layers[layer] >> 1;
		int lBound = (((l - base) >> layers[layer]) << layers[layer]) + base;
		int lBlock = ((l - lBound) >> bSzLog) + 1;
		int rBlock = ((r - lBound) >> bSzLog) - 1;
		SqrtTreeItem ans = suf[layer][l];
		if (lBlock <= rBlock) {
			SqrtTreeItem add = (layer == 0) ? (
				query(n + lBlock, n + rBlock, (1 << lg) - n, n)
			) : (
				between[layer-1][betweenOffs + lBound + (lBlock << bCntLog) + rBlock]
			);
			ans = op(ans, add);
		}
		ans = op(ans, pref[layer][r]);
		return ans;
	}
public:
	inline SqrtTreeItem query(int l, int r) {
		return query(l, r, 0, 0);
	}
	
	inline void update(int x, const SqrtTreeItem &item) {
		v[x] = item;
		update(0, 0, n, 0, x);
	}
	
	SqrtTree(const vector<SqrtTreeItem>& a)
		: n((int)a.size()), lg(log2Up(n)), v(a), clz(1 << lg), onLayer(lg+1) {
		clz[0] = 0;
		for (int i = 1; i < (int)clz.size(); i++) {
			clz[i] = clz[i >> 1] + 1;
		}
		int tlg = lg;
		while (tlg > 1) {
			onLayer[tlg] = (int)layers.size();
			layers.push_back(tlg);
			tlg = (tlg+1) >> 1;
		}
		for (int i = lg-1; i >= 0; i--) {
			onLayer[i] = max(onLayer[i], onLayer[i+1]);
		}
		int betweenLayers = max(0, (int)layers.size() - 1);
		int bSzLog = (lg+1) >> 1;
		int bSz = 1 << bSzLog;
		indexSz = (n + bSz - 1) >> bSzLog;
		v.resize(n + indexSz);
		pref.assign(layers.size(), vector<SqrtTreeItem>(n + indexSz));
		suf.assign(layers.size(), vector<SqrtTreeItem>(n + indexSz));
		between.assign(betweenLayers, vector<SqrtTreeItem>((1 << lg) + bSz));
		build(0, 0, n, 0);
	}
};

~~~~~


## Bài tập

[CodeChef - SEGPROD](https://www.codechef.com/NOV17/problems/SEGPROD)
