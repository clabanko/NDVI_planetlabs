import rasterio
import os
import numpy
import numpy as np

#This code calculates the NDVI index from Planet Labs images. You need to keep all the Planet Labs images ("tifs" ending with _SR) and the .xml metadata from each tile in the same directory. The code creates a new file with the same name, but with "ndvi" at the end. Be aware that once the NDVI are created they should be stroed in another directory. 
image_list=[]
directory = r'C:\planet labs imagery\20180919_3m'
for filename in os.listdir(directory):
    if filename.endswith(".tif") :
        #print(os.path.jo"in(filename))
        image_list.append(filename)
        image_array=np.asarray(image_list) 
    else:
        continue

xml_list=[]
directory = r'C:\planet labs imagery\20180919_3m'
for filename in os.listdir(directory):
    if filename.endswith(".xml") :
        #print(os.path.jo"in(filename))
        xml_list.append(filename)
        xml_array=np.asarray(xml_list) 
    else:
        continue


for image_file in image_list:
  imageName = image_file
  imagexml = "" #initialize your variable to be populated in the inner loop
  for xml in xml_list:
    if xml.startswith(imageName.split("_")[0]):
      imagexml = xml
      break #break out of the inner loop - we have a match
  if imagexml != "": #just to make sure we have something
    #generic naming
    outraster = imageName.replace(".tif", "_ndvi.tif")




# #image_file = "20180919_015945_103d_3B_AnalyticMS_SR.tif"
# for image_file in image_array:

    # Load red and NIR bands - note all PlanetScope 4-band images have band order BGRN
    with rasterio.open(image_file) as src:
        band_red = src.read(3)
    
    with rasterio.open(image_file) as src:
        band_nir = src.read(4)
        
    from xml.dom import minidom
    
    xmldoc = minidom.parse(imagexml)
    nodes = xmldoc.getElementsByTagName("ps:bandSpecificMetadata")
    
    # XML parser refers to bands by numbers 1-4
    coeffs = {}
    for node in nodes:
        bn = node.getElementsByTagName("ps:bandNumber")[0].firstChild.data
        if bn in ['1', '2', '3', '4']:
            i = int(bn)
            value = node.getElementsByTagName("ps:reflectanceCoefficient")[0].firstChild.data
            coeffs[i] = float(value)
            
    # Multiply by corresponding coefficients
    band_red = band_red * coeffs[3]
    band_nir = band_nir * coeffs[4]
    
    # Allow division by zero
    numpy.seterr(divide='ignore', invalid='ignore')
    
    # Calculate NDVI
    ndvi = (band_nir.astype(float) - band_red.astype(float)) / (band_nir + band_red)
    
    # Set spatial characteristics of the output object to mirror the input
    kwargs = src.meta
    kwargs.update(
        dtype=rasterio.float32,
        count = 1)
    
    # Create the files

    with rasterio.open(outraster, 'w', **kwargs) as dst:
            dst.write_band(1, ndvi.astype(rasterio.float32))
            
