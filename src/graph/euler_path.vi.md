---
title: Finding the Eulerian path in O(M)
tags:
  - Translated
e_maxx_link: euler_path
translation:
  source: graph/euler_path.md
  source_commit: e7b256576411f560daa049ea933b177231b01035
  status: draft
  last_synced: 2026-08-08
---
# Tìm đường đi Euler trong $O(M)$

**Đường đi Euler** là một đường đi trong đồ thị đi qua mọi cạnh đúng một lần.
**Chu trình Euler** là một đường đi Euler đồng thời là một chu trình.

Bài toán ở đây là tìm đường đi Euler trong một **đa đồ thị vô hướng có cạnh khuyên**.

## Thuật toán

Trước hết, ta có thể kiểm tra đường đi Euler có tồn tại hay không.
Ta dùng định lý sau. Chu trình Euler tồn tại khi và chỉ khi bậc của mọi đỉnh đều chẵn.
Còn đường đi Euler tồn tại khi và chỉ khi số đỉnh có bậc lẻ bằng hai (hoặc bằng không, trong trường hợp tồn tại chu trình Euler).
Ngoài ra, hiển nhiên đồ thị phải đủ liên thông (tức sau khi loại bỏ mọi đỉnh cô lập, phần còn lại phải là một đồ thị liên thông).

Để tìm đường đi Euler / chu trình Euler, ta có thể dùng chiến lược sau:
Ta tìm tất cả các chu trình đơn rồi ghép chúng lại thành một chu trình duy nhất — đó sẽ là chu trình Euler.
Nếu đồ thị chỉ có đường đi Euler mà không có chu trình Euler, hãy thêm cạnh còn thiếu, tìm chu trình Euler rồi loại cạnh thêm vào khỏi kết quả.

Việc tìm tất cả các chu trình và ghép chúng có thể thực hiện bằng một thủ tục đệ quy đơn giản:

```nohighlight
procedure FindEulerPath(V)
  1. iterate through all the edges outgoing from vertex V;
       remove this edge from the graph,
       and call FindEulerPath from the second end of this edge;
  2. add vertex V to the answer.
```

Độ phức tạp của thuật toán này hiển nhiên là tuyến tính theo số cạnh.

Ta cũng có thể viết cùng thuật toán dưới dạng không đệ quy:

```nohighlight
stack St;
put start vertex in St;
until St is empty
  let V be the value at the top of St;
  if degree(V) = 0, then
    add V to the answer;
    remove V from the top of St;
  otherwise
    find any edge coming out of V;
    remove it from the graph;
    put the second end of this edge in St;
```

Dễ dàng kiểm tra hai dạng trên là tương đương. Tuy nhiên, dạng thứ hai rõ ràng nhanh hơn trong thực tế và mã cài đặt cũng hiệu quả hơn.

## Bài toán Domino

Sau đây là một bài toán kinh điển về chu trình Euler — bài toán Domino.

Có $N$ quân domino. Như thường thấy, trên hai đầu của mỗi quân domino có ghi hai số (thông thường từ 1 đến 6, nhưng trong bài toán này điều đó không quan trọng). Ta muốn xếp tất cả quân domino thành một hàng sao cho với mọi hai quân kề nhau, hai số nằm ở phía tiếp giáp của chúng bằng nhau. Được phép lật các quân domino.

Ta phát biểu lại bài toán. Xem các số xuất hiện trên domino là các đỉnh của đồ thị, còn các quân domino là các cạnh của đồ thị (mỗi quân domino mang hai số $(a,b)$ tương ứng với các cạnh $(a,b)$ và $(b, a)$). Khi đó, bài toán được quy về tìm đường đi Euler trong đồ thị này.

## Cài đặt

Chương trình dưới đây tìm và in ra một chu trình Euler hoặc đường đi Euler trong đồ thị, hoặc in $-1$ nếu không tồn tại.

Trước hết, chương trình kiểm tra bậc các đỉnh: nếu không có đỉnh bậc lẻ thì đồ thị có chu trình Euler; nếu có $2$ đỉnh bậc lẻ thì đồ thị chỉ có đường đi Euler (không có chu trình Euler); nếu có nhiều hơn $2$ đỉnh như vậy thì không tồn tại chu trình Euler hay đường đi Euler.
Để tìm đường đi Euler không phải chu trình, làm như sau: nếu $V1$ và $V2$ là hai đỉnh có bậc lẻ, chỉ cần thêm cạnh $(V1, V2)$; trong đồ thị thu được ta tìm chu trình Euler (chu trình này hiển nhiên tồn tại), rồi loại cạnh "giả" $(V1, V2)$ khỏi đáp án.
Ta tìm chu trình Euler đúng như mô tả ở trên (phiên bản không đệ quy), đồng thời khi thuật toán kết thúc sẽ kiểm tra đồ thị có liên thông hay không (nếu đồ thị không liên thông thì một số cạnh vẫn còn lại, và khi đó cần in $-1$).
Cuối cùng, chương trình cũng xét trường hợp đồ thị có các đỉnh cô lập.

**Ghi chú bản dịch:** Trong snippet nguồn, biến n được khai báo rồi dùng ngay để tạo ma trận kề trước khi có bước đọc hoặc khởi tạo giá trị của n. Bản dịch giữ nguyên code theo policy; lỗi cài đặt này được tách để đề xuất sửa upstream.

Lưu ý rằng cài đặt này dùng ma trận kề.
Ngoài ra, cách cài đặt này tìm đỉnh tiếp theo bằng vét cạn, nên phải duyệt đi duyệt lại toàn bộ một hàng của ma trận.
Một cách tốt hơn là lưu đồ thị bằng danh sách kề, xóa cạnh trong $O(1)$ và đánh dấu các cạnh ngược trong một danh sách riêng.
Bằng cách đó, ta có thể đạt một thuật toán $O(N)$.

**Ghi chú bản dịch:** Ở câu trên, nguồn dùng $O(N)$ dù toàn bộ đoạn đang phân tích độ phức tạp theo số cạnh và mục tiêu của bài là tuyến tính theo số cạnh. Với ký hiệu của bài, bound phù hợp phải là $O(M)$ (hoặc $O(V+E)$ nếu viết theo số đỉnh và cạnh). Bản dịch giữ wording nguồn và tách correction này để đề xuất sửa upstream.

```cpp
int main() {
    int n;
    vector<vector<int>> g(n, vector<int>(n));
    // reading the graph in the adjacency matrix

    vector<int> deg(n);
    for (int i = 0; i < n; ++i) {
        for (int j = 0; j < n; ++j)
            deg[i] += g[i][j];
    }

    int first = 0;
    while (first < n && !deg[first])
        ++first;
    if (first == n) {
        cout << -1;
        return 0;
    }

    int v1 = -1, v2 = -1;
    bool bad = false;
    for (int i = 0; i < n; ++i) {
        if (deg[i] & 1) {
            if (v1 == -1)
                v1 = i;
            else if (v2 == -1)
                v2 = i;
            else
                bad = true;
        }
    }

    if (v1 != -1)
        ++g[v1][v2], ++g[v2][v1];

    stack<int> st;
    st.push(first);
    vector<int> res;
    while (!st.empty()) {
        int v = st.top();
        int i;
        for (i = 0; i < n; ++i)
            if (g[v][i])
                break;
        if (i == n) {
            res.push_back(v);
            st.pop();
        } else {
            --g[v][i];
            --g[i][v];
            st.push(i);
        }
    }

    if (v1 != -1) {
        for (size_t i = 0; i + 1 < res.size(); ++i) {
            if ((res[i] == v1 && res[i + 1] == v2) ||
                (res[i] == v2 && res[i + 1] == v1)) {
                vector<int> res2;
                for (size_t j = i + 1; j < res.size(); ++j)
                    res2.push_back(res[j]);
                for (size_t j = 1; j <= i; ++j)
                    res2.push_back(res[j]);
                res = res2;
                break;
            }
        }
    }

    for (int i = 0; i < n; ++i) {
        for (int j = 0; j < n; ++j) {
            if (g[i][j])
                bad = true;
        }
    }

    if (bad) {
        cout << -1;
    } else {
        for (int x : res)
            cout << x << " ";
    }
}
```
### Bài tập luyện tập:

- [CSES : Mail Delivery](https://cses.fi/problemset/task/1691)
- [CSES : Teleporters Path](https://cses.fi/problemset/task/1693)
- [Codeforces - Melody](https://codeforces.com/contest/2110/problem/E)
- [Codeforces - Tanya and Password](https://codeforces.com/contest/508/problem/D)
