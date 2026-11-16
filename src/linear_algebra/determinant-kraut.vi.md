---
title: Calculating the determinant using Kraut method
tags:
  - Original
translation:
  source: linear_algebra/determinant-kraut.md
  source_commit: af69961aca7c3ed7a5779ff2e968713fec64e3ce
  status: draft
  last_synced: 2026-11-16
---
# Tính định thức bằng phương pháp Kraut trong $O(N^3)$

Trong bài này, ta sẽ mô tả cách tìm định thức của ma trận bằng phương pháp Kraut với độ phức tạp $O(N^3)$.

Thuật toán Kraut tìm phép phân tích ma trận $A$ thành $A = L U$, trong đó $L$ là ma trận tam giác dưới và $U$ là ma trận tam giác trên. Không mất tính tổng quát, ta có thể giả sử mọi phần tử trên đường chéo của $L$ đều bằng 1. Khi đã biết hai ma trận này, ta dễ dàng tính được định thức của $A$: đó là tích các phần tử trên đường chéo chính của ma trận $U$.

Có một định lý phát biểu rằng một ma trận khả nghịch có phép phân tích LU và phép phân tích đó là duy nhất khi và chỉ khi tất cả các định thức con chính của nó đều khác không. Ta chỉ xét phép phân tích trong đó đường chéo của ma trận $L$ gồm các số một.

**Ghi chú của người dịch:** Điều kiện chuẩn cho phép phân tích LU duy nhất thuộc dạng này là các định thức con chính đầu đều khác không; yêu cầu mọi định thức con chính khác không là mạnh hơn mức cần thiết. Chẳng hạn, ma trận gồm hai hàng (1, 1) và (1, 0) vẫn có phân tích LU duy nhất dù định thức con chính ở hàng và cột thứ hai bằng không.

Gọi $A$ là ma trận và $N$ là kích thước của nó. Ta sẽ tìm các phần tử của ma trận $L$ và $U$ theo các bước sau:

 1. Đặt $L_{i i} = 1$ với $i = 1, 2, ..., N$.
 2. Với mỗi $j = 1, 2, ..., N$, thực hiện:
      - Với $i = 1, 2, ..., j$, tìm các giá trị

        \[U_{ij} = A_{ij} - \sum_{k=1}^{i-1} L_{ik} \cdot U_{kj}\]

      - Tiếp theo, với $i = j+1, j+2, ..., N$, tìm các giá trị

        \[L_{ij} = \frac{1}{U_{jj}} \left(A_{ij} - \sum_{k=1}^{j-1} L_{ik} \cdot U_{kj} \right).\]

## Cài đặt

**Ghi chú của người dịch:** Mã nguồn có thể trả kết quả sai ngay cả với ma trận có định thức khác không: ma trận một phần tử âm bị nhận nhầm là có hàng toàn không vì vòng kiểm tra chỉ tìm phần tử dương. Kết quả còn được làm tròn thành số nguyên và mọi ngoại lệ đều khiến hàm trả về không.

```java
static BigInteger det (BigDecimal a [][], int n) {
	try {

	for (int i=0; i<n; i++) {
		boolean nonzero = false;
		for (int j=0; j<n; j++)
			if (a[i][j].compareTo (new BigDecimal (BigInteger.ZERO)) > 0)
				nonzero = true;
		if (!nonzero)
			return BigInteger.ZERO;
	}

	BigDecimal scaling [] = new BigDecimal [n];
	for (int i=0; i<n; i++) {
		BigDecimal big = new BigDecimal (BigInteger.ZERO);
		for (int j=0; j<n; j++)
			if (a[i][j].abs().compareTo (big) > 0)
				big = a[i][j].abs();
		scaling[i] = (new BigDecimal (BigInteger.ONE)) .divide
			(big, 100, BigDecimal.ROUND_HALF_EVEN);
	}

	int sign = 1;

	for (int j=0; j<n; j++) {
		for (int i=0; i<j; i++) {
			BigDecimal sum = a[i][j];
			for (int k=0; k<i; k++)
				sum = sum.subtract (a[i][k].multiply (a[k][j]));
			a[i][j] = sum;
		}

		BigDecimal big = new BigDecimal (BigInteger.ZERO);
		int imax = -1;
		for (int i=j; i<n; i++) {
			BigDecimal sum = a[i][j];
			for (int k=0; k<j; k++)
				sum = sum.subtract (a[i][k].multiply (a[k][j]));
			a[i][j] = sum;
			BigDecimal cur = sum.abs();
			cur = cur.multiply (scaling[i]);
			if (cur.compareTo (big) >= 0) {
				big = cur;
				imax = i;
			}
		}

		if (j != imax) {
			for (int k=0; k<n; k++) {
				BigDecimal t = a[j][k];
				a[j][k] = a[imax][k];
				a[imax][k] = t;
			}

			BigDecimal t = scaling[imax];
			scaling[imax] = scaling[j];
			scaling[j] = t;

			sign = -sign;
		}

		if (j != n-1)
			for (int i=j+1; i<n; i++)
				a[i][j] = a[i][j].divide
					(a[j][j], 100, BigDecimal.ROUND_HALF_EVEN);

	}

	BigDecimal result = new BigDecimal (1);
	if (sign == -1)
		result = result.negate();
	for (int i=0; i<n; i++)
		result = result.multiply (a[i][i]);

	return result.divide
		(BigDecimal.valueOf(1), 0, BigDecimal.ROUND_HALF_EVEN).toBigInteger();
	}
	catch (Exception e) {
		return BigInteger.ZERO;
	}
}
```
