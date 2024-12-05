from datetime import datetime, timedelta
import re
from dados import VEICULOS, TEMPOS_VEICULOS, DIAS_SEMANA, MESES

data_hora_atual = datetime.now()
dia_semana_ptbr = DIAS_SEMANA[data_hora_atual.weekday()]
mes_ptbr = MESES[data_hora_atual.month]
data_ptbr = data_hora_atual.strftime("%d/%m/%Y")
hora_ptbr = data_hora_atual.strftime("%H:%M")


class Veiculo:
    id = 1

    def __init__(self, nome, cpf, email, telefone, categoria, modelo, placa):
        self.id = Veiculo.id
        Veiculo.id += 1
        self.nome = nome
        self.cpf = cpf
        self.email = email
        self.telefone = telefone
        self.categoria = categoria
        self.modelo = modelo
        self.placa = placa

    def exibir_dados(self):
        print(f"\n### Dados do Veículo ###")
        print(f"ID: {self.id}")
        print(
            f"Proprietário: {self.nome} (CPF: {self.cpf}) (Email: {self.email}) (Telefone: {self.telefone})"
        )
        print(f"Categoria: {self.categoria}")
        print(f"Modelo: {self.modelo}")
        print(f"Placa: {self.placa}\n")


class SistemaVeiculos:
    def __init__(self):
        self.veiculos = []

    def validar_cpf(self, cpf):
        return re.match(r"^\d{3}\.\d{3}\.\d{3}-\d{2}$", cpf) is not None

    def obter_cpf(self):
        while True:
            cpf = input("Por favor, insira seu CPF (formato: xxx.xxx.xxx-xx): ").strip()
            if self.validar_cpf(cpf):
                return cpf
            else:
                print("CPF inválido. Certifique-se de que está no formato correto.")

    def validar_email(self, email):
        return re.match(r"[^@]+@[^@]+\.[^@]+", email) is not None

    def obter_email(self):
        while True:
            email = input("Por favor, insira seu email: ").strip()
            if self.validar_email(email):
                return email
            else:
                print("Email inválido. Tente novamente.")

    def validar_telefone(self, telefone):
        return re.match(r"^\(?\d{2}\)?\s?\d{4,5}-\d{4}$", telefone) is not None

    def obter_telefone(self):
        while True:
            telefone = input(
                "Por favor, insira seu telefone (formato: (xx) xxxxx-xxxx ou xxxx-xxxx): "
            ).strip()
            if self.validar_telefone(telefone):
                return telefone
            else:
                print("Telefone inválido. Tente novamente.")

    def validar_placa(self, placa):
        return re.match(r"^[A-Z]{3}-\d{4}$", placa) is not None

    def obter_placa(self):
        while True:
            placa = (
                input("Por favor, insira a placa do veículo (formato: ABC-1234): ")
                .strip()
                .upper()
            )
            if self.validar_placa(placa):
                return placa
            else:
                print("Placa inválida. Tente novamente.")

    def identificar_categoria(self, modelo_parcial):
        """Identifica a categoria de um modelo de veículo baseado em uma busca parcial."""
        modelo_parcial = modelo_parcial.lower()
        for categoria, modelos in VEICULOS.items():
            for modelo in modelos:
                if modelo_parcial in modelo.lower():
                    return categoria, modelo
        return None, None

    def obter_modelo(self):
        """Obtém o modelo do veículo diretamente do usuário."""
        while True:
            modelo_escolhido = (
                input("Digite o nome do modelo do veículo: ").strip().title()
            )
            if modelo_escolhido:
                return modelo_escolhido
            else:
                print("Modelo inválido. Tente novamente.")

    def cadastrar_veiculo(self):
        print("\n### Cadastro de Veículo ###")
        nome = input("Qual o seu nome? ").strip().title()
        cpf = self.obter_cpf()
        email = self.obter_email()
        telefone = self.obter_telefone()

        while True:
            modelo_parcial = self.obter_modelo()
            categoria, modelo_completo = self.identificar_categoria(modelo_parcial)

            if categoria:
                print(f"Modelo encontrado: {modelo_completo} (Categoria: {categoria})")
                break
            else:
                print(
                    "Modelo não encontrado ou inválido. Certifique-se de que está correto ou tente novamente."
                )

        placa = self.obter_placa()

        veiculo = Veiculo(nome, cpf, email, telefone, categoria, modelo_completo, placa)
        self.veiculos.append(veiculo)
        print("\nVeículo cadastrado com sucesso!\n")

    def consultar_veiculo(self):
        placa = self.obter_placa()
        for veiculo in self.veiculos:
            if veiculo.placa == placa:
                return veiculo
        return None

    def listar_veiculos(self):
        if not self.veiculos:
            print("\nNenhum veículo cadastrado.")
        else:
            for veiculo in self.veiculos:
                veiculo.exibir_dados()

    def obter_opcao_lavagem(self):
        while True:
            opcao = input("Deseja lavar o veículo agora? (S/N): ").strip().upper()
            if opcao in ["S", "N"]:
                return opcao == "S"
            print("Opção inválida. Digite 'S' para Sim ou 'N' para Não.")

    def obter_data_hora_lavagem(self):
        while True:
            try:
                data = input(
                    "Digite a data desejada para a lavagem (formato: DD/MM/AAAA): "
                ).strip()
                hora = input(
                    "Digite a hora desejada para a lavagem (formato: HH:MM): "
                ).strip()
                data_hora_str = f"{data} {hora}"
                data_hora = datetime.strptime(data_hora_str, "%d/%m/%Y %H:%M")

                if data_hora < datetime.now():
                    print(
                        "A data e hora informadas devem ser futuras. Tente novamente."
                    )
                else:
                    return data_hora
            except ValueError:
                print(
                    "Formato inválido. Certifique-se de usar o formato DD/MM/AAAA e HH:MM."
                )

    def lavar_veiculo(self, placa):
        for veiculo in self.veiculos:
            if veiculo.placa == placa:
                tipo_veiculo = veiculo.categoria
                if tipo_veiculo is None:
                    print(
                        "A categoria do veículo não foi identificada corretamente. Verifique os dados do cadastro."
                    )
                    return

                lavar_agora = self.obter_opcao_lavagem()

                if lavar_agora:
                    data_hora_inicio = datetime.now()
                else:
                    data_hora_inicio = self.obter_data_hora_lavagem()

                tempo = TEMPOS_VEICULOS[tipo_veiculo]
                data_hora_fim = data_hora_inicio + timedelta(minutes=tempo)

                dia_semana_inicio = DIAS_SEMANA[data_hora_inicio.weekday()]
                dia_semana_fim = DIAS_SEMANA[data_hora_fim.weekday()]

                print(
                    f"O veículo de {veiculo.nome} ({veiculo.modelo}, tipo {tipo_veiculo}) será lavado a partir de: "
                    f"{data_hora_inicio.strftime('%H:%M - %d/%m/%Y')} ({dia_semana_inicio}) "
                    f"e ficará pronto às {data_hora_fim.strftime('%H:%M - %d/%m/%Y')} ({dia_semana_fim}).\n"
                )
                return

        print("Veículo não encontrado. Verifique a placa e tente novamente.")


def menu_principal():
    sistema = SistemaVeiculos()

    while True:
        print(" Bem-vindo ao Sistema Lava Jato ".center(50, "#"))
        print(f"{dia_semana_ptbr} - {data_ptbr} - {hora_ptbr} ")
        print("[1] Cadastrar Veículo")
        print("[2] Consultar Veículo pela Placa")
        print("[3] Listar Todos os Veículos Cadastrados")
        print("[4] Lavar Veículo")
        print("[5] Sair")

        opcao = input("\nEscolha uma opção: ")

        if opcao == "1":
            sistema.cadastrar_veiculo()

        elif opcao == "2":
            veiculo = sistema.consultar_veiculo()
            if veiculo:
                veiculo.exibir_dados()
            else:
                print("Veículo não encontrado.")

        elif opcao == "3":
            sistema.listar_veiculos()

        elif opcao == "4":
            placa = sistema.obter_placa()
            sistema.lavar_veiculo(placa)

        elif opcao == "5":
            print("Saindo do sistema...")
            break

        else:
            print("Opção inválida. Tente novamente.")


if __name__ == "__main__":
    menu_principal()
