#include "CAR_TASK.h"
#include "tim.h"
#include "mpu6050.h"
#include "echo.h"
#include "stdio.h"
#include "inv_mpu.h"
#include "contrl.h"
#include "delay.h"
#include "my_usart.h"
#include "oled.h"
#define RXBUFFER_LEN 20

int ii=0;
int flag=0;
int time =0;
struct mpu6050_data outMpu;
int Balance_PWm,Velocity_Pwm,Turn_Pwm;//ֱ�������ٶȻ������pwm
int Encoder_left,Encoder_right;//������ֵ
int Motor1,Motor2;//���ҵ�����������pwm
float  Movement = 0;//Ŀ���ٶ�
float straight_speed=0.0f;
int Contrl_Turn = 0;//
//int hf_Mode = 1;//С������ģʽ 0 ң��ģʽ��1 ����ģʽ��2 Ѳ��ģʽ��
//int Distance;//�����������ֵ
//�������ݲɼ�����
void diaodian(void);
void Car_Task_200HZ(void)
{
	
	//static struct mpu6050_data Last_Data;
	mpu_dmp_get_data(&outMpu.pitch,&outMpu.roll,&outMpu.yaw);
//	distance(&straight_speed);
}


/**************************************************************************************************************
*������:Car_Task_100HZ(void)
*���ܣ�100hz����
*�β�:��
*����ֵ:��
*ȷ��ֱ�������ٶȻ���ת���Լ����õ��pwm
**************************************************************************************************************/
void Car_Task_100HZ(void)
{ if(ii==0)
 { HAL_Delay(4000);
 ii++;
 }
	Encoder_left = Read_Encoder(1);
	Encoder_right = -Read_Encoder(2);//��������
	Balance_PWm =Vertical_Ring_PD(outMpu.pitch,outMpu.gyro_y);//ֱ����
	Movement = straight_speed/2.4;
		if(ii==1)
	{
	straight_speed=-27.0f;
	xunji();
	outner(0);
	}
	Turn_Pwm = Vertical_turn_PD(Contrl_Turn,outMpu.gyro_z);
	Velocity_Pwm = Vertical_speed_PI(Encoder_left,Encoder_right,outMpu.pitch,Movement );//�ٶȻ�
	Motor1 = Balance_PWm+Velocity_Pwm-Turn_Pwm;
	Motor2 = Balance_PWm+Velocity_Pwm+0.8*Turn_Pwm;
	diaodian();
	PWM_Limiting(&Motor1,&Motor2);//pwm�޷�
	if(Turn_off(outMpu.pitch)==1){//���䱣��
		Motor1 = 0;           
		Motor2 = 0; 
	}
	Set_PWM(Motor1,Motor2);
}



/**************************************************************************************************************
*������:Car_Task_5HZ(void)
*���ܣ�5hz����
*�β�:��
*����ֵ:��
*ȷ��ֱ�������ٶȻ���ת���Լ����õ��pwm
**************************************************************************************************************/
void Car_Task_5HZ(void)
	{
		ii=1;
		//Getdistance();
//		printf("acc_x = %d\n",outMpu.acc_x);
//	printf("acc_y = %d\n",outMpu.acc_y);
//	printf("acc_z = %d\n",outMpu.acc_z);
//	printf("gyro_x = %d\n",outMpu.gyro_x);
//	printf("gyro_y = %d\n",outMpu.gyro_y);
//	printf("gyro_z = %d\n",outMpu.gyro_z);
//	printf("pitch = %f\n",outMpu.pitch);
//	printf("roll = %f\n",outMpu.roll);
//	printf("yaw = %f\n",outMpu.yaw);
//	printf("\r\n");
//		
//			printf("Encoder_left = %d\n",Encoder_left);
//			printf("Encoder_right = %d\n",Encoder_right);
//			TIM2->CNT = 0;
//			TIM4->CNT = 0;
	}
	
	void Car_Task_Interaction(void)
	{
		if(outMpu.pitch<0) 
		{
			OLED_ShowChar(46,1,'-',2);
			OLED_ShowFloat(50,1,-outMpu.pitch,3,2);
		}
		else 
		{
			OLED_ShowChar(46,1,' ',2);
			OLED_ShowFloat(50,1,outMpu.pitch,3,2);
		}
		
		if(outMpu.roll<0) 
		{
			OLED_ShowChar(46,3,'-',2);
			OLED_ShowFloat(50,3,-outMpu.roll,3,2);
		}
		else 
		{
			OLED_ShowChar(46,3,' ',2);
			OLED_ShowFloat(50,3,outMpu.roll,3,2);
		}
		
		if(outMpu.yaw<0) 
		{
			OLED_ShowChar(46,5,'-',2);
			OLED_ShowFloat(50,5,-outMpu.yaw,3,2);
		}
		else 
		{
			OLED_ShowChar(46,5,' ',2);
			OLED_ShowFloat(50,5,outMpu.yaw,3,2);
		}
	}
	
	void motor(void)
	{
    straight(-30,&Movement);
	}
	
  	void  xunji(void)
	{
	Contrl_Turn=(BT_Data.resulte[0]+BT_Data.resulte[2]-250)/2;

	}
			void outner(int x)//1Ϊ��һȦΪ��Ȧ  3Ϊ�ڶ�ȦΪ��Ȧ  .......
	{
	
		if((BT_Data.resulte[1]!=0||BT_Data.resulte[4]==0)&&flag==0)
{
   flag=1;	 	 
}
if(flag==1&&time<100)
{
 	Contrl_Turn=0;
	time++;
if(time==100) flag=2;
}
	}
		void diaodian(void)
		{
		
		if(BT_Data.resulte[4]>=2)
		{
		Motor1=0;
		Motor2=0;
		}
		}