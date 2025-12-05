import os
import time
import random
import requests
from datetime import datetime

class Motorista:
    def __init__(self, nome, placa, modelo, avaliacao):
        self.nome = nome
        self.placa = placa
        self.modelo = modelo
        self.avaliacao = avaliacao
        self.distancia = random.uniform(0.5, 5.0)

class SistemaTransporte:
    def __init__(self):
        self.motoristas = [
            Motorista("João Silva", "ABC-1234", "Toyota Corolla", 4.8),
            Motorista("Maria Santos", "DEF-5678", "Honda Civic", 4.9),
            Motorista("Pedro Oliveira", "GHI-9012", "Chevrolet Onix", 4.7),
            Motorista("Ana Costa", "JKL-3456", "Volkswagen Gol", 4.6),
            Motorista("Carlos Souza", "MNO-7890", "Fiat Argo", 4.9)
        ]
        self.viagem_ativa = None
        self.cidade_base = "Porto Alegre, RS"
        self.historico = []  

    def limpar_tela(self):
        os.system('clear' if os.name != 'nt' else 'cls')
    
    def exibir_logo(self):
        print("----------------------------------------")
        print("         TRANSPORTE EXPRESS")
        print("----------------------------------------")
        print()
    
    def buscar_localizacao(self, endereco):
        try:
            url = "https://nominatim.openstreetmap.org/search"
            params = {
                'q': f"{endereco}, {self.cidade_base}",
                'format': 'json',
                'limit': 5
            }
            headers = {
                'User-Agent': 'TransporteExpress/1.0'
            }
            response = requests.get(url, params=params, headers=headers, timeout=5)
            if response.status_code == 200:
                return response.json()
            return []
        except:
            return []
    
    def calcular_distancia(self, lat1, lon1, lat2, lon2):
        from math import radians, cos, sin, asin, sqrt
        lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
        c = 2 * asin(sqrt(a))
        km = 6371 * c
        return km
    
    def selecionar_local(self, prompt_msg):
        endereco = input(prompt_msg)
        if not endereco:
            return None
        
        print("\nBuscando locais...")
        locais = self.buscar_localizacao(endereco)
        
        if not locais:
            print("Nenhum local encontrado. Tente novamente.")
            time.sleep(2)
            return None
        
        print(f"\nEncontrados {len(locais)} resultados:\n")
        
        for i, local in enumerate(locais, 1):
            nome = local.get('display_name', 'Desconhecido')
            nome_parts = nome.split(',')
            nome_curto = ', '.join(nome_parts[:3])
            print(f"{i}. {nome_curto}")
        
        print("0. Buscar novamente")
        
        escolha = input("\nEscolha um local: ")
        
        if escolha == "0":
            return self.selecionar_local(prompt_msg)
        
        if escolha.isdigit() and 1 <= int(escolha) <= len(locais):
            local_selecionado = locais[int(escolha) - 1]
            return {
                'nome': local_selecionado.get('display_name', '').split(',')[0],
                'nome_completo': local_selecionado.get('display_name', ''),
                'lat': float(local_selecionado.get('lat', 0)),
                'lon': float(local_selecionado.get('lon', 0))
            }
        
        return None
    
    def menu_principal(self):
        self.limpar_tela()
        self.exibir_logo()
        print(f"Cidade base: {self.cidade_base}\n")
        print("1. Solicitar Corrida")
        print("2. Ver Corridas Anteriores")
        print("3. Mudar Cidade Base")
        print("4. Sair")
        print()
        return input("Escolha uma opção: ")
    
    def mudar_cidade(self):
        self.limpar_tela()
        self.exibir_logo()
        print("MUDAR CIDADE BASE\n")
        nova_cidade = input("Digite a cidade e estado (ex: São Paulo, SP): ")
        if nova_cidade:
            self.cidade_base = nova_cidade
            print(f"Cidade alterada para: {self.cidade_base}")
        else:
            print("Cidade não alterada")
        time.sleep(2)
    
    def solicitar_corrida(self):
        self.limpar_tela()
        self.exibir_logo()
        print("NOVA CORRIDA\n")
        
        print("Local de origem")
        origem = self.selecionar_local("Digite o endereço de origem: ")
        if not origem:
            return
        
        self.limpar_tela()
        self.exibir_logo()
        print(f"Origem selecionada: {origem['nome']}\n")
        
        print("Destino")
        destino = self.selecionar_local("Digite o endereço de destino: ")
        if not destino:
            return
        
        distancia_real = self.calcular_distancia(
            origem['lat'], origem['lon'],
            destino['lat'], destino['lon']
        )
        
        if distancia_real < 0.5:
            print("\nDistância muito curta. Vá a pé.")
            time.sleep(3)
            return
        
        print("\nProcurando motoristas...")
        time.sleep(2)
        
        motoristas_disponiveis = random.sample(self.motoristas, min(3, len(self.motoristas)))
        
        self.limpar_tela()
        self.exibir_logo()
        print(f"Origem: {origem['nome']}")
        print(f"Destino: {destino['nome']}")
        print(f"Distância: {distancia_real:.1f} km\n")
        print("Motoristas disponíveis:\n")
        
        for i, m in enumerate(motoristas_disponiveis, 1):
            tempo_chegada = int(m.distancia * 2)
            preco = 5.00 + (distancia_real * 2.5) + random.uniform(-2, 3)
            
            print(f"{i}. {m.nome}")
            print(f"   {m.modelo} - {m.placa}")
            print(f"   Avaliação: {m.avaliacao}")
            print(f"   Distância: {m.distancia:.1f} km | Chegada: {tempo_chegada} min")
            print(f"   Preço: R$ {preco:.2f}")
            print()
        
        print("0. Voltar")
        escolha = input("\nEscolher motorista: ")
        
        if escolha.isdigit() and 1 <= int(escolha) <= len(motoristas_disponiveis):
            motorista = motoristas_disponiveis[int(escolha) - 1]
            preco_final = 5.00 + (distancia_real * 2.5) + random.uniform(-2, 3)
            self.iniciar_viagem(motorista, origem, destino, distancia_real, preco_final)
    
    def iniciar_viagem(self, motorista, origem, destino, distancia, preco):
        self.limpar_tela()
        self.exibir_logo()
        
        print("Corrida confirmada!\n")
        print(f"Motorista: {motorista.nome}")
        print(f"Veículo: {motorista.modelo} - {motorista.placa}")
        print(f"Avaliação: {motorista.avaliacao}")
        print()
        
        tempo_chegada = int(motorista.distancia * 2)
        print(f"Motorista chegando em {tempo_chegada} minutos...")
        
        for i in range(5):
            time.sleep(0.8)
            print(".", end="", flush=True)
        
        print("\n\nMotorista chegou! Iniciando viagem...")
        time.sleep(2)
        
        tempo_viagem = int(distancia * 3)
        
        self.limpar_tela()
        self.exibir_logo()
        print("EM VIAGEM\n")
        print(f"Origem: {origem['nome']}")
        print(f"Destino: {destino['nome']}\n")
        
        for _ in range(8):
            print(".", end="", flush=True)
            time.sleep(0.5)
        
        print("\n\nViagem concluída!")
        
        print(f"\nValor: R$ {preco:.2f}")
        print(f"Distância: {distancia:.1f} km")
        print(f"Tempo: {tempo_viagem} min")

        # *** REGISTRO NO HISTÓRICO ***
        self.historico.append({
            "motorista": motorista.nome,
            "origem": origem["nome"],
            "destino": destino["nome"],
            "distancia": distancia,
            "preco": preco,
            "data": datetime.now().strftime("%d/%m/%Y %H:%M")
        })
        
        input("\nPressione Enter para avaliar o motorista...")
        
        self.avaliar_motorista(motorista)
    
    def avaliar_motorista(self, motorista):
        self.limpar_tela()
        self.exibir_logo()
        print(f"Avaliação para {motorista.nome}\n")
        print("1. *")
        print("2. **")
        print("3. ***")
        print("4. ****")
        print("5. *****")
        
        avaliacao = input("\nSua avaliação (1-5): ")
        
        if avaliacao.isdigit() and 1 <= int(avaliacao) <= 5:
            print("\nObrigado pela avaliação!")
            time.sleep(2)
        else:
            print("\nAvaliação inválida")
            time.sleep(2)
    
    def ver_corridas_anteriores(self):
        self.limpar_tela()
        self.exibir_logo()
        print("CORRIDAS ANTERIORES\n")

        if not self.historico:
            print("Nenhuma corrida realizada ainda.\n")
            input("Pressione Enter para voltar...")
            return

        for i, c in enumerate(self.historico, 1):
            print(f"{i}. {c['data']}")
            print(f"   Motorista: {c['motorista']}")
            print(f"   Origem: {c['origem']}")
            print(f"   Destino: {c['destino']}")
            print(f"   Distância: {c['distancia']:.1f} km")
            print(f"   Preço: R$ {c['preco']:.2f}\n")

        input("Pressione Enter para voltar...")

    def executar(self):
        while True:
            opcao = self.menu_principal()
            
            if opcao == "1":
                self.solicitar_corrida()
            elif opcao == "2":
                self.ver_corridas_anteriores()
            elif opcao == "3":
                self.mudar_cidade()
            elif opcao == "4":
                self.limpar_tela()
                print("Até logo!")
                break
            else:
                print("Opção inválida!")
                time.sleep(1)

if __name__ == "__main__":
    sistema = SistemaTransporte()
    sistema.executar()
