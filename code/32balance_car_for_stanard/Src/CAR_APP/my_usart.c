#include "my_usart.h"
#include "stdlib.h"
#include <string.h>
User_USART BT_Data;		//接收数据

//初始化函数
void User_USART_Init(User_USART *Data)
{
		for(uint8_t i=0; i < RXBUFFER_LEN; i++)	Data->RxBuffer[i] = 0;
		Data->frame_head = 0xA5;
		Data->frame_tail = 0x5A;
		Data->Rx_flag = 0;
		Data->Rx_len = 0;
		Data->x = 0;
		Data->y = 0;
		Data->w = 0;
		Data->h = 0;
		Data->m = 0;
}

void BTData_Process(uint8_t *RxBuffer)
{
		//检查帧头帧尾
//		if(RxBuffer[0] != BT_Data.frame_head) return;
//		if(RxBuffer[5] != BT_Data.frame_tail) return;
		
//		BT_Data.x = (RxBuffer[3]<<8)|RxBuffer[2];
//		BT_Data.y = (RxBuffer[5]<<8)|RxBuffer[4];
//		BT_Data.w = (RxBuffer[7]<<8)|RxBuffer[6];
//		BT_Data.h = (RxBuffer[9]<<8)|RxBuffer[8];
	  memcpy( BT_Data.bufferes, RxBuffer, 9);
    memcpy(&BT_Data.x,  BT_Data.bufferes, 4);
    memcpy( BT_Data.linees,  BT_Data.bufferes + 4, 4);
//	   memcpy(BT_Data.bufferes,RxBuffer,6);
//     memcpy(BT_Data.linees,BT_Data.bufferes,5);
	   BT_Data.resulte[1]= BT_Data.linees[0];
	   BT_Data.resulte[2]= BT_Data.linees[1];
	   BT_Data.resulte[3]= BT_Data.linees[2];
	   BT_Data.resulte[4]= BT_Data.linees[3];
		 BT_Data.resulte[0]= BT_Data.x;
     
	
//		if (BT_Data.x>127) BT_Data.x-=255;
//		if (abs(BT_Data.x)<10) BT_Data.x = 0;//消除转向抖动
//		if (BT_Data.y>127) BT_Data.y-=255;
//		if (abs(BT_Data.y)<10) BT_Data.y = 0;//消除前进抖动
}

