import pickle
import numpy as np
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras import Input, Model
from tensorflow.keras.layers import LSTM, Dropout, Dense, Embedding, Bidirectional, Add, Concatenate, Dropout

class Transliterator:


    def __init__(self):
        self.max_sing_len = 65
        self.SINHALA_VOCAB_SIZE = 87
        self.SINGLISH_VOCAB_SIZE = 27
        with open('models/singlish_tokenizer.pickle', 'rb') as handle:
            self.singlish_tokenizer = pickle.load(handle)
        with open('models/sinhala_tokenizer.pickle', 'rb') as handle:
            self.sinhala_tokenizer = pickle.load(handle)

         # Encoder
        encoder_input = Input(shape=(None, ))
        encoder_embd = Embedding(self.SINGLISH_VOCAB_SIZE,1024, mask_zero=True)(encoder_input)
        encoder_lstm = Bidirectional(LSTM(256, return_state=True))
        encoder_output, forw_state_h, forw_state_c, back_state_h, back_state_c = encoder_lstm(encoder_embd)
        state_h_final = Concatenate()([forw_state_h, back_state_h])
        state_c_final = Concatenate()([forw_state_c, back_state_c])

        ## Now take only states and create context vector
        encoder_states= [state_h_final, state_c_final]

        #Decoder
        decoder_input = Input(shape=(None,))
        # For zero padding we have added +1 in marathi vocab size
        decoder_embd = Embedding(self.SINHALA_VOCAB_SIZE, 1024, mask_zero=True)
        decoder_embedding= decoder_embd(decoder_input)
        # We used bidirectional layer above so we have to double units of this lstm
        decoder_lstm = LSTM(512, return_state=True,return_sequences=True )
        # just take output of this decoder dont need self states
        decoder_outputs, _, _= decoder_lstm(decoder_embedding, initial_state=encoder_states)
        # here this is going to predicct so we can add dense layer here
        # here we want to convert predicted numbers into probability so use softmax
        decoder_dense= Dense(self.SINHALA_VOCAB_SIZE, activation='softmax')
        # We will again feed predicted output into decoder to predict its next word
        decoder_outputs = decoder_dense(decoder_outputs)

        model = Model([encoder_input, decoder_input], decoder_outputs)
        model.load_weights("models/transliteration_model.h5")

        self.encoder_model = Model(encoder_input, encoder_states)
        decoder_state_input_h = Input(shape=(512,))
        decoder_state_input_c = Input(shape=(512,))
        decoder_states_input = [decoder_state_input_h, decoder_state_input_c]

        dec_embd2 = decoder_embd(decoder_input)

        decoder_output2, state_h2, state_c2 = decoder_lstm(dec_embd2, initial_state=decoder_states_input)
        deccoder_states2 = [state_h2, state_c2]

        decoder_output2 = decoder_dense(decoder_output2)

        self.decoder_model = Model([decoder_input] + decoder_states_input,[decoder_output2] + deccoder_states2)


    def get_predicted_sentence(self,input_seq):
        # Encode the input as state vectors.
        states_value = self.encoder_model.predict(input_seq)

        # Generate empty target sequence of length 1.
        target_seq = np.zeros((1, 1))

        # Populate the first character of target sequence with the start character.
        target_seq[0, 0] = self.sinhala_tokenizer.word_index['sos']

        # Sampling loop for a batch of sequences

        # (to simplify, here we assume a batch of size 1).
        stop_condition = False
        decoded_sentence = ''

        while not stop_condition:
            output_tokens, h, c = self.decoder_model.predict([target_seq] + states_value)
            # Sample a token
            sampled_token_index = np.argmax(output_tokens[0, -1, :])
            if sampled_token_index == 0:
                break
            else:
                # convert max index number to marathi word
                sampled_char = self.sinhala_tokenizer.index_word[sampled_token_index]
            # aapend it ti decoded sent
            decoded_sentence += ' ' + sampled_char

            # Exit condition: either hit max length or find stop token.
            if (sampled_char == 'eos' or len(decoded_sentence) >= 43):
                stop_condition = True

            # Update the target sequence (of length 1).
            target_seq = np.zeros((1, 1))
            target_seq[0, 0] = sampled_token_index

            # Update states
            states_value = [h, c]

        return decoded_sentence

    def singlish2sinhala(self,input_sent):
        english_alp = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's',
                       't', 'u', 'v', 'w', 'x', 'y', 'z',
                       'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S',
                       'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
        special_words = ["kg", "ml", "bike"]
        input_sent_word_list = input_sent.split()
        sinh_sent = ""
        for word in input_sent_word_list:
            break_points = [-1]
            words = []
            for i in range(len(word)):
                if word[i] not in english_alp:
                    break_points.append(i)
            for ind in range(len(break_points)):
                if ind < len(break_points) - 1:
                    words.append(word[break_points[ind] + 1:break_points[ind + 1]])
                else:
                    words.append(word[break_points[ind] + 1:])
            sin_word = ""
            break_points = break_points[1:]
            arg = False
            for word_part in words:
                if word_part in special_words:
                    add = word_part
                elif len(word_part) > 0:
                    seq = []
                    for let in word_part:
                        seq.append(self.singlish_tokenizer.word_index[let.lower()])
                    seq = pad_sequences([seq], maxlen=self.max_sing_len, padding='post')
                    add = "".join(self.get_predicted_sentence(seq.reshape(1, self.max_sing_len))[:-4].split())
                else:
                    add = ""
                if arg:
                    point = break_points[0]
                    break_points = break_points[1:]
                    sin_word = sin_word + word[point] + add
                else:
                    sin_word = sin_word + add
                arg = True
            sinh_sent = sinh_sent + " " + sin_word
        return (sinh_sent[1:])