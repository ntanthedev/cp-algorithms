---
tags:
  - Translated
e_maxx_link: games_on_graphs
translation:
  source: game_theory/games_on_graphs.md
  source_commit: 3ca79d1934e6e5e488acc56696a4247a334eee08
  status: draft
  last_synced: 2026-11-16
---

# Trò chơi trên đồ thị bất kỳ

Xét một trò chơi có hai người chơi trên đồ thị bất kỳ $G$. Trạng thái hiện tại của trò chơi là một đỉnh. Hai người lần lượt đi, mỗi lượt di chuyển từ đỉnh hiện tại đến một đỉnh kề qua một cạnh nối chúng. Tùy trò chơi, người không thể đi tiếp sẽ thua hoặc thắng.

Ta xét trường hợp tổng quát nhất: đồ thị có hướng bất kỳ, có thể có chu trình. Với một trạng thái ban đầu, nhiệm vụ của ta là xác định ai sẽ thắng nếu cả hai chơi tối ưu, hoặc xác định kết quả hòa.

Ta sẽ giải bài toán này rất hiệu quả: tìm kết quả cho mọi đỉnh xuất phát trong thời gian tuyến tính theo số cạnh, tức $O(m)$.

**Ghi chú của người dịch:** Với đồ thị tùy ý, việc duyệt hoặc khởi tạo tất cả các đỉnh cũng cần được tính vào độ phức tạp. Cận tổng quát là tuyến tính theo tổng số đỉnh và số cạnh; chẳng hạn, một đồ thị có nhiều đỉnh cô lập nhưng không có cạnh vẫn cần xử lý các đỉnh đó.

## Mô tả thuật toán

Ta gọi một đỉnh là đỉnh thắng nếu người bắt đầu ở trạng thái đó sẽ thắng khi chơi tối ưu, bất kể đối thủ đi thế nào. Tương tự, một đỉnh là đỉnh thua nếu người bắt đầu ở đó sẽ thua khi đối thủ chơi tối ưu.

Với một số đỉnh, ta đã biết trước chúng là đỉnh thắng hay thua: đó là các đỉnh không có cạnh đi ra.

Ta còn có các **quy tắc** sau:

- Nếu một đỉnh có cạnh đi ra dẫn tới đỉnh thua, thì bản thân nó là đỉnh thắng.
- Nếu mọi cạnh đi ra từ một đỉnh đều dẫn tới đỉnh thắng, thì đỉnh đó là đỉnh thua.
- Nếu tại một thời điểm vẫn còn các đỉnh chưa xác định và không đỉnh nào áp dụng được một trong hai quy tắc đầu, thì mỗi đỉnh đó khi được chọn làm điểm xuất phát sẽ dẫn đến hòa nếu cả hai chơi tối ưu.

Từ đây, ta có ngay thuật toán thời gian $O(n m)$: duyệt mọi đỉnh, thử áp dụng hai quy tắc đầu rồi lặp lại.

Tuy nhiên, ta có thể tăng tốc để đạt độ phức tạp $O(m)$.

Ta duyệt mọi đỉnh mà ta đã biết từ đầu là thắng hay thua. Với mỗi đỉnh, ta bắt đầu một lượt [tìm kiếm theo chiều sâu](../graph/depth-first-search.md). DFS này đi ngược theo các cạnh đảo chiều. Trước hết, nó không đi vào những đỉnh đã được xác định là thắng hoặc thua.

Nếu lượt tìm kiếm đi từ một đỉnh thua đến một đỉnh chưa xác định, ta đánh dấu đỉnh mới là thắng và tiếp tục DFS từ đó. Nếu đi từ một đỉnh thắng đến một đỉnh chưa xác định, ta phải kiểm tra xem mọi cạnh đi ra từ đỉnh mới có dẫn tới đỉnh thắng hay không. Ta có thể kiểm tra trong $O(1)$ bằng cách lưu số cạnh dẫn tới đỉnh thắng cho mỗi đỉnh.

Vì vậy, khi đi từ một đỉnh thắng đến một đỉnh chưa xác định, ta tăng bộ đếm và so sánh với số cạnh đi ra. Nếu hai số bằng nhau, ta đánh dấu đỉnh này là thua và tiếp tục DFS từ đó. Nếu không, ta chưa biết đỉnh đó thắng hay thua, nên chưa tiếp tục DFS từ nó.

Mỗi đỉnh thắng hoặc thua được thăm đúng một lần, các đỉnh chưa xác định không được thăm, và mỗi cạnh cũng được xét nhiều nhất một lần. Do đó độ phức tạp là $O(m)$.

## Cài đặt

Sau đây là cách cài đặt DFS. Giả sử biến `adj_rev` lưu danh sách kề của đồ thị ở dạng **đảo chiều**, tức thay vì lưu cạnh $(i, j)$ ta lưu $(j, i)$. Ta cũng giả sử đã tính sẵn bậc ra của mỗi đỉnh.

```cpp 
vector<vector<int>> adj_rev;

vector<bool> winning;
vector<bool> losing;
vector<bool> visited;
vector<int> degree;

void dfs(int v) {
    visited[v] = true;
    for (int u : adj_rev[v]) {
        if (!visited[u]) {
            if (losing[v])
                winning[u] = true;
            else if (--degree[u] == 0)
                losing[u] = true;
            else
                continue;
            dfs(u);
        }
    }
}
```

## Ví dụ: "Cảnh sát và kẻ trộm"

Đây là một ví dụ cụ thể của trò chơi trên.

Có một bàn cờ kích thước $m \times n$. Một số ô không thể đi vào. Biết tọa độ ban đầu của cảnh sát và kẻ trộm, và có một ô là lối thoát. Nếu tại bất kỳ thời điểm nào cảnh sát và kẻ trộm ở cùng ô, cảnh sát thắng. Nếu kẻ trộm ở ô lối thoát mà cảnh sát không cùng ở ô đó, kẻ trộm thắng. Cảnh sát có thể đi theo cả 8 hướng, còn kẻ trộm chỉ đi theo 4 hướng dọc các trục tọa độ. Hai người đi luân phiên, nhưng cũng có thể bỏ lượt nếu muốn. Cảnh sát đi trước.

Giờ ta sẽ **xây dựng đồ thị**. Để làm điều đó, ta cần hình thức hóa luật chơi. Trạng thái hiện tại được xác định bởi tọa độ cảnh sát $P$, tọa độ kẻ trộm $T$ và người đến lượt; gọi biến biểu thị người đến lượt là $P_{\text{turn}}$ (đúng khi đến lượt cảnh sát). Do đó mỗi đỉnh của đồ thị được xác định bởi bộ ba $(P, T, P_{\text{turn}})$. Sau đó có thể dễ dàng dựng đồ thị theo luật chơi.

Tiếp theo ta cần xác định những đỉnh thắng và thua ban đầu. Có một **điểm cần chú ý**: ngoài tọa độ, tính thắng/thua còn phụ thuộc vào $P_{\text{turn}}$, tức người đến lượt. Nếu đến lượt cảnh sát, đỉnh là thắng khi tọa độ cảnh sát và kẻ trộm trùng nhau; nếu không phải đỉnh thắng mà kẻ trộm ở lối thoát thì đó là đỉnh thua. Nếu đến lượt kẻ trộm, đỉnh là thua khi tọa độ hai người trùng nhau; nếu không phải đỉnh thua mà kẻ trộm ở lối thoát thì đó là đỉnh thắng.

Trước khi cài đặt, ta cần quyết định dựng đồ thị **tường minh** hay chỉ xây dựng **khi cần**. Dựng tường minh dễ hơn và ít có khả năng mắc lỗi hơn. Mặt khác, cách này làm tăng lượng mã và thời gian chạy so với dựng khi cần.

Phần cài đặt sau dựng đồ thị tường minh:

```cpp
struct State {
    int P, T;
    bool Pstep;
};

vector<State> adj_rev[100][100][2]; // [P][T][Pstep]
bool winning[100][100][2];
bool losing[100][100][2];
bool visited[100][100][2];
int degree[100][100][2];

void dfs(State v) {
    visited[v.P][v.T][v.Pstep] = true;
    for (State u : adj_rev[v.P][v.T][v.Pstep]) {
        if (!visited[u.P][u.T][u.Pstep]) {
            if (losing[v.P][v.T][v.Pstep])
                winning[u.P][u.T][u.Pstep] = true;
            else if (--degree[u.P][u.T][u.Pstep] == 0)
                losing[u.P][u.T][u.Pstep] = true;
            else
                continue;
            dfs(u);
        }
    }
}

int main() {
    int n, m;
    cin >> n >> m;
    vector<string> a(n);
    for (int i = 0; i < n; i++)
        cin >> a[i];

    for (int P = 0; P < n*m; P++) {
        for (int T = 0; T < n*m; T++) {
            for (int Pstep = 0; Pstep <= 1; Pstep++) {
                int Px = P/m, Py = P%m, Tx = T/m, Ty = T%m;
                if (a[Px][Py]=='*' || a[Tx][Ty]=='*')
                    continue;
                
                bool& win = winning[P][T][Pstep];
                bool& lose = losing[P][T][Pstep];
                if (Pstep) {
                    win = Px==Tx && Py==Ty;
                    lose = !win && a[Tx][Ty] == 'E';
                } else {
                    lose = Px==Tx && Py==Ty;
                    win = !lose && a[Tx][Ty] == 'E';
                }
                if (win || lose)
                    continue;

                State st = {P,T,!Pstep};
                adj_rev[P][T][Pstep].push_back(st);
                st.Pstep = Pstep;
                degree[P][T][Pstep]++;
                
                const int dx[] = {-1, 0, 1, 0, -1, -1, 1, 1};
                const int dy[] = {0, 1, 0, -1, -1, 1, -1, 1};
                for (int d = 0; d < (Pstep ? 8 : 4); d++) {
                    int PPx = Px, PPy = Py, TTx = Tx, TTy = Ty;
                    if (Pstep) {
                        PPx += dx[d];
                        PPy += dy[d];
                    } else {
                        TTx += dx[d];
                        TTy += dy[d];
                    }

                    if (PPx >= 0 && PPx < n && PPy >= 0 && PPy < m && a[PPx][PPy] != '*' &&
                        TTx >= 0 && TTx < n && TTy >= 0 && TTy < m && a[TTx][TTy] != '*')
                    {
                        adj_rev[PPx*m+PPy][TTx*m+TTy][!Pstep].push_back(st);
                        ++degree[P][T][Pstep];
                    }
                }
            }
        }
    }

    for (int P = 0; P < n*m; P++) {
        for (int T = 0; T < n*m; T++) {
            for (int Pstep = 0; Pstep <= 1; Pstep++) {
                if ((winning[P][T][Pstep] || losing[P][T][Pstep]) && !visited[P][T][Pstep])
                    dfs({P, T, (bool)Pstep});
            }
        }
    }

    int P_st, T_st;
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < m; j++) {
            if (a[i][j] == 'P')
                P_st = i*m+j;
            else if (a[i][j] == 'T')
                T_st = i*m+j;
        }
    }

    if (winning[P_st][T_st][true]) {
        cout << "Police catches the thief"  << endl;
    } else if (losing[P_st][T_st][true]) {
        cout << "The thief escapes" << endl;
    } else {
        cout << "Draw" << endl;
    }
}
```
