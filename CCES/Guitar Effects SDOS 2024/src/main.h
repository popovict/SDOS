/*****************************************************************************
 * main.h
 *****************************************************************************/

#ifndef __MAIN_H__
#define __MAIN_H__

void delay(const pm int * input_signal, int * output_signal, unsigned int signal_length);
void echo(const pm int * input_signal, int * output_signal, unsigned int signal_lenght);
void compressor(const pm int * input_signal, int * output_signal, unsigned int signal_length);
void noise_gate(int * input_signal, int * output_signal, unsigned int signal_length);
void volume_pedal(int * input_signal, int * output_signal, unsigned int signal_length);
void tape_saturation(int * input_signal, int * output_signal, unsigned int signal_length);
void octave_up(int * input_signal, int * output_signal, unsigned int signal_length);
void envelope_filter(int * input_signal, int * output_signal, unsigned int signal_length);
void tremolo(int * input_signal, int * output_signal, unsigned int signal_length);
float m_function(int n);
void distorsion(int * input_signal, int * output_signal, unsigned int signal_length);
void override(int * input_signal, int * output_signal, unsigned int signal_length);
void initSRU(void);
void delay_cycles(unsigned int delayCount);
void leds(void);
#endif /* __MAIN_H__ */
