<h1>Edge Detection Using the Dual Tree Complex Wavelet Transform</h1>

<img src="figures/merged.jpg" width=800px>

<div>
    In this project, I followed the methodology that  <a href="https://www.sciencedirect.com/science/article/abs/pii/S0165168409003107">Kare et al. (2010) </a>used to extract the strong edges from an ultrasound image. I then compared it to the Canny edge detection algorithm applied to the raw image, which the DTCWT method appears to outperform by a significant margin.</br></br>
</div>

The dual-tree complex wavelet transform (DTCWT) has several advantages over the discrete wavelet transform (DWT) in that it possesses:

<ol>
    <li><b>Approximate shift invariance</b>. This preserves the phase information of the original image, which is important in the context of ultrasound imaging. </li>
    <li><b>Increased directional sensitivity</b> - there are 6 directional components roughly corresponding to: 15, 45, 75, 105, 135, and 165 degrees whereas the DWT only provides the horizontal, vertical and diagonal components.</li>
    <br/>
</ol>
A good example that demonstrates this directional sensitivity is shown below:<br/>
<img src="./figures/lines.jpg" width=300px style="display:block; margin:auto;">
<br/>
Using the DWT:
<img src="./figures/lines_merged.png" width=400px style="display:block; margin:auto;"><br/>
Using the DTCWT:
<img src="./figures/lines_edges.png" width=700px style="display:block; margin:auto;"><br/>

Applied to the original ultrasound image:
<img src="figures/detected_edges.png">