#python3 version
import rsa
import socket
from threading import Thread

print('--------------')
print('*FATECLANDO*')
print('--------------')

print('Servidor TCP 2 vias - Lado Johnatan')

arqnomepub = 'clientePub.txt'   
arqnomepriv = 'chavePri.txt' 

def enviar():
    global tcp_con, arqnomepub
    while True:
        try:
            msg = input()
            if not msg:
                continue
            msg_bytes = msg.encode('utf-8')
            
            # Lê a chave pública do destinatário para cifrar
            with open(arqnomepub, 'rb') as arq:
                txt = arq.read()
            
            pub = rsa.PublicKey.load_pkcs1(txt, format='PEM')
            msgc = rsa.encrypt(msg_bytes, pub)
            
            # Envia os bytes cifrados DIRETAMENTE pelo socket (sem ficheiro intermédio)
            tcp_con.sendall(msgc)
            print('Mensagem cifrada enviada com sucesso.')
        except Exception as e:
            print(f'Erro ao enviar: {e}')
            break

def receber():
    global tcp_con, arqnomepriv
    while True: 
        try:
            dados_recebidos = tcp_con.recv(2048)
            if not dados_recebidos:
                break
        
            with open(arqnomepriv, 'rb') as arq:
                txt_priv = arq.read()
            
            priv = rsa.PrivateKey.load_pkcs1(txt_priv, format='PEM')

            # Decifra diretamente os bytes recebidos usando a chave privada
            msg = rsa.decrypt(dados_recebidos, priv) 

            print('\nMensagem decifrada: ' + msg.decode('utf-8'))
        except Exception as e:
            print(f'\nErro ao decifrar mensagem: {e}')
            break

HOST = ''
PORT = 5002 

tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
orig = (HOST, PORT)

tcp.bind(orig)
tcp.listen(2)

print(f'Servidor à escuta na porta {PORT}...')

while True: 
    tcp_con, cliente = tcp.accept()
    print('Conectado por ', cliente)
    
    t_env = Thread(target=enviar, args=())
    t_env.start()
    
    t_rec = Thread(target=receber, args=())
    t_rec.start()