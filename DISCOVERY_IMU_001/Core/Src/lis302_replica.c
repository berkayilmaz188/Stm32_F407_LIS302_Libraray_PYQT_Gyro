/*
 * lis302_replica.c
 *
 *  Created on: Aug 10, 2023
 *      Author: berkay.yilmaz
 */


#include "lis302_replica.h"
#include <math.h>


#define LIS302DL_CS_PIN      GPIO_PIN_3
#define LIS302DL_CS_GPIO_PORT GPIOE

#define RAD_TO_DEG  (180.0 / M_PI)


#define CONNECT_LIS302()    HAL_GPIO_WritePin(LIS302DL_CS_GPIO_PORT, LIS302DL_CS_PIN, GPIO_PIN_RESET)
#define DISCONNECT_LS302()  HAL_GPIO_WritePin(LIS302DL_CS_GPIO_PORT, LIS302DL_CS_PIN, GPIO_PIN_SET)


// Init fonctions
static void lis302dl_write_reg(SPI_HandleTypeDef *hspi, uint8_t reg, uint8_t value) {
  CONNECT_LIS302() ;
  HAL_SPI_Transmit(hspi, &reg, 1, HAL_MAX_DELAY);
  HAL_SPI_Transmit(hspi, &value, 1, HAL_MAX_DELAY);
  DISCONNECT_LS302();
}

void lis302dl_init(SPI_HandleTypeDef *hspi) {
  lis302dl_write_reg(hspi, LIS302DL_CTRL_REG1, LIS302DL_CTRL_REG1_2G_CONF);
}


//Read sensor data fonctions
void read_lis302(SPI_HandleTypeDef *hspi, uint8_t *u8X, uint8_t *u8Y, uint8_t *u8Z) {
  uint8_t raw_data;

  CONNECT_LIS302();
  uint8_t out_x_address = LIS302DL_OUT_X + LIS302DL_READ;
  HAL_SPI_Transmit(hspi, &out_x_address, 1, HAL_MAX_DELAY);
  HAL_SPI_Receive(hspi, &raw_data, 1, HAL_MAX_DELAY);
  DISCONNECT_LS302();
  *u8X = raw_data;

  CONNECT_LIS302();
  uint8_t out_y_address = LIS302DL_OUT_Y + LIS302DL_READ;
  HAL_SPI_Transmit(hspi, &out_y_address, 1, HAL_MAX_DELAY);
  HAL_SPI_Receive(hspi, &raw_data, 1, HAL_MAX_DELAY);
  DISCONNECT_LS302();
  *u8Y = raw_data;

  CONNECT_LIS302();
  uint8_t out_z_address = LIS302DL_OUT_Z + LIS302DL_READ;
  HAL_SPI_Transmit(hspi, &out_z_address, 1, HAL_MAX_DELAY);
  HAL_SPI_Receive(hspi, &raw_data, 1, HAL_MAX_DELAY);
  DISCONNECT_LS302();
  *u8Z = raw_data;
}

// USB Transmit Fonctions
void transmit_data(uint8_t u8X, uint8_t u8Y, uint8_t u8Z) {
  uint8_t DataToSend[100];
  sprintf((char *)DataToSend, "X:%u,Y:%u,Z:%u\r\n", u8X, u8Y, u8Z);
  CDC_Transmit_FS(DataToSend, strlen((char *)DataToSend));
}

// Calculate Pitch Roll Fonctions
void compute_orientation(uint8_t u8X, uint8_t u8Y, uint8_t u8Z, float *pitch, float *roll) {

  float x = (u8X / 127.5f - 1.0f) * 2.0f; // -2g to +2g
  float y = (u8Y / 127.5f - 1.0f) * 2.0f; // -2g to +2g
  float z = (u8Z / 127.5f - 1.0f) * 2.0f; // -2g to +2g

  // Hesaplamalar radyan cinsinden olacak
  *pitch = atan2f(y, sqrtf(x * x + z * z));
  *roll = atan2f(-x, sqrtf(y * y + z * z));

  // Radyan cinsinden dereceye dönüşüm
  *pitch *= 180.0f / M_PI;
  *roll *= 180.0f / M_PI;
}






