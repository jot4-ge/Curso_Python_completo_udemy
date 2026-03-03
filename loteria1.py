import random
import math
from collections import Counter

# =========================
# 1) CONFIGURAÇÃO DO MODELO (NOVA COLUNA)
# =========================

states = ["A", "B", "C"]

# Proporções observadas nesta nova coluna
p0 = {"A": 0.468966, "B": 0.427586, "C": 0.103448}

# Matriz de transição (Markov) estimada nesta nova coluna
T = {
    "A": {"A": 0.522388, "B": 0.417910, "C": 0.059701},
    "B": {"A": 0.419355, "B": 0.451613, "C": 0.129032},
    "C": {"A": 0.400000, "B": 0.400000, "C": 0.200000},
}

# Emissões (valores dentro de cada grupo) — média e desvio estimados (GMM)
means = {"A": 3.092370, "B": 9.661119, "C": 20.386822}
stds  = {"A": 1.693370, "B": 3.098675, "C": 6.368373}

# Limites observados na nova coluna
MIN_VAL, MAX_VAL = 1, 33

# Quanto menor, mais "filtrado"
SIGMA_CUT = 1.25

# =========================
# 2) FUNÇÕES AUXILIARES
# =========================

def classify_value(v):
    """Classificação (nova coluna): A=1..5, B=6..15, C=16..33."""
    if v <= 5:
        return "A"
    elif v <= 15:
        return "B"
    else:
        return "C"

def gaussian_pdf(x, mu, sigma):
    """Densidade normal (peso relativo)."""
    if sigma <= 0:
        return 0.0
    z = (x - mu) / sigma
    return math.exp(-0.5 * z * z) / (sigma * math.sqrt(2 * math.pi))

def candidate_values_for_group(g):
    """Candidatos mais prováveis dentro do grupo g, filtrados por sigma e pelos limites do grupo."""
    mu = means[g]
    sd = stds[g]

    lo = max(MIN_VAL, int(math.floor(mu - SIGMA_CUT * sd)))
    hi = min(MAX_VAL, int(math.ceil(mu + SIGMA_CUT * sd)))

    # reforça cortes por grupo
    if g == "A":
        lo = max(lo, 1)
        hi = min(hi, 5)
    elif g == "B":
        lo = max(lo, 6)
        hi = min(hi, 15)
    else:
        lo = max(lo, 16)
        hi = min(hi, 33)

    return list(range(lo, hi + 1))

def next_value_topN(last_value=None, last_group=None, topN=10):
    """
    Retorna TOP-N próximos valores inteiros mais prováveis.
    Você pode informar last_value OU last_group.
    """
    if last_group is None:
        if last_value is None:
            last_group = max(p0, key=p0.get)
        else:
            last_group = classify_value(last_value)

    scored = []
    for g2 in states:
        p_group = T[last_group][g2]
        for v in candidate_values_for_group(g2):
            p_emit = gaussian_pdf(v, means[g2], stds[g2])
            score = p_group * p_emit
            scored.append((score, g2, v))

    scored.sort(reverse=True, key=lambda x: x[0])

    total = sum(s for s, _, _ in scored[:topN])
    out = []
    for s, g2, v in scored[:topN]:
        out.append({"valor": v, "grupo": g2, "peso_relativo": (s / total) if total > 0 else 0.0})
    return out

def beam_search_next_sequences(last_value, steps=5, beam_width=10):
    """
    Gera as sequências mais prováveis para os próximos 'steps' passos (beam search).
    """
    start_g = classify_value(last_value)
    beam = [(0.0, start_g, [], [])]  # (logp, last_group, seq_values, seq_groups)

    for _ in range(steps):
        new_beam = []
        for logp, g_prev, seqv, seqg in beam:
            for g2 in states:
                p_group = T[g_prev][g2]
                if p_group <= 0:
                    continue
                for v in candidate_values_for_group(g2):
                    p_emit = gaussian_pdf(v, means[g2], stds[g2])
                    if p_emit <= 0:
                        continue
                    new_logp = logp + math.log(p_group) + math.log(p_emit)
                    new_beam.append((new_logp, g2, seqv + [v], seqg + [g2]))

        new_beam.sort(reverse=True, key=lambda x: x[0])
        beam = new_beam[:beam_width]

    results = []
    for logp, g_last, seqv, seqg in beam:
        results.append({"log_score": logp, "grupos": "".join(seqg), "valores": seqv})
    return results

# =========================
# 3) EXEMPLO (RODANDO)
# =========================
if __name__ == "__main__":
    last = 1  # <- se quiser testar outro "último valor", altere aqui
    print(f"TOP próximos valores (dado last={last}):")
    for item in next_value_topN(last_value=last, topN=10):
        print(item)

    print(f"\nTOP sequências (5 passos, beam=10) dado last={last}:")
    best = beam_search_next_sequences(last_value=last, steps=5, beam_width=10)
    for r in best[:5]:
        print(r)
