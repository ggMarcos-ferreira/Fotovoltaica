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

# Otimizando o ângulo para maximizar a produção de energia
resultado = minimize(energia_total, x0=[45], bounds=[(0, 60)])  # Ângulo inicial de 45° e limite de 0° a 60°
angulo_otimo = resultado.x[0]

# Gráfico de energia captada ao longo do dia com ângulo otimizado
horarios = np.linspace(0, 24, 100)
energia_ajustada = [rad_solar_real(h, angulo_otimo) for h in horarios]

plt.figure(figsize=(10, 6))
plt.plot(horarios, energia_ajustada, label=f'Energia com Ângulo Otimizado ({angulo_otimo:.2f}°)', color='b')
plt.title('Otimização do Ângulo dos Painéis Solares com Dados Reais')
plt.xlabel('Hora do Dia')
plt.ylabel('Energia Captada (W)')
plt.legend()
plt.grid()
plt.show()

# Energia total captada no dia (em Wh)
energia_total_dia = np.sum(energia_ajustada) * (24 / 100)
print(f"Energia total captada ao longo do dia com ângulo otimizado: {energia_total_dia:.2f} Wh")
