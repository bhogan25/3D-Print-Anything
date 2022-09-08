

def serialize_image(imageFilePathName)
    with open(imageFilePathName, 'rb', encoding="utf-8") as file:
        image = file.read()
    return image