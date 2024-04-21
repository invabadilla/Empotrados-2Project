from PIL import Image, ImageFilter

def negative_test():
    imagen = Image.open('negative-test.bmp')
    imagen_negativa = Image.eval(imagen, lambda x: 255 - x)
    imagen_negativa.save('negative-test-result.bmp')

def blur_test():
    imagen = Image.open('blur-test.bmp')
    imagen_suavizada = imagen.filter(ImageFilter.SMOOTH)
    imagen_suavizada = imagen_suavizada.filter(ImageFilter.SMOOTH)
    imagen_suavizada.save('blur-test-result.bmp')


# Función para leer un archivo BMP y almacenar su contenido en un buffer
def read_image_file(file_name):
    with open(file_name, 'rb') as f:
        return f.read()

# Función para escribir el buffer en un archivo BMP
def write_image_file(file_name, buffer):
    with open(file_name, 'wb') as f:
        f.write(buffer)

# Leer la imagen BMP y almacenarla en un buffer
buffer = read_image_file("scared_cat.bmp")

# Guardar los valores ASCII en una lista
ascii_array = [byte for byte in buffer]

# Restaurar la imagen BMP a partir de la lista de valores ASCII
restored_buffer = bytes(ascii_array)

# Escribir la imagen restaurada en un nuevo archivo BMP
write_image_file("restored_image.bmp", restored_buffer)

print("Imagen BMP restaurada exitosamente.")


# Abrir la imagen BMP
imagen = Image.open('restored_image.bmp')

# Aplicar filtro negativo
imagen_negativa = Image.eval(imagen, lambda x: 255 - x)

# Aplicar filtro de suavizado
imagen_suavizada = imagen.filter(ImageFilter.SMOOTH)

# Guardar las imágenes resultantes
imagen_negativa.save('imagen_negativa.bmp')
imagen_suavizada.save('imagen_suavizada.bmp')

negative_test()
blur_test()
