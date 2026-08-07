---
tags:
  - Translated
e_maxx_link: rabin_karp
translation:
  source: string/rabin-karp.md
  source_commit: e9dcc74da525e47cdd893346f44d024d021ab758
  status: draft
  last_synced: 2026-08-07
---

# Thuật toán Rabin-Karp cho so khớp chuỗi

Thuật toán này dựa trên ý tưởng băm, vì vậy nếu chưa quen với băm chuỗi, hãy xem bài [băm chuỗi](string-hashing.md).
 
Thuật toán được Rabin và Karp đề xuất vào năm 1987.

Bài toán: Cho hai chuỗi — mẫu $s$ và văn bản $t$ — hãy xác định mẫu có xuất hiện trong văn bản hay không; nếu có, liệt kê mọi vị trí xuất hiện trong thời gian $O(|s| + |t|)$.

Thuật toán: Tính giá trị băm của mẫu $s$.
Tính giá trị băm cho mọi tiền tố của văn bản $t$.
Khi đó, nhờ các giá trị băm đã tính, ta có thể so sánh một chuỗi con có độ dài $|s|$ với $s$ trong thời gian hằng số.
Vì vậy, ta lần lượt so sánh từng chuỗi con có độ dài $|s|$ với mẫu. Tổng thời gian cho bước này là $O(|t|)$.
Do đó, độ phức tạp cuối cùng của thuật toán là $O(|t| + |s|)$: cần $O(|s|)$ để tính giá trị băm của mẫu và $O(|t|)$ để so sánh từng chuỗi con có độ dài $|s|$ với mẫu.

## Cài đặt
```{.cpp file=rabin_karp}
vector<int> rabin_karp(string const& s, string const& t) {
    const int p = 31; 
    const int m = 1e9 + 9;
    int S = s.size(), T = t.size();

    vector<long long> p_pow(max(S, T)); 
    p_pow[0] = 1; 
    for (int i = 1; i < (int)p_pow.size(); i++) 
        p_pow[i] = (p_pow[i-1] * p) % m;

    vector<long long> h(T + 1, 0); 
    for (int i = 0; i < T; i++)
        h[i+1] = (h[i] + (t[i] - 'a' + 1) * p_pow[i]) % m; 
    long long h_s = 0; 
    for (int i = 0; i < S; i++) 
        h_s = (h_s + (s[i] - 'a' + 1) * p_pow[i]) % m; 

    vector<int> occurrences;
    for (int i = 0; i + S - 1 < T; i++) {
        long long cur_h = (h[i+S] + m - h[i]) % m;
        if (cur_h == h_s * p_pow[i] % m)
            occurrences.push_back(i);
    }
    return occurrences;
}
```

## Bài tập

* [SPOJ - Pattern Find](http://www.spoj.com/problems/NAJPF/)
* [Codeforces - Good Substrings](http://codeforces.com/problemset/problem/271/D)
* [Codeforces - Palindromic characteristics](https://codeforces.com/problemset/problem/835/D)
* [Leetcode - Longest Duplicate Substring](https://leetcode.com/problems/longest-duplicate-substring/)
