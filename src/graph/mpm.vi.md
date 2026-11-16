---
tags:
  - Original
translation:
  source: graph/mpm.md
  source_commit: 2d7c8ba7e725edfc29e5fa455725e049b1608fd9
  status: draft
  last_synced: 2026-11-16
---

# Luồng cực đại - Thuật toán MPM

Thuật toán MPM (Malhotra, Pramodh-Kumar và Maheshwari) giải bài toán luồng cực đại trong $O(V^3)$. Thuật toán này tương tự [thuật toán Dinic](dinic.md).

## Thuật toán

Giống thuật toán Dinic, MPM chạy theo từng pha; trong mỗi pha ta tìm luồng chặn trong mạng phân lớp của mạng dư của $G$. Khác biệt chính so với Dinic là cách tìm luồng chặn. Xét mạng phân lớp $L$. Với mỗi đỉnh, ta định nghĩa _thế vào_ và _thế ra_ như sau:

$$\begin{align}
p_{in}(v) &= \sum\limits_{(u, v)\in L}(c(u, v) - f(u, v)) \\\\
p_{out}(v) &= \sum\limits_{(v, u)\in L}(c(v, u) - f(v, u))
\end{align}$$

Ta cũng đặt $p_{in}(s) = p_{out}(t) = \infty$. Từ $p_{in}$ và $p_{out}$, định nghĩa _thế_ là $p(v) = min(p_{in}(v), p_{out}(v))$. Gọi đỉnh $r$ là _đỉnh tham chiếu_ nếu $p(r) = min\{p(v)\}$. Xét một đỉnh tham chiếu $r$. Ta khẳng định có thể tăng luồng thêm $p(r)$ sao cho $p(r)$ trở thành $0$.

Điều này đúng vì $L$ không có chu trình: ta có thể đẩy luồng ra khỏi $r$ theo các cạnh đi ra và luồng sẽ đến $t$, vì mỗi đỉnh có đủ thế ra để đẩy lượng luồng đến nó đi tiếp. Tương tự, ta có thể kéo luồng từ $s$. Cách dựng luồng chặn dựa trên tính chất này. Ở mỗi vòng lặp, ta tìm một đỉnh tham chiếu và đẩy luồng từ $s$ đến $t$ qua $r$.

Có thể mô phỏng quá trình bằng BFS. Mọi cung đã bão hòa hoàn toàn có thể bị xóa khỏi $L$ vì chúng sẽ không được dùng lại trong pha này. Tương tự, mọi đỉnh khác $s$ và $t$ không có cung đi ra hoặc không có cung đi vào đều có thể bị xóa.

Mỗi pha chạy trong $O(V^2)$ vì có nhiều nhất $V$ vòng lặp (ít nhất đỉnh tham chiếu được chọn bị xóa), và ở mỗi vòng ta xóa mọi cạnh đã đi qua trừ nhiều nhất $V$ cạnh. Cộng lại được $O(V^2 + E) = O(V^2)$. Vì có ít hơn $V$ pha (xem chứng minh [tại đây](dinic.md)), tổng thời gian của MPM là $O(V^3)$.

Ghi chú bản dịch: Bước rút gọn độ phức tạp ở trên dùng giả thiết số cạnh được chặn bởi bình phương số đỉnh; với đa đồ thị có số cạnh song song không bị chặn, cần giữ số hạng phụ thuộc vào số cạnh.

## Cài đặt

```{.cpp file=mpm}
struct MPM{
    struct FlowEdge{
        int v, u;
        long long cap, flow;
        FlowEdge(){}
        FlowEdge(int _v, int _u, long long _cap, long long _flow)
            : v(_v), u(_u), cap(_cap), flow(_flow){}
        FlowEdge(int _v, int _u, long long _cap)
            : v(_v), u(_u), cap(_cap), flow(0ll){}
    };
    const long long flow_inf = 1e18;
    vector<FlowEdge> edges;
    vector<char> alive;
    vector<long long> pin, pout;
    vector<list<int> > in, out;
    vector<vector<int> > adj;
    vector<long long> ex;
    int n, m = 0;
    int s, t;
    vector<int> level;
    vector<int> q;
    int qh, qt;
    void resize(int _n){
        n = _n;
        ex.resize(n);
        q.resize(n);
        pin.resize(n);
        pout.resize(n);
        adj.resize(n);
        level.resize(n);
        in.resize(n);
        out.resize(n);
    }
    MPM(){}
    MPM(int _n, int _s, int _t){resize(_n); s = _s; t = _t;}
    void add_edge(int v, int u, long long cap){
        edges.push_back(FlowEdge(v, u, cap));
        edges.push_back(FlowEdge(u, v, 0));
        adj[v].push_back(m);
        adj[u].push_back(m + 1);
        m += 2;
    }
    bool bfs(){
        while(qh < qt){
            int v = q[qh++];
            for(int id : adj[v]){
                if(edges[id].cap - edges[id].flow < 1)continue;
                if(level[edges[id].u] != -1)continue;
                level[edges[id].u] = level[v] + 1;
                q[qt++] = edges[id].u;
            }
        }
        return level[t] != -1;
    }
    long long pot(int v){
        return min(pin[v], pout[v]);
    }
    void remove_node(int v){
        for(int i : in[v]){
            int u = edges[i].v;
            auto it = find(out[u].begin(), out[u].end(), i);
            out[u].erase(it);
            pout[u] -= edges[i].cap - edges[i].flow;
        }
        for(int i : out[v]){
            int u = edges[i].u;
            auto it = find(in[u].begin(), in[u].end(), i);
            in[u].erase(it);
            pin[u] -= edges[i].cap - edges[i].flow;
        }
    }
    void push(int from, int to, long long f, bool forw){
        qh = qt = 0;
        ex.assign(n, 0);
        ex[from] = f;
        q[qt++] = from;
        while(qh < qt){
            int v = q[qh++];
            if(v == to)
                break;
            long long must = ex[v];
            auto it = forw ? out[v].begin() : in[v].begin();
            while(true){
                int u = forw ? edges[*it].u : edges[*it].v;
                long long pushed = min(must, edges[*it].cap - edges[*it].flow);
                if(pushed == 0)break;
                if(forw){
                    pout[v] -= pushed;
                    pin[u] -= pushed;
                }
                else{
                    pin[v] -= pushed;
                    pout[u] -= pushed;
                }
                if(ex[u] == 0)
                    q[qt++] = u;
                ex[u] += pushed;
                edges[*it].flow += pushed;
                edges[(*it)^1].flow -= pushed;
                must -= pushed;
                if(edges[*it].cap - edges[*it].flow == 0){
                    auto jt = it;
                    ++jt;
                    if(forw){
                        in[u].erase(find(in[u].begin(), in[u].end(), *it));
                        out[v].erase(it);
                    }
                    else{
                        out[u].erase(find(out[u].begin(), out[u].end(), *it));
                        in[v].erase(it);
                    }
                    it = jt;
                }
                else break;
                if(!must)break;
            }
        }
    }
    long long flow(){
        long long ans = 0;
        while(true){
            pin.assign(n, 0);
            pout.assign(n, 0);
            level.assign(n, -1);
            alive.assign(n, true);
            level[s] = 0;
            qh = 0; qt = 1;
            q[0] = s;
            if(!bfs())
                break;
            for(int i = 0; i < n; i++){
                out[i].clear();
                in[i].clear();
            }
            for(int i = 0; i < m; i++){
                if(edges[i].cap - edges[i].flow == 0)
                    continue;
                int v = edges[i].v, u = edges[i].u;
                if(level[v] + 1 == level[u] && (level[u] < level[t] || u == t)){
                    in[u].push_back(i);
                    out[v].push_back(i);
                    pin[u] += edges[i].cap - edges[i].flow;
                    pout[v] += edges[i].cap - edges[i].flow;
                }
            }
            pin[s] = pout[t] = flow_inf;
            while(true){
                int v = -1;
                for(int i = 0; i < n; i++){
                    if(!alive[i])continue;
                    if(v == -1 || pot(i) < pot(v))
                        v = i;
                }
                if(v == -1)
                    break;
                if(pot(v) == 0){
                    alive[v] = false;
                    remove_node(v);
                    continue;
                }
                long long f = pot(v);
                ans += f;
                push(v, s, f, false);
                push(v, t, f, true);
                alive[v] = false;
                remove_node(v);
            }
        }
        return ans;
    }
};
```
