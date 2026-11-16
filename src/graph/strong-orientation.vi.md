---
tags:
  - Original
translation:
  source: graph/strong-orientation.md
  source_commit: 69a7b37d91b78c03bc6974c9974dbd03a72a71b4
  status: draft
  last_synced: 2026-11-15
---

# Định hướng mạnh

Một **định hướng mạnh** của đồ thị vô hướng là cách gán hướng cho từng cạnh để tạo thành một [đồ thị liên thông mạnh](strongly-connected-components.md).
Nghĩa là sau khi *định hướng*, ta có thể đi từ bất kỳ đỉnh nào đến bất kỳ đỉnh nào bằng cách đi theo các cạnh có hướng.

## Lời giải

Dĩ nhiên, không phải đồ thị nào cũng làm được như vậy.
Xét một [cạnh cầu](bridge-searching.md) trong đồ thị.
Ta phải gán hướng cho nó, khiến cạnh cầu này chỉ có thể được đi qua theo một chiều. Điều đó có nghĩa là ta không thể đi từ một đầu của cạnh cầu sang đầu kia theo ít nhất một trong hai chiều, nên không thể làm đồ thị liên thông mạnh.

Bây giờ xét phép [DFS](depth-first-search.md) trên một đồ thị liên thông không có cầu.
Rõ ràng ta sẽ thăm mỗi đỉnh.
Vì không có cầu, ta có thể xóa bất kỳ cạnh cây DFS nào mà vẫn đi được từ phía dưới lên phía trên cạnh đó bằng một đường đi chứa ít nhất một cạnh ngược.
Do đó, từ bất kỳ đỉnh nào ta có thể đi đến gốc cây DFS.
Ngoài ra, từ gốc cây DFS ta có thể đi đến bất kỳ đỉnh nào.
Vậy ta đã tìm được một định hướng mạnh!

Nói cách khác, để định hướng mạnh một đồ thị liên thông không có cầu, chạy DFS trên đồ thị, hướng các cạnh cây DFS ra xa gốc DFS và hướng mọi cạnh còn lại từ đỉnh hậu duệ về đỉnh tổ tiên trong cây DFS.

Kết quả rằng các đồ thị liên thông không có cầu chính là các đồ thị có định hướng mạnh được gọi là **định lý Robbins**.

## Mở rộng bài toán

Xét bài toán tìm cách định hướng đồ thị sao cho số thành phần liên thông mạnh (SCC) là nhỏ nhất.

Dĩ nhiên, mỗi thành phần liên thông của đồ thị có thể được xét riêng.
Vì chỉ các đồ thị không có cầu mới có thể được định hướng mạnh, ta tạm thời xóa tất cả các cạnh cầu.
Ta thu được một số thành phần không có cầu (chính xác bằng *số thành phần ban đầu* + *số cạnh cầu*) và biết rằng mỗi thành phần đó có thể được định hướng mạnh.

Ta chỉ được phép định hướng cạnh, không được xóa chúng, nhưng hóa ra ta có thể định hướng các cạnh cầu tùy ý.
Dĩ nhiên, cách dễ nhất là chạy thuật toán mô tả ở trên mà không sửa đổi trên từng thành phần liên thông ban đầu.

### Cài đặt

Dữ liệu vào gồm *n* — số đỉnh, *m* — số cạnh, rồi *m* dòng mô tả các cạnh.

Dòng đầu của kết quả là số SCC nhỏ nhất; dòng thứ hai là một xâu gồm *m* ký tự,
mỗi ký tự là `>` — cho biết cạnh tương ứng trong dữ liệu vào được hướng từ đỉnh bên trái sang đỉnh bên phải (theo thứ tự trong dữ liệu vào),
hoặc `<` — theo chiều ngược lại.

Đây là thuật toán tìm cầu được sửa đổi để đồng thời định hướng các cạnh; ta cũng có thể định hướng các cạnh trước rồi đếm SCC trong đồ thị có hướng ở bước thứ hai.

```cpp
vector<vector<pair<int, int>>> adj; // adjacency list - vertex and edge pairs
vector<pair<int, int>> edges;

vector<int> tin, low;
int bridge_cnt;
string orient;
vector<bool> edge_used;
void find_bridges(int v) {
	static int time = 0;
	low[v] = tin[v] = time++;
	for (auto p : adj[v]) {
		if (edge_used[p.second]) continue;
		edge_used[p.second] = true;
		orient[p.second] = v == edges[p.second].first ? '>' : '<';
		int nv = p.first;
		if (tin[nv] == -1) { // if nv is not visited yet
			find_bridges(nv);
			low[v] = min(low[v], low[nv]);
			if (low[nv] > tin[v]) {
				// a bridge between v and nv
				bridge_cnt++;
			}
		} else {
			low[v] = min(low[v], tin[nv]);
		}
	}
}

int main() {
	int n, m;
	scanf("%d %d", &n, &m);
	adj.resize(n);
	tin.resize(n, -1);
	low.resize(n, -1);
	orient.resize(m);
	edges.resize(m);
	edge_used.resize(m);
	for (int i = 0; i < m; i++) {
		int a, b;
		scanf("%d %d", &a, &b);
		a--; b--;
		adj[a].push_back({b, i});
		adj[b].push_back({a, i});
		edges[i] = {a, b};
	}
	int comp_cnt = 0;
	for (int v = 0; v < n; v++) {
		if (tin[v] == -1) {
			comp_cnt++;
			find_bridges(v);
		}
	}
	printf("%d\n%s\n", comp_cnt + bridge_cnt, orient.c_str());
}
```

## Bài tập

* [26th Polish OI - Osiedla](https://szkopul.edu.pl/problemset/problem/nldsb4EW1YuZykBlf4lcZL1Y/site/)
