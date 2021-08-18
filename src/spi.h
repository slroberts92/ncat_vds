/**
 * @file spi.h
 * @author Steven Lane Roberts (slroberts@neptunetg.com)
 * @brief 
 * @version 0.1
 * @date 2021-03-01
 * 
 * @copyright Copyright (c) 2021
 * 
 */

#ifndef SPI_H
#define SPI_H

#ifdef __cplusplus
extern "C" {
#endif

void spi_enable(void);
void spi_disable(void);

void spi_init(void);

void spi_sendbyte(const uint8_t sendbyte);

void spi_sendbuffer(const uint8_t * const p_tx_buffer,
                    const size_t buf_len            );

void spi_read(uint8_t * const p_rx_buffer,
              const size_t buf_len      );

#ifdef __cplusplus
}
#endif

#endif /* SPI_H */
