import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import minimize

# Função de radiação solar com base na hora do dia e no ângulo do painel
def rad_solar(hora, angulo):
    # Modela a radiação com base na hora e no ângulo do painel
    return max(0, np.sin((hora - 6) * np.pi / 12) * np.cos(np.radians(angulo)))

# Função para calcular a produção de energia com um ângulo específico ao longo do dia
def energia_total(angulo):
    horarios = np.linspace(0, 24, 100)
    energia = [rad_solar(h, angulo[0]) for h in horarios]
    return -np.sum(energia)  # Retorna valor negativo para maximização

# Otimização do ângulo
resultado = minimize(energia_total, x0=[30], bounds=[(0, 90)])
angulo_otimo = resultado.x[0]

# Gráfico de energia captada ao longo do dia com ângulo otimizado
horarios = np.linspace(0, 24, 100)
energia_ajustada = [rad_solar(h, angulo_otimo) for h in horarios]

plt.figure(figsize=(10, 6))
plt.plot(horarios, energia_ajustada, label=f'Energia com Ângulo Otimizado ({angulo_otimo:.2f}°)', color='b')
plt.title('Otimização do Ângulo dos Painéis Solares')
plt.xlabel('Hora do Dia')
plt.ylabel('Energia Captada')
plt.legend()
plt.grid()
plt.show()
