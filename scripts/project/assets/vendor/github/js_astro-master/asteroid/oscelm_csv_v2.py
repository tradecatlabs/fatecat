import numpy as np
from numpy.polynomial import chebyshev as C
import csv

n = 2924
deg = 10
for filename in ['01_ceres.csv', '02_pallas.csv', '03_juno.csv', '04_vesta.csv', '05_chiron.csv', '06_eris.csv', '07_sedna.csv']:
	with open('csv/' + filename) as f:
		a = np.zeros(n)
		l = np.zeros(n)
		h = np.zeros(n) # e * sin(pi)
		k = np.zeros(n) # e * cos(pi)
		p = np.zeros(n) # sin(i / 2) * sin(Omg)
		q = np.zeros(n) # sin(i / 2) * cos(Omg)
		t = np.zeros(n)
		nrev = 0
		m_pi = np.pi
		rrev = 2.0 * np.pi
		ma0 = None
		L0 = None
		ii = 0

		reader = csv.reader(f)
		# ファイルを読み取る
		for row in reader:
			jd = float(row[0])
			# 25 日ごとにサンプリングする
			t_jd = (jd - 2460675) / 36525

			# 接触軌道要素を算出する
			# a = res[0]
			e = float(row[2])
			g = np.sin(np.deg2rad(float(row[4])) / 2.0)
			Omg = np.deg2rad(float(row[5]))
			w   = np.deg2rad(float(row[6]))
			ma  = np.deg2rad(float(row[9]))

			pi  = Omg + w
			L   = pi + ma
			while L >= rrev:
				L -= rrev
			if L0 is not None and L0 > m_pi and L < m_pi:
				nrev += 1
			
			t[ii] = t_jd
			a[ii] = float(row[11])
			l[ii] = L + nrev * rrev
			h[ii] = e * np.sin(pi)
			k[ii] = e * np.cos(pi)
			p[ii] = g * np.sin(Omg)
			q[ii] = g * np.cos(Omg)

			ma0 = ma
			L0 = L
			ii += 1

		# Chebyshev 多項式近似する
		c, stats = C.chebfit(t, a, deg, full=True)
		print('a coefs = ' + str(c))
		print('residuals = ' + str(stats[0]))

		c, stats = C.chebfit(t, l, deg, full=True)
		print('l coefs = ' + str(c))
		print('residuals = ' + str(stats[0]))

		c, stats = C.chebfit(t, h, deg, full=True)
		print('h coefs = ' + str(c))
		print('residuals = ' + str(stats[0]))

		c, stats = C.chebfit(t, k, deg, full=True)
		print('k coefs = ' + str(c))
		print('residuals = ' + str(stats[0]))

		c, stats = C.chebfit(t, p, deg, full=True)
		print('p coefs = ' + str(c))
		print('residuals = ' + str(stats[0]))

		c, stats = C.chebfit(t, q, deg, full=True)
		print('q coefs = ' + str(c))
		print('residuals = ' + str(stats[0]))

		print('=====')
