---
tags:
  - Translated
e_maxx_link: bfs
translation:
  source: graph/breadth-first-search.md
  source_commit: 7d5943c8c1737c6b4aa63aff77bf2dbe4d4b9dbd
  status: draft
  last_synced: 2026-08-06
---

# Tìm kiếm theo chiều rộng

Tìm kiếm theo chiều rộng (Breadth-First Search, viết tắt là BFS) là một trong những thuật toán tìm kiếm cơ bản và quan trọng nhất trên đồ thị.

Nhờ cách thuật toán hoạt động, đường đi BFS tìm được từ đỉnh xuất phát đến bất kỳ đỉnh nào là đường đi ngắn nhất đến đỉnh đó, tức đường đi chứa ít cạnh nhất trong đồ thị không trọng số.

Thuật toán chạy trong $O(n + m)$, trong đó $n$ là số đỉnh và $m$ là số cạnh.

## Mô tả thuật toán

Đầu vào của thuật toán là một đồ thị không trọng số và chỉ số của đỉnh xuất phát $s$. Đồ thị có thể có hướng hoặc vô hướng; điều này không làm thay đổi cách BFS hoạt động.

Có thể hình dung thuật toán như một đám cháy lan trên đồ thị: ở bước thứ không, chỉ đỉnh nguồn $s$ đang cháy. Ở mỗi bước tiếp theo, lửa tại từng đỉnh lan sang tất cả các đỉnh kề. Sau mỗi vòng lặp, "vòng lửa" mở rộng thêm một lớp, vì thế thuật toán có tên là tìm kiếm theo chiều rộng.

Cụ thể hơn, ta tạo một hàng đợi $q$ chứa các đỉnh cần xử lý và một mảng Boolean $used[]$ cho biết mỗi đỉnh đã được thăm hay chưa.

Ban đầu, đưa đỉnh nguồn $s$ vào hàng đợi, đặt $used[s] = true$, còn với mọi đỉnh $v$ khác thì đặt $used[v] = false$.
Sau đó, lặp cho đến khi hàng đợi rỗng. Trong mỗi vòng lặp, lấy một đỉnh ở đầu hàng đợi, duyệt mọi cạnh đi ra từ đỉnh đó; nếu một cạnh dẫn đến đỉnh chưa được thăm, đánh dấu đỉnh ấy đã được thăm và đưa nó vào hàng đợi.

Khi hàng đợi rỗng, BFS đã thăm mọi đỉnh có thể đi tới từ nguồn $s$, và mỗi đỉnh được tiếp cận theo đường đi ngắn nhất có thể.
Ta cũng có thể tính độ dài đường đi ngắn nhất bằng cách duy trì mảng khoảng cách $d[]$, đồng thời lưu thông tin để khôi phục các đường đi bằng mảng "cha" $p[]$, trong đó $p[v]$ là đỉnh mà từ đó ta đi tới $v$ lần đầu.

## Cài đặt

Dưới đây là cách cài đặt thuật toán bằng C++ và Java.

=== "C++"
    ```cpp
    vector<vector<int>> adj;  // adjacency list representation
    int n; // number of nodes
    int s; // source vertex

    queue<int> q;
    vector<bool> used(n);
    vector<int> d(n), p(n);

    q.push(s);
    used[s] = true;
    p[s] = -1;
    while (!q.empty()) {
        int v = q.front();
        q.pop();
        for (int u : adj[v]) {
            if (!used[u]) {
                used[u] = true;
                q.push(u);
                d[u] = d[v] + 1;
                p[u] = v;
            }
        }
    }
    ```
=== "Java"
    ```java
    ArrayList<ArrayList<Integer>> adj = new ArrayList<>(); // adjacency list representation
        
    int n; // number of nodes
    int s; // source vertex


    LinkedList<Integer> q = new LinkedList<Integer>();
    boolean used[] = new boolean[n];
    int d[] = new int[n];
    int p[] = new int[n];

    q.push(s);
    used[s] = true;
    p[s] = -1;
    while (!q.isEmpty()) {
        int v = q.pop();
        for (int u : adj.get(v)) {
            if (!used[u]) {
                used[u] = true;
                q.push(u);
                d[u] = d[v] + 1;
                p[u] = v;
            }
        }
    }
    ```
    
Nếu cần khôi phục và in đường đi ngắn nhất từ nguồn đến một đỉnh $u$, ta có thể làm như sau:
    
=== "C++"
    ```cpp
    if (!used[u]) {
        cout << "No path!";
    } else {
        vector<int> path;
        for (int v = u; v != -1; v = p[v])
            path.push_back(v);
        reverse(path.begin(), path.end());
        cout << "Path: ";
        for (int v : path)
            cout << v << " ";
    }
    ```
=== "Java"
    ```java
    if (!used[u]) {
        System.out.println("No path!");
    } else {
        ArrayList<Integer> path = new ArrayList<Integer>();
        for (int v = u; v != -1; v = p[v])
            path.add(v);
        Collections.reverse(path);
        for(int v : path)
            System.out.println(v);
    }
    ```
    
## Ứng dụng của BFS

* Tìm đường đi ngắn nhất từ một đỉnh nguồn đến các đỉnh khác trong đồ thị không trọng số.

* Tìm mọi thành phần liên thông trong đồ thị vô hướng trong $O(n + m)$:
ta chạy BFS từ từng đỉnh, ngoại trừ các đỉnh đã được thăm trong những lần chạy trước.
Nói cách khác, ta thực hiện BFS thông thường từ mỗi đỉnh nhưng không đặt lại mảng $used[]$ khi chuyển sang một thành phần liên thông mới. Tổng thời gian vẫn là $O(n + m)$. Việc chạy nhiều lần BFS trên cùng đồ thị mà không xóa mảng $used []$ được gọi là một chuỗi các lần tìm kiếm theo chiều rộng.

* Tìm lời giải của một bài toán hoặc trò chơi với số bước ít nhất, nếu mỗi trạng thái có thể được biểu diễn bằng một đỉnh và mỗi phép chuyển trạng thái được biểu diễn bằng một cạnh của đồ thị.

* Tìm đường đi ngắn nhất trong đồ thị có trọng số cạnh bằng 0 hoặc 1:
chỉ cần sửa BFS thông thường một chút. Thay vì duy trì mảng $used[]$, ta kiểm tra xem khoảng cách mới đến một đỉnh có nhỏ hơn khoảng cách tốt nhất hiện tại hay không. Nếu cạnh đang xét có trọng số 0, đưa đỉnh vào đầu hàng đợi; nếu trọng số là 1, đưa nó vào cuối hàng đợi. Biến thể này được giải thích chi tiết trong bài [0-1 BFS](01_bfs.md).

* Tìm chu trình ngắn nhất trong đồ thị có hướng không trọng số:
chạy BFS từ từng đỉnh.
Ngay khi từ đỉnh hiện tại có thể quay lại đỉnh nguồn, ta đã tìm được chu trình ngắn nhất chứa nguồn đó.
Khi ấy có thể dừng BFS hiện tại và bắt đầu BFS từ đỉnh tiếp theo.
Trong tất cả các chu trình thu được, nhiều nhất một chu trình từ mỗi lần BFS, chọn chu trình ngắn nhất.

* Tìm mọi cạnh nằm trên ít nhất một đường đi ngắn nhất giữa hai đỉnh $(a, b)$.
Ta chạy hai lần tìm kiếm theo chiều rộng:
một lần từ $a$ và một lần từ $b$.
Gọi $d_a []$ là mảng khoảng cách ngắn nhất thu được từ BFS bắt đầu tại $a$, và $d_b []$ là mảng khoảng cách ngắn nhất thu được từ BFS bắt đầu tại $b$.
Với mỗi cạnh $(u, v)$, có thể kiểm tra dễ dàng cạnh đó có nằm trên một đường đi ngắn nhất giữa $a$ và $b$ hay không bằng điều kiện $d_a [u] + 1 + d_b [v] = d_a [b]$.

* Tìm mọi đỉnh nằm trên ít nhất một đường đi ngắn nhất giữa hai đỉnh $(a, b)$.
Ta cũng chạy hai lần tìm kiếm theo chiều rộng:
một lần từ $a$ và một lần từ $b$.
Gọi $d_a []$ là mảng khoảng cách ngắn nhất từ $a$, và $d_b []$ là mảng khoảng cách ngắn nhất từ $b$.
Với mỗi đỉnh $v$, nó nằm trên một đường đi ngắn nhất giữa $a$ và $b$ khi và chỉ khi $d_a [v] + d_b [v] = d_a [b]$.

* Tìm hành trình ngắn nhất có độ dài chẵn từ đỉnh nguồn $s$ đến đỉnh đích $t$ trong đồ thị không trọng số:
ta xây dựng một đồ thị phụ, trong đó mỗi đỉnh là một trạng thái $(v, c)$; $v$ là đỉnh hiện tại, còn $c = 0$ hoặc $c = 1$ biểu thị tính chẵn lẻ của độ dài hành trình hiện tại.
Mỗi cạnh $(u, v)$ của đồ thị gốc được thay bằng hai cạnh $((u, 0), (v, 1))$ và $((u, 1), (v, 0))$ trong đồ thị mới.
Sau đó, chạy BFS để tìm hành trình ngắn nhất từ trạng thái đầu $(s, 0)$ đến trạng thái cuối $(t, 0)$.<br>**Lưu ý**: Ở đây dùng thuật ngữ "_hành trình_" thay vì "_đường đi_" là có chủ ý, vì một đỉnh có thể xuất hiện nhiều lần trong hành trình tìm được để tổng số cạnh trở thành chẵn. Bài toán tìm _đường đi_ chẵn ngắn nhất là NP-Complete trên đồ thị có hướng, và [có thể giải trong thời gian tuyến tính](https://onlinelibrary.wiley.com/doi/abs/10.1002/net.3230140403) trên đồ thị vô hướng, nhưng cần một cách tiếp cận phức tạp hơn nhiều.

## Bài tập luyện tập

* [SPOJ: AKBAR](http://spoj.com/problems/AKBAR)
* [SPOJ: NAKANJ](http://www.spoj.com/problems/NAKANJ/)
* [SPOJ: WATER](http://www.spoj.com/problems/WATER)
* [SPOJ: MICE AND MAZE](http://www.spoj.com/problems/MICEMAZE/)
* [Timus: Caravans](http://acm.timus.ru/problem.aspx?space=1&num=2034)
* [DevSkill - Holloween Party (archived)](http://web.archive.org/web/20200930162803/http://www.devskill.com/CodingProblems/ViewProblem/60)
* [DevSkill - Ohani And The Link Cut Tree (archived)](http://web.archive.org/web/20170216192002/http://devskill.com:80/CodingProblems/ViewProblem/150)
* [SPOJ - Spiky Mazes](http://www.spoj.com/problems/SPIKES/)
* [SPOJ - Four Chips (hard)](http://www.spoj.com/problems/ADV04F1/)
* [SPOJ - Inversion Sort](http://www.spoj.com/problems/INVESORT/)
* [Codeforces - Shortest Path](http://codeforces.com/contest/59/problem/E)
* [SPOJ - Yet Another Multiple Problem](http://www.spoj.com/problems/MULTII/)
* [UVA 11392 - Binary 3xType Multiple](https://uva.onlinejudge.org/index.php?option=com_onlinejudge&Itemid=8&page=show_problem&problem=2387)
* [UVA 10968 - KuPellaKeS](https://uva.onlinejudge.org/index.php?option=com_onlinejudge&Itemid=8&page=show_problem&problem=1909)
* [Codeforces - Police Stations](http://codeforces.com/contest/796/problem/D)
* [Codeforces - Okabe and City](http://codeforces.com/contest/821/problem/D)
* [SPOJ - Find the Treasure](http://www.spoj.com/problems/DIGOKEYS/)
* [Codeforces - Bear and Forgotten Tree 2](http://codeforces.com/contest/653/problem/E)
* [Codeforces - Cycle in Maze](http://codeforces.com/contest/769/problem/C)
* [UVA - 11312 - Flipping Frustration](https://uva.onlinejudge.org/index.php?option=com_onlinejudge&Itemid=8&page=show_problem&problem=2287)
* [SPOJ - Ada and Cycle](http://www.spoj.com/problems/ADACYCLE/)
* [CSES - Labyrinth](https://cses.fi/problemset/task/1193)
* [CSES - Message Route](https://cses.fi/problemset/task/1667/)
* [CSES - Monsters](https://cses.fi/problemset/task/1194)
* [UVA 704 - Colour Hash](https://onlinejudge.org/index.php?option=com_onlinejudge&Itemid=8&category=9&page=show_problem&problem=645) (bidirectional BFS)