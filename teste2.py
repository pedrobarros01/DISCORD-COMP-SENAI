
from datetime import datetime, time
def comparar_data_agora(data):
    data = data.split('/')
    if len(data) == 3:
        return False
    if len(data) == 2:
        data.append(str(datetime.now().year))

    data_de_hoje = datetime.now()
    data_prova = datetime(day=int(data[0]), month=int(data[1]), year=int(data[2]))
    #print(data_prova)
    if data_de_hoje > data_prova:
        return False
    else:
        return True
    
# print(comparar_data_agora("29/03"))
