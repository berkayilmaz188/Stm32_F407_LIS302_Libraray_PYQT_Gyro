# Description Turkish 

Projede STM32 F407 Discovery üzerinde bulunan lis302 imu sensörüne SPI ile veri okumak için register kütüphanesi yazılmıştır. 

Sensörden aldığım verileri F407 üzerinde bulunan USB Device ile verileri bilgisayara aktardım.

Usb ile gelen X Y Z verileri animasyon kısmı hazır alınan PyQt'de arayüzleştirdildi. Pitch Roll hesaplarını PyQt tarafında yapılarak stm tarafına extra yük bindirilmemesi hedeflendi.

# Description English

In the project, a register library has been written to read data from the LIS302 IMU sensor on the STM32 F407 Discovery using SPI.

The data obtained from the sensor has been transferred to the computer using the USB device on the F407.

The X, Y, Z data received via USB was visualized in the animation part, which was prepared and implemented in the PyQt interface. The calculation of Pitch and Roll was performed on the PyQt side, aiming to avoid additional load on the STM side.

# Pictures

![1](https://r.resimlink.com/qThQ2x-.png)

![2](https://r.resimlink.com/ldyJ_tWv7fj.png)

![3](https://r.resimlink.com/9WAQe.png)

