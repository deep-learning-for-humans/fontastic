import torch
import torch.nn as nn
import torch.optim as optim
from torch.optim import lr_scheduler
import numpy as np
import torchvision
from torchvision import datasets, models, transforms
import matplotlib.pyplot as plt
import time
import os
import pandas as pd
from sklearn.model_selection import train_test_split
import shutil
import time
import copy
from models.lr_finder import LRFinder
from fastai.vision import transform as tfm
from PIL import Image
import pickle
import ssl
ssl._create_default_https_context = ssl._create_unverified_context


def get_train_files_path(experiments_path, data_path, phase):
    if phase == 'train':
        file_name = 'train.csv'
    elif phase == 'test':
        file_name = 'test.csv'
    else:
        print("phase can only have train and test as parameter values")
        exit()
    file_path = os.path.join(experiments_path, file_name)
    train_df = pd.read_csv(file_path, delimiter=',')
    files_path = []
    fonts_class = []
    for row in train_df.iterrows():
        files_path.append(os.path.join(
            data_path, row[1]['class'], row[1]['filename']))
        fonts_class.append(row[1]['class'])

    return files_path, fonts_class


def copy_images_to_path(file_path, file_class, destination_dir):
    font_folder = os.path.join(destination_dir, file_class)
    if os.path.exists(font_folder) == False:
        os.makedirs(font_folder)

    print("File being copied from {}:{}".format(file_path, font_folder))
    shutil.copy(file_path, font_folder)


def create_model_training_data(experiments_path, data_path):
    X_train, y_train = get_train_files_path(
        experiments_path, data_path, phase='train')
    X_test, y_test = get_train_files_path(
        experiments_path, data_path, phase='test')
    train_dir = os.path.join(experiments_path, 'train')
    test_dir = os.path.join(experiments_path, 'test')

    if not os.path.exists(train_dir):
        os.makedirs(train_dir)

    if not os.path.exists(test_dir):
        os.makedirs(test_dir)

    for file_path, font_class in zip(X_train, y_train):
        copy_images_to_path(file_path, font_class, train_dir)

    for file_path, font_class in zip(X_test, y_test):
        copy_images_to_path(file_path, font_class, test_dir)

    image_datasets = {x: datasets.ImageFolder(os.path.join(
        experiments_path, x), data_transforms[x]) for x in ['train', 'test']}
    class_names = image_datasets['train'].classes
    dataloaders = {x: torch.utils.data.DataLoader(image_datasets[x],
                                                  batch_size=32,
                                                  shuffle=True,
                                                  num_workers=4)
                   for x in ['train', 'test']}
    device = torch.device("cuda:1" if torch.cuda.is_available() else "cpu")
    dataset_sizes = {x: len(image_datasets[x]) for x in ['train', 'test']}


def train_model(model, criterion, optimizer, scheduler, num_epochs=20):
    since = time.time()
    best_acc = 0.0
    best_model = copy.deepcopy(model.state_dict())
    epoch_information = []

    '''
    The epoch information will contain gradcam 
    for all the layers for selected images
    There will be 2 sliders, one for epoch, given epoch, grad cam at each layer
    '''

    new_freeze_state = None
    prev_freeze_state = False
    for epoch in range(num_epochs):
        print("Epoch {}/{}".format(epoch, num_epochs - 1))
        print('-' * 10)
        for phase in ['train', 'test']:
            if phase == 'train':
                scheduler.step()
                model.train()
            else:
                model.eval()

            running_loss = 0.0
            running_corrects = 0

            for inputs, labels in dataloaders[phase]:
                inputs = inputs.to(device)
                labels = labels.to(device)
                # print(inputs.shape)

                optimizer.zero_grad()

                with torch.set_grad_enabled(phase == 'train'):
                    outputs = model(inputs)
                    _, preds = torch.max(outputs, 1)
                    loss = criterion(outputs, labels)

                    if phase == 'train':
                        loss.backward()
                        optimizer.step()

                running_loss += loss.item() * inputs.size(0)
                running_corrects += torch.sum(preds == labels.data)

            epoch_loss = running_loss / dataset_sizes[phase]
            epoch_acc = running_corrects.double() / dataset_sizes[phase]

            '''
            Grad cam generation for selected images
            '''

            grad_cam_epoch_image = []
            for i in range(len(example_list)):
                print("Reading example index {}".format(i))
                orig_image, preprocess_image, target_class = select_image(i)
                if orig_image != None:
                    grad_cam_epoch_layer = []
                    for layer_number in range(1, 10):
                        try:
                            print("Processing layer number {}".format(layer_number))
                            cam = generate_grad_cam(
                                model, preprocess_image, target_class, layer=layer_number)
                            cam, cam_im_on_image = apply_colormap_on_image(
                                orig_image, cam, colormap_name='hsv')
                            grad_cam_epoch_layer.append(cam_im_on_image)
                        except Exception as e:
                            break

                    print("Adding all layers grad cam to list {}".format(
                        len(grad_cam_epoch_layer)))
                    model = model.to(torch.device(device))
                    grad_cam_epoch_image.append(grad_cam_epoch_layer)
            if phase == 'train':
                epoch_information.append(grad_cam_epoch_image)

            print('{} Loss: {:.4f} Acc:{:.4f}'.format(
                phase, epoch_loss, epoch_acc))

            if phase == 'test' and epoch_acc > best_acc:
                best_acc = epoch_acc
                best_model = copy.deepcopy(model.state_dict())

            print()

    time_elapsed = time.time() - since
    print('Training complete in {:0f}m {:.0f}s'.format(
        time_elapsed // 60, time_elapsed % 60))
    print('Best val acc: {:4f}'.format(best_acc))

    model.load_state_dict(best_model)
    return model, epoch_information


def fetch_pretrained_model():
    model_ft = models.resnet50(pretrained=True)
    num_frts = model_ft.fc.in_features
    model_ft.fc = nn.Linear(num_frts, len(class_names))

    model_ft = model_ft.to(device)
    criterion = nn.CrossEntropyLoss()

    optimizer_ft = optim.SGD(model_ft.parameters(), lr=0.01, momentum=0.9)
    #optimizer_ft = optim.Adam(model_ft.parameters(), lr=1e-03, weight_decay=1e-02)
    exp_lr_scheduler = lr_scheduler.StepLR(
        optimizer_ft, step_size=7, gamma=0.1)

    return model_ft, optimizer_ft exp_lr_scheduler


model_ft_resnet50, epoch_information_resnet50 = train_model(
    model_ft, criterion, optimizer_ft, exp_lr_scheduler, num_epochs=20)
