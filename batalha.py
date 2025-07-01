# batalha.py

import random
from cores import Cor

class Batalha:
    def __init__(self, jogador, inimigo, log_callback):
        self.jogador = jogador
        self.inimigo = inimigo
        self.adicionar_mensagem = log_callback
        self.jogador._set_log_callback(self.adicionar_mensagem)
        self.inimigo._set_log_callback(self.adicionar_mensagem)

    def processar_turno_jogador(self, acao, dados_habilidade=None):
        """Processa a ação do jogador e retorna True se o turno foi consumido."""
        if acao == "atacar":
            self.adicionar_mensagem(f"{Cor.CIANO}{self.jogador.nome} ataca {self.inimigo.nome}!{Cor.RESET}")
            self.executar_ataque(self.jogador, self.inimigo)
            return True
        elif acao == "habilidade":
            if dados_habilidade:
                self.executar_habilidade_jogador(dados_habilidade)
                return True
        elif acao == "fugir":
            if self.tentar_fuga():
                # A fuga em si é tratada no main.py, aqui apenas validamos
                return False # Fuga bem-sucedida não consome o turno do inimigo
            else:
                return True # Fuga falhou, consome o turno
        
        self.adicionar_mensagem("Ação inválida no processamento da batalha.")
        return False

    def processar_turno_inimigo(self):
        """Processa o turno completo do inimigo."""
        if not self.inimigo.esta_vivo or not self.jogador.esta_vivo:
            return

        self.adicionar_mensagem(f"\n{Cor.VERMELHO_BRILHANTE}--- Turno de {self.inimigo.nome} ---{Cor.RESET}")
        
        if any(a.get("tipo") in ["atordoamento", "congelar", "medo"] for a in self.inimigo.aflicoes):
            self.adicionar_mensagem(f"{Cor.AMARELO}{self.inimigo.nome} está incapacitado e não pode agir!{Cor.RESET}")
            return

        habilidade_escolhida = self.escolher_acao_inimiga()
        if habilidade_escolhida:
            self.adicionar_mensagem(f"{Cor.VERMELHO}{self.inimigo.nome} usa '{habilidade_escolhida['nome']}'!{Cor.RESET}")
            if self.inimigo.usar_mana(habilidade_escolhida.get('custo', 0)):
                self.executar_ataque(self.inimigo, self.jogador, habilidade_escolhida)
            else:
                self.adicionar_mensagem(f"{self.inimigo.nome} tentou, mas falhou em usar a habilidade.")
                self.executar_ataque(self.inimigo, self.jogador) # Ataque básico como fallback
        else:
            self.executar_ataque(self.inimigo, self.jogador) # Ataque básico como fallback

    def executar_ataque(self, atacante, defensor, habilidade=None):
        nome_ataque = "um ataque básico"
        if habilidade:
            nome_ataque = f"a habilidade '{habilidade['nome']}'"
        
        dano, critico = self.calcular_dano(atacante, defensor, dados_habilidade=habilidade)
        
        cor_atacante = Cor.CIANO if isinstance(atacante, self.jogador.__class__) else Cor.VERMELHO
        
        if critico:
            self.adicionar_mensagem(f"{Cor.LARANJA}💥 ACERTO CRÍTICO! {atacante.nome} usou {nome_ataque} e causou {dano} de dano em {defensor.nome}! 💥{Cor.RESET}")
        else:
            if dano > 0:
                 self.adicionar_mensagem(f"{cor_atacante}{atacante.nome} atacou com {nome_ataque} causando {dano} de dano em {defensor.nome}.{Cor.RESET}")
            else:
                 self.adicionar_mensagem(f"{atacante.nome} atacou {defensor.nome}, mas não causou dano.")

        defensor.sofrer_dano(dano)

    def calcular_dano(self, atacante, defensor, dados_habilidade=None):
        dano_base = 0
        is_critico = False
        multiplicador = 1.0
        
        tipo_ataque = "fisico"
        if dados_habilidade and dados_habilidade.get("tipo"):
            tipo_ataque = dados_habilidade['tipo']
            multiplicador = dados_habilidade.get("multiplicador", 1.0)

        # Cálculo do dano base e chance de crítico
        if tipo_ataque == 'magico':
            dano_base = random.randint(atacante.inteligencia, atacante.inteligencia * 2)
            chance_critico_total = getattr(atacante, 'chance_critico_magico_base', 0.02)
        else: # Físico
            dano_base = random.randint(atacante.forca, atacante.forca * 2)
            chance_critico_total = getattr(atacante, 'chance_critico_base', 0.05)
        
        # Adicionar bônus de chance de crítico do equipamento (se for jogador)
        if isinstance(atacante, self.jogador.__class__):
             chance_critico_total += atacante.chance_critico_bonus

        dano_total = dano_base * multiplicador

        # Aplicar crítico
        if random.random() < chance_critico_total:
            is_critico = True
            dano_total *= 1.5

        # Cálculo da defesa
        defesa_defensor = defensor.vitalidade // 2 + getattr(defensor, 'resistencia_defesa_fisica_base', 0)
        
        # Dano final
        dano_final = max(0, int(dano_total - defesa_defensor))
        return dano_final, is_critico
    
    def tentar_fuga(self):
        self.adicionar_mensagem(f"{Cor.AZUL}Você tenta fugir...{Cor.RESET}")
        
        rank_mod = {'Comum': 0.20, 'Capitão': 0.0, 'General': -0.25, 'Rei': -0.50}.get(self.inimigo.rank, 0.0)
        nivel_mod = (self.jogador.nivel - self.inimigo.nivel) * 0.05
        destreza_mod = (self.jogador.destreza - self.inimigo.destreza) * 0.01
        
        chance_fuga = 0.5 + rank_mod + nivel_mod + destreza_mod
        chance_fuga = max(0.05, min(0.95, chance_fuga))

        if random.random() < chance_fuga:
            self.adicionar_mensagem(f"{Cor.VERDE_BRILHANTE}Você conseguiu escapar e recuou para a sala anterior! 💨{Cor.RESET}")
            return True
        else:
            self.adicionar_mensagem(f"{Cor.VERMELHO}A fuga falhou! O inimigo bloqueia seu caminho!{Cor.RESET}")
            return False
            
    def escolher_acao_inimiga(self):
        habilidades_usaveis = [h for h in self.inimigo.habilidades if self.inimigo.mp_atual >= h.get("custo", 0) and random.random() < h.get("chance", 1.0)]
        
        # Lógica de cura
        habilidades_cura = [h for h in habilidades_usaveis if h.get("tipo") == "cura"]
        if habilidades_cura and self.inimigo.hp_atual < self.inimigo.hp_max * 0.4: # Mais propenso a curar com menos vida
            return random.choice(habilidades_cura)

        # Lógica de buff/debuff
        habilidades_debuff = [h for h in habilidades_usaveis if h.get("tipo") == "debuff"]
        if habilidades_debuff and not any(a.get("tipo_debuff") == h.get("tipo_debuff") for a in self.jogador.aflicoes):
             if random.random() < 0.3: # Chance de tentar aplicar um debuff
                return random.choice(habilidades_debuff)

        habilidades_dano = [h for h in habilidades_usaveis if h.get("tipo") in ["fisico", "magico"]]
        if habilidades_dano:
            return random.choice(habilidades_dano)
            
        # Fallback para o ataque básico se nenhuma outra opção for escolhida
        from inimigo import HABILIDADES_INIMIGAS
        return HABILIDADES_INIMIGAS.get("ataque_normal")