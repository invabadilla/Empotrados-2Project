#include <stdio.h>
#include <stdlib.h>
#include "libbmp.h"

// Función para leer un archivo BMP y almacenar su contenido en un buffer
int readImageFile(char *fileName, char **buffer, int *sizeOfBuffer) {
    FILE* fp = fopen(fileName, "rb");

    if (fp == NULL) {
        fprintf(stderr, "No se pudo abrir el archivo: %s", fileName);
        return 1;
    }

    fseek(fp, 0L, SEEK_END);
    *sizeOfBuffer = ftell(fp);
    fseek(fp, 0L, SEEK_SET);
    *buffer = (char *)malloc(*sizeOfBuffer);
    fread(*buffer, *sizeOfBuffer, 1, fp);
    fclose(fp);
    return 0;
}

// Función para guardar los valores ASCII en un array
void saveToASCIIArray(char *buffer, int sizeOfBuffer, int *asciiArray) {
    for (int i = 0; i < sizeOfBuffer; i++) {
        asciiArray[i] = (unsigned char)buffer[i];
    }
}

// Función para reconstruir la imagen BMP a partir del array de valores ASCII
char* restoreFromASCIIArray(int *asciiArray, int sizeOfArray) {
    char *buffer = (char *)malloc(sizeOfArray * sizeof(char));
    if (buffer == NULL) {
        fprintf(stderr, "No se pudo asignar memoria para el buffer\n");
        return NULL;
    }

    for (int i = 0; i < sizeOfArray; i++) {
        buffer[i] = (char)asciiArray[i];
    }

    return buffer;
}

// Función para escribir el buffer en un archivo BMP
int writeImageFile(char *fileName, char *buffer, int sizeOfBuffer) {
    FILE* fp = fopen(fileName, "wb");

    if (fp == NULL) {
        fprintf(stderr, "No se pudo abrir el archivo: %s", fileName);
        return 1;
    }

    fwrite(buffer, sizeOfBuffer, 1, fp);
    fclose(fp);
    return 0;
}


int main() {
    char *buffer;
    int sizeOfBuffer;
    int *asciiArray;
    char *restoredBuffer;

    // Leer la imagen BMP y almacenarla en un buffer
    if (readImageFile("../R.bmp", &buffer, &sizeOfBuffer) == 0) {
        // Crear un array para almacenar los valores ASCII
        asciiArray = (int *)malloc(sizeOfBuffer * sizeof(int));
        if (asciiArray == NULL) {
            fprintf(stderr, "Error: No se pudo asignar memoria para el array ASCII\n");
            free(buffer);
            return 1;
        }

        // Guardar los valores ASCII en el array
        saveToASCIIArray(buffer, sizeOfBuffer, asciiArray);

        // Restaurar la imagen BMP a partir del array de valores ASCII
        restoredBuffer = restoreFromASCIIArray(asciiArray, sizeOfBuffer);

        // Escribir la imagen restaurada en un nuevo archivo BMP
        if (writeImageFile("../restored_image.bmp", restoredBuffer, sizeOfBuffer) == 0) {
            printf("Imagen BMP restaurada exitosamente.\n");
        } else {
            printf("Error al escribir la imagen restaurada en el archivo.\n");
        }

        // Liberar la memoria asignada al buffer y al array ASCII
        free(buffer);
        free(asciiArray);
        free(restoredBuffer);
    }

    /*bmp_img img_restored;
    const char *input_file = "C:/Users/PC/Desktop/Empotrados/restored_image.bmp";
    const char *output_file = "C:/Users/PC/Desktop/Empotrados/test_image_copy.bmp";

    // Leer la imagen
    if (bmp_img_read(&img_restored, input_file) != BMP_OK) {
        fprintf(stderr, "Error al abrir la imagen: %s\n", input_file);
        return 1;
    }

    // Escribir la imagen sin modificar
    if (bmp_img_write(&img_restored, output_file) != BMP_OK) {
        fprintf(stderr, "Error al guardar la imagen: %s\n", output_file);
        bmp_img_free(&img_restored);
        return 1;
    }

    // Aplicar filtro de negativo a la imagen restaurada
    for (size_t y = 0; y < abs(img_restored.img_header.biHeight); y++) {
        for (size_t x = 0; x < img_restored.img_header.biWidth; x++) {
            bmp_pixel *pxl = &img_restored.img_pixels[y][x];
            pxl->red = 255 - pxl->red;
            pxl->green = 255 - pxl->green;
            pxl->blue = 255 - pxl->blue;

        }

    }


    // Guardar la imagen con el filtro de negativo aplicado
    if (bmp_img_write(&img_restored, "C:/Users/PC/Desktop/Empotrados/restored_image_negative.bmp") != BMP_OK) {
        fprintf(stderr, "Error al guardar la imagen con filtro de negativo\n");
        bmp_img_free(&img_restored);
        return 1;
    }

    // Aplicar filtro de suavizado a la imagen restaurada (puedes implementar tu propia función de suavizado aquí)

    // Guardar la imagen con el filtro de suavizado aplicado

    // Liberar la memoria utilizada por la imagen restaurada
    bmp_img_free(&img_restored);*/

    return 0;
}
