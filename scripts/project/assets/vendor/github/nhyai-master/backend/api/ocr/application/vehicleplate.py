"""
行驶证
"""
from apphelper.image import union_rbox
import re
class vehicleplate:
    """
    驾驶证结构化识别
    """
    def __init__(self,result):
        self.result = union_rbox(result,0.2)
        self.N = len(self.result)
        self.res = {}
        self.license_type()
        self.license_no()
        self.full_name()
        self.address()
        self.birthday()
        self.first_issue()
        self.be_class()
        self.valid_period()
        print("999999999999999999999999   result====",result)


    def full_name(self):
        """
        驾驶证姓名
        """
        name={}
        for i in range(self.N):
            txt = self.result[i]['text'].replace(' ','')
            txt = txt.replace(' ','')
            ##匹配姓名
            res = re.findall("姓名[\u4e00-\u9fa5]+",txt)
            if len(res)>0:
                name['姓名']  =res[0].replace('姓名','')
            res = re.findall("始名[\u4e00-\u9fa5]+",txt)
            if len(res)>0:
                name['姓名']  =res[0].replace('始名','')
                # self.res.update(name) 
                # break
            if '男'  in txt:
                    name["性别"] = '男'
                    # self.res.update(sex) 
                    # break
            elif '女'  in txt:
                    name["性别"] = '女'

            res = re.findall(".*国籍[\u4e00-\u9fa5]+",txt)
            if len(res)>0:
                name["国籍"] = res[0].split('国籍')[-1]
                self.res.update(name) 
                break
   
    def address(self):
        """
        住址
        ##此处地址匹配还需完善
        """
        add={}
        addString=[]
        for i in range(self.N):
            txt = self.result[i]['text'].replace(' ','')
            txt = txt.replace(' ','')
            
            ##住址
            if '住址' in txt or '省' in txt or '市' in txt or '县' in txt or '街' in txt or '村' in txt or "镇" in txt or "区" in txt or "城" in txt or "室" in txt or "房" in txt:
                addString.append(txt.replace('住址',''))
            else:
                ##增加地址第二行判断
                res = re.findall(r'\d+号',txt)
            
            if len(res)>0:
                addString.append(txt.replace('住址',''))
            
        if len(addString)>0:
            add['住址']  =''.join(addString)
            self.res.update(add) 

    def birthday(self):
        """
        出生日期
        """
        birth={}
        for i in range(self.N):
            txt = self.result[i]['text'].replace(' ','')
            txt = txt.replace(' ','')
            ##出生日期
            res = re.findall(r'出生日期\d*-\d*-\d*-',txt)
            res = re.findall(r'\d*-\d*-\d*-',txt)
            
            if len(res)>0:
                birth['出生日期']  =res[0].replace('出生日期','')
                self.res.update(birth) 
                break
             
    
    def first_issue(self):
        """
        初次领证日期
        """
        first_issue={}
        for i in range(self.N):
            txt = self.result[i]['text'].replace(' ','')
            txt = txt.replace(' ','')
            res = re.findall("初次领证日期[\u4e00-\u9fa5]+",txt)
            if len(res)>0:
                print("111111111111111111  =",txt)
                first_issue['初次领证日期']  =res[0].replace('初次领证日期','')
                self.res.update(first_issue) 
                break    
    
    def be_class(self):
        """
        准驾车型
        """
        be_class={}
        for i in range(self.N):
            txt = self.result[i]['text'].replace(' ','')
            txt = txt.replace(' ','')
            res = re.findall("准驾车型[\u4e00-\u9fa5]+",txt)
            if len(res)>0:
                print("111111111111111111  =",txt)
                be_class['准驾车型']  =res[0].replace('准驾车型','')
                self.res.update(be_class) 
                break    
    
    def valid_period(self):
        """
        有效期限
        """
        valid_period={}
        for i in range(self.N):
            txt = self.result[i]['text'].replace(' ','')
            txt = txt.replace(' ','')
            res = re.findall("有效期限[\u4e00-\u9fa5]+",txt)
            if len(res)>0:
                print("111111111111111111  =",txt)
                valid_period['有效期限']  =res[0].replace('有效期限','')
                self.res.update(valid_period) 
                break    
        