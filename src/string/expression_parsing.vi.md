---
tags:
  - Translated
e_maxx_link: expressions_parsing
translation:
  source: string/expression_parsing.md
  source_commit: 6014535bc25b1d84823dbaab855622b2f3a823fc
  status: draft
  last_synced: 2026-11-16
---

# Phân tích biểu thức

Cho một chuỗi chứa biểu thức toán học gồm các số và nhiều toán tử.
Ta cần tính giá trị của biểu thức trong $O(n)$, với $n$ là độ dài chuỗi.

Thuật toán ở đây chuyển biểu thức sang **ký pháp Ba Lan ngược** (một cách tường minh hoặc ngầm định), rồi tính giá trị của biểu thức.

## Ký pháp Ba Lan ngược

Ký pháp Ba Lan ngược là cách viết biểu thức toán học trong đó các toán tử đứng sau các toán hạng của chúng.
Ví dụ, biểu thức sau

$$a + b * c * d + (e - f) * (g * h + i)$$

có thể được viết bằng ký pháp Ba Lan ngược như sau:

$$a b c * d * + e f - g h * i + * +$$

Ký pháp Ba Lan ngược được nhà triết học và chuyên gia khoa học máy tính người Úc Charles Hamblin phát triển vào giữa thập niên 1950, dựa trên ký pháp Ba Lan do nhà toán học người Ba Lan Jan Łukasiewicz đề xuất năm 1920.

Điểm thuận tiện của ký pháp Ba Lan ngược là các biểu thức dạng này rất **dễ tính giá trị** trong thời gian tuyến tính.
Ta dùng một ngăn xếp, ban đầu rỗng.
Ta duyệt các toán hạng và toán tử của biểu thức theo ký pháp Ba Lan ngược.
Nếu phần tử hiện tại là số, ta đưa giá trị đó lên đỉnh ngăn xếp; nếu là toán tử, ta lấy hai phần tử trên cùng ra, thực hiện phép toán và đưa kết quả trở lại đỉnh ngăn xếp.
Cuối cùng, ngăn xếp còn đúng một phần tử, chính là giá trị của biểu thức.

Hiển nhiên cách tính đơn giản này chạy trong thời gian $O(n)$.

## Phân tích biểu thức đơn giản

Trước hết, ta chỉ xét một bài toán đơn giản hơn:
giả sử mọi toán tử đều là **hai ngôi** (tức là nhận hai đối số) và đều **kết hợp trái** (nếu cùng độ ưu tiên thì được thực hiện từ trái sang phải).
Biểu thức được phép có dấu ngoặc.

Ta tạo hai ngăn xếp: một cho các số, một cho các toán tử và dấu ngoặc.
Ban đầu cả hai đều rỗng.
Với ngăn xếp thứ hai, ta duy trì điều kiện các phép toán được sắp theo độ ưu tiên giảm nghiêm ngặt.
Nếu có dấu ngoặc trong ngăn xếp thì mỗi khối toán tử (tương ứng với một cặp ngoặc) được sắp thứ tự, nhưng toàn bộ ngăn xếp không nhất thiết được sắp.

Ta duyệt các ký tự của biểu thức từ trái sang phải.
Nếu ký tự hiện tại là chữ số, ta đưa giá trị của số đó vào ngăn xếp.
Nếu ký tự hiện tại là dấu ngoặc mở, ta đưa nó vào ngăn xếp.
Nếu ký tự hiện tại là dấu ngoặc đóng, ta thực hiện các toán tử trong ngăn xếp cho tới khi gặp dấu ngoặc mở (nói cách khác là thực hiện mọi phép toán bên trong cặp ngoặc).
Cuối cùng, nếu ký tự hiện tại là một toán tử, ta thực hiện các toán tử ở đỉnh ngăn xếp chừng nào chúng có độ ưu tiên bằng hoặc cao hơn, rồi đưa toán tử mới vào ngăn xếp.

Sau khi duyệt hết chuỗi, một số toán tử vẫn có thể còn trong ngăn xếp, nên ta thực hiện chúng.

Dưới đây là cài đặt phương pháp này với bốn toán tử $+$ $-$ $*$ $/$:

```{.cpp file=expression_parsing_simple}
bool delim(char c) {
    return c == ' ';
}

bool is_op(char c) {
    return c == '+' || c == '-' || c == '*' || c == '/';
}

int priority (char op) {
    if (op == '+' || op == '-')
        return 1;
    if (op == '*' || op == '/')
        return 2;
    return -1;
}

void process_op(stack<int>& st, char op) {
    int r = st.top(); st.pop();
    int l = st.top(); st.pop();
    switch (op) {
        case '+': st.push(l + r); break;
        case '-': st.push(l - r); break;
        case '*': st.push(l * r); break;
        case '/': st.push(l / r); break;
    }
}

int evaluate(string& s) {
    stack<int> st;
    stack<char> op;
    for (int i = 0; i < (int)s.size(); i++) {
        if (delim(s[i]))
            continue;
        
        if (s[i] == '(') {
            op.push('(');
        } else if (s[i] == ')') {
            while (op.top() != '(') {
                process_op(st, op.top());
                op.pop();
            }
            op.pop();
        } else if (is_op(s[i])) {
            char cur_op = s[i];
            while (!op.empty() && priority(op.top()) >= priority(cur_op)) {
                process_op(st, op.top());
                op.pop();
            }
            op.push(cur_op);
        } else {
            int number = 0;
            while (i < (int)s.size() && isalnum(s[i]))
                number = number * 10 + s[i++] - '0';
            --i;
            st.push(number);
        }
    }

    while (!op.empty()) {
        process_op(st, op.top());
        op.pop();
    }
    return st.top();
}
```

Như vậy, ta đã biết cách tính giá trị biểu thức trong $O(n)$, đồng thời sử dụng ngầm ký pháp Ba Lan ngược.
Bằng cách sửa đôi chút cài đặt trên, ta cũng có thể thu được biểu thức dưới dạng ký pháp Ba Lan ngược một cách tường minh.

## Toán tử một ngôi

Bây giờ giả sử biểu thức còn chứa các toán tử **một ngôi** (toán tử nhận một đối số).
Dấu cộng và dấu trừ một ngôi là những ví dụ thường gặp.

Một khác biệt trong trường hợp này là ta phải xác định toán tử hiện tại là một ngôi hay hai ngôi.

Ta có thể nhận thấy trước một toán tử một ngôi luôn là một toán tử khác, một dấu ngoặc mở, hoặc không có gì (nếu nó ở ngay đầu biểu thức).
Ngược lại, trước một toán tử hai ngôi luôn là một toán hạng (số) hoặc dấu ngoặc đóng.
Vì vậy, ta dễ dàng đánh dấu liệu toán tử tiếp theo có thể là một ngôi hay không.

Ngoài ra, ta phải thực hiện toán tử một ngôi và hai ngôi theo cách khác nhau.
Ta cũng phải chọn độ ưu tiên của toán tử một ngôi cao hơn mọi toán tử hai ngôi.

Cần lưu ý rằng một số toán tử một ngôi (chẳng hạn dấu cộng và dấu trừ một ngôi) thực ra **kết hợp phải**.

## Tính kết hợp phải

Kết hợp phải nghĩa là khi độ ưu tiên bằng nhau, các toán tử phải được tính từ phải sang trái.

Như đã nói ở trên, các toán tử một ngôi thường kết hợp phải.
Một ví dụ khác là toán tử lũy thừa ($a \wedge b \wedge c$ thường được hiểu là $a^{b^c}$ chứ không phải $(a^b)^c$).

Ta cần thay đổi gì để xử lý đúng toán tử kết hợp phải?
Hóa ra chỉ cần thay đổi rất ít.
Điểm khác biệt duy nhất là khi độ ưu tiên bằng nhau, ta sẽ trì hoãn thực hiện toán tử kết hợp phải.

Dòng duy nhất cần thay là
```cpp
while (!op.empty() && priority(op.top()) >= priority(cur_op))
```
bằng
```cpp
while (!op.empty() && (
        (left_assoc(cur_op) && priority(op.top()) >= priority(cur_op)) ||
        (!left_assoc(cur_op) && priority(op.top()) > priority(cur_op))
    ))
```
trong đó `left_assoc` là hàm quyết định một toán tử có kết hợp trái hay không.

Dưới đây là một cài đặt cho các toán tử hai ngôi $+$ $-$ $*$ $/$ và các toán tử một ngôi $+$ và $-$.

**Ghi chú bản dịch:** Cài đặt dưới đây dùng giá trị âm của kiểu char để đánh dấu toán tử một ngôi. Nó phụ thuộc vào việc char có dấu; nếu char mặc định không dấu, cách nhận biết này không hoạt động đúng.

```{.cpp file=expression_parsing_unary}
bool delim(char c) {
    return c == ' ';
}

bool is_op(char c) {
    return c == '+' || c == '-' || c == '*' || c == '/';
}

bool is_unary(char c) {
    return c == '+' || c=='-';
}

int priority (char op) {
    if (op < 0) // unary operator
        return 3;
    if (op == '+' || op == '-')
        return 1;
    if (op == '*' || op == '/')
        return 2;
    return -1;
}

void process_op(stack<int>& st, char op) {
    if (op < 0) {
        int l = st.top(); st.pop();
        switch (-op) {
            case '+': st.push(l); break;
            case '-': st.push(-l); break;
        }
    } else {
        int r = st.top(); st.pop();
        int l = st.top(); st.pop();
        switch (op) {
            case '+': st.push(l + r); break;
            case '-': st.push(l - r); break;
            case '*': st.push(l * r); break;
            case '/': st.push(l / r); break;
        }
    }
}

int evaluate(string& s) {
    stack<int> st;
    stack<char> op;
    bool may_be_unary = true;
    for (int i = 0; i < (int)s.size(); i++) {
        if (delim(s[i]))
            continue;
        
        if (s[i] == '(') {
            op.push('(');
            may_be_unary = true;
        } else if (s[i] == ')') {
            while (op.top() != '(') {
                process_op(st, op.top());
                op.pop();
            }
            op.pop();
            may_be_unary = false;
        } else if (is_op(s[i])) {
            char cur_op = s[i];
            if (may_be_unary && is_unary(cur_op))
                cur_op = -cur_op;
            while (!op.empty() && (
                    (cur_op >= 0 && priority(op.top()) >= priority(cur_op)) ||
                    (cur_op < 0 && priority(op.top()) > priority(cur_op))
                )) {
                process_op(st, op.top());
                op.pop();
            }
            op.push(cur_op);
            may_be_unary = true;
        } else {
            int number = 0;
            while (i < (int)s.size() && isalnum(s[i]))
                number = number * 10 + s[i++] - '0';
            --i;
            st.push(number);
            may_be_unary = false;
        }
    }

    while (!op.empty()) {
        process_op(st, op.top());
        op.pop();
    }
    return st.top();
}
```
