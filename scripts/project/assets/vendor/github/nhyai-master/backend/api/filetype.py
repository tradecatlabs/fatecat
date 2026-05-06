
# coding:utf-8
# wangshujing
import os

# 文件类型检测
class FileType:
    # 支持文件类型
    # 用16进制字符串的目的是可以知道文件头是多少字节
    # 各种文件头的长度不一样，少半2字符，长则8字符
    def typeList(self):
        # print('获取文件格式十六进制码表……')
        return {
            '68746D6C3E': 'html',
            'd0cf11e0a1b11ae10000': 'xls',
            '44656C69766572792D64': 'eml',
            'ffd8ffe000104a464946': 'jpg',
            '89504e470d0a1a0a0000': 'png',
            '47494638396126026f01': 'gif',
            '49492a00227105008037': 'tif',
            '424d228c010000000000': 'bmp',
            '424d8240090000000000': 'bmp',
            '424d8e1b030000000000': 'bmp',
            '41433130313500000000': 'dwg',
            '3c21444f435459504520': 'html',
            '3c21646f637479706520': 'htm',
            '48544d4c207b0d0a0942': 'css',
            '696b2e71623d696b2e71': 'js',
            '7b5c727466315c616e73': 'rtf',
            '38425053000100000000': 'psd',
            '46726f6d3a203d3f6762': 'eml',
            'd0cf11e0a1b11ae10000': 'doc',
            'd0cf11e0a1b11ae10000': 'vsd',
            '5374616E64617264204A': 'mdb',
            '252150532D41646F6265': 'ps',
            '255044462d312e350d0a': 'pdf',
            '2e524d46000000120001': 'rmvb',
            '464c5601050000000900': 'flv',
            '00000020667479706d70': 'mp4',
            '49443303000000002176': 'mp3',
            '000001ba210001000180': 'mpg',
            '3026b2758e66cf11a6d9': 'wmv',
            '52494646e27807005741': 'wav',
            '52494646d07d60074156': 'avi',
            '4d546864000000060001': 'mid',
            '504b0304140000080044': 'zip',
            '504b03040a0000080000': 'zip',
            '504b03040a0000000000': 'zip',
            '526172211a0700cf9073': 'rar',
            '235468697320636f6e66': 'ini',
            '504b03040a0000000000': 'jar',
            '4d5a9000030000000400': 'exe',
            '3c25402070616765206c': 'jsp',
            '4d616e69666573742d56': 'mf',
            '3c3f786d6c2076657273': 'xml',
            '494e5345525420494e54': 'sql',
            '7061636b616765207765': 'java',
            '406563686f206f66660d': 'bat',
            '1f8b0800000000000000': 'gz',
            '6c6f67346a2e726f6f74': 'properties',
            'cafebabe0000002e0041': 'class',
            '49545346030000006000': 'chm',
            '04000000010000001300': 'mxp',
            '504b0304140006000800': 'docx',
            'd0cf11e0a1b11ae10000': 'wps',
            '6431303a637265617465': 'torrent',
        }


    # 字节码转16进制字符串
    def bytes2hex(self,bytes):

        # print('关键码转码……')
        num = len(bytes)
        hexstr = u""
        for i in range(num):
            t = u"%x" % bytes[i]
            if len(t) % 2:
                hexstr += u"0"
            hexstr += t
        return hexstr.upper()

    # 获取文件类型
    def filetype(self,filename):
        # print('读文件二进制码中……')
        binfile = open(filename, 'rb')  # 必需二制字读取
        # print('提取关键码……')
        bins = binfile.read(20)  # 提取20个字符
        binfile.close()  # 关闭文件流
        bins = self.bytes2hex(bins)  # 转码
        bins = bins.lower()  # 小写
        # print(bins)
        tl = self.typeList()  # 文件类型
        ftype = 'unknown'
        # print('关键码比对中……')
        for hcode in tl.keys():
            lens = len(hcode)  # 需要的长度
            if bins[0:lens] == hcode:
                ftype = tl[hcode]
                break
            if ftype == 'unknown':  # 全码未找到，优化处理，码表取5位验证
                bins = bins[0:5]
                for hcode in tl.keys():
                    if len(hcode) > 5 and bins == hcode[0:5]:
                        ftype = tl[hcode]
                        break
        return ftype


    # 文件扫描，如果是目录，就将遍历文件，是文件就判断文件类型
    def filescanner(self,path):
        if type(path) != type('a'):  # 判断是否为字符串
            print('抱歉，你输入的不是一个字符串路径！')
        elif path.strip() == '':  # 将两头的空格移除
            print('输入的路径为空！')
        elif not os.path.exists(path):
            print('输入的路径不存在！')
        elif os.path.isfile(path):
            print('输入的路径指向的是文件，验证文件类型……')
            if path.rfind('.') > 0:
                print('文件名:', os.path.split(path)[1])
            else:
                print('文件名中没有找到格式')
            file_type = self.filetype(path)
            print('解析文件判断格式：'+ file_type)
            return file_type
        elif os.path.isdir(path):
            print('输入的路径指向的是目录，开始遍历文件')
            for p, d, fs in os.walk(path):
                print(os.path.split(p))
                for n in fs:
                    n = n.split('.')
                    print('\t'+n[0]+'\t'+n[1])

if __name__ == '__main__':
    # path = 'D:\\var\\www\\gallery\\media\\text\\f56c9e13cc8d4e0485abd94cc2a90d49.docx'
    path = 'D:\\var\\www\\gallery\\media\\text\\test.docx'
    file_type = FileType().filescanner(path)
    print(file_type)
