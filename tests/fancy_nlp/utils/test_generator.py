# -*- coding: utf-8 -*-

import os

import math

from fancy_nlp.utils import load_ner_data_and_labels, load_spm_data_and_labels
from fancy_nlp.preprocessors import NERPreprocessor, SPMPreprocessor
from fancy_nlp.utils import NERGenerator, SPMGenerator


class TestGenerator:
    def test_ner_generator(self):
        test_file = os.path.join(os.path.dirname(__file__), '../../../data/ner/msra/example.txt')
        x_train, y_train = load_ner_data_and_labels(test_file)

        preprocessor = NERPreprocessor(x_train, y_train)
        generator = NERGenerator(preprocessor, x_train, batch_size=64)
        assert len(generator) == math.ceil(len(x_train) / 64)
        for i, (features, y) in enumerate(generator):
            if i < len(generator) - 1:
                assert features.shape[0] == 64
                assert y is None
            else:
                assert features.shape[0] == len(x_train) - 64 * (len(generator) - 1)
                assert y is None

    def test_spm_generator(self):
        test_file = os.path.join(os.path.dirname(__file__), '../../../data/spm/webank/example.txt')
        x_train, y_train = load_spm_data_and_labels(test_file)

        preprocessor = SPMPreprocessor(x_train, y_train)
        generator = SPMGenerator(preprocessor, x_train, batch_size=64)
        assert len(generator) == math.ceil(len(x_train[0]) / 64)
        for i, (features, y) in enumerate(generator):
            if i < len(generator) - 1:
                assert features[0].shape[0] == features[1].shape[0] == 64
                assert y is None
            else:
                assert features[0].shape[0] == features[1].shape[0] == \
                       len(x_train[0]) - 64 * (len(generator) - 1)
                assert y is None
