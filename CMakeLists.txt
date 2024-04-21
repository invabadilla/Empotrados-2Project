cmake_minimum_required(VERSION 3.27)
project(Empotrados C)

set(CMAKE_C_STANDARD 11)

add_executable(Empotrados main.c
        test.c
        libbmp.c
        libbmp.h
)
