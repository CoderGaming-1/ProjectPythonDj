from django.test import TestCase
import os

# Create your tests here.
print('helu')

# # Lấy đường dẫn thư mục hiện tại
# current_directory = os.getcwd()

# # Nối đường dẫn thư mục hiện tại với tên tệp để tạo đường dẫn tuyệt đối
# absolute_path = os.path.join(current_directory, 'models.py')

# print(absolute_path)

# content = ''
# with open('Patient/models.py', 'rb') as file_in:
#     content = file_in.read().replace(b'\x00', b'')
#     print(content)
# with open('Patient/models.py', 'wb') as file_out:
#     file_out.write(content)

# content = []
# with open('Patient/models.py', 'r') as file_in:
#     content = file_in.readlines()


# new_content = [] 
# for line in content:
#     print(line)
#     clean_line = line.replace('\x00', '')
#     new_content.append(clean_line)

# with open('Patient/models.py', 'w') as file_out:
#     for line in new_content:
#         file_out.write(line)