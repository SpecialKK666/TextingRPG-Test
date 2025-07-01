# inimigo.py

import random
from cores import Cor
from personagem import Personagem

class Inimigo(Personagem):
    def __init__(self, nome, rank, nivel, hp, mp, forca, destreza, inteligencia, vitalidade, sabedoria, recompensa_xp,
                 recompensa_ouro, tabela_drop, habilidades=None, descricao="Uma criatura hostil das profundezas."):
        super().__init__(nome, nivel, hp, mp, forca, destreza, inteligencia, vitalidade, sabedoria)
        self.rank = rank  # 'Comum', 'Capitão', 'General', 'Rei'
        self.recompensa_xp = recompensa_xp
        self.recompensa_ouro = recompensa_ouro
        self.tabela_drop = tabela_drop
        self.habilidades = habilidades if habilidades else []
        self.descricao = descricao
        self._log_callback = lambda msg: print(msg)

    def _set_log_callback(self, callback_func):
        self._log_callback = callback_func

    def exibir_status_combate(self):
        self._log_callback(f"\n{Cor.VERMELHO_BRILHANTE}--- Status de {self.nome} ({self.rank}) ---{Cor.RESET}")
        self._log_callback(f"HP: {self.hp_atual}/{self.hp_max} | MP: {self.mp_atual}/{self.mp_max}")
        self._log_callback(f"Nível: {self.nivel}")
        self._log_callback(f"Descrição: {self.descricao}")
        
        if self.aflicoes:
            self._log_callback("Aflições Ativas:")
            for aflicao in self.aflicoes:
                duracao = aflicao.get('duracao', 'N/A')
                self._log_callback(f" - {aflicao['nome']} (Duração: {duracao if duracao != float('inf') else 'Permanente'})")
        else:
            self._log_callback("Aflições Ativas: Nenhuma")
        
        habilidades_conhecidas = [hab['nome'] for hab in self.habilidades if hab['nome'] != "Ataque Simples"]
        if habilidades_conhecidas:
             self._log_callback("Habilidades Notáveis:")
             self._log_callback(f" - {', '.join(habilidades_conhecidas)}")
        self._log_callback(f"{Cor.VERMELHO_BRILHANTE}{'-' * (len(self.nome) + len(self.rank) + 14)}{Cor.RESET}\n")

# --- Habilidades Inimigas ---
HABILIDADES_INIMIGAS = {
    "ataque_normal": {"nome": "Ataque Simples", "tipo": "fisico", "multiplicador": 1.0, "custo": 0, "chance": 1.0},
    "ataque_forte": {"nome": "Golpe Pesado", "tipo": "fisico", "multiplicador": 1.5, "custo": 5, "chance": 0.4},
    "mordida_venenosa": {"nome": "Mordida Venenosa", "tipo": "dano_ao_longo_do_tempo", "duracao": 3, "dano_por_turno": 5, "custo": 7, "chance": 0.4},
    "raio_arcano": {"nome": "Raio Arcano", "tipo": "magico", "multiplicador": 1.2, "custo": 10, "chance": 0.5},
    "maldicao_enfraquecedora": {"nome": "Maldição Enfraquecedora", "tipo": "debuff", "tipo_debuff": "debuff_forca", "quantidade_debuff": 0.15, "duracao": 3, "custo": 15, "chance": 0.3},
    "enfurecer": {"nome": "Enfurecer", "tipo": "buff", "tipo_buff": "buff_forca", "quantidade_buff": 0.25, "duracao": 3, "custo": 10, "chance": 0.2},
    "fortificar": {"nome": "Fortificar", "tipo": "buff", "tipo_buff": "buff_defesa", "quantidade_buff": 0.30, "duracao": 3, "custo": 12, "chance": 0.2},
    "punhalada_rapida": {"nome": "Punhalada Rápida", "tipo": "fisico", "multiplicador": 0.8, "acertos": 2, "custo": 8, "chance": 0.4},
    "grito_aterrorizante": {"nome": "Grito Aterrorizante", "tipo": "debuff", "tipo_debuff": "medo", "duracao": 1, "custo": 20, "chance": 0.25},
    "cura_menor": {"nome": "Cura Menor", "tipo": "cura", "quantidade": 50, "custo": 15, "chance": 0.15},
    "bola_de_fogo": {"nome": "Bola de Fogo", "tipo": "magico", "multiplicador": 1.4, "custo": 12, "chance": 0.4},
    "chuva_de_flechas": {"nome": "Chuva de Flechas", "tipo": "fisico", "multiplicador": 1.1, "aoe": True, "custo": 18, "chance": 0.3}
}

# --- Definição dos Inimigos por Rank ---
# (Valores de XP e Ouro são apenas base, serão escalados)
monstros_comuns = [
    Inimigo("Batedor Goblin", "Comum", 1, 35, 0, 6, 8, 2, 6, 2, 10, 5, {"normal": 0.20}, descricao="Pequeno e covarde, prefere atacar em grupos e fugir quando em desvantagem."),
    Inimigo("Ladrão Goblin", "Comum", 2, 40, 5, 5, 10, 2, 6, 2, 12, 8, {"normal": 0.25}, descricao="Um goblin ágil que se move nas sombras, buscando bolsos desatentos."),
    Inimigo("Guerreiro Goblin", "Comum", 3, 60, 10, 10, 6, 3, 8, 3, 15, 12, {"normal": 0.15}, descricao="Armado com sucata afiada, este goblin é mais corajoso que seus pares."),
    Inimigo("Goblin com Funda", "Comum", 2, 30, 0, 4, 9, 1, 5, 2, 11, 6, {"normal": 0.22}, descricao="Mantém distância, atirando pedras com uma precisão irritante."),
    Inimigo("Goblin Sucateiro", "Comum", 1, 45, 0, 7, 5, 2, 7, 2, 9, 10, {"normal": 0.30}, descricao="Carrega uma armadura improvisada de lixo metálico, tornando-o surpreendentemente resistente."),
    Inimigo("Rato de Esgoto Gigante", "Comum", 1, 30, 0, 5, 7, 1, 5, 1, 8, 3, {"normal": 0.1}, descricao="Uma praga comum nos andares superiores, seus dentes podem transmitir doenças."),
    Inimigo("Morcego Sanguessuga", "Comum", 2, 25, 10, 4, 11, 2, 4, 3, 9, 4, {"normal": 0.15}, descricao="Voa erraticamente, tentando se prender à sua vítima para drenar seu sangue."),
    Inimigo("Esqueleto Frágil", "Comum", 3, 50, 0, 8, 5, 1, 6, 1, 12, 7, {"normal": 0.18}, descricao="Restos reanimados de um aventureiro azarado. Seus ossos estalam a cada movimento."),
    Inimigo("Zumbi Apodrecido", "Comum", 4, 70, 0, 9, 3, 1, 9, 1, 14, 9, {"normal": 0.20}, descricao="Lento e previsível, mas seu toque pode espalhar a podridão necrosante."),
    Inimigo("Aranha da Caverna", "Comum", 2, 38, 5, 6, 9, 2, 5, 2, 11, 6, {"normal": 0.20}, descricao="Tece teias pegajosas para prender suas presas antes de injetar seu veneno paralisante."),
]

monstros_capitaes = [
    Inimigo("Chefe de Guerra Goblin 'Racha-Crânios'", "Capitão", 8, 250, 20, 20, 12, 5, 18, 8, 100, 50, {"normal": 0.1, "magica": 0.2}, [HABILIDADES_INIMIGAS["ataque_forte"], HABILIDADES_INIMIGAS["enfurecer"]], "Um goblin anormalmente grande com um capacete feito de um crânio. Lidera pelo medo e pela força bruta."),
    Inimigo("Carcereiro Esqueleto Amaldiçoado", "Capitão", 10, 300, 40, 22, 10, 10, 20, 12, 120, 60, {"magica": 0.25}, [HABILIDADES_INIMIGAS["ataque_forte"], HABILIDADES_INIMIGAS["maldicao_enfraquecedora"]], "Este esqueleto guarda as chaves de celas esquecidas e usa correntes como arma. Sua maldição enfraquece a vontade de lutar."),
    Inimigo("Matriarca da Ninhada de Aranhas", "Capitão", 12, 280, 30, 18, 15, 8, 16, 10, 110, 55, {"magica": 0.22}, [HABILIDADES_INIMIGAS["mordida_venenosa"], HABILIDADES_INIMIGAS["punhalada_rapida"]], "Uma aranha gigante cujo abdômen pulsa com ovos. Defende seu ninho com uma fúria venenosa e ataques rápidos."),
    Inimigo("Ogro Brutamontes", "Capitão", 15, 450, 10, 30, 8, 4, 25, 5, 150, 80, {"magica": 0.15, "rara": 0.05}, [HABILIDADES_INIMIGAS["ataque_forte"]], "Grande, estúpido e incrivelmente forte. Usa um tronco de árvore como clava e esmaga tudo em seu caminho."),
    Inimigo("Xamã Goblin", "Capitão", 9, 200, 80, 10, 12, 18, 14, 15, 130, 70, {"magica": 0.3}, [HABILIDADES_INIMIGAS["bola_de_fogo"], HABILIDADES_INIMIGAS["cura_menor"]], "Um goblin astuto que aprendeu os rudimentos da magia elemental e de cura, tornando seu grupo muito mais perigoso."),
]

monstros_generais = [
    Inimigo("General Orc Vrak, o Punho de Ferro", "General", 20, 1200, 80, 45, 15, 10, 35, 15, 500, 250, {"rara": 0.15}, [HABILIDADES_INIMIGAS["ataque_forte"], HABILIDADES_INIMIGAS["enfurecer"], HABILIDADES_INIMIGAS["grito_aterrorizante"]], "Um orc veterano com uma armadura de placas e uma reputação temível. Comanda legiões de monstros menores."),
    Inimigo("Arquilich Zarthus, o Colecionador de Almas", "General", 25, 950, 300, 20, 18, 50, 28, 40, 700, 350, {"rara": 0.20, "épico": 0.05}, [HABILIDADES_INIMIGAS["raio_arcano"], HABILIDADES_INIMIGAS["maldicao_enfraquecedora"], HABILIDADES_INIMIGAS["cura_menor"]], "Um mago que enganou a morte, mas perdeu sua humanidade no processo. Seu poder sobre a necromancia é vasto."),
    Inimigo("Golem de Obsidiana", "General", 30, 1500, 50, 60, 5, 5, 50, 10, 800, 400, {"rara": 0.25}, [HABILIDADES_INIMIGAS["ataque_forte"], HABILIDADES_INIMIGAS["fortificar"]], "Uma construção mágica imensa, imune a ataques normais. Sua pele de obsidiana é quase impenetrável."),
    Inimigo("Lorde Vampiro Alucard", "General", 35, 1100, 150, 40, 35, 30, 30, 25, 900, 500, {"rara": 0.1, "épico": 0.1}, [HABILIDADES_INIMIGAS["punhalada_rapida"], HABILIDADES_INIMIGAS["mordida_venenosa"]], "Um nobre amaldiçoado com a imortalidade e a sede de sangue. Move-se com velocidade sobrenatural e regenera seus ferimentos."),
]

monstros_reis = [
    Inimigo("Rei Ogro Grolnok, o Devorador", "Rei", 35, 5000, 150, 80, 10, 15, 60, 20, 2000, 1000, {"épico": 0.15, "lendario": 0.02}, [HABILIDADES_INIMIGAS["ataque_forte"], HABILIDADES_INIMIGAS["enfurecer"], HABILIDADES_INIMIGAS["fortificar"]], "Um monarca brutal cujo apetite é tão grande quanto seu reino subterrâneo. Cada aventureiro derrotado é apenas mais uma refeição."),
    Inimigo("A Rainha Lich, Soberana dos Caídos", "Rei", 40, 3800, 1200, 40, 25, 100, 45, 80, 3000, 1500, {"épico": 0.20, "lendario": 0.05}, [HABILIDADES_INIMIGAS["raio_arcano"], HABILIDADES_INIMIGAS["grito_aterrorizante"], HABILIDADES_INIMIGAS["maldicao_enfraquecedora"], HABILIDADES_INIMIGAS["cura_menor"]], "A governante de todos os mortos-vivos da masmorra, seu poder arcano é lendário e sua crueldade, infinita."),
    Inimigo("Dragão Vermelho Ancestral, Ignis", "Rei", 50, 7500, 500, 120, 15, 80, 80, 50, 5000, 3000, {"épico": 0.25, "lendario": 0.1}, [HABILIDADES_INIMIGAS["bola_de_fogo"], HABILIDADES_INIMIGAS["grito_aterrorizante"], HABILIDADES_INIMIGAS["ataque_forte"]], "Uma das criaturas mais antigas e poderosas. Seu covil é um mar de ouro e ossos, e seu sopro de fogo pode derreter aço."),
    Inimigo("O Avatar do Sofrimento Eterno", "Rei", 60, 10000, 2000, 100, 40, 120, 100, 100, 10000, 5000, {"lendario": 0.2, "excelencia": 0.01}, [HABILIDADES_INIMIGAS["maldicao_enfraquecedora"], HABILIDADES_INIMIGAS["grito_aterrorizante"], HABILIDADES_INIMIGAS["raio_arcano"]], "A personificação da própria masmorra. Uma entidade de pura malícia e desespero que busca consumir toda a esperança."),
]

# Lista agregada para seleção aleatória inicial (será filtrada por rank no main.py)
todos_os_monstros_base = monstros_comuns + monstros_capitaes + monstros_generais + monstros_reis