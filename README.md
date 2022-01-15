# CS440-Intro-AI-Project-4

Summary:

The purpose of this assignment is to demonstrate and explore some basic techniques in supervised learning and computer vision.

Typically, a color image is represented by a matrix of 3-component vectors, where Image[x][y] = (r,g,b) indicates that the pixel at position (x, y) has color (r, g, b) where r represents the level of red, g of green, and b blue respectively, as values between 0 and 255. A classical color to gray conversion formula is given by
Gray(r, g, b) = 0.21r + 0.72g + 0.07b,

where the resulting value Gray(r,g,b) is between 0 and 255, representing the corresponding shade of gray (from totally black to completely white).

Note that converting from color to grayscale is (with some exceptions) losing information. For most shades of gray, there will be many (r, g, b) values that correspond to that same shade.

For the purpose of this assignment, you are to take a single color image (of reasonable size and interest - check with me if you’re uncertain). By converting this image to black and white, you have useful data capturing the correspondence between color images and black and white images. We will use the left half of each image as training data, and the right half of each image as testing data. You will implement the basic model described below to try to re-color the right half of the black and white image based on the color/grayscale correspondence of the left half, and as usual, try to do something better.

MORE INFO: Assignment4-440.pdf

FINAL REPORT: AI_4.pdf
