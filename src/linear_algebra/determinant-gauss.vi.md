---
tags:
  - Translated
e_maxx_link: determinant_gauss
translation:
  source: linear_algebra/determinant-gauss.md
  source_commit: f6c78df9c7e625a466be28181edec28cd417683e
  status: draft
  last_synced: 2026-11-15
---

# Tính định thức ma trận bằng phương pháp Gauss

Bài toán: Cho ma trận $A$ kích thước $N \times N$. Hãy tính định thức của ma trận.

## Thuật toán

Ta sử dụng ý tưởng của [phương pháp Gauss để giải hệ phương trình tuyến tính](linear-system-gauss.md).

Ta thực hiện các bước như khi giải hệ phương trình tuyến tính, chỉ bỏ thao tác chia hàng hiện tại cho $a_{ij}$. Các phép biến đổi này không làm thay đổi giá trị tuyệt đối của định thức ma trận. Tuy nhiên, khi đổi chỗ hai hàng, dấu của định thức có thể thay đổi.

Sau khi áp dụng phép khử Gauss, ta thu được ma trận đường chéo; định thức của ma trận này bằng tích các phần tử trên đường chéo. Như đã nói, dấu được xác định bởi số lần đổi chỗ hàng: nếu số lần này lẻ thì ta đổi dấu định thức. Do đó, thuật toán Gauss tính định thức có độ phức tạp $O(N^3)$.

Lưu ý rằng nếu tại một bước nào đó không tìm được ô khác 0 trong cột hiện tại, thuật toán phải dừng và trả về 0.

## Cài đặt

```cpp
const double EPS = 1E-9;
int n;
vector < vector<double> > a (n, vector<double> (n));

double det = 1;
for (int i=0; i<n; ++i) {
	int k = i;
	for (int j=i+1; j<n; ++j)
		if (abs (a[j][i]) > abs (a[k][i]))
			k = j;
	if (abs (a[k][i]) < EPS) {
		det = 0;
		break;
	}
	swap (a[i], a[k]);
	if (i != k)
		det = -det;
	det *= a[i][i];
	for (int j=i+1; j<n; ++j)
		a[i][j] /= a[i][i];
	for (int j=0; j<n; ++j)
		if (j != i && abs (a[j][i]) > EPS)
			for (int k=i+1; k<n; ++k)
				a[j][k] -= a[i][k] * a[j][i];
}

cout << det;
```

## Bài tập thực hành
* [Codeforces - Wizards and Bets](http://codeforces.com/contest/167/problem/E)
