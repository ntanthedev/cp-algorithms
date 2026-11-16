---
tags:
  - Translated
e_maxx_link: profile_dynamics
translation:
  source: dynamic_programming/profile-dynamics.md
  source_commit: 4503daae596847f01b980aa2a3c88b168bfcb37f
  status: draft
  last_synced: 2026-11-15
---

# Quy hoạch động theo biên dạng gãy. Bài toán "Parquet"

Các bài toán thường được giải bằng quy hoạch động theo biên dạng gãy (broken profile) bao gồm:

- đếm số cách phủ kín một vùng (ví dụ bàn cờ/lưới) bằng các hình (ví dụ domino)
- tìm cách phủ kín một vùng bằng ít hình nhất
- tìm cách phủ một phần sao cho diện tích chưa phủ (hoặc số ô chưa phủ trên lưới) là nhỏ nhất
- tìm cách phủ một phần bằng ít hình nhất sao cho không thể đặt thêm hình nào

## Bài toán "Parquet"

**Đề bài.** Cho một lưới kích thước $N \times M$. Đếm số cách phủ lưới bằng các hình kích thước $2 \times 1$ (không để ô nào chưa được phủ và các hình không chồng lên nhau).

Gọi trạng thái quy hoạch động là $dp[i, mask]$, với $i = 1, \ldots N$ và $mask = 0, \ldots 2^M - 1$.

$i$ biểu thị số hàng trong lưới hiện tại, còn $mask$ là trạng thái của hàng cuối cùng của lưới đó. Nếu bit thứ $j$ của $mask$ bằng $0$ thì ô tương ứng đã được phủ; ngược lại, ô đó chưa được phủ.

Rõ ràng đáp án của bài toán là $dp[N, 0]$.

Ta sẽ xây dựng trạng thái quy hoạch động bằng cách duyệt từng $i = 1, \cdots N$ và từng $mask = 0, \ldots 2^M - 1$. Với mỗi $mask$, ta chỉ chuyển trạng thái về phía trước, tức là _thêm_ các hình vào lưới hiện tại.

Ghi chú bản dịch: Mô tả bit ở trên không nhất quán với mã: trong calc, bit bằng 1 là ô đã được phủ từ hàng trước; bit bằng 0 là ô cần xử lý. Mã cũng dùng trạng thái ban đầu dp[0][0].

### Cài đặt

```cpp
int n, m;
vector < vector<long long> > dp;


void calc (int x = 0, int y = 0, int mask = 0, int next_mask = 0)
{
	if (x == n)
		return;
	if (y >= m)
		dp[x+1][next_mask] += dp[x][mask];
	else
	{
		int my_mask = 1 << y;
		if (mask & my_mask)
			calc (x, y+1, mask, next_mask);
		else
		{
			calc (x, y+1, mask, next_mask | my_mask);
			if (y+1 < m && ! (mask & my_mask) && ! (mask & (my_mask << 1)))
				calc (x, y+2, mask, next_mask);
		}
	}
}


int main()
{
	cin >> n >> m;

	dp.resize (n+1, vector<long long> (1<<m));
	dp[0][0] = 1;
	for (int x=0; x<n; ++x)
		for (int mask=0; mask<(1<<m); ++mask)
			calc (x, 0, mask, 0);

	cout << dp[n][0];

}
```

## Bài tập luyện tập

- [UVA 10359 - Tiling](https://onlinejudge.org/index.php?option=com_onlinejudge&Itemid=8&page=show_problem&problem=1300)
- [UVA 10918 - Tri Tiling](https://onlinejudge.org/index.php?option=com_onlinejudge&Itemid=8&page=show_problem&problem=1859)
- [SPOJ GNY07H (Four Tiling)](https://www.spoj.com/problems/GNY07H/)
- [SPOJ M5TILE (Five Tiling)](https://www.spoj.com/problems/M5TILE/)
- [SPOJ MNTILE (MxN Tiling)](https://www.spoj.com/problems/MNTILE/)
- [SPOJ DOJ1](https://www.spoj.com/problems/DOJ1/)
- [SPOJ DOJ2](https://www.spoj.com/problems/DOJ2/)
- [SPOJ BTCODE_J](https://www.spoj.com/problems/BTCODE_J/)
- [SPOJ PBOARD](https://www.spoj.com/problems/PBOARD/)
- [ACM HDU 4285 - Circuits](http://acm.hdu.edu.cn/showproblem.php?pid=4285)
- [LiveArchive 4608 - Mosaic](https://vjudge.net/problem/UVALive-4608)
- [Timus 1519 - Formula 1](https://acm.timus.ru/problem.aspx?space=1&num=1519)
- [Codeforces Parquet](https://codeforces.com/problemset/problem/26/C)

## Tài liệu tham khảo

- [Blog by EvilBunny](https://web.archive.org/web/20180712171735/https://blog.evilbuggy.com/2018/05/broken-profile-dynamic-programming.html)
- [TopCoder Recipe by "syg96"](https://apps.topcoder.com/forums/?module=Thread&start=0&threadID=697369)
- [Blogpost by sk765](http://sk765.blogspot.com/2012/02/dynamic-programming-with-profile.html)
