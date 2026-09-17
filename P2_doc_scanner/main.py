'''
This is the first major project (second technicallly if u consider vegetation detector too) for the roadmap given in roadmap.md
The goal is to build a document scanner pipeline using opencv2
load input image(s)
detect the papaer
find outline
find corners
fix the perspective transform 
present the scanned document in output folder 

proposed preliminary pipeline is 
Photograph
   ↓
Grayscale
   ↓
Blur
   ↓
Canny
   ↓
Contour detection
   ↓
Find document contour
   ↓
approxPolyDP()
   ↓
4 corners
   ↓
Perspective transform
   ↓
Scanned document
'''