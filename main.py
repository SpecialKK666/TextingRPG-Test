# main.py

import os
import sys
import time
import random
import traceback
from datetime import datetime

from cores import Cor
from personagem import Jogador
from inimigo import Inimigo, todos_os_monstros_base, monstros_comuns, monstros_capitaes, monstros_generais, monstros_reis
from item import Arma, Armadura, Escudo, Consumivel, FragmentoLiterario, todos_consumiveis, todos_itens, pools_drop_monstro, DADOS_FRAGMENTOS_LITERARIOS
from batalha import Batalha # NOVO: Importa a classe de Batalha refatorada

# --- Funções Auxiliares de UI ---
LARGURA_CONSOLE = 110

def limpar_tela():
    os.system('cls' if os.name == 'nt' else 'clear')

def imprimir_cabecalho(titulo, cor=Cor.BRANCO_BRILHANTE, bg_cor=Cor.BG_AZUL):
    print(f"{bg_cor}{cor}{' ' * LARGURA_CONSOLE}{Cor.RESET}")
    print(f"{bg_cor}{cor}{titulo.center(LARGURA_CONSOLE)}{Cor.RESET}")
    print(f"{bg_cor}{cor}{' ' * LARGURA_CONSOLE}{Cor.RESET}")
    print("\n")

def imprimir_cabecalho_secao(titulo, cor=Cor.BRANCO_BRILHANTE, bg_cor=Cor.BG_PRETO):
    print(f"\n{bg_cor}{cor}{titulo.center(LARGURA_CONSOLE)}{Cor.RESET}")
    print(f"{bg_cor}{cor}{'-' * LARGURA_CONSOLE}{Cor.RESET}")

def imprimir_mensagem(mensagem, cor=Cor.BRANCO):
    print(f"{cor}{mensagem}{Cor.RESET}")

def obter_entrada(prompt, cor=Cor.AMARELO_BRILHANTE):
    return input(f"{cor}{prompt}{Cor.RESET} ").strip().lower()

def pressionar_enter_para_continuar():
    input(f"\n{Cor.AZUL_BRILHANTE}Pressione ENTER para continuar...{Cor.RESET}")

def quebrar_texto(texto, largura):
    palavras = texto.split(' ')
    linhas = []
    linha_atual = []
    for palavra in palavras:
        palavra_sem_cor = ''.join(palavra.split('\033')[::2])
        linha_teste_sem_cor = ' '.join([p.split('\033')[::2][0] for p in linha_atual] + [palavra_sem_cor])
        
        if len(linha_teste_sem_cor) <= largura:
            linha_atual.append(palavra)
        else:
            linhas.append(' '.join(linha_atual))
            linha_atual = [palavra]
    linhas.append(' '.join(linha_atual))
    return linhas

def exibir_log_mensagens_ui(mensagens_log, max_linhas=15):
    imprimir_cabecalho_secao("Log de Eventos", Cor.BRANCO, Cor.BG_PRETO_BRILHANTE)
    mensagens_exibidas = mensagens_log[-max_linhas:]
    for msg in mensagens_exibidas:
        for linha in quebrar_texto(msg, LARGURA_CONSOLE - 4):
            print("  " + linha)
    print(f"{Cor.BG_PRETO_BRILHANTE}{Cor.BRANCO}{'-' * LARGURA_CONSOLE}{Cor.RESET}\n")

# --- CLASSE DA LOJA ---
class Loja:
    def __init__(self):
        self.inventario_consumiveis = [item for item in todos_consumiveis]
        self.inventario_equipamentos = []
        self.gerar_estoque_equipamentos()

    def gerar_estoque_equipamentos(self):
        self.inventario_equipamentos.clear()
        
        # Seleciona 3 a 5 itens comuns
        itens_comuns = [item for item in todos_itens if item.raridade == "normal" and item.tipo_item in ['arma', 'armadura', 'escudo']]
        num_itens_comuns = random.randint(3, 5)
        if len(itens_comuns) >= num_itens_comuns:
            self.inventario_equipamentos.extend(random.sample(itens_comuns, num_itens_comuns))

        # 35% de chance de adicionar um item mágico
        if random.random() < 0.35:
            itens_magicos = [item for item in todos_itens if item.raridade == "magica" and item.tipo_item in ['arma', 'armadura', 'escudo']]
            if itens_magicos:
                self.inventario_equipamentos.append(random.choice(itens_magicos))

class Jogo:
    def __init__(self):
        self.jogador = None
        self._nome_jogador_temporario = ""
        self.inimigo_atual = None
        self.batalha_atual = None # NOVO: Para gerenciar a instância da batalha
        self.loja = Loja() # NOVO: Instância da loja
        self.inimigo_derrotado_era_boss = False
        self.estado_jogo = "MENU_PRINCIPAL"
        self.modo_jogo = None
        self.bestiario_encontrados = set()
        self.monstros_derrotados_survival = 0
        self.andar_max_survival = 1
        self.mensagens_jogo = []
        self.andar_masmorra_atual = 1
        self.sala_masmorra_atual = 0
        self.salas_no_andar_atual = 0

    def adicionar_mensagem(self, mensagem):
        self.mensagens_jogo.append(mensagem)
        if len(self.mensagens_jogo) > 100:
            self.mensagens_jogo = self.mensagens_jogo[-100:]

    def definir_estado(self, novo_estado):
        self.estado_jogo = novo_estado
        if novo_estado != "COMBATE":
            limpar_tela()

    def reiniciar_jogo(self):
        self.adicionar_mensagem("Iniciando um novo jogo...")
        self.__init__()
        self.definir_estado("CRIAR_PERSONAGEM_NOME")
        self.adicionar_mensagem("Digite o nome do seu herói:")

    def executar(self):
        while True:
            if self.estado_jogo != "COMBATE":
                limpar_tela()
            
            if self.estado_jogo == "MENU_PRINCIPAL": self.menu_principal()
            elif self.estado_jogo == "CRIAR_PERSONAGEM_NOME": self.criar_personagem_nome()
            elif self.estado_jogo == "CRIAR_PERSONAGEM_CLASSE": self.criar_personagem_classe()
            elif self.estado_jogo == "CRIAR_PERSONAGEM_MODO": self.criar_personagem_modo()
            elif self.estado_jogo == "MAPA_MUNDI": self.mapa_mundi()
            elif self.estado_jogo == "LOJA": self.tela_loja() # NOVO ESTADO
            elif self.estado_jogo == "STATUS_PERSONAGEM": self.tela_status_personagem()
            elif self.estado_jogo == "INVENTARIO": self.tela_inventario()
            elif self.estado_jogo == "FRAGMENTOS": self.tela_fragmentos_literarios()
            elif self.estado_jogo == "BESTIARIO": self.tela_bestiario()
            elif self.estado_jogo == "EXPLORANDO_MASMORRA": self.explorando_masmorra()
            elif self.estado_jogo == "COMBATE": self.tela_combate()
            elif self.estado_jogo == "DECISAO_POS_BOSS": self.tela_decisao_pos_boss()
            elif self.estado_jogo == "FIM_DE_JOGO": self.tela_fim_de_jogo()

    def menu_principal(self):
        imprimir_cabecalho("Aventura RPG de Texto")
        imprimir_mensagem("1. Novo Jogo")
        imprimir_mensagem("2. Sair")
        exibir_log_mensagens_ui(self.mensagens_jogo)

        escolha = obter_entrada("Digite sua escolha: ")
        if escolha == "1":
            self.reiniciar_jogo()
        elif escolha == "2":
            sys.exit("Saindo do jogo.")
        else:
            self.adicionar_mensagem("Escolha inválida.")
    
    def criar_personagem_nome(self):
        imprimir_cabecalho("Criação de Personagem - Nome")
        exibir_log_mensagens_ui(self.mensagens_jogo)
        nome = input(f"{Cor.AMARELO_BRILHANTE}Nome do herói: {Cor.RESET}").strip()
        if nome:
            self._nome_jogador_temporario = nome
            self.adicionar_mensagem(f"Nome definido como: {nome}. Agora escolha sua classe.")
            self.definir_estado("CRIAR_PERSONAGEM_CLASSE")
        else:
            self.adicionar_mensagem("O nome não pode estar vazio.")

    def criar_personagem_classe(self):
        imprimir_cabecalho("Criação de Personagem - Classe")
        imprimir_mensagem(f"Nome: {self._nome_jogador_temporario}")
        imprimir_mensagem("1. Guerreiro")
        imprimir_mensagem("2. Mago")
        imprimir_mensagem("3. Arqueiro")
        imprimir_mensagem("4. Ladino")
        exibir_log_mensagens_ui(self.mensagens_jogo)
        
        escolha = obter_entrada("Escolha sua classe: ")
        mapa_classes = {"1": "Guerreiro", "2": "Mago", "3": "Arqueiro", "4": "Ladino"}
        if escolha in mapa_classes:
            self.jogador = Jogador(self._nome_jogador_temporario, mapa_classes[escolha], self.adicionar_mensagem)
            self.definir_estado("CRIAR_PERSONAGEM_MODO")
        else:
            self.adicionar_mensagem("Classe inválida.")

    def criar_personagem_modo(self):
        imprimir_cabecalho("Criação de Personagem - Modo de Jogo")
        imprimir_mensagem("Escolha como você enfrentará o Sofrimento Eterno:")
        print(f"{Cor.CIANO}1. Modo Normal:{Cor.RESET} Se você cair, retornará à vila, mas perderá 60% de seu ouro.")
        print(f"{Cor.VERMELHO}2. Modo Survival:{Cor.RESET} A masmorra é mais perigosa, mas as recompensas são maiores. A morte é permanente.")
        
        escolha = obter_entrada("Escolha o modo de jogo: ")
        if escolha == '1':
            self.modo_jogo = "Normal"
            self.adicionar_mensagem(f"\n{Cor.VERDE_BRILHANTE}Bem-vindo(a), {self.jogador.nome}! Sua jornada no modo Normal começa.{Cor.RESET}")
            pressionar_enter_para_continuar()
            self.definir_estado("MAPA_MUNDI")
        elif escolha == '2':
            self.modo_jogo = "Survival"
            self.adicionar_mensagem(f"\n{Cor.VERMELHO_BRILHANTE}Que os deuses tenham piedade de sua alma, {self.jogador.nome}. Sua jornada no modo Survival começa.{Cor.RESET}")
            pressionar_enter_para_continuar()
            self.definir_estado("MAPA_MUNDI")
        else:
            self.adicionar_mensagem("Modo inválido.")

    def mapa_mundi(self):
        imprimir_cabecalho("Vila de Aethelgard")
        imprimir_mensagem("Você está no último bastião de segurança antes da escuridão da masmorra.")
        imprimir_cabecalho_secao("Opções", Cor.CIANO)
        imprimir_mensagem("1. Entrar no 'Sofrimento Eterno' (Masmorra)")
        imprimir_mensagem("2. Visitar a Loja do Ferreiro")
        imprimir_mensagem("3. Ver Status do Personagem")
        imprimir_mensagem("4. Acessar Inventário")
        imprimir_mensagem("5. Ler Fragmentos Literários")
        imprimir_mensagem("6. Consultar Bestiário")
        imprimir_mensagem("7. Reiniciar Jogo")
        imprimir_mensagem("8. Sair do Jogo")
        exibir_log_mensagens_ui(self.mensagens_jogo, max_linhas=5)

        escolha = obter_entrada("O que deseja fazer?: ")
        if escolha == '1':
            self.adicionar_mensagem("O estoque da loja foi renovado.")
            self.loja.gerar_estoque_equipamentos()
            self.definir_estado("EXPLORANDO_MASMORRA")
        elif escolha == '2': self.definir_estado("LOJA")
        elif escolha == '3': self.definir_estado("STATUS_PERSONAGEM")
        elif escolha == '4': self.definir_estado("INVENTARIO")
        elif escolha == '5': self.definir_estado("FRAGMENTOS")
        elif escolha == '6': self.definir_estado("BESTIARIO")
        elif escolha == '7':
            if obter_entrada("Tem certeza que deseja reiniciar? (s/n): ") == 's':
                self.reiniciar_jogo()
        elif escolha == '8': sys.exit("Obrigado por jogar!")
        else: self.adicionar_mensagem("Opção inválida.")

    def tela_loja(self):
        imprimir_cabecalho("Loja do Ferreiro")
        print(f"Seu ouro: {Cor.AMARELO}{self.jogador.ouro}{Cor.RESET}\n")

        todos_os_itens_venda = self.loja.inventario_equipamentos + self.loja.inventario_consumiveis
        
        imprimir_cabecalho_secao("Equipamentos", Cor.CIANO)
        if not self.loja.inventario_equipamentos:
            print("O ferreiro não tem equipamentos novos no momento.")
        else:
            for i, item in enumerate(self.loja.inventario_equipamentos, 1):
                cor = item.obter_cor_raridade()
                print(f"{i}. {cor}{item.nome}{Cor.RESET} (Nv.{item.level_req}) - {Cor.AMARELO}{item.valor} Ouro{Cor.RESET}")
        
        imprimir_cabecalho_secao("Consumíveis", Cor.CIANO)
        for i, item in enumerate(self.loja.inventario_consumiveis, len(self.loja.inventario_equipamentos) + 1):
            cor = item.obter_cor_raridade()
            print(f"{i}. {cor}{item.nome}{Cor.RESET} - {Cor.AMARELO}{item.valor} Ouro{Cor.RESET}")

        print("\nDigite o número do item para comprar, ou '0' para sair.")
        escolha = obter_entrada("Sua escolha: ")

        if escolha == '0':
            self.definir_estado("MAPA_MUNDI")
            return
        
        try:
            indice = int(escolha) - 1
            if 0 <= indice < len(todos_os_itens_venda):
                item_a_comprar = todos_os_itens_venda[indice]
                self.comprar_item(item_a_comprar)
            else:
                self.adicionar_mensagem("Número de item inválido.")
        except ValueError:
            self.adicionar_mensagem("Entrada inválida.")
        
        pressionar_enter_para_continuar()
        self.definir_estado("LOJA") # Recarrega a tela da loja

    def comprar_item(self, item):
        if self.jogador.ouro >= item.valor:
            self.jogador.ouro -= item.valor
            self.jogador.inventario.append(item)
            self.adicionar_mensagem(f"Você comprou {item.nome} por {item.valor} de ouro!")
            
            # Remove o item do estoque de equipamentos se for um
            if item in self.loja.inventario_equipamentos:
                self.loja.inventario_equipamentos.remove(item)
        else:
            self.adicionar_mensagem("Ouro insuficiente!")
            
    def tela_status_personagem(self):
        imprimir_cabecalho("Status do Personagem")
        p = self.jogador
        print(f"Nome: {p.nome} ({p.classe_personagem}) - Modo: {self.modo_jogo}")
        print(f"Nível: {p.nivel} ({p.xp}/{p.xp_para_proximo_nivel} XP)")
        print(f"HP: {p.hp_atual}/{p.hp_max} | MP: {p.mp_atual}/{p.mp_max}")
        print(f"Ouro: {p.ouro}")
        imprimir_cabecalho_secao("Atributos", Cor.AMARELO_BRILHANTE)
        print(f"Força: {p.forca} | Destreza: {p.destreza} | Inteligência: {p.inteligencia} | Vitalidade: {p.vitalidade} | Sabedoria: {p.sabedoria}")
        imprimir_cabecalho_secao("Equipamento", Cor.CIANO)
        for slot, item in p.equipamento.items():
            if item:
                print(f"{slot.capitalize()}: {item.obter_cor_raridade()}{item.nome}{Cor.RESET} (Nv. {item.level_req})")
            else:
                print(f"{slot.capitalize()}: Nenhum")
        pressionar_enter_para_continuar()
        self.definir_estado("MAPA_MUNDI")

    def tela_inventario(self):
        imprimir_cabecalho("Inventário")
        if not self.jogador.inventario: print("Seu inventário está vazio.")
        else:
            for i, item in enumerate(self.jogador.inventario):
                req = f"(Nv. {item.level_req})" if hasattr(item, 'level_req') else ""
                print(f"{i + 1}. {item.obter_cor_raridade()}{item.nome}{Cor.RESET} {req} ({item.tipo_item})")
        
        imprimir_cabecalho_secao("Opções", Cor.CIANO)
        print("Digite o número do item para equipar/usar, ou '0' para voltar.")
        escolha = obter_entrada("Sua escolha: ")
        if escolha == '0': self.definir_estado("MAPA_MUNDI"); return
            
        try:
            item_selecionado = self.jogador.inventario[int(escolha) - 1]
            if item_selecionado.tipo_item in ["arma", "armadura", "escudo"]:
                self.jogador.equipar_item(item_selecionado)
            elif item_selecionado.tipo_item == "consumivel":
                self.jogador.curar(item_selecionado.quantidade_curar)
                self.jogador.inventario.remove(item_selecionado)
                self.adicionar_mensagem(f"Você usou {item_selecionado.nome}.")
            pressionar_enter_para_continuar()
        except (ValueError, IndexError):
            self.adicionar_mensagem("Escolha inválida.")
            pressionar_enter_para_continuar()
        self.definir_estado("INVENTARIO")

    def tela_fragmentos_literarios(self):
        imprimir_cabecalho("Fragmentos Literários Coletados")
        fragmentos = [f for f in DADOS_FRAGMENTOS_LITERARIOS if f.id_fragmento in self.jogador.fragmentos_coletados]
        if not fragmentos: print("Você ainda não encontrou nenhum fragmento de lendas.")
        else:
            for i, frag in enumerate(fragmentos): print(f"{i + 1}. {Cor.VERDE}{frag.nome}{Cor.RESET}")
        
        imprimir_cabecalho_secao("Opções", Cor.CIANO)
        print("Digite o número do fragmento para ler, ou '0' para voltar.")
        escolha = obter_entrada("Sua escolha: ")
        if escolha == '0': self.definir_estado("MAPA_MUNDI"); return

        try:
            frag_selecionado = fragmentos[int(escolha) - 1]
            limpar_tela()
            imprimir_cabecalho(frag_selecionado.nome, cor=Cor.VERDE_BRILHANTE, bg_cor=Cor.BG_PRETO_BRILHANTE)
            for linha in quebrar_texto(frag_selecionado.conteudo, LARGURA_CONSOLE - 4): print("  " + linha)
            pressionar_enter_para_continuar()
        except (ValueError, IndexError):
            self.adicionar_mensagem("Escolha inválida.")
        self.definir_estado("FRAGMENTOS")

    def tela_bestiario(self):
        imprimir_cabecalho("Bestiário de Aethelgard")
        if not self.bestiario_encontrados: print("Você ainda não derrotou nenhum monstro.")
        else:
            monstros = [m for m in todos_os_monstros_base if m.nome in self.bestiario_encontrados]
            for i, m in enumerate(monstros): print(f"{i + 1}. {Cor.VERMELHO}{m.nome}{Cor.RESET} ({m.rank})")

        imprimir_cabecalho_secao("Opções", Cor.CIANO)
        print("Digite o número do monstro para ver detalhes, ou '0' para voltar.")
        escolha = obter_entrada("Sua escolha: ")
        if escolha == '0': self.definir_estado("MAPA_MUNDI"); return

        try:
            monstro_selecionado = [m for m in todos_os_monstros_base if m.nome in self.bestiario_encontrados][int(escolha) - 1]
            limpar_tela()
            imprimir_cabecalho(monstro_selecionado.nome, cor=Cor.VERMELHO_BRILHANTE, bg_cor=Cor.BG_PRETO_BRILHANTE)
            print(f"{Cor.AMARELO}Rank: {monstro_selecionado.rank}{Cor.RESET}")
            print(f"\n'{monstro_selecionado.descricao}'")
            pressionar_enter_para_continuar()
        except (ValueError, IndexError):
            self.adicionar_mensagem("Escolha inválida.")
        self.definir_estado("BESTIARIO")

    def explorando_masmorra(self):
        if self.modo_jogo == 'Survival': self.andar_max_survival = max(self.andar_max_survival, self.andar_masmorra_atual)
        if self.sala_masmorra_atual == 0:
            self.sala_masmorra_atual = 1; self.salas_no_andar_atual = random.randint(10, 20)
            self.adicionar_mensagem(f"Você adentra o Andar {self.andar_masmorra_atual}...")
        
        imprimir_cabecalho(f"Masmorra - Andar {self.andar_masmorra_atual} - Sala {self.sala_masmorra_atual}/{self.salas_no_andar_atual}")
        imprimir_mensagem("1. Avançar"); imprimir_mensagem("2. Retornar à Vila")
        exibir_log_mensagens_ui(self.mensagens_jogo, 5)
        escolha = obter_entrada("Sua decisão: ")
        if escolha == '1': self.avancar_sala()
        elif escolha == '2': self.definir_estado("MAPA_MUNDI")
        else: self.adicionar_mensagem("Decisão inválida.")

    def avancar_sala(self):
        self.sala_masmorra_atual += 1
        self.adicionar_mensagem(f"\nVocê avança para a sala {self.sala_masmorra_atual}...")
        self.gerar_proximo_inimigo()
        if self.inimigo_atual:
            self.batalha_atual = Batalha(self.jogador, self.inimigo_atual, self.adicionar_mensagem)
            self.definir_estado("COMBATE")
        else:
            self.adicionar_mensagem("A sala está estranhamente vazia.")
            if self.sala_masmorra_atual > self.salas_no_andar_atual:
                self.inimigo_derrotado_era_boss = True
                self.definir_estado("DECISAO_POS_BOSS")
            else: self.definir_estado("EXPLORANDO_MASMORRA")
    
    def tela_decisao_pos_boss(self):
        imprimir_cabecalho(f"Fim do Andar {self.andar_masmorra_atual}")
        imprimir_mensagem("O guardião deste andar foi derrotado. O caminho para as profundezas está aberto.")
        imprimir_mensagem("1. Avançar para o próximo andar"); imprimir_mensagem("2. Permanecer neste andar")
        
        escolha = obter_entrada("Sua escolha: ")
        if escolha == '1':
            self.andar_masmorra_atual += 1; self.sala_masmorra_atual = 0
            self.inimigo_derrotado_era_boss = False
            self.jogador.curar(self.jogador.hp_max * 0.5)
            self.adicionar_mensagem("Você recupera parte de suas forças.")
            pressionar_enter_para_continuar()
            self.definir_estado("EXPLORANDO_MASMORRA")
        elif escolha == '2':
            self.sala_masmorra_atual = 0; self.inimigo_derrotado_era_boss = False
            self.adicionar_mensagem("Você decide permanecer para explorar mais.")
            pressionar_enter_para_continuar()
            self.definir_estado("EXPLORANDO_MASMORRA")
        else: self.adicionar_mensagem("Escolha inválida.")

    def tela_combate(self):
        limpar_tela()
        imprimir_cabecalho(f"Combate - Andar {self.andar_masmorra_atual}")
        print(f"{Cor.CIANO}{self.jogador.nome} (Nv {self.jogador.nivel}){Cor.RESET} | HP: {Cor.VERDE}{self.jogador.hp_atual}/{self.jogador.hp_max}{Cor.RESET} | MP: {Cor.AZUL}{self.jogador.mp_atual}/{self.jogador.mp_max}{Cor.RESET}")
        print(f"{Cor.VERMELHO}{self.inimigo_atual.nome} (Nv {self.inimigo_atual.nivel}){Cor.RESET} | HP: {Cor.VERMELHO}{self.inimigo_atual.hp_atual}/{self.inimigo_atual.hp_max}{Cor.RESET}")
        exibir_log_mensagens_ui(self.mensagens_jogo)

        if not self.jogador.esta_vivo:
            self.definir_estado("FIM_DE_JOGO"); return
        if not self.inimigo_atual.esta_vivo:
            self.recompensas_fim_combate()
            pressionar_enter_para_continuar()
            if self.inimigo_derrotado_era_boss: self.definir_estado("DECISAO_POS_BOSS")
            else: self.definir_estado("EXPLORANDO_MASMORRA")
            return

        imprimir_cabecalho_secao("Seu Turno", Cor.CIANO)
        imprimir_mensagem("1. Atacar | 2. Fugir | 3. Ver Status Inimigo")
        escolha = obter_entrada("Sua ação: ")
        
        turno_consumido = False
        if escolha == "1": turno_consumido = self.batalha_atual.processar_turno_jogador("atacar")
        elif escolha == "2": turno_consumido = not self.batalha_atual.processar_turno_jogador("fugir") # Fuga bem sucedida retorna false
        elif escolha == "3": self.inimigo_atual.exibir_status_combate(); pressionar_enter_para_continuar()
        else: self.adicionar_mensagem("Ação inválida.")
        
        if turno_consumido and self.inimigo_atual.esta_vivo:
            self.batalha_atual.processar_turno_inimigo()

    def tela_fim_de_jogo(self):
        limpar_tela()
        if self.modo_jogo == "Normal":
            imprimir_cabecalho("Você foi gravemente ferido!", cor=Cor.AMARELO_BRILHANTE, bg_cor=Cor.BG_VERMELHO)
            ouro_perdido = int(self.jogador.ouro * 0.60)
            self.jogador.ouro -= ouro_perdido
            self.adicionar_mensagem(f"{Cor.VERMELHO}Você desmaia e acorda na vila, perdendo {ouro_perdido} de ouro!{Cor.RESET}")
            self.jogador.hp_atual = self.jogador.hp_max; self.jogador.mp_atual = self.jogador.mp_max
            self.jogador.esta_vivo = True
            pressionar_enter_para_continuar()
            self.definir_estado("MAPA_MUNDI")
        else: # Survival
            imprimir_cabecalho(f"A JORNADA DE {self.jogador.nome.upper()} CHEGOU AO FIM", Cor.VERMELHO_BRILHANTE, Cor.BG_PRETO_BRILHANTE)
            print(f"Nível Final: {self.jogador.nivel} | Andar Máximo: {self.andar_max_survival} | Monstros Derrotados: {self.monstros_derrotados_survival}")
            imprimir_mensagem("1. Recomeçar | 2. Sair do Jogo")
            while True:
                escolha = obter_entrada("Sua escolha: ")
                if escolha == '1': self.reiniciar_jogo(); return
                elif escolha == '2': sys.exit("Obrigado por jogar!")

    def gerar_proximo_inimigo(self):
        rank = 'Comum'
        roll = random.random()
        if self.andar_masmorra_atual >= 50 and roll < 0.10: rank = 'Rei'
        elif self.andar_masmorra_atual >= 30 and roll < 0.20: rank = 'General'
        elif self.andar_masmorra_atual >= 5 and roll < 0.35: rank = 'Capitão'

        if self.sala_masmorra_atual > self.salas_no_andar_atual:
            if self.andar_masmorra_atual >= 50: rank = 'Rei'
            elif self.andar_masmorra_atual >= 30: rank = 'General'
            else: rank = 'Capitão'
        
        self.inimigo_atual = self.criar_inimigo_rank(rank)

    def criar_inimigo_rank(self, rank):
        mapa = {'Comum': monstros_comuns, 'Capitão': monstros_capitaes, 'General': monstros_generais, 'Rei': monstros_reis}
        base = random.choice(mapa.get(rank, monstros_comuns))
        fator_andar = 1 + (self.andar_masmorra_atual - 1) * 0.25
        fator_dificuldade = 1.5 if self.modo_jogo == "Survival" else 1.0
        nivel = max(1, int(self.jogador.nivel * (0.8 + (self.andar_masmorra_atual * 0.05))))
        hp = int(base.hp_max * fator_andar * fator_dificuldade)
        forca = int(base.forca * fator_andar * fator_dificuldade)
        xp = int(base.recompensa_xp * fator_andar); ouro = int(base.recompensa_ouro * fator_andar)
        return Inimigo(base.nome, rank, nivel, hp, base.mp_max, forca, base.destreza, base.inteligencia, base.vitalidade, base.sabedoria, xp, ouro, base.tabela_drop, base.habilidades, base.descricao)

    def recompensas_fim_combate(self):
        inimigo = self.inimigo_atual
        self.adicionar_mensagem(f"\n{Cor.AMARELO_BRILHANTE}--- {inimigo.nome} foi derrotado(a)! ---{Cor.RESET}")
        self.bestiario_encontrados.add(inimigo.nome)
        if self.modo_jogo == 'Survival': self.monstros_derrotados_survival += 1
        self.jogador.ganhar_xp(inimigo.recompensa_xp)
        self.jogador.ouro += inimigo.recompensa_ouro
        self.adicionar_mensagem(f"Você ganhou {inimigo.recompensa_ouro} ouro.")
        if inimigo.rank == 'Rei': self.inimigo_derrotado_era_boss = True
        item_dropado = self.gerar_drop_item(inimigo)
        if item_dropado:
            self.adicionar_mensagem(f"Você encontrou: {item_dropado.obter_cor_raridade()}{item_dropado.nome}{Cor.RESET}!")
            if isinstance(item_dropado, FragmentoLiterario):
                if item_dropado.id_fragmento not in self.jogador.fragmentos_coletados:
                    self.jogador.fragmentos_coletados.add(item_dropado.id_fragmento)
                    self.adicionar_mensagem(f"{Cor.VERDE_BRILHANTE}** Novo fragmento descoberto! **{Cor.RESET}")
            else: self.jogador.inventario.append(item_dropado)
    
    def gerar_drop_item(self, inimigo):
        mod_rank = {'Comum': 1.0, 'Capitão': 1.8, 'General': 3.0, 'Rei': 10.0}.get(inimigo.rank, 1.0)
        mod_modo = 1.2 if self.modo_jogo == 'Survival' else 1.0
        if random.random() > (0.4 * mod_rank * mod_modo): return None
        chances = {'excelencia': 0.001, 'lendario': 0.01, 'épico': 0.05, 'rara': 0.15, 'magica': 0.30}
        roll = random.random()
        raridade = "normal"
        for r, c in chances.items():
            if roll < (c * mod_rank * mod_modo): raridade = r; break
        if random.random() < (0.15 * mod_rank):
            if pools_drop_monstro["literario"]: return random.choice(pools_drop_monstro["literario"])
        pool = pools_drop_monstro.get(raridade)
        return random.choice(pool) if pool else None

if __name__ == "__main__":
    jogo = Jogo()
    try:
        while True:
            jogo.executar()
    except Exception as e:
        limpar_tela()
        print(f"{Cor.VERMELHO_BRILHANTE}O JOGO ENCONTROU UM ERRO FATAL!{Cor.RESET}")
        traceback.print_exc()
        sys.exit(1)