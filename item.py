# item.py

import random
from cores import Cor

class Item:
    def __init__(self, nome, descricao, raridade, tipo_item, valor, level_req=1):
        self.nome = nome
        self.descricao = descricao
        self.raridade = raridade
        self.tipo_item = tipo_item
        self.valor = valor
        self.level_req = level_req  # NOVO: Requisito de nível para usar/equipar
        self.bonus_atributo = {}
        self.propriedades = {}

    def obter_cor_raridade(self):
        cores = {
            "normal": Cor.BRANCO,
            "magica": Cor.MAGENTA_BRILHANTE,
            "rara": Cor.AZUL_BRILHANTE,
            "épico": Cor.MAGENTA,
            "lendario": Cor.AMARELO_BRILHANTE,
            "excelencia": Cor.VERDE_BRILHANTE,
            "literario": Cor.VERDE,
        }
        return cores.get(self.raridade, Cor.BRANCO)

class Arma(Item):
    def __init__(self, nome, descricao, raridade, valor, dano_min, dano_max, level_req=1, bonus_atributo=None, propriedades=None):
        super().__init__(nome, descricao, raridade, "arma", valor, level_req)
        self.dano_min = dano_min
        self.dano_max = dano_max
        self.bonus_atributo = bonus_atributo if bonus_atributo else {}
        self.propriedades = propriedades if propriedades else {}

class Armadura(Item):
    def __init__(self, nome, descricao, raridade, valor, defesa, level_req=1, bonus_atributo=None, propriedades=None, slot="armadura"):
        super().__init__(nome, descricao, raridade, "armadura", valor, level_req)
        self.defesa = defesa
        self.bonus_atributo = bonus_atributo if bonus_atributo else {}
        self.propriedades = propriedades if propriedades else {}
        self.slot = slot

class Escudo(Item):
    def __init__(self, nome, descricao, raridade, valor, defesa, chance_bloqueio, level_req=1, bonus_atributo=None, propriedades=None):
        super().__init__(nome, descricao, raridade, "escudo", valor, level_req)
        self.defesa = defesa
        self.chance_bloqueio = chance_bloqueio
        self.bonus_atributo = bonus_atributo if bonus_atributo else {}
        self.propriedades = propriedades if propriedades else {}

class Consumivel(Item):
    def __init__(self, nome, descricao, raridade, valor, quantidade_curar=0, quantidade_restaurar_mana=0, level_req=1):
        super().__init__(nome, descricao, raridade, "consumivel", valor, level_req)
        self.quantidade_curar = quantidade_curar
        self.quantidade_restaurar_mana = quantidade_restaurar_mana

class FragmentoLiterario(Item):
    def __init__(self, id_fragmento, nome, conteudo):
        super().__init__(nome, "Um fragmento de lendas esquecidas de Aethelgard.", "literario", "literario", 1, 1)
        self.id_fragmento = id_fragmento
        self.conteudo = conteudo


# --- Dados do Jogo (Listas de Itens) ---
# ALTERADO: Adicionado 'level_req' a todos os equipamentos e criados novos itens.

# ARMAS
todas_armas = [
    # Normal (Nível 1-20)
    Arma("Adaga de Couro", "Uma adaga básica com cabo de couro.", "normal", 8, 4, 8, 1),
    Arma("Porrete de Carvalho Simples", "Um pedaço de madeira pesado.", "normal", 12, 6, 10, 1),
    Arma("Arco Curto de Galho", "Um arco improvisado.", "normal", 15, 5, 9, 1),
    Arma("Cajado Torto de Bordo", "Um galho que mal canaliza energia.", "normal", 9, 3, 5, 1),
    Arma("Machadinha de Lenhador", "Útil para cortar madeira e inimigos.", "normal", 14, 7, 11, 3),
    Arma("Lança Pontiaguda", "Uma haste com uma pedra afiada na ponta.", "normal", 13, 6, 12, 3),
    Arma("Maça de Madeira", "Uma cabeça de madeira pesada numa haste.", "normal", 15, 7, 12, 5),
    Arma("Clava com Pregos", "Um porrete melhorado com pregos enferrujados.", "normal", 16, 8, 13, 5),
    Arma("Soco Inglês de Ferro", "Para quem gosta de resolver as coisas de perto.", "normal", 9, 5, 8, 7),
    Arma("Martelo de Ferreiro", "Pesado e lento, mas o impacto é forte.", "normal", 20, 10, 16, 10),
    Arma("Espadão de Ferro Velho", "Pesado e desbalanceado, mas melhor que nada.", "normal", 25, 12, 20, 15),

    # Mágica (Nível 10-40)
    Arma("Espada Curta Enferrujada", "Uma lâmina de aço que viu combates.", "magica", 25, 10, 16, 10, bonus_atributo={"forca": 2}),
    Arma("Cajado de Salgueiro Encantado", "Um cajado com leve ressonância mágica.", "magica", 30, 8, 14, 10, bonus_atributo={"inteligencia": 2}),
    Arma("Adaga Sibilante", "A lâmina assobia ao cortar o ar.", "magica", 22, 9, 14, 12, propriedades={"chance_critico_bonus_percentual": 0.03}),
    Arma("Maça de Ferro Bruto", "Pesada, ideal para penetrar armaduras leves.", "magica", 28, 12, 18, 15, bonus_atributo={"forca": 3}),
    Arma("Arco de Teixo Elfico", "Leve e preciso, um item comum entre elfos.", "magica", 40, 14, 20, 18, bonus_atributo={"destreza": 4}),
    Arma("Machado de Batalha Orc", "Sujo e brutal, com um encanto de força.", "magica", 38, 15, 22, 20, bonus_atributo={"forca": 4}),
    Arma("Varinha de Cristal", "Um cristal bruto que amplifica magias simples.", "magica", 33, 10, 18, 22, bonus_atributo={"inteligencia": 3}),
    Arma("Besta Leve Reforçada", "Mais potente que um arco comum.", "magica", 35, 13, 19, 25, bonus_atributo={"destreza": 3}),
    Arma("Lâmina de Gelo", "Uma espada curta que emana um frio cortante.", "magica", 50, 20, 28, 30, propriedades={"chance_desacelerar_percentual": 0.10}),
    Arma("Cajado do Xamã Goblin", "Decorado com penas e ossos.", "magica", 45, 15, 25, 35, bonus_atributo={"sabedoria": 3}),
    Arma("Espadão de Aço", "Uma espada de duas mãos bem balanceada.", "magica", 60, 25, 35, 40, bonus_atributo={"forca": 5}),

    # Rara (Nível 30-60)
    Arma("Alabarda do Vigia Noturno", "Usada por guardas de elite.", "rara", 160, 25, 38, 30, bonus_atributo={"forca": 5, "vitalidade": 2}),
    Arma("Lâmina do Assassino Silencioso", "Esta adaga absorve o som.", "rara", 150, 22, 35, 35, bonus_atributo={"destreza": 6}, propriedades={"chance_critico_bonus_percentual": 0.08}),
    Arma("Arco Longo da Floresta Sombria", "Entalhado de madeira antiga.", "rara", 170, 30, 45, 40, bonus_atributo={"destreza": 7, "sabedoria": 2}),
    Arma("Grimório do Vidente Esquecido", "Suas páginas sussurram feitiços.", "rara", 180, 25, 50, 45, bonus_atributo={"inteligencia": 8, "sabedoria": 3}),
    Arma("Cajado de Osso de Dragão", "Feito da fíbula de um dragão jovem.", "rara", 200, 30, 55, 50, bonus_atributo={"inteligencia": 10}),
    Arma("Machado de Batalha do Executor", "Dizem que nunca precisou de um segundo golpe.", "rara", 190, 40, 60, 55, bonus_atributo={"forca": 8}),
    Arma("Katana do Ronin", "Uma lâmina de uma terra distante.", "rara", 168, 27, 41, 60, bonus_atributo={"destreza": 5, "forca": 3}),

    # Épico (Nível 50-80)
    Arma("Espada da Ruína Lunar", "Seus golpes drenam a vitalidade do inimigo.", "épico", 550, 50, 75, 50, bonus_atributo={"forca": 12, "vitalidade": 6}, propriedades={"percentual_roubo_vida": 0.08}),
    Arma("Cajado da Tempestade Ressonante", "Feito de um raio petrificado.", "épico", 600, 45, 80, 55, bonus_atributo={"inteligencia": 15, "sabedoria": 5}, propriedades={"chance_atordoamento": 0.10, "duracao_atordoamento": 1}),
    Arma("Adagas Gêmeas da Sombrathal", "Duas lâminas negras com veneno letal.", "épico", 540, 40, 60, 60, bonus_atributo={"destreza": 16}, propriedades={"chance_desacelerar_percentual": 0.25, "duracao_desaceleracao": 2}),
    Arma("Lâmina Vorpal", "Em um golpe de sorte, pode decapitar o inimigo.", "épico", 700, 60, 95, 65, bonus_atributo={"destreza": 10, "forca": 10}, propriedades={"chance_executar_percentual": 0.05}),
    Arma("Tomo do Arquimago Lich", "Contém o poder de roubar a essência da vida.", "épico", 750, 50, 100, 70, bonus_atributo={"inteligencia": 20, "sabedoria": 10}, propriedades={"roubo_de_mana_percentual": 0.10}),
    Arma("Arco do Caçador de Dragões", "Suas flechas perfuram escamas.", "épico", 680, 70, 110, 75, bonus_atributo={"destreza": 20, "forca": 5}),
    Arma("Devoradora de Almas", "Um machado que se fortalece a cada morte.", "épico", 800, 80, 120, 80, bonus_atributo={"forca": 22}, propriedades={"ganho_forca_por_morte": 1}),

    # Lendário (Nível 70-95)
    Arma("Portadora da Alvorada", "Uma espada que brilha com a luz do sol.", "lendario", 2500, 100, 150, 70, bonus_atributo={"forca": 25, "sabedoria": 15}, propriedades={"dano_extra_mortos_vivos": 1.5, "aura_de_cura": 5}),
    Arma("Sussurro do Vazio", "Adaga forjada da matéria escura.", "lendario", 2400, 90, 130, 75, bonus_atributo={"destreza": 30, "inteligencia": 10}, propriedades={"chance_silenciar": 0.20, "ignorar_defesa_percentual": 0.25}),
    Arma("Quebra-Mundos, o Martelo Sísmico", "Seu impacto pode ser sentido em outros continentes.", "lendario", 3000, 150, 200, 85, bonus_atributo={"forca": 40}, propriedades={"chance_atordoamento_area": 0.25, "duracao_atordoamento": 2}),
    Arma("Paradoxo Temporal", "Um arco que atira flechas que atingem o alvo no passado.", "lendario", 2800, 120, 180, 90, bonus_atributo={"destreza": 35, "sabedoria": 10}, propriedades={"chance_turno_extra": 0.10}),
    Arma("Tomo Infinito de Aethel", "O grimório do primeiro mago.", "lendario", 3200, 100, 200, 95, bonus_atributo={"inteligencia": 40, "sabedoria": 20}, propriedades={"reducao_custo_mana_percentual": 0.25, "copiar_magia_inimiga": 0.10}),

    # Excelência (Nível 100)
    Arma("Lâmina Estilhaço Celestial", "Uma extensão da própria vontade do cosmo.", "excelencia", 10000, 180, 250, 100, bonus_atributo={"inteligencia": 30, "forca": 30, "destreza": 30}, propriedades={"dano_verdadeiro_percentual": 0.20, "imunidade_a_medo": True, "restaurar_recursos_ao_matar_percentual": 0.10}),
    Arma("Fúria do Berserker", "Uma espada que se alimenta da dor de seu portador.", "excelencia", 9000, 200, 300, 100, bonus_atributo={"forca": 50, "vitalidade": -20}, propriedades={"aumento_dano_por_hp_perdido": 0.5, "percentual_roubo_vida": 0.15, "imunidade_a_atordoamento": True}),
    Arma("Olho do Oráculo", "Um cajado que manipula a própria realidade.", "excelencia", 9500, 150, 220, 100, bonus_atributo={"inteligencia": 40, "sabedoria": 40}, propriedades={"chance_negar_dano": 0.15, "reducao_recarga_global": 0.20, "regeneracao_mana_por_turno": 15}),
]

# ARMADURAS
todas_armaduras = [
    # Normal (Nível 1-20)
    Armadura("Túnica Simples de Pano", "Roupa de camponês.", "normal", 8, 3, 1),
    Armadura("Gibão de Couro", "Um colete de couro que cobre o torso.", "normal", 18, 6, 1),
    Armadura("Peitoral de Couro Cru", "Proteção de couro de baixa qualidade.", "normal", 15, 5, 3),
    Armadura("Armadura de Placas de Osso", "Placas de osso amarradas com cipó.", "normal", 22, 8, 5),
    Armadura("Manto de Viajante", "Um manto pesado que protege do tempo.", "normal", 6, 2, 8),
    Armadura("Peitoral de Bronze", "Oferece proteção decente contra cortes.", "normal", 30, 10, 15),

    # Mágica (Nível 10-40)
    Armadura("Cota de Malha Remendada", "Feita de anéis de metal.", "magica", 40, 12, 10, bonus_atributo={"vitalidade": 2}),
    Armadura("Robe de Seda Encantado", "Leve, oferece barreira mágica sutil.", "magica", 30, 8, 12, bonus_atributo={"sabedoria": 2}),
    Armadura("Peitoral de Aço Batido", "Uma única peça de aço moldada.", "magica", 50, 15, 18, bonus_atributo={"forca": 2}),
    Armadura("Armadura de Couro Negro", "Tratado com óleos que facilitam a furtividade.", "magica", 45, 14, 25, bonus_atributo={"destreza": 3}),
    Armadura("Cota de Escamas de Bronze", "Flexível e mais resistente que a malha.", "magica", 55, 18, 30, bonus_atributo={"vitalidade": 3}),
    Armadura("Manto do Estudante", "Encantado para resistir a feitiços.", "magica", 35, 10, 35, bonus_atributo={"inteligencia": 2}),
    Armadura("Peitoral de Ferro Sólido", "Pesado mas muito protetor.", "magica", 70, 25, 40, bonus_atributo={"vitalidade": 5}),

    # Rara (Nível 30-60)
    Armadura("Peitoral de Placas Forjado", "Placas de aço conectadas.", "rara", 170, 28, 30, bonus_atributo={"forca": 5, "vitalidade": 3}),
    Armadura("Manto do Mago de Batalha", "Tecido com fios de metal.", "rara", 160, 22, 35, bonus_atributo={"inteligencia": 6, "vitalidade": 2}),
    Armadura("Armadura de Escamas de Basilisco", "Extremamente resistentes.", "rara", 190, 35, 45, bonus_atributo={"vitalidade": 8}),
    Armadura("Peitoral Espelhado", "Pode refletir feitiços.", "rara", 180, 26, 50, bonus_atributo={"inteligencia": 4}, propriedades={"chance_refletir_magia": 0.05}),
    Armadura("Armadura de Coral Encantado", "Respira debaixo d'água.", "rara", 160, 24, 55, bonus_atributo={"vitalidade": 6}),
    Armadura("Cota de Mithril", "Leve como pluma, resistente como aço.", "rara", 250, 40, 60, bonus_atributo={"destreza": 5, "vitalidade": 5}),

    # Épico (Nível 50-80)
    Armadura("Armadura do Dragão Escamado", "Reflete ataques de fogo.", "épico", 680, 55, 50, bonus_atributo={"forca": 10, "vitalidade": 10}, propriedades={"resistencia_fogo_percentual": 0.20}),
    Armadura("Peitoral do Colosso", "Pesada como parte de uma montanha.", "épico", 800, 80, 60, bonus_atributo={"forca": 15, "vitalidade": 15}, propriedades={"resistencia_atordoamento": 0.5}),
    Armadura("Robe do Arquimago", "O tecido é pura energia mágica.", "épico", 640, 45, 65, bonus_atributo={"inteligencia": 18, "sabedoria": 10}, propriedades={"regeneracao_mana_por_turno": 10}),
    Armadura("Abraço de Gaia", "Armadura de madeira viva que se regenera.", "épico", 720, 60, 75, bonus_atributo={"vitalidade": 20}, propriedades={"regeneracao_hp_por_turno": 10}),
    Armadura("Carapaça de Adamantina", "Praticamente indestrutível.", "épico", 900, 90, 80, bonus_atributo={"vitalidade": 25}),

    # Lendário (Nível 70-95)
    Armadura("Peitoral do Rei Anão de Ferro Profundo", "Forjada com metal estelar.", "lendario", 2800, 150, 75, bonus_atributo={"forca": 25, "vitalidade": 25}, propriedades={"resistencia_defesa_fisica": 20, "reducao_dano_recebido_percentual": 0.10}),
    Armadura("Manto do Observador Cósmico", "Tecido com fios de éter.", "lendario", 2500, 80, 80, bonus_atributo={"inteligencia": 30, "sabedoria": 20}, propriedades={"regeneracao_mana_por_turno": 12, "chance_refletir_magia": 0.15}),
    Armadura("Armadura da Fênix Imortal", "Ressuscita seu portador uma vez.", "lendario", 3200, 120, 90, bonus_atributo={"vitalidade": 30, "forca": 15}, propriedades={"auto_ressurreicao": 1, "aura_de_fogo": 10}),
    Armadura("Armadura do Aspecto do Dragão", "Concede o poder de um dragão.", "lendario", 3500, 180, 95, bonus_atributo={"forca": 20, "vitalidade": 20, "inteligencia": 20}, propriedades={"imunidade_a_medo": True}),
    
    # Excelência (Nível 100)
    Armadura("Casca do Mundo-Tartaruga", "Feita do casco de uma criatura mítica.", "excelencia", 10000, 300, 100, bonus_atributo={"vitalidade": 60}, propriedades={"reducao_dano_absoluta": 50, "imunidade_a_criticos": True, "refletir_dano_fisico_percentual": 0.15}),
    Armadura("Manto do Ilusionista Arcano", "Feito de sombra e luar solidificados.", "excelencia", 9500, 120, 100, bonus_atributo={"inteligencia": 45, "destreza": 25}, propriedades={"chance_esquiva_magia_percentual": 0.25, "regeneracao_mana_por_turno": 20, "invisibilidade_inicio_combate": 2}),
    Armadura("Armadura do Vazio Ecoante", "Forjada com o silêncio entre os mundos.", "excelencia", 9800, 150, 100, bonus_atributo={"destreza": 40, "sabedoria": 30}, propriedades={"chance_negar_ataque": 0.20, "roubo_de_velocidade": 0.10, "imunidade_a_lentidao": True}),
]

# ESCUDOS
todos_escudos = [
    # Normal (Nível 1-20)
    Escudo("Escudo de Madeira", "Um escudo simples e leve.", "normal", 12, 5, 0.10, 1),
    Escudo("Brotel de Couro", "Pequeno e ágil.", "normal", 10, 4, 0.12, 3),
    Escudo("Escudo Torre de Madeira", "Grande e pesado, oferece boa cobertura.", "normal", 20, 8, 0.05, 10),

    # Mágico (Nível 10-40)
    Escudo("Escudo de Ferro", "Um escudo resistente de ferro forjado.", "magica", 45, 12, 0.15, 10, bonus_atributo={"vitalidade": 2}),
    Escudo("Brotel Reforçado com Aço", "Ágil com bordas de aço.", "magica", 40, 10, 0.18, 15, bonus_atributo={"destreza": 2}),
    Escudo("Escudo da Sentinela", "Encantado para absorver um pouco mais de impacto.", "magica", 60, 15, 0.14, 25, bonus_atributo={"vitalidade": 4}),
    
    # Raro (Nível 30-60)
    Escudo("Escudo do Guardião Rúnico", "Runas anãs brilham na superfície.", "rara", 180, 25, 0.25, 30, bonus_atributo={"vitalidade": 5, "forca": 2}, propriedades={"resistencia_defesa_fisica": 8}),
    Escudo("Escudo Espelhado", "Pode refletir feitiços de volta.", "rara", 200, 20, 0.20, 40, bonus_atributo={"inteligencia": 4}, propriedades={"chance_refletir_magia": 0.10}),
    Escudo("Muralha do Centurião", "Um escudo torre de aço, quase impenetrável.", "rara", 220, 35, 0.15, 55, bonus_atributo={"forca": 5, "vitalidade": 5}),

    # Épico (Nível 50-80)
    Escudo("Escudo do Dragão Negro", "Absorve magia sombria.", "épico", 700, 50, 0.30, 55, bonus_atributo={"vitalidade": 12}, propriedades={"resistencia_magia_negra_percentual": 0.25}),
    Escudo("Escudo da Reflexão Perfeita", "Reflete uma porção de todo dano recebido.", "épico", 800, 40, 0.25, 70, propriedades={"refletir_dano_percentual": 0.15}),

    # Lendário (Nível 70-95)
    Escudo("Égide Ancestral", "Pode repelir os ataques mais poderosos.", "lendario", 3000, 80, 0.40, 80, bonus_atributo={"vitalidade": 20, "sabedoria": 15}, propriedades={"reducao_dano_recebido_percentual": 0.15, "chance_negar_dano": 0.05}),
    Escudo("Baluarte Inabalável de Aethelgard", "O escudo do rei fundador.", "lendario", 3200, 100, 0.35, 95, bonus_atributo={"vitalidade": 30}, propriedades={"imunidade_a_medo": True, "aura_de_protecao_grupo": 10}),
    
    # Excelência (Nível 100)
    Escudo("Baluarte do Rei Guardião", "Protegeu o último rei de Aethelgard.", "excelencia", 9800, 120, 0.40, 100, bonus_atributo={"vitalidade": 50, "sabedoria": 20}, propriedades={"reducao_dano_recebido_percentual": 0.20, "refletir_dano_percentual": 0.20, "imunidade_debuffs_defensivos": True}),
    Escudo("Paradoxo do Defensor", "Bloqueia um ataque antes de acontecer.", "excelencia", 9500, 100, 0.50, 100, bonus_atributo={"destreza": 40, "inteligencia": 20}, propriedades={"chance_resetar_recarga_habilidade": 0.15, "esquiva_garantida_periodica": 5}),
    Escudo("A Singularidade", "Um buraco negro em miniatura que absorve ataques.", "excelencia", 11000, 80, 0.30, 100, bonus_atributo={"forca": 30, "vitalidade": 30}, propriedades={"absorver_dano_para_liberar": True, "puxao_gravitacional": True}),
]

# CONSUMÍVEIS
todos_consumiveis = [
    Consumivel("Poção de Vida Menor", "Restaura 50 HP.", "normal", 10, quantidade_curar=50, level_req=1),
    Consumivel("Poção de Mana Menor", "Restaura 30 Mana.", "normal", 10, quantidade_restaurar_mana=30, level_req=1),
    Consumivel("Poção de Vida Média", "Restaura 120 HP.", "magica", 25, quantidade_curar=120, level_req=10),
    Consumivel("Poção de Mana Média", "Restaura 70 Mana.", "magica", 25, quantidade_restaurar_mana=70, level_req=10),
    Consumivel("Poção de Vida Forte", "Restaura 300 HP.", "rara", 60, quantidade_curar=300, level_req=30),
    Consumivel("Poção de Mana Forte", "Restaura 180 Mana.", "rara", 60, quantidade_restaurar_mana=180, level_req=30),
    Consumivel("Poção de Vida Épica", "Restaura 800 HP.", "épico", 200, quantidade_curar=800, level_req=50),
    Consumivel("Panaceia Universal", "Remove todos os debuffs e cura um pouco.", "épico", 250, quantidade_curar=200, quantidade_restaurar_mana=100, level_req=40),
]

# FRAGMENTOS LITERÁRIOS (Reordenados e com novas adições)
DADOS_FRAGMENTOS_LITERARIOS = [
    # A Queda de Aethelgard
    FragmentoLiterario("REI_CAIDO_1", "Diário do Rei Caído, p.1", "Primeiro dia do cerco. Os muros de Aethelgard, que julgávamos inexpugnáveis, rangem sob o ataque da Horda. Grond, meu general, diz que a muralha leste não aguentará outra investida. A esperança, como a luz do dia, começa a desvanecer."),
    FragmentoLiterario("REI_CAIDO_2", "Diário do Rei Caído, p.5", "A fome se tornou nossa maior inimiga. Os armazéns estão vazios. Vi crianças roendo couro de armadura. Esta noite, autorizei uma surtida desesperada para buscar suprimentos. Rezo para que não seja a última vez que vejo meus homens."),
    FragmentoLiterario("REI_CAIDO_3", "Diário do Rei Caído, p.12", "Eles romperam a muralha. O som de aço e gritos ecoa pela cidade. Minha guarda real luta bravamente, mas são poucos. Visto minha armadura pela última vez. Não como rei, mas como um soldado de meu povo. Que os deuses tenham piedade de nós."),
    FragmentoLiterario("CODIGO_CAVALEIROS", "O Código dos Cavaleiros da Chama Prateada", "Um cavaleiro não busca glória, mas justiça. Um cavaleiro não teme a morte, mas a desonra. Um cavaleiro protege os fracos, mesmo que o mundo os tenha esquecido. (Uma página encontrada junto ao corpo de um cavaleiro na muralha)."),
    
    # A Corrupção da Masmorra
    FragmentoLiterario("ALQUIMISTA_LOUCO_1", "Notas do Alquimista, frasco 7", "A corrupção do 'Sofrimento Eterno' não é natural. É uma praga alquímica, uma fusão de matéria e desespero. A amostra do limo do Andar 3 reage violentamente ao extrato de Flor Lunar. Há uma fraqueza... preciso de mais flores."),
    FragmentoLiterario("ALQUIMISTA_LOUCO_2", "Notas do Alquimista, frasco 19", "O ar nos andares inferiores... ele respira! É um organismo. A própria masmorra é uma criatura colossal e doente. Os monstros não são invasores, são seus anticorpos, suas células cancerígenas. Eu preciso ir mais fundo."),
    FragmentoLiterario("ALQUIMISTA_LOUCO_3", "Notas do Alquimista, última página", "Encontrei o coração. Lateja com uma luz doentia. A cura... não há cura. Apenas... purificação. O fogo alquímico deve consumir tudo. Adeus, mundo. Que as cinzas sejam mais férteis que a carne."),
    FragmentoLiterario("RELATORIO_BATEDOR", "Relatório de Batedor Élfico", "A corrupção se espalha da masmorra como uma doença. As árvores perto da entrada estão morrendo. A água do rio ficou negra. Precisamos agir antes que a floresta inteira sucumba."),
    FragmentoLiterario("FRAGMENTO_ESPELHO_NEGRO", "Fragmento de Espelho Negro", "Um pequeno pedaço de obsidiana polida. Ao olhar para ele, você não vê seu reflexo, mas sim uma versão distorcida e malévola de si mesmo, sussurrando sobre o poder que a masmorra oferece."),

    # Contos de Aventureiros
    FragmentoLiterario("CARTA_AMOR_SOLDADO", "Carta a Elara", "Meu amor, a cada passo mais fundo nesta masmorra, mais penso em seu rosto. O ouro que busco é para nosso futuro, longe desta escuridão. Se esta carta chegar até você, saiba que lutei pensando em nossos campos ensolarados."),
    FragmentoLiterario("RESPOSTA_ELARA", "Resposta de Elara (nunca enviada)", "Meu querido, não quero o ouro. Quero você. Os campos não têm sol sem seu sorriso. Volte para casa. Por favor, volte."),
    FragmentoLiterario("DIARIO_LADRAO_1", "Diário de 'Sombra'", "Entrei. A segurança é uma piada. Os guardas goblins estão mais interessados em brigar por um osso do que vigiar. O cofre do General Orc deve estar no próximo andar."),
    FragmentoLiterario("DIARIO_LADRAO_2", "Diário de 'Sombra' (última entrada)", "Armadilha. Não era um cofre. Era uma isca. A sala está se fechando. O riso... o riso vem das paredes..."),
    FragmentoLiterario("CONTRATO_MERCENARIO", "Contrato dos Lâminas Cinzentas", "Cláusula 3: Qualquer tesouro de origem 'real' (coroas, cetros, etc.) encontrado no covil do Rei Grak torna-se propriedade exclusiva do contratante. Gemas e ouro serão divididos igualmente."),
    FragmentoLiterario("ADENDO_CONTRATO", "Adendo ao Contrato (manchado de sangue)", "Cláusula 8: Em caso de 'possessão demoníaca' de um membro, a terminação do contrato (e do membro) é imediata e sem compensação adicional."),
    FragmentoLiterario("PEDIDO_SOCORRO_MAGO", "Mensagem Mágica Flutuante", "Estou preso no Laboratório do Arquilich. Ele está usando minha energia para alimentar seus filactérios. A senha para o laboratório é o nome de sua primeira amada. Rápido... minha força se esvai..."),
    FragmentoLiterario("AVISO_AVENTUREIRO", "Nota de um Sobrevivente", "Não confie nas paredes. Não beba a água que escorre. E se ouvir uma canção de ninar, corra. Não lute. Apenas corra."),
    
    # Lendas e Profecias
    FragmentoLiterario("PROFECIA_ESQUECIDA_1", "Fragmento da Profecia de Aethelgard", "Quando a escuridão consumir a montanha e os reis caírem, um herói de fora virá. Não de sangue nobre, mas de coração forjado em batalha..."),
    FragmentoLiterario("PROFECIA_ESQUECIDA_2", "Continuação da Profecia", "...Ele(a) empunhará a luz contra o sofrimento eterno... ou será consumido por ele, tornando-se o novo Rei da Noite."),
    FragmentoLiterario("LENDA_ARQUEIRO_FANTASMA", "O Arqueiro e a Lua de Sangue", "...e dizem que, nas noites de lua de sangue, o espírito de Orion, o Arqueiro, ainda caça nas profundezas, buscando vingança contra a besta que lhe roubou a vida. Suas flechas nunca erram, e carregam o frio da sepultura."),
    FragmentoLiterario("O CONTO DA FÊNIX", "O Conto da Fênix", "A lenda diz que uma armadura forjada nas lágrimas de uma fênix pode trazer seu portador de volta da morte uma única vez. Mas tal poder tem um preço: uma vida pela outra."),

    # Mundo e Cultura
    FragmentoLiterario("RUNA_AVISO_ANAO", "Aviso Rúnico Anão", "A rocha chora. A ganância cavou fundo demais. O que despertamos não dorme mais. Fujam. Selamos o portão, mas por quanto tempo? O ouro daqui é amaldiçoado."),
    FragmentoLiterario("CANCAO_BEBER_ANAO", "Canção de Taverna Anã", "Um gole pela montanha, forte e alta! / Outro pelo ouro que o chão nos dá! / Um terceiro pela barba, que não falha! / E um quarto pra quem na cadeira ainda está!"),
    FragmentoLiterario("GOBLIN_FILOSOFO", "Pensamentos de Grak o Pensador", "Chefe diz: 'Esmague!' Eu pergunto: 'Por quê?' Chefe diz: 'Para pegar brilhantes!' Eu pergunto: 'Por que pegar brilhantes?' Chefe me bateu. Pensar dói mais que porrete."),
    FragmentoLiterario("CONTO_INFANTIL_ORC", "Grunk, o Orc que Queria Plantar Flores", "Grunk não gostava de esmagar. Gostava de flores. Outros orcs riam. Um dia, Grunk encontrou uma semente brilhante. Plantou-a. Nasceu uma planta carnívora gigante que comeu os outros orcs. Grunk ficou com todas as flores para si. Fim."),
    FragmentoLiterario("RECEITA_CURANDEIRA", "Receita de Cataplasma da Bruxa do Pântano", "Folhas de Salgueiro-chorão, moídas. Musgo de Golem adormecido. Duas gotas de veneno de Aranha-de-cristal. Misturar sob a lua nova. Aplique no ferimento. Se o paciente gritar e ficar verde, a dosagem foi excessiva."),
]


# Combinação de todos os itens em uma lista
todos_itens = todas_armas + todas_armaduras + todos_escudos + todos_consumiveis + DADOS_FRAGMENTOS_LITERARIOS

# Pools de drop para monstros, gerados a partir da lista principal
pools_drop_monstro = {
    "normal": [item for item in todos_itens if item.raridade == "normal" and item.tipo_item != 'literario'],
    "magica": [item for item in todos_itens if item.raridade == "magica" and item.tipo_item != 'literario'],
    "rara": [item for item in todos_itens if item.raridade == "rara" and item.tipo_item != 'literario'],
    "épico": [item for item in todos_itens if item.raridade == "épico" and item.tipo_item != 'literario'],
    "lendario": [item for item in todos_itens if item.raridade == "lendario" and item.tipo_item != 'literario'],
    "excelencia": [item for item in todos_itens if item.raridade == "excelencia" and item.tipo_item != 'literario'],
    "literario": [item for item in todos_itens if item.raridade == "literario"],
}