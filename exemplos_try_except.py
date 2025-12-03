# Exemplos de Try/Except em Python


# ------------------------------
# Exemplo 1: Tratando divisão por zero
# ------------------------------
def exemplo_divisao(a, b):
    try:
        resultado = a / b
        return f"Resultado: {resultado}"
    except ZeroDivisionError:
        return "Erro: Divisão por zero não é permitida."

# Testes
print(exemplo_divisao(10, 2))
print(exemplo_divisao(5, 0))


# ------------------------------
# Exemplo 2: Tratando erro de conversão
# ------------------------------
def exemplo_conversao(valor):
    try:
        numero = int(valor)
        return f"Conversão bem-sucedida: {numero}"
    except ValueError:
        return "Erro: Não é possível converter para inteiro."

# Testes
print(exemplo_conversao("25"))
print(exemplo_conversao("abc"))


# ------------------------------
# Exemplo 3: Múltiplos tipos de exceções
# ------------------------------
def exemplo_multiplas_excecoes(lista, indice):
    try:
        return lista[indice]
    except IndexError:
        return "Erro: Índice fora do alcance da lista."
    except TypeError:
        return "Erro: Tipo inválido para acessar índice."

# Testes
print(exemplo_multiplas_excecoes([1, 2, 3], 1))
print(exemplo_multiplas_excecoes([1, 2, 3], 5))
print(exemplo_multiplas_excecoes(123, 1))


# ------------------------------
# Exemplo 4: Finally
# ------------------------------
def exemplo_finally():
    try:
        print("Tentando executar algo...")
        x = 10 / 0
    except ZeroDivisionError:
        print("Peguei o erro!")
    finally:
        print("O bloco 'finally' sempre executa.")

exemplo_finally()


# ------------------------------
# Exemplo 5: Try/Except dentro de loop
# ------------------------------
def exemplo_loop(valores):
    resultados = []
    for v in valores:
        try:
            resultados.append(10 / v)
        except ZeroDivisionError:
            resultados.append("Erro: Zero não permitido.")
    return resultados

# Testes
print(exemplo_loop([5, 2, 0, 1]))


# ------------------------------
# Exemplo 6: Raising Exceptions
# ------------------------------
def exemplo_raise(idade):
    try:
        if idade < 0:
            raise ValueError("Idade não pode ser negativa.")
        return f"Idade válida: {idade}"
    except ValueError as e:
        return f"Erro detectado: {e}"

# Testes
print(exemplo_raise(20))
print(exemplo_raise(-5))
