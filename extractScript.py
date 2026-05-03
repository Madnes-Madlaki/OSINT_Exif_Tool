from exif import Image
import sys
import json
import datetime
import requests

metadata_dictionary = {}

def extractionFunc(imagePath):
    try :
        latitude = None
        longitude = None
        latitude_ref = None
        longitude_ref = None
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

                    #storing each metadata in a dictionary
                    metadata_dictionary[metadataName] = str(metadataValue)

                    #creating the google maps link section
                    if metadataName == 'gps_latitude':
                        latitude = metadataValue
                    elif  metadataName == 'gps_latitude_ref':
                        latitude_ref = metadataValue

                    elif metadataName == 'gps_longitude':
                        longitude = metadataValue
                    elif metadataName == 'gps_longitude_ref':
                        longitude_ref = metadataValue

                if latitude and latitude_ref and longitude and longitude_ref:
                    latitude_degrees, latitude_minutes, latitude_secondes = latitude
                    longitude_degrees, longitude_minutes, longitude_secondes = longitude

                    latitude_decimal = gpsMetadata_intoDecimal(latitude_degrees, latitude_minutes, latitude_secondes, latitude_ref)
                    longitude_decimal = gpsMetadata_intoDecimal(longitude_degrees, longitude_minutes, longitude_secondes, longitude_ref)
                    latitude_decimal = round(latitude_decimal, 6)
                    longitude_decimal = round(longitude_decimal, 6)
                    link = f"https://www.google.com/maps?q={latitude_decimal},{longitude_decimal}"

                    metadata_dictionary['google_mapsLink'] = link
                    metadata_dictionary['gps_longitude_decimal'] = longitude_decimal  
                    metadata_dictionary['gps_latitude_decimal'] = latitude_decimal    

                    geoCodedAddress = adressGeocoding(latitude_decimal, longitude_decimal)
                    metadata_dictionary['geoCoded_Address'] = geoCodedAddress

                else: print("no gps data found")

                 #Dictionnary contunuity section, open a json file and store what we extracted into the dictionary in it
                outputFile = f"metadata_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
                with open(outputFile, 'w') as fileVar:
                    json.dump(metadata_dictionary, fileVar, indent=4)
                print("metadata has been saved into a json file")
                
                return link

            else: print("the image has been stripped away from its metadata\n")

    except Exception as error:
        print(f"some kind of error occured, please check the path of the image/file || {error}\n" )

def gpsMetadata_intoDecimal(degrees, minutes, seconds, ref):
    decimal = degrees + minutes / 60 + seconds / 3600
    if ref in ['S', 'W']:
        decimal = -decimal
    return decimal
    #the exif library gives the coordinates in DMS format, we need to handle this within the function

def adressGeocoding(latitude, longitude):
    #we'll just take the coords the gps function gives us and convert it into a readable address
    try:
        link2 = f"https://nominatim.openstreetmap.org/reverse?lat={latitude}&lon={longitude}&format=json&zoom=18"
        response = requests.get(link2, headers={'User-Agent': 'OSINT_Metadata_Tool/1.0'}, timeout=5)
        #get the request to the link2, timeout after 5s if no response
        if response.status_code == 200:
            outputed_data = response.json()
            #get only the address, if no address return address not found
            return outputed_data.get('display_name', 'address not found')

        else: 
            return 'addressGeocoding not working'

    except requests.exceptions.Timeout:
        return 'Too much latency, try later'
    except requests.exceptions.ConnectionError:  
        return 'No internet connection, try later' 
        
    except Exception as error:  
        #:50 to avoid way too long error messages
        return f'Geocoding failed: {str(error)[:50]}'  


if __name__ == "__main__":
    if len(sys.argv) != 2:
        #user has to give 2 arguments, the name of the script and the path of the image
        print("command : python extractScript.py <image_path>.format (eg: python extractScript.py C:\\Users\\user\\Desktop\\image.jpg)\n")
        sys.exit(404)


    imagePath = sys.argv[1]
    #argv[0] is the name of the script, argv[1] is the path of the image
    print("*"*50)
    print("wait for extraction\n")
    print(f"analyzing path : {imagePath}\n")
    print("*"*50)
    link = extractionFunc(imagePath)
    print("\n" + "*"*50)
    print(f"{link}")
    print("*"*50)



