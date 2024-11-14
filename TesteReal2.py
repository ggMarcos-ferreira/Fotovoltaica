import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import minimize

# Dados reais com parâmetros ajustáveis
radiacao_maxima = 1200  # Intensidade da radiação solar (W/m²)
eficiencia_painel = 0.20  # Eficiência do painel (%)
area_painel = 2.0  # Área do painel (m²)

# Função de radiação solar com base na hora do dia e no ângulo do painel
def rad_solar_real(hora, angulo):
    irradiancia = radiacao_maxima * max(0, np.sin((hora - 6) * np.pi / 12)) * np.cos(np.radians(angulo))
    return irradiancia * eficiencia_painel * area_painel

# Função para calcular a produção total de energia ao longo do dia com um ângulo específico
def energia_total(angulo):
    horarios = np.linspace(0, 24, 100)
    energia = [rad_solar_real(h, angulo[0]) for h in horarios]
    return -np.sum(energia)

# Parâmetros de teste para otimização
parametros_teste = [
    {'x0': [10], 'bounds': [(0, 45)]},
    {'x0': [30], 'bounds': [(10, 80)]},
    {'x0': [60], 'bounds': [(30, 90)]},
    {'x0': [45], 'bounds': [(0, 90)]},
]

# Armazenando os resultados para cada conjunto de parâmetros
resultados = []
for params in parametros_teste:
    resultado = minimize(energia_total, x0=params['x0'], bounds=params['bounds'])
    angulo_otimo = resultado.x[0]
    
    # Cálculo da energia ao longo do dia para o ângulo ótimo
    horarios = np.linspace(0, 24, 100)
    energia_ajustada = [rad_solar_real(h, angulo_otimo) for h in horarios]
    energia_total_dia = np.sum(energia_ajustada) * (24 / 100)  # Energia total diária em Wh
    
    # Armazenando o resultado
    resultados.append({
        'x0': params['x0'],
        'bounds': params['bounds'],
        'angulo_otimo': angulo_otimo,
        'energia_total_dia': energia_total_dia
    })
    
    # Exibindo o gráfico para o ângulo ótimo de cada teste
    plt.figure(figsize=(10, 6))
    plt.plot(horarios, energia_ajustada, label=f'Ângulo Otimizado ({angulo_otimo:.2f}°)')
    plt.title(f'Otimização do Ângulo com x0={params["x0"]} e bounds={params["bounds"]}')
    plt.xlabel('Hora do Dia')
    plt.ylabel('Energia Captada (W)')
    plt.legend()
    plt.grid()
    plt.show()

# Exibindo os resultados para cada teste
for res in resultados:
    print(f"Parâmetros de Teste: x0={res['x0']}, bounds={res['bounds']}")
    print(f"Ângulo Ótimo: {res['angulo_otimo']:.2f}°")
    print(f"Energia Total Captada no Dia: {res['energia_total_dia']:.2f} Wh\n")
