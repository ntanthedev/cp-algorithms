---
tags:
  - Translated
e_maxx_link: stacks_for_minima
translation:
  source: data_structures/stack_queue_modification.md
  source_commit: 6374e56efe1523f6754baadfc892522f711849cf
  status: draft
  last_synced: 2026-11-16
---

# Ngăn xếp tìm cực tiểu / Hàng đợi tìm cực tiểu

Trong bài này ta xét ba bài toán:
trước hết biến đổi một ngăn xếp để tìm được phần tử nhỏ nhất trong $O(1)$, sau đó làm tương tự với hàng đợi, và cuối cùng dùng các cấu trúc này để tìm giá trị nhỏ nhất của mọi đoạn con có độ dài cố định trong một mảng trong $O(n)$.

## Biến đổi ngăn xếp

Ta muốn biến đổi cấu trúc ngăn xếp sao cho có thể tìm phần tử nhỏ nhất trong ngăn xếp trong thời gian $O(1)$, đồng thời giữ nguyên độ phức tạp tiệm cận của việc thêm và xóa phần tử.
Nhắc lại rằng với ngăn xếp, ta chỉ thêm và xóa phần tử ở một đầu.

Để làm vậy, ta không chỉ lưu các phần tử trong ngăn xếp, mà lưu chúng thành từng cặp: bản thân phần tử và giá trị nhỏ nhất trong ngăn xếp tính từ phần tử đó trở xuống.

```cpp
stack<pair<int, int>> st;
```

Rõ ràng việc tìm giá trị nhỏ nhất trong toàn bộ ngăn xếp chỉ cần xem giá trị `stack.top().second`.

Việc thêm hoặc xóa một phần tử trong ngăn xếp cũng hiển nhiên có thể thực hiện trong thời gian hằng số.

Cài đặt:

* Thêm phần tử:
```cpp
int new_min = st.empty() ? new_elem : min(new_elem, st.top().second);
st.push({new_elem, new_min});
```

* Xóa phần tử:
```cpp
int removed_element = st.top().first;
st.pop();
```

* Tìm giá trị nhỏ nhất:
```cpp
int minimum = st.top().second;
```

## Biến đổi hàng đợi (cách 1)

Bây giờ ta muốn thực hiện các thao tác tương tự với hàng đợi, tức là thêm phần tử vào cuối và xóa chúng ở đầu.

Ta xét một cách đơn giản để biến đổi hàng đợi.
Tuy nhiên, cách này có nhược điểm lớn là hàng đợi đã biến đổi thực tế sẽ không lưu tất cả các phần tử.

Ý tưởng chính là chỉ lưu các phần tử cần thiết để xác định giá trị nhỏ nhất trong hàng đợi.
Cụ thể, ta giữ các phần tử theo thứ tự không giảm (tức là giá trị nhỏ nhất nằm ở đầu), và dĩ nhiên không phải theo cách tùy ý: giá trị nhỏ nhất thực sự phải luôn được giữ trong hàng đợi.
Nhờ đó phần tử nhỏ nhất luôn ở đầu hàng đợi.
Trước khi thêm phần tử mới, chỉ cần thực hiện một phép “cắt”:
ta xóa mọi phần tử ở cuối hàng đợi lớn hơn phần tử mới, rồi thêm phần tử mới vào hàng đợi.
Làm vậy không phá vỡ thứ tự, đồng thời không làm mất phần tử hiện tại nếu nó trở thành giá trị nhỏ nhất ở một bước sau đó.
Những phần tử đã xóa không bao giờ có thể là giá trị nhỏ nhất, nên thao tác này được phép.
Khi muốn lấy một phần tử ở đầu, phần tử đó có thể không còn trong hàng đợi (vì trước đó ta đã xóa nó khi thêm một phần tử nhỏ hơn).
Vì vậy khi xóa một phần tử khỏi hàng đợi, ta cần biết giá trị của phần tử đó.
Nếu đầu hàng đợi có cùng giá trị, ta có thể xóa nó; nếu không thì không làm gì.

Xét cách cài đặt các thao tác trên:

```cpp
deque<int> q;
```

* Tìm giá trị nhỏ nhất:
```cpp
int minimum = q.front();
```

* Thêm phần tử:
```cpp
while (!q.empty() && q.back() > new_element)
    q.pop_back();
q.push_back(new_element);
```

* Xóa phần tử:
```cpp
if (!q.empty() && q.front() == remove_element)
    q.pop_front();
```

Rõ ràng trung bình tất cả các thao tác này chỉ mất $O(1)$ thời gian (vì mỗi phần tử chỉ có thể được thêm và lấy ra một lần).

## Biến đổi hàng đợi (cách 2)

Đây là một biến thể của cách 1.
Ta muốn có thể xóa phần tử mà không cần biết phần tử phải xóa là gì.
Ta có thể làm điều đó bằng cách lưu chỉ số của từng phần tử trong hàng đợi.
Ta cũng ghi nhớ số phần tử đã thêm và đã xóa.

```cpp
deque<pair<int, int>> q;
int cnt_added = 0;
int cnt_removed = 0;
```

* Tìm giá trị nhỏ nhất:
```cpp
int minimum = q.front().first;
```

* Thêm phần tử:
```cpp
while (!q.empty() && q.back().first > new_element)
    q.pop_back();
q.push_back({new_element, cnt_added});
cnt_added++;
```

* Xóa phần tử:
```cpp
if (!q.empty() && q.front().second == cnt_removed) 
    q.pop_front();
cnt_removed++;
```

## Biến đổi hàng đợi (cách 3)

Ở đây ta xét một cách khác để biến đổi hàng đợi nhằm tìm giá trị nhỏ nhất trong $O(1)$.
Cách này phức tạp hơn một chút khi cài đặt, nhưng lần này ta thực sự lưu tất cả phần tử.
Ta cũng có thể xóa phần tử ở đầu mà không cần biết giá trị của nó.

Ý tưởng là đưa bài toán về bài toán ngăn xếp đã giải ở trên.
Vì vậy ta chỉ cần tìm hiểu cách mô phỏng hàng đợi bằng hai ngăn xếp.

Ta tạo hai ngăn xếp `s1` và `s2`.
Tất nhiên chúng có dạng ngăn xếp đã biến đổi để tìm giá trị nhỏ nhất trong $O(1)$.
Ta thêm phần tử mới vào ngăn xếp `s1` và xóa phần tử khỏi ngăn xếp `s2`.
Nếu tại thời điểm nào đó `s2` rỗng, ta chuyển tất cả phần tử từ `s1` sang `s2` (thao tác này về cơ bản đảo ngược thứ tự của chúng).
Cuối cùng, tìm giá trị nhỏ nhất trong hàng đợi chỉ cần tìm giá trị nhỏ nhất của hai ngăn xếp.

Như vậy ta thực hiện mọi thao tác trong thời gian trung bình $O(1)$ (mỗi phần tử được thêm vào ngăn xếp `s1` một lần, chuyển sang `s2` một lần và lấy ra khỏi `s2` một lần).

Cài đặt:

```cpp
stack<pair<int, int>> s1, s2;
```

* Tìm giá trị nhỏ nhất:
```cpp
if (s1.empty() || s2.empty()) 
    minimum = s1.empty() ? s2.top().second : s1.top().second;
else
    minimum = min(s1.top().second, s2.top().second);
```

* Thêm phần tử:
```cpp
int minimum = s1.empty() ? new_element : min(new_element, s1.top().second);
s1.push({new_element, minimum});
```

* Xóa phần tử:
```cpp
if (s2.empty()) {
    while (!s1.empty()) {
        int element = s1.top().first;
        s1.pop();
        int minimum = s2.empty() ? element : min(element, s2.top().second);
        s2.push({element, minimum});
    }
}
int remove_element = s2.top().first;
s2.pop();
```

## Tìm giá trị nhỏ nhất của mọi đoạn con có độ dài cố định

Giả sử ta có mảng $A$ độ dài $N$ và một giá trị $M \le N$.
Ta cần tìm giá trị nhỏ nhất của mỗi đoạn con độ dài $M$ trong mảng, tức là cần tìm:

$$\min_{0 \le i \le M-1} A[i], \min_{1 \le i \le M} A[i], \min_{2 \le i \le M+1} A[i],~\dots~, \min_{N-M \le i \le N-1} A[i]$$

Ta phải giải bài toán này trong thời gian tuyến tính, tức là $O(n)$.

Ta có thể dùng bất kỳ hàng đợi biến đổi nào trong ba cách trên để giải bài toán.
Cách giải khá rõ ràng:
ta thêm $M$ phần tử đầu tiên của mảng, tìm và xuất giá trị nhỏ nhất, rồi thêm phần tử tiếp theo vào hàng đợi và xóa phần tử đầu tiên của mảng, tìm và xuất giá trị nhỏ nhất, v.v.
Vì mọi thao tác với hàng đợi có thời gian trung bình hằng số nên độ phức tạp của toàn bộ thuật toán là $O(n)$.

## Bài tập
* [Queries with Fixed Length](https://www.hackerrank.com/challenges/queries-with-fixed-length/problem)
* [Sliding Window Minimum](https://cses.fi/problemset/task/3221)
* [Binary Land](https://www.codechef.com/MAY20A/problems/BINLAND)
