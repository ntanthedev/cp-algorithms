---
tags:
  - Translated
e_maxx_link: schedule_with_completion_duration
translation:
  source: schedules/schedule-with-completion-duration.md
  source_commit: e7d63bed3e4c244f49782852e2b32904134af22a
  status: draft
  last_synced: 2026-11-15
---

# Lập lịch tối ưu cho các công việc có thời hạn và thời lượng

Giả sử ta có một tập công việc, biết thời hạn và thời lượng của mỗi công việc. Một công việc đã bắt đầu thì không thể bị ngắt trước khi kết thúc. Cần lập lịch để hoàn thành được nhiều công việc nhất.

## Lời giải

Thuật toán sử dụng phương pháp **tham lam**. Sắp xếp tất cả công việc theo thời hạn và xét theo thứ tự giảm dần. Ta cũng tạo một hàng đợi $q$, lần lượt đưa các công việc vào đó và lấy ra công việc có thời gian chạy nhỏ nhất (chẳng hạn có thể dùng set hoặc priority_queue). Ban đầu, $q$ rỗng.

Giả sử ta đang xét công việc thứ $i$. Trước hết đưa nó vào $q$. Xét khoảng thời gian giữa thời hạn của công việc thứ $i$ và thời hạn của công việc thứ $i-1$. Khoảng này có độ dài $T$. Ta lấy các công việc ra khỏi $q$ (theo thứ tự tăng dần của thời lượng còn lại) và thực hiện cho đến khi lấp đầy khoảng $T$. Lưu ý: nếu tại một thời điểm, công việc được lấy ra chỉ có thể thực hiện một phần trước khi khoảng $T$ được lấp đầy, ta thực hiện nó nhiều nhất có thể, tức là trong thời gian $T$, rồi đưa phần còn lại của công việc trở lại $q$.

**Ghi chú bản dịch:** Việc chia thời lượng ở đây là bước tính toán khi xét ngược các khoảng thời gian, không có nghĩa lịch thực tế được phép ngắt công việc. Sau khi chọn xong tập công việc, có thể sắp xếp chúng theo thời hạn để lập lịch không ngắt như phần cài đặt nêu.

Khi thuật toán kết thúc, ta sẽ chọn được lời giải tối ưu (hoặc ít nhất là một trong nhiều lời giải tối ưu). Thời gian chạy của thuật toán là $O(n \log n)$.

## Cài đặt

Hàm sau nhận một vector các công việc (gồm thời hạn, thời lượng và chỉ số của công việc) và tính vector chứa mọi chỉ số của các công việc được dùng trong lịch tối ưu.
Lưu ý rằng bạn vẫn cần sắp xếp các công việc này theo thời hạn nếu muốn viết lịch một cách tường minh.

```{.cpp file=schedule_deadline_duration}
struct Job {
    int deadline, duration, idx;

    bool operator<(Job o) const {
        return deadline < o.deadline;
    }
};

vector<int> compute_schedule(vector<Job> jobs) {
    sort(jobs.begin(), jobs.end());

    set<pair<int,int>> s;
    vector<int> schedule;
    for (int i = jobs.size()-1; i >= 0; i--) {
        int t = jobs[i].deadline - (i ? jobs[i-1].deadline : 0);
        s.insert(make_pair(jobs[i].duration, jobs[i].idx));
        while (t && !s.empty()) {
            auto it = s.begin();
            if (it->first <= t) {
                t -= it->first;
                schedule.push_back(it->second);
            } else {
                s.insert(make_pair(it->first - t, it->second));
                t = 0;
            }
            s.erase(it);
        }
    }
    return schedule;
}
```
