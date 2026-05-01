from exif import Image
import sys

def extractionFunc(imagePath):
    try :
        with open(imagePath, 'rb') as imageFile:  
            #as imageFile takes the user data and converts it into something that the exif func can understand
            #then store it in a new var
            userImage = Image(imageFile)

            if userImage.has_exif: 
                #sometimes images are stripped away from their exif data // metadata, in social media platforms for example
                print("Metadata is present in the user image\n")
                for metadataName, metadataValue in userImage.get_all().items():
                    #iterate through the metadata to get each field and its value, date : 01/01/2000 for example
                    print(f"{metadataName} : {metadataValue}")
            
            else: print("the image has been stripped away from its metadata\n")

    except Exception as error:
        print(f"some kind of error occured, please check the path of the image/file || {error}\n" )

if __name__ == "__main__":
    if len(sys.argv) != 2:
        #user has to give 2 arguments, the name of the script and the path of the image
        print("command : python extractScript.py <image_path>.format (eg: python extractScript.py C:\\Users\\user\\Desktop\\image.jpg)\n")
        sys.exit(404)


imagePath = sys.argv[1]
#argv[0] is the name of the script, argv[1] is the path of the image
print("wait for extraction")
print(f"analyzing path : {imagePath}")
extractionFunc(imagePath)



