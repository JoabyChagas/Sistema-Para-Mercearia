from model import *
from dao import *
from datetime import datetime


class ControllerCategoria:
    def cadastrarCategoria(self, novaCategoria):
        existe = False
        x = DaoCategorias.ler()
        for i in x:
            if i.categoria == novaCategoria:
                existe = True

        if not existe:
            DaoCategorias.salvar(novaCategoria)
            print('Categoria cadastrada com sucesso.')

        else:
            print('A categoria que deseja cadastrar já existe')

    def removerCategoria(self, categoriaRemover):
        x = DaoCategorias.ler()
        cat = list(filter(lambda x: x.categoria == categoriaRemover, x))

        if len(cat) <= 0:
            print('A categoria que deseja remover não existe')
        else:
            for i in range(len(x)):
                if x[i].categoria == categoriaRemover:
                    del x[i]
                    break
            print('Categoria removida com sucesso')

            with open('categorias.txt', 'w') as arq:
                for i in x:
                    arq.writelines(i.categoria)
                    arq.writelines('\n')

        estoque = DaoEstoque.ler()

        estoque = list(map(lambda x: Estoque(Produtos(x.produto.nome, x.produto.preco, 'Sem Categoria'), x.quantidade) 
                           if(x.produto.categoria == categoriaRemover) else(x), estoque))
        with open('estoque.txt', 'w') as arq:
            for i in estoque:
                arq.writelines(i.produto.nome + '|' + i.produto.preco + '|' + i.produto.categoria + '|' + str(i.quantidade))
                arq.writelines('\n')

    def alterarCategoria(self, categoriaAlterar, categoriaAlterada):
        x = DaoCategorias.ler()

        cat = list(filter(lambda x: x.categoria == categoriaAlterar, x))

        if len(cat) > 0:
            cat1 = list(filter(lambda x: x.categoria == categoriaAlterada, x))
            if len(cat1) == 0:
                x = list(map(lambda x: Categorias(categoriaAlterada)
                         if (x.categoria == categoriaAlterar) else (x), x))
                print('A alteração foi efetuada com sucesso')

                estoque = DaoEstoque.ler()

                estoque = list(map(lambda x: Estoque(Produtos(x.produto.nome, x.produto.preco, categoriaAlterada), x.quantidade) 
                                   if(x.produto.categoria == categoriaAlterar) else(x), estoque))
                with open('estoque.txt', 'w') as arq:
                    for i in estoque:
                        arq.writelines(i.produto.nome + '|' + i.produto.preco + '|' + i.produto.categoria + '|' + str(i.quantidade))
                        arq.writelines('\n')

            else:
                print('A categoria para qual deseja alterar já existe')

        else:
            print('A categoria para qual deseja alterar não existe')

        with open('categorias.txt', 'w') as arq:
            for i in x:
                arq.writelines(i.categoria)
                arq.writelines('\n')

    def mostrarCategoria(self):
        categorias = DaoCategorias.ler()
        if len(categorias) == 0:
            print('Categoria vazia!')
        else:
            for i in categorias:
                print(f'Categoria: {i.categoria}')


class ControllerEstoque:
    def cadastrarProduto(self, nome, preco, categoria, quantidade):
        x = DaoEstoque.ler()
        y = DaoCategorias.ler()
        h = list(filter(lambda x: x.categoria == categoria, y))
        est = list(filter(lambda x: x.produto.nome == nome, x))

        if len(h) > 0:
            if len(est) == 0:
                produto = Produtos(nome, preco, categoria)
                DaoEstoque.salvar(produto, quantidade)
                print('Produto cadastrado com sucesso')
            else:
                print('Produto já existe em estoque')
        else:
            print('Categoria inexistente')

    def removerProduto(self, nome):
        x = DaoEstoque.ler()
        est = list(filter(lambda x: x.produto.nome == nome, x))
        if len(est) > 0:
            for i in range(len(x) - 1, -1, -1):
                if x[i].produto.nome == nome:
                    del x[i]
                    break
            print('produto removido com sucesso')

        else:
            print('O produto que deseja remover não existe')

        with open('estoque.txt', 'w') as arq:
            for i in x:
                arq.writelines(i.produto.nome + '|' + i.produto.preco +
                               '|' + i.produto.categoria + '|' + str(i.quantidade))
                arq.writelines('\n')

    def alterarProduto(self, nomeAlterar, novoNome, novoPreço, novaCategoria, novaQuantidade):
        x = DaoEstoque.ler()
        y = DaoCategorias.ler()
        h = list(filter(lambda x: x.categoria == novaCategoria, y))
        if len(h) > 0:
            est = list(filter(lambda x: x.produto.nome == nomeAlterar, x))
            if len(est) > 0:
                est = list(filter(lambda x: x.produto.nome == novoNome, x))
                if len(est) == 0:
                    x = list(map(lambda x: Estoque(Produtos(novoNome, novoPreço, novaCategoria), novaQuantidade) if (
                        x.produto.nome == nomeAlterar) else (x), x))
                    print('Produto alterado com sucesso')

                else:
                    print('Produto já cadastrado')
            else:
                print('O produto que deseja alterar não existe')

            with open('estoque.txt', 'w') as arq:
                for i in x:
                    arq.writelines(i.produto.nome + '|' + i.produto.preco + '|' +
                                   i.produto.categoria + '|' + str(i.quantidade))
                    arq.writelines('\n')
        else:
            print('A categoria não existe')

    def mostrarEstoque(self):
        estoque = DaoEstoque.ler()
        if len(estoque) == 0:
            print('Categoria vazia!')
        else:
            print('==========Produtos==========')
            for i in estoque:
                print('\n',
                      f'Nome: {i.produto.nome}\n',
                      f'Preço: {i.produto.preco}\n',
                      f'Categoria: {i.produto.categoria}\n',
                      f'Quantidade: {i.quantidade}')
                print('----------------------------')


class ControllerVenda:
    def cadastrarVenda(self, nomeProduto, vendedor, comprador, quantidadeVendida):
        x = DaoEstoque.ler()
        temp = []
        existe = False
        quantidade = False

        for i in x:
            if existe == False:
                if i.produto.nome == nomeProduto:
                    existe = True
                    if i.quantidade >= quantidadeVendida:
                        quantidade = True
                        i.quantidade = int(i.quantidade) - \
                            int(quantidadeVendida)

                        vendido = Venda(Produtos(i.produto.nome, i.produto.preco, i.produto.categoria),
                                        vendedor, comprador, quantidadeVendida)
                        valorCompra = int(quantidadeVendida) * \
                            int(i.produto.preco)

                        DaoVenda.salvar(vendido)
            temp.append([Produtos(i.produto.nome, i.produto.preco,
                        i.produto.categoria), i.quantidade])

        arq = open('estoque.txt', 'w')
        arq.write('')

        for i in temp:
            with open('estoque.txt', 'a') as arq:
                arq.writelines(i[0].nome + '|' + i[0].preco + '|' +
                               i[0].categoria + '|' + str(i[1]))
                arq.writelines('\n')

        if existe == False:
            print('O produto não existe')
            return None
        elif not quantidade:
            print('A quantidade vendida não existe em estoque')
            return None
        else:
            print('Venda realizada com sucesso!')
            return valorCompra

    def mostrarVenda(self, dataInicio, dataTermino):
        vendas = DaoVenda.ler()
        dataInicio1 = datetime.strptime(dataInicio, "%d/%m/%Y")
        dataTermino1 = datetime.strptime(dataTermino, "%d/%m/%Y")

        vendasSelecionadas = list(filter(lambda x: datetime.strptime(x.data, "%d/%m/%Y") >= dataInicio1
                                         and datetime.strptime(x.data, "%d/%m/%Y") <= dataTermino1, vendas))

        cont = 1
        total = 0
        for i in vendasSelecionadas:
            print(f'==========Produtos[{cont}]==========')
            print(f'Nome: {i.itensVendido.nome}\n'
                  f'Categoria: {i.itensVendido.categoria}\n'
                  f'Data: {i.data}\n'
                  f'Quantidade: {i.quantidadeVendida}\n'
                  f'Cliente: {i.comprador}\n'
                  f'Vendedor: {i.vendedor}\n')
            total += int(i.itensVendido.preco) * int(i.quantidadeVendida)
            cont += 1
        print(f'Total vendido: {total}')

    def relatorioVendas(self):
        vendas = DaoVenda.ler()
        produtos = []
        for i in vendas:
            nome = i.itensVendido.nome
            quantidade = i.quantidadeVendida
            tamanho = list(filter(lambda x: x['produto'] == nome, produtos))
            if len(tamanho) > 0:
                produtos = list(map(lambda x: {'produto': nome, 'quantidade': int(x['quantidade']) + int(quantidade)}
                                    if (x['produto'] == nome) else (x), produtos))
            else:
                produtos.append(
                    {'produto': nome, 'quantidade': int(quantidade)})
        ordenado = sorted(
            produtos, key=lambda k: k['quantidade'], reverse=True)

        print('Esses são os produtos mais vendidos')
        a = 1
        for i in ordenado:
            print(f'==========Produtos[{a}]==========')
            print(f'Produto: {i["produto"]}\n'
                  f'Quantidade: {i["quantidade"]}\n')
            a += 1


class ControllerFornecedor:
    def cadastrarFornecedor(self, nome, cnpj, telefone, categoria):
        x = DaoFornecedor.ler()
        filtroCnpj = list(filter(lambda x: x.cnpj == cnpj, x))
        filtroTelefone = list(filter(lambda x: x.telefone == telefone, x))
        if len(filtroCnpj) > 0:
            print('O cnpj já existe')
        elif len(filtroTelefone) > 0:
            print('O telefone já existe')
        else:
            if len(cnpj) == 14 and len(telefone) <= 11 and len(telefone) >= 10:
                DaoFornecedor.salvar(Fornecedor(
                    nome, cnpj, telefone, categoria))
                print('Fornecedor cadastrado com sucesso.')
            else:
                print('Digite um cnpj ou telefone válido.')

    def alterarFornecedor(self, nomeAlterar, novoNome, novoCnpj, novoTelefone, novoCategoria):
        x = DaoFornecedor.ler()

        validarNome = list(filter(lambda x: x.nome == nomeAlterar, x))
        if len(validarNome) > 0:
            validarCnpj = list(filter(lambda x: x.cnpj == novoCnpj, x))
            if len(validarCnpj) == 0:
                x = list(map(lambda x: Fornecedor(novoNome, novoCnpj, novoTelefone,
                         novoCategoria) if (x.nome == nomeAlterar) else (x), x))

                with open('fornecedores.txt', 'w') as arq:
                    for i in x:
                        arq.writelines(i.nome + '|' + i.cnpj +
                                       '|' + i.telefone + '|' + str(i.categoria))
                        arq.writelines('\n')
                print('Fornecedor alterado com sucesso.')

            else:
                print('Cnpj já existe.')
        else:
            print('O fornecedor que deseja alterar não existe.')

    def removerFornecedor(self, nome):
        fornecedores = DaoFornecedor.ler()
        validarForn = list(filter(lambda x: x.nome == nome, fornecedores))
        if len(validarForn) > 0:
            for i in range(len(fornecedores) - 1, -1, -1):
                if fornecedores[i].nome == nome:
                    del fornecedores[i]
                    break
            print('Fornecedor removido com sucesso.')

        else:
            print('O fornecedor não existe.')

        with open('fornecedores.txt', 'w') as arq:
            for i in fornecedores:
                arq.writelines(i.nome + '|' + i.cnpj + '|' +
                               i.telefone + '|' + str(i.categoria))
                arq.writelines('\n')

    def mostrarFornecedores(self):
        fornecedores = DaoFornecedor.ler()
        if len(fornecedores) == 0:
            print('Nenhum fornecedor cadastrado.')
        else:
            print('==========Fornecedores==========')
            for fornecedor in fornecedores:
                print(f'Nome: {fornecedor.nome}\n'
                      f'CNPJ: {fornecedor.cnpj}\n'
                      f'Telefone: {fornecedor.telefone}\n'
                      f'Categoria: {fornecedor.categoria}\n'
                      '--------------------------------')


class ControllerCliente:
    def cadastrarCliente(self, nome, telefone, cpf, email, endereco):
        clientes = DaoPessoa.ler()
        filtrarCpf = list(
            filter(lambda clientes: clientes.cpf == cpf, clientes))
        filtrarTelefone = list(
            filter(lambda clientes: clientes.telefone == telefone, clientes))
        if len(filtrarCpf) > 0:
            print('Cpf já cadastrado no sistema.')
        elif len(filtrarTelefone) > 0:
            print('Telefone já está cadastrado no sistema.')
        else:
            if len(cpf) == 11 and len(telefone) <= 11 and len(telefone) >= 10:
                DaoPessoa.salvar(Pessoa(nome, telefone, cpf, email, endereco))
                print('Cliente cadastrado com sucesso.')
            else:
                print('Cpf ou Telefone invalido.')

    def removerCliente(self, nome):
        clientes = DaoPessoa.ler()
        filtroNome = list(filter(lambda x: x.nome == nome, clientes))
        if len(filtroNome) > 0:
            for i in range(len(clientes)):
                if clientes[i].nome == nome:
                    del clientes[i]
                    break
            print('Cliente removido com sucesso.')
        else:
            print('O cliente que deseja remover não existe.')

        with open('clientes.txt',  'w') as arq:
            for i in clientes:
                arq.writelines(i.nome + '|' + i.telefone + '|' +
                               i.cpf + '|' + i.email + '|' + i.endereco)
                arq.writelines('\n')

    def alterarCliente(self, nomeAlterar, novoNome, novoTelefone, novoCpf, novoEmail, novoEndereco):
        clientes = DaoPessoa.ler()

        validarNome = list(filter(lambda x: x.nome == nomeAlterar, clientes))
        if len(validarNome) > 0:
            if len(novoCpf) == 11:
                x = list(map(lambda x: Pessoa(novoNome, novoTelefone, novoCpf, novoEmail, novoEndereco) if (
                    x.nome == nomeAlterar) else (x), clientes))

                with open('clientes.txt', 'w') as arq:
                    for i in x:
                        arq.writelines(
                            i.nome + '|' + i.telefone + '|' + i.cpf + '|' + i.email + '|' + i.endereco)
                        arq.writelines('\n')
                print('Cliente alterado com sucesso.')
            else:
                print('O CPF digitado não é valido.')
        else:
            print('O cliente que deseja alterar não existe.')

    def mostrarClientes(self):
        clientes = DaoPessoa.ler()
        if len(clientes) == 0:
            print('Nenhum cliente cadastrado.')
        else:
            print('==========Clientes==========')
            for cliente in clientes:
                print(f'Nome: {cliente.nome}\n'
                      f'Telefone: {cliente.telefone}\n'
                      f'CPF: {cliente.cpf}\n'
                      f'E-mail: {cliente.email}\n'
                      f'Endereço: {cliente.endereco}\n'
                      '--------------------------------')


class ControllerFuncionario:
    def cadastrarFuncionario(self, clt, nome, telefone, cpf, email, endereco):
        funcionarios = DaoFuncionario.ler()
        filtrarCpf = list(
            filter(lambda clientes: clientes.cpf == cpf, funcionarios))
        filtrarClt = list(
            filter(lambda clientes: clientes.clt == clt, funcionarios))
        if len(filtrarCpf) > 0:
            print('Cpf já cadastrado no sistema.')
        elif len(filtrarClt) > 0:
            print('clt já está cadastrado no sistema.')
        else:
            if len(cpf) == 11 and len(telefone) <= 11 and len(telefone) >= 10:
                DaoFuncionario.salvar(Funcionario(
                    clt, nome, telefone, cpf, email, endereco))
                print('Cliente cadastrado com sucesso.')
            else:
                print('Cpf ou Telefone invalido.')

    def removerFuncionario(self, clt):
        funcionarios = DaoFuncionario.ler()
        filtroClt = list(filter(lambda x: x.clt == clt, funcionarios))
        if len(filtroClt) > 0:
            for i in range(len(funcionarios)):
                if funcionarios[i].clt == clt:
                    del funcionarios[i]
                    break
            print('funcionario removido com sucesso.')
        else:
            print('A CLT do funcionario que deseja remover não existe.')

        with open('funcionarios.txt',  'w') as arq:
            for i in funcionarios:
                arq.writelines(i.clt + '|' + i.nome + '|' + i.telefone +
                               '|' + i.cpf + '|' + i.email + '|' + i.endereco)
                arq.writelines('\n')

    def alterarFuncionario(self, nomeAlterar, novaClt, novoNome, novoTelefone, novoCpf, novoEmail, novoEndereco):
        funcionarios = DaoFuncionario.ler()

        validarNome = list(
            filter(lambda x: x.nome == nomeAlterar, funcionarios))
        if len(validarNome) > 0:
            if len(novoCpf) == 11:
                x = list(map(lambda x: Funcionario(novaClt, novoNome, novoTelefone, novoCpf,
                         novoEmail, novoEndereco) if (x.nome == nomeAlterar) else (x), funcionarios))

                with open('funcionarios.txt', 'w') as arq:
                    for i in x:
                        arq.writelines(i.clt + '|' + i.nome + '|' + i.telefone +
                                       '|' + i.cpf + '|' + i.email + '|' + i.endereco)
                        arq.writelines('\n')
                print('Funcionario alterado com sucesso.')
            else:
                print('O CPF digitado não é valido.')
        else:
            print('O Funcionario que deseja alterar não existe.')

    def mostrarFuncionarios(self):
        funcionarios = DaoFuncionario.ler()
        if len(funcionarios) == 0:
            print('Nenhum funcionário cadastrado.')
        else:
            print('==========Funcionários==========')
            for funcionario in funcionarios:
                print(f'Clt: {funcionario.clt}\n'
                      f'Nome: {funcionario.nome}\n'
                      f'Telefone: {funcionario.telefone}\n'
                      f'CPF: {funcionario.cpf}\n'
                      f'E-mail: {funcionario.email}\n'
                      f'Endereço: {funcionario.endereco}\n'
                      '--------------------------------')