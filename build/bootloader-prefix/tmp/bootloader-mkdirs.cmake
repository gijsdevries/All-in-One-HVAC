# Distributed under the OSI-approved BSD 3-Clause License.  See accompanying
# file Copyright.txt or https://cmake.org/licensing for details.

cmake_minimum_required(VERSION 3.5)

file(MAKE_DIRECTORY
  "/home/gijs/esp/esp-idf-v5.5.1/components/bootloader/subproject"
  "/home/gijs/Documents/espidfprojects/sensoren_klimaatkamer/build/bootloader"
  "/home/gijs/Documents/espidfprojects/sensoren_klimaatkamer/build/bootloader-prefix"
  "/home/gijs/Documents/espidfprojects/sensoren_klimaatkamer/build/bootloader-prefix/tmp"
  "/home/gijs/Documents/espidfprojects/sensoren_klimaatkamer/build/bootloader-prefix/src/bootloader-stamp"
  "/home/gijs/Documents/espidfprojects/sensoren_klimaatkamer/build/bootloader-prefix/src"
  "/home/gijs/Documents/espidfprojects/sensoren_klimaatkamer/build/bootloader-prefix/src/bootloader-stamp"
)

set(configSubDirs )
foreach(subDir IN LISTS configSubDirs)
    file(MAKE_DIRECTORY "/home/gijs/Documents/espidfprojects/sensoren_klimaatkamer/build/bootloader-prefix/src/bootloader-stamp/${subDir}")
endforeach()
if(cfgdir)
  file(MAKE_DIRECTORY "/home/gijs/Documents/espidfprojects/sensoren_klimaatkamer/build/bootloader-prefix/src/bootloader-stamp${cfgdir}") # cfgdir has leading slash
endif()
