import random
import math
from collections import Counter

# =========================
# 1) CONFIGURAÇÃO DO MODELO
# =========================

states = ["A", "B", "C"]

# Proporções iniciais (se você não souber o grupo inicial)
p0 = {"A": 0.3724, "B": 0.4207, "C": 0.2069}

# Matriz de transição (Markov) — você pode ajustar se recalcular a partir de dados reais
T = {
    "A": {"A": 0.3019, "B": 0.5094, "C": 0.1887},
    "B": {"A": 0.4262, "B": 0.3443, "C": 0.2295},
    "C": {"A": 0.4000, "B": 0.4333, "C": 0.1667},
}

# Emissões (valores dentro de cada grupo) — média e desvio
# (esses números foram derivados do ajuste estatístico anterior)
means = {"A": 15.07, "B": 28.94, "C": 39.05}
stds  = {"A": 4.01,  "B": 4.62,  "C": 5.96}

# Limites observados
MIN_VAL, MAX_VAL = 3, 54

# Faixas "fortes" (para filtrar mais): restringe busca do próximo valor por grupo
# Você pode apertar (ex.: usar mean ± 1.0*std em vez de 1.5*std)
SIGMA_CUT = 1.25

# =========================
# 2) FUNÇÕES AUXILIARES
# =========================

def classify_value(v):
    """Classificação simples (mesma ideia dos 3 clusters)."""
    if v <= 21:
        return "A"
    elif v <= 35:
        return "B"
    else:
        return "C"

def gaussian_pdf(x, mu, sigma):
    """Densidade normal (usada como peso relativo)."""
    if sigma <= 0:
        return 0.0
    z = (x - mu) / sigma
    return math.exp(-0.5 * z * z) / (sigma * math.sqrt(2 * math.pi))

def candidate_values_for_group(g):
    """Gera candidatos inteiros mais prováveis dentro do grupo g, com filtro por sigma."""
    mu = means[g]
    sd = stds[g]
    lo = max(MIN_VAL, int(math.floor(mu - SIGMA_CUT * sd)))
    hi = min(MAX_VAL, int(math.ceil(mu + SIGMA_CUT * sd)))
    # reforça cortes por grupo (evita valores fora do regime)
    if g == "A":
        hi = min(hi, 21)
    elif g == "B":
        lo = max(lo, 22)
        hi = min(hi, 35)
    else:
        lo = max(lo, 36)
    return list(range(lo, hi + 1))

def next_value_topN(last_value=None, last_group=None, topN=10):
    """
    Retorna os TOP-N próximos valores inteiros mais prováveis.
    Você pode informar last_value OU last_group.
    """
    if last_group is None:
        if last_value is None:
            # se não sabe nada, assume mistura inicial
            last_group = max(p0, key=p0.get)
        else:
            last_group = classify_value(last_value)

    scored = []
    # 1) escolhe próximo grupo com probabilidade T[last_group][g2]
    for g2 in states:
        p_group = T[last_group][g2]
        # 2) dentro do grupo, escolhe valores mais prováveis pela normal
        for v in candidate_values_for_group(g2):
            p_emit = gaussian_pdf(v, means[g2], stds[g2])
            score = p_group * p_emit
            scored.append((score, g2, v))

    scored.sort(reverse=True, key=lambda x: x[0])
    # normaliza scores para virar "probabilidade relativa"
    total = sum(s for s,_,_ in scored[:topN])
    out = []
    for s, g2, v in scored[:topN]:
        out.append({"valor": v, "grupo": g2, "peso_relativo": (s / total) if total > 0 else 0.0})
    return out

def beam_search_next_sequences(last_value, steps=5, beam_width=10):
    """
    Gera as sequências mais prováveis (TOP) para os próximos 'steps' passos.
    Beam search reduz MUITO a quantidade de opções e mantém as mais prováveis.
    """
    start_g = classify_value(last_value)
    # cada item: (logp, last_group, seq_values, seq_groups)
    beam = [(0.0, start_g, [], [])]

    for _ in range(steps):
        new_beam = []
        for logp, g_prev, seqv, seqg in beam:
            for g2 in states:
                p_group = T[g_prev][g2]
                if p_group <= 0:
                    continue
                # candidatos filtrados
                for v in candidate_values_for_group(g2):
                    p_emit = gaussian_pdf(v, means[g2], stds[g2])
                    if p_emit <= 0:
                        continue
                    new_logp = logp + math.log(p_group) + math.log(p_emit)
                    new_beam.append((new_logp, g2, seqv + [v], seqg + [g2]))

        new_beam.sort(reverse=True, key=lambda x: x[0])
        beam = new_beam[:beam_width]

    # formata
    results = []
    for logp, g_last, seqv, seqg in beam:
        results.append({"log_score": logp, "grupos": "".join(seqg), "valores": seqv})
    return results

# =========================
# 3) EXEMPLOS (RODANDO)
# =========================
if __name__ == "__main__":
    # Exemplo 1: dado o último valor observado, sugere TOP-10 próximos valores
    last = 37
    print("TOP próximos valores (dado last=37):")
    for item in next_value_topN(last_value=last, topN=10):
        print(item)

    # Exemplo 2: melhores sequências para os próximos 5 passos
    print("\nTOP sequências (5 passos, beam=10) dado last=37:")
    best = beam_search_next_sequences(last_value=last, steps=5, beam_width=10)
    for r in best[:5]:
        print(r)
