# LOG TABLE

### **1. pvt_log - 29/01/26**

3 cicli separati nel log da "-", cold start, acquisizione di 10 min di PVT a 1Hz una volta raggiunto il 3DFIX/Float di:
- nSv
- Lat e Lon
- hAcc
- Time

attesa di 10 min

### **2. relposned_test - 30/01/26**

Test per verificare relposned che nella classe ubx_reader viene già parsato e fatta la somma tra la parte normale e quella "high precision".
1 singolo ciclo, 60 sec di acquisizione e confrontato con il log generato dalla view table di ublox. Caricati entrambi i csv. Quello di ublox
ha più campioni. Controllare iTOW!

- table_test_relposned.csv  -> log da table
- relposned_test.csv        -> log dello script 

### **3. test_2cycle - 30/01/26**

Test composto da 2 cicli di cold start a distanza di 1h e finestra di acquisizione di 3 minuti. Il tempo di "wait" è aggiustato per 
fare in modo che la distanza tra i due cold_start sia effettivamente rispettata nonostante le acquisizioni inizino dopo un tempo variabile
dovuto all'attesa del 3D/FIXED.

- 3_table_test_2cycle.csv
- 3_test_2cycle.csv

### **4. test_2cycle - 30/01/26**

Test rapido, 3 cicli, hot start, 30 sec acquisizione, 120 di attesa. Aspetto il fixed. Salvo ENU, cycle, data e orario, ttff e ttsf.

- 4_enu_log.csv

### **5. test_forward - 04/02/26**

20min wait time, 2 cicli, hot start. Usato il forward via seriale. GNSS non posizionati bene (vicino al marciapiede), quindi fix molto lungo (ha impiegato quais tutto il wait time).

- 5_enu_log_forward.csv

### **6. log MOVE - 06/02/26**

Log nel terrazzo esterno di MOVE, GNSS messi male (sul ghiaino ma vicini alla struttura - tempi per fix lunghi). Versione programma M3. Tre cicli di un ora, acquisizione di 60 s.

- 6_enu_log.csv