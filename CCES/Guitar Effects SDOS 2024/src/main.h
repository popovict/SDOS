/*****************************************************************************
 * main.h
 *****************************************************************************/

#ifndef __MAIN_H__
#define __MAIN_H__

void delay(const pm int * input_signal, int * output_signal, unsigned int signal_length);
void echo(const pm int * input_signal, int * output_signal, unsigned int signal_lenght);
void compressor(const pm int * input_signal, int * output_signal, unsigned int signal_length);
void noise_gate(const pm int * input_signal, int * output_signal, unsigned int signal_length);
void volume_pedal(const pm int * input_signal, int * output_signal, unsigned int signal_length);
void tape_saturation(const pm int * input_signal, int * output_signal, unsigned int signal_length);
void octave_up(const pm int * input_signal, int * output_signal, unsigned int signal_length);
void envelope_filter(const pm int * input_signal, int * output_signal, unsigned int signal_length);
void tremolo(const pm int * input_signal, pm int * output_signal, dm unsigned int signal_length);
float m_function(int n);
void distorsion(const pm int * input_signal, int * output_signal, unsigned int signal_length);
void override(const pm int * input_signal, int * output_signal, unsigned int signal_length);
void initSRU(void);
void delay_cycles(unsigned int delayCount);
void loading_bar(void);
#endif /* __MAIN_H__ */
