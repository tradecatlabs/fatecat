# -*- coding: utf-8 -*-
"""
@author: wangshujing
"""
import sys
import subprocess
import platform
import io
import sys
#改变标准输出的默认编码
sys.stdout=io.TextIOWrapper(sys.stdout.buffer,encoding='utf8')
import os

class audio:
    def __init__(self):
        self = self

    def RunShellWithReturnCode(self,command):
        p = subprocess.Popen(command,stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=True)
        p.wait()
        output = ""
        while True:
            line = p.stderr.read()
            if not line:
                break
            output += line.decode("utf-8")
        # print(output)
        return output

    def getOneAudioContent(self, wavpath):
        #copy filepath to scp file
        if wavpath is None:
            return False
        
        (path, tempfilename) = os.path.split(wavpath)
        (filename, _) = os.path.splitext(tempfilename)
        scpfilename = filename + ".scp"
        scppath = os.path.join(path , scpfilename)

        with open(scppath,'w+') as scpfile:
            scpinfo = 'T0055G0036S0002 ' + wavpath
            scpfile.write(scpinfo)

        # print(platform.system())
        sysstr = platform.system()

        if(sysstr =="Windows"):
            cmd='online2-wav-nnet3-latgen-faster.exe ' \
            '--config=backend/api/kaldi/aidatatang_200zh/s5/exp/chain/nnet_online/conf/online_win.conf ' \
            '--do-endpointing=false ' \
            '--frames-per-chunk=20 ' \
            '--extra-left-context-initial=0 '\
            '--online=true '\
            '--frame-subsampling-factor=3 '\
            '--max-active=7000 '\
            '--beam=15.0 '\
            '--lattice-beam=6.0 '\
            '--online=false '\
            '--acoustic-scale=1.4 '\
            '--word-symbol-table=backend/api/kaldi/aidatatang_200zh/s5/data/lang/words.txt '\
            'backend/api/kaldi/aidatatang_200zh/s5/exp/chain/tdnn_1a_sp/final.mdl '\
            'backend/api/kaldi/aidatatang_200zh/s5/exp/chain/tdnn_1a_sp/graph/HCLG.fst '\
            'ark:backend/api/kaldi/aidatatang_200zh/s5/data/test/spk2utt_2_one '\
            'scp:' + scppath + ' '\
            'ark,t:backend/api/kaldi/aidatatang_200zh/s5/20190619.txt'
        elif(sysstr == "Linux"):
            cmd='online2-wav-nnet3-latgen-faster ' \
            '--config=backend/api/kaldi/aidatatang_200zh/s5/exp/chain/nnet_online/conf/online_dev.conf ' \
            '--do-endpointing=false ' \
            '--frames-per-chunk=20 ' \
            '--extra-left-context-initial=0 '\
            '--online=true '\
            '--frame-subsampling-factor=3 '\
            '--max-active=7000 '\
            '--beam=15.0 '\
            '--lattice-beam=6.0 '\
            '--online=false '\
            '--acoustic-scale=1.4 '\
            '--word-symbol-table=backend/api/kaldi/aidatatang_200zh/s5/data/lang/words.txt '\
            'backend/api/kaldi/aidatatang_200zh/s5/exp/chain/tdnn_1a_sp/final.mdl '\
            'backend/api/kaldi/aidatatang_200zh/s5/exp/chain/tdnn_1a_sp/graph/HCLG.fst '\
            'ark:backend/api/kaldi/aidatatang_200zh/s5/data/test/spk2utt_2_one '\
            'scp:' + scppath + ' '\
            'ark,t:backend/api/kaldi/aidatatang_200zh/s5/20190619.txt'
        else:
            print ("No Support audios in this platform")
            return False
        
        # cmd = 'dir'

        out = self.RunShellWithReturnCode(cmd)
        lines = str(out).split('\n')
        index = 0
        for line in lines:
            if 'IOR' in line:
                break
            index += 1
            # if (index == 8):
            if 'T0055G0036S0002' in line:
                output = line.split("T0055G0036S0002")[1].strip()
                #替换无法识别语音 <UNK>
                output = output.replace("<UNK>", "")
                print ("Result:%s" % output)
                return output

if __name__ == '__main__':
    myaudio = audio()
    # Windows
    myaudio.getOneAudioContent("D:\\var\\www\\gallery\\media\\audios\\T0055G0036S0010.wav")

    # Linux
    # myaudio.getOneAudioContent("/var/www/gallery/media/audios/T0055G0036S0003.wav")