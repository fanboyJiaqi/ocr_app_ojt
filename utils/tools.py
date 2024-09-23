import base64

def image_to_base64(image_path):
    """
    Hàm chuyển đổi ảnh từ file thành chuỗi base64.
    
    :param image_path: Đường dẫn tới file ảnh
    :return: Chuỗi base64 của ảnh
    """
    with open(image_path, "rb") as image_file:
        base64_string = base64.b64encode(image_file.read()).decode('utf-8')
    return base64_string
