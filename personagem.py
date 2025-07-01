# personagem.py

import random
from cores import Cor
# A importação das classes de Item foi movida para o final para evitar importação circular
# já que Inimigo também está neste arquivo e é usado em outros lugares.

class Personagem:
    def __init__(self, nome, nivel, hp, mp, forca, destreza, inteligencia, vitalidade, sabedoria):
        self.nome = nome
        self.nivel = nivel
        self.hp_max = hp
        self.hp_atual = hp
        self.mp_max = mp
        self.mp_atual = mp
        self.forca = forca
        self.destreza = destreza
        self.inteligencia = inteligencia
        self.vitalidade = vitalidade
        self.sabedoria = sabedoria
        self.esta_vivo = True
        self.equipamento = {"arma": None, "armadura": None, "escudo": None}
        self.aflicoes = []
        self._log_callback = lambda msg: print(msg)

    def _set_log_callback(self, callback_func):
        self._log_callback = callback_func

    def sofrer_dano(self, dano):
        dano_original = dano
        dano_reduzido = 0
        dano_final = dano

        # Efeito de escudo de item/habilidade
        for aflicao in list(self.aflicoes):
            if aflicao.get("tipo") == "escudo_critico":
                percentual_absorcao = aflicao["percentual_absorcao"] / 100
                dano_absorvido = int(dano_final * percentual_absorcao)
                dano_reduzido += dano_absorvido
                dano_final = max(0, dano_final - dano_absorvido)
                aflicao["duracao"] -= 1
                if aflicao["duracao"] <= 0:
                    self._log_callback(f"{Cor.CIANO_BRILHANTE}O escudo de energia de {self.nome} se dissipou.{Cor.RESET}")
                    self.aflicoes.remove(aflicao)
                break
        
        # Lógica de bloqueio do escudo (se equipado)
        if isinstance(self, Jogador) and self.equipamento["escudo"]:
            if random.random() < self.equipamento["escudo"].chance_bloqueio:
                # Bloqueio reduz o dano com base na defesa do escudo
                reducao_bloqueio = self.equipamento["escudo"].defesa + self.vitalidade // 2
                dano_reduzido += reducao_bloqueio
                dano_final = max(0, dano_final - reducao_bloqueio)
                self._log_callback(f"🛡️ {Cor.AZUL_BRILHANTE}{self.nome} bloqueou com o escudo!{Cor.RESET}")

        if dano_reduzido > 0:
            self._log_callback(f"{Cor.AZUL_BRILHANTE}A defesa de {self.nome} reduziu {dano_reduzido} de dano!{Cor.RESET}")

        dano_a_aplicar = max(1, dano_final)
        self.hp_atual -= dano_a_aplicar
        
        if self.hp_atual <= 0:
            self.hp_atual = 0
            self.esta_vivo = False
            self._log_callback(f"{Cor.VERMELHO_BRILHANTE}!!! {self.nome} foi derrotado(a)! !!!{Cor.RESET}")

    def curar(self, quantidade):
        quantidade = max(0, quantidade)
        hp_antes = self.hp_atual
        self.hp_atual += quantidade
        if self.hp_atual > self.hp_max:
            self.hp_atual = self.hp_max
        cura_realizada = self.hp_atual - hp_antes
        self._log_callback(f"{Cor.VERDE}{self.nome} curou {cura_realizada} HP. HP atual: {self.hp_atual}/{self.hp_max}{Cor.RESET}")

    def usar_mana(self, quantidade):
        custo_efetivo = quantidade
        if isinstance(self, Jogador) and self.equipamento["arma"] and self.equipamento["arma"].propriedades.get("reducao_custo_mana_percentual", 0) > 0:
            reducao = self.equipamento["arma"].propriedades["reducao_custo_mana_percentual"]
            custo_efetivo = int(quantidade * (1 - reducao))
            self._log_callback(f"{Cor.AZUL_BRILHANTE}Custo de mana reduzido em {reducao*100}% por {self.equipamento['arma'].nome}.{Cor.RESET}")

        custo_efetivo = max(0, custo_efetivo)

        if self.mp_atual >= custo_efetivo:
            self.mp_atual -= custo_efetivo
            return True
        else:
            self._log_callback(f"{Cor.AMARELO}Mana insuficiente. Custo: {custo_efetivo}, Atual: {self.mp_atual}{Cor.RESET}")
            return False

    def regenerar_mana(self):
        quantidade_regen = max(1, self.sabedoria // 4)
        if isinstance(self, Jogador) and self.equipamento.get("arma") and self.equipamento["arma"].propriedades.get("regeneracao_mana_por_turno", 0) > 0:
            bonus_regen = self.equipamento["arma"].propriedades["regeneracao_mana_por_turno"]
            quantidade_regen += bonus_regen
            self._log_callback(f"{Cor.AZUL_BRILHANTE}+{bonus_regen} de Mana regenerada por {self.equipamento['arma'].nome}!{Cor.RESET}")

        mp_antes = self.mp_atual
        self.mp_atual += quantidade_regen
        if self.mp_atual > self.mp_max:
            self.mp_atual = self.mp_max
        
        regen_real = self.mp_atual - mp_antes
        if regen_real > 0:
            self._log_callback(f"{self.nome} regenerou {regen_real} mana.")

class Jogador(Personagem):
    def __init__(self, nome, classe_personagem, log_func):
        self.classe_personagem = classe_personagem
        if classe_personagem == "Guerreiro":
            super().__init__(nome, 1, 150, 40, 12, 5, 3, 10, 4)
            self.chance_critico_base = 0.05
            self.chance_critico_magico_base = 0.01
        elif classe_personagem == "Mago":
            super().__init__(nome, 1, 90, 100, 4, 4, 12, 6, 10)
            self.chance_critico_base = 0.02
            self.chance_critico_magico_base = 0.10
        elif classe_personagem == "Arqueiro":
            super().__init__(nome, 1, 110, 60, 6, 12, 4, 7, 7)
            self.chance_critico_base = 0.08
            self.chance_critico_magico_base = 0.03
        elif classe_personagem == "Ladino":
            super().__init__(nome, 1, 100, 50, 7, 12, 5, 6, 5)
            self.chance_critico_base = 0.12
            self.chance_critico_magico_base = 0.02
        else:
            raise ValueError("Classe inválida.")

        self._set_log_callback(log_func)
        self.xp = 0
        self.xp_para_proximo_nivel = 100
        self.ouro = 150
        self.inventario = []
        self.pontos_habilidade = 0
        self.habilidades_conhecidas = []
        self.chance_critico_bonus = 0.0
        self.chance_critico_magico_bonus = 0.0
        self.resistencia_defesa_fisica_base = 0
        self.fragmentos_coletados = set()
        self._adicionar_equipamento_inicial()

    def _adicionar_equipamento_inicial(self):
        from item import todas_armas, todas_armaduras, todos_escudos
        self._log_callback(f"\nDistribuindo equipamento inicial para {self.nome}...")
        
        arma_inicial, armadura_inicial, escudo_inicial = None, None, None

        if self.classe_personagem == "Guerreiro":
            arma_inicial = next((w for w in todas_armas if w.nome == "Espada Curta Enferrujada"), None)
            armadura_inicial = next((a for a in todas_armaduras if a.nome == "Cota de Malha Remendada"), None)
            escudo_inicial = next((s for s in todos_escudos if s.nome == "Escudo de Ferro"), None)
        elif self.classe_personagem == "Mago":
            arma_inicial = next((w for w in todas_armas if w.nome == "Cajado de Salgueiro Encantado"), None)
            armadura_inicial = next((a for a in todas_armaduras if a.nome == "Túnica Simples de Pano"), None)
        elif self.classe_personagem == "Arqueiro":
            arma_inicial = next((w for w in todas_armas if w.nome == "Arco Curto de Galho"), None)
            armadura_inicial = next((a for a in todas_armaduras if a.nome == "Gibão de Couro"), None)
        elif self.classe_personagem == "Ladino":
            arma_inicial = next((w for w in todas_armas if w.nome == "Adaga de Couro"), None)
            armadura_inicial = next((a for a in todas_armaduras if a.nome == "Gibão de Couro"), None)

        if arma_inicial: self.equipar_item(arma_inicial, silencioso=True)
        if armadura_inicial: self.equipar_item(armadura_inicial, silencioso=True)
        if escudo_inicial: self.equipar_item(escudo_inicial, silencioso=True)
        
        self._log_callback("Equipamento inicial pronto!")

    def ganhar_xp(self, quantidade):
        self.xp += quantidade
        self._log_callback(f"{Cor.VERDE_BRILHANTE}Você ganhou {quantidade} XP! Total: {self.xp}/{self.xp_para_proximo_nivel}{Cor.RESET}")
        while self.xp >= self.xp_para_proximo_nivel:
            self.subir_nivel()

    def subir_nivel(self):
        self.nivel += 1
        self.xp -= self.xp_para_proximo_nivel
        self.xp_para_proximo_nivel = int(self.xp_para_proximo_nivel * 1.15)
        self.pontos_habilidade += 3
        self._log_callback(f"{Cor.AMARELO_BRILHANTE}\n{'*' * 15} LEVEL UP! {'*' * 15}{Cor.RESET}")
        self._log_callback(f"{Cor.AMARELO_BRILHANTE}✨ PARABÉNS! {self.nome} atingiu o Nível {self.nivel}! ✨{Cor.RESET}")
        self.aplicar_status_subida_nivel()
        self.hp_atual = self.hp_max
        self.mp_atual = self.mp_max
        self._log_callback(f"{Cor.AMARELO_BRILHANTE}{'*' * (38)}{Cor.RESET}\n")


    def aplicar_status_subida_nivel(self):
        if self.classe_personagem == "Guerreiro":
            self.forca += 4; self.vitalidade += 4; self.hp_max += 25
            self._log_callback(f"{Cor.VERDE}+4 Força, +4 Vitalidade, +25 HP Máximo.{Cor.RESET}")
        elif self.classe_personagem == "Mago":
            self.inteligencia += 4; self.sabedoria += 4; self.mp_max += 20
            self._log_callback(f"{Cor.AZUL}+4 Inteligência, +4 Sabedoria, +20 MP Máximo.{Cor.RESET}")
        elif self.classe_personagem == "Arqueiro":
            self.destreza += 4; self.forca += 2; self.vitalidade += 2; self.hp_max += 15; self.mp_max += 10
            self._log_callback(f"{Cor.CIANO}+4 Destreza, +2 Força, +2 Vitalidade, +15 HP Máx, +10 MP Máx.{Cor.RESET}")
        elif self.classe_personagem == "Ladino":
            self.destreza += 4; self.forca += 2; self.vitalidade += 1; self.hp_max += 12; self.mp_max += 8
            self._log_callback(f"{Cor.MAGENTA}+4 Destreza, +2 Força, +1 Vitalidade, +12 HP Máx, +8 MP Máx.{Cor.RESET}")

    def distribuir_pontos_habilidade(self, atributo, pontos):
        if self.pontos_habilidade >= pontos:
            if atributo == "forca": self.forca += pontos
            elif atributo == "destreza": self.destreza += pontos
            elif atributo == "inteligencia": self.inteligencia += pontos
            elif atributo == "vitalidade": self.vitalidade += pontos; self.hp_max += (pontos * 5)
            elif atributo == "sabedoria": self.sabedoria += pontos; self.mp_max += (pontos * 3)
            self.pontos_habilidade -= pontos
            self._log_callback(f"Distribuídos {pontos} pontos para {atributo} com sucesso.")
            return True
        self._log_callback(f"Pontos de habilidade insuficientes. Você tem {self.pontos_habilidade}.")
        return False

    def equipar_item(self, item, silencioso=False):
        # ALTERADO: Adicionado verificação de nível
        if self.nivel < item.level_req:
            if not silencioso:
                self._log_callback(f"{Cor.VERMELHO}Nível insuficiente para equipar {item.nome}. Requer Nível {item.level_req}, você é Nível {self.nivel}.{Cor.RESET}")
            return False

        item_antigo = None
        slot_alvo = None
        if item.tipo_item == "arma": slot_alvo = "arma"
        elif item.tipo_item == "armadura": slot_alvo = "armadura"
        elif item.tipo_item == "escudo": slot_alvo = "escudo"
        else:
            if not silencioso: self._log_callback("Este item não pode ser equipado.")
            return False

        if self.equipamento.get(slot_alvo):
            item_antigo = self.equipamento[slot_alvo]
            self._remover_efeitos_item(item_antigo)
            self.inventario.append(item_antigo)
            if not silencioso: self._log_callback(f"'{item_antigo.nome}' foi desequipado e voltou para o seu inventário.")

        self.equipamento[slot_alvo] = item
        if item in self.inventario: self.inventario.remove(item)
        if not silencioso: self._log_callback(f"'{item.nome}' equipado como {item.tipo_item}.")
        self._aplicar_efeitos_item(item)
        return True

    def _aplicar_efeitos_item(self, item):
        if item.bonus_atributo:
            for atr, bonus in item.bonus_atributo.items():
                if hasattr(self, atr): setattr(self, atr, getattr(self, atr) + bonus)
        if item.propriedades:
            if "chance_critico_bonus_percentual" in item.propriedades: self.chance_critico_bonus += item.propriedades["chance_critico_bonus_percentual"]
            if "resistencia_defesa_fisica" in item.propriedades: self.resistencia_defesa_fisica_base += item.propriedades["resistencia_defesa_fisica"]
            if "bonus_hp_max" in item.propriedades: self.hp_max += item.propriedades["bonus_hp_max"]; self.hp_atual += item.propriedades["bonus_hp_max"]
            if "bonus_mp_max" in item.propriedades: self.mp_max += item.propriedades["bonus_mp_max"]; self.mp_atual += item.propriedades["bonus_mp_max"]

    def _remover_efeitos_item(self, item):
        if item.bonus_atributo:
            for atr, bonus in item.bonus_atributo.items():
                if hasattr(self, atr): setattr(self, atr, getattr(self, atr) - bonus)
        if item.propriedades:
            if "chance_critico_bonus_percentual" in item.propriedades: self.chance_critico_bonus -= item.propriedades["chance_critico_bonus_percentual"]
            if "resistencia_defesa_fisica" in item.propriedades: self.resistencia_defesa_fisica_base -= item.propriedades["resistencia_defesa_fisica"]
            if "bonus_hp_max" in item.propriedades: self.hp_max -= item.propriedades["bonus_hp_max"]; self.hp_atual = min(self.hp_atual, self.hp_max)
            if "bonus_mp_max" in item.propriedades: self.mp_max -= item.propriedades["bonus_mp_max"]; self.mp_atual = min(self.mp_atual, self.mp_max)

from item import Arma, Armadura, Consumivel, FragmentoLiterario