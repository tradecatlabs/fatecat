lunar
=====

# 热词:阴历,天干,地支,五行,算命

import lunar
imprt datetime

myBZ = lunar.BazhiDate(1999,1,1)

print u"天干地支", myBZ.ganzhi()

print u"纳音",myBZ.nayin

print u"属相",myBZ.shuXiang

...
