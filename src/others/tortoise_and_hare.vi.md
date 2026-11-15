---
tags:
  - Original
translation:
  source: others/tortoise_and_hare.md
  source_commit: 0e127fb53867ee271019b5b9fc31d44c903cadd5
  status: draft
  last_synced: 2026-11-15
---

# Thuật toán Floyd tìm chu trình trong danh sách liên kết

Cho một danh sách liên kết có điểm đầu là **head**, có thể có hoặc không có chu trình. Ví dụ:

<div style="text-align: center;">
  <img src="tortoise_hare_algo.png" alt=""Linked list with cycle"">
</div>

Ta cần tìm điểm **C**, tức điểm bắt đầu của chu trình.

## Thuật toán đề xuất
Thuật toán này được gọi là **thuật toán tìm chu trình Floyd hoặc thuật toán rùa và thỏ**.
Để tìm điểm bắt đầu chu trình, trước hết ta cần xác định có chu trình hay không.
Việc này gồm hai bước:
1. Xác định sự tồn tại của chu trình.
2. Tìm điểm bắt đầu chu trình.

### Bước 1: Xác định có chu trình
1. Dùng hai con trỏ $slow$ và $fast$.
2. Ban đầu cả hai đều trỏ tới đầu danh sách liên kết.
3. Mỗi lần $slow$ di chuyển một bước.
4. Mỗi lần $fast$ di chuyển hai bước (nhanh gấp đôi con trỏ $slow$).
5. Kiểm tra xem chúng có trỏ tới cùng một nút trước khi một trong hai (hoặc cả hai) chạm null hay không.
6. Nếu tại một thời điểm chúng trỏ tới cùng một nút, danh sách liên kết có chu trình.
7. Nếu gặp null, danh sách liên kết không có chu trình.

**Ghi chú bản dịch:** Hai con trỏ ban đầu cùng trỏ tới đầu danh sách, nên chỉ so sánh sau khi đã di chuyển. Trước mỗi lần di chuyển cần kiểm tra điều kiện null như trong mã bên dưới.

<div style="text-align: center;">
  <img src="tortoise_hare_cycle_found.png" alt=""Found cycle"">
</div>

Sau khi xác định có chu trình trong danh sách liên kết, bước tiếp theo là tìm điểm bắt đầu chu trình, tức **C**.
### Bước 2: Điểm bắt đầu chu trình
1. Đưa con trỏ $slow$ về **head** của danh sách liên kết.
2. Mỗi lần di chuyển cả hai con trỏ một bước.
3. Điểm chúng gặp nhau là điểm bắt đầu chu trình.

```java
// Presence of cycle
public boolean hasCycle(ListNode head) {
    ListNode slow = head;
    ListNode fast = head;

    while(fast != null && fast.next != null){
        slow = slow.next;
        fast = fast.next.next;
        if(slow==fast){
            return true;
        }
    }

    return false;
}
```

```java
// Assuming there is a cycle present and slow and fast are point to their meeting point
slow = head;
while(slow!=fast){
	slow = slow.next;
	fast = fast.next;
}

return slow; // the starting point of the cycle.
```

## Tại sao thuật toán đúng

### Bước 1: Xác định có chu trình
Vì con trỏ $fast$ di chuyển nhanh gấp đôi $slow$, tại mọi thời điểm, quãng đường $fast$ đã đi gấp đôi quãng đường $slow$ đã đi.
Ta cũng suy ra hiệu giữa quãng đường hai con trỏ đã đi tăng thêm $1$ mỗi bước. 
```
slow: 0 --> 1 --> 2 --> 3 --> 4 (distance covered)
fast: 0 --> 2 --> 4 --> 6 --> 8 (distance covered)
diff: 0 --> 1 --> 2 --> 3 --> 4 (difference between distance covered by both pointers)
```
Gọi $L$ là độ dài chu trình và $a$ là số bước con trỏ chậm cần đi để tới điểm vào chu trình. Tồn tại số nguyên dương $k$ ($k > 0$) sao cho $k \cdot L \geq a$.
Khi con trỏ chậm đi được $k \cdot L$ bước và con trỏ nhanh đi được $2 \cdot k \cdot L$ bước, cả hai đều ở trong chu trình. Khi đó hiệu quãng đường đã đi là $k \cdot L$. Vì chu trình dài $L$, hai con trỏ ở cùng một điểm trong chu trình và gặp nhau.

### Bước 2: Điểm bắt đầu chu trình

Ta hãy tính quãng đường mỗi con trỏ đi được cho tới điểm gặp nhau trong chu trình.

<div style="text-align: center;">
  <img src="tortoise_hare_proof.png" alt=""Proof"">
</div>

$slowDist = a + xL + b$            , $x\ge0$

$fastDist = a + yL + b$            , $y\ge0$

- $slowDist$ là tổng quãng đường con trỏ chậm đã đi.
- $fastDist$ là tổng quãng đường con trỏ nhanh đã đi.
- $a$ là số bước mỗi con trỏ cần đi để vào chu trình.
- $b$ là khoảng cách từ **C** đến **G**, tức từ điểm bắt đầu chu trình đến điểm gặp nhau của hai con trỏ.
- $x$ là số vòng con trỏ chậm đã đi trong chu trình, bắt đầu và kết thúc tại **C**.
- $y$ là số vòng con trỏ nhanh đã đi trong chu trình, bắt đầu và kết thúc tại **C**.

$fastDist = 2 \cdot (slowDist)$

$a + yL + b = 2(a + xL + b)$

Biến đổi công thức, ta được:

$a=(y-2x)L-b$

trong đó $y-2x$ là một số nguyên

Điều này có nghĩa là đi $a$ bước tương đương với đi một số vòng đầy đủ trong chu trình rồi lùi $b$ bước.
Vì con trỏ nhanh đã ở trước điểm vào chu trình $b$ bước, nếu đi thêm $a$ bước thì nó sẽ tới điểm vào chu trình.
Vì ta cho con trỏ chậm bắt đầu từ đầu danh sách liên kết, sau $a$ bước nó cũng tới điểm vào chu trình. Do đó, nếu cả hai cùng đi $a$ bước, chúng sẽ gặp nhau tại điểm vào chu trình.

# Bài tập:
- [Linked List Cycle (EASY)](https://leetcode.com/problems/linked-list-cycle/)
- [Happy Number (Easy)](https://leetcode.com/problems/happy-number/)
- [Find the Duplicate Number (Medium)](https://leetcode.com/problems/find-the-duplicate-number/)
- [Linked List Cycle II](https://leetcode.com/problems/linked-list-cycle-ii/)

