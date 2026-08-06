---
tags:
  - Translated
e_maxx_link: dfs
translation:
  source: graph/depth-first-search.md
  source_commit: d8b695280d395a1513e5e0570b9ecb0312d439f3
  status: draft
  last_synced: 2026-08-07
---

# Tìm kiếm theo chiều sâu

Tìm kiếm theo chiều sâu (Depth-First Search, viết tắt là DFS) là một trong những thuật toán đồ thị quan trọng nhất.

Từ một đỉnh nguồn $u$, DFS tìm đường đi nhỏ nhất theo thứ tự từ điển đến từng đỉnh của đồ thị.
DFS cũng tìm được đường đi ngắn nhất trong cây, vì giữa hai đỉnh chỉ tồn tại một đường đi đơn. Tuy nhiên, tính chất này không đúng với đồ thị tổng quát.

Thuật toán chạy trong thời gian $O(m + n)$, trong đó $n$ là số đỉnh và $m$ là số cạnh.

## Mô tả thuật toán

Ý tưởng của DFS là đi sâu vào đồ thị hết mức có thể, rồi quay lui khi đến một đỉnh không còn đỉnh kề nào chưa được thăm.

Thuật toán có thể được mô tả và cài đặt bằng đệ quy rất dễ dàng:
ta bắt đầu tìm kiếm tại một đỉnh.
Sau khi thăm đỉnh đó, ta tiếp tục chạy DFS từ từng đỉnh kề chưa được thăm.
Bằng cách này, ta sẽ thăm mọi đỉnh có thể đi tới từ đỉnh xuất phát.

Xem phần cài đặt bên dưới để hiểu rõ hơn.

## Ứng dụng của tìm kiếm theo chiều sâu

  * Tìm một đường đi bất kỳ từ đỉnh nguồn $u$ đến mọi đỉnh khác trong đồ thị.
  
  * Tìm đường đi nhỏ nhất theo thứ tự từ điển từ đỉnh nguồn $u$ đến mọi đỉnh.
  
  * Kiểm tra một đỉnh trong cây có phải là tổ tiên của một đỉnh khác hay không:
  
    Ở đầu và cuối mỗi lời gọi tìm kiếm, ta lưu thời điểm vào và thời điểm ra của từng đỉnh.
    Khi đó, có thể trả lời cho mỗi cặp đỉnh $(i, j)$ trong $O(1)$:
    đỉnh $i$ là tổ tiên của đỉnh $j$ khi và chỉ khi $\text{entry}[i] < \text{entry}[j]$ và $\text{exit}[i] > \text{exit}[j]$.
  
  * Tìm tổ tiên chung gần nhất (Lowest Common Ancestor — LCA) của hai đỉnh.
  
  * Sắp xếp tô-pô:
  
    Chạy một chuỗi các lần tìm kiếm theo chiều sâu sao cho mỗi đỉnh được thăm đúng một lần, với tổng thời gian $O(n + m)$.
    Thứ tự tô-pô cần tìm là các đỉnh được sắp theo thứ tự giảm dần của thời điểm ra.
  
  
  * Kiểm tra đồ thị có chu trình hay không và tìm chu trình trong đồ thị, bằng cách nhận diện các cạnh ngược trong từng thành phần liên thông như trình bày bên dưới.
  
  * Tìm các thành phần liên thông mạnh trong đồ thị có hướng:
  
    Trước hết, thực hiện sắp xếp tô-pô trên đồ thị.
    Sau đó, đảo chiều mọi cạnh và chạy một chuỗi DFS khác theo thứ tự do phép sắp xếp tô-pô xác định. Thành phần được tạo bởi mỗi lời gọi DFS là một thành phần liên thông mạnh.
  
  * Tìm các cầu trong đồ thị vô hướng:
  
    Trước hết, chuyển đồ thị đã cho thành đồ thị có hướng bằng cách chạy một chuỗi DFS và định hướng mỗi cạnh theo chiều ta duyệt qua nó. Tiếp theo, tìm các thành phần liên thông mạnh trong đồ thị có hướng này. Các cầu là những cạnh có hai đầu thuộc hai thành phần liên thông mạnh khác nhau.

## Phân loại các cạnh của đồ thị

Ta có thể phân loại các cạnh của đồ thị $G$ dựa trên thời điểm vào và ra của hai đầu mút $u$, $v$ của cạnh $(u,v)$.
Cách phân loại này thường được sử dụng trong các bài toán như [tìm cầu](bridge-searching.md) và [tìm đỉnh khớp](cutpoints.md).

Ta chạy DFS và phân loại các cạnh gặp được theo các quy tắc sau.

Nếu $v$ chưa được thăm:

* Cạnh cây (Tree Edge) — Nếu $v$ được thăm sau $u$, cạnh $(u,v)$ được gọi là cạnh cây. Nói cách khác, nếu $v$ được thăm lần đầu trong lúc $u$ đang được xử lý, thì $(u,v)$ là một cạnh cây.
Các cạnh này tạo thành cây DFS, vì vậy chúng được gọi là cạnh cây.

Nếu $v$ đã được thăm trước $u$:

* Cạnh ngược (Back Edge) — Nếu $v$ là tổ tiên của $u$, cạnh $(u,v)$ là một cạnh ngược. $v$ là tổ tiên của $u$ khi ta đã đi vào $v$ nhưng chưa đi ra khỏi nó. Cạnh ngược tạo thành một chu trình: trong cây đệ quy DFS đã có đường đi từ tổ tiên $v$ đến hậu duệ $u$, còn cạnh ngược đi từ $u$ trở lại $v$. Vì vậy, có thể phát hiện chu trình bằng các cạnh ngược.

* Cạnh xuôi (Forward Edge) — Nếu $v$ là hậu duệ của $u$, cạnh $(u, v)$ là một cạnh xuôi. Nói cách khác, nếu ta đã thăm và đi ra khỏi $v$, đồng thời $\text{entry}[u] < \text{entry}[v]$, thì $(u,v)$ là một cạnh xuôi.
* Cạnh chéo (Cross Edge) — Nếu $v$ không phải tổ tiên cũng không phải hậu duệ của $u$, cạnh $(u, v)$ là một cạnh chéo. Nói cách khác, nếu ta đã thăm và đi ra khỏi $v$, đồng thời $\text{entry}[u] > \text{entry}[v]$, thì $(u,v)$ là một cạnh chéo.

**Định lý**. Cho $G$ là một đồ thị vô hướng. Khi chạy DFS trên $G$, mọi cạnh gặp được đều được phân loại là cạnh cây hoặc cạnh ngược; nói cách khác, cạnh xuôi và cạnh chéo chỉ tồn tại trong đồ thị có hướng.

Xét một cạnh tùy ý $(u,v)$ của $G$. Không mất tính tổng quát, giả sử $u$ được thăm trước $v$, tức $\text{entry}[u] < \text{entry}[v]$. Vì DFS chỉ xử lý mỗi cạnh một lần, chỉ có hai cách để xử lý và phân loại cạnh $(u,v)$:

* Lần đầu ta duyệt cạnh $(u,v)$ là theo chiều từ $u$ đến $v$. Vì $\text{entry}[u] < \text{entry}[v]$, tính đệ quy của DFS bảo đảm đỉnh $v$ sẽ được duyệt xong và thoát ra trước khi ta có thể quay ngược lên ngăn xếp lời gọi để thoát khỏi $u$. Do đó, tại thời điểm DFS lần đầu duyệt cạnh $(u,v)$ từ $u$ sang $v$, đỉnh $v$ phải chưa được thăm; nếu không, DFS đã duyệt cạnh này từ $v$ sang $u$ trước khi rời $v$, vì $u$ và $v$ kề nhau. Vì vậy, $(u,v)$ là cạnh cây.

* Lần đầu ta duyệt cạnh $(u,v)$ là theo chiều từ $v$ đến $u$. Do $u$ được phát hiện trước $v$ và mỗi cạnh chỉ được xử lý một lần, trường hợp này chỉ có thể xảy ra nếu tồn tại một đường khác từ $u$ đến $v$ không sử dụng cạnh $(u,v)$, khiến $u$ trở thành tổ tiên của $v$. Khi đó, cạnh $(u,v)$ khép kín một chu trình vì nó đi từ hậu duệ $v$ về tổ tiên $u$, là đỉnh chưa được thoát ra. Vì vậy, $(u,v)$ là cạnh ngược.

Chỉ có hai cách xử lý cạnh $(u,v)$ như trên. Do đó, khi chạy DFS trên đồ thị vô hướng $G$, mọi cạnh gặp được đều là cạnh cây hoặc cạnh ngược; cạnh xuôi và cạnh chéo chỉ tồn tại trong đồ thị có hướng. Định lý được chứng minh.

## Cài đặt

```cpp
vector<vector<int>> adj; // graph represented as an adjacency list
int n; // number of vertices

vector<bool> visited;

void dfs(int v) {
	visited[v] = true;
	for (int u : adj[v]) {
		if (!visited[u])
			dfs(u);
    }
}
```
Đây là cách cài đặt đơn giản nhất của tìm kiếm theo chiều sâu.
Như đã nêu trong phần ứng dụng, đôi khi ta cần tính thêm thời điểm vào, thời điểm ra và màu của mỗi đỉnh.
Ta tô màu 0 cho đỉnh chưa được thăm, màu 1 cho đỉnh đang được thăm và màu 2 cho đỉnh đã được xử lý xong.

Dưới đây là một cách cài đặt tổng quát có tính thêm các thông tin đó:

```cpp
vector<vector<int>> adj; // graph represented as an adjacency list
int n; // number of vertices

vector<int> color;

vector<int> time_in, time_out;
int dfs_timer = 0;

void dfs(int v) {
	time_in[v] = dfs_timer++;
	color[v] = 1;
	for (int u : adj[v])
		if (color[u] == 0)
			dfs(u);
	color[v] = 2;
	time_out[v] = dfs_timer++;
}
```

## Bài tập luyện tập

* [SPOJ: ABCPATH](http://www.spoj.com/problems/ABCPATH/)
* [SPOJ: EAGLE1](http://www.spoj.com/problems/EAGLE1/)
* [Codeforces: Kefa and Park](http://codeforces.com/problemset/problem/580/C)
* [Timus:Werewolf](http://acm.timus.ru/problem.aspx?space=1&num=1242)
* [Timus:Penguin Avia](http://acm.timus.ru/problem.aspx?space=1&num=1709)
* [Timus:Two Teams](http://acm.timus.ru/problem.aspx?space=1&num=1106)
* [SPOJ - Ada and Island](http://www.spoj.com/problems/ADASEA/)
* [UVA 657 - The die is cast](https://uva.onlinejudge.org/index.php?option=com_onlinejudge&Itemid=8&page=show_problem&problem=598)
* [SPOJ - Sheep](http://www.spoj.com/problems/KOZE/)
* [SPOJ - Path of the Rightenous Man](http://www.spoj.com/problems/RIOI_2_3/)
* [SPOJ - Validate the Maze](http://www.spoj.com/problems/MAKEMAZE/)
* [SPOJ - Ghosts having Fun](http://www.spoj.com/problems/GHOSTS/)
* [Codeforces - Underground Lab](http://codeforces.com/contest/781/problem/C)
* [DevSkill - Maze Tester (archived)](http://web.archive.org/web/20200319103915/https://www.devskill.com/CodingProblems/ViewProblem/3)
* [DevSkill - Tourist (archived)](http://web.archive.org/web/20190426175135/https://devskill.com/CodingProblems/ViewProblem/17)
* [Codeforces - Anton and Tree](http://codeforces.com/contest/734/problem/E)
* [Codeforces - Transformation: From A to B](http://codeforces.com/contest/727/problem/A)
* [Codeforces - One Way Reform](http://codeforces.com/contest/723/problem/E)
* [Codeforces - Centroids](http://codeforces.com/contest/709/problem/E)
* [Codeforces - Generate a String](http://codeforces.com/contest/710/problem/E)
* [Codeforces - Broken Tree](http://codeforces.com/contest/758/problem/E)
* [Codeforces - Dasha and Puzzle](http://codeforces.com/contest/761/problem/E)
* [Codeforces - Making genome In Berland](http://codeforces.com/contest/638/problem/B)
* [Codeforces - Road Improvement](http://codeforces.com/contest/638/problem/C)
* [Codeforces - Garland](http://codeforces.com/contest/767/problem/C)
* [Codeforces - Labeling Cities](http://codeforces.com/contest/794/problem/D)
* [Codeforces - Send the Fool Further!](http://codeforces.com/contest/802/problem/J1)
* [Codeforces - The tag Game](http://codeforces.com/contest/813/problem/C)
* [Codeforces - Leha and Another game about graphs](http://codeforces.com/contest/841/problem/D)
* [Codeforces - Shortest path problem](http://codeforces.com/contest/845/problem/G)
* [Codeforces - Upgrading Tree](http://codeforces.com/contest/844/problem/E)
* [Codeforces - From Y to Y](http://codeforces.com/contest/849/problem/C)
* [Codeforces - Chemistry in Berland](http://codeforces.com/contest/846/problem/E)
* [Codeforces - Wizards Tour](http://codeforces.com/contest/861/problem/F)
* [Codeforces - Ring Road](http://codeforces.com/contest/24/problem/A)
* [Codeforces - Mail Stamps](http://codeforces.com/contest/29/problem/C)
* [Codeforces - Ant on the Tree](http://codeforces.com/contest/29/problem/D)
* [SPOJ - Cactus](http://www.spoj.com/problems/CAC/)
* [SPOJ - Mixing Chemicals](http://www.spoj.com/problems/AMR10J/)
