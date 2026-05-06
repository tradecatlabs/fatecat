"""
created by: Wangshujing
"""

from __future__ import print_function
import os
import argparse
import numpy as np
import pandas as pd
import time
import shutil
from PIL import Image
from tqdm import tqdm
import torch
import cv2
from torch.utils.data import Dataset, DataLoader
from torch.autograd import Variable
import torchvision.models as models

# 添加当前项目到环境变量
import sys
sys.path.append(os.path.join(os.getcwd(),"backend","api"))
from util import ProtestDatasetEvalFile, modified_resnet50
import logging
logging.basicConfig(level = logging.INFO,format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class violence:
    def __init__(self, cuda):
        self = self
        self.path = os.getcwd()
        self.model_path = 'model_best.pth.tar'
        self.cuda = cuda
        print("*** loading model from {model}".format(model = self.model_path))
        self.model = modified_resnet50()
        if self.cuda:
            self.model = self.model.cuda()
        
        with open(os.path.join(self.path, 'backend' ,'api', self.model_path), 'rb') as f:
            self.model.load_state_dict(torch.load(f ,map_location='cpu')['state_dict'])

    def eval_one_file(self,img_path, model):
            """
            return model output of a images
            """
            model.eval()
            batch_size = 1
            workers = 0
            cuda = self.cuda
            timeout = 1
            # make dataloader
            try:

                dataset = ProtestDatasetEvalFile(img_path = img_path)
                data_loader = DataLoader(dataset,
                                        num_workers = workers,
                                        batch_size = batch_size,
                                        timeout= timeout)
                # load model

                outputs = []
                imgpaths = []

                n_imgs = 1
                with tqdm(total=n_imgs) as pbar:
                    for i, sample in enumerate(data_loader):
                        imgpath, input = sample['imgpath'], sample['image']
                        if cuda:
                            input = input.cuda()

                        input_var = Variable(input)
                        output = model(input_var)
                        outputs.append(output.cpu().data.numpy())
                        imgpaths = imgpath
                        if i < n_imgs / batch_size:
                            pbar.update(batch_size)
                        else:
                            pbar.update(n_imgs%batch_size)

                array = np.concatenate(outputs)
                return {
                    'protest': array[0][0],
                    'violence': array[0][1], 
                    'sign': array[0][2], 
                    'photo': array[0][3], 
                    'fire': array[0][4],
                    'police': array[0][5], 
                    'children': array[0][6], 
                    'group_20': array[0][7], 
                    'group_100': array[0][8], 
                    'flag': array[0][9],
                    'night': array[0][10], 
                    'shouting': array[0][11]
                }
            except:
                return {'protest': 0,'violence': 0}
                
    def check_violence(self,img_file):
    # load trained model
        # path = os.getcwd()
        # model_path = 'model_best.pth.tar'
        # cuda = False
        # print("*** loading model from {model}".format(model = model_path))
        # model = modified_resnet50()
        # if cuda:
        #     model = model.cuda()
        
        # with open(os.path.join(path, 'backend' ,'api', model_path), 'rb') as f:
        #     model.load_state_dict(torch.load(f ,map_location='cpu')['state_dict'])
        #     # calculate output
        # df = eval_one_file(img_file, model)
        # return df
        return self.eval_one_file(img_file, self.model)

if __name__ == '__main__':
    is_gpu = False
    myviolence = violence(is_gpu)
    result = myviolence.check_violence(os.path.join(os.getcwd(),"backend","api","yahoo","open_nsfw","images","BDPAk8S.jpg"))
    print (result)