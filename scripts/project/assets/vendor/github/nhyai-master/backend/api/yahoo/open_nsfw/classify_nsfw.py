# -*- coding: utf-8 -*-
#!/usr/bin/env python
"""
Copyright 2016 Yahoo Inc.
Licensed under the terms of the 2 clause BSD license. 
Please see LICENSE file in the project root for terms.
"""

import numpy as np
import os
import sys
import argparse
import glob
import time
from PIL import Image
try:
    from StringIO import StringIO
except ImportError:
    from io import BytesIO
import caffe

class nsfw:
    def __init__(self):
        self = self
        self.model_def = os.path.join(os.getcwd(),"backend","api","yahoo","open_nsfw","nsfw_model","deploy.prototxt")
        self.pretrained_model = os.path.join(os.getcwd(),"backend","api","yahoo","open_nsfw","nsfw_model","resnet_50_1by2_nsfw.caffemodel")
        self.output_layers = ['prob']
        # Pre-load caffe model.
        self.nsfw_net = caffe.Net(self.model_def,  # pylint: disable=invalid-name
                        self.pretrained_model, caffe.TEST)
        # Load transformer
        # Note that the parameters are hard-coded for best results
        self.caffe_transformer = caffe.io.Transformer({'data': self.nsfw_net.blobs['data'].data.shape})
        self.caffe_transformer.set_transpose('data', (2, 0, 1))  # move image channels to outermost
        self.caffe_transformer.set_mean('data', np.array([104, 117, 123]))  # subtract the dataset-mean value in each channel
        self.caffe_transformer.set_raw_scale('data', 255)  # rescale from [0, 1] to [0, 255]
        self.caffe_transformer.set_channel_swap('data', (2, 1, 0))  # swap channels from RGB to BGR


    def resize_image(self, data, sz=(256, 256)):
        """
        Resize image. Please use this resize logic for best results instead of the 
        caffe, since it was used to generate training dataset 
        :param str data:
            The image data
        :param sz tuple:
            The resized image dimensions
        :returns bytearray:
            A byte array with the resized image
        """
        im = Image.open(BytesIO(data))
        if im.mode != "RGB":
            im = im.convert('RGB')
        imr = im.resize(sz, resample=Image.BILINEAR)
        fh_im = BytesIO()
        imr.save(fh_im, format='JPEG')
        fh_im.seek(0)
        return fh_im

    def caffe_preprocess_and_compute(self, pimg, caffe_transformer=None, caffe_net=None,
        output_layers=None):
        """
        Run a Caffe network on an input image after preprocessing it to prepare
        it for Caffe.
        :param PIL.Image pimg:
            PIL image to be input into Caffe.
        :param caffe.Net caffe_net:
            A Caffe network with which to process pimg afrer preprocessing.
        :param list output_layers:
            A list of the names of the layers from caffe_net whose outputs are to
            to be returned.  If this is None, the default outputs for the network
            are returned.
        :return:
            Returns the requested outputs from the Caffe net.
        """
        if caffe_net is not None:

            # Grab the default output names if none were requested specifically.
            if output_layers is None:
                output_layers = caffe_net.outputs

            img_bytes = resize_image(pimg, sz=(256, 256))
            image = caffe.io.load_image(img_bytes)

            H, W, _ = image.shape
            _, _, h, w = caffe_net.blobs['data'].data.shape
            h_off = max((H - h) / 2, 0)
            w_off = max((W - w) / 2, 0)
            crop = image[int(h_off):int(h_off + h), int(w_off):int(w_off + w), :]
            transformed_image = caffe_transformer.preprocess('data', crop)
            transformed_image.shape = (1,) + transformed_image.shape

            input_name = caffe_net.inputs[0]
            all_outputs = caffe_net.forward_all(blobs=output_layers,
                        **{input_name: transformed_image})

            outputs = all_outputs[output_layers[0]][0].astype(float)
            return outputs
        else:
            return []

    def caffe_preprocess_and_compute_api(self, img):
        """
        Run a Caffe network on an input image after preprocessing it to prepare
        it for Caffe.
        :param img:
            image path to be input into Caffe.
        :return:
            Returns the requested outputs from the Caffe net.
        """
        try:
            image_data = open(img, 'rb').read()

            # Classify.
            img_bytes = self.resize_image(image_data, sz=(256, 256))
            image = caffe.io.load_image(img_bytes)

            H, W, _ = image.shape
            _, _, h, w = self.nsfw_net.blobs['data'].data.shape
            h_off = max((H - h) / 2, 0)
            w_off = max((W - w) / 2, 0)
            crop = image[int(h_off):int(h_off + h), int(w_off):int(w_off + w), :]
            transformed_image = self.caffe_transformer.preprocess('data', crop)
            transformed_image.shape = (1,) + transformed_image.shape

            input_name = self.nsfw_net.inputs[0]
            all_outputs = self.nsfw_net.forward_all(blobs=self.output_layers,
                        **{input_name: transformed_image})

            outputs = all_outputs[self.output_layers[0]][0].astype(float)
            return outputs
        except:
            outs = [0,0]
            return outs

    def main(argv):
        pycaffe_dir = os.path.dirname(__file__)

        parser = argparse.ArgumentParser()
        # Required arguments: input file.
        parser.add_argument(
            "input_file",
            help="Path to the input image file"
        )

        # Optional arguments.
        parser.add_argument(
            "--model_def",
            help="Model definition file."
        )
        parser.add_argument(
            "--pretrained_model",
            help="Trained model weights file."
        )

        args = parser.parse_args()
        image_data = open(args.input_file, 'rb').read()

        # Pre-load caffe model.
        nsfw_net = caffe.Net(args.model_def,  # pylint: disable=invalid-name
            args.pretrained_model, caffe.TEST)

        # Load transformer
        # Note that the parameters are hard-coded for best results
        caffe_transformer = caffe.io.Transformer({'data': nsfw_net.blobs['data'].data.shape})
        caffe_transformer.set_transpose('data', (2, 0, 1))  # move image channels to outermost
        caffe_transformer.set_mean('data', np.array([104, 117, 123]))  # subtract the dataset-mean value in each channel
        caffe_transformer.set_raw_scale('data', 255)  # rescale from [0, 1] to [0, 255]
        caffe_transformer.set_channel_swap('data', (2, 1, 0))  # swap channels from RGB to BGR

        # Classify.
        scores = caffe_preprocess_and_compute(image_data, caffe_transformer=caffe_transformer, caffe_net=nsfw_net, output_layers=['prob'])

        # Scores is the array containing SFW / NSFW image probabilities
        # scores[1] indicates the NSFW probability
        print ("NSFW score:  %f" %  float(scores[1]))

if __name__ == '__main__':
    # main(sys.argv)
    mynsfw = nsfw()
    scores = mynsfw.caffe_preprocess_and_compute_api(os.path.join(os.getcwd(),"backend","api","yahoo","open_nsfw","images","BDPAk8S.jpg"))
    print ("NSFW score:  %f" %  float(scores[1]))