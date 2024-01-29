/*****************************************************************************
 * main.c
 *****************************************************************************/

#include "main.h"
#include <stdlib.h>
#include <stdio.h>
#include <sys/platform.h>
#include "adi_initialize.h"
#include "sound_array.h"
#include <cycle_count.h>
#include <math.h>
#include <def21489.h>
#include <sru21489.h>
#include <SYSREG.h>


/******************************************************************************
 * Delay, Echo, Compressor effect parameters
 *****************************************************************************/
#define SAMPLE_RATE 44100
#define DELAY_TIME 0.25
#define DELAY_SAMPLES (int)(DELAY_TIME * SAMPLE_RATE)
#define GAIN 0.3
/******************************************************************************
 * Noise Gate effect parameter
 *****************************************************************************/
#define THRESHOLD 500
/******************************************************************************
 * Volume Pedal effect parameter
 *****************************************************************************/
#define PEDAL_POSITION 0.7
/******************************************************************************
 * Tape Saturation effect parameter
 *****************************************************************************/
#define SATURATION_FACTOR 0.7
/******************************************************************************
 * Envelope Filter effect parameter
 *****************************************************************************/
#define ALPHA 0.1
#define DT 1/SAMPLE_RATE
/******************************************************************************
 * Tremolo effect parameter
 *****************************************************************************/
#define DEPTH 0.9
#define FLFO 5.0
#define M_PI 3.14159265358979323846
/******************************************************************************
 * Override and Distorsion effect parametes
 *****************************************************************************/
#define GI 0.005
#define GO 2000.0
/******************************************************************************
 * Variables for code profiling
 *****************************************************************************/
cycle_t start_count;
cycle_t final_count;

static char extra_heap[716800];

int main(int argc, char *argv[])
{

	adi_initComponents();
	pm int * output_signal = NULL;
	FILE * file;
	int index = 0, uid = 999; /* arbitrary user id for heap */
	/* Install extra_heap[] as a heap */
	index = heap_install(extra_heap, sizeof(extra_heap), uid);
	if (index < 0)
	{
		printf("installation failed\n");
		return 1;
	}

	output_signal = (pm int *)heap_malloc(index, sound_wav_len*sizeof(int));
	if(output_signal == NULL)
	{
		printf("Memory allocation of output_signal failed!");
		return -1;
	}

	for(int i = 0; i < sound_wav_len; i++)
		output_signal[i] = 0;

	loading_bar();
	START_CYCLE_COUNT(start_count);
	// Uncomment one by one effect!
	//delay(sound_wav, output_signal, sound_wav_len);
	//echo(sound_wav, output_signal, sound_wav_len);
	//compressor(sound_wav, output_signal, sound_wav_len);
	//noise_gate(sound_wav, output_signal, sound_wav_len);
	//envelope_filter(sound_wav, output_signal, sound_wav_len);
	//volume_pedal(sound_wav, output_signal, sound_wav_len);
	//tape_saturation(sound_wav, output_signal, sound_wav_len);
	//octave_up(sound_wav, output_signal, sound_wav_len);
	tremolo(sound_wav, output_signal, sound_wav_len);
	//override(sound_wav, output_signal, sound_wav_len);
	//distorsion(sound_wav, output_signal, sound_wav_len);
	STOP_CYCLE_COUNT(final_count, start_count);
	PRINT_CYCLES("Broj ciklusa prilikom primjene Echo efekta: ", final_count);
	//Change the name of txt file!
	file = fopen("distorsion_effect.txt", "w");
	if(file == NULL)
	{
		printf("Error while opening .txt file!");
		return -1;
	}
	for(int i = 0; i< sound_wav_len; i++)
		fprintf(file, "%d\n", output_signal[i]);
	fclose(file);
	printf("Writing is done!");
	heap_free(index, output_signal);

	return 0;
}

void delay(const pm int * restrict input_signal, int * output_signal, unsigned int signal_length)
{
	int delayed_value = 0;
	//#pragma no_vectorization
	#pragma SIMD_for
	for(int i = 0; i < signal_length; i++)
	{
		if(expected_true(i - DELAY_SAMPLES >= 0))
			delayed_value = input_signal[i - DELAY_SAMPLES];
		else
			delayed_value = 0;
		output_signal[i] = input_signal[i] + GAIN * delayed_value;
	}
}

void echo(const pm int * restrict input_signal, int * restrict output_signal, unsigned int signal_length)
{
	int delayed_value = 0;
	#pragma SIMD_for
	for(int i = 0; i < signal_length; i++)
	{
		if (expected_true(i - DELAY_SAMPLES >= 0))
			delayed_value = output_signal[i - DELAY_SAMPLES];
		else
			delayed_value = 0;
		output_signal[i] = input_signal[i] - GAIN * delayed_value;
	}
}

void compressor(const pm int * restrict input_signal, int * restrict output_signal, unsigned int signal_length)
{
	//#pragma SIMD_for
	#pragma no_vectorization
	for(int i = 1; i < signal_length; i++)
		output_signal[i] = GAIN * input_signal[i] + (1 - GAIN) * output_signal[i - 1];
}

void noise_gate(const pm int * restrict input_signal, int * restrict output_signal, unsigned int signal_length)
{
	//#pragma SIMD_for
	//#pragma no_vectorization
	for(int i = 0; i < signal_length; i++)
	{
		//if(fabs(input_signal[i]) >= THRESHOLD)
		if(expected_false(fabs(input_signal[i]  - THRESHOLD) >= 0))
			output_signal[i] = input_signal[i];
		else
			output_signal[i] = 0;
	}
}

void volume_pedal(const pm int * restrict input_signal, int * restrict output_signal, unsigned int signal_length)
{
	#pragma SIMD_for
	for(int i = 0; i < signal_length; i++)
		output_signal[i] = input_signal[i] * PEDAL_POSITION;
}

void tape_saturation(const pm int * input_signal, int * output_signal, unsigned int signal_length)
{
	//#pragma SIMD_for
	for(int i = 0; i < signal_length; i++)
		output_signal[i] = tanh(input_signal[i] * SATURATION_FACTOR);
}

void octave_up(const pm int * restrict input_signal, int * restrict output_signal, unsigned int signal_length)
{
	//#pragma SIMD_for
	for(int i = 0; i < signal_length; i++)
		output_signal[i] = input_signal[i] + GAIN * fabs(input_signal[i]);
}

void envelope_filter(const pm int * restrict input_signal, int * restrict output_signal, unsigned int signal_length)
{
	float envelope = 0.0;
	output_signal[0] = input_signal[0];

	//#pragma SIMD_for
	for(int i = 1; i < signal_length; i++)
	{
		envelope += ALPHA * (fabs(input_signal[i]) - envelope) * DT;
		output_signal[i] = output_signal[i - 1] + envelope * DT * input_signal[i];
	}
}
//float depth = 0.9;
//int flfo = 5;
//int samplerate = 44100;
inline float m_function(int n)
{
	return 1 + DEPTH * cosf(2.0 * M_PI * n * FLFO / SAMPLE_RATE);
}

void tremolo(const pm int *  restrict input_signal, pm int * restrict output_signal, dm unsigned int signal_length)
{
	#pragma SIMD_for
	for(int i = 0; i < signal_length; i++)
	{
		output_signal[i] = input_signal[i] * m_function(i);
	}
}

//void tremolo(const pm int *  restrict input_signal, pm int * restrict output_signal, dm unsigned int signal_length)
//{

	//#pragma loop_unroll 1000
	//#pragma loop_unroll 100
	//#pragma loop_unroll 10
//	for(int i = 0; i < signal_length; i+=2)
//	{
//		output_signal[i] = input_signal[i] * m_function(i);
//		output_signal[i+1] = input_signal[i+1] * m_function(i+1);
//	}
//}

void distorsion(const pm int * restrict input_signal, int * restrict output_signal, unsigned int signal_length)
{

	for(int i = 0; i < signal_length; i++)
	{
		int x = input_signal[i];
		if(expected_false(GI * x <= -1))
		//if(expected_false(GI * x + 1 <= 0))
			output_signal[i] = - GO;
		else if (expected_true(GI * x >= -1 && GI * x < 1))
		//else if(expected_true(GI * x + 1 >= 0 && GI * x - 1 < 0))
			output_signal[i] =(int)(GI * GO * x);
		else
			output_signal[i] = GO;
	}
}
//void distorsion(const pm int * restrict input_signal, int * restrict output_signal, unsigned int signal_length)
//{
//
//	for(int i = 0; i < signal_length; i++)
//	{
//		int x = input_signal[i];
//		if(GI * x + 1 <= 0)
//			output_signal[i] = - GO;
//		else if(GI * x + 1 >= 0 && GI * x - 1 < 0)
//			output_signal[i] =(int)(GI * GO * x);
//		else
//			output_signal[i] = GO;
//	}
//}

void override(const pm int * restrict input_signal, int * restrict output_signal, unsigned int signal_length)
{
	#pragma SIMD_for
	for(int i = 0; i < signal_length; i++)
	{
		int x = input_signal[i];
		if(expected_false(GI * x <= -1))
			output_signal[i] =(int)(- GO * 2/3);
		else if (expected_true(GI * x >= -1 && GI * x < 1))
			output_signal[i] = (int)(GO * (GO * x - pow(GI * x, 3)/3));
		else
			output_signal[i] = (int)(GO * 2/3);
	}
}

void initSRU(void)
{
	//** LED01**//
	SRU(HIGH,DPI_PBEN06_I);
	SRU(FLAG4_O,DPI_PB06_I);
	//** LED02**//
	SRU(HIGH,DPI_PBEN13_I);
	SRU(FLAG5_O,DPI_PB13_I);
	//** LED03**//
	SRU(HIGH,DPI_PBEN14_I);
	SRU(FLAG6_O,DPI_PB14_I);
	//** LED04**//
	SRU(HIGH,DAI_PBEN03_I);
	SRU(HIGH,DAI_PB03_I);
	//** LED05**//
	SRU(HIGH,DAI_PBEN04_I);
	SRU(HIGH,DAI_PB04_I);
	//** LED06**//
	SRU(HIGH,DAI_PBEN15_I);
	SRU(HIGH,DAI_PB15_I);
	//** LED07**//
	SRU(HIGH,DAI_PBEN16_I);
	SRU(HIGH,DAI_PB16_I);
	//** LED08**//
	SRU(HIGH,DAI_PBEN17_I);
	SRU(HIGH,DAI_PB17_I);
	//Setting flag pins as outputs
	sysreg_bit_set(sysreg_FLAGS, (FLG4O|FLG5O|FLG6O) );
	//Setting HIGH to flag pins
	sysreg_bit_set(sysreg_FLAGS, (FLG4|FLG5|FLG6) );
}

void delay_cycles(unsigned int delayCount)
{
	/* delayCount = 1 => 38ns delay */
	while(delayCount--);
}

void loading_bar(void)
{
	initSRU();
	//turn off LEDs
	sysreg_bit_clr(sysreg_FLAGS, FLG4);
	sysreg_bit_clr(sysreg_FLAGS, FLG5);
	sysreg_bit_clr(sysreg_FLAGS, FLG6);
	SRU(LOW,DAI_PB03_I);
	SRU(LOW,DAI_PB04_I);
	SRU(LOW,DAI_PB15_I);
	SRU(LOW,DAI_PB16_I);
	SRU(LOW,DAI_PB17_I);
	//turn on LEDs with delay
	delay_cycles(3500000);
	sysreg_bit_set(sysreg_FLAGS, FLG4);
	delay_cycles(3500000);
	sysreg_bit_set(sysreg_FLAGS, FLG5);
	delay_cycles(3500000);
	sysreg_bit_set(sysreg_FLAGS, FLG6);
	delay_cycles(3500000);
	SRU(HIGH,DAI_PB03_I);
	delay_cycles(3500000);
	SRU(HIGH,DAI_PB04_I);
	delay_cycles(3500000);
	SRU(HIGH,DAI_PB15_I);
	delay_cycles(3500000);
	SRU(HIGH,DAI_PB16_I);
	delay_cycles(3500000);
	SRU(HIGH,DAI_PB17_I);

}
