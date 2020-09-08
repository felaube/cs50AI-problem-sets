Instructions to get the dataset:

Download the data set for this project and unzip it. Move the resulting gtsrb directory inside of your traffic directory.
https://cdn.cs50.net/ai/2020/x/projects/5/gtsrb.zip

For a smaller dataset, you can download a modified dataset that contains only 3 different types of road signs instead of 43.
https://cdn.cs50.net/ai/2020/x/projects/5/gtsrb-small.zip


I started working with the small dataset.

The first thing I tried, to get some familiarity with the functions, was to simply use the same network from handwriting.py,
with a few modifications such as the image size and the number of categories. I tried with 10 epochs and 100 epochs, both resulting in bad results,
with an accuracy of only 60%.

Looking up online about CNNs, I found out that a common practice is to append multiple layers of convolution and pooling,
in a way that as our output spatial volume decreases, our number of filters learned increases. So I added 3 convolution
layers, with 32, 64 and 128 layers, each one followed by a (2x2) max pooling. The result was also not satisfactory, with 62% of accuracy.

After that, I started adding different Conv2D layers, modifying the number of filters, the kernel size and the type of padding,
as I slowly increased the number of categories in the dataset.  

At the end, I was able to achieve a 97% accuracy on the regular sized dataset using 3 convolution layers, each followed by a 2 x 2 pooling,
1 fully conected layer with 512 units, and 1 output layer.
