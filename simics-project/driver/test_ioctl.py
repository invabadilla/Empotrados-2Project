import fcntl
import os

CHARACTER_DEVICE_DRIVER_PATH = "/dev/pci_capture_chr_dev-0"
WR_VALUE = 1074291041  # _IOW('a','a',int32_t *)
RD_VALUE = 2148033122  # _IOR('b','b',int32_t *)

def main():
    print("*********************************")
    print(">>> Opening character device")
    try:
        fd = os.open(CHARACTER_DEVICE_DRIVER_PATH, os.O_RDWR)
    except OSError as e:
        print("Cannot open character device file...")
        return

    print("*********************************")

    buffer = bytearray(4)
    fcntl.ioctl(fd, RD_VALUE, buffer)
    value = int.from_bytes(buffer, byteorder='little', signed=False)
    print(f"Read test_register: 0x{value:08x}")

    value = 0x19
    fcntl.ioctl(fd, WR_VALUE, value.to_bytes(4, byteorder='little', signed=False))
    print("Write test_register successfully done")

    print("*********************************")
    print(" >>> Closing character device")
    print("*********************************")
    os.close(fd)

if __name__ == "__main__":
    main()

#board.mb.phys_mem.write 0x250000014 0x1
#board.mb.nb.pci_bus.mem_space.write 0xf1000000 0x18 0x4
#run
#start-agent-manager
#agent_manager.connect-to-agent
#matic0.upload -executable /home/usuario/Documents/Empotrados-2Project/simics-project/driver/Makefile /home/simics/driver
#matic0.upload -executable /home/usuario/Documents/Empotrados-2Project/simics-project/driver/pci_capture_driver.c /home/simics/driver
#matic0.upload -executable /home/usuario/Documents/Empotrados-2Project/simics-project/driver/test_ioctl.c /home/simics/test_driver
#matic0.upload -executable /home/usuario/Documents/Empotrados-2Project/simics-project/driver/test_ioctl.py /home/simics/test_driver
#matic0.upload -executable -overwrite /home/usuario/Documents/Empotrados-2Project/filters.py /home/simics/scripts
#matic0.upload -executable /home/usuario/Documents/Empotrados-2Project/imagen_negativa.bmp /home/simics/images
#matic0.upload -executable /home/usuario/Documents/Empotrados-2Project/imagen_suavizada.bmp /home/simics/images
#matic0.upload -executable /home/usuario/Documents/Empotrados-2Project/blur-test-result.bmp /home/simics/images
#matic0.upload -executable /home/usuario/Documents/Empotrados-2Project/blur-test.bmp /home/simics/images
#matic0.upload -executable /home/usuario/Documents/Empotrados-2Project/negative-test-result.bmp /home/simics/images
#matic0.upload -executable /home/usuario/Documents/Empotrados-2Project/negative-test.bmp /home/simics/images
#matic0.upload -executable /home/usuario/Documents/Empotrados-2Project/R.bmp /home/simics/images
#matic0.upload -executable /home/usuario/Documents/Empotrados-2Project/restored_image.bmp /home/simics/images
#matic0.upload -executable /home/usuario/Documents/Empotrados-2Project/scared_cat.bmp /home/simics/images
#matic0.run "make"
#matic0.run "insmod /home/pci_capture_module.ko"
#matic0.run "lsmod"
#matic0.run "gcc -o /home/test_ioctl /home/test_ioctl.c"
#matic0.run "/home/test_ioctl"
#matic0.run "/home/test_ioctl"
#matic0.download-dir -overwrite /home/simics/images /home/usuario/Documents/Empotrados-2Project/
