from PIL import Image, ImageFilter
import fcntl
import os

CHARACTER_DEVICE_DRIVER_PATH = "/dev/pci_capture_chr_dev-0"
WR_VALUE = 1074291041  # _IOW('a','a',int32_t *)
RD_VALUE = 2148033122  # _IOR('b','b',int32_t *)

def negative_test():
    imagen = Image.open('../images/negative-test.bmp')
    imagen_negativa = Image.eval(imagen, lambda x: 255 - x)
    imagen_negativa.save('../images/negative-test-result.bmp')

def blur_test():
    imagen = Image.open('../images/blur-test.bmp')
    imagen_suavizada = imagen.filter(ImageFilter.SMOOTH)
    imagen_suavizada = imagen_suavizada.filter(ImageFilter.SMOOTH)
    imagen_suavizada.save('../images/blur-test-result.bmp')


# Función para leer un archivo BMP y almacenar su contenido en un buffer
def read_image_file(file_name):
    with open(file_name, 'rb') as f:
        return f.read()

# Función para escribir el buffer en un archivo BMP
def write_image_file(file_name, buffer):
    with open(file_name, 'wb') as f:
        f.write(buffer)

# Leer la imagen BMP y almacenarla en un buffer
#buffer = read_image_file("../images/R.bmp")

# Guardar los valores ASCII en una lista
#ascii_array = [byte for byte in buffer]
print("*********************************")
print(">>> Opening character device")
try:
    fd = os.open(CHARACTER_DEVICE_DRIVER_PATH, os.O_RDWR)
except OSError as e:
    print("Cannot open character device file...")
    
print("*********************************")

value = 0x0
fcntl.ioctl(fd, WR_VALUE, value.to_bytes(4, byteorder='little', signed=False))

buffer = bytearray(4)
fcntl.ioctl(fd, RD_VALUE, buffer)
value = int.from_bytes(buffer, byteorder='little', signed=False)
print("Value: " + str(value))
#value = 1607862
ascii_array = [None] * value

for i in range(value):
    j = 0x18 + i
    fcntl.ioctl(fd, WR_VALUE, j.to_bytes(4, byteorder='little', signed=False))

    buffer = bytearray(4)
    fcntl.ioctl(fd, RD_VALUE, buffer)
    j = int.from_bytes(buffer, byteorder='little', signed=False)
    ascii_array[i] = j
    if (i % 10000 == 0):
        print(i)
   



# Restaurar la imagen BMP a partir de la lista de valores ASCII
restored_buffer = bytes(ascii_array)

# Escribir la imagen restaurada en un nuevo archivo BMP
write_image_file("../images/restored_image.bmp", restored_buffer)

print("Imagen BMP restaurada exitosamente.")


# Abrir la imagen BMP
imagen = Image.open('../images/restored_image.bmp')

# Aplicar filtro negativo
imagen_negativa = Image.eval(imagen, lambda x: 255 - x)

# Aplicar filtro de suavizado
imagen_suavizada = imagen.filter(ImageFilter.SMOOTH)

# Guardar las imágenes resultantes
imagen_negativa.save('../images/imagen_negativa.bmp')
imagen_suavizada.save('../images/imagen_suavizada.bmp')

negative_test()
blur_test()
