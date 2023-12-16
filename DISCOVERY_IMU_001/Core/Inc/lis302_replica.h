/*
 * lis302_replica.h
 *
 *  Created on: Aug 10, 2023
 *      Author: berkay.yilmaz
 */

#ifndef INC_LIS302_REPLICA_H_
#define INC_LIS302_REPLICA_H_

#include "main.h"
#include "usb_device.h"
#include "usbd_cdc_if.h"

#define LIS302DL_CTRL_REG1   0x20
#define LIS302DL_CTRL_REG1_2G_CONF 0x47
#define LIS302DL_CTRL_REG1_8G_CONF 0x67

#define LIS302DL_OUT_X       0x29
#define LIS302DL_OUT_Y       0x2B
#define LIS302DL_OUT_Z       0x2D

#define LIS302DL_READ        0x80


void lis302dl_init(SPI_HandleTypeDef *hspi);
void read_lis302(SPI_HandleTypeDef *hspi, uint8_t *u8X, uint8_t *u8Y, uint8_t *u8Z);
void compute_orientation(uint8_t u8X, uint8_t u8Y, uint8_t u8Z, float *pitch, float *roll);
void transmit_data(uint8_t u8X, uint8_t u8Y, uint8_t u8Z);




#endif /* INC_LIS302_REPLICA_H_ */
