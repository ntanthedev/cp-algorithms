---
tags:
  - Translated
e_maxx_link: preflow_push_faster
translation:
  source: graph/push-relabel-faster.md
  source_commit: 24b9e0ce489a087b24788727cfcbc2bda5a642d1
  status: draft
  last_synced: 2026-11-16
---

# Luồng cực đại - Cải tiến phương pháp đẩy - nâng

Ta sẽ cải tiến [phương pháp đẩy - nâng](push-relabel.md) để đạt thời gian chạy tốt hơn.

## Mô tả

Cách cải tiến rất đơn giản:
Trong bài trước, ta chọn một đỉnh có lượng dư mà không theo quy tắc cụ thể nào.
Tuy nhiên, nếu luôn chọn các đỉnh có **độ cao lớn nhất** và thực hiện các phép đẩy và nâng trên chúng thì độ phức tạp sẽ tốt hơn.
Hơn nữa, để chọn các đỉnh có độ cao lớn nhất, thực ra ta không cần cấu trúc dữ liệu nào: chỉ cần lưu chúng vào một danh sách và tính lại danh sách khi đã xử lý hết các đỉnh trong đó (khi ấy những đỉnh vốn có độ cao thấp hơn sẽ được thêm vào danh sách), hoặc khi xuất hiện một đỉnh có lượng dư và độ cao lớn hơn (sau khi nâng một đỉnh).

Dù đơn giản, cải tiến này làm giảm đáng kể độ phức tạp.
Cụ thể, độ phức tạp của thuật toán thu được là $O(V E + V^2 \sqrt{E})$, trong trường hợp xấu nhất là $O(V^3)$.

Cải tiến này do Cheriyan và Maheshwari đề xuất năm 1989.

## Cài đặt

```{.cpp file=push_relabel_faster}
const int inf = 1000000000;

int n;
vector<vector<int>> capacity, flow;
vector<int> height, excess;

void push(int u, int v)
{
    int d = min(excess[u], capacity[u][v] - flow[u][v]);
    flow[u][v] += d;
    flow[v][u] -= d;
    excess[u] -= d;
    excess[v] += d;
}

void relabel(int u)
{
    int d = inf;
    for (int i = 0; i < n; i++) {
        if (capacity[u][i] - flow[u][i] > 0)
            d = min(d, height[i]);
    }
    if (d < inf)
        height[u] = d + 1;
}

vector<int> find_max_height_vertices(int s, int t) {
    vector<int> max_height;
    for (int i = 0; i < n; i++) {
        if (i != s && i != t && excess[i] > 0) {
            if (!max_height.empty() && height[i] > height[max_height[0]])
                max_height.clear();
            if (max_height.empty() || height[i] == height[max_height[0]])
                max_height.push_back(i);
        }
    }
    return max_height;
}

int max_flow(int s, int t)
{
    height.assign(n, 0);
    height[s] = n;
    flow.assign(n, vector<int>(n, 0));
    excess.assign(n, 0);
    excess[s] = inf;
    for (int i = 0; i < n; i++) {
        if (i != s)
            push(s, i);
    }

    vector<int> current;
    while (!(current = find_max_height_vertices(s, t)).empty()) {
        for (int i : current) {
            bool pushed = false;
            for (int j = 0; j < n && excess[i]; j++) {
                if (capacity[i][j] - flow[i][j] > 0 && height[i] == height[j] + 1) {
                    push(i, j);
                    pushed = true;
                }
            }
            if (!pushed) {
                relabel(i);
                break;
            }
        }
    }

    return excess[t];
}
```
