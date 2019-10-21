#ifndef __TOUCHSCREEN_H_
#define __TOUCHSCREEN_H_

#include "stdbool.h"
#include <stdint.h>
#include <stdlib.h>

enum {
    TOUCHSCREEN_TYPE_NS2009 = 0,
    TOUCHSCREEN_TYPE_FT62XX = 1,
};

typedef enum{
    TOUCHSCREEN_STATUS_IDLE =0,
    TOUCHSCREEN_STATUS_RELEASE,
    TOUCHSCREEN_STATUS_PRESS,
    TOUCHSCREEN_STATUS_MOVE
} touchscreen_type_t;

int touchscreen_init(void* arg);
int touchscreen_read(int* type, int* x, int* y);
int touchscreen_deinit();
int touchscreen_calibrate(int w, int h, int* cal);
bool touchscreen_is_init();
int ft52xx_hal_i2c_recv(const uint8_t *send_buf, size_t send_buf_len, uint8_t *receive_buf, size_t receive_buf_len);

/////////////// HAL ////////////////////

#include "machine_i2c.h"
#include "gc.h"
#include "mp.h"
#include "stdlib.h"

#define CALIBRATION_SIZE 7

typedef struct 
{
    machine_hard_i2c_obj_t* i2c;
    int calibration[CALIBRATION_SIZE];          // 7 Bytes
    uint8_t type;
} touchscreen_config_t;

//TODO: replace heap with GC
// #define touchscreen_malloc(p) m_malloc(p)
// #define touchscreen_free(p) m_free(p, gc_nbytes(p))
#define touchscreen_malloc(p) malloc(p)
#define touchscreen_free(p) free(p)

#endif

