import os
import matplotlib.pyplot as plt
from basisfuncties import data_naar_pandas, sorteer_data

new_steam = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'json', 'new_steam.json'))

data = data_naar_pandas(new_steam)
data_gesorteerd = sorteer_data(data, 'average_playtime', False)

x = data_gesorteerd['cijfer']
y = data_gesorteerd['price']

def linear_regression_lsm(x, y):
    #https://www.youtube.com/watch?v=JvS2triCgOY
    x_gemiddelde = sum(x) / len(x)
    y_gemiddelde = sum(y) / len(y)
    teller = 0
    noemer = 0

    for xk, yk in zip(x, y):
        teller += (xk - x_gemiddelde) * (yk - y_gemiddelde)
        noemer += (xk - x_gemiddelde) ** 2

    b1 = teller / noemer
    b0 = y_gemiddelde - b1 * x_gemiddelde

    return b0,b1
def gradient_descent(x, y, num_iterations=1000, learning_rate=0.0001):
    b, a = linear_regression_lsm(x, y)  # b = helling, a = bias

    for iteration in range(num_iterations):
        for xk, yk in zip(x, y):
            error = (a + b * xk) - yk
            a = a - error * learning_rate
            b = b - xk * error * learning_rate

    coefficients = [a, b]
    return coefficients

#zonder gradient descent
coefficients = linear_regression_lsm(x, y)
print(coefficients)
#met gradient descent
coefficients_gradient = gradient_descent(x, y)
print(coefficients_gradient)

print(f'Met een voorspelling game cijfer 6.5 zal de prijs geschat zijn: {coefficients_gradient[0] +coefficients_gradient[1] * 8}')

plt.figure(facecolor='#1b2838')
# Plot van de data en de lineaire regressie
plt.scatter(x, y, color='#354f52', label='Data Punten')
#b0 + b1 * x
plt.plot(x, coefficients[0] + coefficients[1] * x, color='red', label=f'Zonder Gradient Descent \nb0:{coefficients[0]} \nb1:{coefficients[1]}')
plt.plot(x, coefficients_gradient[0] + coefficients_gradient[1] * x, alpha=0.8, color='green', label=f'Met Gradient Descent \nb0:{coefficients_gradient[0]} \nb1:{coefficients_gradient[1]}')
plt.yticks(color="white")
plt.xticks(color="white")
plt.xlabel('Cijfer', color='white')
plt.ylabel('Prijs', color='white')
plt.title("Lineaire regressie en gradient descent", color='white')
plt.legend()
plt.show()

